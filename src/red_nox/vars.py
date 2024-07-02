from __future__ import annotations

import platform

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## Default paths to lint
DEFAULT_LINT_PATHS: list[str] = ["src", "tests"]

## Default logging message/date formats
DEFAULT_NOX_LOGGING_FMT: str = "[NOX] [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
DEFAULT_NOX_LOGGING_DATEFMT: str = "%Y-%m-%D %H:%M:%S"
DEFAULT_RED_NOX_LOGGING_FMT: str = "[RED-NOX] [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
DEFAULT_RED_NOX_LOGGING_DATEFMT: str = "%Y-%m-%D %H:%M:%S"