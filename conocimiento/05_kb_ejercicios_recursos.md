# CONOCIMIENTO 4 — EJERCICIOS, PROYECTOS Y RECURSOS
# Banco de ejercicios, proyectos por nivel, errores frecuentes explicados
# y referencias para mantenerse al día.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BANCO DE EJERCICIOS POR TEMA Y NIVEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

──────────────────────────────────────
VARIABLES, TIPOS Y OPERADORES
──────────────────────────────────────

🟢 E01 — Calculadora de IMC
  Pide al usuario su peso (kg) y altura (m).
  Calcula el IMC = peso / altura²
  Muestra el resultado con 2 decimales e indica si es
  bajo peso, normal, sobrepeso u obesidad.

🟢 E02 — Conversor de temperaturas
  Pide una temperatura en Celsius.
  Muestra la conversión a Fahrenheit (F = C × 9/5 + 32)
  y a Kelvin (K = C + 273.15).

🟢 E03 — Segundo en horas, minutos y segundos
  Pide un número de segundos.
  Muestra: "X horas, Y minutos, Z segundos".
  Ejemplo: 3661 → "1 horas, 1 minutos, 1 segundos"

🟡 E04 — Calculadora de interés compuesto
  Entradas: capital inicial, tasa anual (%), años.
  Fórmula: C × (1 + r)^t
  Muestra el capital final y los intereses generados.

🔴 E05 — Validador de número de tarjeta (Luhn)
  Implementa el algoritmo de Luhn para validar si
  un número de tarjeta de crédito es válido.

──────────────────────────────────────
STRINGS
──────────────────────────────────────

🟢 E06 — Invertir una cadena
  Sin usar [::-1], escribe una función que invierta
  un string usando un bucle.

🟢 E07 — Contar vocales
  Función que recibe un texto y devuelve el número
  de vocales (mayúsculas y minúsculas).

🟡 E08 — Palíndromo
  Función que determine si una palabra es palíndroma.
  Ignora mayúsculas, tildes y espacios.
  "Anita lava la tina" → True

🟡 E09 — Comprimir string
  "aaabbbccddddee" → "a3b3c2d4e2"
  Si el carácter aparece una sola vez, no poner el 1.

🔴 E10 — Anagramas
  Función que determine si dos strings son anagramas.
  "listen" y "silent" → True
  Sin usar sorted().

──────────────────────────────────────
CONDICIONALES Y BUCLES
──────────────────────────────────────

🟢 E11 — FizzBuzz
  Para números del 1 al 100:
  - Si es múltiplo de 3: "Fizz"
  - Si es múltiplo de 5: "Buzz"
  - Si es múltiplo de ambos: "FizzBuzz"
  - Si no: el propio número

🟢 E12 — Adivina el número
  El programa elige un número del 1 al 100.
  El usuario tiene 7 intentos.
  Pistas: "muy alto", "muy bajo", "cerca" (±5).

🟡 E13 — Números primos
  Función que determine si un número es primo.
  Luego listar todos los primos hasta 200.

🟡 E14 — Secuencia de Collatz
  Dada una n: si es par → n/2, si es impar → 3n+1
  Repetir hasta llegar a 1. Mostrar la secuencia
  y cuántos pasos fueron necesarios.

🔴 E15 — Números perfectos
  Un número es perfecto si la suma de sus divisores
  (excepto él mismo) es igual a él.
  Ejemplo: 28 = 1+2+4+7+14
  Encuentra todos los números perfectos hasta 10.000.

──────────────────────────────────────
LISTAS Y ESTRUCTURAS DE DATOS
──────────────────────────────────────

🟢 E16 — Estadísticas de lista
  Sin usar funciones estadísticas de Python,
  calcula: mínimo, máximo, media y mediana
  de una lista de números.

🟢 E17 — Eliminar duplicados preservando orden
  Sin usar set(), elimina duplicados de una lista
  manteniendo el orden de primera aparición.

