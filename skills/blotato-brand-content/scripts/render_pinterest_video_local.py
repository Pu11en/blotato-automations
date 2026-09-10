"""Local, zero-credit renderer for a Pinterest brief's video variant.

Used because Blotato's "Image Slideshow with Text Overlays" template was
found broken on 2026-09-08 (see outputs/blotato-runs diagnostic runs):
text overlays rendered as blank white boxes and no mediaUrl was ever
produced, only per-slide static images. This renderer reuses the same
exact-asset guarantee (the real product photo is never altered by a
generative model) but does the crop/caption/assembly locally with
Pillow + ffmpeg, which are both deterministic and free.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from scripts.blotato import runner as br

REPO_ROOT = Path(__file__).resolve().parents[3]
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FRAME_SIZE = (1080, 1920)  # 9:16


def load_brief_pack(run_dir: Path, brief_key: str) -> dict:
    return json.loads((run_dir / "briefs" / brief_key / "brief.json").read_text())


def load_cinco_profile() -> dict:
    profile = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "profile.json").read_text())
    claims = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "claims.json").read_text())
    profile["claims"] = claims["claims"]
    return profile


def check_claims(text: str, profile: dict) -> None:
    hits = [e["id"] for e in profile["claims"]["blocked"] if re.search(e["pattern"], text, re.IGNORECASE)]
    if hits:
        raise SystemExit(f"caption text hit blocked claims: {hits} :: {text!r}")


def crop_to_frame(im: Image.Image) -> Image.Image:
    target_w, target_h = FRAME_SIZE
    target_ratio = target_w / target_h
    w, h = im.size
    ratio = w / h
    if ratio > target_ratio:
        new_w = int(h * target_ratio)
        x0 = (w - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / target_ratio)
        y0 = (h - new_h) // 2
        im = im.crop((0, y0, w, y0 + new_h))
    return im.resize(FRAME_SIZE, Image.LANCZOS)


def caption_layer(text: str) -> Image.Image:
    """A transparent RGBA overlay holding only the caption band, sized to
    FRAME_SIZE. Kept separate from the photo so captions stay perfectly
    fixed/legible while the photo underneath moves (Ken Burns)."""
    overlay = Image.new("RGBA", FRAME_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = 54
    font = ImageFont.truetype(FONT_PATH, font_size)
    max_width = FRAME_SIZE[0] - 120
    wrapped = textwrap.fill(text, width=28)
    lines = wrapped.split("\n")

    while True:
        line_heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
        line_widths = [draw.textbbox((0, 0), line, font=font)[2] for line in lines]
        if max(line_widths, default=0) <= max_width or font_size <= 28:
            break
        font_size -= 4
        font = ImageFont.truetype(FONT_PATH, font_size)

    line_gap = 12
    total_h = sum(line_heights) + line_gap * (len(lines) - 1)
    band_pad = 40
    band_h = total_h + band_pad * 2
    band_top = FRAME_SIZE[1] - band_h - 60

    draw.rectangle([0, band_top, FRAME_SIZE[0], band_top + band_h], fill=(10, 10, 15, 190))

    y = band_top + band_pad
    for line, lh, lw in zip(lines, line_heights, line_widths):
        x = (FRAME_SIZE[0] - lw) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += lh + line_gap

    return overlay


def crop_to_oversized_frame(im: Image.Image, oversize: float = 1.15) -> Image.Image:
    """Crop/resize to FRAME_SIZE's aspect ratio but oversized, so zoompan
    has room to pan without ever showing empty space at the edges."""
    target_w = int(FRAME_SIZE[0] * oversize)
    target_h = int(FRAME_SIZE[1] * oversize)
    target_ratio = target_w / target_h
    w, h = im.size
    ratio = w / h
    if ratio > target_ratio:
        new_w = int(h * target_ratio)
        x0 = (w - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / target_ratio)
        y0 = (h - new_h) // 2
        im = im.crop((0, y0, w, y0 + new_h))
    return im.resize((target_w, target_h), Image.LANCZOS)


FPS = 30


def render_shot_clip(
    *, source_path: Path, caption_text: str, duration: float, clip_path: Path, zoom_out: bool
) -> None:
    im = Image.open(source_path).convert("RGB")
    im = crop_to_oversized_frame(im)
    bg_path = clip_path.with_suffix(".bg.jpg")
    im.save(bg_path, quality=95)

    caption_path = clip_path.with_suffix(".caption.png")
    caption_layer(caption_text).save(caption_path)

    nframes = max(1, round(duration * FPS))
    ow, oh = im.size
    # Zoom between 1.0 and ~1.12 across the shot; ping-pong direction per
    # shot for a little variety instead of every shot zooming the same way.
    per_frame = 0.12 / nframes
    if zoom_out:
        zoom_expr = f"if(eq(on,1),1.12,zoom-{per_frame:.6f})"
    else:
        zoom_expr = f"min(zoom+{per_frame:.6f},1.12)"

    filter_complex = (
        f"[0:v]scale={ow}:{oh},zoompan=z='{zoom_expr}':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={FRAME_SIZE[0]}x{FRAME_SIZE[1]}:fps={FPS}[bg];"
        f"[bg][1:v]overlay=0:0:shortest=1[out]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(bg_path),
            "-loop", "1", "-i", str(caption_path),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-t", str(duration),
            "-r", str(FPS),
            "-pix_fmt", "yuv420p",
            "-c:v", "libx264",
            str(clip_path),
        ],
        check=True,
        capture_output=True,
    )


def render(*, brief_pack: dict, out_dir: Path) -> dict:
    profile = load_cinco_profile()
    brief = brief_pack["brief"]
    assets_state = {a["id"]: a for a in brief_pack["assets"]}

    out_dir.mkdir(parents=True, exist_ok=True)
    clips_dir = out_dir / "clips"
    clips_dir.mkdir(exist_ok=True)

    clip_paths = []
    for i, shot in enumerate(brief["shots"]):
        check_claims(shot["overlay"], profile)
        asset_id = shot["asset_ids"][0]
        asset = assets_state[asset_id]
        if not asset["ready"]:
            raise SystemExit(f"asset {asset_id} is not ready (approved/rights/checksum)")
        source_path = REPO_ROOT / asset["path"]
        actual = br.hash_file(source_path)
        if actual != asset["sha256"]:
            raise SystemExit(f"checksum drift on {asset_id}; refuse to render")

        duration = shot["end"] - shot["start"]
        clip_path = clips_dir / f"shot{i}.mp4"
        render_shot_clip(
            source_path=source_path,
            caption_text=shot["overlay"],
            duration=duration,
            clip_path=clip_path,
            zoom_out=(i % 2 == 1),
        )
        clip_paths.append(clip_path)

    concat_path = clips_dir / "concat.txt"
    concat_path.write_text("".join(f"file '{p.name}'\n" for p in clip_paths))

    video_path = out_dir / "pinterest-pin.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(video_path),
        ],
        check=True,
        capture_output=True,
    )

    result = {
        "engine": "local (Pillow + ffmpeg, Ken Burns zoom per shot)",
        "reason": "Blotato Image Slideshow with Text Overlays template was broken as of 2026-09-08 (blank captions, no mediaUrl)",
        "credits_spent": 0,
        "video_path": str(video_path.relative_to(REPO_ROOT)),
        "video_checksum_sha256": br.hash_file(video_path),
        "clip_paths": [str(p.relative_to(REPO_ROOT)) for p in clip_paths],
        "duration_seconds": brief["duration_seconds"],
    }
    (out_dir / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    run_dir = REPO_ROOT / "outputs" / "pinterest" / "research-20260908"
    brief_pack = load_brief_pack(run_dir, "cand-after-the-harvest-video-pin-v1-v1")
    out_dir = REPO_ROOT / "outputs" / "blotato-runs" / (br.new_run_id("cinco-h-ranch") + "-local-render")
    result = render(brief_pack=brief_pack, out_dir=out_dir)
    print(json.dumps(result, indent=2))
