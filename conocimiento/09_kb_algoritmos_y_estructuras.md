# CONOCIMIENTO 8 — ALGORITMOS Y ESTRUCTURAS DE DATOS
# Base de conocimiento para PyMentor.
# Complejidad, búsqueda, ordenación, recursión, programación dinámica, grafos y problemas típicos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLEJIDAD ALGORÍTMICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOTACIÓN BIG O

La notación O describe cómo crece el tiempo (o la memoria) de un algoritmo cuando crece el tamaño
de los datos `n`, ignorando constantes.

- O(1) constante: acceder a `lista[i]`, buscar en un dict o set.
- O(log n) logarítmica: búsqueda binaria (cada paso descarta la mitad).
- O(n) lineal: recorrer una lista una vez, `x in lista`.
- O(n log n): las buenas ordenaciones (`sorted`, merge sort).
- O(n²) cuadrática: dos bucles anidados sobre los mismos datos.
- O(2ⁿ) exponencial: probar todas las combinaciones (Fibonacci recursivo sin memoria).

Con n = 1 000 000: O(log n) son unas 20 operaciones, O(n) un millón y O(n²) un billón. Pasar de
O(n²) a O(n) suele ser la mejora más importante que se puede hacer en un programa.

COSTE DE LAS OPERACIONES DE LIST, DICT Y SET

```text
Operación                          list        dict / set
Acceder por índice / clave         O(1)        O(1)
x in coleccion                     O(n)        O(1)
append / añadir                    O(1)        O(1)
insert(0, x) / pop(0)              O(n)        -
pop() del final                    O(1)        -
del por índice / clave             O(n)        O(1)
ordenar                            O(n log n)  -
len()                              O(1)        O(1)
copiar                             O(n)        O(n)
```

Consecuencias prácticas:

- Para comprobar muchas veces si algo está, convierte la lista en set: `vistos = set(lista)`.
- Para una cola (sacar por el principio), usa `collections.deque`, no `lista.pop(0)`.
- Concatenar strings en un bucle con `+=` puede ser O(n²); usa `"".join(partes)`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BÚSQUEDA Y ORDENACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BÚSQUEDA LINEAL Y BÚSQUEDA BINARIA

```python
def busqueda_lineal(lista, objetivo):          # O(n), vale para listas sin ordenar
    for i, x in enumerate(lista):
        if x == objetivo:
            return i
    return -1

def busqueda_binaria(lista, objetivo):         # O(log n), la lista DEBE estar ordenada
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            return medio
        if lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

# En la práctica: el módulo bisect
import bisect
i = bisect.bisect_left(lista, objetivo)
encontrado = i < len(lista) and lista[i] == objetivo
```

ORDENACIONES SIMPLES: BURBUJA, SELECCIÓN E INSERCIÓN

Son O(n²): útiles para entender la idea, no para usarlas en programas reales.

```python
def burbuja(lista):
    datos = lista[:]
    n = len(datos)
    for i in range(n):
        intercambiado = False
        for j in range(n - 1 - i):              # los últimos i ya están en su sitio
            if datos[j] > datos[j + 1]:
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambiado = True
        if not intercambiado:                   # si no hubo cambios, ya está ordenada
            break
    return datos

def seleccion(lista):
    datos = lista[:]
    for i in range(len(datos)):
        minimo = min(range(i, len(datos)), key=datos.__getitem__)
        datos[i], datos[minimo] = datos[minimo], datos[i]
    return datos

def insercion(lista):
    datos = lista[:]
    for i in range(1, len(datos)):
        actual = datos[i]
        j = i - 1
        while j >= 0 and datos[j] > actual:     # desplaza los mayores a la derecha
            datos[j + 1] = datos[j]
            j -= 1
        datos[j + 1] = actual
    return datos
```

La inserción es rápida con listas casi ordenadas, y por eso Timsort la usa por dentro.

MERGE SORT Y QUICKSORT

```python
def merge_sort(lista):                          # O(n log n) siempre, estable
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izq, der = merge_sort(lista[:medio]), merge_sort(lista[medio:])
    resultado, i, j = [], 0, 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    return resultado + izq[i:] + der[j:]

def quicksort(lista):                           # O(n log n) de media, O(n²) en el peor caso
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quicksort(menores) + iguales + quicksort(mayores)
```

En código real usa siempre `sorted()` o `.sort()`: implementan Timsort (en C), que es O(n log n),
estable y muy rápido con datos parcialmente ordenados.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECURSIÓN Y PROGRAMACIÓN DINÁMICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PENSAR DE FORMA RECURSIVA

