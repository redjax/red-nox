from __future__ import annotations

import logging

log = logging.getLogger("red_nox")
log.setLevel("DEBUG")

import platform
import sys

from red_nox.utils import setup_nox_logging

setup_nox_logging()

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
