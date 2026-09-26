"""The approval digest: what a human's credit approval is actually bound to.

`plan` computes it and `submit` recomputes it. If they disagree, the plan's
content changed after it was approved and the approval no longer describes
what would run, so submit refuses.

Only the fields that decide *what gets generated* go into the digest --
model, prompt, media, settings. `max_credits_ceiling` and `approval` are
deliberately excluded, because `blotato approve` writes those after the
digest exists and must not invalidate it.
"""
from __future__ import annotations

import hashlib
import json

DIGEST_FIELDS = ("model_id", "prompt", "media", "settings")


def compute_approval_digest(*, model_id: str, prompt: str, media: dict, settings: dict) -> str:
    material = {
        "model_id": model_id,
        "prompt": prompt,
        "media": media,
        "settings": settings,
    }
    encoded = json.dumps(material, sort_keys=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def digest_for_plan(plan: dict) -> str:
    try:
        return compute_approval_digest(**{field: plan[field] for field in DIGEST_FIELDS})
    except KeyError as exc:
        raise ValueError(f"plan is missing the field {exc}; rebuild it with `blotato plan`") from None


def verify_plan_digest(plan: dict) -> None:
    """Raise ValueError unless the plan still matches its recorded digest."""
    recorded = plan.get("approval_digest")
    if not recorded:
        raise ValueError("plan has no approval_digest; rebuild it with `blotato plan`")
    expected = digest_for_plan(plan)
    if recorded != expected:
        raise ValueError(
            "plan contents do not match its approval_digest -- the plan was edited "
            f"after it was created (recorded {recorded[:23]}..., actual {expected[:23]}...). "
            "Re-run `blotato plan` and approve the new plan."
        )
