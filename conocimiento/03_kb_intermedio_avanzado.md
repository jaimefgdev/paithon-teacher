# CONOCIMIENTO 2 — PYTHON INTERMEDIO Y AVANZADO
# OOP, decoradores, generadores, tipado, concurrencia, testing y más.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROGRAMACIÓN ORIENTADA A OBJETOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
class CuentaBancaria:
    """Representa una cuenta bancaria."""

    tasa_interes = 0.02  # atributo de clase (compartido por todas)

    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        """Constructor — se llama al crear la instancia."""
        self.titular = titular  # atributo público
        self._saldo = saldo_inicial  # atributo "protegido" (convención)
        self.__id = id(self)  # atributo "privado" (name mangling)
        self._historial: list = []

    # Property — acceso controlado a atributos
    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float):
        if valor < 0:
            raise ValueError("El saldo no puede ser negativo")
        self._saldo = valor

    def depositar(self, cantidad: float) -> None:
        """Añade dinero a la cuenta."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")
        self._saldo += cantidad
        self._historial.append(f"+{cantidad:.2f}€")

    def retirar(self, cantidad: float) -> None:
        """Retira dinero de la cuenta."""
        if cantidad > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= cantidad
        self._historial.append(f"-{cantidad:.2f}€")

    # Métodos especiales (dunder methods)
    def __str__(self) -> str:
        """Representación para humanos."""
        return f"Cuenta de {self.titular}: {self._saldo:.2f}€"

    def __repr__(self) -> str:
        """Representación para desarrolladores."""
        return f"CuentaBancaria(titular={self.titular!r}, saldo={self._saldo})"

    def __len__(self) -> int:
        return len(self._historial)

    def __eq__(self, otra) -> bool:
        if not isinstance(otra, CuentaBancaria):
            return NotImplemented
        return self.__id == otra.__id

    def __lt__(self, otra) -> bool:
        return self._saldo < otra._saldo

    def __add__(self, otra):
        """Combina dos cuentas."""
        nueva = CuentaBancaria(f"{self.titular}+{otra.titular}")
        nueva._saldo = self._saldo + otra._saldo
        return nueva

    @classmethod
    def crear_con_bonus(cls, titular: str, saldo: float) -> "CuentaBancaria":
        """Método de clase — constructor alternativo."""
        cuenta = cls(titular, saldo)
        cuenta._saldo *= 1.1
        return cuenta

    @staticmethod
    def validar_iban(iban: str) -> bool:
        """Método estático — no accede a la instancia ni a la clase."""
        return len(iban) == 24 and iban[:2].isalpha()


# HERENCIA
class CuentaPremium(CuentaBancaria):
    """Cuenta con beneficios adicionales."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0, limite_credito: float = 1000.0):
        super().__init__(titular, saldo_inicial)  # llama al padre
        self.limite_credito = limite_credito

    def retirar(self, cantidad: float) -> None:
        """Override: permite descubierto hasta el límite."""
        if cantidad > self._saldo + self.limite_credito:
            raise ValueError("Excede el límite de crédito")
        self._saldo -= cantidad
        self._historial.append(f"-{cantidad:.2f}€")

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} [PREMIUM, crédito: {self.limite_credito:.2f}€]"


# HERENCIA MÚLTIPLE
class Auditable:
    def log(self, mensaje: str):
        print(f"[AUDIT] {mensaje}")


class CuentaAuditada(CuentaBancaria, Auditable):
    def depositar(self, cantidad: float) -> None:
        super().depositar(cantidad)
        self.log(f"Depósito de {cantidad:.2f}€")


# CLASES ABSTRACTAS
from abc import ABC, abstractmethod


class Forma(ABC):
    """Clase base abstracta — no se puede instanciar."""

    @abstractmethod
    def area(self) -> float:
        """Cada subclase DEBE implementar esto."""
        ...

    @abstractmethod
    def perimetro(self) -> float: ...

    def describir(self) -> str:
        return f"Área: {self.area():.2f}, Perímetro: {self.perimetro():.2f}"


class Circulo(Forma):
    def __init__(self, radio: float):
        self.radio = radio

    def area(self) -> float:
        import math

        return math.pi * self.radio**2

    def perimetro(self) -> float:
        import math

        return 2 * math.pi * self.radio


# DATACLASSES (Python 3.7+) — reduce boilerplate
from dataclasses import dataclass, field


