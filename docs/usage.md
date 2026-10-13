# Uso

`json2csv` convierte JSON a CSV como un filtro: lee de un archivo o de la
entrada estándar y escribe en un archivo o en la salida estándar.

```bash
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

| Argumento | Descripción | Por defecto |
|---|---|---|
| `-i`, `--input` | Archivo JSON de entrada | Entrada estándar |
| `-o`, `--output` | Archivo CSV de salida | Salida estándar |
| `-d`, `--delimiter` | Delimitador de columnas (un carácter) | Coma |
| `--version` | Muestra la versión y el número de build | |

## Ejemplo

Entrada:

```json
[{"id": 1, "nombre": "Ana", "dir": {"ciudad": "CdU"}}, {"id": 2, "nombre": "Luis"}]
```

Salida:

```
id,nombre,dir.ciudad
1,Ana,CdU
2,Luis,
```

## Códigos de salida

- `0`: conversión correcta.
- `1`: error de ejecución (archivo inexistente, JSON inválido, entrada vacía,
  estructura no soportada, error de escritura).
- `2`: argumentos inválidos.

## Uso como biblioteca

```python
from tp11.json2csv import parse_json, to_csv

registros = parse_json('[{"a": 1, "b": {"c": 2}}]')
print(to_csv(registros, ","))
```