1. Caso base: el problema más pequeño, que se resuelve directamente.
2. Caso recursivo: reducir el problema a uno más pequeño del mismo tipo.
3. Confiar en que la llamada recursiva resuelve el subproblema.

```python
def potencia(base, exp):
    if exp == 0:
        return 1
    mitad = potencia(base, exp // 2)            # divide y vencerás: O(log n)
    return mitad * mitad * (base if exp % 2 else 1)

def es_palindromo(texto):
    if len(texto) <= 1:
        return True
    return texto[0] == texto[-1] and es_palindromo(texto[1:-1])

def torres_hanoi(n, origen="A", destino="C", auxiliar="B"):
    if n == 0:
        return
    torres_hanoi(n - 1, origen, auxiliar, destino)
    print(f"Mover disco {n} de {origen} a {destino}")
    torres_hanoi(n - 1, auxiliar, destino, origen)
```

MEMOIZACIÓN Y FIBONACCI

```python
# Recursivo ingenuo: O(2ⁿ), con n = 40 ya tarda segundos
def fib_lento(n):
    return n if n < 2 else fib_lento(n - 1) + fib_lento(n - 2)

# Con memoización: O(n), cada valor se calcula una vez
from functools import cache
@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# Iterativo: O(n) y sin límite de recursión
def fib_iterativo(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

PROGRAMACIÓN DINÁMICA: CAMBIO DE MONEDAS Y MOCHILA

La programación dinámica resuelve problemas que se repiten en subproblemas, guardando los
resultados en una tabla.

```python
def minimo_monedas(monedas, cantidad):
    """Menor número de monedas para pagar exacto, o -1 si no se puede."""
    INF = float("inf")
    dp = [0] + [INF] * cantidad                 # dp[x] = monedas mínimas para x
    for x in range(1, cantidad + 1):
        for m in monedas:
            if m <= x:
                dp[x] = min(dp[x], dp[x - m] + 1)
    return dp[cantidad] if dp[cantidad] != INF else -1

minimo_monedas([1, 5, 10, 25], 63)              # 6 (25+25+10+1+1+1)

def mochila(pesos, valores, capacidad):
    """Máximo valor sin superar la capacidad (cada objeto una vez)."""
    dp = [0] * (capacidad + 1)
    for peso, valor in zip(pesos, valores):
        for c in range(capacidad, peso - 1, -1):   # al revés para no reutilizar el objeto
            dp[c] = max(dp[c], dp[c - peso] + valor)
    return dp[capacidad]

def subsecuencia_comun_mas_larga(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]
```

VUELTA ATRÁS: PERMUTACIONES Y SUBCONJUNTOS

```python
def permutaciones(elementos):
    resultado = []
    def explorar(actual, restantes):
        if not restantes:
            resultado.append(actual[:])
            return
        for i in range(len(restantes)):
            actual.append(restantes[i])
            explorar(actual, restantes[:i] + restantes[i + 1:])
            actual.pop()                        # deshacer (backtracking)
    explorar([], elementos)
    return resultado

def subconjuntos(elementos):
    resultado = [[]]
    for x in elementos:
        resultado += [s + [x] for s in resultado]
    return resultado

subconjuntos([1, 2, 3])     # 8 subconjuntos, del vacío a [1, 2, 3]
```

En código real, `itertools.permutations` y `itertools.combinations` hacen esto por ti.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTRUCTURAS DE DATOS CLÁSICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PILAS Y COLAS

```python
# Pila (LIFO: el último en entrar es el primero en salir): una lista
pila = []
pila.append(1); pila.append(2)
pila.pop()          # 2
pila[-1]            # ver la cima sin sacarla

# Cola (FIFO: el primero en entrar es el primero en salir): deque
from collections import deque
cola = deque()
cola.append("a"); cola.append("b")
cola.popleft()      # 'a'

# Paréntesis equilibrados con una pila
def equilibrado(texto):
    pares = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in texto:
        if c in "([{":
            pila.append(c)
        elif c in pares:
            if not pila or pila.pop() != pares[c]:
                return False
    return not pila

equilibrado("{[()()]}")     # True
equilibrado("([)]")         # False
```

LISTA ENLAZADA

```python
class Nodo:
    def __init__(self, valor, siguiente=None):
        self.valor = valor
        self.siguiente = siguiente

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def insertar_inicio(self, valor):           # O(1)
        self.cabeza = Nodo(valor, self.cabeza)

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.valor
            actual = actual.siguiente

    def invertir(self):
        anterior, actual = None, self.cabeza
        while actual:
            actual.siguiente, anterior, actual = anterior, actual, actual.siguiente
        self.cabeza = anterior
