"""Embeddings para la búsqueda semántica, con caché en SQLite.

Se usa la API de Gemini (modelo gemini-embedding-001, con nivel gratuito) mediante HTTP simple, sin SDK.
La caché evita volver a pagar (o a esperar) por textos ya calculados: la clave es un hash del modelo,
la tarea, la dimensión y el texto.
"""

from __future__ import annotations

import hashlib
import math
import sqlite3
import threading
from array import array
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Protocol

from .red import post_json

URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:batchEmbedContents"


class Embedder(Protocol):
    nombre: str

    def documentos(self, textos: Sequence[str]) -> list[list[float]]: ...

    def consulta(self, texto: str) -> list[float]: ...


def normalizar(v: Sequence[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def coseno(a: Sequence[float], b: Sequence[float]) -> float:
    """Producto escalar: los vectores ya están normalizados."""
    return sum(x * y for x, y in zip(a, b, strict=True))


class Cache:
    """Caché de vectores en SQLite. La web atiende cada petición en un hilo distinto: una sola conexión
    compartida (check_same_thread=False) protegida con un cerrojo."""

    def __init__(self, ruta: Path) -> None:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(ruta, check_same_thread=False)
        self.cerrojo = threading.Lock()
        self.db.execute("create table if not exists vectores (clave text primary key, vector blob not null)")

    @staticmethod
    def clave(*partes: str) -> str:
        return hashlib.sha256("\x1f".join(partes).encode("utf-8")).hexdigest()

    def leer(self, clave: str) -> list[float] | None:
        with self.cerrojo:
            fila = self.db.execute("select vector from vectores where clave=?", (clave,)).fetchone()
        return list(array("f", fila[0])) if fila else None

    def guardar(self, clave: str, vector: Sequence[float]) -> None:
        with self.cerrojo:
            self.db.execute("insert or replace into vectores values (?, ?)", (clave, array("f", vector).tobytes()))
            self.db.commit()


class GeminiEmbedder:
    """Embeddings de Gemini. La clave se lee de la variable de entorno GEMINI_API_KEY (nunca del código)."""

    def __init__(
        self, clave_api: str, cache: Cache, modelo: str = "gemini-embedding-001", dimension: int = 768, lote: int = 50
    ) -> None:
        self.clave_api, self.cache, self.modelo, self.dimension, self.lote = clave_api, cache, modelo, dimension, lote
        self.nombre = f"{modelo}/{dimension}"

    def _pedir(self, textos: Sequence[str], tarea: str) -> list[list[float]]:
        cuerpo = {
            "requests": [
                {
                    "model": f"models/{self.modelo}",
                    "content": {"parts": [{"text": t}]},
                    "taskType": tarea,
                    "outputDimensionality": self.dimension,
                }
                for t in textos
            ]
        }
        # Indexar miles de textos choca con el límite por minuto: aquí se reintenta con paciencia.
        datos = post_json(URL.format(modelo=self.modelo), cuerpo, self.clave_api, timeout=60, reintentos=10)
        return [normalizar(e["values"]) for e in datos["embeddings"]]

    def _con_cache(self, textos: Sequence[str], tarea: str) -> list[list[float]]:
        claves = [Cache.clave(self.nombre, tarea, t) for t in textos]
        vectores: list[list[float] | None] = [self.cache.leer(c) for c in claves]
        faltan = [i for i, v in enumerate(vectores) if v is None]
        for inicio in range(0, len(faltan), self.lote):
            grupo = faltan[inicio : inicio + self.lote]
            for i, v in zip(grupo, self._pedir([textos[i] for i in grupo], tarea), strict=True):
                self.cache.guardar(claves[i], v)
                vectores[i] = v
        return [v for v in vectores if v is not None]

    def documentos(self, textos: Sequence[str]) -> list[list[float]]:
        return self._con_cache(textos, "RETRIEVAL_DOCUMENT")

    def consulta(self, texto: str) -> list[float]:
        return self._con_cache([texto], "RETRIEVAL_QUERY")[0]

    def consultas(self, textos: Sequence[str]) -> list[list[float]]:
        """Varios textos embebidos como consulta (las preguntas de ejemplo de cada fragmento)."""
        return self._con_cache(textos, "RETRIEVAL_QUERY")


def _cargar_fastembed(clase: Any, modelo: str, carpeta: Path | None) -> Any:
    """Carga un modelo de fastembed desde una carpeta con ficheros reales.

    La caché de Hugging Face guarda los ficheros como enlaces a una carpeta «blobs»; onnxruntime rechaza los modelos
    grandes cuyos pesos (model.onnx_data) quedan fuera de la carpeta del modelo. Por eso se descarga una copia
    normal (snapshot_download con local_dir) y se carga desde ahí.
    """
    if carpeta is None:
        return clase(model_name=modelo)
    from huggingface_hub import snapshot_download

    descripcion = next(m for m in clase.list_supported_models() if m["model"] == modelo)
    repositorio = descripcion["sources"]["hf"]
    destino = carpeta / repositorio.replace("/", "--")
    if not (destino / ".completo").exists():
        snapshot_download(repositorio, local_dir=destino)
        (destino / ".completo").touch()
    return clase(model_name=modelo, specific_model_path=str(destino))


class LocalEmbedder:
    """Embeddings con un modelo que se ejecuta en el propio ordenador (fastembed, ONNX): sin clave ni cuota.

    El modelo se descarga la primera vez (a .cache/modelos). Los de la familia E5 necesitan los prefijos
    «query: » y «passage: »; los demás reciben el texto tal cual.
    """

    def __init__(self, cache: Cache, modelo: str, carpeta: Path | None = None, lote: int | None = None) -> None:
        # Los modelos grandes con textos de 512 tokens gastan mucha memoria por tanda: tandas pequeñas.
        lote = lote or (4 if "large" in modelo.lower() else 32)
        self.cache, self.modelo, self.carpeta, self.lote = cache, modelo, carpeta, lote
        self.nombre = f"local:{modelo}"
        self._modelo: Any = None

    def _cargar(self) -> Any:
        if self._modelo is None:
            from fastembed import TextEmbedding  # dependencia opcional: pip install fastembed

            self._modelo = _cargar_fastembed(TextEmbedding, self.modelo, self.carpeta)
        return self._modelo

    def _prefijo(self, tarea: str) -> str:
        if "e5" not in self.modelo.lower():
            return ""
        return "query: " if tarea == "RETRIEVAL_QUERY" else "passage: "

    def _con_cache(self, textos: Sequence[str], tarea: str) -> list[list[float]]:
        claves = [Cache.clave(self.nombre, tarea, t) for t in textos]
        vectores: list[list[float] | None] = [self.cache.leer(c) for c in claves]
        faltan = [i for i, v in enumerate(vectores) if v is None]
        if faltan:
            prefijo = self._prefijo(tarea)
            calculados = self._cargar().embed([prefijo + textos[i] for i in faltan], batch_size=self.lote)
            for i, v in zip(faltan, calculados, strict=True):
                vector = normalizar([float(x) for x in v])
                self.cache.guardar(claves[i], vector)
                vectores[i] = vector
        return [v for v in vectores if v is not None]

    def documentos(self, textos: Sequence[str]) -> list[list[float]]:
        return self._con_cache(textos, "RETRIEVAL_DOCUMENT")

    def consulta(self, texto: str) -> list[float]:
        return self._con_cache([texto], "RETRIEVAL_QUERY")[0]

    def consultas(self, textos: Sequence[str]) -> list[list[float]]:
        return self._con_cache(textos, "RETRIEVAL_QUERY")


class LocalReordenador:
    """Reordenador cross-encoder local (fastembed): lee la pregunta y cada candidato juntos y los puntúa."""

    def __init__(self, modelo: str = "jinaai/jina-reranker-v2-base-multilingual", carpeta: Path | None = None) -> None:
        self.modelo, self.carpeta = modelo, carpeta
        self.nombre = f"local:{modelo}"
        self._modelo: Any = None

    def puntuar(self, consulta: str, textos: Sequence[str]) -> list[float]:
        if self._modelo is None:
            from fastembed.rerank.cross_encoder import TextCrossEncoder

            self._modelo = _cargar_fastembed(TextCrossEncoder, self.modelo, self.carpeta)
        return [float(x) for x in self._modelo.rerank(consulta, list(textos))]
