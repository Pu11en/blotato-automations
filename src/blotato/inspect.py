"""The `inspect` action.

Spends zero credits. Fetches the current credit balance and the live
template catalog, sanitizes both, and writes them under
`outputs/blotato-inspect/<timestamp>/`.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import api
from . import runner as br
from .workspace import load_env, outputs_dir


def run(output_root: Path = None, *, workspace: Path = None) -> Path:
    if output_root is None:
        output_root = outputs_dir("blotato-inspect", root=workspace)
    env = load_env(root=workspace)
    api_key = br.load_api_key(env=env)

    credits_raw = api.get_credits(api_key)
    templates_raw = api.list_templates(api_key)

    retrieved_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_dir = output_root / f"{retrieved_at}"
    snapshot_dir.mkdir(parents=True, exist_ok=False)

    (snapshot_dir / "credits.sanitized.json").write_text(
        br.dump_sanitized_json({"retrieved_at": retrieved_at, "response": credits_raw}, secret_values=[api_key])
    )
    (snapshot_dir / "template-catalog.sanitized.json").write_text(
        br.dump_sanitized_json({"retrieved_at": retrieved_at, "response": templates_raw}, secret_values=[api_key])
    )

    # Also emit a plain summary for humans / tests.
    items = templates_raw.get("items", []) if isinstance(templates_raw, dict) else []
    image_input_templates = []
    for item in items:
        for inp in item.get("inputs", []):
            t = (inp.get("type") or {}).get("t")
            if t == "image":
                image_input_templates.append(
                    {
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "description": item.get("description"),
                        "image_input_field": inp.get("name"),
                    }
                )
                break
    summary = {
        "retrieved_at": retrieved_at,
        "credits_remaining": credits_raw.get("creditsRemaining"),
        "account_email": credits_raw.get("accountEmail"),
        "template_count": len(items),
        "image_input_template_count": len(image_input_templates),
        "image_input_templates": image_input_templates,
    }
    (snapshot_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    return snapshot_dir


if __name__ == "__main__":
    snapshot_dir = run()
    summary = json.loads((snapshot_dir / "summary.json").read_text())
    print(json.dumps({"snapshot_dir": str(snapshot_dir), "summary": summary}, indent=2))
