"""Generic submit: any approved plan.json -> one bounded Blotato call,
polled to completion, downloaded. Reuses the same safety checks
(sanitization, publishing/external-credential rejection, checksum
verification) built for blotato-brand-content, since those are
model-agnostic.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.blotato import api, runner as br
from catalog import get_model
from catalog.types import GenerationPlane, MediaItem

REPO_ROOT = Path(__file__).resolve().parents[3]
TERMINAL_STATUSES = {"done", "creation-from-template-failed", "insufficient-credits"}


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


def _resolve_media(plan: dict, api_key: str, repo_root: Path) -> dict:
    """Upload any local-path media items; pass through anything already a URL."""
    resolved = {}
    for role, items in plan["media"].items():
        media_items = []
        for item in items:
            if "url" in item:
                url = item["url"]
            else:
                asset_path = repo_root / item["local_path"]
                actual = br.hash_file(asset_path)
                if actual != item["checksum_sha256"]:
                    raise SystemExit(f"checksum drift on {item['asset_id']}; refuse to submit")
                content_type = "image/png" if asset_path.suffix.lower() == ".png" else "image/jpeg"
                presign = api.create_presigned_upload(api_key, asset_path.name)
                api.put_file_to_presigned_url(presign["presignedUrl"], asset_path, content_type)
                url = presign["publicUrl"]
            media_items.append(MediaItem(asset_id=item["asset_id"], url=url, caption=item.get("caption")))
        resolved[role] = media_items
    return resolved


def submit(plan_path: Path, *, poll_interval: float = 5, poll_timeout: float = 240) -> dict:
    plan = json.loads(plan_path.read_text())
    model = get_model(plan["model_id"])

    if model.broken:
        raise SystemExit(
            f"refusing to submit: catalog model '{model.id}' is marked BROKEN: {model.known_issues}"
        )

    ceiling = plan.get("max_credits_ceiling")
    if not ceiling or ceiling <= 0:
        raise SystemExit("refusing to submit: no positive max_credits_ceiling on the plan")
    if not plan["approval"].get("reference") or not plan["approval"].get("decided_at"):
        raise SystemExit("refusing to submit: plan has no recorded approval reference")

    env = load_env(REPO_ROOT / ".env")
    api_key = br.load_api_key(env=env)

    credits_before = api.get_credits(api_key)
    if credits_before["creditsRemaining"] < ceiling:
        raise SystemExit(
            f"refusing to submit: balance {credits_before['creditsRemaining']} below the {ceiling}-credit ceiling"
        )

    media = _resolve_media(plan, api_key, REPO_ROOT)
    plane = GenerationPlane(model_id=model.id, prompt=plan["prompt"], media=media, settings=plan["settings"])
    inputs = model.build_inputs(plane)

    request_fields = {
        "templateId": model.blotato_template_id,
        "inputs": inputs,
        "render": True,
        "title": f"blotato-studio/{model.id}/{plan['approval_digest'][:18]}",
    }
    br.validate_no_publishing_fields(request_fields)
    br.validate_no_external_provider_credentials(request_fields)

    run_dir = REPO_ROOT / "outputs" / "blotato-studio-runs" / plan["approval_digest"].replace("sha256:", "")[:16]
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True))
    (run_dir / "request.sanitized.json").write_text(
        br.dump_sanitized_json(request_fields, secret_values=[api_key])
    )

    submission = api.create_video_from_template(
        api_key,
        template_id=model.blotato_template_id,
        inputs=inputs,
        title=request_fields["title"],
        render=True,
    )
    job_id = submission["item"]["id"]
    (run_dir / "submission.sanitized.json").write_text(
        br.dump_sanitized_json(submission, secret_values=[api_key])
    )

    deadline = time.time() + poll_timeout
    last = submission["item"]
    poll_log = [last]
    while last.get("status") not in TERMINAL_STATUSES and time.time() < deadline:
        time.sleep(poll_interval)
        polled = api.get_video_creation(api_key, job_id)
        last = polled["item"]
        poll_log.append(last)
    (run_dir / "poll-log.sanitized.json").write_text(br.dump_sanitized_json(poll_log, secret_values=[api_key]))

    credits_after = api.get_credits(api_key)
    result = {
        "run_dir": str(run_dir.relative_to(REPO_ROOT)),
        "model_id": model.id,
        "job_id": job_id,
        "final_status": last.get("status"),
        "error": last.get("error"),
        "credits_before": credits_before["creditsRemaining"],
        "credits_after": credits_after["creditsRemaining"],
        "credits_observed_delta": credits_before["creditsRemaining"] - credits_after["creditsRemaining"],
        "media_path": None,
        "timed_out": last.get("status") not in TERMINAL_STATUSES,
    }

    media_url = last.get("mediaUrl") or next(iter(last.get("imageUrls") or []), None)
    if last.get("status") == "done" and media_url:
        media_dir = run_dir / "media"
        media_dir.mkdir(exist_ok=True)
        ext = Path(media_url).suffix or (".mp4" if last.get("mediaUrl") else ".jpg")
        media_path = media_dir / f"generated{ext}"
        urllib.request.urlretrieve(media_url, media_path)
        result["media_path"] = str(media_path.relative_to(REPO_ROOT))
        result["media_checksum_sha256"] = br.hash_file(media_path)
        result["all_image_urls"] = last.get("imageUrls")

    (run_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Submit an approved blotato-studio plan.")
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    result = submit(Path(args.plan))
    print(json.dumps(result, indent=2))
