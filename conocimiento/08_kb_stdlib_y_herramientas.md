# CONOCIMIENTO 7 — BIBLIOTECA ESTÁNDAR Y HERRAMIENTAS
# Base de conocimiento para pAIthon Teacher.
# Módulos de la biblioteca estándar explicados con ejemplos, entornos, empaquetado e interfaces.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROGRAMAS DE LÍNEA DE COMANDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ARGPARSE: ARGUMENTOS DE UN SCRIPT

```python
import argparse

parser = argparse.ArgumentParser(description="Redimensiona imágenes de una carpeta.")
parser.add_argument("carpeta", help="carpeta con las imágenes")  # obligatorio
parser.add_argument("-a", "--ancho", type=int, default=800, help="ancho en píxeles")
parser.add_argument("-v", "--verbose", action="store_true", help="más mensajes")
parser.add_argument("--formato", choices=["jpg", "png", "webp"], default="jpg")
parser.add_argument("--extensiones", nargs="+", default=[".jpg"])  # uno o más valores
args = parser.parse_args()

print(args.carpeta, args.ancho, args.verbose)
```

```bash
python redimensionar.py fotos --ancho 1200 -v
python redimensionar.py --help        # ayuda generada automáticamente
```

Para subcomandos (`git commit`, `git push`) se usa `parser.add_subparsers()`. Para CLIs más
cómodas existen `typer` y `click` (ver el apartado de CLI tools).

SYS: ARGV, EXIT, STDIN Y PLATAFORMA

```python
import sys

sys.argv  # ['script.py', 'arg1', 'arg2'] → argumentos sin procesar
sys.exit(0)  # terminar el programa (0 = bien; otro número = error)
sys.exit("Falta el fichero")  # imprime el mensaje en stderr y sale con código 1
sys.version  # versión de Python
sys.version_info >= (3, 10)
sys.platform  # 'win32', 'linux', 'darwin' (macOS)
sys.executable  # ruta del intérprete que se está usando (útil con entornos virtuales)
sys.stderr.write("Error\n")  # o print("Error", file=sys.stderr)

for linea in sys.stdin:  # leer lo que llega por tubería: cat datos.txt | python script.py
    procesar(linea.rstrip("\n"))
```

`exit()` y `quit()` están pensados para el REPL; en scripts usa `sys.exit()`.

LIMPIAR LA PANTALLA, PAUSAR Y LEER CONTRASEÑAS

```python
import os, time, getpass

os.system("cls" if os.name == "nt" else "clear")  # limpiar la consola
time.sleep(1.5)  # esperar 1,5 segundos
input("Pulsa Intro para continuar...")  # pausar hasta que el usuario pulse Intro
clave = getpass.getpass("Contraseña: ")  # no se ve lo que se escribe
```

Para colores y tablas en la terminal: la librería `rich` (`from rich import print`).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FECHAS Y HORAS EN DETALLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ZONAS HORARIAS CON ZONEINFO

Una fecha «naive» no tiene zona horaria; una «aware» sí. Mezclarlas da
`TypeError: can't compare offset-naive and offset-aware datetimes`.

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python 3.9+ (en Windows: pip install tzdata)

ahora_utc = datetime.now(timezone.utc)
madrid = datetime.now(ZoneInfo("Europe/Madrid"))
canarias = madrid.astimezone(ZoneInfo("Atlantic/Canary"))

reunion = datetime(2026, 3, 29, 10, 0, tzinfo=ZoneInfo("Europe/Madrid"))  # tiene en cuenta el cambio de hora
reunion.utcoffset()  # 2:00:00 (horario de verano)

# datetime.utcnow() está obsoleto desde 3.12: usa datetime.now(timezone.utc)
```

Buena práctica: guardar y calcular en UTC, y convertir a la hora local solo para mostrar.

ISO 8601, TIMESTAMPS Y PARSEO

```python
from datetime import datetime, date

datetime.now().isoformat()  # '2026-10-05T14:30:00.123456'
datetime.fromisoformat("2026-10-05T14:30:00+02:00")
date.fromisoformat("2026-10-05")

import time

