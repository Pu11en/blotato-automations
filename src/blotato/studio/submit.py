"""Generic submit: any approved plan.json -> one bounded Blotato call,
polled to completion, downloaded. Reuses the same safety checks
(sanitization, publishing/external-credential rejection, checksum
verification) built for blotato-brand-content, since those are
model-agnostic.

Credits are spent at exactly one line in this file: the
`api.create_video_from_template` call. Everything before it is a refusal
gate; everything after it is recovery, because by then the money is gone.
"""
from __future__ import annotations

import json
import time
import urllib.error
from pathlib import Path

from .. import api
from .. import runner as br
from ..catalog import get_model
from ..catalog.types import GenerationPlane, MediaItem
from ..digest import verify_plan_digest
from ..download import download, extension_for
from ..workspace import describe_path, load_env, outputs_dir, resolve_asset

TERMINAL_STATUSES = {"done", "creation-from-template-failed", "insufficient-credits"}


def _resolve_media(plan: dict, api_key: str, workspace: Path = None) -> dict:
    """Upload any local-path media items; pass through anything already a URL."""
    resolved = {}
    for role, items in plan["media"].items():
        media_items = []
        for item in items:
            if "url" in item:
                url = item["url"]
            else:
                asset_path = resolve_asset(item["local_path"], root=workspace)
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


def run_dir_for(plan: dict, *, workspace: Path = None) -> Path:
    return outputs_dir("blotato-studio-runs", root=workspace) / plan["approval_digest"].replace(
        "sha256:", ""
    )[:16]


def _write(run_dir: Path, name: str, payload, api_key: str = None) -> None:
    if api_key is None:
        run_dir.joinpath(name).write_text(json.dumps(payload, indent=2, sort_keys=True))
    else:
        run_dir.joinpath(name).write_text(br.dump_sanitized_json(payload, secret_values=[api_key]))


def _poll_until_terminal(
    api_key: str,
    job_id: str,
    first: dict,
    *,
    poll_interval: float,
    poll_timeout: float,
) -> tuple:
    deadline = time.time() + poll_timeout
    last = first
    poll_log = [last]
    while last.get("status") not in TERMINAL_STATUSES and time.time() < deadline:
        time.sleep(poll_interval)
        last = api.get_video_creation(api_key, job_id)["item"]
        poll_log.append(last)
    return last, poll_log


def _download_media(item: dict, run_dir: Path, *, workspace: Path = None) -> dict:
    """Fetch every asset the job produced, not just the first one."""
    video_url = item.get("mediaUrl")
    image_urls = list(item.get("imageUrls") or [])
    urls = []
    for candidate in ([video_url] if video_url else []) + image_urls:
        if candidate and candidate not in urls:
            urls.append(candidate)
    if not urls:
        return {"media_path": None, "media_paths": [], "all_image_urls": image_urls}

    media_dir = run_dir / "media"
    media_dir.mkdir(exist_ok=True)
    paths, checksums = [], []
    single = len(urls) == 1
    for index, url in enumerate(urls, start=1):
        fallback = ".mp4" if url == video_url else ".jpg"
        ext = extension_for(url, fallback=fallback)
        name = f"generated{ext}" if single else f"generated-{index}{ext}"
        path = media_dir / name
        download(url, path)
        paths.append(describe_path(path, root=workspace))
        checksums.append(br.hash_file(path))

    return {
        "media_path": paths[0],
        "media_paths": paths,
        "media_checksum_sha256": checksums[0],
        "media_checksums_sha256": checksums,
        "all_image_urls": image_urls,
    }


def _finish(
    *,
    run_dir: Path,
    api_key: str,
    model_id: str,
    job_id: str,
    last: dict,
    poll_log: list,
    credits_before,
    workspace: Path = None,
) -> dict:
    _write(run_dir, "poll-log.sanitized.json", poll_log, api_key)
    try:
        remaining = api.get_credits(api_key)["creditsRemaining"]
    except (api.BlotatoHttpError, urllib.error.URLError, OSError):
        # Never lose the run record over a follow-up balance check.
        remaining = None
    timed_out = last.get("status") not in TERMINAL_STATUSES
    result = {
        "run_dir": describe_path(run_dir, root=workspace),
        "model_id": model_id,
        "job_id": job_id,
        "final_status": last.get("status"),
        "error": last.get("error"),
        "credits_before": credits_before,
        "credits_after": remaining,
        "credits_observed_delta": (credits_before - remaining)
        if credits_before is not None and remaining is not None
        else None,
        "media_path": None,
        "media_paths": [],
        "timed_out": timed_out,
    }
    if last.get("status") == "done":
        try:
            result.update(_download_media(last, run_dir, workspace=workspace))
        except (OSError, urllib.error.URLError) as exc:
            # The credits are already spent; record the failure and keep the
            # job id so `blotato poll` can retry the download later.
            result["download_error"] = str(exc)
    if timed_out:
        result["recover_with"] = f"blotato poll {describe_path(run_dir, root=workspace)}"
    _write(run_dir, "result.json", result)
    return result


