from conftest import LLMFalso

from paithon.buscador import Buscador
from paithon.llm import Mensaje
from paithon.tutor import SISTEMA, Tutor, citas_usadas


def test_citas_usadas():
    assert citas_usadas("Sí [2], y [1] y otra vez [2]; [7] no existe", 5) == [2, 1]


def test_tutor_pasa_contexto_numerado_y_citas(fragmentos):
    llm = LLMFalso()
    r = Tutor(Buscador(fragmentos), llm, k=4).preguntar("¿Qué diferencia hay entre una lista y una tupla?")
    sistema, mensajes = llm.recibido[0]
    assert sistema == SISTEMA
    assert mensajes[-1].texto.startswith("Fragmentos de la base de conocimiento:")
    assert "[1] " in mensajes[-1].texto and "[4] " in mensajes[-1].texto
    assert len(r.fuentes) == 4
    assert r.citadas == [1, 2]  # [9] no existe y se descarta


def test_tutor_usa_el_turno_anterior_para_buscar(fragmentos):
    llm = LLMFalso()
    historial = [Mensaje("user", "Explícame los diccionarios"), Mensaje("assistant", "Son pares clave-valor.")]
    r = Tutor(Buscador(fragmentos), llm).preguntar("¿y cómo los recorro?", historial)
    assert any("Diccionarios" in f.fragmento.ruta for f in r.fuentes)
    assert llm.recibido[0][1][:2] == historial
