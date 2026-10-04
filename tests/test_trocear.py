from paithon.trocear import Fragmento, frase, partir, trocear_texto

DOC = """# CONOCIMIENTO 9 — PRUEBAS DE PYTHON

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTRUCTURAS DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Introducción a las estructuras.

LISTAS

Una lista es mutable.

```python
# NO ES UN APARTADO
x = [1, 2]
```

TUPLAS

Una tupla es inmutable.
"""


def test_secciones_y_apartados():
    fs = trocear_texto(DOC, "09_pruebas.md")
    assert [f.ruta for f in fs] == [
        "Pruebas de Python › Estructuras de datos",
        "Pruebas de Python › Estructuras de datos › Listas",
        "Pruebas de Python › Estructuras de datos › Tuplas",
    ]
    assert fs[1].id == "09_pruebas:1"
    assert "# NO ES UN APARTADO" in fs[1].texto  # las líneas en mayúsculas dentro de código no cortan


def test_frase_respeta_siglas():
    assert frase("CONVENCIONES DE NOMBRES (PEP 8)") == "Convenciones de nombres (PEP 8)"
    assert frase("HTTP Y APIS") == "HTTP y APIs"
    assert frase("TYPE() Y ISINSTANCE()") == "type() y isinstance()"


def test_partir_no_deja_codigo_abierto():
    codigo = "```python\n" + "\n\n".join(f"linea_{i} = {i}" for i in range(400)) + "\n```"
    trozos = partir(codigo, maximo=500)
    assert len(trozos) > 1
    for t in trozos:
        assert t.count("```") % 2 == 0
        assert len(t) < 1000


def test_base_real(fragmentos: list[Fragmento]):
    assert len(fragmentos) > 100
    assert len({f.id for f in fragmentos}) == len(fragmentos)
    assert all(f.texto.count("```") % 2 == 0 for f in fragmentos)
