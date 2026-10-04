"""Monta las piezas a partir de la configuración del entorno (rutas y claves de API)."""

from __future__ import annotations

import os
from pathlib import Path

from .buscador import Buscador
from .embeddings import Cache, GeminiEmbedder
from .trocear import trocear_carpeta

RAIZ = Path(__file__).resolve().parents[2]


def carpeta_conocimiento() -> Path:
    return Path(os.environ.get("PAITHON_CONOCIMIENTO", RAIZ / "conocimiento"))


def ruta_cache() -> Path:
    return Path(os.environ.get("PAITHON_CACHE", RAIZ / ".cache" / "embeddings.sqlite"))


def crear_buscador(semantica: bool = True) -> Buscador:
    """Búsqueda híbrida si hay GEMINI_API_KEY y no se desactiva; si no, solo BM25."""
    fragmentos = trocear_carpeta(carpeta_conocimiento())
    clave = os.environ.get("GEMINI_API_KEY") if semantica else None
    embedder = GeminiEmbedder(clave, Cache(ruta_cache())) if clave else None
    return Buscador(fragmentos, embedder)
