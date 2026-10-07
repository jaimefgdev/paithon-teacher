# CONOCIMIENTO 9 — PREGUNTAS FRECUENTES
# Base de conocimiento para pAIthon Teacher.
# Diferencias que confunden, recetas de «cómo hago...», conceptos de Python y novedades recientes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIFERENCIAS QUE SUELEN CONFUNDIR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LISTA, TUPLA, SET Y DICCIONARIO: CUÁL USAR

- Lista `[1, 2, 3]`: colección ordenada que va a cambiar (añadir, quitar). Permite repetidos.
- Tupla `(1, 2, 3)`: colección ordenada fija; para datos que van juntos y no cambian
  (coordenadas, una fila de resultados, varios valores devueltos). Puede ser clave de dict.
- Set `{1, 2, 3}`: sin orden ni repetidos; para quitar duplicados y comprobar pertenencia muy
  rápido.
- Diccionario `{"clave": valor}`: asociar claves con valores; buscar por clave es muy rápido.

Si necesitas «una lista que no cambie», tupla; «buscar si algo está, muchas veces», set;
«buscar un dato a partir de otro», diccionario.

DIFERENCIA ENTRE == E IS

- `==` compara el valor: ¿son iguales?
- `is` compara la identidad: ¿son el mismo objeto en memoria?

```python
a = [1, 2]
b = [1, 2]
a == b  # True: mismo contenido
a is b  # False: dos listas distintas
x is None  # la forma correcta de comparar con None (también True y False en casos concretos)
```

`is` con números o textos puede dar resultados sorprendentes porque Python reutiliza algunos
objetos pequeños (enteros de -5 a 256, ciertos strings). Usa `is` solo con `None`.

APPEND, EXTEND, INSERT Y EL OPERADOR +

```python
a = [1, 2]
a.append([3, 4])  # [1, 2, [3, 4]] → añade UN elemento (aunque sea una lista)
a = [1, 2]
a.extend([3, 4])  # [1, 2, 3, 4] → añade cada elemento
a.insert(0, 99)  # [99, 1, 2, 3, 4] → en una posición
b = a + [5]  # lista NUEVA; a no cambia
a += [5]  # modifica a (como extend)
```

REMOVE, POP, DEL Y CLEAR

```python
x = ["a", "b", "c", "b"]
x.remove("b")  # quita la PRIMERA aparición del valor → ['a', 'c', 'b'] (ValueError si no está)
x.pop()  # quita y DEVUELVE el último → 'b'
x.pop(0)  # quita y devuelve el de la posición 0 → 'a'
del x[0]  # borra por posición (o un rango: del x[1:3]); no devuelve nada
x.clear()  # vacía la lista

# Quitar TODAS las apariciones de un valor
x = [v for v in x if v != "b"]
```

SORT Y SORTED, REVERSE Y REVERSED

- `lista.sort()` ordena la lista original y devuelve `None`; `sorted(x)` devuelve una lista nueva
  y acepta cualquier iterable.
- `lista.reverse()` invierte la original; `reversed(x)` devuelve un iterador; `x[::-1]` crea una
  copia invertida.

COPY Y DEEPCOPY

- Asignar (`b = a`) no copia: los dos nombres apuntan al mismo objeto.
- Copia superficial (`a.copy()`, `a[:]`, `copy.copy(a)`): objeto nuevo, pero los objetos de
  dentro se comparten.
- Copia profunda (`copy.deepcopy(a)`): copia todo, también lo anidado. Necesaria con listas de
  listas o diccionarios con listas si vas a modificar lo de dentro.

FUNCIÓN FRENTE A MÉTODO

Una función se llama sola: `len(lista)`. Un método pertenece a un objeto y se llama con un
punto: `lista.append(3)`. Un método es una función definida dentro de una clase que recibe el
objeto como primer argumento (`self`).

PRINT FRENTE A RETURN

- `print()` muestra un texto en pantalla; la función sigue y, si no hay `return`, devuelve `None`.
- `return` devuelve un valor a quien llamó a la función, para usarlo después; además, termina la
  función.

```python
def doble_print(x):
    print(x * 2)


def doble_return(x):
    return x * 2


resultado = doble_print(5)  # muestra 10, pero resultado es None
resultado = doble_return(5)  # no muestra nada, resultado es 10
```

En el REPL parece lo mismo porque el intérprete muestra el valor devuelto; en un script, no.

MÓDULO, PAQUETE, LIBRERÍA Y FRAMEWORK

