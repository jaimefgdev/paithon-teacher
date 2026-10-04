# Versión Gem de Gemini

El mismo tutor sin servidor: un Gem de Gemini con instrucciones y archivos de conocimiento.

## Montarlo

1. En gemini.google.com, abre **Gems › PyMentor › Editar** (o crea uno nuevo).
2. **Instrucciones:** pega el contenido de [`instrucciones.md`](instrucciones.md).
3. **Conocimiento:** sube estos cuatro archivos de [`../conocimiento`](../conocimiento):
   - `02_kb_fundamentos_python.md`
   - `03_kb_intermedio_avanzado.md`
   - `04_kb_ecosistema_python.md`
   - `05_kb_ejercicios_recursos.md`
4. Guarda.

## Diferencias con el prompt original

`conocimiento/01_system_prompt_python_teacher.txt` es el prompt original. `instrucciones.md` cambia:

- **Ficha del alumno.** Un Gem no recuerda nada entre conversaciones. El original hablaba de un «registro
  mental» que se perdía; ahora el tutor genera una ficha que el alumno guarda y pega al volver.
- **Uso explícito de los archivos.** Las instrucciones dicen qué cubre cada archivo, piden basar las
  explicaciones en ellos y citar el apartado, y tirar del banco de ejercicios y de los errores frecuentes.
- **Código comprobado.** Nada de salidas inventadas: se ejecuta si hay herramienta y, si no, se razona.
- **Menos duplicación.** Las listas de recursos ya están en el archivo 05; repetirlas en las instrucciones
  solo añadía ruido.
- **Ejercicios comprobables** (con un ejemplo de entrada y salida), **ayuda en tres escalones** y **uv** para
  quien ya no es principiante.

La aplicación RAG de este repositorio usa los mismos apuntes, pero la recuperación es propia (BM25 +
embeddings) y medible con `paithon evaluar`; en el Gem, la recuperación la hace Gemini y no se puede medir.
