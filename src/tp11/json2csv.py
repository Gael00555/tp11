"""Convierte datos JSON a CSV con una estrategia de filtro.

Uso::

    python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}

Si no se indica ``-i`` la entrada se lee de la entrada estándar; si no se
indica ``-o`` el resultado se emite por la salida estándar. El delimitador
por defecto es la coma.

Formatos de entrada admitidos:

* Una lista de objetos JSON: cada objeto es una fila.
* Un único objeto JSON: genera una sola fila.

Los objetos anidados se aplanan con claves separadas por punto
(``{"a": {"b": 1}}`` produce la columna ``a.b``). Las listas se escriben
como texto JSON dentro de la celda.

Con ``--version`` muestra la versión y el número de build.

Códigos de salida: 0 correcto, 1 error de ejecución, 2 argumentos inválidos.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections.abc import Sequence
from typing import Any

from tp11 import BUILD, __version__

EXIT_OK = 0
EXIT_ERROR = 1
DEFAULT_DELIMITER = ","
_FORBIDDEN_DELIMITERS = {'"', "\n", "\r"}


class Json2CsvError(Exception):
    """Error controlado de la conversión, apto para mostrar al usuario."""


def parse_delimiter(value: str) -> str:
    """Valida y normaliza el delimitador indicado con ``-d``.

    Acepta la secuencia barra invertida seguida de t como atajo del tabulador.

    Args:
        value: texto recibido en la línea de comandos.

    Returns:
        Un único carácter apto como delimitador CSV.

    Raises:
        argparse.ArgumentTypeError: si no es un único carácter válido.
    """
    if value == "\\t":
        value = "\t"
    if len(value) != 1:
        raise argparse.ArgumentTypeError(
            "el delimitador debe ser exactamente un carácter"
        )
    if value in _FORBIDDEN_DELIMITERS:
        raise argparse.ArgumentTypeError(
            "el delimitador no puede ser comilla doble ni salto de línea"
        )
    return value


def build_parser() -> argparse.ArgumentParser:
    """Construye el analizador de argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="json2csv.py",
        description="Convierte JSON a CSV (filtro: stdin -> stdout).",
    )
    parser.add_argument(
        "-i",
        "--input",
        metavar="input.txt",
        help="archivo JSON de entrada (por defecto, entrada estándar)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="output.txt",
        help="archivo CSV de salida (por defecto, salida estándar)",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        type=parse_delimiter,
        default=DEFAULT_DELIMITER,
        metavar="delimitador",
        help="delimitador de columnas (por defecto, coma)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__} (build {BUILD})",
    )
    return parser


def read_text(path: str | None) -> str:
    """Lee el texto de entrada desde un archivo o desde stdin.

    Args:
        path: ruta del archivo, o ``None`` para usar la entrada estándar.

    Raises:
        Json2CsvError: si el archivo no existe, no se puede leer o no es
            texto UTF-8 válido.
    """
    try:
        if path is None:
            return sys.stdin.read()
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        raise Json2CsvError(f"no existe el archivo de entrada: {path}") from None
    except IsADirectoryError:
        raise Json2CsvError(f"la entrada es un directorio: {path}") from None
    except PermissionError:
        raise Json2CsvError(f"sin permiso para leer: {path}") from None
    except UnicodeDecodeError:
        raise Json2CsvError("la entrada no es texto UTF-8 válido") from None
    except OSError as error:
        raise Json2CsvError(f"error leyendo la entrada: {error}") from None


def parse_json(text: str) -> list[dict[str, Any]]:
    """Interpreta el texto JSON y lo normaliza a una lista de objetos.

    Raises:
        Json2CsvError: si el JSON es inválido o su estructura no es una
            lista de objetos ni un objeto único.
    """
    if not text.strip():
        raise Json2CsvError("la entrada está vacía")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise Json2CsvError(
            f"JSON inválido (línea {error.lineno}, columna {error.colno}): {error.msg}"
        ) from None
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        for position, item in enumerate(data):
            if not isinstance(item, dict):
                raise Json2CsvError(
                    f"el elemento {position} de la lista no es un objeto JSON"
                )
        return data
    raise Json2CsvError("el JSON debe ser un objeto o una lista de objetos")


def _format_value(value: Any) -> str:
    """Convierte un valor JSON escalar o lista a texto de celda."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def flatten(record: dict[str, Any], prefix: str = "") -> dict[str, str]:
    """Aplana un objeto anidado usando claves con punto como separador."""
    flat: dict[str, str] = {}
    for key, value in record.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict) and value:
            flat.update(flatten(value, prefix=f"{name}."))
        else:
            flat[name] = _format_value(value)
    return flat


def to_csv(records: list[dict[str, Any]], delimiter: str) -> str:
    """Genera el texto CSV (con encabezado) para una lista de objetos.

    El encabezado es la unión de las claves en orden de primera aparición;
    las celdas faltantes quedan vacías.
    """
    rows = [flatten(record) for record in records]
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    if not columns:
        return ""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=columns,
        delimiter=delimiter,
        restval="",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def write_text(path: str | None, text: str) -> None:
    """Escribe el resultado en un archivo o en la salida estándar.

    Raises:
        Json2CsvError: si no se puede escribir el archivo de salida.
    """
    try:
        if path is None:
            sys.stdout.write(text)
            sys.stdout.flush()
            return
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except IsADirectoryError:
        raise Json2CsvError(f"la salida es un directorio: {path}") from None
    except PermissionError:
        raise Json2CsvError(f"sin permiso para escribir: {path}") from None
    except OSError as error:
        raise Json2CsvError(f"error escribiendo la salida: {error}") from None


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada del programa.

    Convierte primero y escribe después, de modo que un error de conversión
    nunca deja un archivo de salida vacío o a medias.

    Returns:
        Código de salida del proceso.
    """
    args = build_parser().parse_args(argv)
    try:
        text = read_text(args.input)
        records = parse_json(text)
        result = to_csv(records, args.delimiter)
        write_text(args.output, result)
    except Json2CsvError as error:
        print(f"json2csv: error: {error}", file=sys.stderr)
        return EXIT_ERROR
    except BrokenPipeError:
        return EXIT_OK
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
