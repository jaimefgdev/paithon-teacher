# CONOCIMIENTO 5 — FUNDAMENTOS AMPLIADOS
# Base de conocimiento para PyMentor.
# Completa los fundamentos: primeros pasos, números, textos, bytes, match, errores explicados y más.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIMEROS PASOS CON PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALAR PYTHON

- Windows: descarga el instalador de python.org (o la tienda de Microsoft). En el instalador marca
  «Add python.exe to PATH». Desde 2025 también existe el «Python install manager» (comando `py`),
  que permite tener varias versiones a la vez.
- macOS: instalador de python.org o Homebrew (`brew install python`). El `python3` que trae el
  sistema no conviene usarlo para tus proyectos.
- Linux: casi siempre viene instalado (`python3`). Para versiones nuevas: el gestor de paquetes de
  la distribución, `pyenv` o `uv python install 3.13`.

Comprobar la versión:

```bash
python --version      # Windows (o: py --version)
python3 --version     # macOS y Linux
```

Si en Windows escribes `python` y se abre la Microsoft Store, es que Python no está en el PATH:
reinstala marcando la casilla o usa el lanzador `py`.

EJECUTAR CÓDIGO: REPL, SCRIPTS E IDE

```bash
python                 # abre el intérprete interactivo (REPL): >>> 2 + 2
python mi_script.py    # ejecuta un fichero
python -m modulo       # ejecuta un módulo como programa (python -m pip, python -m venv...)
python -i script.py    # ejecuta y se queda en el REPL con las variables cargadas
```

En el REPL, `_` guarda el último resultado y `help(objeto)` muestra la ayuda. Para salir:
`exit()` o Ctrl+D (Ctrl+Z e Intro en Windows). Desde Python 3.13 el REPL tiene colores,
edición multilínea y acepta `exit` sin paréntesis.

Editores recomendados: VS Code con la extensión de Python (gratuito), PyCharm (Community es
gratuito), Thonny (pensado para principiantes, con depurador muy visual).

SINTAXIS BÁSICA: SANGRÍA, COMENTARIOS Y LÍNEAS LARGAS

Python usa la sangría (indentación) para delimitar bloques, en lugar de llaves. Lo estándar son
4 espacios por nivel. Mezclar tabuladores y espacios da `TabError`.

```python
if edad >= 18:
    print("Mayor de edad")  # dentro del if
    if edad >= 65:
        print("Jubilado")  # dentro del segundo if
print("Fin")  # fuera de los dos

# Esto es un comentario de una línea

"""Un string suelto entre triples comillas no es un comentario de verdad,
pero se usa como docstring al principio de módulos, clases y funciones."""
```

Cómo partir una línea larga y cómo no escribir varias sentencias juntas:

```python
# fmt: off
# Líneas largas: dentro de paréntesis, corchetes o llaves se puede partir libremente
total = (precio_base
         + impuestos
         - descuento)

# También con barra invertida (menos recomendable)
total = precio_base + \
        impuestos

# Varias sentencias en una línea (posible, pero desaconsejado)
x = 1; y = 2
# fmt: on
```

Las líneas `# fmt: off` y `# fmt: on` le dicen a los formateadores automáticos (ruff, black) que no
toquen ese trozo; aquí sirven para conservar los ejemplos tal cual.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NÚMEROS EN PROFUNDIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIVISIÓN ENTERA Y MÓDULO CON NEGATIVOS

```python
7 / 2  # 3.5   → la división / siempre devuelve float
7 // 2  # 3     → división entera (redondea hacia abajo, hacia -infinito)
7 % 2  # 1     → resto
-7 // 2  # -4    → ¡no -3! redondea hacia abajo
-7 % 2  # 1     → el resto tiene el signo del divisor
divmod(17, 5)  # (3, 2) → cociente y resto a la vez

# Saber si un número es par
n % 2 == 0

# Último dígito de un número
1234 % 10  # 4
# Quitar el último dígito
1234 // 10  # 123
```

ROUND() Y EL REDONDEO DEL BANQUERO

`round()` usa el «redondeo del banquero»: cuando el número está exactamente a mitad de camino,
redondea al par más cercano. Además, muchos decimales no se pueden representar exactos en float.

```python
round(2.5)  # 2   (no 3: redondea al par)
round(3.5)  # 4
round(0.5)  # 0
round(2.675, 2)  # 2.67 (2.675 en float es en realidad 2.67499999...)
round(3.14159, 2)  # 3.14

# Redondeo «escolar» (la mitad siempre hacia arriba): usar Decimal
from decimal import Decimal, ROUND_HALF_UP

Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)  # Decimal('3')
Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # Decimal('2.68')

# Para mostrar con 2 decimales no hace falta redondear: basta con formatear
f"{3.14159:.2f}"  # '3.14'

# Truncar, redondear arriba y abajo
import math

math.trunc(-3.7)  # -3  (quita los decimales)
math.floor(-3.7)  # -4  (hacia abajo)
math.ceil(3.2)  # 4   (hacia arriba)
int(3.99)  # 3   (int() trunca)
```

FLOAT: PRECISIÓN, INFINITO Y NAN

