# CONOCIMIENTO 3 — ECOSISTEMA PYTHON
# Librerías, frameworks, herramientas y casos de uso.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GESTIÓN DE PAQUETES Y ENTORNOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIP — GESTOR DE PAQUETES CLÁSICO
```bash
pip install requests              # instalar
pip install requests==2.31.0      # versión exacta
pip install "requests>=2.28"      # mínimo
pip install -r requirements.txt   # desde fichero
pip install -e .                  # modo editable (desarrollo)
pip uninstall requests
pip list                          # paquetes instalados
pip show requests                 # info del paquete
pip freeze > requirements.txt     # guardar dependencias
pip install --upgrade requests    # actualizar
```

UV — GESTOR MODERNO (recomendado 2024+)
```bash
# 10-100x más rápido que pip, reemplaza pip + venv + pip-tools
# Instalación oficial (NO usar pip install uv — contamina el entorno global)
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

uv init mi_proyecto               # nuevo proyecto
uv add requests                   # añadir dependencia
uv add --dev pytest ruff mypy     # solo desarrollo
uv remove requests
uv run python script.py           # ejecutar en el entorno del proyecto
uv sync                           # sincronizar entorno con pyproject.toml
uv lock                           # generar lockfile
uv pip install ...                # interfaz compatible con pip
uv python install 3.13            # instalar versiones de Python
```

PYPROJECT.TOML — CONFIGURACIÓN MODERNA
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mi-proyecto"
version = "0.1.0"
description = "Descripción del proyecto"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
    "mypy>=1.9",
]

[tool.ruff]
line-length = 88

[tool.ruff.lint]                    # ⚠️ desde ruff 0.2+ debe ir aquí, no en [tool.ruff]
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESARROLLO WEB — BACKEND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FASTAPI — API moderna y rápida (recomendado para nuevos proyectos)
```python
# pip install fastapi uvicorn[standard] pydantic

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

app = FastAPI(title="Mi API", version="1.0.0")

# Simula una base de datos en memoria
productos_db: dict[int, dict] = {}
_next_id = 1


class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    stock: int = 0

    @field_validator("precio")
    @classmethod
    def precio_positivo(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser positivo")
        return v


class ProductoRespuesta(ProductoCrear):
    id: int


@app.get("/productos", response_model=list[ProductoRespuesta])
async def listar_productos(skip: int = 0, limit: int = 100):
    items = list(productos_db.values())
    return items[skip : skip + limit]


@app.get("/productos/{producto_id}", response_model=ProductoRespuesta)
async def obtener_producto(producto_id: int):
    producto = productos_db.get(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.post("/productos", response_model=ProductoRespuesta, status_code=201)
async def crear_producto(producto: ProductoCrear):
    global _next_id
    nuevo = {"id": _next_id, **producto.model_dump()}
    productos_db[_next_id] = nuevo
    _next_id += 1
    return nuevo


# Dependencias (inyección)
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    usuario = verificar_token(token)
    if not usuario:
        raise HTTPException(status_code=401)
    return usuario


@app.get("/perfil")
async def mi_perfil(usuario=Depends(obtener_usuario_actual)):
    return usuario


# Ejecutar: uvicorn main:app --reload
# Docs automáticas: http://localhost:8000/docs (Swagger)
#                   http://localhost:8000/redoc
```

FLASK — Microframework, simple y flexible
```python
# pip install flask

from flask import Flask, jsonify, request, abort
from functools import wraps

app = Flask(__name__)


@app.route("/productos", methods=["GET"])
def listar_productos():
    productos = obtener_todos()
    return jsonify(productos)


@app.route("/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    producto = buscar_por_id(id)
    if not producto:
        abort(404)
    return jsonify(producto)


@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()
    if not datos:
        abort(400)
    nuevo = guardar(datos)
    return jsonify(nuevo), 201


if __name__ == "__main__":
    app.run(debug=True)  # nunca debug=True en producción
```

