"""Blotato template: Image Slideshow with Text Overlays (video).

BROKEN as of 2026-09-08 -- do not use for production. Confirmed with 3
separate live calls (a 4-slide run and two single-slide diagnostics):
`textOverlay` renders as a blank white box with no text drawn, and the
job never produces `mediaUrl` -- only static per-slide `imageUrls`, even
with a single slide. The real photo crop/resize itself works correctly.

Working fallback: skills/blotato-brand-content/scripts/render_pinterest_video_local.py
does the same job locally (Pillow + ffmpeg) for zero credits. Retest this
template periodically in case Blotato fixes it, then flip `broken=False`.
"""
from ..types import GenerationPlane, ModelEntry, SettingField


def build_inputs(plane: GenerationPlane) -> dict:
    slides = [
        {"imageSource": item.url, "textOverlay": item.caption or ""}
        for item in plane.media["reference"]
    ]
    settings = plane.settings
    return {
        "slides": slides,
        "aspectRatio": settings.get("aspectRatio", "9:16"),
        "slideDuration": settings.get("slideDuration", 3),
        "transition": settings.get("transition", "none"),
        "textPosition": settings.get("textPosition", "bottom"),
        "textStyle": settings.get("textStyle", "elegant"),
        "textColor": settings.get("textColor", "#FFFFFF"),
    }


ENTRY = ModelEntry(
    id="image-slideshow-text-overlays",
    blotato_template_id="/base/v2/image-slideshow/5903b592-1255-43b4-b9ac-f8ed7cbf6a5f/v1",
    surface="video",
    label="Image Slideshow with Text Overlays",
    description="Multi-slide slideshow video with a per-slide caption band.",
    roles={"reference": (1, 50)},
    settings={
        "aspectRatio": SettingField(kind="enum", values=("16:9", "1:1", "4:5", "9:16"), default="9:16"),
        "slideDuration": SettingField(kind="range", min=1, max=10, default=3),
        "transition": SettingField(kind="enum", values=("none", "fade", "slide", "zoom"), default="none"),
        "textPosition": SettingField(kind="enum", values=("top", "center", "bottom"), default="bottom"),
        "textStyle": SettingField(kind="enum", values=("minimal", "elegant", "modern"), default="elegant"),
    },
    build_inputs=build_inputs,
    known_issues=(
        "BROKEN 2026-09-08: textOverlay renders as a blank box, no text drawn; job "
        "never produces mediaUrl, only static per-slide imageUrls, even for one slide. "
        "Use render_pinterest_video_local.py (Pillow+ffmpeg) instead until this is fixed.",
    ),
    broken=True,
    verified_at="2026-09-08",
)
