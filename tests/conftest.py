from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import pytest

from paithon.llm import Mensaje
from paithon.trocear import Fragmento, trocear_carpeta

CONOCIMIENTO = Path(__file__).resolve().parents[1] / "conocimiento"


class EmbedderFalso:
    """Bolsa de palabras con vocabulario fijo: suficiente para probar la fusión sin red."""

    nombre = "falso"
    VOCABULARIO = ("lista", "tupla", "diccionario", "bucle", "error", "clase", "fichero", "repetir")

    def _vector(self, texto: str) -> list[float]:
        t = texto.lower()
        v = [float(t.count(p)) for p in self.VOCABULARIO]
        n = sum(x * x for x in v) ** 0.5 or 1.0
        return [x / n for x in v]

    def documentos(self, textos: Sequence[str]) -> list[list[float]]:
        return [self._vector(t) for t in textos]

    def consulta(self, texto: str) -> list[float]:
        return self._vector(texto)


class LLMFalso:
    nombre = "falso"

    def __init__(self, respuesta: str = "Una tupla es inmutable [1]. Ver también [2] y [9].") -> None:
        self.respuesta = respuesta
        self.recibido: list[tuple[str, list[Mensaje]]] = []

    def responder(self, sistema: str, mensajes: Sequence[Mensaje]) -> str:
        self.recibido.append((sistema, list(mensajes)))
        return self.respuesta


@pytest.fixture(scope="session")
def fragmentos() -> list[Fragmento]:
    return trocear_carpeta(CONOCIMIENTO)
