"""Interfaz web de chat (FastAPI). Arranque: `paithon web` o `uvicorn paithon.web:app`."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import __version__
from .buscador import Buscador
from .llm import LLM, Mensaje, desde_entorno
from .montaje import crear_buscador
from .tutor import Tutor

ESTATICOS = Path(__file__).parent / "estatico"

app = FastAPI(title="PyMentor", version=__version__)


@lru_cache(maxsize=1)
def buscador() -> Buscador:
    return crear_buscador()


@lru_cache(maxsize=1)
def llm() -> LLM | None:
    return desde_entorno()


class Turno(BaseModel):
    rol: str = Field(pattern="^(user|assistant)$")
    texto: str = Field(max_length=20_000)


class Pregunta(BaseModel):
    pregunta: str = Field(min_length=1, max_length=4_000)
    historial: list[Turno] = Field(default_factory=list, max_length=40)


@app.get("/")
def inicio() -> FileResponse:
    return FileResponse(ESTATICOS / "index.html")


@app.get("/api/estado")
def estado() -> dict[str, object]:
    modelo = llm()
    return {
        "version": __version__,
        "busqueda": buscador().modo,
        "fragmentos": len(buscador().fragmentos),
        "modelo": modelo.nombre if modelo else None,
    }


@app.get("/api/buscar")
def buscar(q: str, k: int = 5) -> list[dict[str, object]]:
    return [
        {"ruta": r.fragmento.ruta, "puntuacion": round(r.puntuacion, 4), "origen": r.origen, "texto": r.fragmento.texto}
        for r in buscador().buscar(q, min(k, 20))
    ]


@app.post("/api/preguntar")
def preguntar(p: Pregunta) -> dict[str, object]:
    modelo = llm()
    if modelo is None:
        raise HTTPException(503, "El servidor no tiene configurada ANTHROPIC_API_KEY ni GEMINI_API_KEY.")
    r = Tutor(buscador(), modelo).preguntar(p.pregunta, [Mensaje(t.rol, t.texto) for t in p.historial])
    return {
        "respuesta": r.texto,
        "fuentes": [
            {"n": n, "ruta": f.fragmento.ruta, "texto": f.fragmento.texto, "citada": n in r.citadas}
            for n, f in enumerate(r.fuentes, 1)
        ],
    }