```python
0.1 + 0.2  # 0.30000000000000004
0.1 + 0.2 == 0.3  # False
import math

math.isclose(0.1 + 0.2, 0.3)  # True → así se comparan floats

float("inf")  # infinito
float("-inf")
float("nan")  # «not a number»
math.isinf(x), math.isnan(x)
float("nan") == float("nan")  # False: NaN no es igual ni a sí mismo

1e6  # 1000000.0 (notación científica)
1_000_000  # 1000000 (los guiones bajos solo ayudan a leer)
```

Los int de Python no tienen límite de tamaño (`2 ** 1000` funciona). Lo que sí está limitado,
por seguridad, es convertir a texto enteros de más de 4300 dígitos (`sys.set_int_max_str_digits`).

DECIMAL Y FRACTION: CUÁNDO USARLOS

```python
from decimal import Decimal, getcontext

# Para dinero: Decimal, creado SIEMPRE desde string
Decimal("0.1") + Decimal("0.2")  # Decimal('0.3')
Decimal(0.1)  # Decimal('0.1000000000000000055511...')  ← mal
precio = Decimal("19.99")
iva = (precio * Decimal("0.21")).quantize(Decimal("0.01"))  # Decimal('4.20')

getcontext().prec = 50  # precisión de los cálculos (dígitos significativos)

from fractions import Fraction

Fraction(1, 3) + Fraction(1, 6)  # Fraction(1, 2)
Fraction("0.75")  # Fraction(3, 4)
```

- float: cálculos científicos y generales, rápido.
- Decimal: dinero, facturas, cualquier cosa donde el céntimo importa.
- Fraction: fracciones exactas (matemáticas, enseñanza).

MÓDULO MATH

```python
import math

math.sqrt(16)  # 4.0
math.isqrt(17)  # 4 (raíz entera)
math.pow(2, 3)  # 8.0 (float); 2 ** 3 da 8 (int)
math.pi, math.e, math.tau
math.factorial(5)  # 120
math.gcd(12, 18)  # 6   (máximo común divisor)
math.lcm(4, 6)  # 12  (mínimo común múltiplo, 3.9+)
math.log(100, 10)  # 2.0
math.log2(8), math.log10(1000)
math.sin(math.radians(30))  # 0.49999999999999994
math.hypot(3, 4)  # 5.0
math.comb(5, 2)  # 10 (combinaciones)
math.perm(5, 2)  # 20 (variaciones)
math.prod([2, 3, 4])  # 24
math.dist((0, 0), (3, 4))  # 5.0

abs(-7)  # 7 (built-in)
pow(2, 10)  # 1024; pow(2, 10, 1000) = 24 (con módulo, muy eficiente)
```

BASES NUMÉRICAS: BINARIO, OCTAL Y HEXADECIMAL

```python
bin(10)  # '0b1010'
oct(8)  # '0o10'
hex(255)  # '0xff'
int("1010", 2)  # 10
int("ff", 16)  # 255
0b1010, 0o10, 0xFF  # literales: 10, 8, 255
f"{10:b}", f"{255:x}", f"{255:08b}"  # '1010', 'ff', '11111111'

# Operadores de bits
5 & 3  # 1  (AND)
5 | 3  # 7  (OR)
5 ^ 3  # 6  (XOR)
~5  # -6 (NOT)
1 << 3  # 8  (desplazar a la izquierda = multiplicar por 2^3)
16 >> 2  # 4
(255).bit_count()  # 8 (Python 3.10+)
```

NÚMEROS ALEATORIOS: RANDOM

```python
import random

random.random()  # float en [0.0, 1.0)
random.randint(1, 6)  # entero entre 1 y 6, AMBOS incluidos (dado)
random.randrange(0, 10, 2)  # 0, 2, 4, 6 u 8 (el final no se incluye)
random.uniform(1.5, 3.5)  # float entre 1.5 y 3.5
random.choice(["piedra", "papel", "tijera"])
random.choices(["a", "b"], weights=[90, 10], k=5)  # con repetición y pesos
random.sample(range(1, 50), 6)  # 6 distintos, sin repetición (lotería)
cartas = [1, 2, 3, 4]
random.shuffle(cartas)  # baraja EN EL SITIO, devuelve None

random.seed(42)  # misma semilla → misma secuencia (útil para tests)
```

`random` NO es seguro para contraseñas ni tokens: es predecible. Para eso, `secrets`.

SECRETS: ALEATORIEDAD SEGURA

```python
import secrets
import string

secrets.token_hex(16)  # 32 caracteres hexadecimales
secrets.token_urlsafe(32)  # token para enlaces de recuperación, API keys...
secrets.randbelow(100)  # entero seguro en [0, 100)
secrets.choice("abc")

# Generar una contraseña
alfabeto = string.ascii_letters + string.digits + string.punctuation
contraseña = "".join(secrets.choice(alfabeto) for _ in range(16))

secrets.compare_digest(a, b)  # comparar tokens sin filtrar información por el tiempo
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEXTOS AMPLIADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SECUENCIAS DE ESCAPE Y RAW STRINGS

```python
"Línea 1\nLínea 2"  # \n salto de línea

