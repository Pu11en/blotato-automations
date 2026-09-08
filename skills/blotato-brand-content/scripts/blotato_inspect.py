"""blotato-brand-content: `inspect` action.

Spends zero credits. Fetches the current credit balance and the live
template catalog, sanitizes both, and writes them under
`outputs/blotato-inspect/<timestamp>/`.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blotato_api as api
import blotato_run as br


def load_env(env_path: Path) -> dict:
    env: dict = {}
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def run(repo_root: Path, output_root: Path) -> Path:
    env = load_env(repo_root / ".env")
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
    repo_root = Path(__file__).resolve().parents[3]
    output_root = repo_root / "outputs" / "blotato-inspect"
    snapshot_dir = run(repo_root, output_root)
    summary = json.loads((snapshot_dir / "summary.json").read_text())
    print(json.dumps({"snapshot_dir": str(snapshot_dir), "summary": summary}, indent=2))