- Módulo: un fichero `.py`.
- Paquete: una carpeta con módulos (normalmente con `__init__.py`).
- Librería: código reutilizable que tú llamas (requests, pandas); puede ser un paquete o varios.
- Framework: estructura que llama a tu código y marca cómo organizarlo (Django, FastAPI).
- Biblioteca estándar: los módulos que vienen con Python sin instalar nada.
- PyPI: el repositorio público de paquetes que instala `pip`.

ITERABLE, ITERADOR Y GENERADOR

- Iterable: algo que se puede recorrer con `for` (lista, string, dict, fichero). Tiene `__iter__`.
- Iterador: el objeto que va dando los elementos uno a uno con `next()` y se agota. `iter(lista)`
  devuelve un iterador.
- Generador: una forma fácil de crear iteradores, con `yield` o con `(x for x in ...)`. Calcula
  los valores bajo demanda, sin guardarlos todos en memoria.

```python
numeros = [1, 2, 3]  # iterable: se puede recorrer muchas veces
it = iter(numeros)
next(it), next(it)  # 1, 2
gen = (x * 2 for x in numeros)
list(gen)  # [2, 4, 6]
list(gen)  # [] → el generador ya se agotó
```

ARGUMENTOS Y PARÁMETROS

Los parámetros son los nombres de la definición (`def saludar(nombre)`); los argumentos, los
valores que se pasan al llamar (`saludar("Ana")`). Los argumentos pueden ser posicionales (por
orden) o con nombre (`saludar(nombre="Ana")`).

COMPILADO O INTERPRETADO: CÓMO SE EJECUTA PYTHON

Python (CPython, la implementación oficial) compila primero el código a bytecode (los `.pyc` de
`__pycache__`) y luego lo ejecuta en su máquina virtual. Por eso se dice que es interpretado,
aunque hay un paso de compilación automático. Otras implementaciones: PyPy (con compilador JIT,
más rápido en bucles de Python puro), MicroPython (microcontroladores). Desde Python 3.13 CPython
incluye un compilador JIT experimental, desactivado por defecto.

PYTHON 2 FRENTE A PYTHON 3

Python 2 dejó de mantenerse en 2020. Si ves `print "hola"` sin paréntesis, `raw_input()`,
`xrange()` o `unicode()`, es código de Python 2. Aprende y usa siempre Python 3.

Diferencias que aparecen al leer código antiguo:

- `raw_input()` de Python 2 es el `input()` de Python 3; el `input()` de Python 2 evaluaba lo
  escrito como código (peligroso).
- `xrange()` de Python 2 es el `range()` de Python 3; el `range()` de Python 2 creaba una lista
  entera en memoria.
- `5 / 2` daba 2 en Python 2 (división entera entre enteros); en Python 3 da 2.5.
- En Python 2 los textos eran bytes por defecto: un fichero con tildes o eñes necesitaba la línea
  `# -*- coding: utf-8 -*-` al principio, o daba `SyntaxError: Non-ASCII character 'Ã'... but
  no encoding declared`. En Python 3 el código es UTF-8 por defecto y esa línea ya no hace falta.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONCEPTOS QUE APARECEN EN TODAS PARTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUÉ SIGNIFICA IF __NAME__ == "__MAIN__"

Cada módulo tiene la variable `__name__`. Si ejecutas el fichero directamente, vale
`"__main__"`; si otro fichero lo importa, vale el nombre del módulo. Así el código de dentro del
`if` solo se ejecuta al lanzar el script, no al importarlo.

```python
def sumar(a, b):
    return a + b


if __name__ == "__main__":
    print(sumar(2, 3))  # solo al hacer: python mi_modulo.py
```

LOS USOS DEL GUION BAJO

```python
for _ in range(3):  # variable que no se usa
    ...
nombre, _, edad = datos  # ignorar un valor al desempaquetar
_interno = 1  # convención: «uso interno»
__privado = 2  # en clases: cambio de nombre para evitar choques
__init__  # métodos especiales («dunder»: double underscore)
1_000_000  # separador de miles en números
_  # en el REPL: el último resultado
match x:
    case _:
        ...  # en match: cualquier valor
```

QUÉ SON *ARGS Y **KWARGS

`*args` recoge los argumentos posicionales sobrantes en una tupla; `**kwargs`, los argumentos con
nombre sobrantes en un diccionario. Los nombres son convención: lo que importa son los asteriscos.

