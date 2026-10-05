"""Llamadas HTTP a la API de Gemini con reintentos ante cuota agotada o saturación pasajera."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

REINTENTOS = 4
REINTENTABLES = {429, 500, 503}  # cuota por minuto agotada, error interno, modelo saturado
MAX_ESPERA = 60  # si la API pide esperar más (cuota diaria agotada), no se espera: se avisa


def espera_pedida(cuerpo_error: bytes) -> float | None:
    """Segundos que la API pide esperar (RetryInfo.retryDelay, p. ej. «26s»), con un margen."""
    try:
        detalles = json.loads(cuerpo_error)["error"].get("details", [])
    except (ValueError, KeyError, TypeError, AttributeError):
        return None
    for d in detalles:
        if str(d.get("retryDelay", "")).endswith("s"):
            return float(d["retryDelay"][:-1]) + 2
    return None


def post_json(
    url: str, cuerpo: dict[str, Any], clave_api: str, timeout: float = 120, reintentos: int = REINTENTOS
) -> Any:
    peticion = urllib.request.Request(
        url,
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": clave_api},
    )
    for intento in range(reintentos + 1):
        try:
            with urllib.request.urlopen(peticion, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in REINTENTABLES or intento == reintentos:
                raise
            espera = espera_pedida(e.read()) or 5 * 2**intento
            if espera > MAX_ESPERA:
                raise
            time.sleep(espera)
    raise AssertionError("inalcanzable")
