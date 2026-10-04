"""El tutor: recupera fragmentos de la base de conocimiento y pide al modelo una respuesta citada."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field

from .buscador import Buscador, Resultado
from .llm import LLM, Mensaje

SISTEMA = """Eres PyMentor, un profesor de Python paciente y con criterio. Respondes siempre en español.

Cómo respondes:
- Básate en los fragmentos de la base de conocimiento que se te dan, numerados como [1], [2]...
- Cita el fragmento en el que te apoyas con su número entre corchetes, justo después de la idea.
- Si los fragmentos no cubren la pregunta, dilo con claridad («Esto no está en mis apuntes») y responde
  con prudencia, sin inventar citas.
- Explica con ejemplos cortos de código ejecutable y adapta el nivel al del alumno.
- Si el alumno pega código, señala primero lo que está bien, después los errores y por qué, y propón
  la corrección.
- Termina, cuando tenga sentido, con un mini ejercicio para practicar lo explicado."""

CITA = re.compile(r"\[(\d+)\]")
HISTORIAL_MAXIMO = 8


def contexto(resultados: Sequence[Resultado]) -> str:
    bloques = [f"[{n}] {r.fragmento.ruta}\n{r.fragmento.texto}" for n, r in enumerate(resultados, 1)]
    return "Fragmentos de la base de conocimiento:\n\n" + "\n\n---\n\n".join(bloques)


def citas_usadas(respuesta: str, total: int) -> list[int]:
    """Números de fragmento citados en la respuesta, sin repetir y descartando los que no existen."""
    vistos: list[int] = []
    for m in CITA.finditer(respuesta):
        n = int(m.group(1))
        if 1 <= n <= total and n not in vistos:
            vistos.append(n)
    return vistos


@dataclass
class Respuesta:
    texto: str
    fuentes: list[Resultado]
    citadas: list[int] = field(default_factory=list)


class Tutor:
    def __init__(self, buscador: Buscador, llm: LLM, k: int = 5) -> None:
        self.buscador, self.llm, self.k = buscador, llm, k

    def preguntar(self, pregunta: str, historial: Sequence[Mensaje] = ()) -> Respuesta:
        # Se busca con la pregunta y el último turno del alumno: «¿y con diccionarios?» necesita el contexto previo.
        previas = [m.texto for m in historial if m.rol == "user"][-1:]
        resultados = self.buscador.buscar(" ".join([*previas, pregunta]), self.k)
        mensajes = [
            *historial[-HISTORIAL_MAXIMO:],
            Mensaje("user", f"{contexto(resultados)}\n\nPregunta del alumno: {pregunta}"),
        ]
        texto = self.llm.responder(SISTEMA, mensajes)
        return Respuesta(texto, resultados, citas_usadas(texto, len(resultados)))
