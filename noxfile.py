from __future__ import annotations

import logging
from pathlib import Path
import platform
import shutil
import sys

log = logging.getLogger("red_nox")
log.setLevel("DEBUG")

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

## Define available Python versions
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Set PDM version to use within nox
PDM_VER: str = "2.15.4"

## Set directory where requirements files will be exported to
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")


@nox.session(python=PY_VERSIONS, name="setup", tags=["setup", "init"])
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_session(session: nox.Session, pdm_ver: str):
    log.info("Running initial setup")

    session.install("-r", "requirements/requirements.dev.txt")


@nox.session(python=PY_VERSIONS, name="build-env")
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str) -> None:
    log.debug(f"Default Python: {DEFAULT_PYTHON}")
    session.install(f"pdm>={pdm_ver}")

    log.info("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"
## Set PDM version to install throughout
PDM_VER: str = "2.15.4"

## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")

## List of dicts with a source & destination, for creating copies of files.
#  TODO: Use templates
INIT_COPY_FILES: list[dict[str, str]] = [
    {"src": "config/.secrets.example.toml", "dest": "config/.secrets.toml"},
    {"src": "config/settings.toml", "dest": "config/settings.local.toml"},
]


@nox.session(python=[PY_VERSIONS], name="pipeline-setup")
def setup_pipeline(session: nox.Session):
    session.install("-r", "requirements/requirements.dev.txt")


@nox.session(python=[PY_VERSIONS], name="init-setup")
def run_initial_setup(session: nox.Session):
    log.info(f"Running initial setup.")
    if INIT_COPY_FILES is None:
        log.warning(f"INIT_COPY_FILES is empty. Skipping")
        pass

    else:
        for pair_dict in INIT_COPY_FILES:
            src = Path(pair_dict["src"])
            dest = Path(pair_dict["dest"])
            if not dest.exists():
                log.info(f"Copying {src} to {dest}")
                try:
                    shutil.copy(src, dest)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception copying file from '{src}' to '{dest}'. Details: {exc}"
                    )
                    log.error(msg)


@nox.session(python=[PY_VERSIONS], name="pip-export")
def pip_freeze(session: nox.Session):
    log.info("Freezing pip requirements to requirements.txt")
    session.run("pip", "freeze", ">", "requirements.txt")


@nox.session(python=[DEFAULT_PYTHON], name="pdm-export")
@nox.parametrize("pdm_ver", [PDM_VER])
@nox.parametrize("requirements_output_dir", REQUIREMENTS_OUTPUT_DIR)
def export_requirements(
    session: nox.Session, pdm_ver: str, requirements_output_dir: Path
):
    ## Ensure REQUIREMENTS_OUTPUT_DIR path exists
    if not requirements_output_dir.exists():
        try:
            requirements_output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(
                f"Unable to create requirements export directory: '{requirements_output_dir}'. Details: {exc}"
            )
            log.error(msg)

            requirements_output_dir: Path = Path("./")

    session.install(f"pdm>={pdm_ver}")

    log.info("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
    )

    log.info("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
    )
