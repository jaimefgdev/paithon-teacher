# CONOCIMIENTO 1 — FUNDAMENTOS DE PYTHON
# Base de conocimiento para pAIthon Teacher.
# Cubre todo lo que un alumno de nivel 0 a intermedio necesita.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUÉ ES PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python es un lenguaje de programación interpretado, de alto nivel y
propósito general creado por Guido van Rossum y publicado en 1991.

Características clave:
- Sintaxis limpia y legible (similar al pseudocódigo)
- Tipado dinámico y fuerte
- Gestión automática de memoria (garbage collector)
- Multiparadigma: imperativo, OOP, funcional
- Enorme biblioteca estándar ("batteries included")
- Comunidad masiva y ecosistema de librerías (PyPI: 500.000+ paquetes)

Usos principales:
- Automatización y scripting
- Desarrollo web (backend): Django, FastAPI, Flask
- Ciencia de datos y ML: NumPy, Pandas, scikit-learn, PyTorch
- DevOps y herramientas de sistema
- APIs y microservicios
- Aplicaciones de escritorio: tkinter, PyQt
- Seguridad y hacking ético
- Educación (es el lenguaje más enseñado del mundo)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VARIABLES Y TIPOS DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIPOS BÁSICOS

```python
# int — números enteros
edad = 25
temperatura = -3
año = 2024

# float — números decimales
precio = 9.99
pi = 3.14159
porcentaje = 0.15

# str — cadenas de texto
nombre = "Ana"
mensaje = "Hola, mundo"
multilinea = """Esto es un texto
que ocupa varias
líneas"""

# bool — verdadero o falso
activo = True
pagado = False

# None — ausencia de valor (como null en otros lenguajes)
resultado = None
```

CONVENCIONES DE NOMBRES (PEP 8)
```python
# Variables y funciones: snake_case
nombre_completo = "Ana García"
precio_con_iva = 12.10

# Constantes: MAYÚSCULAS
VELOCIDAD_LUZ = 299792458
MAX_INTENTOS = 3


# Clases: PascalCase
class CuentaBancaria:
    pass


# Módulos: minúsculas con guiones bajos
# mi_modulo.py
```

TYPE() Y ISINSTANCE()
```python
x = 42
print(type(x))  # <class 'int'>
print(isinstance(x, int))  # True
print(isinstance(x, (int, float)))  # True — varios tipos
```

CONVERSIÓN DE TIPOS
```python
# str → int (falla con ValueError si no es número)
numero = int("42")  # 42
numero = int("3.14")  # ValueError — usa float() primero

# str → float
precio = float("9.99")  # 9.99

# int/float → str
texto = str(42)  # "42"
texto = str(3.14)  # "3.14"

# Conversiones útiles
bool(0)  # False
bool(1)  # True
bool("")  # False
bool("texto")  # True
bool([])  # False
bool([1, 2])  # True

# int desde otras bases
int("FF", 16)  # 255 (hexadecimal)
int("1010", 2)  # 10 (binario)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPERADORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ARITMÉTICOS
```python
a, b = 10, 3

a + b  # 13  — suma
a - b  # 7   — resta
a * b  # 30  — multiplicación
a / b  # 3.333... — división (siempre float)
a // b  # 3   — división entera (floor division)
a % b  # 1   — módulo (resto de la división)
a**b  # 1000 — potencia
```

COMPARACIÓN (devuelven bool)
```python
a == b  # False — igual a
a != b  # True  — distinto de
a > b  # True  — mayor que
a < b  # False — menor que
a >= b  # True  — mayor o igual
a <= b  # False — menor o igual
```

LÓGICOS
```python
True and False  # False — ambos deben ser True
True or False  # True  — al menos uno debe ser True
not True  # False — niega el valor

# Short-circuit evaluation
# and: si el primero es False, no evalúa el segundo
# or: si el primero es True, no evalúa el segundo
```

ASIGNACIÓN
```python
x = 5
x += 3  # x = x + 3 → 8
x -= 2  # x = x - 2 → 6
x *= 4  # x = x * 4 → 24
x /= 6  # x = x / 6 → 4.0
x //= 3  # x = x // 3 → 1
x **= 3  # x = x ** 3 → 1
x %= 7  # x = x % 7 → 1
```

OPERADORES DE IDENTIDAD Y PERTENENCIA
```python
# is / is not — mismo objeto en memoria
a = [1, 2]
b = [1, 2]
a == b  # True  — mismo valor
a is b  # False — distinto objeto

