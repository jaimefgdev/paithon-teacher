# paithon-teacher

**PyMentor**, un tutor de Python en español que responde con RAG (*retrieval-augmented generation*) sobre unos
apuntes propios (9 documentos, unos 260 000 caracteres) y **cita el apartado** en el que se apoya cada respuesta.

Nació como un Gem de Gemini. Esta versión es el mismo tutor convertido en una aplicación: recuperación
híbrida hecha a mano, evaluación medible, API, interfaz web y tests.

```
pregunta ──► BM25 (léxico) ──┐
         └─► embeddings ─────┴─► fusión RRF ─► 5 fragmentos ─► LLM (Claude o Gemini) ─► respuesta con [citas]
```

## Qué tiene de interesante

- **Troceo por estructura, no por tamaño.** Los apuntes tienen secciones y apartados; cada fragmento es un apartado
  con su ruta (`Fundamentos de Python › Estructuras de datos › Diccionarios`). Los apartados largos se parten por
  párrafos y, si el corte cae dentro de un bloque de código, se cierra y se reabre para que cada trozo siga siendo
  código válido.
- **Búsqueda híbrida.** BM25 implementado en Python puro, con normalización para español (acentos, palabras vacías,
  recorte de sufijos) que respeta identificadores de Python (`__init__`, `f-string`, y no descarta `with`, `is` o
  `for`, que en otro contexto serían palabras vacías). Los embeddings (`gemini-embedding-001`) cubren las preguntas
  dichas con otras palabras. Las dos listas se combinan con *Reciprocal Rank Fusion*.
- **Funciona sin claves.** Sin `GEMINI_API_KEY` la búsqueda es solo BM25; los embeddings se guardan en una caché
  SQLite, así que la base se vectoriza una vez. Las llamadas a la API reintentan solas ante cuota agotada (429) o
  saturación (503), esperando lo que pide la propia API: con el nivel gratuito (100 textos/minuto) la primera
  indexación tarda en torno a minuto y medio.
- **Citas verificables.** El modelo recibe los fragmentos numerados y debe citar `[n]`; la aplicación comprueba
  qué números existen y enseña el texto de cada fuente.
- **Evaluación.** `evals/preguntas.jsonl` tiene 78 preguntas de alumno con el apartado que debería recuperarse.
  `paithon evaluar` mide recall@k y MRR, y un test de CI impide que un cambio hunda la recuperación.
- **Sin dependencias en el núcleo.** Troceo, BM25, fusión y clientes HTTP usan solo la biblioteca estándar.
  FastAPI y el SDK de Anthropic son opcionales.

## Resultados de recuperación

78 preguntas de alumno; acierto = el apartado esperado aparece entre los 5 fragmentos recuperados. Las 40
últimas se escribieron al ampliar los apuntes y antes de medir, para no ajustar el texto a las preguntas.

| Modo | recall@5 | MRR |
|---|---|---|
| Solo BM25 | 88 % | 0,69 |
| Híbrido (BM25 + `gemini-embedding-001`, RRF) | **94 %** | **0,79** |

Los embeddings rescatan las preguntas dichas con otras palabras («repetir algo mientras el usuario no
acierte» → bucle `while`); BM25, las que nombran algo exacto (`isinstance`, `0.1 + 0.2`).

```
paithon evaluar --detalle            # lista las preguntas falladas
paithon evaluar --solo-bm25          # compara sin embeddings
```

## Uso

```bash
python -m venv .venv && . .venv/bin/activate     # en Windows: .venv\Scripts\activate
pip install -e ".[web,claude]"

export GEMINI_API_KEY=...       # embeddings (nivel gratuito) y, si no hay otra, generación
export ANTHROPIC_API_KEY=...    # opcional: genera con Claude

paithon buscar "¿por qué mi lista por defecto acumula valores?"   # solo recuperación, sin LLM
paithon preguntar "¿qué diferencia hay entre una lista y una tupla?"
paithon preguntar                                                # conversación
paithon web                                                      # http://127.0.0.1:8000
```

Con Docker:

```bash
docker build -t paithon .
docker run -p 8000:8000 -e GEMINI_API_KEY paithon
```

| Variable | Para qué |
|---|---|
| `GEMINI_API_KEY` | Embeddings y generación con Gemini |
| `ANTHROPIC_API_KEY` | Generación con Claude (tiene prioridad) |
| `PAITHON_MODELO` | Modelo de generación (por defecto `claude-sonnet-5-5` o `gemini-flash-latest`) |
| `PAITHON_CONOCIMIENTO` | Carpeta con los `.md` de la base de conocimiento |
| `PAITHON_CACHE` | Ruta de la caché de embeddings |

## Estructura

```
conocimiento/        base de conocimiento (Markdown) y prompt original del Gem
src/paithon/
  trocear.py         documentos -> fragmentos con ruta
  texto.py, bm25.py  búsqueda léxica
  embeddings.py      embeddings de Gemini + caché SQLite
  buscador.py        fusión RRF
  llm.py, tutor.py   generación con citas
  web.py, cli.py     interfaces
  evaluar.py         recall@k y MRR
evals/               preguntas de evaluación
gem/                 instrucciones y archivos para la versión Gem de Gemini
tests/               pytest, sin red (embedder y LLM falsos)
```

## Desarrollo

```bash
pip install -e ".[dev,web]"
pytest && ruff check . && mypy
```

## Licencia

MIT.