🟡 E18 — Rotar lista
  Función que rote una lista k posiciones hacia la derecha.
  rotar([1,2,3,4,5], 2) → [4,5,1,2,3]
  Sin crear listas auxiliares.

🟡 E19 — Aplanar lista anidada
  Función recursiva que convierta una lista con cualquier
  nivel de anidamiento en una lista plana.
  [[1,[2,3]],[4,[5,[6]]]] → [1,2,3,4,5,6]

🔴 E20 — Implementar una pila (stack)
  Clase Pila con métodos: push, pop, peek, esta_vacia,
  tamaño. Sin usar las listas directamente en el exterior.
  Lanza StackEmptyError al hacer pop en pila vacía.

──────────────────────────────────────
DICCIONARIOS
──────────────────────────────────────

🟢 E21 — Frecuencia de palabras
  Dado un texto, construye un diccionario con la
  frecuencia de cada palabra (ignorando mayúsculas
  y signos de puntuación).

🟡 E22 — Invertir diccionario
  Dado un dict {clave: valor}, devuelve {valor: [claves]}
  agrupando las claves con el mismo valor.
  {"a":1, "b":2, "c":1} → {1:["a","c"], 2:["b"]}

🟡 E23 — Agenda de contactos
  Clase Agenda con métodos: añadir, buscar, eliminar,
  listar, guardar en JSON, cargar desde JSON.

🔴 E24 — Cache LRU manual
  Implementa un cache LRU (Least Recently Used) sin
  usar functools.lru_cache.
  Operaciones: get(clave), put(clave, valor), capacidad máxima.

──────────────────────────────────────
FUNCIONES Y SCOPE
──────────────────────────────────────

🟢 E25 — Calculadora con funciones
  Funciones separadas para suma, resta, multiplicación,
  división, potencia y raíz cuadrada.
  Menú en bucle hasta que el usuario elija salir.

🟡 E26 — Decorador de tiempo
  Crea un decorador que mida el tiempo de ejecución
  de una función y lo imprima.

🟡 E27 — Memoización manual
  Implementa memoización en la función de Fibonacci
  sin usar @lru_cache. Usa un diccionario como caché.

🔴 E28 — Pipeline funcional
  Función pipeline(*funciones) que aplique una serie
  de funciones en cadena a un valor.
  pipeline(str.upper, str.strip, lambda x: x + "!")("  hola  ")
  → "HOLA!"

──────────────────────────────────────
PROGRAMACIÓN ORIENTADA A OBJETOS
──────────────────────────────────────

🟢 E29 — Clase Rectángulo
  Atributos: base, altura.
  Métodos: area(), perimetro(), es_cuadrado().
  __str__ que muestre la info del rectángulo.

🟡 E30 — Biblioteca de libros
  Clases: Libro (título, autor, isbn, disponible),
  Biblioteca (añadir, buscar, prestar, devolver, listar).
  Prestar debe marcar el libro como no disponible.
  Guardar y cargar el estado en JSON.

🟡 E31 — Sistema de formas geométricas
  Clase base abstracta Forma con método area() abstracto.
  Subclases: Circulo, Rectangulo, Triangulo, Hexagono.
  Función que reciba una lista de formas y devuelva
  la de mayor área.

🔴 E32 — Implementar __iter__ y __next__
  Clase InfiniteCounter que sea un iterador infinito
  configurable: inicio, paso, límite opcional.
  Debe funcionar con for y con next().

──────────────────────────────────────
FICHEROS Y JSON
──────────────────────────────────────

🟢 E33 — Contador de líneas, palabras y caracteres
  Dado un fichero de texto, muestra:
  - Número de líneas
  - Número de palabras
  - Número de caracteres (con y sin espacios)

🟡 E34 — Organizador de notas
  CLI para gestionar notas guardadas en JSON.
  Comandos: nueva, listar, buscar (por texto), eliminar.
  Cada nota tiene: id, título, contenido, fecha.

