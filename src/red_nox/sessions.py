from __future__ import annotations

import logging
from pathlib import Path
import platform

import nox

log = logging.getLogger("red_nox")

from .utils import detect_container_env
from .vars import DEFAULT_LINT_PATHS, DEFAULT_PYTHON, PY_VER_TUPLE

CONTAINER_ENV: bool = detect_container_env()


@nox.session(name="print-python", tags=["ext", "debug"])
def debug_python_ver(session: nox.Session):
    """Nox session to debug-print Python version information detected from the session."""
    log.info("Printing Python platform info")
    print("")

    print(f"Default Python version: {DEFAULT_PYTHON}")
    print(f"Python version tuple: {PY_VER_TUPLE}")


@nox.session(name="debug-env", tags=["ext", "debug"])
def debug_environment(session: nox.Session):
    """Nox session to debug platform information detected from the session."""
    log.info("Printing platform info")

    _uname = platform.uname()
    _system = platform.system()
    _node = platform.node()
    _release = platform.release()
    _version = platform.version()
    _machine = platform.machine()
    _processor = platform.processor()
    _architecture = platform.architecture()
    _platform = platform.platform()
    _py_build = platform.python_build()
    _py_compiler = platform.python_compiler()
    _py_impl = platform.python_implementation()
    _py_version = platform.python_version()

    print("")

    print("[HOST]")
    print(f"Uname: {_uname}")
    print(f"System: {_system}")
    print(f"Node: {_node}")
    print(f"OS Release: {_release}")
    print(f"OS Version: {_version}")

    print("")

    print("[Machine]")
    print(f"Machine: {_machine}")
    print(f"Processor: {_processor}")
    print(f"Architecture: {_architecture}")
    print(f"Platform: {_platform}")

    print("")

    print("[Python]")
    print(f"Python build: {_py_build}")
    print(f"Python compiler: {_py_compiler}")
    print(f"Python implementation: {_py_impl}")
    print(f"Python version: {_py_version}")


@nox.session(python=[DEFAULT_PYTHON], name="ruff-lint", tags=["ext", "clean", "lint"])
def run_linter(session: nox.Session, lint_paths: list[str] = DEFAULT_LINT_PATHS):
    """Nox session to run Ruff code linting."""
    session.install("ruff")

    if not Path("ruff.toml").exists():
        log.error(FileNotFoundError("Could not find ruff.toml"))

        return

    log.info("Linting code")
    for d in lint_paths:
        if not Path(d).exists():
            log.warning(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            log.info(f"Running ruff imports sort on '{d}'")
            session.run(
                "ruff",
                "check",
                lint_path,
                "--select",
                "I",
                "--fix",
            )

            log.info(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "check",
                lint_path,
                "--fix",
            )

    log.info("Linting noxfile.py")
    session.run(
        "ruff",
        "check",
        f"{Path('./noxfile.py')}",
        "--fix",
    )
