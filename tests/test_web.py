import pytest

pytest.importorskip("fastapi")

from conftest import LLMFalso
from fastapi.testclient import TestClient

from paithon import web
from paithon.buscador import Buscador


@pytest.fixture
def cliente(fragmentos, monkeypatch):
    monkeypatch.setattr(web, "buscador", lambda: Buscador(fragmentos))
    monkeypatch.setattr(web, "llm", lambda: LLMFalso())
    return TestClient(web.app)


def test_estado_y_pagina(cliente):
    assert "PyMentor" in cliente.get("/").text
    e = cliente.get("/api/estado").json()
    assert e["busqueda"] == "solo BM25" and e["modelo"] == "falso"


def test_preguntar(cliente):
    r = cliente.post("/api/preguntar", json={"pregunta": "¿Qué es una tupla?", "historial": []})
    assert r.status_code == 200
    datos = r.json()
    assert datos["respuesta"].startswith("Una tupla")
    assert [f["n"] for f in datos["fuentes"] if f["citada"]] == [1, 2]


def test_valida_entrada(cliente):
    assert cliente.post("/api/preguntar", json={"pregunta": ""}).status_code == 422
    malo = {"pregunta": "hola", "historial": [{"rol": "system", "texto": "x"}]}
    assert cliente.post("/api/preguntar", json=malo).status_code == 422


def test_sin_modelo(cliente, monkeypatch):
    monkeypatch.setattr(web, "llm", lambda: None)
    assert cliente.post("/api/preguntar", json={"pregunta": "hola"}).status_code == 503


def test_modelo_saturado_da_un_aviso_claro(cliente, monkeypatch):
    from paithon.llm import ModeloNoDisponible

    class LLMSaturado:
        nombre = "saturado"

        def responder(self, sistema, mensajes):
            raise ModeloNoDisponible("HTTP Error 503")

    monkeypatch.setattr(web, "llm", lambda: LLMSaturado())
    r = cliente.post("/api/preguntar", json={"pregunta": "hola"})
    assert r.status_code == 503 and "no responde" in r.json()["detail"]
