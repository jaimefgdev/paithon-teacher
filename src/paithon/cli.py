"""Línea de órdenes: `paithon buscar`, `paithon preguntar`, `paithon evaluar`, `paithon web`."""

from __future__ import annotations

import argparse
import io
import sys

from . import __version__
from .llm import Mensaje, ModeloNoDisponible, desde_entorno
from .montaje import crear_buscador
from .tutor import Tutor


def _buscar(args: argparse.Namespace) -> int:
    buscador = crear_buscador(not args.solo_bm25)
    print(f"Modo: {buscador.modo}\n")
    for n, r in enumerate(buscador.buscar(args.consulta, args.k), 1):
        print(f"[{n}] {r.puntuacion:.4f} ({r.origen})  {r.fragmento.ruta}")
    return 0


def _preguntar(args: argparse.Namespace) -> int:
    llm = desde_entorno()
    if llm is None:
        print("Falta ANTHROPIC_API_KEY o GEMINI_API_KEY en el entorno.", file=sys.stderr)
        return 2
    tutor = Tutor(crear_buscador(not args.solo_bm25), llm, args.k)
    historial: list[Mensaje] = []
    pregunta = args.pregunta or _leer()
    while pregunta:
        try:
            r = tutor.preguntar(pregunta, historial)
        except ModeloNoDisponible:
            print(
                f"\nEl modelo ({llm.nombre}) no responde ahora mismo: está saturado o no hay conexión. "
                "Prueba de nuevo en unos minutos.",
                file=sys.stderr,
            )
            if args.pregunta:
                return 1
            pregunta = _leer()
            continue
        print(f"\n{r.texto}\n")
        for n in r.citadas:
            print(f"  [{n}] {r.fuentes[n - 1].fragmento.ruta}")
        historial += [Mensaje("user", pregunta), Mensaje("assistant", r.texto)]
        pregunta = None if args.pregunta else _leer()
    return 0


def _leer() -> str | None:
    try:
        return input("\nTú> ").strip() or None
    except EOFError:
        return None


def _evaluar(args: argparse.Namespace) -> int:
    from .evaluar import evaluar, imprimir

    resumen = evaluar(crear_buscador(not args.solo_bm25), args.preguntas, args.k)
    imprimir(resumen, detalle=args.detalle)
    return 0 if resumen.recall >= args.minimo else 1


def _generar_preguntas(args: argparse.Namespace) -> int:
    import os

    from . import preguntas
    from .montaje import carpeta_conocimiento, ruta_preguntas
    from .red import post_json
    from .trocear import trocear_carpeta

    clave = os.environ.get("GEMINI_API_KEY")
    if not clave:
        print("Falta GEMINI_API_KEY en el entorno.", file=sys.stderr)
        return 2
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{args.modelo}:generateContent"

    def pedir(instrucciones: str, texto: str) -> str:
        cuerpo = {
            "systemInstruction": {"parts": [{"text": instrucciones}]},
            "contents": [{"role": "user", "parts": [{"text": texto}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7},
        }
        datos = post_json(url, cuerpo, clave)
        return "".join(p.get("text", "") for p in datos["candidates"][0]["content"]["parts"])

    preguntas.generar(trocear_carpeta(carpeta_conocimiento()), ruta_preguntas(), pedir)
    return 0


def _web(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run("paithon.web:app", host=args.host, port=args.puerto)
    return 0


def main(argv: list[str] | None = None) -> int:
    for flujo in (sys.stdout, sys.stderr):  # la consola de Windows no usa UTF-8 por defecto
        if isinstance(flujo, io.TextIOWrapper):
            flujo.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="paithon", description="pAIthon Teacher: tutor de Python con RAG.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="orden", required=True)

    b = sub.add_parser("buscar", help="muestra los fragmentos que se recuperarían")
    b.add_argument("consulta")
    pr = sub.add_parser("preguntar", help="pregunta al tutor (sin pregunta: modo conversación)")
    pr.add_argument("pregunta", nargs="?")
    e = sub.add_parser("evaluar", help="mide la recuperación con el conjunto de preguntas")
    e.add_argument("--preguntas", default=None, help="fichero JSONL (por defecto evals/preguntas.jsonl)")
    e.add_argument("--minimo", type=float, default=0.0, help="recall mínimo; por debajo, sale con error")
    e.add_argument("--detalle", action="store_true", help="lista las preguntas falladas")
    g = sub.add_parser("generar-preguntas", help="genera las preguntas de ejemplo de cada fragmento (una vez)")
    g.add_argument("--modelo", default="gemini-flash-lite-latest")
    w = sub.add_parser("web", help="arranca la interfaz web de chat")
    w.add_argument("--host", default="127.0.0.1")
    w.add_argument("--puerto", type=int, default=8000)
    for s in (b, pr, e):
        s.add_argument("-k", type=int, default=5, help="fragmentos a recuperar")
        s.add_argument("--solo-bm25", action="store_true", help="no usar embeddings aunque haya clave")

    args = p.parse_args(argv)
    ordenes = {
        "buscar": _buscar,
        "preguntar": _preguntar,
        "evaluar": _evaluar,
        "generar-preguntas": _generar_preguntas,
        "web": _web,
    }
    return ordenes[args.orden](args)


if __name__ == "__main__":
    raise SystemExit(main())