@dataclass
class Producto:
    nombre: str
    precio: float
    stock: int = 0
    etiquetas: list = field(default_factory=list)

    def __post_init__(self):
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")

    def con_descuento(self, porcentaje: float) -> "Producto":
        return Producto(nombre=self.nombre, precio=self.precio * (1 - porcentaje), stock=self.stock)


@dataclass(frozen=True)  # inmutable, hasheable
class Punto:
    x: float
    y: float
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECORADORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
import functools


# Decorador básico
def log_llamada(funcion):
    @functools.wraps(funcion)  # preserva nombre, docstring, etc.
    def wrapper(*args, **kwargs):
        print(f"Llamando a {funcion.__name__}")
        resultado = funcion(*args, **kwargs)
        print(f"{funcion.__name__} terminó")
        return resultado

    return wrapper


@log_llamada
def saludar(nombre):
    return f"Hola, {nombre}"


# Decorador con argumentos
def reintentar(veces=3, pausa=1.0):
    def decorador(funcion):
        @functools.wraps(funcion)
        def wrapper(*args, **kwargs):
            import time

            for intento in range(veces):
                try:
                    return funcion(*args, **kwargs)
                except Exception as e:
                    if intento == veces - 1:
                        raise
                    print(f"Intento {intento + 1} fallido: {e}")
                    time.sleep(pausa)

        return wrapper

    return decorador


@reintentar(veces=3, pausa=0.5)
def llamada_api(): ...


# Decorador de clase (para todos los métodos)
def medir_tiempo(cls):
    import time

    for nombre, metodo in vars(cls).items():
        if callable(metodo) and not nombre.startswith("_"):
            setattr(cls, nombre, log_llamada(metodo))
    return cls


# Decoradores de la stdlib
@property  # acceso controlado a atributo
@classmethod  # método de clase
@staticmethod  # método estático
@functools.lru_cache(maxsize=128)  # memoización automática
@functools.cache  # Python 3.9+, ilimitado
@functools.cached_property  # property calculada una vez
# lru_cache — cachea resultados de función (muy útil)
@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


fibonacci(100)  # instantáneo con caché, sin caché tardaría siglos
fibonacci.cache_info()  # estadísticas del caché
fibonacci.cache_clear()  # limpiar caché
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENERADORES E ITERADORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Generador — función que usa yield
def contar_hasta(n):
    """Genera números del 1 al n sin guardarlos todos en memoria."""
    i = 1
    while i <= n:
        yield i
        i += 1


gen = contar_hasta(5)
next(gen)  # 1
next(gen)  # 2
for num in contar_hasta(5):
    print(num)


# yield from — delega a otro iterable
def cadena(*iterables):
    for it in iterables:
        yield from it


list(cadena([1, 2], [3, 4], [5]))  # [1, 2, 3, 4, 5]


# Generadores infinitos
def enteros_naturales():
    n = 1
    while True:
        yield n
        n += 1


# Con itertools
import itertools

list(itertools.islice(enteros_naturales(), 10))  # primeros 10

# Generator expression
cuadrados = (x**2 for x in range(1000000))  # no crea lista
sum(cuadrados)  # eficiente en memoria


# Iterador personalizado
class Rango:
    def __init__(self, inicio, fin, paso=1):
        self.actual = inicio
        self.fin = fin
        self.paso = paso

    def __iter__(self):
        return self

    def __next__(self):
        if self.actual >= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual += self.paso
        return valor


# itertools — herramientas para iteración
import itertools

itertools.count(10, 2)  # 10, 12, 14, ... (infinito)
itertools.cycle([1, 2, 3])  # 1, 2, 3, 1, 2, 3, ... (infinito)
itertools.repeat(5, 3)  # 5, 5, 5
itertools.chain([1, 2], [3, 4])  # 1, 2, 3, 4
itertools.islice(gen, 5)  # primeros 5 de cualquier iterable
itertools.product([1, 2], [3, 4])  # producto cartesiano
itertools.combinations([1, 2, 3], 2)  # (1,2), (1,3), (2,3)
itertools.permutations([1, 2, 3], 2)  # todas las permutaciones
itertools.groupby(lista, key)  # agrupar por función
itertools.accumulate([1, 2, 3, 4], lambda a, b: a + b)  # 1,3,6,10
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXT MANAGERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Implementar __enter__ y __exit__
class ConexionBD:
    def __init__(self, url: str):
        self.url = url
        self.conexion = None

    def __enter__(self):
        self.conexion = conectar(self.url)
        return self.conexion

    def __exit__(self, tipo_exc, valor_exc, traceback):
        if self.conexion:
            self.conexion.cerrar()
        # Retorna True para suprimir la excepción, False/None para propagarla
        return False