🔴 E35 — Procesador de CSV con estadísticas
  Lee un CSV de ventas (fecha, producto, cantidad, precio).
  Muestra: total de ventas, ventas por producto,
  mejor día, peor día, media diaria.

──────────────────────────────────────
ALGORITMOS Y ESTRUCTURAS DE DATOS
──────────────────────────────────────

🟡 E36 — Ordenación
  Implementa de cero: bubble sort, selection sort,
  insertion sort. Compara el número de operaciones
  de cada uno con la misma lista de 1000 elementos.

🟡 E37 — Búsqueda binaria
  Implementa búsqueda binaria iterativa y recursiva.
  Compara el número de comparaciones vs búsqueda lineal.

🔴 E38 — Árbol binario de búsqueda
  Clase BST con: insertar, buscar, eliminar,
  recorrido inorden (debe dar resultado ordenado).

🔴 E39 — Grafo y BFS/DFS
  Clase Grafo con lista de adyacencia.
  Implementa BFS (anchura) y DFS (profundidad).
  Encuentra el camino más corto entre dos nodos.

──────────────────────────────────────
PROYECTOS COMPLETOS POR NIVEL
──────────────────────────────────────

NIVEL PRINCIPIANTE (Módulo 0-1 completados)

  P01 — Generador de contraseñas
    · Longitud configurable
    · Opciones: mayúsculas, minúsculas, números, símbolos
    · Múltiples contraseñas a la vez
    · Verificar fortaleza

  P02 — Conversor de unidades completo
    · Longitud, peso, temperatura, velocidad, área
    · CLI con menú
    · Historial de conversiones en sesión

  P03 — Juego de ahorcado
    · Lista de palabras por categoría
    · Dibujar el ahorcado con ASCII art
    · Puntuación por partida

NIVEL INTERMEDIO (Módulo 2 completado)

  P04 — Gestor de tareas (TODO) con persistencia
    · Tareas con prioridad, categoría, fecha límite
    · Guardar en JSON
    · Filtrar, ordenar, marcar como hecho
    · CLI completa con argparse o typer

  P05 — Web scraper de noticias
    · Scrapear titulares de 3 fuentes (HN, Reddit, BBC)
    · Filtrar por palabras clave
    · Guardar en CSV o JSON
    · Resumen diario

  P06 — Bot de Telegram básico
    · Comandos: /start, /ayuda, /clima, /cita, /conversor
    · Persistencia de usuarios en SQLite
    · Desplegable en servidor

NIVEL AVANZADO (Módulo 3 completado)

  P07 — API REST completa con FastAPI
    · Auth con JWT
    · CRUD completo
    · Base de datos con SQLAlchemy
    · Tests con pytest
    · Documentación automática
    · Dockerizado

  P08 — CLI tool para gestión de ficheros
    · Organizar por tipo, fecha, tamaño
    · Encontrar duplicados (por hash)
    · Comprimir/descomprimir
    · Preview de cambios antes de ejecutar
    · Deshacer última operación

  P09 — Pipeline de análisis de datos
    · Cargar CSV de cualquier estructura
    · Limpiar datos (nulos, tipos, outliers)
    · Estadísticas descriptivas
    · Gráficas automáticas
    · Exportar informe en HTML

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ERRORES FRECUENTES — EXPLICACIÓN COMPLETA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MUTABILIDAD EN PARÁMETROS POR DEFECTO
```python
# MAL — la lista se crea UNA SOLA VEZ y se reutiliza
def añadir(item, lista=[]):
    lista.append(item)
    return lista


añadir(1)  # [1]
añadir(2)  # [1, 2]  ← inesperado para el principiante


# BIEN
def añadir(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

REFERENCIAS VS COPIAS
```python
# Las listas se asignan por referencia
a = [1, 2, 3]
b = a  # b apunta al mismo objeto
b.append(4)
print(a)  # [1, 2, 3, 4] ← inesperado

