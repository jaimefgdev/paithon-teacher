"""Monta las piezas a partir de la configuración del entorno (rutas y claves de API)."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

from . import preguntas
from .buscador import Buscador
from .embeddings import Cache, Embedder, GeminiEmbedder, LocalEmbedder, LocalReordenador
from .trocear import trocear_carpeta

RAIZ = Path(__file__).resolve().parents[2]


def carpeta_conocimiento() -> Path:
    return Path(os.environ.get("PAITHON_CONOCIMIENTO", RAIZ / "conocimiento"))


def ruta_cache() -> Path:
    return Path(os.environ.get("PAITHON_CACHE", RAIZ / ".cache" / "embeddings.sqlite"))


def ruta_preguntas() -> Path:
    """Preguntas de ejemplo generadas para cada fragmento (ver preguntas.py)."""
    return carpeta_conocimiento() / "preguntas_generadas.json"


MODELO_LOCAL = "intfloat/multilingual-e5-large"


def crear_embedder() -> Embedder | None:
    """Qué modelo de embeddings usar.

    PAITHON_EMBEDDINGS=local:<modelo> o =gemini lo fija. Sin indicarlo: el modelo local (multilingual-e5-large, sin
    clave ni cuota; necesita `pip install fastembed`) si está instalado; si no, Gemini si hay GEMINI_API_KEY.
    """
    eleccion = os.environ.get("PAITHON_EMBEDDINGS", "")
    if not eleccion and importlib.util.find_spec("fastembed"):
        eleccion = f"local:{MODELO_LOCAL}"
    if eleccion.startswith("local:"):
        return LocalEmbedder(Cache(ruta_cache()), eleccion.removeprefix("local:"), RAIZ / ".cache" / "modelos")
    clave = os.environ.get("GEMINI_API_KEY")
    return GeminiEmbedder(clave, Cache(ruta_cache())) if clave else None


def crear_buscador(semantica: bool = True) -> Buscador:
    """Búsqueda híbrida si hay modelo de embeddings y no se desactiva; si no, solo BM25."""
    fragmentos = trocear_carpeta(carpeta_conocimiento())
    embedder = crear_embedder() if semantica else None
    generadas = preguntas.para_fragmentos(fragmentos, preguntas.cargar(ruta_preguntas()))
    # PAITHON_REORDENAR=local:<modelo> añade un reordenador cross-encoder en este ordenador
    eleccion = os.environ.get("PAITHON_REORDENAR", "")
    reordenador = (
        LocalReordenador(eleccion.removeprefix("local:"), RAIZ / ".cache" / "modelos")
        if semantica and eleccion.startswith("local:")
        else None
    )
    return Buscador(fragmentos, embedder, generadas, reordenador)
