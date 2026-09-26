"""Blotato template: AI Video with AI Voice (video).

Multi-scene narrated video. Each scene is an image plus a line of script
that gets read aloud, and Blotato burns in captions.

A scene's `mediaSource` accepts **either** a media URL **or** a plain text
image prompt -- the live template listing's own default uses prompts ("A
serene winter landscape with snow-covered mountains..."). The earlier
version of this entry required uploaded reference media and so could not
reach the prompt-driven path at all, which is the one that needs no assets.

Two ways to describe scenes:

1. **No reference media** -- the prompt is split into scenes on lines
   containing only `---`. Within a scene, `::` separates the image prompt
   from the narration; with no `::` the same text is used for both::

       A cluttered desk at night, harsh lamp light :: Most creators start here.
       ---
       The same desk, clean, one warm lamp :: Ten minutes of setup changes everything.

2. **With `--reference`** -- one scene per reference item, using each
   item's caption as its narration line.
"""
from ..types import GenerationPlane, ModelEntry, SettingField

SCENE_SEPARATOR = "---"
SCRIPT_SEPARATOR = "::"

VOICES = (
    "Alice (British, confident)",
    "Aria (American, expressive)",
    "Bill (American, trustworthy)",
    "Brian (American, deep)",
    "Callum (Transatlantic, intense)",
    "Charlie (Australian, natural)",
)

IMAGE_MODELS = (
    "fal-ai/nano-banana",
    "replicate/black-forest-labs/flux-schnell",
    "replicate/black-forest-labs/flux-dev",
    "replicate/black-forest-labs/flux-1.1-pro",
    "replicate/recraft-ai/recraft-v3",
)


def parse_scenes(prompt: str) -> list:
    """Split a prompt into (image_source, script) pairs."""
    scenes = []
    for block in prompt.split(f"\n{SCENE_SEPARATOR}\n"):
        block = block.strip()
        if not block:
            continue
        if SCRIPT_SEPARATOR in block:
            media_source, _, script = block.partition(SCRIPT_SEPARATOR)
            scenes.append((media_source.strip(), script.strip()))
        else:
            scenes.append((block, block))
    return scenes


def build_inputs(plane: GenerationPlane) -> dict:
    refs = plane.media.get("reference", [])
    if refs:
        scenes = [{"mediaSource": item.url, "script": item.caption or ""} for item in refs]
    else:
        scenes = [{"mediaSource": source, "script": script} for source, script in parse_scenes(plane.prompt)]

    settings = plane.settings
    return {
        "scenes": scenes,
        "enableVoiceover": settings.get("enableVoiceover", True),
        "voiceName": settings.get("voiceName", "Brian (American, deep)"),
        "aiImageModel": settings.get("aiImageModel", "fal-ai/nano-banana"),
        "animateAiImages": settings.get("animateAiImages", False),
        "captionPosition": settings.get("captionPosition", "center"),
        "highlightColor": settings.get("highlightColor", "#FFFF00"),
        "transition": settings.get("transition", "none"),
        "aspectRatio": settings.get("aspectRatio", "9:16"),
        "trimToVoiceover": settings.get("trimToVoiceover", True),
    }


ENTRY = ModelEntry(
    id="ai-video-with-ai-voice",
    blotato_template_id="/base/v2/ai-story-video/5903fe43-514d-40ee-a060-0d6628c5f8fd/v1",
    surface="video",
    label="AI Video with AI Voice",
    description=(
        "Multi-scene narrated video with burned-in captions. Each scene is an AI "
        "image prompt (or an uploaded image/video) plus a line of script read aloud. "
        "Separate scenes with a line containing only '---', and split image prompt "
        "from narration with '::'. Caution: this repo's Pinterest research found ~85% "
        "of viewers watch muted, so a voiceover-dependent video may underperform "
        "there specifically -- fine where audio is expected."
    ),
    roles={"reference": (0, 20)},
    settings={
        "enableVoiceover": SettingField(kind="boolean", default=True),
        "voiceName": SettingField(kind="enum", values=VOICES, default="Brian (American, deep)"),
        "aiImageModel": SettingField(kind="enum", values=IMAGE_MODELS, default="fal-ai/nano-banana"),
        "animateAiImages": SettingField(kind="boolean", default=False),
        "captionPosition": SettingField(kind="enum", values=("top", "center", "bottom"), default="center"),
        "highlightColor": SettingField(kind="text", default="#FFFF00"),
        "transition": SettingField(kind="enum", values=("none", "fade", "slide", "zoom"), default="none"),
        "aspectRatio": SettingField(kind="enum", values=("16:9", "1:1", "4:5", "9:16"), default="9:16"),
        "trimToVoiceover": SettingField(kind="boolean", default=True),
    },
    build_inputs=build_inputs,
    known_issues=(
        "Voiceover length drives duration: the 2026-09-26 run rendered 3 scenes as an "
        "11.5s 1080x1920 clip with trimToVoiceover on, so scene count alone does not "
        "predict length -- script length does.",
        "Scene images are generated, not sourced. Nothing in the output is a real "
        "photograph of anything, even when the prompt names a real place or product.",
    ),
    broken=False,
    # Live run 2026-09-26: 3 prompt-driven scenes, no uploaded media, voiceover on.
    # Returned a 17 MB mp4, 11.46s, 1080x1920, with both a video and an audio track.
    verified_at="2026-09-26",
    observed_credits=45,
)