# Copia superficial
b = a.copy()  # o a[:]
b = list(a)

# Copia profunda (para estructuras anidadas)
import copy

b = copy.deepcopy(a)
```

SCOPE Y VARIABLES NO DEFINIDAS
```python
# Esto funciona (closure)
def exterior():
    x = 10

    def interior():
        print(x)  # puede leer x del scope exterior

    interior()


# Esto falla (intenta leer antes de asignar en mismo scope)
def problema():
    print(x)  # UnboundLocalError
    x = 5  # Python ve que x es local y espera que se defina primero
```

ITERACIÓN CON MODIFICACIÓN DE LISTA
```python
# MAL — modificar la lista mientras se itera
numeros = [1, 2, 3, 4, 5]
for n in numeros:
    if n % 2 == 0:
        numeros.remove(n)  # comportamiento impredecible

# BIEN — iterar sobre copia o usar comprehension
numeros = [n for n in numeros if n % 2 != 0]
# o
for n in numeros[:]:  # copia con slice
    if n % 2 == 0:
        numeros.remove(n)
```

COMPARAR STRINGS CON ==
```python
# Para strings, == compara valor (correcto)
"hola" == "hola"  # True

# is compara identidad (solo para internados — impredecible)
a = "hola"
b = "hola"
a is b  # puede ser True o False según la implementación
# NUNCA usar is para comparar strings de usuario o ficheros
```

LAMBDA EN BUCLE
```python
# MAL — todas las lambdas capturan la misma i
funciones = [lambda x: x * i for i in range(5)]
funciones[0](2)  # 8, no 0. i vale 4 al ejecutar.

# BIEN — capturar el valor actual
funciones = [lambda x, i=i: x * i for i in range(5)]
funciones[0](2)  # 0
```

FLOAT Y PRECISIÓN
```python
0.1 + 0.2 == 0.3  # False  ← aritmética de punto flotante
0.1 + 0.2  # 0.30000000000000004

# BIEN para comparar floats
import math

math.isclose(0.1 + 0.2, 0.3)  # True

# Para dinero: usar Decimal
from decimal import Decimal

Decimal("0.1") + Decimal("0.2")  # Decimal("0.3")
```

RECURSIÓN SIN CASO BASE
```python
# Error: RecursionError (stack overflow)
def factorial(n):
    return n * factorial(n - 1)  # nunca termina


# BIEN
def factorial(n):
    if n <= 1:  # caso base
        return 1
    return n * factorial(n - 1)


# El límite por defecto de recursión en Python es ~1000
import sys

sys.getrecursionlimit()  # 1000
sys.setrecursionlimit(5000)  # cambiar (con cuidado)
```

RETURN EN GENERADOR
```python
# En un generador, return sin valor termina la iteración
# return con valor lanza StopIteration con ese valor
def mi_gen():
    yield 1
    yield 2
    return "fin"  # StopIteration("fin")
    yield 3  # nunca llega aquí
```

OPEN SIN ENCODING
```python
# En Windows y macOS, el encoding por defecto puede ser diferente
with open("fichero.txt") as f:  # puede fallar con emojis/tildes
    contenido = f.read()

# SIEMPRE especificar encoding
with open("fichero.txt", encoding="utf-8") as f:
    contenido = f.read()
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEBUGGING — TÉCNICAS Y HERRAMIENTAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Print debugging — el más básico
print(f"{variable=}")  # Python 3.8+ — muestra nombre y valor

# pdb — debugger interactivo de la stdlib
import pdb

pdb.set_trace()  # pausa aquí e inicia sesión interactiva
# o más moderno:
breakpoint()  # Python 3.7+ — equivalente pero configurable

