# tp11 — json2csv

Conversor de JSON a CSV implementado como **filtro**: lee de un archivo o de
la entrada estándar y escribe en un archivo o en la salida estándar.

* [GitHub](https://github.com/Gael00555/tp11/) | [Documentación](https://Gael00555.github.io/tp11/)
* Autor: Gael Gabriel Guiffrey
* Licencia MIT

Proyecto del TP11 de Ingeniería de Software II (FCyT-UADER).

## Características

* Estrategia de filtro: sin argumentos funciona como `stdin -> stdout`.
* Entrada: una lista de objetos JSON (una fila por objeto) o un único objeto.
* Los objetos anidados se aplanan con punto (`{"dir": {"ciudad": "X"}}`
  genera la columna `dir.ciudad`).
* Las listas se escriben como texto JSON dentro de la celda.
* El encabezado es la unión de las claves, en orden de primera aparición;
  las celdas faltantes quedan vacías.
* Escapado correcto de comas, comillas y saltos de línea en los valores.
* Delimitador configurable (coma por defecto; `\t` equivale a tabulador).
* Errores controlados con mensaje claro y código de salida, sin trazas.
* Un error de conversión nunca deja un archivo de salida vacío o a medias.

## Instalación

Requiere Python 3.12 o superior.

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux/macOS:           source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Uso

```bash
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

| Argumento | Descripción | Por defecto |
|---|---|---|
| `-i`, `--input` | Archivo JSON de entrada | Entrada estándar |
| `-o`, `--output` | Archivo CSV de salida | Salida estándar |
| `-d`, `--delimiter` | Delimitador de columnas (un carácter) | `,` |

### Ejemplos

Entrada `datos.json`:

```json
[{"id": 1, "nombre": "Ana", "dir": {"ciudad": "CdU"}},
 {"id": 2, "nombre": "Luis"}]
```

Desde archivo a archivo:

```bash
python json2csv.py -i datos.json -o datos.csv
```

Resultado en `datos.csv`:

```
id,nombre,dir.ciudad
1,Ana,CdU
2,Luis,
```

Como filtro en una tubería:

```bash
cat datos.json | python json2csv.py > datos.csv
```

Con punto y coma como delimitador:

```bash
python json2csv.py -i datos.json -d ";"
```

> En Windows PowerShell 5.1, canalizar texto con `|` puede alterar los
> caracteres no ASCII. Para datos con tildes o eñes, usar `-i archivo`.

### Códigos de salida

| Código | Significado |
|---|---|
| 0 | Conversión correcta |
| 1 | Error de ejecución (archivo inexistente, JSON inválido, entrada vacía, estructura no soportada, error de escritura) |
| 2 | Argumentos inválidos (por ejemplo, delimitador de más de un carácter) |

## Desarrollo

El proyecto usa [uv](https://docs.astral.sh/uv/) y
[just](https://github.com/casey/just) para las tareas de desarrollo:

```bash
just check    # formato, lint (ruff), tipos (ty) y tests (pytest)
just fix      # aplica formato y correcciones automáticas
just coverage # tests con cobertura
```

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el detalle de instalación,
pruebas y documentación.

> Los controles adicionales requeridos por el TP (black, mypy, pyright,
> bandit, cobertura mínima del 85 %) se incorporan al flujo de integración
> continua en pasos posteriores y esta sección se actualizará con ellos.

## Registro de cambios

Ver la carpeta `CHANGELOG/` (cambios pendientes en
[`CHANGELOG/unreleased.md`](CHANGELOG/unreleased.md)).

## Uso de IA

Los prompts utilizados con herramientas de IA están documentados en
[CONTEXT.md](CONTEXT.md).

## Licencia

MIT. Ver [LICENSE](LICENSE).

Creado con [Cookiecutter](https://github.com/cookiecutter/cookiecutter) y la
plantilla [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage).