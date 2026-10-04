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
