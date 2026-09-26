"""Blotato Studio: pick a generation technique, plan it for free, approve a
credit ceiling, then spend credits on exactly one bounded call.

This package is meant to be depended on. Another project installs it, imports
from here, and gets Blotato's capabilities plus the guardrails, rather than
writing its own client:

    from blotato import build_plan, submit, list_models, workspace_root

    for technique in list_models(include_broken=False):
        print(technique.id, technique.observed_credits)

    plan = build_plan(model_id="infographic-whiteboard", prompt="...", media={})
    plan["max_credits_ceiling"] = 60
    plan["approval"] = {"reference": "who approved", "decided_at": "..."}
    result = submit_plan_file(path)

Everything named here is the supported surface; anything else is internal and
may move. To contribute your own techniques without forking, declare a
`blotato.techniques` entry point -- see docs/using-from-another-project.md.

Nothing in this package publishes, schedules, or touches a social account.
``BLOTATO_API_KEY`` is read from the environment (or the workspace `.env`)
and is never accepted as a function or CLI argument.
"""
from . import api
from .catalog import (
    DuplicateModelError,
    ENTRY_POINT_GROUP,
    GenerationPlane,
    MediaItem,
    ModelEntry,
    SettingField,
    UnknownModelError,
    get_model,
    list_models,
    origins,
    register,
)
from .digest import compute_approval_digest, verify_plan_digest
from .download import download
from .ledger import BudgetExceeded, ledger_path
from .ledger import entries as ledger_entries
from .ledger import spent as credits_spent
from .runner import MissingCredentialError, hash_file, load_api_key, sanitize
from .studio.plan import build_plan
from .studio.submit import poll as poll_run
from .studio.submit import submit as submit_plan_file
from .workspace import load_env, outputs_dir, resolve_asset, workspace_root

__version__ = "0.2.0"

__all__ = [
    # techniques
    "get_model",
    "list_models",
    "register",
    "origins",
    "ModelEntry",
    "SettingField",
    "GenerationPlane",
    "MediaItem",
    "ENTRY_POINT_GROUP",
    # the plan -> approve -> submit flow
    "build_plan",
    "submit_plan_file",
    "poll_run",
    "compute_approval_digest",
    "verify_plan_digest",
    # plumbing a consumer may legitimately need
    "api",
    "download",
    "credits_spent",
    "ledger_entries",
    "ledger_path",
    "hash_file",
    "sanitize",
    "load_api_key",
    "load_env",
    "workspace_root",
    "outputs_dir",
    "resolve_asset",
    # errors worth catching by name
    "UnknownModelError",
    "DuplicateModelError",
    "MissingCredentialError",
    "BudgetExceeded",
    "__version__",
]
