import io
import json
import urllib.error

from paithon import red


def _error(codigo, cuerpo=b"{}"):
    return urllib.error.HTTPError("https://x", codigo, "error", {}, io.BytesIO(cuerpo))


def test_espera_pedida():
    cuerpo = json.dumps({"error": {"details": [{"retryDelay": "26s"}]}}).encode()
    assert red.espera_pedida(cuerpo) == 28
    assert red.espera_pedida(b"no es json") is None


def test_reintenta_429_y_luego_responde(monkeypatch):
    respuestas = [_error(429), _error(503), io.BytesIO(b'{"ok": true}')]

    def falso_urlopen(peticion, timeout):
        r = respuestas.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    esperas = []
    monkeypatch.setattr(red.urllib.request, "urlopen", falso_urlopen)
    monkeypatch.setattr(red.time, "sleep", esperas.append)
    assert red.post_json("https://x", {}, "clave") == {"ok": True}
    assert len(esperas) == 2


def test_no_reintenta_404(monkeypatch):
    def falso_urlopen(peticion, timeout):
        raise _error(404)

    monkeypatch.setattr(red.urllib.request, "urlopen", falso_urlopen)
    try:
        red.post_json("https://x", {}, "clave")
    except urllib.error.HTTPError as e:
        assert e.code == 404
    else:
        raise AssertionError("debía fallar")


def test_no_espera_horas_si_se_agota_la_cuota_diaria(monkeypatch):
    cuerpo = json.dumps({"error": {"details": [{"retryDelay": "3600s"}]}}).encode()

    def falso_urlopen(peticion, timeout):
        raise _error(429, cuerpo)

    esperas = []
    monkeypatch.setattr(red.urllib.request, "urlopen", falso_urlopen)
    monkeypatch.setattr(red.time, "sleep", esperas.append)
    try:
        red.post_json("https://x", {}, "clave")
    except urllib.error.HTTPError as e:
        assert e.code == 429
    else:
        raise AssertionError("debía fallar")
    assert esperas == []


def test_gemini_usa_el_modelo_de_respaldo(monkeypatch):
    from paithon import llm

    pedidos = []

    def falso_post_json(url, cuerpo, clave, reintentos=red.REINTENTOS):
        pedidos.append(url.split("/models/")[1].split(":")[0])
        if "lite" not in url:
            raise _error(429)
        return {"candidates": [{"content": {"parts": [{"text": "hola"}]}}]}

    monkeypatch.setattr(llm, "post_json", falso_post_json)
    g = llm.Gemini("clave", "principal", respaldo=["ligero-lite"])
    assert g.responder("sistema", [llm.Mensaje("user", "hola")]) == "hola"
    assert pedidos == ["principal", "ligero-lite"]


def test_gemini_avisa_si_no_responde_ningun_modelo(monkeypatch):
    from paithon import llm

    def falso_post_json(url, cuerpo, clave, reintentos=red.REINTENTOS):
        raise _error(503)

    monkeypatch.setattr(llm, "post_json", falso_post_json)
    g = llm.Gemini("clave", "principal", respaldo=["ligero"])
    try:
        g.responder("sistema", [llm.Mensaje("user", "hola")])
    except llm.ModeloNoDisponible:
        pass
    else:
        raise AssertionError("debía avisar")