```

En Python casi nunca hace falta: `list` y `deque` cubren estos usos. Se estudia porque es una
pregunta clásica y enseña a trabajar con referencias.

ÁRBOLES BINARIOS DE BÚSQUEDA

```python
class NodoArbol:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

def insertar(raiz, valor):
    if raiz is None:
        return NodoArbol(valor)
    if valor < raiz.valor:
        raiz.izq = insertar(raiz.izq, valor)
    else:
        raiz.der = insertar(raiz.der, valor)
    return raiz

def en_orden(raiz):                 # izquierda, raíz, derecha → valores ordenados
    if raiz:
        yield from en_orden(raiz.izq)
        yield raiz.valor
        yield from en_orden(raiz.der)

def altura(raiz):
    return 0 if raiz is None else 1 + max(altura(raiz.izq), altura(raiz.der))

raiz = None
for v in [8, 3, 10, 1, 6]:
    raiz = insertar(raiz, v)
list(en_orden(raiz))                # [1, 3, 6, 8, 10]
```

Recorridos: preorden (raíz, izq, der), en orden (izq, raíz, der), postorden (izq, der, raíz) y
por niveles (con una cola).

GRAFOS: RECORRIDO EN ANCHURA Y EN PROFUNDIDAD

```python
from collections import deque

# Grafo como diccionario de adyacencia
grafo = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": ["F"],
    "F": [],
}

def bfs(grafo, inicio, fin):
    """Camino más corto (en número de pasos) con búsqueda en anchura."""
    cola = deque([[inicio]])
    vistos = {inicio}
    while cola:
        camino = cola.popleft()
        nodo = camino[-1]
        if nodo == fin:
            return camino
        for vecino in grafo[nodo]:
            if vecino not in vistos:
                vistos.add(vecino)
                cola.append(camino + [vecino])
    return None

def dfs(grafo, nodo, vistos=None):
    """Todos los nodos alcanzables, con búsqueda en profundidad."""
    if vistos is None:
        vistos = set()
    vistos.add(nodo)
    for vecino in grafo[nodo]:
        if vecino not in vistos:
            dfs(grafo, vecino, vistos)
    return vistos

bfs(grafo, "A", "F")        # ['A', 'B', 'D', 'F']
```

Para caminos con distancias o pesos distintos se usa el algoritmo de Dijkstra (con `heapq`), y
para trabajar con grafos grandes, la librería `networkx`.

DIJKSTRA: CAMINO MÁS CORTO CON PESOS

```python
import heapq

def dijkstra(grafo, inicio):
    """grafo = {'A': [('B', 4), ('C', 1)], ...}  →  distancia mínima a cada nodo."""
    distancias = {inicio: 0}
    cola = [(0, inicio)]
    while cola:
        dist, nodo = heapq.heappop(cola)
        if dist > distancias.get(nodo, float("inf")):
            continue
        for vecino, peso in grafo.get(nodo, []):
            nueva = dist + peso
            if nueva < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva
                heapq.heappush(cola, (nueva, vecino))
    return distancias
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROBLEMAS TÍPICOS RESUELTOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOS NÚMEROS QUE SUMAN UN OBJETIVO

```python
def dos_suma(numeros, objetivo):
    """Índices de dos números que suman objetivo. O(n) con un diccionario."""
    vistos = {}                                 # valor → índice
    for i, n in enumerate(numeros):
        complemento = objetivo - n
        if complemento in vistos:
            return vistos[complemento], i
        vistos[n] = i
    return None

dos_suma([2, 7, 11, 15], 9)     # (0, 1)
```

La versión con dos bucles anidados es O(n²); el diccionario la convierte en O(n).

ANAGRAMAS, PALÍNDROMOS Y CONTAR PALABRAS

```python
from collections import Counter

def son_anagramas(a, b):
    limpiar = lambda s: s.replace(" ", "").lower()
    return Counter(limpiar(a)) == Counter(limpiar(b))

def es_palindromo(texto):
    solo_letras = [c.lower() for c in texto if c.isalnum()]
    return solo_letras == solo_letras[::-1]

es_palindromo("Anita lava la tina")     # True

def palabras_frecuentes(texto, n=3):
    palabras = texto.lower().split()
    return Counter(p.strip(".,;:¡!¿?") for p in palabras).most_common(n)

# Agrupar palabras que son anagramas entre sí
from collections import defaultdict
grupos = defaultdict(list)
for palabra in ["roma", "amor", "mora", "sol"]:
    grupos["".join(sorted(palabra))].append(palabra)
list(grupos.values())       # [['roma', 'amor', 'mora'], ['sol']]
```

NÚMEROS PRIMOS Y CRIBA DE ERATÓSTENES

