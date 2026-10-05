from conftest import EmbedderFalso

from paithon.bm25 import BM25
from paithon.buscador import Buscador
from paithon.texto import raiz, tokens


def test_tokens():
    assert tokens("¿Cómo se usan las listas?") == ["usan", "lista"]
    assert "__init__" in tokens("El método __init__")
    assert "with" in tokens("¿Para qué sirve with?")  # palabra clave de Python, no palabra vacía
    assert tokens("0.1 + 0.2") == ["0.1", "0.2"]
    assert raiz("diccionarios") == raiz("diccionario") == "diccionario"


def test_bm25_ordena_por_relevancia():
    bm = BM25(["las listas son mutables", "las tuplas son inmutables", "los diccionarios tienen claves"])
    assert bm.buscar("tuplas")[0][0] == 1
    assert bm.buscar("nada que ver") == []


def test_buscador_bm25_encuentra_apartados(fragmentos):
    b = Buscador(fragmentos)
    assert b.modo == "solo BM25"
    rutas = [r.fragmento.ruta for r in b.buscar("isinstance", 3)]
    assert any("isinstance" in r for r in rutas)
    assert all(r.origen == "bm25" for r in b.buscar("diccionario"))


def test_fusion_rrf(fragmentos):
    b = Buscador(fragmentos, EmbedderFalso())
    assert b.modo.startswith("híbrido")
    resultados = b.buscar("diferencia entre lista y tupla", 5)
    assert len(resultados) == 5
    puntos = [r.puntuacion for r in resultados]
    assert puntos == sorted(puntos, reverse=True)
    assert any(r.origen == "ambas" for r in resultados)


def test_semantica_da_resultados_sin_coincidencia_lexica(fragmentos):
    b = Buscador(fragmentos, EmbedderFalso())
    assert b.bm25.buscar("zzz") == []
    assert all(r.origen == "semantica" for r in b.buscar("zzz", 3))


def test_si_falla_la_api_de_embeddings_sigue_con_bm25(fragmentos):
    class EmbedderCaido(EmbedderFalso):
        def consulta(self, texto: str) -> list[float]:
            raise OSError("HTTP Error 503: Service Unavailable")

    resultados = Buscador(fragmentos, EmbedderCaido()).buscar("¿Qué es una tupla?", 5)
    assert resultados and all(r.origen == "bm25" for r in resultados)


def test_si_no_hay_cuota_de_embeddings_al_arrancar_busca_con_bm25(fragmentos):
    class EmbedderSinCuota(EmbedderFalso):
        def documentos(self, textos):
            raise OSError("HTTP Error 429: Too Many Requests")

    b = Buscador(fragmentos, EmbedderSinCuota())
    assert b.modo == "solo BM25" and "429" in b.aviso
    assert b.buscar("¿Qué es una tupla?", 3)


def test_sin_vectores_de_preguntas_sigue_con_los_de_los_fragmentos(fragmentos):
    class EmbedderParcial(EmbedderFalso):
        def consultas(self, textos):
            raise OSError("HTTP Error 429: Too Many Requests")

    b = Buscador(fragmentos, EmbedderParcial(), preguntas={fragmentos[0].id: ["¿qué es python?"]})
    assert b.modo.startswith("híbrido") and b.vectores_preguntas == [] and "429" in b.aviso
