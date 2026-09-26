"""Standard-library runner foundation for the blotato-brand-content skill.

Covers configuration, atomic run-directory state, asset hashing, resume
behavior, secret sanitization, and strict pre-flight validation. No HTTP
calls live here yet -- those are added on top of this foundation by the
live-inspection and generation tasks.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import os
import re
import secrets
import string
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

SCHEMA_VERSION = 1

# Keep in sync with schemas/blotato-run.schema.json.
STATES = (
    "INSPECTED",
    "PLANNED",
    "IMAGE_RUNNING",
    "IMAGE_READY",
    "IMAGE_APPROVED",
    "VIDEO_RUNNING",
    "VIDEO_READY",
    "AUDIT_READY",
    "FAILED",
    "TIMED_OUT",
    "REJECTED",
)

ALLOWED_TRANSITIONS = {
    "INSPECTED": {"PLANNED"},
    "PLANNED": {"IMAGE_RUNNING"},
    "IMAGE_RUNNING": {"IMAGE_READY", "FAILED", "TIMED_OUT"},
    "IMAGE_READY": {"IMAGE_APPROVED", "REJECTED"},
    "IMAGE_APPROVED": {"VIDEO_RUNNING"},
    "VIDEO_RUNNING": {"VIDEO_READY", "FAILED", "TIMED_OUT"},
    "VIDEO_READY": {"AUDIT_READY", "REJECTED"},
    "AUDIT_READY": set(),
    "FAILED": set(),
    "TIMED_OUT": set(),
    "REJECTED": set(),
}

GENERATION_STAGES = ("image", "video")

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


class InvalidTransitionError(BlotatoRunError):
    pass


class DuplicateSubmissionError(BlotatoRunError):
    """Raised when code tries to submit a second paid request for a stage
    that already has a stored external request id."""


class RunLockedError(BlotatoRunError):
    pass


class RunValidationError(BlotatoRunError):
    pass


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def new_run_id(brand_id: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short_id = "".join(secrets.choice(string.hexdigits.lower()[:16]) for _ in range(6))
    return f"{timestamp}-{brand_id}-{short_id}"


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
# Run state
# --------------------------------------------------------------------------

class RunState:
    def __init__(self, data: dict):
        self._data = data

    @classmethod
    def new(cls, brand_id: str, run_id: Optional[str] = None) -> "RunState":
        now = utcnow_iso()
        return cls(
            {
                "schema_version": SCHEMA_VERSION,
                "run_id": run_id or new_run_id(brand_id),
                "brand_id": brand_id,
                "created_at": now,
                "updated_at": now,
                "state": "INSPECTED",
            }
        )

    @property
    def run_id(self) -> str:
        return self._data["run_id"]

    @property
    def state(self) -> str:
        return self._data["state"]

    def to_dict(self) -> dict:
        return copy.deepcopy(self._data)

    def can_transition(self, target_state: str) -> bool:
        return target_state in ALLOWED_TRANSITIONS.get(self.state, set())

    def transition(self, target_state: str) -> None:
        if target_state not in STATES:
            raise InvalidTransitionError(f"unknown state: {target_state}")
        if not self.can_transition(target_state):
            raise InvalidTransitionError(
                f"cannot transition from {self.state} to {target_state}"
            )
        self._data["state"] = target_state
        self._data["updated_at"] = utcnow_iso()

    def pending_request_id(self, stage: str) -> Optional[str]:
        """Return a stored external request id for `stage` if one already
        exists, so callers poll instead of submitting a duplicate."""
        record = self._data.get(stage)
        if record:
            return record.get("request_id")
        return None

    def begin_generation(self, stage: str, request_id: str) -> None:
        if stage not in GENERATION_STAGES:
            raise BlotatoRunError(f"unknown generation stage: {stage}")
        existing = self.pending_request_id(stage)
        if existing is not None:
            raise DuplicateSubmissionError(
                f"{stage} already has request id {existing}; resume by polling it, "
                "do not submit another"
            )
        self._data[stage] = {
            "request_id": request_id,
            "status": "submitted",
            "submitted_at": utcnow_iso(),
        }
        self._data["updated_at"] = utcnow_iso()

    def complete_generation(
        self,
        stage: str,
        *,
        output_path: str,
        checksum_sha256: str,
        credits_observed_delta: float,
    ) -> None:
        if stage not in GENERATION_STAGES:
            raise BlotatoRunError(f"unknown generation stage: {stage}")
        record = self._data.get(stage)
        if not record or not record.get("request_id"):
            raise BlotatoRunError(f"cannot complete {stage} generation with no pending request")
        record["status"] = "succeeded"
        record["completed_at"] = utcnow_iso()
        record["output_path"] = output_path
        record["checksum_sha256"] = checksum_sha256
        record["credits_observed_delta"] = credits_observed_delta
        self._data["updated_at"] = utcnow_iso()

    def record_image_approval(
        self, *, decision: str, bound_checksum_sha256: str, decision_reference: str
    ) -> None:
        image = self._data.get("image")
        if not image or image.get("checksum_sha256") != bound_checksum_sha256:
            raise RunValidationError(
                "approval checksum does not match the generated image's checksum"
            )
        self._data["image_approval"] = {
            "decision": decision,
            "bound_checksum_sha256": bound_checksum_sha256,
            "decided_at": utcnow_iso(),
            "decision_reference": decision_reference,
        }
        self._data["updated_at"] = utcnow_iso()


# --------------------------------------------------------------------------
# Run store: atomic, single-writer, file-backed
# --------------------------------------------------------------------------

class RunStore:
    def __init__(self, outputs_root: Path):
        self.outputs_root = Path(outputs_root)

    def run_dir(self, run_id: str) -> Path:
        return self.outputs_root / run_id

    def state_path(self, run_id: str) -> Path:
        return self.run_dir(run_id) / "state.json"

    def create(self, run_state: RunState) -> Path:
        run_dir = self.run_dir(run_state.run_id)
        run_dir.mkdir(parents=True, exist_ok=False)
        self.save(run_state)
        return run_dir

    def save(self, run_state: RunState) -> None:
        run_dir = self.run_dir(run_state.run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        _atomic_write_json(self.state_path(run_state.run_id), run_state.to_dict())

    def load(self, run_id: str) -> RunState:
        path = self.state_path(run_id)
        if not path.is_file():
            raise BlotatoRunError(f"no run found: {run_id}")
        return RunState(json.loads(path.read_text()))

    @contextlib.contextmanager
    def lock(self, run_id: str):
        run_dir = self.run_dir(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        lock_path = run_dir / ".lock"
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise RunLockedError(f"run {run_id} is locked by another writer") from exc
        try:
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            yield
        finally:
            with contextlib.suppress(FileNotFoundError):
                os.remove(lock_path)


def _atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    tmp_path.write_text(json.dumps(data, indent=2, sort_keys=True))
    os.replace(tmp_path, path)


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


def validate_state_transition(run_state: RunState, target_state: str) -> None:
    if target_state not in STATES:
        raise RunValidationError(f"unknown target state: {target_state}")
    if not run_state.can_transition(target_state):
        raise RunValidationError(
            f"invalid state transition: {run_state.state} -> {target_state}"
        )


def validate_source_asset(profile: dict, asset_id: str, repo_root: Path) -> dict:
    assets = {asset["asset_id"]: asset for asset in profile.get("assets", [])}
    asset = assets.get(asset_id)
    if asset is None:
        raise RunValidationError(f"unknown source asset: {asset_id}")

    provenance = asset.get("provenance") or ""
    rights = asset.get("rights") or ""
    if not provenance.strip() or not rights.strip():
        raise RunValidationError(
            f"source asset {asset_id} is missing provenance or rights metadata"
        )

    asset_path = repo_root / asset["path"]
    if not asset_path.is_file():
        raise RunValidationError(f"source asset {asset_id} is not accessible at {asset_path}")

    recorded_checksum = asset.get("checksum_sha256")
    if recorded_checksum:
        actual_checksum = hash_file(asset_path)
        if actual_checksum != recorded_checksum:
            raise RunValidationError(
                f"source asset {asset_id} checksum mismatch: "
                f"recorded {recorded_checksum}, actual {actual_checksum}"
            )
    return asset


def validate_generation_request(
    *,
    profile: dict,
    run_state: RunState,
    target_state: str,
    source_asset_id: str,
    request_fields: dict,
    repo_root: Path,
) -> None:
    """Run every pre-flight check required before a paid HTTP call. Raises
    RunValidationError on the first violation found; callers must not
    proceed to an HTTP request if this raises."""
    validate_no_publishing_fields(request_fields)
    validate_no_external_provider_credentials(request_fields)
    validate_state_transition(run_state, target_state)
    validate_source_asset(profile, source_asset_id, repo_root)
