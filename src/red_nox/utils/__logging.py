from __future__ import annotations

import logging
import logging.config

from red_nox.vars import (
    DEFAULT_NOX_LOGGING_DATEFMT,
    DEFAULT_NOX_LOGGING_FMT,
    DEFAULT_RED_NOX_LOGGING_DATEFMT,
    DEFAULT_RED_NOX_LOGGING_FMT,
)

from .__methods import detect_container_env

CONTAINER_ENV: bool = detect_container_env()


def setup_nox_logging(
    level_name: str = "DEBUG",
    nox_level_name: str = None,
    nox_fmt: str = DEFAULT_NOX_LOGGING_FMT,
    nox_datefmt: str = DEFAULT_NOX_LOGGING_DATEFMT,
    red_nox_fmt: str = DEFAULT_RED_NOX_LOGGING_FMT,
    red_nox_datefmt: str = DEFAULT_RED_NOX_LOGGING_DATEFMT,
    disable_loggers: list[str] | None = [],
    container_env: bool = CONTAINER_ENV,
) -> None:
    """Configure a logger for the Nox module.

    Params:
        level_name (str): The uppercase string repesenting a logging logLevel.
        disable_loggers (list[str] | None): A list of logger names to disable, i.e. for 3rd party apps.
            Note: Disabling means setting the logLevel to `WARNING`, so you can still see errors.

    """
    ## If container environment detected, default to logging.DEBUG
    if container_env:
        level_name: str = "DEBUG"
        nox_level_name: str = "DEBUG"
    else:
        if nox_level_name is None:
            nox_level_name: str = "WARNING"

    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "nox": {
                "level": nox_level_name,
                "handlers": ["console"],
                "propagate": False,
            },
            "red_nox": {
                "level": level_name.upper(),
                "handlers": ["red_nox_console"],
                "propagate": False,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "nox",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            },
            "red_nox_console": {
                "class": "logging.StreamHandler",
                "formatter": "red_nox",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            },
        },
        "formatters": {
            "nox": {
                "format": nox_fmt,
                "datefmt": nox_datefmt,
            },
            "red_nox": {
                "format": red_nox_fmt,
                "datefmt": red_nox_datefmt,
            },
        },
    }

    ## Configure logging. Only run this once in an application
    logging.config.dictConfig(config=logging_config)

    ## Disable loggers by name. Sets logLevel to logging.WARNING to suppress all but warnings & errors
    for _logger in disable_loggers:
        logging.getLogger(_logger).setLevel(logging.WARNING)