# Comandos de pdb más útiles:
# n (next)      — siguiente línea
# s (step)      — entrar en función
# c (continue)  — continuar hasta el siguiente breakpoint
# l (list)      — mostrar código alrededor
# p expr        — evaluar expresión
# pp expr       — pretty print
# w (where)     — mostrar stack trace
# u/d           — subir/bajar en el stack
# q (quit)      — salir

# icecream — alternativa más ergonómica a print debug
# pip install icecream
from icecream import ic

ic(variable)  # imprime: ic| variable: valor

# VS Code — debugging visual
# Crear .vscode/launch.json y usar F5
# Breakpoints visuales, inspección de variables, call stack

# Logging para debugging (mejor que print en código real)
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Estado: {variable=}")

# traceback — mostrar errores completos en catches
import traceback

try:
    funcion_problematica()
except Exception:
    traceback.print_exc()  # o traceback.format_exc() para string

# Variables de entorno para debugging
import os

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
if DEBUG:
    print(f"Estado interno: {datos}")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RENDIMIENTO Y PROFILING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# timeit — medir tiempo de expresiones
import timeit

# Comparar dos implementaciones
t1 = timeit.timeit('"".join(lista)', setup='lista=["a"]*1000', number=10000)
t2 = timeit.timeit('suma=""\nfor x in lista:\n suma+=x', setup='lista=["a"]*1000', number=10000)

# Desde terminal
# python -m timeit -n 10000 '"".join(["a"]*1000)'

# cProfile — profiling completo
import cProfile

cProfile.run("mi_funcion(datos)", sort="cumulative")

# Desde terminal
# python -m cProfile -s cumulative mi_script.py

# memory_profiler — consumo de memoria
# pip install memory_profiler
from memory_profiler import profile


@profile
def funcion_con_muchos_datos():
    lista = [i for i in range(1000000)]
    return lista


# line_profiler — profiling línea a línea
# pip install line_profiler
# Luego: kernprof -l -v mi_script.py

# Trucos de optimización
# 1. Usa comprehensions en vez de bucles con append
# 2. Usa generadores para conjuntos de datos grandes
# 3. Usa set para búsquedas O(1) vs lista O(n)
# 4. Usa collections.deque para colas (O(1) por los dos extremos)
# 5. Usa numpy para operaciones numéricas masivas
# 6. lru_cache para funciones puras que se repiten
# 7. Slots para objetos con muchas instancias


class Punto:
    __slots__ = ["x", "y"]  # 30-50% menos memoria que sin slots

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECURSOS PARA MANTENERSE AL DÍA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTICIAS Y NOVEDADES
  python.org/news/              → Anuncios oficiales
  peps.python.org               → Cambios propuestos al lenguaje
  discuss.python.org            → Debates del core team
  realpython.com/python-news/   → Resúmenes semanales
  pycoders.com                  → Newsletter semanal curada
  pythonweekly.com              → Otra newsletter semanal
  talkpython.fm                 → Podcast (inglés, muy bueno)
  pythonbytes.fm                → Podcast de noticias Python
  reddit.com/r/Python           → Comunidad y novedades
  github.com/trending/python    → Proyectos populares

PLATAFORMAS DE EJERCICIOS
  exercism.org/tracks/python    → Con mentores reales
  codewars.com                  → Kata gamificado
  leetcode.com                  → Algoritmos (entrevistas)
  hackerrank.com/domains/python → Por temáticas
  adventofcode.com              → Diciembre, puzzles épicos
  projecteuler.net              → Matemático y lógico
  checkio.org                   → Gamificado visual
  practicepython.org            → 40 ejercicios progresivos
  w3resource.com/python-exercises → Masivo por categorías
  edabit.com/challenges/python3 → Rápidos y variados
  codingbat.com/python          → Para principiantes

APRENDIZAJE ESTRUCTURADO
  docs.python.org/3/tutorial/   → Tutorial oficial (el mejor punto de partida)
  realpython.com                → Artículos de calidad, con explicaciones
  python.land                   → Guía moderna completa
  pythonlikeyoumeanit.com       → Conceptual y profundo
  learnpython.org               → Interactivo en el navegador
  futurecoder.io                → Para aprender desde cero

