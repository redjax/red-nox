from __future__ import annotations

import logging

log = logging.getLogger("red_nox.sessions.git")

from red_nox.vars import DEFAULT_PYTHON

import nox

@nox.session(python=[DEFAULT_PYTHON], name="prune-local-branches", tags=["ext", "git"])
def clean_branches(session: nox.Session):
    log.info("Cleaning local branches that have been deleted from the remote.")
    PROTECTED_BRANCHES: list[str] = ["main", "master", "dev", "rc", "gh-pages"]

    try:
        options = session.posargs or session.default_args
    except Exception as exc:
        msg = Exception(
            f"({type(exc)}) Unhandled exception getting session args: {exc}"
        )
        options = session.posargs

    force = "force" in options

    ## Install GitPython
    session.install("gitpython")

    ## Import gitpython
    try:
        import git
    except ImportError as import_err:
        log.error(
            f"GitPython module is not installed. The nox session will install gitpython, but in order to get branches using the gitpython module, it must be installed on the host as well."
        )

        return

    ## Initialize repository
    repo = git.Repo(".")

    ## Fetch latest changes & prune deleted branches
    repo.git.fetch("--prune")

    ## Get a list of local branches
    local_branches: list[str] = [head.name for head in repo.heads]
    log.info(f"Found [{len(local_branches)}] local branch(es).")
    if len(local_branches) < 15:
        log.debug(f"Local branches: {local_branches}")

    ## Get a list of remote branches
    remote_branches: list[str] = [
        ref.name.replace("origin/", "") for ref in repo.remotes.origin.refs
    ]
    log.info(f"Found [{len(remote_branches)}] remote branch(es).")
    if len(remote_branches) < 15:
        log.debug(f"Remote branches: {remote_branches}")

    ## Find local branches that are not present in remote branches
    branches_to_delete: list[str] = [
        branch for branch in local_branches if branch not in remote_branches
    ]
    log.info(f"Prepared [{len(branches_to_delete)}] branch(es) for deletion.")
    if len(branches_to_delete) < 15:
        log.debug(f"Deleting branches: {branches_to_delete}")

    for branch in branches_to_delete:
        if branch not in PROTECTED_BRANCHES:  ## Avoid deleting specified branches
            try:
                repo.git.branch("-d", branch)
                log.info(f"Deleted branch '{branch}'")
            except git.GitError as git_err:
                msg = Exception(
                    f"Git error while deleting branch '{branch}'. Details: {git_err}"
                )

                if force:
                    log.warning("Force=True, attempting to delete with -D")
                    try:
                        repo.git.branch("-D", branch)
                        log.info(f"Force-deleted branch '{branch}'")
                    except git.GitError as git_err2:
                        msg2 = Exception(
                            f"Git error while force deleting branch '{branch}'. Details: {git_err2}"
                        )
                        log.warning(
                            f"Branch '{branch}' was not deleted. Reason: {msg2}"
                        )

                        ## Retry with subprocess
                        try:
                            log.info("Retrying using subprocess.")
                            session.run(["git", "branch", "-D", branch], external=True)
                            log.info(
                                f"Force-deleted branch '{branch}'. Required fallback to subprocess."
                            )
                        except git.GitError as git_err3:
                            msg3 = Exception(
                                f"Git error while force deleting branch '{branch}'. Details: {git_err3}"
                            )
                            log.warning(
                                f"Branch '{branch}' was not deleted. Reason: {msg3}"
                            )
                        except Exception as exc:
                            msg = Exception(
                                f"Unhandled exception attempting to delete git branch '{branch}' using subprocess.run(). Details: {exc}"
                            )
                            log.error(msg)

                else:
                    log.warning(f"Branch '{branch}' was not deleted. Reason: {msg}")

                continue
