from __future__ import annotations

import logging

log = logging.getLogger("red_nox")


from . import sessions, utils
from .vars import (
    DEFAULT_LINT_PATHS,
    DEFAULT_NOX_LOGGING_DATEFMT,
    DEFAULT_NOX_LOGGING_FMT,
    DEFAULT_PYTHON,
    DEFAULT_RED_NOX_LOGGING_DATEFMT,
    DEFAULT_RED_NOX_LOGGING_FMT,
    PY_VER_TUPLE,
)