"Columna\tColumna"  # \t tabulador
'Comillas: "hola"'  # \" comilla doble
"It's"  # \' comilla simple (o usa "It's")
"Barra: \\"  # \\ una barra invertida
"\u00f1"  # 'ñ' (carácter Unicode por su código)

# Raw string: las barras invertidas no se interpretan
r"C:\Users\ana\nuevo"  # útil para rutas de Windows y expresiones regulares
# (una raw string no puede terminar en una sola barra invertida)
```

MÉTODOS DE STRING PARA COMPROBAR Y BUSCAR

```python
"123".isdigit()  # True
"12.5".isdigit()  # False → para decimales, intenta float() con try
"abc".isalpha()  # True
"abc123".isalnum()  # True
"   ".isspace()  # True
"Hola".istitle()  # True
"HOLA".isupper(), "hola".islower()

"banana".find("na")  # 2 (primera posición; -1 si no está)
"banana".rfind("na")  # 4 (última)
"banana".index("x")  # ValueError si no está (find devuelve -1)
"banana".count("a")  # 3
"informe.pdf".endswith((".pdf", ".doc"))  # True (acepta tupla)
"https://web.es".startswith("https")  # True

"nombre=Ana".partition("=")  # ('nombre', '=', 'Ana')
"a,b,,c".split(",")  # ['a', 'b', '', 'c']
"  varias   palabras ".split()  # ['varias', 'palabras'] (sin argumento: cualquier espacio)
"a,b,c".split(",", 1)  # ['a', 'b,c'] (máximo de cortes)
"línea1\nlínea2".splitlines()  # ['línea1', 'línea2']
```

METER VARIABLES DENTRO DE UN TEXTO CON F-STRINGS

Para poner el valor de una variable dentro de un texto, escribe una `f` delante de las comillas y
la variable entre llaves. Dentro de las llaves puede ir cualquier expresión.

```python
nombre = "Ana"
edad = 30
print(f"Hola, {nombre}. Tienes {edad} años.")  # Hola, Ana. Tienes 30 años.
print(f"El año que viene tendrás {edad + 1}")  # operaciones dentro de las llaves
print(f"Nombre en mayúsculas: {nombre.upper()}")  # métodos
print(f"Precio: {9.5:.2f} €")  # con formato: Precio: 9.50 €

# Sin f-string habría que convertir y concatenar a mano:
print("Hola, " + nombre + ". Tienes " + str(edad) + " años.")
```

Si olvidas la `f`, se imprimen las llaves tal cual: `"Hola {nombre}"`.

MÉTODOS DE STRING PARA TRANSFORMAR

Para quitar los espacios del principio y del final de un texto se usa `strip()` (o `lstrip()` y
`rstrip()` para un solo lado); para cambiar mayúsculas, `upper()`, `lower()` y `title()`; para
sustituir, `replace()`.

```python
"hola mundo".title()  # 'Hola Mundo'
"hola mundo".capitalize()  # 'Hola mundo'
"Hola".swapcase()  # 'hOLA'
"ß".casefold()  # 'ss' → para comparar sin mayúsculas mejor que lower()

"7".zfill(3)  # '007'
"hola".center(10, "*")  # '***hola***'
"hola".ljust(8, "."), "hola".rjust(8)

"  hola  ".strip()  # 'hola'  (también lstrip y rstrip)
"xxhola".strip("x")  # 'hola'  (quita esos caracteres por los extremos)
"informe.pdf".removesuffix(".pdf")  # 'informe' (3.9+)
"Sr. López".removeprefix("Sr. ")  # 'López'

"hola".replace("o", "0")  # 'h0la'
tabla = str.maketrans("áéíóú", "aeiou")
"canción".translate(tabla)  # 'cancion'

", ".join(["a", "b", "c"])  # 'a, b, c' (los elementos deben ser str)
", ".join(map(str, [1, 2, 3]))  # '1, 2, 3'
"hola"[::-1]  # 'aloh' (invertir)
```

QUITAR TILDES DE UN TEXTO

```python
import unicodedata


