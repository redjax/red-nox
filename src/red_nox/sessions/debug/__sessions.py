from __future__ import annotations

import logging

log = logging.getLogger("red_nox.sessions.debug")

import platform

from red_nox.vars import DEFAULT_PYTHON, PY_VER_TUPLE

import nox

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