```python
def info(*args, **kwargs):
    print(args)  # (1, 2)
    print(kwargs)  # {'a': 3}


info(1, 2, a=3)
```

Al llamar, los asteriscos hacen lo contrario: desempaquetan (`f(*lista)`, `f(**diccionario)`).

QUÉ ES PASS, NONE Y ELLIPSIS

- `pass`: no hace nada; sirve para dejar un bloque vacío (`def pendiente(): pass`).
- `None`: el valor «nada». Lo devuelven las funciones sin `return`.
- `...` (Ellipsis): un objeto que también se usa como marcador de «por completar» o en anotaciones
  de tipo y en NumPy.

QUÉ ES PEP 8 Y QUÉ ES UNA PEP

Una PEP (Python Enhancement Proposal) es un documento que propone o describe algo de Python.
PEP 8 es la guía de estilo: 4 espacios de sangría, `snake_case` para funciones y variables,
`PascalCase` para clases, `MAYÚSCULAS` para constantes, espacios alrededor de los operadores,
imports al principio (primero la biblioteca estándar, luego terceros y luego los tuyos) y dos
líneas en blanco entre funciones de nivel superior. PEP 20 es «El Zen de Python»:
`import this`. Herramientas como `ruff format` o `black` aplican el estilo automáticamente.

EL ZEN DE PYTHON

`import this` muestra los principios del lenguaje. Los más citados: «Bello es mejor que feo»,
«Explícito es mejor que implícito», «Simple es mejor que complejo», «La legibilidad cuenta»,
«Los errores nunca deberían pasar en silencio» y «Debería haber una, y preferiblemente solo una,
manera obvia de hacerlo».

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CÓMO HAGO: LISTAS Y DICCIONARIOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUITAR DUPLICADOS MANTENIENDO EL ORDEN

```python
datos = [3, 1, 3, 2, 1]
list(dict.fromkeys(datos))  # [3, 1, 2] → conserva el orden
list(set(datos))  # sin repetidos, pero sin orden garantizado

# Con objetos no hashables (diccionarios), por un campo
vistos, unicos = set(), []
for p in personas:
    if p["email"] not in vistos:
        vistos.add(p["email"])
        unicos.append(p)
```

APLANAR UNA LISTA DE LISTAS

```python
anidada = [[1, 2], [3], [4, 5]]
[x for sub in anidada for x in sub]  # [1, 2, 3, 4, 5]
from itertools import chain

list(chain.from_iterable(anidada))
# Para anidamientos de profundidad variable: una función recursiva
```

DIVIDIR UNA LISTA EN TROZOS

```python
def trozos(lista, n):
    return [lista[i : i + n] for i in range(0, len(lista), n)]


trozos([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]

from itertools import batched  # Python 3.12+

list(batched([1, 2, 3, 4, 5], 2))  # [(1, 2), (3, 4), (5,)]
```

ENCONTRAR LA POSICIÓN DE UN ELEMENTO

```python
frutas = ["pera", "uva", "pera"]
frutas.index("uva")  # 1 (ValueError si no está)
[i for i, f in enumerate(frutas) if f == "pera"]  # [0, 2] → todas las posiciones
"kiwi" in frutas  # comprobar antes de index
frutas.count("pera")  # 2
```

INVERTIR UN DICCIONARIO Y BUSCAR LA CLAVE DE UN VALOR

```python
precios = {"pan": 1.2, "leche": 0.9}
invertido = {v: k for k, v in precios.items()}  # valor → clave (si los valores son únicos)
claves = [k for k, v in precios.items() if v == 0.9]  # claves con ese valor
max(precios, key=precios.get)  # 'pan' → la clave del valor máximo
```

FUSIONAR Y ACTUALIZAR DICCIONARIOS

```python
a = {"x": 1, "y": 2}
b = {"y": 20, "z": 30}
a | b  # {'x': 1, 'y': 20, 'z': 30} (Python 3.9+; gana el de la derecha)
{**a, **b}  # lo mismo en versiones anteriores
a |= b  # actualiza a (igual que a.update(b))

# Sumar valores de claves repetidas
from collections import Counter

Counter(a) + Counter(b)
```

ACCEDER A DATOS ANIDADOS SIN ERRORES

```python
usuario = {"perfil": {"direccion": {"ciudad": "Madrid"}}}
usuario.get("perfil", {}).get("direccion", {}).get("ciudad")  # 'Madrid' o None


def obtener(datos, *claves, defecto=None):
    for clave in claves:
        try:
            datos = datos[clave]
        except (KeyError, IndexError, TypeError):
            return defecto
    return datos


obtener(usuario, "perfil", "direccion", "ciudad")
```