VISUALIZACIÓN DE CÓDIGO
  pythontutor.com               → Visualiza ejecución paso a paso
                                  Fundamental para principiantes
  carbon.now.sh                 → Screenshots bonitos de código

LIBROS GRATUITOS
  automatetheboringstuff.com    → Python práctico (Automate the Boring Stuff)
  inventwithpython.com          → Varios libros (juegos, criptografía, etc.)
  pythonlikeyoumeanit.com       → Bases conceptuales sólidas
  greenteapress.com/thinkpython → Think Python (académico, riguroso)
  docs.python-guide.org         → Hitchhiker's Guide to Python

LIBROS DE PAGO (valen la pena)
  Fluent Python — Luciano Ramalho (el mejor libro de Python avanzado)
  Python Tricks — Dan Bader
  Effective Python — Brett Slatkin
  Clean Code in Python — Mariano Anaya
  Architecture Patterns with Python — Harry Percival & Bob Gregory

CANALES YOUTUBE RECOMENDADOS

  EN INGLÉS
  Corey Schafer    → El mejor canal educativo de Python
  Tech With Tim    → Proyectos prácticos y tutoriales
  Sentdex          → Python, data science, IA
  mCoding          → Python avanzado e internals (muy técnico)
  ArjanCodes       → Arquitectura y buenas prácticas
  Real Python      → Canal del sitio realpython.com

  EN ESPAÑOL
  Hola Mundo       → Tutoriales claros
  pildorasinformaticas → Cursos completos
  mouredev (Brais Moure) → Proyectos reales, muy activo,
                           roadmaps de programación

COMUNIDADES
  reddit.com/r/learnpython      → Para dudas de aprendizaje
  reddit.com/r/Python           → Comunidad general
  stackoverflow.com             → Para errores concretos
  discord.gg/python             → Discord oficial Python
  python.es                     → Comunidad Python España
  twitter/X: #Python, #Python3  → Novedades

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOJA DE RUTA COMPLETA (ROADMAP)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SEMANA 1-2   — Entorno, print, variables, tipos, operadores
SEMANA 3-4   — Strings en profundidad, input, conversión tipos
SEMANA 5-6   — Condicionales, bucles, range()
SEMANA 7-8   — Listas, tuplas, sets
SEMANA 9-10  — Diccionarios, comprehensions
SEMANA 11-12 — Funciones, scope, lambda
SEMANA 13-14 — Manejo de errores, ficheros, JSON
SEMANA 15-16 — Módulos stdlib más usados
SEMANA 17-18 — OOP: clases básicas, atributos, métodos
SEMANA 19-20 — OOP: herencia, métodos especiales, propiedades
SEMANA 21-22 — Generadores, iteradores, comprehensions avanzadas
SEMANA 23-24 — Decoradores, context managers
SEMANA 25-26 — Testing con pytest
SEMANA 27-28 — Concurrencia básica (threading, asyncio intro)
SEMANA 29-30 — Type hints, dataclasses, Pydantic
SEMANA 31-32 — Librerías del área de interés (web, data, etc.)
SEMANA 33-36 — Proyecto completo integrando todo

HITOS VERIFICABLES:
  ✅ Puede escribir y ejecutar scripts simples sin ayuda
  ✅ Entiende y corrige sus propios mensajes de error
  ✅ Puede buscar en la documentación oficial
  ✅ Resuelve ejercicios de Codewars nivel 7-6 kyu
  ✅ Ha completado al menos 2 proyectos propios de nivel principiante
  ✅ Puede leer y entender código de terceros
  ✅ Usa git y tiene proyectos en GitHub
  ✅ Escribe funciones con type hints y docstrings
  ✅ Tiene tests para su código
  ✅ Puede hacer code review básico a código de otros
