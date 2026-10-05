import json

from paithon import preguntas
from paithon.buscador import Buscador
from paithon.trocear import Fragmento

FRAGMENTOS = [
    Fragmento("d:0", "Doc", "Operadores", "Morsa", "El operador := asigna dentro de una expresión."),
    Fragmento("d:1", "Doc", "Tipos", "Type", "Con type() se ve la clase de un objeto."),
]


def test_genera_guarda_por_huella_y_reutiliza(tmp_path):
    ruta = tmp_path / "preguntas.json"
    llamadas = []

    def pedir(instrucciones, texto):
        llamadas.append(texto)
        return json.dumps({"d:0": ["¿qué es :=?"], "d:1": ["¿hay typeof en python?"]})

    generadas = preguntas.generar(FRAGMENTOS, ruta, pedir, aviso=lambda _: None, pausa=0)
    assert preguntas.para_fragmentos(FRAGMENTOS, generadas) == {
        "d:0": ["¿qué es :=?"],
        "d:1": ["¿hay typeof en python?"],
    }
    assert len(llamadas) == 1

    # Segunda vez: no hace falta pedir nada; si cambia un fragmento, solo se pide ese.
    preguntas.generar(FRAGMENTOS, ruta, pedir, aviso=lambda _: None, pausa=0)
    assert len(llamadas) == 1
    cambiado = [FRAGMENTOS[0], Fragmento("d:1", "Doc", "Tipos", "Type", "Texto nuevo.")]
    preguntas.generar(cambiado, ruta, pedir, aviso=lambda _: None, pausa=0)
    assert len(llamadas) == 2 and "Texto nuevo." in llamadas[-1] and "asigna" not in llamadas[-1]
    assert len(preguntas.cargar(ruta)) == 2  # la del texto antiguo se descarta


def test_el_buscador_encuentra_por_las_preguntas():
    b = Buscador(FRAGMENTOS, preguntas={"d:1": ["¿hay typeof en python?"]})
    assert b.buscar("typeof", 1)[0].fragmento.id == "d:1"
    assert Buscador(FRAGMENTOS).buscar("typeof", 1) == []


def test_lee_json_con_barras_sin_escapar():
    assert preguntas.leer_json(r'{"a": ["¿qué hace \d en una regex?"]}') == {"a": [r"¿qué hace \d en una regex?"]}
    assert preguntas.leer_json('Aquí tienes: {"a": ["x"]} ¡listo!') == {"a": ["x"]}


def test_salta_un_lote_ilegible_sin_perder_los_demas(tmp_path):
    respuestas = iter(["no es json", "tampoco", "nada"])
    generadas = preguntas.generar(
        FRAGMENTOS, tmp_path / "p.json", lambda i, t: next(respuestas), aviso=lambda _: None, pausa=0
    )
    assert generadas == {}