with ConexionBD("postgresql://...") as conn:
    conn.ejecutar("SELECT 1")

# Con contextlib.contextmanager — más sencillo
from contextlib import contextmanager, suppress


@contextmanager
def tempdir():
    import tempfile, shutil

    directorio = tempfile.mkdtemp()
    try:
        yield directorio
    finally:
        shutil.rmtree(directorio)


with tempdir() as td:
    # td existe aquí
    pass
# td fue eliminado automáticamente

# suppress — ignorar excepciones específicas
with suppress(FileNotFoundError):
    Path("no_existe.txt").unlink()

# ExitStack — múltiples context managers dinámicamente
from contextlib import ExitStack

archivos = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    fds = [stack.enter_context(open(f)) for f in archivos]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIPADO ESTÁTICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Python es dinámico pero permite type hints (PEP 484+)
# No son obligatorios ni se verifican en runtime (salvo con mypy/pyright)

from typing import Optional, Union, Any, Callable
from typing import List, Dict, Tuple, Set  # Python < 3.9
# Python 3.9+: usar list, dict, tuple, set directamente


# Funciones
def saludar(nombre: str, formal: bool = False) -> str: ...


def procesar(datos: list[int]) -> dict[str, int]: ...


# Optional (puede ser None)
def buscar(id: int) -> Optional[str]:  # str | None en 3.10+
    ...


# Union (varios tipos posibles)
def parsear(valor: Union[str, int]) -> str:  # str | int en 3.10+
    ...


# Callable
def aplicar(funcion: Callable[[int], str], valor: int) -> str:
    return funcion(valor)


# TypeVar — tipos genéricos
from typing import TypeVar, Generic

T = TypeVar("T")


def primero(lista: list[T]) -> T:
    return lista[0]


# Literal — valores concretos
from typing import Literal


def ordenar(orden: Literal["asc", "desc"]) -> None: ...


# TypedDict — diccionario con tipos
from typing import TypedDict


class Persona(TypedDict):
    nombre: str
    edad: int
    email: str


# Protocol — duck typing con tipos (Python 3.8+)
from typing import Protocol


class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...


# Verificar con mypy
# pip install mypy
# mypy mi_script.py

# Verificar con pyright (más rápido, el que usa Pylance en VS Code)
# pip install pyright
# pyright mi_script.py
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXPRESIONES REGULARES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
import re

texto = "Mi email es ana@ejemplo.com y mi teléfono 612-345-678"

# Funciones principales
re.search(patron, texto)  # primer match en cualquier posición
re.match(patron, texto)  # match solo al inicio
re.fullmatch(patron, texto)  # match de todo el texto
re.findall(patron, texto)  # lista de todos los matches
re.finditer(patron, texto)  # iterador de objetos Match
re.sub(patron, reemplazo, texto)  # sustituir
re.split(patron, texto)  # dividir

# Compilar para reusar (más eficiente)
patron_email = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
emails = patron_email.findall(texto)

# Metacaracteres
# .    cualquier carácter excepto \n
# ^    inicio de línea
# $    fin de línea
# *    0 o más repeticiones
# +    1 o más repeticiones
# ?    0 o 1 repetición
# {n}  exactamente n repeticiones
# {n,} mínimo n repeticiones
# {n,m} entre n y m repeticiones
# []   clase de caracteres
# [^]  clase de caracteres negada
# |    alternativa (or)
# ()   grupo de captura
# (?:) grupo sin captura
# \d   dígito [0-9]
# \D   no dígito
# \w   alfanumérico + guion bajo [a-zA-Z0-9_]
# \W   no alfanumérico
# \s   espacio en blanco
# \S   no espacio
# \b   límite de palabra
# r"" prefijo raw — no interpreta backslashes

# Grupos de captura
patron = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
match = patron.search("Fecha: 2024-03-15")
if match:
    año, mes, dia = match.groups()
    año = match.group(1)  # "2024"

# Grupos con nombre
patron = re.compile(r"(?P<año>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})")
match = patron.search("2024-03-15")
if match:
    print(match.group("año"))  # "2024"

