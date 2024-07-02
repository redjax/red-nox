from __future__ import annotations

import logging

log = logging.getLogger("red_nox.sessions.debug")

import platform
import sys

from red_nox.utils import detect_container_env
from red_nox.vars import DEFAULT_PYTHON, PY_VER_TUPLE

import nox

def _return_host_msg(include_header: bool = False, header: str = "[HOST]") -> str:
    _container_env: bool = detect_container_env()
    _uname: platform.uname_result = platform.uname()

    HOST_MSG: str = f"""Container environment: {_container_env}
Node: {_uname.node}
System: {_uname.system}
OS Release: {_uname.release}
OS Version: {_uname.version}
CPU Architecture: {_uname.machine}"""

    if include_header:
        HOST_MSG = f"""{header}\n{HOST_MSG}"""

    return HOST_MSG


def _return_cpu_msg(include_header: bool = False, header: str = "[CPU]") -> str:
    _machine: str = platform.machine()
    _processor: str = platform.processor()
    _architecture: tuple[str, str] = platform.architecture()
    _platform: str = platform.platform()

    CPU_MSG: str = f"""Machine: {_machine}
Processor: {_processor if _processor else '<Could not read processor info>'}
CPU Architecture: {_architecture[0]}
Platform: {_platform}"""

    if include_header:
        CPU_MSG = f"""{header}\n{CPU_MSG}"""

    return CPU_MSG


def _return_python_msg(include_header: bool = False, header: str = "[PYTHON]") -> str:
    _py_build: tuple[str, str] = platform.python_build()
    _py_compiler: str = platform.python_compiler()
    _py_impl: str = platform.python_implementation()
    _py_version: str = platform.python_version()
    _py_executable: str = sys.executable

    PYTHON_MSG: str = f"""Python build: {_py_build}
Python compiler: {_py_compiler}
Python implementation: {_py_impl}
Python version: {_py_version}
Python bin: {_py_executable}"""

    if include_header:
        PYTHON_MSG = f"""{header}\n{PYTHON_MSG}"""

    return PYTHON_MSG


def _return_debug_string(include_headers: bool = True) -> str:
    _host_msg: str = _return_host_msg(include_header=include_headers)
    _cpu_msg: str = _return_cpu_msg(include_header=include_headers)
    _python_msg: str = _return_python_msg(include_header=include_headers)

    DEBUG_MSG: str = f"""
+ Debug environment Nox is running in

{_host_msg}

{_cpu_msg}

{_python_msg}
"""

    return DEBUG_MSG


@nox.session(name="debug-python", tags=["ext", "debug"])
def debug_python_ver(session: nox.Session) -> None:
    """Nox session to debug-print Python version information detected from the session."""
    log.info("Printing Python platform info")

    msg: str = _return_python_msg(include_headers=True)

    print(f"\n{msg}\n")


@nox.session(name="debug-host", tags=["ext", "debug"])
def debug_python_ver(session: nox.Session) -> None:
    """Nox session to debug-print host environment information detected from the session."""
    log.info("Printing Python platform info")

    msg: str = _return_host_msg(include_header=True)

    print(f"\n{msg}\n")


@nox.session(name="debug-cpu", tags=["ext", "debug"])
def debug_python_ver(session: nox.Session) -> None:
    """Nox session to debug-print CPU information detected from the session."""
    log.info("Printing Python platform info")

    msg: str = _return_cpu_msg(include_header=True)

    print(f"\n{msg}\n")


@nox.session(name="debug-env", tags=["ext", "debug"])
def debug_environment(session: nox.Session):
    """Nox session to debug platform information detected from the session."""
    log.info(msg="Printing platform info")

    msg: str = _return_debug_string(include_headers=True)
    print(msg)