c = a
a is c  # True  — mismo objeto

# None siempre con is, nunca con ==
if x is None:
    ...
if x is not None:
    ...

# in / not in — pertenencia
"a" in "casa"  # True
3 in [1, 2, 3]  # True
"z" not in "casa"  # True
"clave" in {"clave": 1, "otra": 2}  # True — busca en claves
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRINGS EN PROFUNDIDAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
texto = "Python es genial"

# Indexación (base 0)
texto[0]  # 'P'
texto[-1]  # 'l' — último carácter
texto[-3]  # 'i' — tercero desde el final

# Slicing [inicio:fin:paso]
texto[0:6]  # 'Python'
texto[7:]  # 'es genial'
texto[:6]  # 'Python'
texto[::2]  # 'Pto sgnl' — cada 2 caracteres
texto[::-1]  # 'laineg se nohtyP' — invertido

# len()
len(texto)  # 16

# Inmutabilidad: los strings no se pueden modificar
# texto[0] = "p"  → TypeError

# Concatenación y repetición
"Hola" + " " + "mundo"  # "Hola mundo"
"Ja" * 3  # "JaJaJa"
```

MÉTODOS DE STRING MÁS USADOS
```python
s = "  Hola Mundo  "

s.strip()  # "Hola Mundo"      — quita espacios extremos
s.lstrip()  # "Hola Mundo  "    — solo izquierda
s.rstrip()  # "  Hola Mundo"    — solo derecha
s.lower()  # "  hola mundo  "
s.upper()  # "  HOLA MUNDO  "
s.title()  # "  Hola Mundo  "  — primera letra de cada palabra
s.capitalize()  # "  hola mundo  "  — solo primera del todo

"hola mundo".replace("mundo", "Python")  # "hola Python"
"a,b,c".split(",")  # ["a", "b", "c"]
",".join(["a", "b", "c"])  # "a,b,c"

"hola".startswith("ho")  # True
"hola".endswith("la")  # True
"hola mundo".find("mundo")  # 5  — índice donde empieza (-1 si no)
"hola mundo".count("o")  # 2

"  ".isspace()  # True
"abc".isalpha()  # True
"123".isdigit()  # True
"abc123".isalnum()  # True

"hola mundo".center(20, "-")  # "---hola mundo----"
"42".zfill(5)  # "00042"
```

F-STRINGS (PYTHON 3.6+) — LA FORMA CORRECTA
```python
nombre = "Ana"
edad = 30
precio = 9.5

# Básico
print(f"Me llamo {nombre} y tengo {edad} años")

# Expresiones dentro
print(f"El doble de mi edad es {edad * 2}")
print(f"Soy {'mayor' if edad >= 18 else 'menor'} de edad")

# Formato numérico
print(f"Precio: {precio:.2f}€")  # "Precio: 9.50€"
print(f"Pi: {3.14159:.3f}")  # "Pi: 3.142"
print(f"Porcentaje: {0.15:.1%}")  # "Porcentaje: 15.0%"
print(f"Número: {1000000:,}")  # "Número: 1,000,000"
print(f"Binario: {255:b}")  # "Binario: 11111111"
print(f"Hex: {255:x}")  # "Hex: ff"

# Alineación
print(f"{'izq':<10}|")  # "izq       |"
print(f"{'der':>10}|")  # "       der|"
print(f"{'cen':^10}|")  # "   cen    |"

# Python 3.8+ — debug con =
x = 42
print(f"{x=}")  # "x=42"
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTRADA Y SALIDA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# input() siempre devuelve str
nombre = input("¿Cómo te llamas? ")
edad = int(input("¿Cuántos años tienes? "))  # convertir si hace falta

# print() — separador y fin de línea
print("a", "b", "c")  # a b c
print("a", "b", "c", sep="-")  # a-b-c
print("sin salto", end="")  # sin \n al final
print("a", "b", sep="\n")  # una por línea

