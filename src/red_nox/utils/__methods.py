from __future__ import annotations

import os

def detect_container_env(container_env_varname: str = "CONTAINER_ENV") -> bool:
    """Detect the presence of an env variable denoting a container environment.

    Params:
        container_env_varname (str): The name of the environment variable to search for.

    Returns:
        (True): If the environment variable is detected and it is set to `True`.
        (False): If the environment variable is not detected, or if it is detected and it is set to `False`.

    """
    ## Detect container env, or default to False
    if container_env_varname in os.environ:
        CONTAINER_ENV: bool = os.environ[container_env_varname]
    else:
        CONTAINER_ENV: bool = False

    return CONTAINER_ENV
