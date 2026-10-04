# Versión Gem de Gemini

El mismo tutor sin servidor: un Gem de Gemini con instrucciones y archivos de conocimiento.

## Montarlo

1. En gemini.google.com, abre **Gems › pAIthon Teacher › Editar** (o crea uno nuevo).
2. **Instrucciones:** pega el contenido de [`instrucciones.md`](instrucciones.md) (sustituye todo el texto).
3. **Conocimiento:** sube estos cuatro archivos de [`../conocimiento`](../conocimiento):
   - `02_kb_fundamentos_python.md`
   - `03_kb_intermedio_avanzado.md`
   - `04_kb_ecosistema_python.md`
   - `05_kb_ejercicios_recursos.md`
4. Guarda.

## Diferencias con la versión anterior

`instrucciones_gem_anterior.txt` es el texto que tenía el Gem antes de este cambio. `instrucciones.md` lo conserva
entero y solo añade o corrige:

- **Archivos de conocimiento.** El Gem no tenía ninguno subido. Hay una sección nueva, «Tus apuntes», que dice
  qué cubre cada archivo y pide basar las explicaciones en ellos, citar el apartado y sacar de ellos los
  ejercicios y los errores frecuentes.
- **Ficha del alumno.** Un Gem no recuerda nada entre conversaciones. Antes solo se sugería «apuntar notas»;
  ahora el tutor genera una ficha con formato fijo, y al volver basta con pegarla para seguir donde se dejó.
- **Código comprobado.** Antes de decir qué imprime algo, se ejecuta si hay herramienta y, si no, se razona;
  nunca se inventan salidas ni mensajes de error.
- **Erratas.** «pAlthon» (con ele) pasa a ser «pAIthon», y se quita «un profesor que recuerda», que contradecía
  la falta de memoria.

`conocimiento/01_system_prompt_python_teacher.txt` es una versión aún más antigua del prompt.

La aplicación RAG de este repositorio usa los mismos apuntes, pero la recuperación es propia (BM25 +
embeddings) y medible con `paithon evaluar`; en el Gem, la recuperación la hace Gemini y no se puede medir.
