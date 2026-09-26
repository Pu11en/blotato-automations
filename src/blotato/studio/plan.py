"""Generic plan builder: any catalog model + prompt + media + settings ->
a reviewable plan.json. No HTTP calls, zero credit cost.

Note on state model: blotato-brand-content's RunState (INSPECTED -> PLANNED
-> IMAGE_RUNNING -> ... -> AUDIT_READY) assumes every technique is a
two-stage image-then-video pipeline. Live testing showed that's not true
across Blotato's templates -- some return an image directly, some a video
directly, none we've tried do a clean two-stage handoff. This tool uses a
simpler, honest state instead: PLANNED -> RUNNING -> READY/FAILED/TIMED_OUT.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .. import runner as br
from ..catalog import get_model
from ..digest import compute_approval_digest
from ..workspace import resolve_asset


def _validate_settings(model, settings: dict) -> None:
    """Enforce the bounds each catalog entry declares on its own settings.

    `SettingField` has carried min/max and min_length/max_length since it was
    written, and nothing read them.
    """
    for name, value in settings.items():
        spec = model.settings.get(name)
        if spec is None:
            raise ValueError(
                f"model {model.id} has no setting '{name}'; known: {sorted(model.settings)}"
            )
        if spec.kind == "enum" and spec.values and value not in spec.values:
            raise ValueError(f"setting '{name}' must be one of {list(spec.values)}; got {value!r}")
        if spec.kind == "range":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"setting '{name}' must be a number; got {value!r}")
            if spec.min is not None and value < spec.min:
                raise ValueError(f"setting '{name}' must be >= {spec.min}; got {value!r}")
            if spec.max is not None and value > spec.max:
                raise ValueError(f"setting '{name}' must be <= {spec.max}; got {value!r}")
        if spec.kind == "boolean" and not isinstance(value, bool):
            raise ValueError(f"setting '{name}' must be a boolean; got {value!r}")
        if spec.kind == "text":
            if not isinstance(value, str):
                raise ValueError(f"setting '{name}' must be a string; got {value!r}")
            if spec.min_length is not None and len(value) < spec.min_length:
                raise ValueError(
                    f"setting '{name}' must be at least {spec.min_length} characters"
                )
            if spec.max_length is not None and len(value) > spec.max_length:
                raise ValueError(
                    f"setting '{name}' must be at most {spec.max_length} characters"
                )


def build_plan(
    *,
    model_id: str,
    prompt: str,
    media: dict,
    settings: dict = None,
    workspace: Path = None,
) -> dict:
    model = get_model(model_id)
    settings = dict(settings or {})
    media = media or {}

    if not prompt or not prompt.strip():
        raise ValueError("prompt must not be empty")
    _validate_settings(model, settings)

    for role, (lo, hi) in model.roles.items():
        count = len(media.get(role, []))
        if not (lo <= count <= hi):
            raise ValueError(f"role '{role}' expects {lo}-{hi} item(s) for {model_id}, got {count}")
    for role in media:
        if role not in model.roles:
            raise ValueError(f"model {model_id} does not accept role '{role}'")

    resolved_media = {}
    for role, items in media.items():
        resolved_items = []
        for item in items:
            if "path" in item:
                asset_path = resolve_asset(item["path"], root=workspace)
                if not asset_path.is_file():
                    raise ValueError(f"asset not accessible: {asset_path}")
                checksum = br.hash_file(asset_path)
                if item.get("checksum_sha256") and item["checksum_sha256"] != checksum:
                    raise ValueError(f"checksum drift on {item.get('asset_id', item['path'])}")
                resolved_items.append(
                    {
                        "asset_id": item.get("asset_id", asset_path.name),
                        "local_path": item["path"],
                        "checksum_sha256": checksum,
                        "caption": item.get("caption"),
                    }
                )
            elif "url" in item:
                resolved_items.append(
                    {
                        "asset_id": item.get("asset_id", item["url"]),
                        "url": item["url"],
                        "caption": item.get("caption"),
                    }
                )
            else:
                raise ValueError(f"media item needs 'path' or 'url': {item}")
        resolved_media[role] = resolved_items

    plan = {
        "schema_version": 1,
        "model_id": model.id,
        "blotato_template_id": model.blotato_template_id,
        "surface": model.surface,
        "label": model.label,
        "prompt": prompt,
        "media": resolved_media,
        "settings": settings,
        "known_issues": list(model.known_issues),
        "broken": model.broken,
        "verified_at": model.verified_at,
        "max_credits_ceiling": None,
        "approval": {"reference": None, "decided_at": None},
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    plan["approval_digest"] = compute_approval_digest(
        model_id=model.id, prompt=prompt, media=resolved_media, settings=settings
    )

    if model.broken:
        print(
            f"WARNING: catalog model '{model.id}' is marked BROKEN: {model.known_issues}",
            file=sys.stderr,
        )

    return plan


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build a blotato-studio plan (zero cost).")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        help="Repo-relative path to a local reference image (repeatable).",
    )
    parser.add_argument("--out", required=True, help="Where to write plan.json")
    args = parser.parse_args()

    media = {"reference": [{"path": p} for p in args.reference]} if args.reference else {}
    plan = build_plan(model_id=args.model, prompt=args.prompt, media=media)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2, sort_keys=True))
    print(json.dumps(plan, indent=2))
