"""Top-level package for tp11."""

import os
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tp11")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+unknown"

BUILD = os.environ.get("TP11_BUILD", "dev")

__all__ = ["BUILD", "__version__"]
