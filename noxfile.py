from __future__ import annotations

import logging

log = logging.getLogger("red_nox")

import platform
import sys

import nox
import red_nox
from red_nox.vars import DEFAULT_PYTHON, PY_VER_TUPLE

## Set nox options
nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

CONTAINER_ENV: bool = red_nox.utils.detect_container_env()

red_nox.utils.setup_nox_logging()
