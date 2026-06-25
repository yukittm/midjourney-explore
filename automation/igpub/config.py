"""Config loading. Account id + defaults come from automation/config.yml (gitignored, non-secret).
The access token is read from the IG_SYSTEM_USER_TOKEN env var ONLY — never a file in the repo."""
from __future__ import annotations

import os

import yaml

CONFIG_PATH = "automation/config.yml"
TOKEN_ENV = "IG_SYSTEM_USER_TOKEN"


def load_config(repo_root: str = ".", path: str = CONFIG_PATH) -> dict:
    full = os.path.join(repo_root, path)
    if not os.path.isfile(full):
        return {}
    with open(full, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_token() -> str:
    token = os.environ.get(TOKEN_ENV, "")
    if not token:
        raise RuntimeError(
            f"{TOKEN_ENV} is not set — the System User token is read from the environment, never the repo"
        )
    return token