# Flags
re.IGNORECASE  # re.I — insensible a mayúsculas
re.MULTILINE  # re.M — ^ y $ aplican a cada línea
re.DOTALL  # re.S — . incluye \n
re.VERBOSE  # re.X — permite espacios y comentarios en el patrón
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONCURRENCIA Y PARALELISMO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# THREADING — I/O concurrente (GIL limita CPU)
import threading


def descargar(url: str):
    print(f"Descargando {url}")
    # ... lógica de descarga


hilos = []
urls = ["url1", "url2", "url3"]
for url in urls:
    hilo = threading.Thread(target=descargar, args=(url,))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()  # espera a que termine

# Lock — evitar race conditions
lock = threading.Lock()
contador = 0


def incrementar():
    global contador
    with lock:
        contador += 1


# MULTIPROCESSING — paralelismo real de CPU
import multiprocessing


def procesar(datos):
    return [x**2 for x in datos]


with multiprocessing.Pool(processes=4) as pool:
    resultados = pool.map(procesar, listas_de_datos)

# ASYNCIO — I/O asíncrono (Python 3.7+)
import asyncio
import aiohttp  # pip install aiohttp


async def descargar_async(session, url: str) -> str:
    async with session.get(url) as respuesta:
        return await respuesta.text()


async def main():
    urls = ["https://ejemplo.com/1", "https://ejemplo.com/2"]
    async with aiohttp.ClientSession() as session:
        tareas = [descargar_async(session, url) for url in urls]
        resultados = await asyncio.gather(*tareas)
    return resultados


asyncio.run(main())

# Conceptos asyncio
# async def   — define corrutina
# await       — suspende la corrutina hasta que el awaitable termina
# asyncio.gather() — ejecuta corrutinas concurrentemente
# asyncio.create_task() — programa una tarea
# asyncio.sleep()  — pausa sin bloquear
# asyncio.timeout()  — timeout para operaciones (Python 3.11+)


async def con_timeout():
    try:
        async with asyncio.timeout(5.0):
            await operacion_lenta()
    except TimeoutError:
        print("Timeout")


# CONCURRENT.FUTURES — interfaz de alto nivel
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Para I/O (threads)
with ThreadPoolExecutor(max_workers=10) as executor:
    futuros = [executor.submit(descargar, url) for url in urls]
    resultados = [f.result() for f in futuros]

# map funcional
with ThreadPoolExecutor() as executor:
    resultados = list(executor.map(procesar, datos))
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTING CON PYTEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# pip install pytest pytest-cov

# test_calculadora.py
import pytest
from calculadora import dividir, suma


# Test básico
def test_suma_dos_enteros():
    assert suma(2, 3) == 5


def test_suma_negativos():
    assert suma(-1, -1) == -2


# Test de excepción
def test_division_por_cero():
    with pytest.raises(ValueError, match="cero"):
        dividir(10, 0)


# Fixtures — setup y teardown reutilizables
@pytest.fixture
def cuenta_bancaria():
    """Crea una cuenta para usar en los tests."""
    from banco import CuentaBancaria

    return CuentaBancaria("Test", 100.0)


@pytest.fixture(scope="module")  # se crea una vez por módulo
def bd_temporal():
    # setup
    db = crear_bd_test()
    yield db  # el test se ejecuta aquí
    # teardown
    db.eliminar()


def test_depositar(cuenta_bancaria):
    cuenta_bancaria.depositar(50)
    assert cuenta_bancaria.saldo == 150.0


# Parametrize — el mismo test con múltiples casos
@pytest.mark.parametrize(
    "a, b, esperado",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -50, 50),
    ],
)
def test_suma_parametrizado(a, b, esperado):
    assert suma(a, b) == esperado


# Marks — categorizar tests
@pytest.mark.slow
def test_proceso_largo(): ...


@pytest.mark.skip(reason="No implementado aún")
def test_pendiente(): ...


@pytest.mark.xfail  # se espera que falle
def test_bug_conocido(): ...


# Mocks — simular dependencias externas
from unittest.mock import patch, MagicMock, call


def test_enviar_email():
    with patch("modulo.smtplib.SMTP") as mock_smtp:
        mock_smtp.return_value.__enter__.return_value.sendmail = MagicMock()
        enviar_email("dest@test.com", "Asunto", "Cuerpo")
        mock_smtp.assert_called_once()


# Ejecutar tests
# pytest                        — todos los tests
# pytest tests/                 — directorio específico
# pytest -v                     — verbose
# pytest -k "test_suma"         — filtrar por nombre
# pytest -m "not slow"          — excluir marks
# pytest --cov=mi_modulo        — con coverage
# pytest --cov=mi_modulo --cov-report=html  — reporte HTML
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGGING PROFESIONAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
import logging
import logging.config

