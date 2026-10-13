# CONTEXT.md

Registro de las herramientas de IA utilizadas en este proyecto y de los
prompts empleados, según lo requerido por la consigna del TP11
(Ingeniería de Software II, FCyT-UADER).

## Herramienta de IA utilizada

| Dato | Valor |
|---|---|
| Asistente | Claude (Anthropic), interfaz de chat web/móvil |
| Modelo | Claude Sonnet 5.5 |
| Fecha de uso | 2026-10-12 |
| Uso declarado | Generación del código de `json2csv.py`, guía paso a paso para armar el proyecto |

## Criterio de uso

- El código generado por la IA fue **revisado y verificado** por el autor
  antes de incorporarlo al repositorio.
- La IA indicó explícitamente que no pudo ejecutar ruff, black, mypy,
  pyright, bandit ni pytest en su entorno; esos controles se validan en la
  máquina del autor y en el workflow de CI.
- Los resultados de la IA no se aceptan sin contraste con la consigna.

## Registro de prompts

### Prompt 1: desarrollo de la herramienta

**Propósito:** generar `json2csv.py`.

**Prompt (texto de la consigna):**

> Desarrolle una herramienta en lenguaje Python para convertir archivos de
> formato JSON a formato CSV. El programa deberá implementarse con una
> estrategia de filtro. El formato de ejecución será:
> `python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}`
> Si no se informa el argumento "-i" el programa podrá aceptar el archivo de
> entrada mediante entrada estándar, al mismo tiempo si no se informa el
> argumento "-o" se emitirá el texto resultante mediante salida estándar. Se
> utilizará la coma como delimitador, excepto que se indique uno distinto con
> el argumento "-d".

**Resultado:** archivo `json2csv.py` (lectura desde archivo o stdin, escritura
a archivo o stdout, delimitador configurable, aplanado de objetos anidados,
manejo de errores con códigos de salida).

**Verificación realizada:** pruebas manuales en línea de comandos (entrada por
stdin y por archivo, delimitadores `;` y tabulador, objeto único, JSON
inválido, entrada vacía, archivo inexistente, salida a directorio, UTF-8
inválido, cierre de tubería).

### Prompt 2: guía de implementación por pasos

**Propósito:** recibir una guía ordenada para cumplir los puntos a, b, c, etc.
de la consigna del proyecto.

**Prompt:**

> vaamos por orden, a,b,c,etc

**Resultado:** pasos para el entorno virtual (a) y el esqueleto con
CookieCutter (b).

### Prompt 3 y 4: confirmación de avance

> listo el venv

> listo se creo el repo

**Resultado:** continuación con el paso b (CookieCutter) y el paso c
(este archivo).

## Cómo mantener este archivo

Cada vez que se use IA para una tarea nueva del proyecto (tests con pytest,
workflow de GitHub Actions, documentación, etc.), agregar una entrada con:
propósito, prompt, resultado y verificación realizada.