time.time()  # segundos desde 1970 (timestamp Unix)
datetime.fromtimestamp(1700000000, tz=timezone.utc)
datetime.now().timestamp()

datetime.strptime("05/10/2026 14:30", "%d/%m/%Y %H:%M")
# Códigos: %Y año, %m mes, %d día, %H hora 24h, %I hora 12h, %M minutos, %S segundos,
# %A nombre del día, %B nombre del mes, %j día del año, %W semana del año, %z desfase horario
```

Los nombres de días y meses de `strftime` salen en inglés salvo que cambies el `locale`; para
español es más fiable una lista propia:

```python
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
DIAS[date.today().weekday()]  # weekday(): lunes = 0
```

OPERACIONES HABITUALES CON FECHAS

```python
from datetime import date, timedelta
import calendar

hoy = date.today()
nacimiento = date(1995, 7, 20)

# Edad exacta
edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

(date(2026, 12, 25) - hoy).days  # días hasta Navidad
hoy + timedelta(days=30)  # dentro de 30 días
hoy.isoweekday()  # lunes = 1 ... domingo = 7
hoy.isocalendar().week  # número de semana ISO
calendar.isleap(2028)  # True: año bisiesto
calendar.monthrange(2026, 2)  # (6, 28): día de la semana del día 1 y días del mes
print(calendar.month(2026, 10))  # calendario del mes en texto

# Sumar meses: timedelta no tiene meses → dateutil (pip install python-dateutil)
from dateutil.relativedelta import relativedelta

hoy + relativedelta(months=1)


# Días laborables entre dos fechas (sin festivos)
def laborables(desde: date, hasta: date) -> int:
    dias = (hasta - desde).days
    return sum(1 for i in range(dias) if (desde + timedelta(i)).weekday() < 5)
```

MEDIR CUÁNTO TARDA UN CÓDIGO

```python
import time

inicio = time.perf_counter()  # el reloj más preciso para medir duraciones
hacer_algo()
print(f"Tardó {time.perf_counter() - inicio:.3f} s")

time.monotonic()  # nunca retrocede (para timeouts)
time.time()  # hora real (puede saltar si se ajusta el reloj)
```

Para comparar fragmentos pequeños, `timeit` repite el código muchas veces. Y para saber qué
parte de un programa lento es la que tarda, no midas a mano: usa un profiler, que mide todas las
funciones a la vez.

```bash
python -m cProfile -s cumulative mi_script.py   # tiempo por función, de más a menos
pip install line_profiler                      # o línea a línea dentro de una función
```

El apartado de rendimiento y profiling explica cómo leer los resultados y cómo optimizar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATOS EN FICHEROS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

JSON EN DETALLE

```python
import json
from pathlib import Path

datos = {"nombre": "José", "edad": 30, "aficiones": ["leer", "correr"]}

texto = json.dumps(datos, ensure_ascii=False, indent=2)  # sin ensure_ascii la é sale como é
Path("datos.json").write_text(texto, encoding="utf-8")
cargado = json.loads(Path("datos.json").read_text(encoding="utf-8"))

with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
with open("datos.json", encoding="utf-8") as f:
    cargado = json.load(f)

# Tipos que JSON no admite directamente: fechas, Decimal, sets, objetos propios
from datetime import datetime


def convertir(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, set):
        return sorted(obj)
    raise TypeError(f"No se puede convertir {type(obj).__name__}")


json.dumps({"cuando": datetime.now()}, default=convertir)

json.dumps(datos, sort_keys=True, separators=(",", ":"))  # compacto y ordenado
```

Equivalencias: dict ↔ objeto, list ↔ array, str ↔ string, int/float ↔ número,
True/False ↔ true/false, None ↔ null. Las tuplas se guardan como listas y las claves siempre como
texto. Un JSON mal formado da `json.JSONDecodeError`, que indica la línea y la columna.

CSV EN DETALLE

```python
import csv

