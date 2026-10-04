"""Índice BM25 (Okapi) en Python puro: la búsqueda léxica del RAG."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Sequence

from .texto import tokens


class BM25:
    def __init__(self, documentos: Sequence[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.docs = [Counter(tokens(d)) for d in documentos]
        self.longitudes = [sum(c.values()) for c in self.docs]
        self.media = sum(self.longitudes) / max(len(self.docs), 1)
        frecuencia: Counter[str] = Counter()
        for c in self.docs:
            frecuencia.update(c.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - df + 0.5) / (df + 0.5)) for t, df in frecuencia.items()}

    def puntuar(self, consulta: str) -> list[float]:
        terminos = tokens(consulta)
        puntos = []
        for c, longitud in zip(self.docs, self.longitudes, strict=True):
            s = 0.0
            for t in terminos:
                tf = c.get(t, 0)
                if tf:
                    s += (
                        self.idf[t]
                        * tf
                        * (self.k1 + 1)
                        / (tf + self.k1 * (1 - self.b + self.b * longitud / self.media))
                    )
            puntos.append(s)
        return puntos

    def buscar(self, consulta: str, k: int = 10) -> list[tuple[int, float]]:
        """Índices de los k documentos más relevantes con su puntuación (solo los que puntúan > 0)."""
        puntos = self.puntuar(consulta)
        orden = sorted(range(len(puntos)), key=lambda i: puntos[i], reverse=True)
        return [(i, puntos[i]) for i in orden[:k] if puntos[i] > 0]
