"""Preguntas de ejemplo por fragmento («doc2query»): mejoran la búsqueda de preguntas cortas o coloquiales.

Un alumno pregunta «¿hay typeof en Python?» o «¿qué es :=?», con palabras que no aparecen en el apartado que lo
responde. Para cada fragmento se generan una vez, con un modelo de lenguaje, varias preguntas de alumno que ese
fragmento responde, y se indexan junto a su texto (BM25 y embeddings). El generador solo ve los apuntes, nunca las
preguntas de evaluación.

Se guardan en conocimiento/preguntas_generadas.json, con la huella (sha256) del texto de cada fragmento: si un
apartado cambia, sus preguntas se vuelven a generar y las demás se reutilizan.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Callable, Sequence
from pathlib import Path

from .trocear import Fragmento

POR_FRAGMENTO = 10
LOTE = 6  # fragmentos por llamada al modelo
VERSION = 2  # forma parte de la huella: al cambiar las instrucciones se regeneran todas

INSTRUCCIONES = f"""Eres un generador de preguntas para el buscador de un tutor de Python en español.
Para cada fragmento de los apuntes que recibes, escribe {POR_FRAGMENTO} preguntas DISTINTAS que haría un alumno
y que ese fragmento responde:
- La MITAD, como un principiante que NO conoce el nombre técnico: describe lo que quiere conseguir o lo que le
  pasa, con palabras normales («hacer una lista en una sola línea», «subir mi librería para que otros la
  instalen», «meter un objeto dentro de otro», «mi programa no encuentra el archivo»). Sin jerga.
- La otra mitad, con el nombre técnico (función, módulo, error, operador...), cortas (3 a 6 palabras).
- Varía el tono: coloquial como en un foro, como duda práctica («cómo hago...», «por qué...», «me sale...»).
- Si el fragmento trata un operador o símbolo, incluye el símbolo tal cual en alguna pregunta.
No inventes cosas que el fragmento no trate. Responde SOLO con JSON: {{"id del fragmento": ["pregunta", ...], ...}}"""


def leer_json(respuesta: str) -> dict[str, list[str]]:
    """El objeto JSON de la respuesta. Corrige barras sin escapar («\\d» en una pregunta sobre regex)."""
    trozo = respuesta[respuesta.find("{") : respuesta.rfind("}") + 1]
    try:
        datos = json.loads(trozo)
    except json.JSONDecodeError:
        datos = json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", trozo))
    if not isinstance(datos, dict):
        raise ValueError("no es un objeto JSON")
    return datos


def huella(f: Fragmento) -> str:
    return hashlib.sha256(f"v{VERSION}\n{f.ruta}\n{f.texto}".encode()).hexdigest()[:16]


def cargar(ruta: Path) -> dict[str, list[str]]:
    """Preguntas guardadas por huella del fragmento ({} si no hay fichero)."""
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}


def para_fragmentos(fragmentos: Sequence[Fragmento], guardadas: dict[str, list[str]]) -> dict[str, list[str]]:
    """Preguntas de cada fragmento por su id (los que no tienen preguntas generadas no aparecen)."""
    return {f.id: guardadas[huella(f)] for f in fragmentos if huella(f) in guardadas}


def generar(
    fragmentos: Sequence[Fragmento],
    ruta: Path,
    pedir: Callable[[str, str], str],
    aviso: Callable[[str], None] = print,
    pausa: float = 4.0,
) -> dict[str, list[str]]:
    """Genera las preguntas que falten y las guarda. `pedir(instrucciones, texto)` devuelve la respuesta del modelo."""
    guardadas = cargar(ruta)
    vigentes = {huella(f) for f in fragmentos}
    faltan = [f for f in fragmentos if huella(f) not in guardadas]
    aviso(f"{len(fragmentos)} fragmentos; faltan {len(faltan)}.")
    for inicio in range(0, len(faltan), LOTE):
        lote = faltan[inicio : inicio + LOTE]
        texto = "\n\n".join(f"### id: {f.id}\nApartado: {f.ruta}\n{f.texto}" for f in lote)
        datos = None
        for intento in range(3):  # respuesta mal formada o corte de red: se pide otra vez
            try:
                datos = leer_json(pedir(INSTRUCCIONES, texto))
                break
            except ValueError:
                continue
            except OSError as e:  # sin conexión, DNS, API caída tras sus propios reintentos
                aviso(f"  lote {inicio // LOTE + 1}: {e}; reintento")
                time.sleep(pausa * 5 * (intento + 1))
        if datos is None:
            aviso(f"  lote {inicio // LOTE + 1}: sin respuesta válida, se salta (se completará en otra ejecución)")
            continue
        for f in lote:
            preguntas = [str(p).strip() for p in datos.get(f.id, []) if str(p).strip()]
            if preguntas:
                guardadas[huella(f)] = preguntas[:POR_FRAGMENTO]
        # Se guarda tras cada lote (solo las de fragmentos que siguen existiendo): si se corta, no se pierde nada.
        limpias = {h: p for h, p in guardadas.items() if h in vigentes}
        ruta.write_text(json.dumps(limpias, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        aviso(f"  {min(inicio + LOTE, len(faltan))}/{len(faltan)}")
        time.sleep(pausa)  # respeta el límite de peticiones por minuto del nivel gratuito
    return {h: p for h, p in guardadas.items() if h in vigentes}
