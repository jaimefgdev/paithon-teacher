"""Divide la base de conocimiento de PyMentor en fragmentos citables.

Los documentos usan este formato:

    # CONOCIMIENTO 1 — FUNDAMENTOS DE PYTHON        <- título del documento
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    STRINGS EN PROFUNDIDAD                          <- sección
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    MÉTODOS DE STRING MÁS USADOS                    <- apartado (línea en mayúsculas)

Cada fragmento es un apartado (o la parte de una sección antes de su primer apartado). Los apartados
muy largos se parten por líneas en blanco; si lo largo es un bloque de código, se cierra en un fragmento
y se reabre en el siguiente, para que cada trozo siga siendo código válido.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SEPARADOR = re.compile(r"^━{10,}\s*$")
VALLA = re.compile(r"^\s*```")
MAX_CARACTERES = 1800
SIGLAS = {
    "pep",
    "oop",
    "poo",
    "api",
    "apis",
    "json",
    "csv",
    "http",
    "https",
    "sql",
    "cli",
    "etl",
    "rest",
    "aws",
    "ide",
    "solid",
    "dom",
    "orm",
    "url",
    "html",
    "css",
    "ia",
    "ml",
    "gil",
    "io",
    "os",
    "uv",
    "pypi",
    "repl",
    "venv",
}


@dataclass(frozen=True)
class Fragmento:
    id: str
    documento: str
    seccion: str
    apartado: str
    texto: str

    @property
    def ruta(self) -> str:
        """Dónde está el fragmento: «Fundamentos de Python › Strings en profundidad › Métodos de string»."""
        return " › ".join(p for p in (self.documento, self.seccion, self.apartado) if p)


def frase(titulo: str) -> str:
    """«STRINGS EN PROFUNDIDAD» -> «Strings en profundidad», respetando siglas (PEP 8, JSON, API...)."""
    salida = []
    for n, palabra in enumerate(titulo.strip().lower().split()):
        limpia = palabra.strip("()[],.:;")
        if limpia in SIGLAS:
            sigla = limpia[:-1].upper() + "s" if limpia.endswith("is") and limpia[:-1] in SIGLAS else limpia.upper()
            palabra = palabra.replace(limpia, sigla)
        elif limpia == "python":
            palabra = palabra.replace("python", "Python")
        elif n == 0 and not palabra.endswith("()"):  # «type()» se queda en minúscula
            palabra = palabra[:1].upper() + palabra[1:]
        salida.append(palabra)
    return " ".join(salida)


def _es_apartado(linea: str) -> bool:
    """Una línea entera en mayúsculas que empieza por letra o número (no código, listas ni flechas)."""
    s = linea.strip()
    if len(s) < 4 or len(s) > 80 or not s[0].isalnum():
        return False
    letras = [c for c in s if c.isalpha()]
    return len(letras) >= 3 and all(c.isupper() for c in letras)


def _titulo_documento(lineas: list[str], defecto: str) -> str:
    for linea in lineas[:5]:
        if linea.startswith("# "):
            # «CONOCIMIENTO 1 — FUNDAMENTOS DE PYTHON» -> «Fundamentos de Python»
            return frase(linea[2:].split("—", 1)[-1])
    return defecto


def partir(texto: str, maximo: int = MAX_CARACTERES) -> list[str]:
    """Parte un texto largo por líneas en blanco, sin dejar ningún bloque de código abierto."""
    if len(texto) <= maximo:
        return [texto]
    bloques: list[str] = []
    actual: list[str] = []
    en_codigo = False
    apertura = "```"
    for linea in texto.split("\n"):
        if VALLA.match(linea):
            en_codigo = not en_codigo
            if en_codigo:
                apertura = linea.strip()
        actual.append(linea)
        if linea.strip() == "" and len("\n".join(actual)) >= maximo * 0.6:
            if en_codigo:
                bloques.append("\n".join(actual).rstrip() + "\n```")
                actual = [apertura]
            else:
                bloques.append("\n".join(actual).strip())
                actual = []
    resto = "\n".join(actual).strip()
    if resto and resto != apertura:
        bloques.append(resto)
    return bloques


def trocear_texto(texto: str, nombre: str) -> list[Fragmento]:
    lineas = texto.splitlines()
    documento = _titulo_documento(lineas, nombre)
    fragmentos: list[Fragmento] = []
    seccion = apartado = ""
    buffer: list[str] = []
    en_codigo = False

    def volcar() -> None:
        cuerpo = "\n".join(buffer).strip()
        buffer.clear()
        if not cuerpo or not seccion:
            return
        for trozo in partir(cuerpo):
            fragmentos.append(
                Fragmento(
                    f"{Path(nombre).stem}:{len(fragmentos)}",
                    documento,
                    frase(seccion),
                    frase(apartado) if apartado else "",
                    trozo,
                )
            )

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if VALLA.match(linea):
            en_codigo = not en_codigo
            buffer.append(linea)
        elif not en_codigo and SEPARADOR.match(linea):
            if i + 2 < len(lineas) and SEPARADOR.match(lineas[i + 2]):  # ━━━ / TÍTULO / ━━━ -> nueva sección
                volcar()
                seccion, apartado = lineas[i + 1].strip(), ""
                i += 3
                continue
        elif not en_codigo and seccion and _es_apartado(linea):
            volcar()
            apartado = linea.strip()
        elif seccion or not linea.startswith("# "):
            buffer.append(linea)
        i += 1
    volcar()
    return fragmentos


def trocear_carpeta(carpeta: Path) -> list[Fragmento]:
    """Todos los documentos de conocimiento (*.md) de la carpeta, en orden."""
    fragmentos: list[Fragmento] = []
    for ruta in sorted(carpeta.glob("*.md")):
        fragmentos.extend(trocear_texto(ruta.read_text(encoding="utf-8"), ruta.name))
    return fragmentos