```python
def es_primo(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, int(n ** 0.5) + 1, 2):    # basta probar hasta la raíz cuadrada
        if n % d == 0:
            return False
    return True

def criba(limite):
    """Todos los primos hasta limite. O(n log log n)."""
    es_primo = [True] * (limite + 1)
    es_primo[0:2] = [False, False]
    for i in range(2, int(limite ** 0.5) + 1):
        if es_primo[i]:
            es_primo[i * i::i] = [False] * len(range(i * i, limite + 1, i))
    return [i for i, p in enumerate(es_primo) if p]

criba(30)       # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def factorizar(n):
    factores, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factores.append(d)
            n //= d
        d += 1
    if n > 1:
        factores.append(n)
    return factores

factorizar(360)     # [2, 2, 2, 3, 3, 5]
```

FIZZBUZZ, MÁXIMO SIN MAX Y OTROS CLÁSICOS

```python
for i in range(1, 101):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

def maximo(numeros):                    # sin usar max()
    mayor = numeros[0]
    for n in numeros[1:]:
        if n > mayor:
            mayor = n
    return mayor

def segundo_mayor(numeros):
    distintos = sorted(set(numeros), reverse=True)
    return distintos[1] if len(distintos) > 1 else None

def invertir_palabras(frase):
    return " ".join(reversed(frase.split()))

def contar_vocales(texto):
    return sum(1 for c in texto.lower() if c in "aeiouáéíóú")

def es_bisiesto(año):
    return año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)

def mcd(a, b):                          # algoritmo de Euclides (o math.gcd)
    while b:
        a, b = b, a % b
    return a

def decimal_a_binario(n):               # sin usar bin()
    if n == 0:
        return "0"
    digitos = []
    while n > 0:
        digitos.append(str(n % 2))
        n //= 2
    return "".join(reversed(digitos))
```

DOS PUNTEROS Y VENTANA DESLIZANTE

```python
# Dos punteros: en una lista ordenada, encontrar un par que sume objetivo en O(n)
def par_con_suma(ordenada, objetivo):
    i, j = 0, len(ordenada) - 1
    while i < j:
        s = ordenada[i] + ordenada[j]
        if s == objetivo:
            return ordenada[i], ordenada[j]
        if s < objetivo:
            i += 1
        else:
            j -= 1
    return None

# Ventana deslizante: suma máxima de k elementos seguidos en O(n)
def suma_maxima(numeros, k):
    ventana = sum(numeros[:k])
    mejor = ventana
    for i in range(k, len(numeros)):
        ventana += numeros[i] - numeros[i - k]  # entra uno, sale otro
        mejor = max(mejor, ventana)
    return mejor

# Subcadena más larga sin caracteres repetidos
def subcadena_sin_repetir(texto):
    ultimo, inicio, mejor = {}, 0, 0
    for i, c in enumerate(texto):
        if ultimo.get(c, -1) >= inicio:
            inicio = ultimo[c] + 1
        ultimo[c] = i
        mejor = max(mejor, i - inicio + 1)
    return mejor

subcadena_sin_repetir("abcabcbb")   # 3 ("abc")
```

MATRICES: TRANSPONER, ROTAR Y RECORRER

```python
matriz = [[1, 2, 3],
          [4, 5, 6]]

transpuesta = [list(fila) for fila in zip(*matriz)]     # [[1, 4], [2, 5], [3, 6]]
rotada_90 = [list(fila) for fila in zip(*matriz[::-1])] # giro en el sentido del reloj
suma_total = sum(sum(fila) for fila in matriz)
aplanada = [x for fila in matriz for x in fila]

# Crear una matriz de ceros correctamente
ceros = [[0] * 3 for _ in range(2)]
mal = [[0] * 3] * 2             # MAL: las dos filas son la misma lista

# Vecinos de una celda (útil en juegos de tablero)
def vecinos(m, f, c):
    for df in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nf, nc = f + df, c + dc
            if (df or dc) and 0 <= nf < len(m) and 0 <= nc < len(m[0]):
                yield nf, nc
```

Para cálculo numérico con matrices grandes (multiplicar, invertir), usa NumPy.

CÓMO ENFRENTARSE A UN PROBLEMA NUEVO

1. Entiende el enunciado: qué entra, qué sale y casos límite (lista vacía, un elemento,
   negativos, repetidos).
2. Resuelve ejemplos pequeños a mano antes de programar.
3. Empieza por la solución más simple que funcione (aunque sea lenta).
4. Pruébala con los ejemplos y los casos límite.
5. Busca dónde se repite trabajo: muchas veces un dict o un set convierte O(n²) en O(n);
   ordenar primero permite usar dos punteros o búsqueda binaria.
6. Analiza la complejidad final en tiempo y memoria.
