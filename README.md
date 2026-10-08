# PyMentor

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
  `for`) y conserva los operadores (`:=`, `**`, `//`, `>>`, `&`). Los embeddings cubren las preguntas dichas con
  otras palabras. Las dos listas se combinan con *Reciprocal Rank Fusion* (k = 10, 50 candidatos por lista).
- **Embeddings en el propio ordenador.** Por defecto, `multilingual-e5-large` con fastembed (ONNX, sin PyTorch, sin
  clave ni cuota; `pip install -e ".[local]"`). Rinde igual que `gemini-embedding-001` en estas pruebas, que en el
  nivel gratuito solo permite 1000 textos al día. `PAITHON_EMBEDDINGS=gemini` vuelve a Gemini.
- **Preguntas de ejemplo por apartado (doc2query).** `paithon generar-preguntas` pide a Gemini, una vez, preguntas
  de alumno que responde cada fragmento: la mitad como las haría alguien que no conoce el nombre técnico («hacer
  una lista en una sola línea»), la otra mitad con el término exacto. Hay entre 10 y 18 por fragmento (dos tandas
  de instrucciones combinadas) en `conocimiento/preguntas_generadas.json`, con la huella del fragmento: si un
  apartado cambia, solo se regeneran las suyas. Se indexan con BM25 y cada una con su propio vector (cuenta el
  parecido más alto): una pregunta corta se parece más a otra pregunta corta que a un apartado largo. El generador
  nunca ve las preguntas de evaluación.
- **Funciona sin claves ni red.** Con el modelo local, la búsqueda no necesita ninguna API; solo la respuesta usa
  un LLM. Si un servicio no responde, se sigue con lo que haya (BM25 o los vectores ya guardados) en vez de
  fallar, y la web avisa con un mensaje claro.
- **Citas verificables.** El modelo recibe los fragmentos numerados y debe citar `[n]`; la aplicación comprueba
  qué números existen y enseña el texto de cada fuente.
- **Evaluación.** `evals/preguntas.jsonl` tiene 78 preguntas de alumno con el apartado que debería recuperarse.
  `paithon evaluar` mide recall@k y MRR, y un test de CI impide que un cambio hunda la recuperación.
- **Sin dependencias en el núcleo.** Troceo, BM25, fusión y clientes HTTP usan solo la biblioteca estándar.
  FastAPI y el SDK de Anthropic son opcionales.

## Resultados de recuperación

Acierto = el apartado que responde aparece entre los 5 fragmentos recuperados (recall@5). Dos conjuntos:

- `evals/preguntas.jsonl`: 78 preguntas de alumno escritas por nosotros (las 40 últimas, al ampliar los apuntes y
  antes de medir).
- `evals/preguntas_stackoverflow.jsonl`: 95 títulos de las preguntas sobre Python más votadas de
  [Stack Overflow en español](https://es.stackoverflow.com), con el enlace a cada una (contenido CC BY-SA 4.0),
  elegidas entre las de Python general. Para no ajustar la búsqueda a las preguntas, se partieron en dos mitades
  por el número de pregunta: con la mitad par se probaron las mejoras y la impar se reservó hasta el final.

| Conjunto | Solo BM25 | Híbrido (BM25 + e5-large) |
|---|---|---|
| Propias (78) | 95 % | **99 %** (MRR 0,86) |
| Stack Overflow, todas (95) | 80 % | **91 %** (MRR 0,73) |
| Stack Overflow, mitad reservada (49) | 78 % | **90 %** (MRR 0,75) |

La mitad reservada dio un 84 % en la primera medida; al revisar los fallos, en tres de ellos lo recuperado
respondía la pregunta (por ejemplo, «Estructuras de datos › Listas» con `numeros.sort()` para «¿Cómo ordeno los
elementos de una lista numéricamente?») y la etiqueta solo admitía otro apartado; con la etiqueta corregida, 90 %.
Antes de estos cambios, las 95 preguntas de Stack Overflow daban un 81 %. Tres de las elegidas al principio no
tenían respuesta en los apuntes (el «shebang», un error propio de Python 2 y la concatenación implícita de
literales); se añadieron y no cuentan en la evaluación.

```
paithon evaluar --preguntas evals/preguntas_stackoverflow.jsonl --detalle
```

Los embeddings rescatan las preguntas dichas con otras palabras («repetir algo mientras el usuario no
acierte» → bucle `while`); BM25, las que nombran algo exacto (`isinstance`, `0.1 + 0.2`).

```
paithon evaluar --detalle            # lista las preguntas falladas
paithon evaluar --solo-bm25          # compara sin embeddings
```

## Uso

```bash
python -m venv .venv && . .venv/bin/activate     # en Windows: .venv\Scripts\activate
pip install -e ".[web,claude,local]"   # local: embeddings en este ordenador (descarga e5-large, 2,2 GB)

export GEMINI_API_KEY=...       # generación con Gemini (y embeddings si no se instala [local])
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
| `PAITHON_MODELO` | Modelo de generación (por defecto `claude-sonnet-5-5` o `gemini-flash-latest`; con Gemini, si el modelo no responde o agota su cuota, se usa `gemini-flash-lite-latest`) |
| `PAITHON_CONOCIMIENTO` | Carpeta con los `.md` de la base de conocimiento |
| `PAITHON_CACHE` | Ruta de la caché de embeddings |
| `PAITHON_EMBEDDINGS` | `local:<modelo>` o `gemini` (por defecto, el modelo local si está instalado fastembed) |
| `PAITHON_REORDENAR` | `local:<modelo>`: reordenador cross-encoder opcional (en las pruebas no mejoró los resultados) |

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