# Formatear antes de imprimir
resultado = f"Hola, {nombre}. Tienes {edad} años."
print(resultado)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTROL DE FLUJO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONDICIONALES
```python
# Estructura básica
nota = 7

if nota >= 9:
    calificacion = "Sobresaliente"
elif nota >= 7:
    calificacion = "Notable"
elif nota >= 5:
    calificacion = "Aprobado"
else:
    calificacion = "Suspenso"

print(calificacion)  # "Notable"

# Operador ternario (expresión condicional)
estado = "mayor" if edad >= 18 else "menor"

# Truthy y Falsy — qué evalúa como False:
# False, None, 0, 0.0, "", [], {}, set(), ()
# Todo lo demás evalúa como True

# Uso idiomático de truthy/falsy
nombre = input("Nombre: ")
if nombre:  # equivale a if nombre != ""
    print(f"Hola, {nombre}")
else:
    print("No has introducido nombre")
```

BUCLE WHILE
```python
# Itera mientras la condición sea True
contador = 0
while contador < 5:
    print(contador)
    contador += 1

# Bucle infinito controlado
while True:
    respuesta = input("¿Continuar? (s/n): ")
    if respuesta.lower() == "n":
        break

# while/else — el else se ejecuta si el bucle termina sin break
intentos = 0
while intentos < 3:
    password = input("Contraseña: ")
    if password == "secreta":
        print("Acceso concedido")
        break
    intentos += 1
else:
    print("Demasiados intentos fallidos")
```

BUCLE FOR
```python
# Itera sobre cualquier iterable
frutas = ["manzana", "pera", "uva"]
for fruta in frutas:
    print(fruta)

# range()
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10):  # 2, 3, 4, ..., 9
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)

for i in range(10, 0, -1):  # 10, 9, 8, ..., 1
    print(i)

# enumerate — índice + valor
for i, fruta in enumerate(frutas):
    print(f"{i}: {fruta}")

# enumerate con inicio diferente
for i, fruta in enumerate(frutas, start=1):
    print(f"{i}. {fruta}")

# zip — iterar dos listas a la vez
nombres = ["Ana", "Luis", "María"]
edades = [25, 30, 28]
for nombre, edad in zip(nombres, edades):
    print(f"{nombre} tiene {edad} años")

# break, continue, pass
for i in range(10):
    if i == 3:
        continue  # salta esta iteración
    if i == 7:
        break  # termina el bucle
    print(i)

for _ in range(5):  # _ cuando no necesitas la variable
    print("hola")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTRUCTURAS DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LISTAS
```python
# Mutable, ordenada, permite duplicados, cualquier tipo
numeros = [1, 2, 3, 4, 5]
mixta = [1, "dos", 3.0, True, None]
vacia = []

# Indexación y slicing (igual que strings)
numeros[0]  # 1
numeros[-1]  # 5
numeros[1:3]  # [2, 3]
numeros[::-1]  # [5, 4, 3, 2, 1]

# Métodos principales
numeros.append(6)  # añade al final
numeros.insert(0, 0)  # inserta en posición
numeros.extend([7, 8])  # añade varios elementos
numeros.remove(3)  # elimina primera ocurrencia de valor
numeros.pop()  # elimina y devuelve el último
numeros.pop(0)  # elimina y devuelve el de índice 0
numeros.index(4)  # índice del valor 4
numeros.count(2)  # cuántas veces aparece 2
numeros.sort()  # ordena in-place
numeros.sort(reverse=True)  # ordena descendente
numeros.reverse()  # invierte in-place
sorted(numeros)  # devuelve nueva lista ordenada
numeros.copy()  # copia superficial
numeros.clear()  # vacía la lista

# Ordenar por criterio personalizado
personas = [("Ana", 30), ("Luis", 25), ("María", 35)]
personas.sort(key=lambda p: p[1])  # por edad

# Lista de listas (2D)
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matriz[1][2]  # 6

# Comprobar si elemento existe
if 3 in numeros:
    print("Está")

# Desempaquetar
a, b, c = [1, 2, 3]
primero, *resto = [1, 2, 3, 4, 5]  # primero=1, resto=[2,3,4,5]
*inicio, ultimo = [1, 2, 3, 4, 5]  # inicio=[1,2,3,4], ultimo=5
```

TUPLAS
```python
# Inmutable, ordenada, permite duplicados
coordenadas = (10, 20)
rgb = (255, 128, 0)
singleton = (42,)  # coma obligatoria para una sola tupla
vacia = ()

# Acceso igual que listas
coordenadas[0]  # 10

# Desempaquetado
x, y = coordenadas
r, g, b = rgb

# Útiles como claves de diccionarios (inmutables)
posiciones = {(0, 0): "origen", (1, 0): "derecha"}

# Intercambio de variables sin temporal
a, b = 1, 2
a, b = b, a  # a=2, b=1