CONVERTIR ENTRE LISTAS, TEXTOS Y DICCIONARIOS

```python
" ".join(["hola", "mundo"])  # lista → texto
"a,b,c".split(",")  # texto → lista
list("hola")  # ['h', 'o', 'l', 'a']
dict(zip(["a", "b"], [1, 2]))  # dos listas → dict {'a': 1, 'b': 2}
list(d.items())  # dict → lista de tuplas
dict([("a", 1), ("b", 2)])  # lista de pares → dict
list(map(int, "1 2 3".split()))  # [1, 2, 3]
str([1, 2])  # '[1, 2]'
import ast

ast.literal_eval("[1, 2, 3]")  # texto con una lista de Python → lista (seguro; nunca eval)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CÓMO HAGO: TEXTOS, NÚMEROS Y FICHEROS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTAR PALABRAS Y LETRAS

```python
texto = "el gato y el perro"
len(texto.split())  # 5 palabras
from collections import Counter

Counter(texto.split()).most_common(1)  # [('el', 2)]
Counter(c for c in texto if c.isalpha())  # frecuencia de cada letra
texto.count("el")  # 2 (cuenta subcadenas, también dentro de palabras)
```

COMPROBAR SI UN TEXTO ES UN NÚMERO

```python
def es_numero(texto: str) -> bool:
    try:
        float(texto.replace(",", "."))
        return True
    except ValueError:
        return False


"42".isdigit()  # True, pero "-5" y "3.5" dan False → mejor intentar convertir
```

VALIDAR UN EMAIL, UN DNI O UN TELÉFONO

```python
import re


def email_valido(email: str) -> bool:
    # Comprobación razonable de formato; la única prueba real es enviar un correo
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}", email) is not None


def dni_valido(dni: str) -> bool:
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    dni = dni.upper().replace("-", "").replace(" ", "")
    if not re.fullmatch(r"\d{8}[A-Z]", dni):
        return False
    return letras[int(dni[:8]) % 23] == dni[8]


def telefono_es(telefono: str) -> bool:  # móviles y fijos españoles de 9 cifras
    limpio = re.sub(r"[\s\-]", "", telefono).removeprefix("+34")
    return re.fullmatch(r"[6789]\d{8}", limpio) is not None
```

FORMATEAR DINERO Y PORCENTAJES EN ESPAÑOL

```python
def euros(cantidad: float) -> str:
    texto = f"{cantidad:,.2f}"  # '1,234.50'
    return texto.replace(",", "_").replace(".", ",").replace("_", ".") + " €"


euros(1234.5)  # '1.234,50 €'
f"{0.215:.1%}".replace(".", ",")  # '21,5%'
```

LEER Y ESCRIBIR UN FICHERO DE TEXTO SIN COMPLICACIONES

```python
from pathlib import Path

texto = Path("notas.txt").read_text(encoding="utf-8")  # todo de una vez
lineas = Path("notas.txt").read_text(encoding="utf-8").splitlines()
Path("salida.txt").write_text("hola\n", encoding="utf-8")  # sobrescribe

with open("registro.txt", "a", encoding="utf-8") as f:  # añadir al final
    f.write("nueva línea\n")

if Path("config.json").exists():  # comprobar si existe
    ...
```

RECORRER TODOS LOS FICHEROS DE UNA CARPETA

```python
from pathlib import Path

for ruta in Path("documentos").rglob("*.pdf"):  # incluye subcarpetas
    print(ruta.name, ruta.stat().st_size)

# Renombrar en bloque: foto1.jpg → vacaciones_001.jpg
for i, ruta in enumerate(sorted(Path("fotos").glob("*.jpg")), start=1):
    ruta.rename(ruta.with_name(f"vacaciones_{i:03d}.jpg"))
```

EJECUTAR ALGO CADA CIERTO TIEMPO

```python
import time

while True:
    comprobar_algo()
    time.sleep(60)  # cada minuto (el programa debe seguir abierto)
```

Para tareas programadas de verdad: el Programador de tareas de Windows, `cron` en Linux/macOS,
la librería `schedule` (`schedule.every().day.at("09:00").do(tarea)`) o, en servidores,
herramientas como systemd timers o Celery.

CONVERTIR UN SCRIPT EN UN EJECUTABLE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed mi_app.py      # crea dist/mi_app.exe (Windows)
```