# Leer como diccionarios (la primera fila son los nombres de las columnas)
with open("clientes.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["nombre"], fila["email"])

# Escribir diccionarios
campos = ["nombre", "email"]
with open("salida.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(lista_de_dicts)

# CSV de Excel en español: separador ; y encoding con BOM
with open("excel.csv", newline="", encoding="utf-8-sig") as f:
    lector = csv.reader(f, delimiter=";")
```

- Pon siempre `newline=""` al abrir un CSV: sin él aparecen líneas en blanco de más en Windows.
- Todos los valores se leen como texto: convierte con `int()`, `float()` o `Decimal()`.
- Los decimales con coma («3,5») hay que convertirlos: `float(valor.replace(",", "."))`.
- Para análisis de datos, `pandas.read_csv` es más cómodo.

SQLITE3: BASE DE DATOS EN UN FICHERO

```python
import sqlite3

con = sqlite3.connect("tienda.db")  # crea el fichero si no existe
con.row_factory = sqlite3.Row  # filas accesibles por nombre de columna

con.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
    )
""")

# Parámetros con ? : NUNCA construyas el SQL con f-strings (inyección SQL)
with con:  # confirma (commit) al salir, o deshace si hay error
    con.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ("Taza", 6.5))
    con.executemany("INSERT INTO productos (nombre, precio) VALUES (?, ?)", [("Plato", 4.0), ("Vaso", 2.5)])

for fila in con.execute("SELECT * FROM productos WHERE precio < ?", (5,)):
    print(fila["nombre"], fila["precio"])

uno = con.execute("SELECT * FROM productos WHERE id = ?", (1,)).fetchone()
todos = con.execute("SELECT nombre FROM productos").fetchall()
con.close()  # el with de arriba confirma, pero no cierra
```

Ojo con `(5,)`: un solo parámetro necesita la coma para ser una tupla. SQLite viene incluido en
Python y basta para aplicaciones pequeñas y medianas; para muchos usuarios a la vez, PostgreSQL.

PICKLE Y SHELVE

```python
import pickle

with open("estado.pkl", "wb") as f:
    pickle.dump(objeto, f)  # guarda casi cualquier objeto de Python
with open("estado.pkl", "rb") as f:
    objeto = pickle.load(f)
```

Nunca cargues un pickle de una fuente que no controlas: al cargarlo puede ejecutar código
arbitrario. Para intercambiar datos usa JSON. `shelve` ofrece un diccionario persistente en disco
basado en pickle (`with shelve.open("datos") as db: db["clave"] = valor`).

CONFIGURACIÓN: TOML, INI Y VARIABLES DE ENTORNO

```python
import tomllib  # Python 3.11+, solo lectura

with open("config.toml", "rb") as f:  # se abre en binario
    config = tomllib.load(f)

import configparser  # ficheros .ini

cp = configparser.ConfigParser()
cp.read("config.ini", encoding="utf-8")
cp["basedatos"]["host"]
cp.getint("basedatos", "puerto")

import os

os.environ.get("API_KEY")  # None si no existe
os.environ["API_KEY"]  # KeyError si no existe

# Fichero .env (pip install python-dotenv)
from dotenv import load_dotenv

load_dotenv()  # carga las variables de .env en os.environ
```

Las contraseñas y claves van en variables de entorno o en un `.env` incluido en `.gitignore`,
nunca escritas en el código.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FICHEROS Y CARPETAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PATHLIB EN DETALLE

```python
from pathlib import Path

p = Path("informes") / "2026" / "octubre.pdf"
p.name  # 'octubre.pdf'
p.stem  # 'octubre'
p.suffix  # '.pdf'
p.parent  # Path('informes/2026')
p.with_suffix(".txt")
p.with_name("noviembre.pdf")
p.exists(), p.is_file(), p.is_dir()
p.stat().st_size  # tamaño en bytes
p.resolve()  # ruta absoluta

carpeta = Path("fotos")
list(carpeta.glob("*.jpg"))  # en esa carpeta
list(carpeta.rglob("*.jpg"))  # también en subcarpetas
[f for f in carpeta.iterdir() if f.is_file()]

p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hola", encoding="utf-8")
p.read_text(encoding="utf-8")
p.rename("nuevo.txt")
p.unlink(missing_ok=True)  # borrar fichero
Path("vacia").rmdir()  # borrar carpeta vacía

# Ruta relativa al propio script (no a la carpeta desde la que se ejecuta)
BASE = Path(__file__).resolve().parent
datos = BASE / "datos" / "clientes.csv"
```

SHUTIL: COPIAR, MOVER Y BORRAR CARPETAS

```python
import shutil

shutil.copy("a.txt", "copia/")  # copia el fichero
shutil.copy2("a.txt", "b.txt")  # copia también la fecha de modificación
shutil.copytree("proyecto", "copia_proyecto")
shutil.move("a.txt", "archivo/a.txt")
shutil.rmtree("carpeta")  # borra la carpeta y TODO su contenido, sin papelera
shutil.make_archive("copia", "zip", "proyecto")  # crea copia.zip
shutil.disk_usage("/")  # espacio total, usado y libre
shutil.which("git")  # ruta del programa o None
```

FICHEROS TEMPORALES Y ZIP

```python
import tempfile, zipfile

with tempfile.TemporaryDirectory() as tmp:  # se borra al salir del with
    ruta = Path(tmp) / "prueba.txt"

with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
    f.write("a,b\n")

with zipfile.ZipFile("fotos.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for foto in Path("fotos").glob("*.jpg"):
        z.write(foto, arcname=foto.name)

with zipfile.ZipFile("fotos.zip") as z:
    z.namelist()
    z.extractall("destino")  # cuidado con zips de origen desconocido (rutas con ..)
```

LEER FICHEROS GRANDES Y BINARIOS

```python
# Línea a línea sin cargar todo en memoria
with open("enorme.log", encoding="utf-8") as f:
    for linea in f:
        if "ERROR" in linea:
            print(linea.rstrip())

# Contar líneas
with open("enorme.log", encoding="utf-8") as f:
    total = sum(1 for _ in f)

# Binario por bloques (por ejemplo, para calcular un hash)
import hashlib

h = hashlib.sha256()
with open("video.mp4", "rb") as f:
    while bloque := f.read(1024 * 1024):
        h.update(bloque)
print(h.hexdigest())

# Las últimas líneas de un fichero
from collections import deque

with open("app.log", encoding="utf-8") as f:
    ultimas = deque(f, maxlen=10)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEGURIDAD, HASHES Y CODIFICACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HASHLIB: HUELLAS DE DATOS

```python
import hashlib

hashlib.sha256("hola".encode()).hexdigest()  # siempre 64 caracteres hexadecimales
hashlib.md5(datos).hexdigest()  # MD5 y SHA-1: solo para comprobar errores, no seguridad
hashlib.file_digest(open("f.zip", "rb"), "sha256").hexdigest()  # Python 3.11+
```

Un hash es de un solo sentido: no se puede «descifrar». Sirve para comprobar que un fichero no ha
cambiado o para identificar contenidos.

GUARDAR CONTRASEÑAS CORRECTAMENTE

Nunca guardes contraseñas en texto plano ni con un hash simple (`sha256(contraseña)`): se rompen
con diccionarios. Usa un algoritmo lento y con sal:

```python
import hashlib, os, hmac


def crear_hash(contraseña: str) -> tuple[bytes, bytes]:
    sal = os.urandom(16)
    h = hashlib.scrypt(contraseña.encode(), salt=sal, n=2**14, r=8, p=1)
    return sal, h


def comprobar(contraseña: str, sal: bytes, h: bytes) -> bool:
    nuevo = hashlib.scrypt(contraseña.encode(), salt=sal, n=2**14, r=8, p=1)
    return hmac.compare_digest(nuevo, h)  # comparación en tiempo constante
```

En aplicaciones reales lo habitual es una librería: `argon2-cffi` o `bcrypt` (o `passlib`).

HMAC, BASE64 Y UUID

```python
import hmac, hashlib, base64, uuid

# HMAC: firmar un mensaje con una clave (verificar webhooks, tokens)
firma = hmac.new(b"clave_secreta", b"mensaje", hashlib.sha256).hexdigest()

# Base64: representar bytes como texto (NO es cifrado)
codificado = base64.b64encode(b"hola").decode()  # 'aG9sYQ=='
base64.b64decode(codificado)  # b'hola'
base64.urlsafe_b64encode(datos)

uuid.uuid4()  # identificador aleatorio único: UUID('3f2b...')
str(uuid.uuid4())
uuid.uuid7()  # Python 3.14+: ordenado por tiempo (bueno como clave de base de datos)
```

CIFRAR DATOS

La biblioteca estándar no trae cifrado simétrico. Se usa la librería `cryptography`:

```python
from cryptography.fernet import Fernet  # pip install cryptography

clave = Fernet.generate_key()  # guárdala en lugar seguro
f = Fernet(clave)
token = f.encrypt(b"datos secretos")
f.decrypt(token)  # b'datos secretos'
```

No inventes tus propios algoritmos de cifrado: usa librerías revisadas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RED E INTERNET CON LA BIBLIOTECA ESTÁNDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

URLLIB: PETICIONES SIN INSTALAR NADA

```python
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse, quote
import json

with urlopen("https://api.github.com/repos/python/cpython", timeout=10) as r:
    datos = json.load(r)

peticion = Request(
    "https://httpbin.org/post",
    data=json.dumps({"a": 1}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urlopen(peticion) as r:
    print(r.status)

urlencode({"q": "café con leche", "page": 2})  # 'q=caf%C3%A9+con+leche&page=2'
urlparse("https://web.es/ruta?x=1").netloc  # 'web.es'
quote("año 2026")  # 'a%C3%B1o%202026'
```

Para algo más que lo básico, `requests` o `httpx` son mucho más cómodos.

SERVIDOR WEB LOCAL Y SOCKETS

```bash
python -m http.server 8000      # sirve los ficheros de la carpeta actual en http://localhost:8000
```

```python
import socket


# Comprobar si un puerto está abierto
def puerto_abierto(host: str, puerto: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, puerto)) == 0


socket.gethostbyname("python.org")  # resolver un nombre a IP
```

Solo escanea equipos propios o con permiso.

ENVIAR CORREOS CON SMTPLIB

```python
import smtplib, os
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Informe semanal"
msg["From"] = "yo@ejemplo.es"
msg["To"] = "ana@ejemplo.es"
msg.set_content("Te adjunto el informe.")
with open("informe.pdf", "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="informe.pdf")

with smtplib.SMTP_SSL("smtp.ejemplo.es", 465) as servidor:
    servidor.login("yo@ejemplo.es", os.environ["SMTP_PASSWORD"])
    servidor.send_message(msg)
```

Con Gmail hace falta una «contraseña de aplicación» (con la verificación en dos pasos activada),
no la contraseña normal. Para puerto 587 se usa `smtplib.SMTP(...)` seguido de `starttls()`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OTROS MÓDULOS ÚTILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COPY: COPIA SUPERFICIAL Y PROFUNDA

```python
import copy

original = {"nombre": "Ana", "notas": [7, 8]}
superficial = copy.copy(original)  # copia el dict, pero comparte la lista de dentro
profunda = copy.deepcopy(original)  # copia también todo lo anidado

superficial["notas"].append(10)  # ¡también cambia original["notas"]!
profunda["notas"].append(10)  # no afecta a original

# Copias superficiales rápidas
lista[:]  # o list(lista) o lista.copy()
dict(original)  # o original.copy()
```

PPRINT, DIFFLIB Y STRING

```python
from pprint import pprint

pprint(datos_anidados, width=60)  # imprime estructuras grandes de forma legible

import difflib

difflib.get_close_matches("pyton", ["python", "java", "ruby"])  # ['python'] → sugerencias
difflib.SequenceMatcher(None, "casa", "cosa").ratio()  # 0.75 → parecido entre textos
for linea in difflib.unified_diff(viejo.splitlines(), nuevo.splitlines(), lineterm=""):
    print(linea)  # diferencias como en git

import string

string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation
```

ENUMERATE, ZIP ESTRICTO E ITER CON CENTINELA

```python
for i, (a, b) in enumerate(zip(nombres, edades), start=1):
    print(i, a, b)

list(zip([1, 2, 3], "ab", strict=True))  # Python 3.10+: ValueError si las longitudes no coinciden

# iter con centinela: llamar a una función hasta que devuelva un valor concreto
with open("datos.bin", "rb") as f:
    for bloque in iter(lambda: f.read(4096), b""):
        procesar(bloque)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTS CON LA BIBLIOTECA ESTÁNDAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UNITTEST

```python
import unittest


def dividir(a, b):
    if b == 0:
        raise ValueError("División entre cero")
    return a / b


class TestDividir(unittest.TestCase):
    def setUp(self):  # antes de cada test
        self.datos = [1, 2, 3]

    def test_normal(self):
        self.assertEqual(dividir(10, 2), 5)

    def test_decimales(self):
        self.assertAlmostEqual(dividir(1, 3), 0.3333, places=4)

    def test_cero(self):
        with self.assertRaises(ValueError):
            dividir(1, 0)


if __name__ == "__main__":
    unittest.main()
```

```bash
python -m unittest discover -v      # busca y ejecuta los ficheros test*.py
```

pytest también ejecuta los tests de unittest, y con menos código (`assert` simple), por eso es
lo más usado hoy.

DOCTEST: EJEMPLOS QUE SON TESTS

```python
def cuadrado(n):
    """Devuelve n al cuadrado.

    >>> cuadrado(3)
    9
    >>> cuadrado(-2)
    4
    """
    return n * n


if __name__ == "__main__":
    import doctest

    doctest.testmod()  # comprueba que los ejemplos del docstring dan ese resultado
```

```bash
python -m doctest -v mi_modulo.py
pytest --doctest-modules
```

MOCK CON UNITTEST.MOCK

```python
from unittest.mock import patch, MagicMock


def obtener_usuario(id):
    import requests

    return requests.get(f"https://api.ejemplo.es/usuarios/{id}").json()


@patch("requests.get")
def test_obtener_usuario(mock_get):
    mock_get.return_value.json.return_value = {"id": 1, "nombre": "Ana"}
    assert obtener_usuario(1)["nombre"] == "Ana"
    mock_get.assert_called_once()
```

Regla de `patch`: se parchea el nombre donde se usa, no donde se define. Si tu módulo hace
`from requests import get`, hay que parchear `mi_modulo.get`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTORNOS, PAQUETES Y PUBLICACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENTORNOS VIRTUALES PASO A PASO

Un entorno virtual es una carpeta con su propio Python y sus propias librerías, para que cada
proyecto tenga sus versiones sin chocar con los demás.

```bash
python -m venv .venv                # crear (una vez por proyecto)

# Activar
.venv\Scripts\activate              # Windows (cmd o PowerShell)
source .venv/bin/activate           # macOS y Linux

python -m pip install requests      # instala dentro del entorno
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt   # en otro ordenador
deactivate                          # salir
```

- No subas `.venv` a git: añádelo a `.gitignore` y comparte `requirements.txt` o `pyproject.toml`.
- En PowerShell, si sale «la ejecución de scripts está deshabilitada»:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- En VS Code: Ctrl+Shift+P → «Python: Select Interpreter» → elige el de `.venv`.
- Con `uv` todo es más rápido: `uv venv`, `uv pip install`, o `uv init` y `uv add requests`.

PROBLEMAS FRECUENTES CON PIP

- `pip` instala en otro Python distinto del que ejecutas: usa siempre `python -m pip install ...`
  (con el mismo `python` que lanza tu programa).
- `error: externally-managed-environment` (Linux y Homebrew): el sistema protege su Python.
  Crea un entorno virtual; para herramientas de terminal, usa `pipx install herramienta`.
- `pip` no se reconoce como comando: Python no está en el PATH; usa `py -m pip` en Windows.
- Conflictos de versiones: crea un entorno nuevo; `pip check` muestra dependencias rotas.
- Actualizar: `python -m pip install --upgrade paquete`; ver lo instalado: `pip list`,
  `pip show paquete`.

PUBLICAR UN PAQUETE EN PYPI

```toml
# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mi-paquete"
version = "0.1.0"
description = "Lo que hace, en una frase."
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
dependencies = ["requests>=2.31"]

[project.scripts]
mi-comando = "mi_paquete.cli:main"      # crea un comando de terminal al instalar
```

```bash
python -m pip install build twine
python -m build                         # genera dist/*.whl y dist/*.tar.gz
twine upload --repository testpypi dist/*   # prueba primero en TestPyPI
twine upload dist/*
# Con uv: uv build y uv publish
```

Hoy se recomienda publicar desde GitHub Actions con «Trusted Publishing» (sin guardar tokens).
Cada versión publicada es definitiva: para corregir algo hay que subir una versión nueva.

VERSIONES SEMÁNTICAS

`MAYOR.MENOR.PARCHE` (por ejemplo 2.4.1):

- PARCHE: correcciones sin cambiar nada de la interfaz.
- MENOR: funciones nuevas compatibles con lo anterior.
- MAYOR: cambios que rompen el código de quien usa la librería.

En dependencias: `requests>=2.31,<3` permite actualizaciones sin saltar a la siguiente versión
mayor.

GIT PARA PROYECTOS PYTHON

```bash
git init
git add .
git commit -m "Primera versión"
git remote add origin https://github.com/usuario/proyecto.git
git push -u origin main
```

`.gitignore` mínimo para Python:

```text
.venv/
__pycache__/
*.pyc
.env
dist/
build/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

`__pycache__` contiene el bytecode compilado (`.pyc`) que Python genera para cargar los módulos
más rápido; se puede borrar sin problema y no se sube al repositorio.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERFACES GRÁFICAS Y JUEGOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TKINTER: VENTANAS SIN INSTALAR NADA

```python
import tkinter as tk
from tkinter import ttk, messagebox


def saludar():
    nombre = entrada.get().strip()
    if not nombre:
        messagebox.showwarning("Aviso", "Escribe tu nombre")
        return
    etiqueta.config(text=f"Hola, {nombre}")


ventana = tk.Tk()
ventana.title("Saludo")
ventana.geometry("300x150")

entrada = ttk.Entry(ventana)
entrada.pack(pady=10)
ttk.Button(ventana, text="Saludar", command=saludar).pack()  # command sin paréntesis
etiqueta = ttk.Label(ventana, text="")
etiqueta.pack(pady=10)

ventana.mainloop()  # bucle de eventos: sin esto la ventana se cierra al momento
```

- `command=saludar` pasa la función; `command=saludar()` la ejecutaría al crear el botón.
- Para colocar elementos: `pack()` (en fila o columna), `grid(row=0, column=1)` (tabla) o
  `place()` (coordenadas). No mezcles `pack` y `grid` en el mismo contenedor.
- Una tarea larga dentro de un botón congela la ventana: usa `ventana.after(ms, funcion)` o un
  hilo.
- Alternativas: `customtkinter` (aspecto moderno), PySide6/PyQt (aplicaciones grandes), Flet o
  NiceGUI (interfaces con tecnología web).

PYGAME: ESTRUCTURA DE UN JUEGO

```python
import pygame  # pip install pygame

pygame.init()
pantalla = pygame.display.set_mode((800, 600))
reloj = pygame.time.Clock()
x, y = 400, 300

ejecutando = True
while ejecutando:  # bucle del juego: eventos → lógica → dibujo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= 5
    if teclas[pygame.K_RIGHT]:
        x += 5

    pantalla.fill((30, 30, 30))
    pygame.draw.circle(pantalla, (255, 200, 0), (x, y), 20)
    pygame.display.flip()  # mostrar el fotograma
    reloj.tick(60)  # 60 fotogramas por segundo

pygame.quit()
```

Para detectar choques se usan rectángulos: `rect1.colliderect(rect2)`.

JUPYTER NOTEBOOKS

Los notebooks (`.ipynb`) mezclan código, resultados, gráficos y texto en celdas. Muy usados en
análisis de datos y para aprender.

```bash
pip install jupyterlab
jupyter lab
```

También se abren directamente en VS Code o en Google Colab (en el navegador, sin instalar nada).
Las celdas se pueden ejecutar en cualquier orden: si algo falla de forma rara, reinicia el kernel
y ejecuta todo de arriba abajo.
