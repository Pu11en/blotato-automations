"""Blotato template: AI Video with AI Voice (video).

NEVER SUBMITTED LIVE. Schema captured from the account's authenticated
GET /v2/videos/templates response on 2026-09-08, but no generation call
has been tried against it. Per the plan-before-spend rule, treat the
first real use of this entry as a fresh live test with a small credit
ceiling, not as a proven technique.
"""
from ..types import GenerationPlane, ModelEntry, SettingField


def build_inputs(plane: GenerationPlane) -> dict:
    refs = plane.media.get("reference", [])
    scenes = []
    for item in refs:
        scenes.append({"mediaSource": item.url, "script": item.caption or ""})
    return {
        "scenes": scenes,
        "enableVoiceover": plane.settings.get("enableVoiceover", True),
    }


ENTRY = ModelEntry(
    id="ai-video-with-ai-voice",
    blotato_template_id="/base/v2/ai-story-video/5903fe43-514d-40ee-a060-0d6628c5f8fd/v1",
    surface="video",
    label="AI Video with AI Voice",
    description=(
        "Multi-scene video; each scene takes an uploaded image/video or an AI-image "
        "prompt, plus a voiceover script line read aloud. Caution: Pinterest research "
        "in this repo found ~85% of viewers watch muted, so a voiceover-dependent video "
        "may underperform there specifically -- fine for platforms where audio is expected."
    ),
    roles={"reference": (1, 20)},
    settings={
        "enableVoiceover": SettingField(kind="boolean", default=True),
    },
    build_inputs=build_inputs,
    known_issues=(
        "Never submitted live -- schema is from the templates listing only. Verify with "
        "a small credit ceiling before trusting this entry.",
    ),
    broken=False,
    verified_at=None,
)