DJANGO — Framework completo (batteries included)
```python
# pip install django djangorestframework

# models.py
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return self.nombre


# views.py (con DRF)
from rest_framework import viewsets, permissions
from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Comandos Django
# django-admin startproject mi_proyecto
# python manage.py startapp productos
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTTP Y APIs — CLIENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUESTS — HTTP para humanos
```python
# pip install requests

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()

# Retry automático
retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

# GET
response = session.get(
    "https://api.ejemplo.com/productos",
    params={"page": 1, "limit": 10},
    headers={"Authorization": "Bearer TOKEN"},
    timeout=(3.05, 27),  # (connect timeout, read timeout)
)
response.raise_for_status()  # lanza HTTPError si 4xx/5xx
datos = response.json()

# POST
response = session.post(
    "https://api.ejemplo.com/productos",
    json={"nombre": "Widget", "precio": 9.99},
    headers={"Authorization": "Bearer TOKEN"},
)

# Descargar fichero
with session.get(url, stream=True) as r:
    r.raise_for_status()
    with open("fichero.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
```

HTTPX — Moderno, async-compatible
```python
# pip install httpx

import httpx

# Síncrono
with httpx.Client(timeout=30.0) as client:
    response = client.get("https://api.ejemplo.com/data")

# Asíncrono
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.ejemplo.com/data")
    datos = response.json()
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDACIÓN DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYDANTIC — Validación de datos
```python
# pip install pydantic (v2)

from pydantic import BaseModel, EmailStr, field_validator, model_validator
from pydantic import Field
from typing import Optional
from datetime import datetime


class Usuario(BaseModel):
    id: int
    nombre: str = Field(min_length=2, max_length=50)
    email: EmailStr
    edad: Optional[int] = Field(None, ge=0, le=150)
    creado: datetime = Field(default_factory=datetime.now)

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, v: str) -> str:
        return v.strip()

    model_config = {"str_strip_whitespace": True}


# Parsear desde dict
u = Usuario(id=1, nombre="Ana", email="ana@ejemplo.com")
u.model_dump()  # → dict
u.model_dump_json()  # → JSON string

# Parsear desde JSON
u = Usuario.model_validate_json('{"id": 1, "nombre": "Ana", "email": "ana@ejemplo.com"}')

# Gestionar settings con pydantic-settings
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_url: str
    secret_key: str
    debug: bool = False

    model_config = {"env_file": ".env"}


config = Config()  # lee automáticamente del .env
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASES DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SQLITE3 — Integrado en Python
```python
import sqlite3
from contextlib import contextmanager


@contextmanager
def conexion(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # acceso por nombre de columna
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


with conexion("productos.db") as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL CHECK(precio > 0)
        )
    """)
    conn.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ("Widget", 9.99))
    cursor = conn.execute("SELECT * FROM productos")
    for fila in cursor:
        print(dict(fila))
```

SQLALCHEMY — ORM moderno (2.x, estilo actual)
```python
# pip install sqlalchemy

from sqlalchemy import create_engine, String, Float, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column

engine = create_engine("postgresql://usuario:pass@localhost/db", pool_size=5, max_overflow=10, echo=False)


class Base(DeclarativeBase):
    pass


# Estilo moderno con Mapped y mapped_column (SQLAlchemy 2.0+)
class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"Producto(id={self.id}, nombre={self.nombre!r})"


# Crear tablas
Base.metadata.create_all(engine)

# Operaciones CRUD (estilo SQLAlchemy 2.x)
with Session(engine) as session:
    # Create
    producto = Producto(nombre="Widget", precio=9.99)
    session.add(producto)
    session.commit()

    # Read — usar select() en lugar de session.query() (deprecated)
    producto = session.get(Producto, 1)
    stmt = select(Producto).where(Producto.precio > 5)
    productos = session.execute(stmt).scalars().all()

    # Update
    producto.precio = 12.99
    session.commit()

    # Delete
    session.delete(producto)
    session.commit()
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCRAPING Y AUTOMATIZACIÓN WEB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEAUTIFULSOUP4 — Parsear HTML/XML
```python
# pip install beautifulsoup4 lxml

import requests
from bs4 import BeautifulSoup

response = requests.get("https://ejemplo.com")
soup = BeautifulSoup(response.text, "lxml")

# Navegar el DOM
titulo = soup.find("h1").text
enlaces = soup.find_all("a", class_="producto")
precio = soup.select_one(".precio").text.strip()
todos_los_links = [a.get("href") for a in soup.select("a[href]")]

# Iterar resultados
for articulo in soup.find_all("article", class_="post"):
    titulo = articulo.find("h2").text
    fecha = articulo.find("time")["datetime"]
    print(titulo, fecha)
```

PLAYWRIGHT — Automatización de navegador (recomendado sobre Selenium)
```python
# pip install playwright
# playwright install chromium

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://ejemplo.com/login")
    page.fill("#email", "usuario@ejemplo.com")
    page.fill("#password", "contraseña")
    page.click("button[type=submit]")

    page.wait_for_url("**/dashboard")
    screenshot = page.screenshot(path="dashboard.png")

    # Scraping de contenido dinámico (JS)
    page.goto("https://spa.ejemplo.com")
    page.wait_for_selector(".productos")
    productos = page.query_selector_all(".producto")
    nombres = [p.inner_text() for p in productos]

    browser.close()
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CIENCIA DE DATOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NUMPY — Arrays y matemática vectorial
```python
# pip install numpy

import numpy as np

# Crear arrays
a = np.array([1, 2, 3, 4, 5])
b = np.zeros((3, 4))
c = np.ones((2, 3))
d = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
e = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1.0]
f = np.random.rand(3, 3)  # valores aleatorios entre 0 y 1

# Operaciones vectoriales (sin bucles explícitos)
a * 2  # [2, 4, 6, 8, 10]
a + b  # broadcasting
np.sqrt(a)
np.sum(a)
np.mean(a)
np.std(a)
np.dot(A, B)  # multiplicación de matrices
A @ B  # equivalente con @

# Indexación avanzada
a[a > 3]  # [4, 5] — boolean indexing
a[[0, 2, 4]]  # [1, 3, 5] — fancy indexing
matriz[0, :]  # primera fila
matriz[:, 0]  # primera columna
matriz[1:3, 1:3]  # submatriz

# Reshape
a.reshape(5, 1)
a.flatten()
np.concatenate([a, b])
np.stack([a, b])
```

PANDAS — Análisis de datos tabular
```python
# pip install pandas

import pandas as pd

# Crear DataFrame
df = pd.DataFrame(
    {"nombre": ["Ana", "Luis", "María"], "edad": [25, 30, 35], "ciudad": ["Madrid", "Barcelona", "Madrid"]}
)

# Desde fichero
df = pd.read_csv("datos.csv")
df = pd.read_excel("datos.xlsx")
df = pd.read_json("datos.json")

# Exploración
df.head(10)
df.tail(5)
df.info()
df.describe()
df.shape  # (filas, columnas)
df.columns
df.dtypes
df.isnull().sum()  # valores nulos por columna

# Selección
df["edad"]  # Serie (columna)
df[["nombre", "edad"]]  # DataFrame (varias columnas)
df.loc[0]  # fila por etiqueta
df.iloc[0]  # fila por posición
df.loc[df["ciudad"] == "Madrid"]  # filtrar
df.query("edad > 28 and ciudad == 'Madrid'")

# Modificar
df["edad_doble"] = df["edad"] * 2
df.rename(columns={"nombre": "name"})
df.drop(columns=["edad_doble"])
df.dropna()  # eliminar filas con nulos
df.fillna(0)  # rellenar nulos con 0

# Agrupar y agregar
df.groupby("ciudad")["edad"].mean()
df.groupby("ciudad").agg({"edad": ["mean", "min", "max"]})

# Ordenar
df.sort_values("edad", ascending=False)

# Merge (JOIN)
pd.merge(df1, df2, on="id", how="left")

# Guardar
df.to_csv("resultado.csv", index=False)
df.to_excel("resultado.xlsx", index=False)
```

POLARS — Alternativa a Pandas, más rápida (Rust)
```python
# pip install polars

import polars as pl

# Crear DataFrame
df = pl.DataFrame(
    {"nombre": ["Ana", "Luis", "María"], "edad": [25, 30, 35], "ciudad": ["Madrid", "Barcelona", "Madrid"]}
)

# Desde fichero (lazy por defecto = más eficiente en memoria)
df = pl.read_csv("datos.csv")
df_lazy = pl.scan_csv("datos_grandes.csv")  # lazy

# Selección y filtrado (API expresiva)
df.select(["nombre", "edad"])
df.filter(pl.col("edad") > 28)
df.filter(pl.col("ciudad") == "Madrid")

# Agrupar
df.group_by("ciudad").agg(pl.col("edad").mean().alias("edad_media"))

# Con lazy (se ejecuta al llamar .collect())
resultado = pl.scan_csv("datos.csv").filter(pl.col("edad") > 25).group_by("ciudad").agg(pl.col("edad").mean()).collect()

# vs Pandas: Polars es 5-20x más rápido en datasets grandes,
# no tiene índice, y la API es más consistente y predecible
```

MATPLOTLIB Y SEABORN — Visualización
```python
# pip install matplotlib seaborn

import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib básico
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot([1, 2, 3], [4, 5, 6], label="Línea A", color="blue")
axes[0].scatter(x, y, c=colores, alpha=0.7)
axes[0].bar(categorias, valores)
axes[0].set_xlabel("Eje X")
axes[0].set_ylabel("Eje Y")
axes[0].set_title("Mi gráfica")
axes[0].legend()

plt.tight_layout()
plt.savefig("grafica.png", dpi=150, bbox_inches="tight")
plt.show()

# Seaborn — estadístico y bonito por defecto
sns.set_theme(style="whitegrid")
sns.histplot(data=df, x="edad", hue="ciudad", kde=True)
sns.boxplot(data=df, x="ciudad", y="precio")
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
sns.pairplot(df, hue="categoria")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYTEST — Framework de testing (estándar de facto)
```python
# pip install pytest pytest-cov pytest-asyncio

import pytest
from unittest.mock import MagicMock, patch


# Test básico
def test_suma():
    assert 1 + 1 == 2


# Fixtures — reutilizar estado entre tests
@pytest.fixture
def usuario():
    return {"id": 1, "nombre": "Ana", "email": "ana@ejemplo.com"}


@pytest.fixture
def db_vacia(tmp_path):
    """Crea una BD temporal en un directorio limpio."""
    db_path = tmp_path / "test.db"
    inicializar_db(db_path)
    yield db_path
    # Limpieza automática al finalizar el test


def test_crear_usuario(usuario, db_vacia):
    resultado = crear_usuario(db_vacia, usuario)
    assert resultado["id"] == usuario["id"]


# Parametrize — ejecutar el mismo test con distintos valores
@pytest.mark.parametrize(
    "entrada,esperado",
    [
        ("hola mundo", "HOLA MUNDO"),
        ("", ""),
        ("  espacios  ", "  ESPACIOS  "),
    ],
)
def test_a_mayusculas(entrada, esperado):
    assert a_mayusculas(entrada) == esperado


# Mocks — reemplazar dependencias externas
def test_enviar_email():
    with patch("mi_modulo.smtplib.SMTP_SSL") as mock_smtp:
        instancia = mock_smtp.return_value.__enter__.return_value
        enviar_email("dest@ejemplo.com", "Asunto", "Cuerpo")
        instancia.send_message.assert_called_once()


# Excepciones esperadas
def test_precio_negativo_lanza_error():
    with pytest.raises(ValueError, match="positivo"):
        validar_precio(-5.0)


# Tests asíncronos
@pytest.mark.asyncio
async def test_obtener_datos_async():
    resultado = await obtener_datos_async()
    assert resultado is not None


# Ejecutar: pytest -v --cov=src --cov-report=html
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASYNC / CONCURRENCIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
import asyncio
import httpx


# Función asíncrona básica
async def obtener_dato(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


# gather — ejecutar varias corrutinas en paralelo
async def main():
    urls = [
        "https://api.ejemplo.com/usuarios/1",
        "https://api.ejemplo.com/usuarios/2",
        "https://api.ejemplo.com/usuarios/3",
    ]
    # Todas las peticiones en paralelo
    resultados = await asyncio.gather(*[obtener_dato(u) for u in urls])
    return resultados


# TaskGroup (Python 3.11+) — manejo de errores más robusto
async def main_taskgroup():
    async with asyncio.TaskGroup() as tg:
        tarea1 = tg.create_task(obtener_dato("https://api.ejemplo.com/a"))
        tarea2 = tg.create_task(obtener_dato("https://api.ejemplo.com/b"))
    # Si cualquier tarea falla, todas se cancelan
    print(tarea1.result(), tarea2.result())


# Timeout
async def con_timeout():
    try:
        resultado = await asyncio.wait_for(obtener_dato(url), timeout=5.0)
    except asyncio.TimeoutError:
        print("La petición tardó demasiado")


# Cola asíncrona (productor-consumidor)
async def productor(queue: asyncio.Queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(0.1)
    await queue.put(None)  # señal de fin


async def consumidor(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        procesar(item)


async def main_queue():
    queue = asyncio.Queue(maxsize=5)
    await asyncio.gather(productor(queue), consumidor(queue))


asyncio.run(main())
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGGING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
import logging
import logging.config
from pathlib import Path

# Configuración básica recomendada
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)  # siempre usar __name__

logger.debug("Detalle de depuración")
logger.info("Información general")
logger.warning("Algo inesperado pero no fatal")
logger.error("Error recuperable")
logger.critical("Error grave")
logger.exception("Error con traceback completo")  # dentro de except


# Configuración avanzada: consola + fichero
def configurar_logging(nivel: str = "INFO", log_file: str | None = None):
    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, nivel.upper()),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )


# Contexto extra en mensajes
logger = logging.getLogger("mi_app.pedidos")
logger.info("Pedido creado", extra={"pedido_id": 42, "usuario": "ana"})

# Suprimir librerías muy verbosas
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Alternativa moderna: structlog (pip install structlog)
# → logs estructurados en JSON, ideal para producción/observabilidad
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLI TOOLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPER — CLI moderno con type hints
```python
# pip install typer rich

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def procesar(
    archivo: typer.FileText = typer.Argument(..., help="Archivo a procesar"),
    salida: str = typer.Option("resultado.txt", "--salida", "-s"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Procesa el archivo y guarda el resultado."""
    if verbose:
        console.print(f"[green]Procesando {archivo.name}...")

    datos = archivo.read()
    # procesar...

    typer.echo(f"Guardado en {salida}")


@app.command()
def listar():
    """Lista todos los elementos."""
    tabla = Table("ID", "Nombre", "Estado")
    tabla.add_row("1", "Elemento A", "[green]OK")
    console.print(tabla)


if __name__ == "__main__":
    app()
```

ARGPARSE — Stdlib, sin dependencias externas
```python
import argparse

parser = argparse.ArgumentParser(description="Mi herramienta CLI")
parser.add_argument("archivo", help="Archivo de entrada")
parser.add_argument("-o", "--salida", default="resultado.txt")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-n", "--numero", type=int, default=10)

args = parser.parse_args()
print(args.archivo, args.salida, args.verbose, args.numero)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATIZACIÓN Y SCRIPTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Organizar archivos por extensión
from pathlib import Path
import shutil


def organizar_descargas(carpeta: Path):
    categorias = {
        "imágenes": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "documentos": [".pdf", ".docx", ".xlsx", ".txt"],
        "vídeos": [".mp4", ".avi", ".mkv", ".mov"],
        "código": [".py", ".js", ".ts", ".html", ".css"],
    }

    for fichero in carpeta.iterdir():
        if not fichero.is_file():
            continue
        extension = fichero.suffix.lower()
        for categoria, extensiones in categorias.items():
            if extension in extensiones:
                destino = carpeta / categoria
                destino.mkdir(exist_ok=True)
                shutil.move(str(fichero), str(destino / fichero.name))
                break


# Enviar email con Python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def enviar_email(destinatario: str, asunto: str, cuerpo: str):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.attach(MIMEText(cuerpo, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
        servidor.send_message(msg)


# Leer y procesar Excel
import openpyxl  # pip install openpyxl

wb = openpyxl.load_workbook("datos.xlsx")
ws = wb.active

for fila in ws.iter_rows(min_row=2, values_only=True):
    id_, nombre, precio = fila
    print(f"{nombre}: {precio}€")

# Tareas programadas
import schedule  # pip install schedule
import time


def tarea_diaria():
    print("Ejecutando informe diario...")


def verificar_api():
    print("Verificando estado de la API...")


def generar_informe_semanal():
    print("Generando informe semanal...")


schedule.every().day.at("08:00").do(tarea_diaria)
schedule.every(30).minutes.do(verificar_api)
schedule.every().monday.do(generar_informe_semanal)

while True:
    schedule.run_pending()
    time.sleep(60)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LIBRERÍAS IMPORTANTES — REFERENCIA RÁPIDA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTTP Y WEB
  requests          → HTTP síncrono, el más usado
  httpx             → HTTP síncrono + async
  aiohttp           → HTTP async nativo
  urllib3           → bajo nivel (requests lo usa internamente)
  fastapi           → API REST/async moderna
  flask             → microframework web
  django            → framework completo
  starlette         → base de FastAPI
  uvicorn           → servidor ASGI rápido
  gunicorn          → servidor WSGI para producción
  websockets        → WebSockets en Python

DATOS Y VALIDACIÓN
  pydantic          → validación de datos, settings
  marshmallow       → serialización/deserialización
  attrs             → como dataclasses pero más potente
  cerberus          → validación de esquemas

BASES DE DATOS
  sqlalchemy        → ORM + Core SQL (usar API 2.x con Mapped/select)
  alembic           → migraciones para SQLAlchemy
  tortoise-orm      → ORM async (para FastAPI/asyncio)
  peewee            → ORM ligero
  psycopg2/3        → driver PostgreSQL (preferir psycopg3)
  aiomysql          → MySQL async
  motor             → MongoDB async
  redis             → cliente Redis
  elasticsearch-py  → cliente Elasticsearch

DATA SCIENCE
  numpy             → arrays y álgebra lineal
  pandas            → análisis de datos tabular
  polars            → alternativa a Pandas más rápida (Rust, recomendada 2025+)
  scipy             → ciencia y matemáticas
  matplotlib        → visualización base
  seaborn           → estadístico y bonito
  plotly            → gráficas interactivas
  bokeh             → visualización web interactiva

MACHINE LEARNING
  scikit-learn      → ML clásico completo
  xgboost           → gradient boosting
  lightgbm          → gradient boosting (rápido)
  pytorch           → DL flexible (investigación y producción)
  tensorflow        → DL de Google
  keras             → API de alto nivel para TF/JAX/PyTorch
  transformers      → modelos LLM de HuggingFace
  langchain         → framework para apps con LLMs
  llama-index       → RAG e indexación de documentos con LLMs
  spacy             → NLP industrial
  nltk              → NLP académico

AUTOMATIZACIÓN
  selenium          → automatización web (legacy)
  playwright        → automatización web (moderno, recomendado)
  pyautogui         → automatizar mouse y teclado
  schedule          → tareas programadas simples
  celery            → cola de tareas distribuida
  apscheduler       → tareas programadas avanzadas
  watchdog          → monitorizar cambios en ficheros

CLI Y TERMINAL
  typer             → CLI con type hints
  click             → CLI flexible y potente
  argparse          → stdlib, sin dependencias
  rich              → salida de consola con color y tablas
  tqdm              → barras de progreso
  prompt_toolkit    → prompts interactivos

TESTING
  pytest            → framework de testing (estándar de facto)
  unittest          → stdlib testing
  hypothesis        → property-based testing
  faker             → generar datos falsos para tests
  factory_boy       → factories para objetos de test
  responses         → mockear llamadas HTTP (síncrono)
  respx             → mockear llamadas httpx (async)
  pytest-asyncio    → testing de código async
  coverage          → medición de cobertura

SEGURIDAD Y CRIPTOGRAFÍA
  cryptography      → criptografía de alto nivel (la mejor)
  bcrypt            → hashing de contraseñas
  python-jose       → JWT
  authlib           → OAuth2 / OpenID Connect
  passlib           → hashing múltiples algoritmos
  certifi           → certificados SSL

CONFIGURACIÓN Y ENTORNO
  python-dotenv     → cargar .env
  pydantic-settings → settings con validación
  dynaconf          → configuración multi-entorno
  click             → también parsea configuración

SERIALIZACIÓN
  json (stdlib)     → JSON
  orjson            → JSON ultrarrápido (C)
  msgpack           → formato binario compacto
  pickle (stdlib)   → serialización Python (no para datos externos)
  protobuf          → Protocol Buffers de Google

CONCURRENCIA Y ASYNC
  asyncio (stdlib)  → base del async en Python
  aiofiles          → I/O de ficheros async
  anyio             → abstracción sobre asyncio/trio
  trio              → async con mejores primitivas
  concurrent.futures → ThreadPool y ProcessPool

LOGGING Y OBSERVABILIDAD
  logging (stdlib)  → logging estándar
  structlog         → logs estructurados (JSON), ideal producción
  loguru            → logging con API más sencilla
  opentelemetry     → trazas, métricas y logs distribuidos

UTILIDADES VARIAS
  pathlib (stdlib)  → rutas modernas
  arrow             → fechas y horas con API mejor que datetime
  pendulum          → fechas con timezone sólido
  humanize          → números y fechas legibles por humanos
  more-itertools    → más herramientas para iteración
  toolz             → funcional en Python
  boltons           → utilidades que deberían estar en stdlib
  chardet           → detectar encoding de texto
  pillow            → manipulación de imágenes
  qrcode            → generar códigos QR
  barcode           → generar códigos de barras
  reportlab         → generar PDFs
  openpyxl          → Excel (.xlsx)
  python-docx       → Word (.docx)
  python-pptx       → PowerPoint (.pptx)
  paramiko          → SSH y SFTP
  fabric            → despliegue y automatización SSH
  docker            → SDK de Docker para Python

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NOVEDADES POR VERSIÓN DE PYTHON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PYTHON 3.10
  · match/case (pattern matching)
  · Union types con | (int | str en lugar de Union[int, str])
  · Mejores mensajes de error de sintaxis

PYTHON 3.11
  · 10-60% más rápido que 3.10
  · ExceptionGroup y except*
  · tomllib en stdlib (leer TOML)
  · Self type en typing
  · Mejor traceback (señala exactamente la expresión que falla)
  · TaskGroup en asyncio (manejo robusto de tareas paralelas)

PYTHON 3.12
  · f-strings más flexibles (expresiones multilínea, comillas anidadas)
  · @override en typing
  · Nueva sintaxis para alias de tipos: type Vector = list[float]
  · Mejor rendimiento del intérprete
  · Deprecación de distutils

PYTHON 3.13 (octubre 2024, release estable)
  · JIT compiler experimental (--enable-experimental-jit)
  · Free-threaded mode experimental (sin GIL) con --disable-gil
    → ya con soporte experimental en numpy, pydantic y otras librerías clave
  · REPL mejorado con coloreado de sintaxis y multilinea
  · copy.replace() para objetos inmutables
  · Mejor rendimiento general (~5% sobre 3.12)

PATTERN MATCHING (3.10+) — MUY ÚTIL
```python
def procesar_comando(comando):
    match comando:
        case {"accion": "crear", "nombre": nombre}:
            return crear(nombre)
        case {"accion": "eliminar", "id": int(id_)}:
            return eliminar(id_)
        case {"accion": "listar"}:
            return listar()
        case _:
            raise ValueError(f"Comando desconocido: {comando}")


# Con clases
match evento:
    case Click(x=x, y=y) if x > 0 and y > 0:
        print(f"Click en cuadrante positivo: {x}, {y}")
    case KeyPress(tecla="q"):
        salir()
    case KeyPress(tecla=tecla):
        print(f"Tecla: {tecla}")
```
