# CONOCIMIENTO 6 — POO Y PYTHON AVANZADO AMPLIADO
# Base de conocimiento para PyMentor.
# Clases explicadas desde cero, métodos especiales, tipado avanzado, itertools, concurrencia e imports.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLASES Y OBJETOS DESDE CERO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUÉ ES UNA CLASE Y QUÉ ES UN OBJETO

Una clase es un molde que describe qué datos (atributos) y qué acciones (métodos) tiene un tipo
de cosa. Un objeto (o instancia) es una cosa concreta creada con ese molde. `Perro` es la clase;
`toby` y `luna` son objetos.

```python
class Perro:
    def __init__(self, nombre, edad):
        self.nombre = nombre  # atributo de instancia
        self.edad = edad

    def ladrar(self):  # método
        return f"{self.nombre} dice: ¡Guau!"


toby = Perro("Toby", 3)  # crear una instancia: llama a __init__
luna = Perro("Luna", 5)
toby.ladrar()  # 'Toby dice: ¡Guau!'
luna.edad  # 5
type(toby)  # <class '__main__.Perro'>
isinstance(toby, Perro)  # True
```

En Python todo es un objeto: los int, las listas y las funciones también tienen clase
(`type(3)` es `int`). Crear tus clases sirve para agrupar datos y el comportamiento que les
corresponde.

QUÉ ES SELF Y QUÉ HACE __INIT__

- `self` es el propio objeto sobre el que se llama al método. `toby.ladrar()` equivale a
  `Perro.ladrar(toby)`: Python pasa el objeto como primer argumento. El nombre `self` es una
  convención, pero úsalo siempre.
- `__init__` es el inicializador: se ejecuta automáticamente al crear el objeto y prepara sus
  atributos. No devuelve nada (no lleva `return` con valor). No es exactamente el «constructor»:
  el objeto ya lo ha creado `__new__`, que casi nunca hace falta tocar.

```python
class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def area(self):
        return self.ancho * self.alto  # sin self.ancho, «ancho» no existiría aquí


r = Rectangulo(3, 4)
r.area()  # 12
```

Error típico: olvidar `self` en la definición del método da
`TypeError: area() takes 0 positional arguments but 1 was given`.

ATRIBUTOS DE CLASE FRENTE A ATRIBUTOS DE INSTANCIA

```python
class Empleado:
    empresa = "ACME"  # atributo de clase: compartido por todas las instancias
    total = 0

    def __init__(self, nombre):
        self.nombre = nombre  # atributo de instancia: propio de cada objeto
        Empleado.total += 1  # modificar el de clase a través de la clase


a = Empleado("Ana")
b = Empleado("Luis")
Empleado.total  # 2
a.empresa  # 'ACME' (lo busca en la instancia y, si no está, en la clase)
```

Trampa: un atributo de clase mutable se comparte entre todos.

```python
class Carrito:
    productos = []  # MAL: la misma lista para todos los carritos

    def añadir(self, p):
        self.productos.append(p)


class Carrito:
    def __init__(self):
        self.productos = []  # BIEN: una lista nueva para cada carrito
```

ENCAPSULACIÓN: GUION BAJO, DOBLE GUION BAJO Y PROPERTY

Python no tiene atributos privados de verdad; usa convenciones:

- `nombre`: público.
- `_nombre`: «interno, no lo toques desde fuera». Es solo un aviso.
- `__nombre`: Python le cambia el nombre (`_Clase__nombre`) para evitar choques en las
  subclases. No es seguridad, solo evita sobrescribirlo por accidente.

`@property` permite que un método se use como si fuera un atributo, para calcular un valor o
validar al asignarlo, sin cambiar cómo se usa la clase desde fuera.

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius  # pasa por el setter de abajo

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, valor):
        if valor < -273.15:
            raise ValueError("Por debajo del cero absoluto")
        self._celsius = valor

    @property
    def fahrenheit(self):  # calculado, de solo lectura
        return self._celsius * 9 / 5 + 32


t = Temperatura(25)
t.fahrenheit  # 77.0 (sin paréntesis)
t.celsius = -300  # ValueError
t.fahrenheit = 10  # AttributeError: no tiene setter
```

No escribas getters y setters «por si acaso» como en Java: empieza con atributos públicos y, si
más adelante hace falta validar, conviértelos en property sin romper el código que los usa.

MÉTODOS DE INSTANCIA, DE CLASE Y ESTÁTICOS

```python
from datetime import date


