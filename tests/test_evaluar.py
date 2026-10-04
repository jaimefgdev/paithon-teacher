from paithon.buscador import Buscador
from paithon.evaluar import evaluar
from paithon.montaje import RAIZ


def test_recall_minimo_bm25(fragmentos):
    """Red de seguridad: un cambio en el troceo o en BM25 no debe hundir la recuperación."""
    r = evaluar(Buscador(fragmentos), RAIZ / "evals" / "preguntas.jsonl", k=5)
    assert len(r.casos) >= 30
    assert r.recall >= 0.75
    assert 0 < r.mrr <= 1
