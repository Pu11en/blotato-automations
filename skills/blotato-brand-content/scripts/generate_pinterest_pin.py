"""Build and submit a Blotato "Image Slideshow with Text Overlays" run
from an approved Pinterest research brief. Uses the real, unaltered
product photo for every slide (true exact-asset: no generative edit of
the product itself), with on-screen captions sourced from the brief's
shot list -- muted-first per the Pinterest research evidence.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.blotato import api as api
from scripts.blotato import runner as br
from blotato_inspect import load_env

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_ID = "/base/v2/image-slideshow/5903b592-1255-43b4-b9ac-f8ed7cbf6a5f/v1"
TERMINAL_STATUSES = {"done", "creation-from-template-failed", "insufficient-credits"}


def load_brief_pack(run_dir: Path, brief_key: str) -> dict:
    return json.loads((run_dir / "briefs" / brief_key / "brief.json").read_text())


def load_cinco_profile() -> dict:
    profile = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "profile.json").read_text())
    claims = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "claims.json").read_text())
    profile["claims"] = claims["claims"]
    return profile


def check_claims(text: str, profile: dict) -> None:
    import re
    hits = [e["id"] for e in profile["claims"]["blocked"] if re.search(e["pattern"], text, re.IGNORECASE)]
    if hits:
        raise SystemExit(f"caption text hit blocked claims: {hits} :: {text!r}")


def run(*, brief_pack: dict, max_credits_ceiling: int, poll_interval=5, poll_timeout=240) -> dict:
    profile = load_cinco_profile()
    brief = brief_pack["brief"]
    assets_state = {a["id"]: a for a in brief_pack["assets"]}

    for shot in brief["shots"]:
        check_claims(shot["overlay"], profile)
        for asset_id in shot["asset_ids"]:
            asset = assets_state[asset_id]
            if not asset["ready"]:
                raise SystemExit(f"asset {asset_id} is not ready (approved/rights/checksum)")

    env = load_env(REPO_ROOT / ".env")
    api_key = br.load_api_key(env=env)

    credits_before = api.get_credits(api_key)
    if credits_before["creditsRemaining"] < max_credits_ceiling:
        raise SystemExit("balance below ceiling; refusing to generate")

    run_id = br.new_run_id(profile["brand_id"])
    run_dir = REPO_ROOT / "outputs" / "blotato-runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "pinterest-brief-pack.json").write_text(json.dumps(brief_pack, indent=2, sort_keys=True))

    # Upload each distinct real asset once; reuse the URL across slides.
    upload_urls: dict[str, str] = {}
    for asset_id, asset in assets_state.items():
        source_path = REPO_ROOT / asset["path"]
        actual = br.hash_file(source_path)
        if actual != asset["sha256"]:
            raise SystemExit(f"checksum drift on {asset_id}; refuse to generate")
        presign = api.create_presigned_upload(api_key, source_path.name)
        content_type = "image/png" if source_path.suffix.lower() == ".png" else "image/jpeg"
        api.put_file_to_presigned_url(presign["presignedUrl"], source_path, content_type)
        upload_urls[asset_id] = presign["publicUrl"]

    slides = []
    for shot in brief["shots"]:
        asset_id = shot["asset_ids"][0]
        slides.append({"imageSource": upload_urls[asset_id], "textOverlay": shot["overlay"]})

    inputs = {
        "slides": slides,
        "textPosition": "bottom",
        "textStyle": "elegant",
        "textColor": "#FFFFFF",
        "aspectRatio": "9:16",
        "slideDuration": max(1, min(10, brief["duration_seconds"] / len(slides))),
        "transition": "fade",
    }

    request_fields = {
        "templateId": TEMPLATE_ID,
        "inputs": inputs,
        "render": True,
        "title": f"cinco-h-ranch/{run_id}/{brief_pack['experiment_id']}",
    }
    br.validate_no_publishing_fields(request_fields)
    br.validate_no_external_provider_credentials(request_fields)

    (run_dir / "request.sanitized.json").write_text(
        br.dump_sanitized_json(request_fields, secret_values=[api_key])
    )

    submission = api.create_video_from_template(
        api_key,
        template_id=TEMPLATE_ID,
        inputs=inputs,
        title=request_fields["title"],
        render=True,
    )
    video_id = submission["item"]["id"]
    (run_dir / "submission.sanitized.json").write_text(
        br.dump_sanitized_json(submission, secret_values=[api_key])
    )
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

    (run_dir / "poll-log.sanitized.json").write_text(br.dump_sanitized_json(poll_log, secret_values=[api_key]))

    credits_after = api.get_credits(api_key)
    result = {
        "run_id": run_id,
        "run_dir": str(run_dir.relative_to(REPO_ROOT)),
        "video_id": video_id,
        "final_status": last.get("status"),
        "error": last.get("error"),
        "credits_before": credits_before["creditsRemaining"],
        "credits_after": credits_after["creditsRemaining"],
        "credits_observed_delta": credits_before["creditsRemaining"] - credits_after["creditsRemaining"],
        "media_url": last.get("mediaUrl"),
        "image_urls": last.get("imageUrls"),
        "media_path": None,
        "timed_out": last.get("status") not in TERMINAL_STATUSES,
    }

    media_source_url = last.get("mediaUrl") or (last.get("imageUrls") or [None])[0]
    if last.get("status") == "done" and media_source_url:
        media_dir = run_dir / "media"
        media_dir.mkdir(exist_ok=True)
        ext = Path(media_source_url).suffix or (".mp4" if last.get("mediaUrl") else ".jpg")
        media_path = media_dir / f"generated{ext}"
        urllib.request.urlretrieve(media_source_url, media_path)
        result["media_path"] = str(media_path.relative_to(REPO_ROOT))
        result["media_checksum_sha256"] = br.hash_file(media_path)

    (run_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    run_dir = REPO_ROOT / "outputs" / "pinterest" / "research-20260908"
    brief_pack = load_brief_pack(run_dir, "cand-after-the-harvest-video-pin-v1-v1")
    result = run(brief_pack=brief_pack, max_credits_ceiling=1000)
    print(json.dumps(result, indent=2))
