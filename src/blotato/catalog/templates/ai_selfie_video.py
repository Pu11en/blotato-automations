"""Blotato template: AI Selfie Talking Video with Consistent Character.

BROKEN as of 2026-09-19 -- do not use. Listed only so nobody rediscovers
this at 400 credits a scene.

It does hold one character across scenes (same face, clothes and props,
indoors and out), but a live 2-scene run cost 800 credits and:

- ignored the character that was described -- asked for a weathered
  detective in his fifties in a brown overcoat, got a man in his twenties
  in fantasy gear;
- wrote gibberish text into the frame.

At 400 per scene that is roughly 5.7x `ai-video-with-ai-voice` for a worse
match. The cheap and exact answer to the same-face problem is
`ai-video-with-ai-voice` with the character still **uploaded** as each
scene's media, which costs nothing and reproduces the image exactly.

Measured and verdicted in the youtube-money repo, 2026-09-19.
"""
from ..types import GenerationPlane, ModelEntry, SettingField

STYLES = (
    "realistic", "cartoon", "anime", "watercolor", "oil-painting",
    "sketch", "cyberpunk", "fantasy", "minimalist",
)


def build_inputs(plane: GenerationPlane) -> dict:
    refs = plane.media.get("reference", [])
    scenes = [{"script": item.caption or ""} for item in refs] or [
        {"script": line.strip()} for line in plane.prompt.split("\n---\n") if line.strip()
    ]
    return {
        "scenes": scenes,
        "style": plane.settings.get("style", "realistic"),
        "characterDescription": plane.settings.get("characterDescription", ""),
        "aspectRatio": plane.settings.get("aspectRatio", "9:16"),
    }


ENTRY = ModelEntry(
    id="ai-selfie-video",
    blotato_template_id="/base/v2/ai-selfie-video/57f5a565-fd17-458b-be43-4a2d8ccaca75/v1",
    surface="video",
    label="AI Selfie Talking Video with Consistent Character",
    description=(
        "Talking video holding one character across scenes. BROKEN: ignores the "
        "character description and renders gibberish on-screen text, at 400 credits "
        "per scene. Use ai-video-with-ai-voice with the character image uploaded "
        "instead -- that path is free and reproduces the image exactly."
    ),
    roles={"reference": (0, 20)},
    settings={
        "style": SettingField(kind="enum", values=STYLES, default="realistic"),
        "characterDescription": SettingField(kind="text", default=""),
        "aspectRatio": SettingField(kind="enum", values=("16:9", "9:16", "1:1"), default="9:16"),
    },
    build_inputs=build_inputs,
    known_issues=(
        "BROKEN 2026-09-19: ignored the described character (a weathered detective in "
        "his fifties in a brown overcoat came back as a man in his twenties in fantasy "
        "gear) and wrote gibberish text into the frame.",
        "400 credits per scene -- a 2-scene run cost 800. Roughly 5.7x "
        "ai-video-with-ai-voice for a worse result.",
    ),
    broken=True,
    verified_at="2026-09-19",
    observed_credits=400,
    cost_note="Per scene. Measured from the live balance: 800 for 2 scenes (youtube-money).",
)
