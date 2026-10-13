## [Unreleased]

### Added

- Esqueleto inicial generado con CookieCutter (`cookiecutter-pypackage`).
- `json2csv`: conversor de JSON a CSV con estrategia de filtro (`-i`, `-o`, `-d`),
  aplanado de objetos anidados y manejo de errores con códigos de salida.
- Opción `--version` con VERSION (desde `pyproject.toml`) y BUILD (`TP11_BUILD`).
- Tests con pytest (38 casos, cobertura total 86,56 %, mínimo 85 %).
- Configuración de calidad: black, ruff (PEP 8 y PEP 257), mypy y pyright en
  modo estricto/estándar, y bandit sin observaciones.
- Workflow de CI/CD: calidad estática, tests en Python 3.12 y 3.13, documentación
  con pdoc como artefacto y empaquetado con prueba de humo.
- `requirements.txt`, `CONTEXT.md`, `VERSION.md` y `docs/usage.md`.

### Changed

- `README.md` reescrito para describir el conversor.
- Largo de línea de ruff pasado de 120 a 88 para coincidir con black.
- Cobertura mínima de 50 % a 85 %.

### Removed

- Insignias y comandos de PyPI del README original.
- `ty` y `ruff format` del workflow de CI (se usan mypy, pyright y black).