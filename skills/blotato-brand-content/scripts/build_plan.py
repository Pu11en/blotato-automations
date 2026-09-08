"""Build a proposed job plan for the Product Scene Placement template
against the Cinco H Ranch profile. Zero credit spend."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blotato_run as br

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_ID = "f524614b-ba01-448c-967a-ce518c52a700"  # Product Scene Placement


def load_profile() -> dict:
    profile = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "profile.json").read_text())
    claims = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "claims.json").read_text())
    profile["claims"] = claims["claims"]
    return profile


def latest_inspect_snapshot() -> Path:
    snapshots = sorted((REPO_ROOT / "outputs" / "blotato-inspect").glob("*/summary.json"))
    if not snapshots:
        raise SystemExit("no inspect snapshot found; run inspect.py first")
    return snapshots[-1].parent


def find_template(catalog: dict, template_id: str) -> dict:
    for item in catalog.get("response", {}).get("items", []):
        if item.get("id") == template_id:
            return item
    raise SystemExit(f"template {template_id} not in saved catalog snapshot")


def check_claims(scene_description: str, profile: dict) -> None:
    blocked = profile["claims"]["blocked"]
    hits = []
    for entry in blocked:
        if re.search(entry["pattern"], scene_description, re.IGNORECASE):
            hits.append(entry["id"])
    if hits:
        raise SystemExit(f"scene description hit blocked claims: {hits}")


def build_plan(*, source_asset_id: str, scene_description: str) -> dict:
    profile = load_profile()

    # Deterministic claims gate on the prompt.
    check_claims(scene_description, profile)

    # Find and validate the source asset.
    assets_by_id = {a["asset_id"]: a for a in profile["assets"]}
    asset = assets_by_id[source_asset_id]
    asset_path = REPO_ROOT / asset["path"]
    if not asset_path.is_file():
        raise SystemExit(f"asset file missing: {asset_path}")
    actual_checksum = br.hash_file(asset_path)
    if actual_checksum != asset["checksum_sha256"]:
        raise SystemExit("asset checksum drift — refuse to plan")

    # Load latest inspect snapshot and select the live template contract.
    snapshot_dir = latest_inspect_snapshot()
    catalog = json.loads((snapshot_dir / "template-catalog.sanitized.json").read_text())
    credits = json.loads((snapshot_dir / "credits.sanitized.json").read_text())
    template = find_template(catalog, TEMPLATE_ID)

    input_names = [inp.get("name") for inp in template.get("inputs", [])]
    if "productImage" not in input_names or "sceneDescription" not in input_names:
        raise SystemExit("live template inputs changed; refuse to plan")

    plan = {
        "schema_version": br.SCHEMA_VERSION,
        "brand_id": profile["brand_id"],
        "template": {
            "id": template["id"],
            "name": template.get("name"),
            "description": template.get("description"),
            "snapshot_dir": str(snapshot_dir.relative_to(REPO_ROOT)),
        },
        "operation": "image-to-video",
        "render_strategy": asset["default_render_strategy"],
        "source_asset": {
            "asset_id": asset["asset_id"],
            "path": asset["path"],
            "checksum_sha256": actual_checksum,
            "provenance": asset["provenance"],
            "rights": asset["rights"],
        },
        "prompt": {"sceneDescription": scene_description},
        "credits": {
            "starting_balance": credits.get("response", {}).get("creditsRemaining"),
            "cost_estimate": "unknown_pre_submission",
            "max_credits_ceiling": None,  # required from the user before generate-image
        },
        "approval": {
            "digest": None,
            "reference": None,
            "decided_at": None,
        },
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Digest over the immutable content of the plan (excludes approval + ceiling).
    digest_material = {
        "template_id": plan["template"]["id"],
        "operation": plan["operation"],
        "render_strategy": plan["render_strategy"],
        "source_asset_checksum": plan["source_asset"]["checksum_sha256"],
        "prompt": plan["prompt"],
    }
    plan["approval"]["digest"] = "sha256:" + hashlib.sha256(
        json.dumps(digest_material, sort_keys=True).encode()
    ).hexdigest()
    return plan


if __name__ == "__main__":
    scene = (
        "The soap bar rests on a weathered oak plank on the porch of a Texas homestead, "
        "warm late-afternoon sunlight, dried herb sprigs and a cast-iron jar nearby, "
        "shallow depth of field, calm and grounded mood."
    )
    plan = build_plan(source_asset_id="texas-campfire-soap-front", scene_description=scene)
    plan_dir = REPO_ROOT / "outputs" / "blotato-plans"
    plan_dir.mkdir(parents=True, exist_ok=True)
    plan_path = plan_dir / f"{plan['approval']['digest'].replace('sha256:', '')[:12]}.json"
    plan_path.write_text(json.dumps(plan, indent=2, sort_keys=True))
    print(json.dumps({"plan_path": str(plan_path.relative_to(REPO_ROOT)), "plan": plan}, indent=2))
