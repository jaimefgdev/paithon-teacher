"""Normalización de texto para buscar en español sin dependencias.

Quita acentos, pasa a minúsculas, descarta palabras vacías y aplica un recorte ligero de sufijos
(plurales y terminaciones frecuentes) para que «listas», «lista» y «listado» se parezcan. Respeta los
identificadores de Python: `__init__`, `f-string`, `isinstance` o `async` se conservan tal cual.
"""

from __future__ import annotations

import re
import unicodedata

PALABRAS_VACIAS = set(
    """a al algo algun alguna algunas alguno algunos ante antes aqui asi aun cada como con contra cual cuales cuando
    de del desde donde dos e el ella ellas ello ellos en entre era es esa esas ese eso esos esta estan estas este esto
    estos fue ha hay hace hacer la las le les lo los mas me mi mis mucho muy ni no nos o os otra otro para pero poco por
    porque puede que quien se sea ser si sin sobre solo son su sus tambien tan te tiene todo todos tu tus un una unas
    uno unos usar uso y ya yo the of to it on how what""".split()
)  # sin «is», «in», «for», «with» ni «and»: en Python son palabras clave y hay que poder buscarlas
# Operadores de Python como palabras propias: «¿qué significa := ?» tiene que poder encontrar el operador morsa.
OPERADORES = r":=|\*\*|//|->|>>|<<|==|!=|<=|>=|\+=|-=|\*=|/=|&|\||\^|~|@|%"
TOKEN = re.compile(r"\d+\.\d+|[a-z0-9_]+(?:-[a-z0-9_]+)*|" + OPERADORES)  # «0.1» es un número, no dos
SUFIJOS = (
    "amientos",
    "imientos",
    "amiento",
    "imiento",
    "aciones",
    "uciones",
    "acion",
    "ucion",
    "mente",
    "ables",
    "ibles",
    "able",
    "ible",
    "ados",
    "idos",
    "ando",
    "iendo",
    "ado",
    "ido",
    "ces",
    "es",
    "s",
)


def sin_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


def raiz(palabra: str) -> str:
    """Recorte de sufijos muy conservador: solo en palabras largas y nunca en identificadores con «_»."""
    if "_" in palabra or len(palabra) <= 4 or palabra.isdigit():
        return palabra
    for sufijo in SUFIJOS:
        if palabra.endswith(sufijo) and len(palabra) - len(sufijo) >= 4:
            return palabra[: -len(sufijo)]
    return palabra


def tokens(texto: str) -> list[str]:
    limpio = sin_acentos(texto.lower())
    return [
        raiz(t)
        for t in TOKEN.findall(limpio)
        if t not in PALABRAS_VACIAS and (len(t) > 1 or t.isdigit() or not t.isalnum())
    ]