def submit(
    plan_path: Path,
    *,
    workspace: Path = None,
    poll_interval: float = 5,
    poll_timeout: float = 240,
) -> dict:
    plan = json.loads(Path(plan_path).read_text())
    model = get_model(plan["model_id"])

    # An approval means nothing unless it is bound to the plan it approved.
    try:
        verify_plan_digest(plan)
    except ValueError as exc:
        # Uniform with every other refusal in this function.
        raise SystemExit(f"refusing to submit: {exc}") from None

    if model.broken:
        raise SystemExit(
            f"refusing to submit: catalog model '{model.id}' is marked BROKEN: {model.known_issues}"
        )

    ceiling = plan.get("max_credits_ceiling")
    if not ceiling or ceiling <= 0:
        raise SystemExit("refusing to submit: no positive max_credits_ceiling on the plan")
    if not plan["approval"].get("reference") or not plan["approval"].get("decided_at"):
        raise SystemExit("refusing to submit: plan has no recorded approval reference")

    run_dir = run_dir_for(plan, workspace=workspace)
    submission_path = run_dir / "submission.sanitized.json"
    if submission_path.is_file():
        # This exact plan was already paid for. Never submit it twice.
        raise SystemExit(
            f"refusing to submit: this plan was already submitted (see {describe_path(run_dir, root=workspace)}). "
            f"To fetch its result without paying again:  blotato poll {describe_path(run_dir, root=workspace)}"
        )
    run_dir.mkdir(parents=True, exist_ok=True)

    env = load_env(root=workspace)
    api_key = br.load_api_key(env=env)

    credits_before = api.get_credits(api_key)["creditsRemaining"]
    if credits_before < ceiling:
        raise SystemExit(
            f"refusing to submit: balance {credits_before} below the {ceiling}-credit ceiling"
        )

    media = _resolve_media(plan, api_key, workspace)
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

    _write(run_dir, "plan.json", plan)
    _write(run_dir, "request.sanitized.json", request_fields, api_key)

    # ---- everything above is free; this line spends credits ----
    submission = api.create_video_from_template(
        api_key,
        template_id=model.blotato_template_id,
        inputs=inputs,
        title=request_fields["title"],
        render=True,
    )
    _write(run_dir, "submission.sanitized.json", submission, api_key)
    job_id = submission["item"]["id"]

    last, poll_log = _poll_until_terminal(
        api_key,
        job_id,
        submission["item"],
        poll_interval=poll_interval,
        poll_timeout=poll_timeout,
    )
    return _finish(
        run_dir=run_dir,
        api_key=api_key,
        model_id=model.id,
        job_id=job_id,
        last=last,
        poll_log=poll_log,
        credits_before=credits_before,
        workspace=workspace,
    )


def poll(
    run_dir: Path,
    *,
    workspace: Path = None,
    poll_interval: float = 5,
    poll_timeout: float = 240,
) -> dict:
    """Resume a run that was already paid for: keep polling its job and
    download whatever it produced. Spends no credits."""
    run_dir = Path(run_dir)
    if not run_dir.is_absolute():
        run_dir = resolve_asset(run_dir, root=workspace)
    submission_path = run_dir / "submission.sanitized.json"
    if not submission_path.is_file():
        raise SystemExit(f"no submitted run at {run_dir} (expected {submission_path.name})")

    submission = json.loads(submission_path.read_text())
    job_id = submission["item"]["id"]
    plan = json.loads((run_dir / "plan.json").read_text())

    api_key = br.load_api_key(env=load_env(root=workspace))
    last = api.get_video_creation(api_key, job_id)["item"]
    last, poll_log = _poll_until_terminal(
        api_key, job_id, last, poll_interval=poll_interval, poll_timeout=poll_timeout
    )
    return _finish(
        run_dir=run_dir,
        api_key=api_key,
        model_id=plan["model_id"],
        job_id=job_id,
        last=last,
        poll_log=poll_log,
        credits_before=None,
        workspace=workspace,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Submit an approved blotato-studio plan.")
    parser.add_argument("--plan", required=True)
    args = parser.parse_args()
    print(json.dumps(submit(Path(args.plan)), indent=2))