class Persona:
    def __init__(self, nombre, nacimiento):
        self.nombre = nombre
        self.nacimiento = nacimiento

    def edad(self):  # de instancia: recibe el objeto (self)
        return date.today().year - self.nacimiento.year

    @classmethod
    def desde_texto(cls, texto):  # de clase: recibe la clase (cls)
        nombre, fecha = texto.split(";")  # típico: constructores alternativos
        return cls(nombre, date.fromisoformat(fecha))

    @staticmethod
    def es_nombre_valido(nombre):  # estático: no recibe ni objeto ni clase
        return nombre.replace(" ", "").isalpha()


p = Persona.desde_texto("Ana;1990-05-20")
Persona.es_nombre_valido("Ana María")  # True
```

- Instancia: necesita los datos del objeto.
- `@classmethod`: crea objetos de otra forma o trabaja con datos de la clase. Al usar `cls`,
  funciona bien con subclases.
- `@staticmethod`: función relacionada con la clase que no usa ni el objeto ni la clase. Si no
  tiene relación clara, mejor una función normal fuera de la clase.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MÉTODOS ESPECIALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STR Y REPR: __STR__ FRENTE A __REPR__

- `__str__`: texto para el usuario; lo usan `print()` y `str()`.
- `__repr__`: texto para el programador; lo usan el REPL, el depurador y los contenedores
  (`print([obj])`). Si es posible, que parezca el código que crea el objeto.
- Si solo defines uno, define `__repr__`: `str()` lo usa cuando no hay `__str__`.

```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"({self.x}, {self.y})"


p = Punto(1, 2)
print(p)  # (1, 2)
p  # Punto(1, 2) en el REPL
print([p])  # [Punto(1, 2)]
f"{p!r}"  # 'Punto(1, 2)'
```

IGUALDAD Y HASH: __EQ__ Y __HASH__

Por defecto, `==` entre objetos de tus clases compara identidad (si son el mismo objeto). Para
comparar por contenido, define `__eq__`. Si defines `__eq__`, Python quita el `__hash__` y el
objeto deja de poder usarse en sets o como clave de dict, salvo que definas `__hash__` con los
mismos campos (y esos campos no cambien).

```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, otro):
        if not isinstance(otro, Punto):
            return NotImplemented  # deja que Python pruebe la otra opción
        return (self.x, self.y) == (otro.x, otro.y)

    def __hash__(self):
        return hash((self.x, self.y))


{Punto(1, 2), Punto(1, 2)}  # un solo elemento
```

Una dataclass con `frozen=True` genera `__eq__` y `__hash__` correctos automáticamente.

COMPARACIONES Y TOTAL_ORDERING

```python
from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, texto):
        self.partes = tuple(int(x) for x in texto.split("."))

    def __eq__(self, otra):
        return self.partes == otra.partes

    def __lt__(self, otra):
        return self.partes < otra.partes

    # total_ordering genera <=, > y >= a partir de __eq__ y __lt__


Version("1.10.0") > Version("1.9.3")  # True (comparar como texto daría False)
sorted([Version("2.0"), Version("1.5")])
```

SOBRECARGA DE OPERADORES

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, otro):  # v1 + v2
        return Vector(self.x + otro.x, self.y + otro.y)

    def __sub__(self, otro):  # v1 - v2
        return Vector(self.x - otro.x, self.y - otro.y)

    def __mul__(self, k):  # v * 3
        return Vector(self.x * k, self.y * k)

    def __rmul__(self, k):  # 3 * v (operando a la derecha)
        return self * k

    def __abs__(self):  # abs(v)
        return (self.x**2 + self.y**2) ** 0.5

    def __neg__(self):  # -v
        return Vector(-self.x, -self.y)

    def __bool__(self):  # if v:
        return bool(self.x or self.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
```