# named tuples — tuplas con nombres
from collections import namedtuple

Punto = namedtuple("Punto", ["x", "y"])
p = Punto(10, 20)
print(p.x, p.y)  # 10 20
```

DICCIONARIOS
```python
# Mutable, clave-valor, claves únicas y hasheables (Python 3.7+ ordered)
persona = {
    "nombre": "Ana",
    "edad": 30,
    "activo": True
}

# Acceso
persona["nombre"]          # "Ana"
persona.get("telefono")    # None (no lanza KeyError)
persona.get("telefono", "Sin teléfono")  # valor por defecto

# Modificar y añadir
persona["edad"] = 31
persona["email"] = "ana@mail.com"

# Eliminar
del persona["activo"]
valor = persona.pop("email")    # elimina y devuelve
persona.pop("x", None)          # no falla si no existe

# Iterar
for clave in persona:                       # solo claves
for clave in persona.keys():               # explícito
for valor in persona.values():             # valores
for clave, valor in persona.items():       # pares

# Comprobar existencia
"nombre" in persona           # True
"telefono" not in persona     # True

# Combinar diccionarios
d1 = {"a": 1}
d2 = {"b": 2}
combinado = {**d1, **d2}        # {"a": 1, "b": 2}
d1.update(d2)                   # d1 ahora tiene "b" también

# Métodos útiles
persona.keys()      # dict_keys (iterable)
persona.values()    # dict_values
persona.items()     # dict_items
persona.copy()      # copia superficial
persona.clear()     # vacía

# setdefault — si la clave no existe, la crea con valor dado
persona.setdefault("rol", "usuario")  # no sobreescribe si ya existe

# defaultdict
from collections import defaultdict
contador = defaultdict(int)
for letra in "mississippi":
    contador[letra] += 1

# Counter
from collections import Counter
Counter("mississippi")  # {'s': 4, 'i': 4, 'p': 2, 'm': 1}
```

CONJUNTOS (SETS)
```python
# Mutable, no ordenado, sin duplicados, elementos hasheables
frutas = {"manzana", "pera", "uva"}
vacio = set()  # {} crea dict vacío, no set

# Operaciones de conjuntos
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b  # {1, 2, 3, 4, 5, 6}  — unión
a & b  # {3, 4}              — intersección
a - b  # {1, 2}              — diferencia (en a pero no en b)
b - a  # {5, 6}
a ^ b  # {1, 2, 5, 6}        — diferencia simétrica

a.issubset(b)  # False
a.issuperset(b)  # False
a.isdisjoint(b)  # False (comparten elementos)

# Útil para eliminar duplicados
lista = [1, 2, 2, 3, 3, 3]
sin_duplicados = list(set(lista))  # orden no garantizado

# Frozenset — inmutable
fs = frozenset({1, 2, 3})
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FUNCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Definición básica
def saludar(nombre):
    """Devuelve un saludo personalizado."""  # docstring
    return f"Hola, {nombre}!"


# Llamada
mensaje = saludar("Ana")


# Parámetros por defecto
def saludar(nombre, formal=False):
    if formal:
        return f"Buenos días, {nombre}."
    return f"Hola, {nombre}!"


saludar("Ana")  # Hola, Ana!
saludar("Ana", formal=True)  # Buenos días, Ana.


# *args — número variable de argumentos posicionales
def sumar(*numeros):
    return sum(numeros)


sumar(1, 2, 3)  # 6
sumar(1, 2, 3, 4, 5)  # 15


# **kwargs — número variable de argumentos con nombre
def mostrar_info(**datos):
    for clave, valor in datos.items():
        print(f"{clave}: {valor}")


mostrar_info(nombre="Ana", edad=30, ciudad="Madrid")


# Combinación completa
def funcion(pos1, pos2, *args, kw1=None, **kwargs):
    pass


# Desempaquetar al llamar
numeros = [1, 2, 3]
print(*numeros)  # 1 2 3

config = {"sep": "-", "end": "\n\n"}
print("a", "b", **config)  # a-b


# Retorno múltiple (en realidad devuelve tupla)
def min_max(lista):
    return min(lista), max(lista)


minimo, maximo = min_max([3, 1, 4, 1, 5])


# Funciones como objetos (first-class)
def aplicar(funcion, valor):
    return funcion(valor)


aplicar(str.upper, "hola")  # "HOLA"
aplicar(len, "hola")  # 4

