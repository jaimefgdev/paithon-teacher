"""Modelos de lenguaje para generar la respuesta: Claude (Anthropic) o Gemini, intercambiables.

Las claves se leen siempre de variables de entorno (ANTHROPIC_API_KEY, GEMINI_API_KEY), nunca del código.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from .red import post_json


class ModeloNoDisponible(Exception):
    """El modelo no ha respondido (saturado, sin cuota o sin conexión) después de los reintentos."""


@dataclass(frozen=True)
class Mensaje:
    rol: str  # "user" o "assistant"
    texto: str


class LLM(Protocol):
    nombre: str

    def responder(self, sistema: str, mensajes: Sequence[Mensaje]) -> str: ...


class Claude:
    def __init__(self, clave_api: str, modelo: str = "claude-sonnet-5-5", max_tokens: int = 1500) -> None:
        import anthropic  # dependencia opcional: solo si se usa Claude

        self.cliente = anthropic.Anthropic(api_key=clave_api)
        self.modelo, self.max_tokens = modelo, max_tokens
        self.nombre = modelo

    def responder(self, sistema: str, mensajes: Sequence[Mensaje]) -> str:
        import anthropic

        try:
            r = self.cliente.messages.create(
                model=self.modelo,
                max_tokens=self.max_tokens,
                system=sistema,
                messages=[{"role": m.rol, "content": m.texto} for m in mensajes],
            )
        except anthropic.APIError as e:  # el SDK ya reintenta los errores pasajeros
            raise ModeloNoDisponible(str(e)) from e
        return "".join(b.text for b in r.content if b.type == "text")


class Gemini:
    URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

    def __init__(self, clave_api: str, modelo: str = "gemini-flash-latest", respaldo: Sequence[str] = ()) -> None:
        self.clave_api, self.modelo = clave_api, modelo
        self.respaldo = [m for m in respaldo if m != modelo]  # se prueban en orden si el principal no responde
        self.nombre = modelo

    def responder(self, sistema: str, mensajes: Sequence[Mensaje]) -> str:
        cuerpo = {
            "systemInstruction": {"parts": [{"text": sistema}]},
            "contents": [
                {"role": "model" if m.rol == "assistant" else "user", "parts": [{"text": m.texto}]} for m in mensajes
            ],
        }
        error: OSError | None = None
        for modelo in [self.modelo, *self.respaldo]:
            try:
                # Pocos reintentos: el alumno está esperando; si no responde, se pasa al modelo de respaldo.
                datos = post_json(self.URL.format(modelo=modelo), cuerpo, self.clave_api, reintentos=1)
                break
            except OSError as e:  # HTTPError (cuota, saturación), URLError y timeouts
                error = e
        else:
            raise ModeloNoDisponible(str(error)) from error
        partes = datos["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in partes)


def desde_entorno() -> LLM | None:
    """Claude si hay ANTHROPIC_API_KEY; si no, Gemini si hay GEMINI_API_KEY; si no, None."""
    if clave := os.environ.get("ANTHROPIC_API_KEY"):
        return Claude(clave, os.environ.get("PAITHON_MODELO", "claude-sonnet-5-5"))
    if clave := os.environ.get("GEMINI_API_KEY"):
        # Cada modelo tiene su propia cuota gratuita: si el principal la agota, responde el ligero.
        return Gemini(
            clave, os.environ.get("PAITHON_MODELO", "gemini-flash-latest"), respaldo=["gemini-flash-lite-latest"]
        )
    return None