# Configuración básica
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Logger por módulo (práctica recomendada)
logger = logging.getLogger(__name__)

logger.debug("Detalle para desarrollo")
logger.info("Información general")
logger.warning("Algo inesperado pero no crítico")
logger.error("Error que requiere atención")
logger.critical("Error grave, posible caída del sistema")

# Logging con contexto
logger.info("Usuario conectado: %s", usuario_id)  # sin f-string: lazy eval
logger.error("Error procesando orden %s: %s", orden_id, str(e), exc_info=True)

# Configuración de producción
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"class": "pythonjsonlogger.jsonlogger.JsonFormatter"},
        "estándar": {"format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"},
    },
    "handlers": {
        "consola": {
            "class": "logging.StreamHandler",
            "formatter": "estándar",
        },
        "fichero": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "estándar",
        },
    },
    "root": {"level": "INFO", "handlers": ["consola", "fichero"]},
}

logging.config.dictConfig(config)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENUMERACIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
from enum import Enum, IntEnum, auto, Flag


class Estado(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


# Uso
estado = Estado.PENDIENTE
estado.name  # "PENDIENTE"
estado.value  # "pendiente"

Estado["PENDIENTE"]  # por nombre
Estado("pendiente")  # por valor

for e in Estado:  # iterable
    print(e)


# auto() — valor automático
class Color(Enum):
    ROJO = auto()  # 1
    VERDE = auto()  # 2
    AZUL = auto()  # 3


# IntEnum — comparable con enteros
class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


Prioridad.ALTA > Prioridad.MEDIA  # True
Prioridad.ALTA > 2  # True


# Flag — combinable con | (bitflags)
class Permisos(Flag):
    LEER = auto()
    ESCRIBIR = auto()
    EJECUTAR = auto()
    ADMIN = LEER | ESCRIBIR | EJECUTAR


permisos = Permisos.LEER | Permisos.ESCRIBIR
Permisos.LEER in permisos  # True
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FUNCIONES AVANZADAS DE LA STDLIB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# COLLECTIONS
from collections import Counter, defaultdict, OrderedDict, deque, ChainMap, namedtuple

# Counter — contar elementos
c = Counter("mississippi")
c.most_common(3)  # [('s', 4), ('i', 4), ('p', 2)]
c + Counter("abc")  # suma
c - Counter("sss")  # resta (elimina negativos)

# defaultdict — diccionario con valor por defecto
grupos = defaultdict(list)
for nombre, grupo in datos:
    grupos[grupo].append(nombre)  # no KeyError al añadir

# deque — cola de doble extremo
cola = deque(maxlen=3)  # descarta el más antiguo cuando llena
cola.append(1)
cola.appendleft(0)  # insertar al inicio
cola.pop()
cola.popleft()
cola.rotate(1)  # rota los elementos

# FUNCTOOLS
import functools

functools.partial(pow, 2)  # nueva función con primer arg fijo
functools.reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10 (fold left)
functools.wraps  # preservar metadatos en decoradores
functools.lru_cache  # memoización
functools.total_ordering  # completa métodos de comparación


@functools.total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, otra):
        return (self.major, self.minor) == (otra.major, otra.minor)

    def __lt__(self, otra):
        return (self.major, self.minor) < (otra.major, otra.minor)

    # __le__, __gt__, __ge__ se generan automáticamente


# DATETIME
from datetime import datetime, date, time, timedelta, timezone

ahora = datetime.now()
hoy = date.today()
utc_ahora = datetime.now(timezone.utc)

# Formatear
ahora.strftime("%Y-%m-%d %H:%M:%S")  # "2024-03-15 14:30:00"
ahora.strftime("%d/%m/%Y")  # "15/03/2024"

# Parsear
datetime.strptime("2024-03-15", "%Y-%m-%d")

# Aritmética
ayer = hoy - timedelta(days=1)
proxima_semana = ahora + timedelta(weeks=1, hours=2)
diferencia = datetime(2024, 12, 31) - datetime.now()
diferencia.days  # días de diferencia

# PATHLIB
from pathlib import Path

# Construir rutas portables
ruta = Path.home() / "documentos" / "proyecto"
ruta.mkdir(parents=True, exist_ok=True)

Path.cwd()  # directorio actual
Path.home()  # directorio home
Path(__file__)  # ruta del script actual

