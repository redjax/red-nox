from __future__ import annotations

import logging

log = logging.getLogger("red_nox.sessions.pre_commit")

from red_nox.utils import check_path_exists
from red_nox.vars import DEFAULT_PYTHON, PY_VER_TUPLE

import nox

@nox.session(python=[DEFAULT_PYTHON], name="pre-commit-all", tags=["ext", "ci"])
def run_pre_commit_all(session: nox.Session):
    if not check_path_exists(p=".pre-commit-config.yaml"):
        return

    session.install("pre-commit")
    session.run("pre-commit")

    log.info("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=[DEFAULT_PYTHON], name="pre-commit-update", tags=["ext", "update"])
def run_pre_commit_autoupdate(session: nox.Session):
    if not check_path_exists(p=".pre-commit-config.yaml"):
        return

    session.install(f"pre-commit")

    log.info("Running pre-commit autoupdate")
    session.run("pre-commit", "autoupdate")


@nox.session(
    python=[DEFAULT_PYTHON], name="pre-commit-nbstripout", tags=["ext", "fix", "style"]
)
def run_pre_commit_nbstripout(session: nox.Session):
    if not check_path_exists(p=".pre-commit-config.yaml"):
        return

    session.install(f"pre-commit")

    log.info("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")