Otros: `__truediv__` (/), `__floordiv__` (//), `__mod__` (%), `__pow__` (**), `__matmul__` (@),
`__iadd__` (+=), `__lt__`/`__le__`/`__gt__`/`__ge__`.

COMPORTARSE COMO UN CONTENEDOR

```python
class Biblioteca:
    def __init__(self):
        self._libros = []

    def __len__(self):  # len(b)
        return len(self._libros)

    def __getitem__(self, i):  # b[0], b[1:3] y permite iterar con for
        return self._libros[i]

    def __setitem__(self, i, libro):  # b[0] = ...
        self._libros[i] = libro

    def __contains__(self, titulo):  # "Dune" in b
        return any(l.titulo == titulo for l in self._libros)

    def __iter__(self):  # for libro in b
        return iter(self._libros)
```

`__call__` hace que el objeto se pueda llamar como una función (`obj()`), útil para objetos con
estado que actúan como funciones. `__enter__` y `__exit__` lo convierten en context manager
(`with`).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERENCIA Y DISEÑO DE CLASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HERENCIA Y SUPER()

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

    def hablar(self):
        return "..."

    def presentarse(self):
        return f"Soy {self.nombre} y digo {self.hablar()}"


class Gato(Animal):  # Gato hereda de Animal
    def __init__(self, nombre, vidas=7):
        super().__init__(nombre)  # ejecuta el __init__ del padre
        self.vidas = vidas

    def hablar(self):  # sobrescribe (override) el método del padre
        return "miau"


Gato("Misi").presentarse()  # 'Soy Misi y digo miau' → polimorfismo
isinstance(Gato("Misi"), Animal)  # True
issubclass(Gato, Animal)  # True
```

Si la subclase define `__init__` y no llama a `super().__init__()`, los atributos del padre no se
crean y aparecerán `AttributeError` más adelante.

MRO: ORDEN DE RESOLUCIÓN EN HERENCIA MÚLTIPLE

Con herencia múltiple, Python busca los métodos siguiendo el MRO (method resolution order),
calculado con el algoritmo C3. `super()` llama al siguiente de esa lista, no necesariamente al
padre directo.

```python
class A:
    def hola(self):
        return "A"


class B(A):
    def hola(self):
        return "B" + super().hola()


class C(A):
    def hola(self):
        return "C" + super().hola()


class D(B, C):
    pass


D().hola()  # 'BCA'
D.__mro__  # (D, B, C, A, object)
```

COMPOSICIÓN FRENTE A HERENCIA

Usa herencia cuando la relación es «es un» (un `Gato` es un `Animal`). Usa composición cuando es
«tiene un»: un `Coche` tiene un `Motor`, no es un motor. La composición suele dar código más
flexible y fácil de probar.

```python
class Motor:
    def arrancar(self):
        return "brum"


class Coche:
    def __init__(self, motor: Motor):
        self.motor = motor  # composición: el coche TIENE un motor

    def arrancar(self):
        return self.motor.arrancar()


coche = Coche(Motor())
```

Los mixins son clases pequeñas que añaden una capacidad concreta (`JsonMixin` con un método
`a_json`) y se combinan por herencia múltiple; no deben tener `__init__` propio.

DUCK TYPING Y PROTOCOLOS

«Si camina como un pato y grazna como un pato, es un pato»: en Python importa qué métodos tiene
un objeto, no de qué clase hereda. Una función que llama a `.read()` funciona con un fichero,
con `io.StringIO` o con cualquier objeto que tenga `read`.

`collections.abc` define las interfaces estándar (`Iterable`, `Sequence`, `Mapping`, `Callable`)
y sirve para comprobar capacidades con `isinstance(x, Iterable)`. `typing.Protocol` hace lo mismo
para el tipado estático sin obligar a heredar.

DATACLASSES EN DETALLE

```python
from dataclasses import dataclass, field, asdict


@dataclass
class Producto:
    nombre: str
    precio: float
    etiquetas: list[str] = field(default_factory=list)  # nunca etiquetas: list = []
    stock: int = 0

    def __post_init__(self):  # validar después del __init__ generado
        if self.precio < 0:
            raise ValueError("Precio negativo")


p = Producto("Taza", 6.5)
p  # Producto(nombre='Taza', precio=6.5, etiquetas=[], stock=0)
asdict(p)  # dict, útil para JSON


@dataclass(frozen=True)  # inmutable y hashable
class Coordenada:
    lat: float
    lon: float


@dataclass(order=True)  # genera <, <=, >, >= comparando campo a campo
class Tarea:
    prioridad: int
    nombre: str = field(compare=False)


@dataclass(slots=True, kw_only=True)  # Python 3.10+: menos memoria; argumentos solo por nombre
class Config:
    host: str
    puerto: int = 8000
```

Genera automáticamente `__init__`, `__repr__` y `__eq__`. Para validar datos que vienen de fuera
(JSON, formularios), Pydantic añade conversión y validación de tipos.

SLOTS: __SLOTS__ PARA AHORRAR MEMORIA

```python
class Punto:
    __slots__ = ("x", "y")  # sin __dict__ por instancia: menos memoria, acceso algo más rápido

    def __init__(self, x, y):
        self.x, self.y = x, y


p = Punto(1, 2)
p.z = 3  # AttributeError: no se pueden añadir atributos nuevos
```

Útil cuando hay millones de instancias. En dataclasses: `@dataclass(slots=True)`.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIPADO AVANZADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GENÉRICOS CON LA SINTAXIS DE PYTHON 3.12

```python
# Python 3.12+: parámetros de tipo directamente en la definición
def primero[T](elementos: list[T]) -> T:
    return elementos[0]


class Pila[T]:
    def __init__(self) -> None:
        self._datos: list[T] = []

    def apilar(self, x: T) -> None:
        self._datos.append(x)

    def desapilar(self) -> T:
        return self._datos.pop()


type Matriz = list[list[float]]  # alias de tipo (sentencia type, 3.12+)

# Equivalente en versiones anteriores
from typing import TypeVar, Generic

T = TypeVar("T")


class PilaAntigua(Generic[T]): ...
```

X | NONE, ANY, OBJECT Y CAST

```python
def buscar(id: int) -> str | None:  # Python 3.10+; antes Optional[str]
    ...


from typing import Any, cast


def registrar(dato: Any) -> None: ...  # Any: desactiva la comprobación (evítalo si puedes)
def mostrar(dato: object) -> None: ...  # object: acepta cualquier cosa pero obliga a comprobar


valor = cast(int, obtener())  # «confía en mí, es un int» (no comprueba nada al ejecutar)
```

Con `str | None`, el comprobador de tipos te obliga a tratar el caso `None` antes de usar
métodos de str: así se evitan muchos `AttributeError: 'NoneType'...`.

SELF, FINAL, CLASSVAR, NEWTYPE Y ANNOTATED

```python
from typing import Self, Final, ClassVar, NewType, Annotated


class Consulta:
    def filtrar(self, campo: str) -> Self:  # 3.11+: devuelve el mismo tipo (también en subclases)
        ...
        return self


MAX_REINTENTOS: Final = 3  # constante: el comprobador avisa si se reasigna


class Contador:
    total: ClassVar[int] = 0  # atributo de clase, no de instancia


UserId = NewType("UserId", int)  # int distinto para el comprobador


def borrar(usuario: UserId) -> None: ...


Edad = Annotated[int, "años, entre 0 y 150"]  # metadatos (Pydantic y FastAPI los usan)
```

OVERLOAD, PARAMSPEC Y TYPEIS

```python
from typing import overload, Literal, Callable, ParamSpec, TypeVar, TypeIs
import functools


# El tipo de retorno depende del valor de un argumento
@overload
def leer(clave: str, como_int: Literal[False] = False) -> str: ...
@overload
def leer(clave: str, como_int: Literal[True]) -> int: ...
def leer(clave: str, como_int: bool = False) -> str | int:
    valor = config[clave]
    return int(valor) if como_int else valor


# Tipar decoradores conservando la firma de la función decorada
P = ParamSpec("P")
R = TypeVar("R")


def registrado(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def envoltura(*args: P.args, **kwargs: P.kwargs) -> R:
        print("Llamando a", func.__name__)
        return func(*args, **kwargs)

    return envoltura


# TypeIs (3.13+): funciones que estrechan el tipo
def es_texto(x: object) -> TypeIs[str]:
    return isinstance(x, str)
```

CÓMO SE COMPRUEBAN LOS TIPOS

Python ignora las anotaciones al ejecutar. Para comprobarlas se usa una herramienta aparte:
`mypy`, `pyright` (el de VS Code/Pylance) o `ty` y `pyrefly`, más recientes. En tiempo de
ejecución solo validan tipos librerías como Pydantic o beartype.

```bash
pip install mypy
mypy src/                   # comprobar
mypy --strict src/          # modo estricto: exige anotar todo
```

Desde Python 3.14 las anotaciones se evalúan de forma diferida (PEP 649): se pueden usar nombres
que se definen más abajo sin ponerlos entre comillas.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERTOOLS, FUNCTOOLS Y COLECCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ITERTOOLS: COMBINATORIA

```python
from itertools import product, permutations, combinations, combinations_with_replacement

list(product("AB", repeat=2))  # [('A','A'), ('A','B'), ('B','A'), ('B','B')]
list(product([1, 2], ["x", "y"]))  # producto cartesiano (como dos for anidados)
list(permutations([1, 2, 3], 2))  # orden importa: (1,2), (1,3), (2,1)... 6 en total
list(combinations([1, 2, 3], 2))  # orden no importa: (1,2), (1,3), (2,3)
list(combinations_with_replacement("ab", 2))  # ('a','a'), ('a','b'), ('b','b')
```

ITERTOOLS: AGRUPAR, TROCEAR Y ENCADENAR

```python
from itertools import chain, islice, groupby, batched, pairwise, accumulate, zip_longest

list(chain([1, 2], [3], [4, 5]))  # [1, 2, 3, 4, 5]
list(chain.from_iterable([[1, 2], [3]]))  # aplanar un nivel
list(islice(generador, 5))  # los 5 primeros (sin crear todo)
list(batched(range(7), 3))  # [(0,1,2), (3,4,5), (6,)]  Python 3.12+
list(pairwise([1, 2, 3, 4]))  # [(1,2), (2,3), (3,4)]   Python 3.10+
list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10] (sumas acumuladas)
list(zip_longest("ab", "xyz", fillvalue="-"))  # [('a','x'), ('b','y'), ('-','z')]

# groupby agrupa elementos CONSECUTIVOS: ordena antes por la misma clave
ventas = [("Madrid", 10), ("Sevilla", 5), ("Madrid", 7)]
ventas.sort(key=lambda v: v[0])
for ciudad, grupo in groupby(ventas, key=lambda v: v[0]):
    print(ciudad, sum(v[1] for v in grupo))  # Madrid 17, Sevilla 5
```

ITERTOOLS: ITERADORES INFINITOS Y FILTROS

```python
from itertools import count, cycle, repeat, takewhile, dropwhile, starmap, compress

for i in count(start=1, step=2):
    ...  # 1, 3, 5, ... sin fin (corta con break o islice)
colores = cycle(["rojo", "verde"])  # rojo, verde, rojo, verde...
list(repeat("x", 3))  # ['x', 'x', 'x']
list(takewhile(lambda x: x < 5, [1, 3, 6, 2]))  # [1, 3] (para al primero que no cumple)
list(dropwhile(lambda x: x < 5, [1, 3, 6, 2]))  # [6, 2]
list(starmap(pow, [(2, 3), (3, 2)]))  # [8, 9]
list(compress("abcd", [1, 0, 1, 0]))  # ['a', 'c']
```

FUNCTOOLS: CACHE, PARTIAL, WRAPS Y SINGLEDISPATCH

```python
from functools import cache, lru_cache, partial, wraps, reduce, cached_property, singledispatch


@cache  # memoriza sin límite (3.9+); lru_cache(maxsize=128) con límite
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


fib(100)  # instantáneo

doble = partial(pow, exp=2)  # fija argumentos
int_binario = partial(int, base=2)
int_binario("1010")  # 10


class Informe:
    @cached_property  # se calcula la primera vez y se guarda en el objeto
    def datos(self):
        return cargar_datos_pesados()


@singledispatch  # una función con versiones según el tipo del primer argumento
def describir(x):
    return "algo"


@describir.register
def _(x: int):
    return "un entero"


@describir.register
def _(x: list):
    return f"una lista de {len(x)}"
```

`@wraps(func)` dentro de un decorador conserva el nombre y el docstring de la función original.

`lambda` frente a `partial`: las dos crean una función nueva, pero `partial(f, x)` fija ya el valor
de x (se evalúa al crear el partial), mientras que `lambda: f(x)` busca x cada vez que se llama, así
que si x cambia después, la lambda usa el valor nuevo. Además, un partial conserva la función
original (`p.func`, `p.args`) y se puede guardar con pickle; una lambda no.

```python
from functools import partial

x = 10
con_partial = partial(print, x)
con_lambda = lambda: print(x)
x = 20
con_partial()  # 10 → el valor que tenía x al crear el partial
con_lambda()  # 20 → el valor de x en el momento de la llamada
```

COLLECTIONS: DEQUE, ORDEREDDICT, CHAINMAP Y NAMEDTUPLE

```python
from collections import deque, OrderedDict, ChainMap, namedtuple, Counter

cola = deque(maxlen=3)  # con maxlen se descartan los más antiguos
cola.append(1)
cola.appendleft(0)
cola.pop()
cola.popleft()
d = deque([1, 2, 3])
d.rotate(1)  # gira en el sitio: d pasa a ser deque([3, 1, 2])

od = OrderedDict(a=1, b=2)
od.move_to_end("a")  # útil para cachés LRU caseras

config = ChainMap(argumentos, variables_entorno, por_defecto)  # busca en orden sin copiar
config["puerto"]

Punto = namedtuple("Punto", ["x", "y"])
p = Punto(1, 2)
p.x
p._asdict()

Counter("abracadabra").most_common(2)  # [('a', 5), ('b', 2)]
Counter(a=3) + Counter(a=1, b=2)  # Counter({'a': 4, 'b': 2})
```

En código nuevo, `typing.NamedTuple` (con anotaciones) suele ser más claro que `namedtuple`, y
una dataclass si el objeto debe ser mutable.

HEAPQ Y BISECT

```python
import heapq

numeros = [5, 1, 8, 3]
heapq.heapify(numeros)  # convierte en montículo (el menor en numeros[0])
heapq.heappush(numeros, 2)
heapq.heappop(numeros)  # 1 (saca siempre el menor)
heapq.nlargest(3, datos)  # los 3 mayores
heapq.nsmallest(2, personas, key=lambda p: p["edad"])
# Cola de prioridad: tuplas (prioridad, contador, tarea)

import bisect

ordenada = [10, 20, 30]
bisect.bisect_left(ordenada, 25)  # 2: posición donde insertar sin desordenar
bisect.insort(ordenada, 25)  # inserta manteniendo el orden


# Calificación por tramos
def nota(puntos, cortes=[50, 70, 90], letras="DCBA"):
    return letras[bisect.bisect(cortes, puntos)]
```

MÓDULO OPERATOR

```python
import operator

operator.add(2, 3)  # 5 (funciones para cada operador)
sorted(datos, key=operator.itemgetter(1, 0))  # por el elemento 1 y luego el 0
sorted(objetos, key=operator.attrgetter("fecha"))
list(map(operator.methodcaller("upper"), ["a", "b"]))  # ['A', 'B']
reduce(operator.mul, [1, 2, 3, 4])  # 24
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONCURRENCIA: CUÁNDO USAR CADA OPCIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EL GIL Y LA ELECCIÓN ENTRE HILOS, PROCESOS Y ASYNCIO

El GIL (Global Interpreter Lock) hace que, en CPython normal, solo un hilo ejecute código Python a
la vez. Por eso:

- Tareas que esperan (red, disco, bases de datos): hilos (`ThreadPoolExecutor`) o `asyncio`.
  Mientras un hilo espera, el GIL se libera y otros avanzan.
- Tareas de cálculo intensivo: procesos (`ProcessPoolExecutor`, `multiprocessing`), que usan
  varios núcleos de verdad; o NumPy, que hace el cálculo en C.
- `asyncio`: miles de conexiones a la vez con un solo hilo, si las librerías son asíncronas
  (`httpx`, `aiohttp`, `asyncpg`).

Desde Python 3.13 existe una versión de CPython sin GIL («free-threaded», `python3.13t`). En 3.13
era experimental; en 3.14 ya tiene soporte oficial, pero es una compilación aparte y opcional, y
no todas las librerías con extensiones en C la admiten todavía.

THREADPOOLEXECUTOR Y PROCESSPOOLEXECUTOR

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import requests

urls = ["https://example.com"] * 10

# Descargas en paralelo (I/O)
with ThreadPoolExecutor(max_workers=8) as pool:
    respuestas = list(pool.map(requests.get, urls))

# Procesar según van terminando
with ThreadPoolExecutor() as pool:
    futuros = {pool.submit(requests.get, u): u for u in urls}
    for futuro in as_completed(futuros):
        print(futuros[futuro], futuro.result().status_code)


# Cálculo en varios núcleos (CPU)
def pesado(n):
    return sum(i * i for i in range(n))


if __name__ == "__main__":  # obligatorio con procesos en Windows y macOS
    with ProcessPoolExecutor() as pool:
        resultados = list(pool.map(pesado, [10**7] * 4))
```

ASYNCIO: ERRORES TÍPICOS

```python
import asyncio, time


async def mal():
    time.sleep(2)  # MAL: bloquea todo el bucle de eventos


async def bien():
    await asyncio.sleep(2)  # BIEN: cede el control mientras espera


async def usar_funcion_bloqueante():
    # Una función síncrona lenta (requests, lectura de disco grande) en un hilo aparte
    datos = await asyncio.to_thread(funcion_lenta, argumento)  # 3.9+


# Llamar a una corrutina sin await no la ejecuta: «coroutine was never awaited»
async def main():
    tarea = descargar()  # MAL: solo crea la corrutina
    resultado = await descargar()  # BIEN


asyncio.run(main())  # punto de entrada; no se puede llamar dentro de otro bucle

# Limitar cuántas tareas van a la vez
semaforo = asyncio.Semaphore(5)


async def descargar_limitado(url):
    async with semaforo:
        return await descargar(url)
```

COLAS ENTRE HILOS Y CONDICIONES DE CARRERA

```python
import threading, queue

cola = queue.Queue()  # segura entre hilos


def trabajador():
    while True:
        tarea = cola.get()
        if tarea is None:  # señal para terminar
            break
        procesar(tarea)
        cola.task_done()


hilos = [threading.Thread(target=trabajador) for _ in range(4)]
for h in hilos:
    h.start()
for t in tareas:
    cola.put(t)
cola.join()  # espera a que se procesen todas
for _ in hilos:
    cola.put(None)

# Condición de carrera: dos hilos modifican lo mismo a la vez → usar Lock
contador = 0
cerrojo = threading.Lock()


def sumar():
    global contador
    with cerrojo:
        contador += 1
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPORTACIONES Y MEMORIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CÓMO FUNCIONA IMPORT Y SYS.PATH

Al hacer `import modulo`, Python lo busca en las carpetas de `sys.path`, en orden: primero la
carpeta del script que ejecutas, luego `PYTHONPATH` y luego las librerías instaladas. El módulo se
ejecuta una sola vez; las siguientes importaciones reutilizan el que ya está en `sys.modules`.

```python
import sys

print(sys.path)  # dónde busca
import json

print(json.__file__)  # de qué fichero viene

import importlib

importlib.reload(mi_modulo)  # volver a cargarlo (útil en el REPL o en notebooks)
```

Por eso un fichero tuyo llamado `random.py` o `json.py` tapa al de la biblioteca estándar.

IMPORTACIONES RELATIVAS Y ABSOLUTAS

```text
proyecto/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── utilidades/
│       ├── __init__.py
│       └── texto.py
```

```python
# En app/main.py
from app.utilidades.texto import limpiar  # absoluta: recomendada
from .utilidades.texto import limpiar  # relativa: . = este paquete, .. = el de arriba
```

Las importaciones relativas solo funcionan dentro de un paquete. Si ejecutas `python app/main.py`
dan `ImportError: attempted relative import with no known parent package`; ejecuta desde la
carpeta del proyecto con `python -m app.main`.

`__init__.py` marca una carpeta como paquete y se ejecuta al importarlo. `__all__ = [...]` define
qué nombres exporta `from paquete import *`.

IMPORTACIONES CIRCULARES

`ImportError: cannot import name 'X' from partially initialized module` aparece cuando `a.py`
importa `b.py` y `b.py` importa `a.py`. Soluciones: mover lo común a un tercer módulo, importar
dentro de la función que lo necesita, o importar el módulo (`import a`) en vez del nombre
(`from a import X`). Si solo hace falta para las anotaciones de tipo, usa
`if TYPE_CHECKING: from a import X`.

RECOLECTOR DE BASURA Y REFERENCIAS DÉBILES

CPython libera un objeto cuando nadie lo referencia (contador de referencias). Para los ciclos
(A apunta a B y B a A) hay además un recolector cíclico (`gc`). Casi nunca hay que intervenir.

```python
import sys, gc, weakref

sys.getrefcount(obj)  # referencias a obj (+1 por la propia llamada)
sys.getsizeof([1, 2, 3])  # bytes del objeto lista (sin contar sus elementos)
del variable  # borra el nombre, no necesariamente el objeto
gc.collect()  # forzar la recogida de ciclos

# weakref: referencia que no mantiene vivo el objeto (útil en cachés)
cache = weakref.WeakValueDictionary()
```

Para encontrar fugas de memoria: `tracemalloc` (biblioteca estándar) compara qué líneas reservan
más memoria entre dos momentos.