# OS
import os

os.environ.get("HOME", "/tmp")  # variable de entorno
os.getcwd()  # directorio actual
os.listdir(".")  # listar directorio
os.path.join("a", "b", "c")  # "a/b/c" o "a\b\c" según SO
os.path.exists(ruta)
os.path.abspath(ruta)  # ruta absoluta
os.makedirs("a/b/c", exist_ok=True)
os.rename("viejo.txt", "nuevo.txt")
os.remove("fichero.txt")
os.getenv("DB_HOST", "localhost")  # equivalente a environ.get

# SUBPROCESS
import subprocess

# Ejecutar comando y capturar salida
resultado = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True,
    check=True,  # lanza CalledProcessError si el código de salida != 0
)
print(resultado.stdout)
print(resultado.returncode)

# Shell (evitar con input de usuario — riesgo de injection)
resultado = subprocess.run("ls -la | grep py", shell=True, capture_output=True, text=True)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
METACLASES Y DESCRIPTORES (AVANZADO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# DESCRIPTORES — controlan acceso a atributos
class Positivo:
    """Descriptor que valida que el valor sea positivo."""

    def __set_name__(self, owner, name):
        self.nombre = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.nombre, 0)

    def __set__(self, instance, valor):
        if valor <= 0:
            raise ValueError(f"{self.nombre} debe ser positivo")
        setattr(instance, self.nombre, valor)


class Producto:
    precio = Positivo()
    stock = Positivo()

    def __init__(self, precio, stock):
        self.precio = precio  # usa el descriptor
        self.stock = stock


# METACLASES — "clases de clases"
class Singleton(type):
    """Metaclase que implementa el patrón Singleton."""

    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]


class Configuracion(metaclass=Singleton):
    def __init__(self):
        self.debug = False
        self.bd_url = ""


# __init_subclass__ — hook para cuando alguien hereda de tu clase
class Plugin:
    subclases = []

    def __init_subclass__(cls, nombre=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.nombre = nombre or cls.__name__
        Plugin.subclases.append(cls)


class MiPlugin(Plugin, nombre="mi_plugin"):
    pass
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUENAS PRÁCTICAS Y PEP 8
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTILO (PEP 8 — guía de estilo oficial)
- Indentación: 4 espacios (nunca tabs)
- Líneas máximo 88-120 caracteres (79 es el histórico, hoy se usa 88/120)
- 2 líneas en blanco entre funciones/clases de nivel superior
- 1 línea en blanco entre métodos dentro de una clase
- Importaciones al principio: stdlib → terceros → locales
- No mezclar ; en una línea con múltiples sentencias

ANTIPATRONES COMUNES
```python
# MAL
if x == True:     # BIEN: if x:
if x == None:     # BIEN: if x is None:
if len(lista) == 0:  # BIEN: if not lista:

# MAL — except demasiado amplio
try: ...
except: ...       # captura hasta SystemExit y KeyboardInterrupt

# MAL — concatenar strings en bucle (O(n²))
resultado = ""
for s in lista:
    resultado += s   # crea un string nuevo en cada iteración

# BIEN
resultado = "".join(lista)

# MAL — construir lista para solo iterar
for x in list(generador):  # innecesario si solo iteras
    ...

# BIEN
for x in generador:
    ...

# MAL — comparar tipo con type()
if type(x) == int:   # no detecta subclases
# BIEN
if isinstance(x, int):

# MAL — abrir sin context manager
f = open("fichero.txt")
contenido = f.read()
# si hay excepción, f nunca se cierra

# BIEN
with open("fichero.txt") as f:
    contenido = f.read()
```

PRINCIPIOS SOLID EN PYTHON
- S: Una clase, una responsabilidad
- O: Abierto para extensión, cerrado para modificación
- L: Las subclases deben poder reemplazar a la clase base
- I: Interfaces pequeñas y específicas (Protocols en Python)
- D: Depender de abstracciones, no de implementaciones concretas

HERRAMIENTAS DE CALIDAD
```bash
# Linting y formateo
pip install ruff    # todo en uno: reemplaza flake8 + black + isort
ruff check .        # linting
ruff format .       # formateo

# Type checking
pip install mypy
mypy mi_modulo.py

# Testing con coverage
pip install pytest pytest-cov
pytest --cov=src --cov-report=html

# Pre-commit hooks (automatizar todo esto)
pip install pre-commit
# crear .pre-commit-config.yaml
```
