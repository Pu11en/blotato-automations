"""Credential loading, hashing, secret sanitization and pre-flight refusals.

This began as a runner for the brand-content skill and also carried a
RunState/RunStore state machine modelling every technique as a two-stage
image-then-video pipeline. Live testing showed that is not how Blotato's
templates behave (see studio/plan.py), nothing ever called it, and its
lock file wedged a run permanently if the process died holding it. It was
removed; `git log -- src/blotato/runner.py` has it if a state machine is
ever wanted again.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Iterable, Optional

_SECRET_KEY_PATTERN = re.compile(
    r"(api[-_]?key|authoriz|auth[-_]?token|access[-_]?token|bearer|secret|password|passwd|cookie)",
    re.IGNORECASE,
)

_PUBLISHING_FIELD_PATTERN = re.compile(
    r"(publish|schedule|social[-_]?account|account[-_]?id|post[-_]?id|calendar)",
    re.IGNORECASE,
)

_EXTERNAL_PROVIDER_PATTERN = re.compile(
    r"(openai|anthropic|stability|replicate|elevenlabs|runway|midjourney|google|azure)"
    r"[-_]?(api[-_]?key|token|secret|credential)",
    re.IGNORECASE,
)

REDACTED = "[REDACTED]"


class BlotatoRunError(Exception):
    """Base class for runner errors."""


class MissingCredentialError(BlotatoRunError):
    pass


class RunValidationError(BlotatoRunError):
    pass


def load_api_key(env: Optional[dict] = None) -> str:
    """Read BLOTATO_API_KEY from the environment only.

    Never accept this as a function/CLI argument in calling code -- that is
    the whole point of routing every caller through this function.
    """
    source = env if env is not None else os.environ
    key = source.get("BLOTATO_API_KEY")
    if not key:
        raise MissingCredentialError("BLOTATO_API_KEY is not set in the environment")
    return key


def hash_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------
# Sanitization
# --------------------------------------------------------------------------

def sanitize(value: Any, secret_values: Iterable[str] = ()) -> Any:
    """Recursively redact credential-shaped fields and any configured
    secret literal values, without mutating the input."""
    secret_values = [s for s in secret_values if s]

    def _sanitize(node: Any) -> Any:
        if isinstance(node, dict):
            result = {}
            for key, val in node.items():
                if isinstance(key, str) and _SECRET_KEY_PATTERN.search(key):
                    result[key] = REDACTED
                else:
                    result[key] = _sanitize(val)
            return result
        if isinstance(node, list):
            return [_sanitize(item) for item in node]
        if isinstance(node, str):
            redacted = node
            for secret in secret_values:
                if secret and secret in redacted:
                    redacted = redacted.replace(secret, REDACTED)
            return redacted
        return node

    return _sanitize(copy.deepcopy(value))


def dump_sanitized_json(value: Any, secret_values: Iterable[str] = ()) -> str:
    return json.dumps(sanitize(value, secret_values), indent=2, sort_keys=True)


# --------------------------------------------------------------------------
# Strict pre-flight validation (2.3)
# --------------------------------------------------------------------------

def _find_matching_keys(payload: Any, pattern: re.Pattern, path: str = "") -> list:
    matches = []
    if isinstance(payload, dict):
        for key, val in payload.items():
            key_path = f"{path}.{key}" if path else str(key)
            if isinstance(key, str) and pattern.search(key):
                matches.append(key_path)
            matches.extend(_find_matching_keys(val, pattern, key_path))
    elif isinstance(payload, list):
        for index, item in enumerate(payload):
            matches.extend(_find_matching_keys(item, pattern, f"{path}[{index}]"))
    return matches


def validate_no_publishing_fields(request_fields: dict) -> None:
    matches = _find_matching_keys(request_fields, _PUBLISHING_FIELD_PATTERN)
    if matches:
        raise RunValidationError(f"publishing-related fields are not permitted: {matches}")


def validate_no_external_provider_credentials(request_fields: dict) -> None:
    matches = _find_matching_keys(request_fields, _EXTERNAL_PROVIDER_PATTERN)
    if matches:
        raise RunValidationError(f"external-provider credential fields are not permitted: {matches}")
