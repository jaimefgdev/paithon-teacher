"""Búsqueda híbrida: BM25 (léxica) + embeddings (semántica), fusionadas con Reciprocal Rank Fusion.

BM25 acierta con nombres exactos («isinstance», «__init__», «KeyError»); los embeddings, con preguntas
dichas con otras palabras («¿cómo repito algo hasta que el usuario acierte?» -> bucle while). La fusión
RRF combina las dos listas por posición, sin tener que igualar escalas de puntuación. Sin clave de API
el buscador funciona solo con BM25.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol

from .bm25 import BM25
from .embeddings import Embedder, coseno
from .trocear import Fragmento

RRF_K = 10  # elegido con las preguntas de evaluación (desarrollo): premia más los primeros puestos
CANDIDATOS = 50
PESOS = {"bm25": 1.0, "semantica": 1.0}  # cuánto cuenta cada lista en la fusión
A_REORDENAR = 20  # los primeros de la fusión que el reordenador vuelve a puntuar


class Reordenador(Protocol):
    """Puntúa la relevancia de cada texto para la consulta leyendo los dos juntos (cross-encoder)."""

    nombre: str

    def puntuar(self, consulta: str, textos: Sequence[str]) -> list[float]: ...


@dataclass(frozen=True)
class Resultado:
    fragmento: Fragmento
    puntuacion: float
    origen: str  # "bm25", "semantica" o "ambas"


def texto_indexable(f: Fragmento, preguntas: Sequence[str] = ()) -> str:
    """La ruta pesa: «Strings en profundidad › Métodos de string» describe muy bien el fragmento. Las preguntas de
    ejemplo (preguntas.py) añaden cómo lo preguntaría un alumno."""
    return "\n".join([f.ruta, f.ruta, *preguntas, f.texto])


class Buscador:
    def __init__(
        self,
        fragmentos: Sequence[Fragmento],
        embedder: Embedder | None = None,
        preguntas: Mapping[str, Sequence[str]] | None = None,
        reordenador: Reordenador | None = None,
    ) -> None:
        self.fragmentos = list(fragmentos)
        preguntas = preguntas or {}
        self.reordenador = reordenador
        # Lo que lee el reordenador: dónde está el fragmento y su texto (sin las preguntas de ejemplo).
        self.textos_reordenar = [(f.ruta + "\n" + f.texto)[:2000] for f in self.fragmentos]
        textos = [texto_indexable(f, preguntas.get(f.id, ())) for f in self.fragmentos]
        self.bm25 = BM25(textos)
        self.embedder = embedder
        self.aviso = ""
        self.vectores: list[list[float]] | None = None
        # Cada pregunta de ejemplo con su propio vector: una pregunta corta del alumno se parece mucho más a otra
        # pregunta corta que a un apartado largo. Se embebe como consulta (mismo tipo de texto que la del alumno).
        self.dueños: list[int] = []
        self.vectores_preguntas: list[list[float]] = []
        if not embedder:
            return
        try:
            self.vectores = embedder.documentos(textos)
        except OSError as e:  # sin cuota o sin red al arrancar: se busca solo con BM25, sin caerse
            self.embedder, self.aviso = None, f"embeddings no disponibles ({e})"
            return
        pares = [(i, q) for i, f in enumerate(self.fragmentos) for q in preguntas.get(f.id, ())]
        if pares:
            embeber = getattr(embedder, "consultas", embedder.documentos)
            try:
                self.vectores_preguntas = embeber([q for _, q in pares])
                self.dueños = [i for i, _ in pares]
            except OSError as e:  # los vectores de los fragmentos sí están: se sigue sin los de las preguntas
                self.aviso = f"vectores de las preguntas de ejemplo no disponibles ({e})"

    @property
    def modo(self) -> str:
        return f"híbrido (BM25 + {self.embedder.nombre})" if self.embedder else "solo BM25"

    def _semantica(self, consulta: str, k: int) -> list[int]:
        if not self.embedder or self.vectores is None:
            return []
        try:
            q = self.embedder.consulta(consulta)
        except OSError:  # la API de embeddings no responde: se sigue solo con BM25
            return []
        puntos = [coseno(q, v) for v in self.vectores]
        for i, v in zip(self.dueños, self.vectores_preguntas, strict=True):
            puntos[i] = max(puntos[i], coseno(q, v))
        return sorted(range(len(puntos)), key=lambda i: puntos[i], reverse=True)[:k]

    def buscar(self, consulta: str, k: int = 5) -> list[Resultado]:
        lexica = [i for i, _ in self.bm25.buscar(consulta, CANDIDATOS)]
        semantica = self._semantica(consulta, CANDIDATOS)
        puntos: dict[int, float] = {}
        origen: dict[int, set[str]] = {}
        for nombre, lista in (("bm25", lexica), ("semantica", semantica)):
            for posicion, i in enumerate(lista):
                puntos[i] = puntos.get(i, 0.0) + PESOS[nombre] / (RRF_K + posicion + 1)
                origen.setdefault(i, set()).add(nombre)
        orden = sorted(puntos, key=lambda i: puntos[i], reverse=True)
        if self.reordenador and orden:
            candidatos = orden[:A_REORDENAR]
            try:
                nuevas = self.reordenador.puntuar(consulta, [self.textos_reordenar[i] for i in candidatos])
                puntos.update(zip(candidatos, nuevas, strict=True))
                orden = sorted(candidatos, key=lambda i: puntos[i], reverse=True)
            except (OSError, RuntimeError):  # si el reordenador falla, vale el orden de la fusión
                pass
        orden = orden[:k]
        return [
            Resultado(self.fragmentos[i], puntos[i], "ambas" if len(origen[i]) > 1 else next(iter(origen[i])))
            for i in orden
        ]