def sin_tildes(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


sin_tildes("Canción pequeña")  # 'Cancion pequena'  (la ñ también pierde la tilde)
```

Si quieres conservar la ñ, sustituye solo las vocales con `str.maketrans`.

FORMATO DE NÚMEROS CON F-STRINGS

```python
n = 1234567.891
f"{n:,.2f}"  # '1,234,567.89' (formato inglés)
f"{n:_.2f}"  # '1_234_567.89'
# Formato español (punto de miles y coma decimal):
f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  # '1.234.567,89'

f"{0.256:.1%}"  # '25.6%'
f"{42:05d}"  # '00042'
f"{3.5:+.1f}"  # '+3.5'
f"{1500000:.2e}"  # '1.50e+06'
f"{'texto':>10}"  # alineado a la derecha en 10 caracteres
f"{'texto':^10}"  # centrado
f"{'texto':*<10}"  # relleno con asteriscos

ancho = 8
f"{3.14159:{ancho}.2f}"  # especificaciones anidadas
```

Para formatos locales de verdad (moneda, miles según el país) se puede usar `locale` o la
librería `babel` (`format_currency(1234.5, "EUR", locale="es_ES")` → '1.234,50 €').

FORMATOS ANTIGUOS: PORCENTAJE Y FORMAT()

Verás código antiguo con estas formas; funcionan, pero hoy se prefieren las f-strings.

```python
"Hola, %s. Tienes %d años" % ("Ana", 30)
"Precio: %.2f" % 9.5
"Hola, {}. Tienes {} años".format("Ana", 30)
"Hola, {nombre}".format(nombre="Ana")
"{0} y {0}".format("eco")

# format() sigue siendo útil cuando la plantilla viene de fuera (un fichero, una traducción)
plantilla = "Estimado {nombre}: su pedido {pedido} ha salido."
plantilla.format(nombre="Ana", pedido=1234)
```

ORD(), CHR() Y COMPARAR TEXTOS

```python
ord("A")  # 65 (código Unicode)
chr(97)  # 'a'
"apple" < "banana"  # True (orden alfabético por código)
"Zeta" < "alfa"  # True: las mayúsculas van antes que las minúsculas
sorted(["b", "A", "c"], key=str.lower)  # ['A', 'b', 'c'] (ignorando mayúsculas)


# Cifrado César sencillo
def cesar(texto, desplazamiento):
    resultado = ""
    for c in texto:
        if c.isalpha() and c.isascii():
            base = ord("A") if c.isupper() else ord("a")
            resultado += chr((ord(c) - base + desplazamiento) % 26 + base)
        else:
            resultado += c
    return resultado
```

TEXTWRAP Y TEXTOS MULTILÍNEA

```python
import textwrap

textwrap.fill(texto_largo, width=40)  # parte en líneas de 40 caracteres
textwrap.shorten("Un texto bastante largo", width=15)  # 'Un texto [...]'
textwrap.dedent("""
    Quita la sangría
    común de todas las líneas
""")
textwrap.indent("a\nb", "> ")  # '> a\n> b'
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BYTES Y CODIFICACIÓN DE CARACTERES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STR FRENTE A BYTES

- `str`: texto (caracteres Unicode). Es lo que manejas casi siempre.
- `bytes`: secuencia de bytes (números de 0 a 255). Es lo que hay en ficheros binarios, redes,
  imágenes o en un texto antes de decodificarlo.

```python
texto = "año"
datos = texto.encode("utf-8")  # b'a\xc3\xb1o' → la ñ ocupa 2 bytes en UTF-8
datos.decode("utf-8")  # 'año'
len(texto), len(datos)  # 3, 4

b"hola"[0]  # 104 (un byte es un int)
bytes([72, 105])  # b'Hi'
bytearray(b"hola")  # versión mutable de bytes
"café".encode("ascii", errors="ignore")  # b'caf'
```

UNICODEDECODEERROR Y ENCODINGS

`UnicodeDecodeError: 'utf-8' codec can't decode byte...` significa que el fichero no está en
UTF-8 (suele ser Windows-1252/latin-1, típico de Excel y programas antiguos de Windows).

```python
# Indicar el encoding correcto al abrir
with open("datos.csv", encoding="latin-1") as f:
    ...

# CSV guardado por Excel con BOM al principio
open("datos.csv", encoding="utf-8-sig")

# Si no sabes el encoding, puedes reemplazar los caracteres que fallen
open("raro.txt", encoding="utf-8", errors="replace")
```

Regla de oro: dentro del programa trabaja con `str`; convierte a `bytes` solo al entrar y salir
(ficheros binarios, red), y especifica siempre el encoding. Está previsto que UTF-8 pase a ser
el encoding por defecto también en Windows (PEP 686), pero ponerlo explícito sigue siendo lo
correcto y funciona en todas las versiones.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTROL DE FLUJO AMPLIADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MATCH CASE: COINCIDENCIA DE PATRONES

Disponible desde Python 3.10. Es más que un «switch»: compara la forma de los datos.

```python
def comando(texto):
    match texto.split():
        case ["salir"] | ["exit"]:
            return "Adiós"
        case ["ir", direccion]:
            return f"Vas hacia {direccion}"
        case ["coger", *objetos]:
            return f"Coges: {', '.join(objetos)}"
        case _:
            return "No entiendo"


# Con valores sencillos (como un switch)
match codigo_http:
    case 200:
        print("OK")
    case 404:
        print("No encontrado")
    case 500 | 502 | 503:
        print("Error del servidor")
    case _:  # _ = cualquier otro caso (como «default»)
        print("Otro código")

# Con guardas (condición extra)
match punto:
    case (0, 0):
        print("Origen")
    case (x, 0) if x > 0:
        print("Eje X positivo")
    case (x, y):
        print(f"Punto {x}, {y}")

# Con diccionarios y clases
match evento:
    case {"tipo": "clic", "x": x, "y": y}:
        print(f"Clic en {x},{y}")
    case {"tipo": "tecla", "tecla": tecla}:
        print(f"Tecla {tecla}")

match figura:
    case Circulo(radio=r):
        area = 3.14 * r**2
    case Rectangulo(ancho=w, alto=h):
        area = w * h
```

Ojo: un nombre suelto en un `case` captura el valor, no lo compara. `case limite:` siempre
coincide; para comparar con una constante usa un nombre con punto (`case Config.LIMITE:`) o un
literal.

OPERADOR MORSA :=

El operador `:=` (Python 3.8+) asigna y devuelve el valor dentro de una expresión.

```python
# Sin morsa
linea = input()
while linea != "fin":
    procesar(linea)
    linea = input()

# Con morsa
while (linea := input()) != "fin":
    procesar(linea)

# Evitar calcular dos veces
if (n := len(datos)) > 10:
    print(f"Demasiados datos ({n})")

# En comprehensions
resultados = [y for x in valores if (y := transformar(x)) is not None]

# Con expresiones regulares
if m := re.search(r"\d+", texto):
    print(m.group())
```

Úsalo cuando ahorre una repetición clara; abusar de él hace el código difícil de leer.

FOR Y WHILE: PATRONES ÚTILES

```python
# Recorrer al revés
for i in range(10, 0, -1):  # 10, 9, ..., 1
    ...
for x in reversed(lista):
    ...

# Recorrer de dos en dos
for i in range(0, len(lista), 2):
    ...

# Recorrer un diccionario ordenado por valor
for nombre, nota in sorted(notas.items(), key=lambda par: par[1], reverse=True):
    print(nombre, nota)


# Salir de dos bucles anidados: usar una función con return
def buscar(matriz, objetivo):
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor == objetivo:
                return i, j
    return None


# for ... else: el else se ejecuta si NO hubo break
for n in numeros:
    if n < 0:
        print("Hay un negativo")
        break
else:
    print("Todos son positivos")
```

PEDIR DATOS AL USUARIO HASTA QUE SEAN VÁLIDOS

```python
def pedir_entero(mensaje: str, minimo: int | None = None, maximo: int | None = None) -> int:
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("Escribe un número entero.")
            continue
        if minimo is not None and numero < minimo:
            print(f"Tiene que ser al menos {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"Tiene que ser como mucho {maximo}.")
        else:
            return numero


edad = pedir_entero("Edad: ", minimo=0, maximo=120)

# Pedir sí o no
respuesta = input("¿Continuar? (s/n): ").strip().lower()
if respuesta in ("s", "si", "sí"):
    ...

# Leer varios números en una línea: «3 5 8»
numeros = [int(x) for x in input("Números: ").split()]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESEMPAQUETADO Y ORDENACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESEMPAQUETADO AVANZADO

```python
a, b, c = [1, 2, 3]
primero, *resto = [1, 2, 3, 4]  # 1, [2, 3, 4]
*inicio, ultimo = [1, 2, 3, 4]  # [1, 2, 3], 4
primero, *_, ultimo = range(10)  # 0, 9 (el _ indica «no me interesa»)
(a, b), c = (1, 2), 3  # anidado

# Unir listas y diccionarios
combinada = [*lista1, *lista2, 99]
config = {**por_defecto, **del_usuario}  # las claves repetidas: gana la última
config = por_defecto | del_usuario  # lo mismo, Python 3.9+


# Pasar una lista como argumentos
def suma(a, b, c):
    return a + b + c


valores = [1, 2, 3]
suma(*valores)
datos = {"a": 1, "b": 2, "c": 3}
suma(**datos)

# Intercambiar
a, b = b, a
```

SORT FRENTE A SORTED Y ORDENAR CON KEY

```python
numeros = [3, 1, 2]
numeros.sort()  # ordena la lista EN EL SITIO y devuelve None
ordenados = sorted(numeros)  # devuelve una lista nueva; vale para cualquier iterable

# Error típico
numeros = numeros.sort()  # ¡numeros pasa a ser None!

sorted(palabras, key=len)  # por longitud
sorted(palabras, key=str.lower)  # sin distinguir mayúsculas
sorted(personas, key=lambda p: p["edad"])  # diccionarios por un campo
sorted(personas, key=lambda p: (-p["nota"], p["nombre"]))  # nota desc., nombre asc.

from operator import itemgetter, attrgetter

sorted(personas, key=itemgetter("edad"))  # igual que la lambda, algo más rápido
sorted(objetos, key=attrgetter("precio"))  # objetos por atributo

# Ordenar un diccionario por valor
dict(sorted(stock.items(), key=lambda par: par[1], reverse=True))

max(personas, key=lambda p: p["edad"])  # la persona de más edad
min(palabras, key=len)
```

La ordenación de Python es estable: si dos elementos empatan, conservan su orden original.
Por eso se puede ordenar en varias pasadas (primero por el criterio secundario y después por el
principal).

ANY, ALL, SUM Y OTRAS FUNCIONES SOBRE ITERABLES

```python
any(n < 0 for n in numeros)  # ¿hay algún negativo?
all(n > 0 for n in numeros)  # ¿son todos positivos? (con lista vacía: True)
sum(numeros)  # suma
sum(numeros) / len(numeros)  # media (cuidado con lista vacía: ZeroDivisionError)
sum(p["precio"] for p in productos)
sum(numeros, start=10)
max(numeros, default=0)  # con default no falla si está vacío

import statistics

statistics.mean([1, 2, 3, 4])  # 2.5
statistics.median([1, 5, 3])  # 3
statistics.mode(["a", "b", "a"])  # 'a'
statistics.stdev([2, 4, 4, 4, 5, 5, 7, 9])
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FUNCIONES AMPLIADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARÁMETROS SOLO POSICIONALES Y SOLO CON NOMBRE

```python
def f(a, b, /, c, *, d): ...


# a y b: solo por posición (antes de /), Python 3.8+
# c: por posición o por nombre
# d: solo por nombre (después de *)

f(1, 2, 3, d=4)  # bien
f(1, 2, c=3, d=4)  # bien
f(a=1, b=2, c=3, d=4)  # TypeError: a y b no admiten nombre
f(1, 2, 3, 4)  # TypeError: d hay que darlo por nombre


# Uso típico de *: obligar a que los parámetros de configuración se escriban con nombre
def enviar(destino, mensaje, *, reintentos=3, urgente=False): ...


enviar("ana@x.es", "hola", urgente=True)
```

DOCSTRINGS Y ANOTACIONES DE TIPO

```python
def area_rectangulo(ancho: float, alto: float) -> float:
    """Devuelve el área de un rectángulo.

    Args:
        ancho: ancho en metros.
        alto: alto en metros.

    Returns:
        El área en metros cuadrados.

    Raises:
        ValueError: si alguna medida es negativa.
    """
    if ancho < 0 or alto < 0:
        raise ValueError("Las medidas no pueden ser negativas")
    return ancho * alto


help(area_rectangulo)  # muestra el docstring
area_rectangulo.__doc__
```

Las anotaciones (`: float`, `-> float`) documentan y permiten que el editor y mypy detecten
errores, pero Python no las comprueba al ejecutar.

GLOBAL Y NONLOCAL

```python
contador = 0


def incrementar():
    global contador  # sin esto: UnboundLocalError al hacer contador += 1
    contador += 1


def crear_contador():
    cuenta = 0

    def siguiente():
        nonlocal cuenta  # modifica la variable de la función de fuera
        cuenta += 1
        return cuenta

    return siguiente


c = crear_contador()
c(), c(), c()  # 1, 2, 3
```

Leer una variable global dentro de una función no necesita `global`; solo asignarla. Aun así,
es mejor pasar valores como parámetros y devolver resultados que depender de variables globales.

RECURSIÓN

Una función recursiva se llama a sí misma. Necesita un caso base que detenga las llamadas.

```python
def factorial(n: int) -> int:
    if n <= 1:  # caso base
        return 1
    return n * factorial(n - 1)


def suma_digitos(n: int) -> int:
    return n if n < 10 else n % 10 + suma_digitos(n // 10)


# Recorrer estructuras anidadas (lo natural es recursivo)
def aplanar(lista):
    resultado = []
    for x in lista:
        if isinstance(x, list):
            resultado.extend(aplanar(x))
        else:
            resultado.append(x)
    return resultado


aplanar([1, [2, [3, 4]], 5])  # [1, 2, 3, 4, 5]
```

Python no optimiza la recursión de cola y tiene un límite de unas 1000 llamadas anidadas
(`sys.getrecursionlimit()`). Para profundidades grandes, usa un bucle. Si una recursión repite
cálculos (como Fibonacci), usa `functools.cache`.

FUNCIONES DE ORDEN SUPERIOR: MAP, FILTER Y REDUCE

```python
numeros = [1, 2, 3, 4, 5]

list(map(lambda x: x * 2, numeros))  # [2, 4, 6, 8, 10]
list(map(int, ["1", "2", "3"]))  # [1, 2, 3]
list(filter(lambda x: x % 2 == 0, numeros))  # [2, 4]
list(filter(None, ["a", "", "b", None]))  # ['a', 'b'] (quita los falsy)

from functools import reduce

reduce(lambda acc, x: acc * x, numeros, 1)  # 120 (producto)

# Normalmente es más legible una comprehension
[x * 2 for x in numeros]
[x for x in numeros if x % 2 == 0]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MODELO DE OBJETOS Y MUTABILIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VARIABLES COMO ETIQUETAS

En Python una variable es un nombre que apunta a un objeto; no es una caja que contiene el
valor. Asignar no copia: hace que otro nombre apunte al mismo objeto.

```python
a = [1, 2, 3]
b = a  # b y a son el MISMO objeto
b.append(4)
print(a)  # [1, 2, 3, 4]
a is b  # True
id(a) == id(b)  # True

x = 10
y = x
y += 1  # los int son inmutables: y pasa a apuntar a un objeto nuevo
print(x)  # 10
```

MUTABLES E INMUTABLES

- Inmutables: int, float, bool, str, tuple, frozenset, bytes, None. Cualquier «cambio» crea un
  objeto nuevo.
- Mutables: list, dict, set, bytearray y casi todos los objetos de tus clases.

```python
def añadir(lista, elemento):
    lista.append(elemento)  # modifica la lista original del que llama


def cambiar(numero):
    numero += 1  # no afecta al que llama: crea un int nuevo dentro
    return numero


# Una tupla es inmutable, pero si contiene una lista, esa lista sí se puede cambiar
t = ([1, 2], 3)
t[0].append(99)  # funciona: ([1, 2, 99], 3)
t[0] = []  # TypeError
```

En Python los argumentos se pasan «por referencia al objeto»: la función recibe el mismo objeto.
Si es mutable y la función lo modifica, el cambio se ve fuera.

HASHABLE: QUÉ PUEDE SER CLAVE DE DICCIONARIO

Las claves de un dict y los elementos de un set deben ser «hashables»: objetos inmutables cuyo
hash no cambia. str, int, float, tuple (si sus elementos son hashables) y frozenset sirven;
list, dict y set no.

```python
d = {(40.4, -3.7): "Madrid"}  # tupla como clave: bien
d = {[1, 2]: "x"}  # TypeError: unhashable type: 'list'
hash("hola")  # un número
{frozenset({1, 2}): "par"}  # set inmutable como clave
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXCEPCIONES AMPLIADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TRY, EXCEPT, ELSE Y FINALLY

```python
try:
    f = open("datos.txt", encoding="utf-8")
    datos = f.read()
except FileNotFoundError:
    print("No existe el fichero")
except (PermissionError, IsADirectoryError) as e:
    print(f"No se puede leer: {e}")
else:
    print("Leído sin errores")  # solo si no hubo excepción
finally:
    print("Esto se ejecuta siempre")  # haya error o no (liberar recursos)
```

- Captura excepciones concretas; `except Exception` solo en el nivel más alto del programa
  (para registrar el error) y nunca un `except:` vacío, que también atrapa Ctrl+C.
- Mete en el `try` solo las líneas que pueden fallar de esa forma.
- Desde Python 3.14 se pueden escribir varias excepciones sin paréntesis
  (`except ValueError, TypeError:`) siempre que no lleve `as`; con paréntesis funciona en todas
  las versiones.

RELANZAR Y ENCADENAR EXCEPCIONES

```python
try:
    procesar()
except ValueError:
    registrar_error()
    raise  # relanza la misma excepción, con su traza original


class ConfigError(Exception):
    pass


try:
    puerto = int(config["puerto"])
except (KeyError, ValueError) as e:
    raise ConfigError("Puerto mal configurado") from e  # conserva la causa original

# Ocultar la causa (poco habitual)
raise ConfigError("...") from None
```

EXCEPCIONES PERSONALIZADAS BIEN HECHAS

```python
class AppError(Exception):
    """Base de los errores de la aplicación."""


class SaldoInsuficiente(AppError):
    def __init__(self, saldo: float, importe: float):
        super().__init__(f"Saldo {saldo:.2f} insuficiente para {importe:.2f}")
        self.saldo = saldo
        self.importe = importe


try:
    raise SaldoInsuficiente(10, 25)
except SaldoInsuficiente as e:
    print(e)  # Saldo 10.00 insuficiente para 25.00
    print(e.importe)  # 25
except AppError:
    ...  # cualquier otro error propio
```

Hereda de `Exception` (no de `BaseException`) y crea una jerarquía con una clase base propia
para poder capturar todos tus errores a la vez.

EXCEPTIONGROUP, EXCEPT* Y ADD_NOTE

Desde Python 3.11, varias excepciones pueden lanzarse juntas (lo hacen `asyncio.TaskGroup` y
algunas librerías).

```python
try:
    raise ExceptionGroup("varios fallos", [ValueError("a"), TypeError("b")])
except* ValueError as grupo:
    print("Valores:", grupo.exceptions)
except* TypeError as grupo:
    print("Tipos:", grupo.exceptions)

# Añadir contexto a una excepción sin cambiarla
try:
    cargar(fila)
except ValueError as e:
    e.add_note(f"Fila {numero_fila} del CSV")
    raise
```

ASSERT

`assert condicion, "mensaje"` lanza `AssertionError` si la condición es falsa. Sirve para
comprobar suposiciones internas y en los tests de pytest, pero no para validar datos del usuario:
con `python -O` los assert se eliminan.

```python
def media(numeros):
    assert numeros, "la lista no puede estar vacía"  # comprobación interna
    return sum(numeros) / len(numeros)
```

WARNINGS: AVISOS SIN DETENER EL PROGRAMA

```python
import warnings


def funcion_antigua():
    warnings.warn("Usa funcion_nueva()", DeprecationWarning, stacklevel=2)


warnings.filterwarnings("ignore", category=DeprecationWarning)  # silenciar
# python -W error script.py → convierte los avisos en errores (útil en tests)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MENSAJES DE ERROR EXPLICADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CÓMO LEER UN TRACEBACK

El traceback se lee de abajo arriba: la última línea dice el tipo de error y el mensaje; justo
encima está la línea exacta donde ocurrió; más arriba, la cadena de llamadas que llevó hasta ahí.

```text
Traceback (most recent call last):
  File "app.py", line 10, in <module>
    total = calcular(datos)
  File "app.py", line 4, in calcular
    return sum(datos) / len(datos)
ZeroDivisionError: division by zero
```

Aquí el fallo está en la línea 4 (`len(datos)` era 0), llamada desde la línea 10. Las versiones
recientes de Python señalan con `^^^^` la parte exacta de la línea y sugieren correcciones
(«Did you mean...?»).

SYNTAXERROR E INDENTATIONERROR

- `SyntaxError: invalid syntax`: algo mal escrito. Lo típico: faltan los dos puntos al final de
  `if`, `for`, `def` o `class`; un paréntesis o comillas sin cerrar (el error suele marcarse en la
  línea siguiente); usar `=` en vez de `==` dentro de un `if`.
- `SyntaxError: '(' was never closed`: paréntesis abierto y sin cerrar.
- `IndentationError: expected an indented block`: después de `if ...:` no hay nada sangrado
  (si aún no tienes el código, pon `pass`).
- `IndentationError: unexpected indent`: una línea tiene sangría donde no toca.
- `TabError: inconsistent use of tabs and spaces`: mezclas tabuladores y espacios; configura el
  editor para insertar 4 espacios.

NAMEERROR Y UNBOUNDLOCALERROR

- `NameError: name 'x' is not defined`: usas un nombre que no existe en ese punto. Causas: error
  de escritura (`Print`, `lenght`), variable creada dentro de un `if` que no se ejecutó, olvidar
  las comillas en un texto (`print(hola)`), o falta un `import`.
- `UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`:
  asignas `x` dentro de la función, así que Python la trata como local en toda la función, y la
  lees antes de asignarla. Solución: pásala como parámetro, o usa `global`/`nonlocal` si de verdad
  quieres modificar la de fuera.

TYPEERROR: LOS MÁS COMUNES

- `can only concatenate str (not "int") to str`: `"Edad: " + 25`. Usa una f-string:
  `f"Edad: {25}"`, o `str(25)`.
- `unsupported operand type(s) for +: 'int' and 'str'`: sumas un número y un texto; muchas veces
  porque `input()` devuelve texto: convierte con `int()`.
- `'NoneType' object is not subscriptable` / `is not iterable`: la variable vale `None`. Suele
  ser una función sin `return`, o haber guardado el resultado de `lista.sort()` (que devuelve
  `None`).
- `'int' object is not callable`: usaste un nombre de función como variable (`sum = 0` y luego
  `sum(lista)`), o falta un operador: `2(3 + 4)` en vez de `2 * (3 + 4)`.
- `missing 1 required positional argument: 'x'`: llamas sin todos los argumentos. Si es un
  método, quizá llamaste a la clase en vez de a una instancia (`Clase.metodo()`).
- `takes 1 positional argument but 2 were given`: en un método olvidaste `self` en la definición.
- `unhashable type: 'list'`: usas una lista como clave de diccionario o elemento de set; usa una
  tupla.
- `'str' object does not support item assignment`: los strings son inmutables; crea uno nuevo.

VALUEERROR, KEYERROR E INDEXERROR

- `ValueError: invalid literal for int() with base 10: 'abc'`: `int()` recibió un texto que no es
  un número entero (también falla con `"3.5"` o `""`). Valida con `try/except`.
- `ValueError: too many values to unpack (expected 2)` o `not enough values`: el número de
  variables a la izquierda no coincide con los elementos. Típico al recorrer un dict sin
  `.items()`.
- `KeyError: 'nombre'`: la clave no existe en el diccionario. Usa `d.get("nombre")`,
  `d.get("nombre", valor_por_defecto)` o comprueba con `in`.
- `IndexError: list index out of range`: el índice no existe. Una lista de `n` elementos va del
  0 al `n - 1`; recorre con `for x in lista` en vez de con índices.

ATTRIBUTEERROR Y MODULENOTFOUNDERROR

- `AttributeError: 'list' object has no attribute 'add'`: ese tipo no tiene ese método (en
  listas es `append`; `add` es de los sets). Comprueba con `dir(objeto)`.
- `AttributeError: 'NoneType' object has no attribute ...`: la variable es `None` (ver TypeError).
- `AttributeError: module 'x' has no attribute 'y'`: a menudo has llamado a tu fichero igual que
  una librería (`random.py`, `json.py`, `requests.py`) y Python importa el tuyo. Cambia el nombre y
  borra la carpeta `__pycache__`.
- `ModuleNotFoundError: No module named 'requests'`: la librería no está instalada en el Python
  que ejecuta el programa. Instálala con `python -m pip install requests` usando el mismo
  intérprete (en VS Code, revisa qué intérprete o entorno virtual está seleccionado).

ERRORES DE FICHEROS Y DE RECURSIÓN

- `FileNotFoundError: [Errno 2] No such file or directory`: la ruta es relativa a la carpeta
  desde la que ejecutas el programa, no a la del script. Usa una ruta basada en el propio script:
  `Path(__file__).parent / "datos.txt"`.
- `PermissionError`: no tienes permiso, o el fichero está abierto en otro programa (por ejemplo,
  un Excel abierto en Windows).
- `RecursionError: maximum recursion depth exceeded`: recursión sin caso base, o demasiado
  profunda; revisa la condición de parada o usa un bucle.
- `ZeroDivisionError: division by zero`: dividir entre 0; comprueba antes el divisor.
- `KeyboardInterrupt`: has pulsado Ctrl+C; no es un fallo del programa.
- `MemoryError`: se ha quedado sin memoria; procesa los datos por partes o con generadores.
