"""Búsqueda híbrida: BM25 (léxica) + embeddings (semántica), fusionadas con Reciprocal Rank Fusion.

BM25 acierta con nombres exactos («isinstance», «__init__», «KeyError»); los embeddings, con preguntas
dichas con otras palabras («¿cómo repito algo hasta que el usuario acierte?» -> bucle while). La fusión
RRF combina las dos listas por posición, sin tener que igualar escalas de puntuación. Sin clave de API
el buscador funciona solo con BM25.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from .bm25 import BM25
from .embeddings import Embedder, coseno
from .trocear import Fragmento

RRF_K = 60
CANDIDATOS = 30


@dataclass(frozen=True)
class Resultado:
    fragmento: Fragmento
    puntuacion: float
    origen: str  # "bm25", "semantica" o "ambas"


def texto_indexable(f: Fragmento) -> str:
    """La ruta pesa: «Strings en profundidad › Métodos de string» describe muy bien el fragmento."""
    return f"{f.ruta}\n{f.ruta}\n{f.texto}"


class Buscador:
    def __init__(self, fragmentos: Sequence[Fragmento], embedder: Embedder | None = None) -> None:
        self.fragmentos = list(fragmentos)
        textos = [texto_indexable(f) for f in self.fragmentos]
        self.bm25 = BM25(textos)
        self.embedder = embedder
        self.vectores = embedder.documentos(textos) if embedder else None

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
        return sorted(range(len(puntos)), key=lambda i: puntos[i], reverse=True)[:k]

    def buscar(self, consulta: str, k: int = 5) -> list[Resultado]:
        lexica = [i for i, _ in self.bm25.buscar(consulta, CANDIDATOS)]
        semantica = self._semantica(consulta, CANDIDATOS)
        puntos: dict[int, float] = {}
        origen: dict[int, set[str]] = {}
        for nombre, lista in (("bm25", lexica), ("semantica", semantica)):
            for posicion, i in enumerate(lista):
                puntos[i] = puntos.get(i, 0.0) + 1.0 / (RRF_K + posicion + 1)
                origen.setdefault(i, set()).add(nombre)
        orden = sorted(puntos, key=lambda i: puntos[i], reverse=True)[:k]
        return [
            Resultado(self.fragmentos[i], puntos[i], "ambas" if len(origen[i]) == 2 else next(iter(origen[i])))
            for i in orden
        ]
