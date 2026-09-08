"""blotato-brand-content: bounded, approved generation run.

Loads an approved plan (must carry a max_credits_ceiling and an approval
reference), uploads the verified source asset, submits exactly one
generation request, persists the request id before polling, polls to a
terminal state, downloads the result, and records the observed credit
delta. Never resubmits automatically.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blotato_api as api
import blotato_run as br
from blotato_inspect import load_env

REPO_ROOT = Path(__file__).resolve().parents[3]

TERMINAL_STATUSES = {"done", "creation-from-template-failed", "insufficient-credits"}


def run(plan_path: Path, *, poll_interval=5, poll_timeout=240) -> dict:
    plan = json.loads(plan_path.read_text())

    ceiling = plan["credits"].get("max_credits_ceiling")
    if not ceiling or ceiling <= 0:
        raise SystemExit("refusing to generate: no positive max_credits_ceiling on the plan")
    if not plan["approval"].get("reference") or not plan["approval"].get("decided_at"):
        raise SystemExit("refusing to generate: plan has no recorded approval reference")

    env = load_env(REPO_ROOT / ".env")
    api_key = br.load_api_key(env=env)

    # Revalidate current balance covers the ceiling.
    credits_before = api.get_credits(api_key)
    if credits_before["creditsRemaining"] < ceiling:
        raise SystemExit(
            f"refusing to generate: balance {credits_before['creditsRemaining']} "
            f"is below the {ceiling}-credit ceiling"
        )

    run_id = br.new_run_id(plan["brand_id"])
    run_dir = REPO_ROOT / "outputs" / "blotato-runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True))

    # Upload the exact verified local asset (not a re-fetch of the live site).
    source_path = REPO_ROOT / plan["source_asset"]["path"]
    actual_checksum = br.hash_file(source_path)
    if actual_checksum != plan["source_asset"]["checksum_sha256"]:
        raise SystemExit("refusing to generate: source asset checksum drift since plan was built")

    presign = api.create_presigned_upload(api_key, source_path.name)
    api.put_file_to_presigned_url(presign["presignedUrl"], source_path, "image/jpeg")
    product_image_url = presign["publicUrl"]

    request_fields = {
        "templateId": plan["template"]["id"],
        "inputs": {
            "productImage": product_image_url,
            "sceneDescription": plan["prompt"]["sceneDescription"],
        },
        "render": True,
        "title": f"cinco-h-ranch/{run_id}",
    }
    # Defense-in-depth: same gate the schema/tests already exercise.
    br.validate_no_publishing_fields(request_fields)
    br.validate_no_external_provider_credentials(request_fields)

    (run_dir / "request.sanitized.json").write_text(
        br.dump_sanitized_json(request_fields, secret_values=[api_key])
    )

    submission = api.create_video_from_template(
        api_key,
        template_id=plan["template"]["id"],
        inputs=request_fields["inputs"],
        title=request_fields["title"],
        render=True,
    )
    video_id = submission["item"]["id"]
    (run_dir / "submission.sanitized.json").write_text(
        br.dump_sanitized_json(submission, secret_values=[api_key])
    )
    # Persist the request id before polling -- resume point if interrupted.
    state_path = run_dir / "state.json"
    state_path.write_text(json.dumps({"run_id": run_id, "video_id": video_id, "status": submission["item"]["status"]}, indent=2))

    deadline = time.time() + poll_timeout
    last = submission["item"]
    poll_log = [last]
    while last.get("status") not in TERMINAL_STATUSES and time.time() < deadline:
        time.sleep(poll_interval)
        polled = api.get_video_creation(api_key, video_id)
        last = polled["item"]
        poll_log.append(last)
        state_path.write_text(json.dumps({"run_id": run_id, "video_id": video_id, "status": last.get("status")}, indent=2))

    (run_dir / "poll-log.sanitized.json").write_text(
        br.dump_sanitized_json(poll_log, secret_values=[api_key])
    )

    credits_after = api.get_credits(api_key)
    delta = credits_before["creditsRemaining"] - credits_after["creditsRemaining"]

    result = {
        "run_id": run_id,
        "run_dir": str(run_dir.relative_to(REPO_ROOT)),
        "video_id": video_id,
        "final_status": last.get("status"),
        "error": last.get("error"),
        "credits_before": credits_before["creditsRemaining"],
        "credits_after": credits_after["creditsRemaining"],
        "credits_observed_delta": delta,
        "media_url": last.get("mediaUrl"),
        "media_path": None,
        "timed_out": last.get("status") not in TERMINAL_STATUSES,
    }

    if last.get("status") == "done" and last.get("mediaUrl"):
        media_dir = run_dir / "media"
        media_dir.mkdir(exist_ok=True)
        ext = Path(last["mediaUrl"]).suffix or ".mp4"
        media_path = media_dir / f"generated{ext}"
        urllib.request.urlretrieve(last["mediaUrl"], media_path)
        result["media_path"] = str(media_path.relative_to(REPO_ROOT))
        result["media_checksum_sha256"] = br.hash_file(media_path)

    (run_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    plan_path = REPO_ROOT / "outputs" / "blotato-plans" / "7de34d01402e.json"
    result = run(plan_path)
    print(json.dumps(result, indent=2))