# Funciones lambda (anónimas, una sola expresión)
cuadrado = lambda x: x**2
suma = lambda a, b: a + b

# Útiles en sorted, map, filter
numeros = [3, 1, 4, 1, 5, 9]
sorted(numeros, key=lambda x: -x)  # descendente

# Scope: LEGB (Local, Enclosing, Global, Built-in)
x = 10  # global


def funcion():
    x = 20  # local — no afecta al global
    print(x)  # 20


print(x)  # 10


def modificar_global():
    global x
    x = 30  # ahora sí modifica el global (evitar si es posible)


# Funciones anidadas y closures
def crear_sumador(n):
    def sumar(x):
        return x + n  # captura n del scope exterior

    return sumar


sumar_5 = crear_sumador(5)
sumar_5(10)  # 15
```

FUNCIONES BUILT-IN MÁS IMPORTANTES
```python
# Matemáticas
abs(-5)  # 5
round(3.14159, 2)  # 3.14
pow(2, 10)  # 1024
divmod(17, 5)  # (3, 2) — cociente y resto

# Secuencias
len([1, 2, 3])  # 3
max([3, 1, 4])  # 4
min([3, 1, 4])  # 1
sum([1, 2, 3])  # 6
sorted([3, 1, 2])  # [1, 2, 3]
reversed([1, 2, 3])  # iterador (list() para lista)
enumerate([...])
zip([...], [...])
range(...)
list(...), tuple(...), set(...), dict(...)

# Otras
print(...)
input(...)
type(...)
isinstance(...)
id(...)  # identidad del objeto en memoria
hash(...)  # valor hash
dir(...)  # atributos y métodos del objeto
help(...)  # documentación
vars(...)  # __dict__ del objeto
callable(...)  # si el objeto es llamable
repr(...)  # representación oficial del objeto
all([True, True, False])  # False — todos verdaderos
any([False, False, True])  # True  — alguno verdadero
filter(func, iterable)
map(func, iterable)
open(...)  # abrir ficheros
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPREHENSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# List comprehension: [expresión for item in iterable if condición]
cuadrados = [x**2 for x in range(10)]
pares = [x for x in range(20) if x % 2 == 0]
palabras_largas = [p.upper() for p in palabras if len(p) > 4]

# Equivalente sin comprehension (más verboso)
cuadrados = []
for x in range(10):
    cuadrados.append(x**2)

# Dict comprehension
cuadrados_dict = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

invertir_dict = {v: k for k, v in mi_dict.items()}

# Set comprehension
letras_unicas = {letra for letra in "mississippi"}
# {'m', 'i', 's', 'p'}

# Generator expression (no crea la lista en memoria)
suma_cuadrados = sum(x**2 for x in range(1000000))  # eficiente

# Anidado (con moderación)
matriz = [[i * j for j in range(1, 4)] for i in range(1, 4)]

# Con condición if/else dentro (ternario)
resultado = ["par" if x % 2 == 0 else "impar" for x in range(5)]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANEJO DE ERRORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Estructura completa
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except (TypeError, ValueError) as e:
    print(f"Error de tipo o valor: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
    raise  # re-lanza la excepción
else:
    print("No hubo error")  # solo si no hubo excepción
finally:
    print("Siempre se ejecuta")  # limpieza, cerrar recursos


# Lanzar excepciones
def dividir(a, b):
    if b == 0:
        raise ValueError("El divisor no puede ser cero")
    return a / b


# Excepciones personalizadas
class SaldoInsuficienteError(Exception):
    def __init__(self, saldo, cantidad):
        self.saldo = saldo
        self.cantidad = cantidad
        super().__init__(f"Saldo insuficiente: tienes {saldo}€, necesitas {cantidad}€")


# Jerarquía de excepciones importantes
# BaseException
# ├── SystemExit
# ├── KeyboardInterrupt
# └── Exception
#     ├── ArithmeticError
#     │   ├── ZeroDivisionError
#     │   └── OverflowError
#     ├── LookupError
#     │   ├── IndexError
#     │   └── KeyError
#     ├── TypeError
#     ├── ValueError
#     ├── AttributeError
#     ├── NameError
#     ├── OSError (IOError, FileNotFoundError, PermissionError...)
#     ├── RuntimeError
#     │   └── RecursionError
#     └── StopIteration
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FICHEROS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Siempre con context manager (with) — cierra el fichero automáticamente
with open("fichero.txt", "r", encoding="utf-8") as f:
    contenido = f.read()  # todo el contenido como string
    # o
    lineas = f.readlines()  # lista de líneas
    # o
    for linea in f:  # más eficiente en memoria
        print(linea.strip())

# Modos
# "r"  — lectura (por defecto)
# "w"  — escritura (sobreescribe si existe)
# "a"  — añadir al final
# "x"  — crear (error si ya existe)
# "rb" — lectura binaria
# "wb" — escritura binaria

# Escritura
with open("salida.txt", "w", encoding="utf-8") as f:
    f.write("Hola, mundo\n")
    f.writelines(["línea 1\n", "línea 2\n"])

# pathlib — forma moderna de manejar rutas
from pathlib import Path

ruta = Path("carpeta/fichero.txt")
ruta.exists()  # si existe
ruta.is_file()  # si es fichero
ruta.is_dir()  # si es directorio
ruta.suffix  # ".txt"
ruta.stem  # "fichero"
ruta.parent  # Path("carpeta")
ruta.name  # "fichero.txt"

# Leer y escribir con pathlib
texto = ruta.read_text(encoding="utf-8")
ruta.write_text("contenido", encoding="utf-8")

# Crear directorio
Path("nueva_carpeta").mkdir(parents=True, exist_ok=True)

# Listar archivos
for f in Path(".").glob("*.txt"):
    print(f)

for f in Path(".").rglob("*.py"):  # recursivo
    print(f)

# JSON
import json

datos = {"nombre": "Ana", "edad": 30}
with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)

