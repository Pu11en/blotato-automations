"""Where the tool reads inputs from and writes outputs to.

The package is installable, so there is no "repo root" to anchor paths to
any more. Everything resolves against a *workspace* directory instead:
``$BLOTATO_WORKSPACE`` if set, otherwise the current working directory.
That is what lets `blotato plan` and `blotato submit` run from any folder
on any machine rather than only from a checkout of this repository.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

WORKSPACE_ENV_VAR = "BLOTATO_WORKSPACE"


def workspace_root(override: Optional[Path] = None) -> Path:
    if override is not None:
        return Path(override).resolve()
    configured = os.environ.get(WORKSPACE_ENV_VAR)
    if configured:
        return Path(configured).resolve()
    return Path.cwd().resolve()


def outputs_dir(kind: str, *, root: Optional[Path] = None) -> Path:
    return workspace_root(root) / "outputs" / kind


def resolve_asset(path, *, root: Optional[Path] = None) -> Path:
    """Absolute paths pass through; relative ones resolve against the workspace."""
    candidate = Path(path)
    return candidate if candidate.is_absolute() else workspace_root(root) / candidate


def describe_path(path: Path, *, root: Optional[Path] = None) -> str:
    """Workspace-relative when possible, absolute otherwise, for logs and results."""
    path = Path(path)
    try:
        return str(path.relative_to(workspace_root(root)))
    except ValueError:
        return str(path)


def read_env_file(env_path: Path) -> dict:
    env: dict = {}
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def load_env(env_path: Optional[Path] = None, *, root: Optional[Path] = None) -> dict:
    """Return the process environment overlaid with the workspace `.env`.

    The real environment wins, so an exported BLOTATO_API_KEY beats a stale
    `.env` line. Nothing here mutates ``os.environ``. Callers pass the
    result to ``runner.load_api_key(env=...)``, which is why a plain
    ``export BLOTATO_API_KEY=...`` with no `.env` file present now works --
    previously only the file was consulted.
    """
    if env_path is None:
        env_path = workspace_root(root) / ".env"
    merged = read_env_file(env_path)
    merged.update({k: v for k, v in os.environ.items() if v})
    return merged