`--windowed` oculta la consola en programas con ventana. El ejecutable se crea para el sistema en
el que lo generas (para Windows hay que generarlo en Windows). Algunos antivirus marcan como
sospechosos los ejecutables de PyInstaller sin firmar. Alternativas: Nuitka (compila a C) o
publicar el programa como paquete instalable con `pipx`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APRENDER Y TRABAJAR CON PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CÓMO PRACTICAR PARA AVANZAR

- Escribe código cada día aunque sean 20 minutos; leer o ver vídeos sin programar avanza poco.
- Antes de mirar una solución, intenta el problema al menos 15-20 minutos y escribe en papel qué
  pasos seguirías.
- Cuando algo funcione, pregúntate por qué; cuando falle, lee el error entero.
- Haz proyectos pequeños que te sirvan de verdad: renombrar fotos, controlar gastos, un bot de
  avisos. Se aprende más terminando proyectos pequeños que empezando uno enorme.
- Lee código de otros (librerías conocidas, soluciones de ejercicios) y reescribe el tuyo cuando
  aprendas una forma mejor.
- Usa la IA como profesor (pide que te explique el error o que te dé pistas), no para que te dé el
  código hecho: si no lo escribes tú, no lo aprendes.

QUÉ ESTUDIAR SEGÚN EL OBJETIVO

- Automatizar tareas: ficheros, pathlib, csv/json, Excel (openpyxl, pandas), requests, Selenium o
  Playwright, programar tareas.
- Desarrollo web backend: HTTP, FastAPI o Django, SQL y un ORM, autenticación, tests, Docker y
  despliegue.
- Datos: pandas o Polars, visualización (matplotlib, seaborn), SQL, estadística básica, Jupyter.
- Machine learning e IA: NumPy, pandas, scikit-learn, después PyTorch; y para aplicaciones con
  modelos de lenguaje, sus APIs, RAG y evaluación.
- Sistemas y DevOps: scripts, subprocess, SSH (paramiko, fabric), Ansible, contenedores, cloud.

CÓMO PEDIR AYUDA CON UN ERROR

Una buena pregunta incluye: qué intentas conseguir, el código mínimo que reproduce el problema,
el traceback completo (copiado como texto, no en captura), qué esperabas que pasara y qué has
probado ya. Muchas veces, al preparar esa información, encuentras tú mismo el fallo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOVEDADES RECIENTES DE PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYTHON 3.13 (OCTUBRE DE 2024)

- REPL nuevo: edición multilínea, historial, colores y `exit` sin paréntesis.
- Mensajes de error con colores en la terminal.
- Versión experimental sin GIL («free-threaded», `python3.13t`).
- Compilador JIT experimental (desactivado por defecto).
- `copy.replace()` para crear copias modificadas de objetos inmutables, como dataclasses frozen.
- `typing.TypeIs` y valores por defecto en parámetros de tipo.
- Se eliminan módulos antiguos («dead batteries»): `cgi`, `crypt`, `telnetlib`, `imghdr` y otros.

PYTHON 3.14 (OCTUBRE DE 2025)

- Plantillas t-strings (PEP 750): `t"Hola {nombre}"` crea un objeto `Template` en vez de un texto,
  para que una librería pueda procesar los valores con seguridad (escapar HTML o SQL).
- Anotaciones diferidas (PEP 649): se evalúan solo cuando se piden; ya no hace falta poner entre
  comillas los nombres que se definen más abajo.
- `except A, B:` sin paréntesis cuando no lleva `as` (PEP 758).
- La versión sin GIL pasa a tener soporte oficial (sigue siendo una compilación opcional).
- Varios intérpretes en un mismo proceso desde Python (`concurrent.interpreters`, PEP 734).
- `compression.zstd` (compresión Zstandard) en la biblioteca estándar, y `uuid.uuid7()`.
- Colores en el REPL (resaltado de sintaxis) y en la salida de `argparse` y `unittest`.

QUÉ VERSIÓN DE PYTHON USAR

Usa una versión con soporte que admitan tus librerías: en general, la última o la anterior.
Cada versión recibe correcciones durante unos 2 años y parches de seguridad hasta los 5 años; una
versión nueva sale cada octubre. Las librerías con partes en C (científicas, de IA) a veces tardan
unas semanas en publicar paquetes para la versión nueva. Comprueba la tuya con `python --version`
y escribe código compatible con la mínima que declares en `requires-python`.