with open("datos.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# También con strings
json_str = json.dumps(datos)
datos = json.loads(json_str)

# CSV
import csv

with open("datos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "edad"])
    writer.writeheader()
    writer.writerow({"nombre": "Ana", "edad": 30})

with open("datos.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for fila in reader:
        print(fila["nombre"])
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MÓDULOS Y PAQUETES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Importar módulo completo
import math
math.pi          # 3.14159...
math.sqrt(16)    # 4.0
math.ceil(3.2)   # 4
math.floor(3.8)  # 3

# Importar elementos específicos
from math import pi, sqrt, ceil
sqrt(16)   # sin prefijo

# Alias
import numpy as np
from datetime import datetime as dt

# Ver qué tiene un módulo
import os
dir(os)       # lista de nombres
help(os.path) # documentación

# __name__ == "__main__" — solo se ejecuta si es el script principal
if __name__ == "__main__":
    main()

# Estructura de paquete
# mi_paquete/
# ├── __init__.py
# ├── modulo_a.py
# └── modulo_b.py

# STDLIB MÁS USADOS
import os           # sistema operativo, rutas, variables de entorno
import sys          # argv, path, versión de Python
import re           # expresiones regulares
import datetime     # fechas y horas
import time         # tiempo y sleep
import random       # números y elecciones aleatorias
import math         # funciones matemáticas
import json         # serialización JSON
import csv          # ficheros CSV
import pathlib      # rutas modernas
import shutil       # operaciones de archivos de alto nivel
import subprocess   # ejecutar comandos del sistema
import argparse     # parsear argumentos de CLI
import logging      # sistema de logging
import unittest     # testing
import collections  # Counter, defaultdict, deque, OrderedDict
import itertools    # herramientas para iteración
import functools    # herramientas funcionales (lru_cache, wraps...)
import copy         # copia superficial y profunda
import hashlib      # funciones hash (MD5, SHA...)
import base64       # codificación base64
import urllib       # URLs
import http        # HTTP básico
import socket       # sockets de red
import threading    # hilos
import multiprocessing  # procesos paralelos
import asyncio      # programación asíncrona
import contextlib   # context managers
import dataclasses  # @dataclass
import typing       # type hints
import abc          # clases abstractas
import enum         # enumeraciones
import io           # streams de I/O en memoria
import tempfile     # ficheros temporales
import pickle       # serialización Python
import sqlite3      # base de datos SQLite
import configparser # ficheros .ini
import getpass      # input de contraseña sin eco
import platform     # info del sistema
import signal       # señales del SO
import weakref      # referencias débiles
import gc           # garbage collector
import traceback    # formateo de tracebacks
import warnings     # sistema de warnings
import inspect      # introspección de objetos
import ast          # árbol sintáctico abstracto
import dis          # desensamblado de bytecode
import profile/cProfile  # profiling
import timeit       # medir tiempo de ejecución
import pdb          # debugger interactivo
```
