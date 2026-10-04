"""Evaluación de la recuperación: ¿aparece el apartado correcto entre los k primeros?

Cada línea de evals/preguntas.jsonl es {"pregunta": ..., "esperado": [...]}, donde `esperado` son trozos
de ruta («Diccionarios», «Manejo de errores › Excepciones personalizadas»). Se acierta si alguno de los
k fragmentos recuperados contiene en su ruta alguno de los trozos esperados (sin distinguir mayúsculas).
Se mide recall@k y MRR (posición media del primer acierto).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .buscador import Buscador
from .montaje import RAIZ


@dataclass
class Caso:
    pregunta: str
    esperado: list[str]
    posicion: int | None = None  # 1..k, o None si falla
    obtenido: list[str] = field(default_factory=list)


@dataclass
class Resumen:
    modo: str
    k: int
    casos: list[Caso]

    @property
    def recall(self) -> float:
        return sum(c.posicion is not None for c in self.casos) / max(len(self.casos), 1)

    @property
    def mrr(self) -> float:
        return sum(1 / c.posicion for c in self.casos if c.posicion) / max(len(self.casos), 1)


def cargar(ruta: Path) -> list[Caso]:
    casos = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            d = json.loads(linea)
            casos.append(Caso(d["pregunta"], d["esperado"]))
    return casos


def evaluar(buscador: Buscador, ruta: str | Path | None = None, k: int = 5) -> Resumen:
    casos = cargar(Path(ruta) if ruta else RAIZ / "evals" / "preguntas.jsonl")
    for c in casos:
        rutas = [r.fragmento.ruta for r in buscador.buscar(c.pregunta, k)]
        c.obtenido = rutas
        for n, ruta_fragmento in enumerate(rutas, 1):
            if any(e.lower() in ruta_fragmento.lower() for e in c.esperado):
                c.posicion = n
                break
    return Resumen(buscador.modo, k, casos)


def imprimir(r: Resumen, detalle: bool = False) -> None:
    print(f"Modo: {r.modo}")
    print(f"Preguntas: {len(r.casos)}   recall@{r.k}: {r.recall:.0%}   MRR: {r.mrr:.3f}")
    if detalle:
        for c in r.casos:
            if c.posicion is None:
                print(f"\n✗ {c.pregunta}\n  esperado: {c.esperado}\n  obtenido: {c.obtenido[:3]}")
