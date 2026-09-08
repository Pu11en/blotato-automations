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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blotato_run as br

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


def draw_caption(im: Image.Image, text: str) -> Image.Image:
    im = im.convert("RGBA")
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = 54
    font = ImageFont.truetype(FONT_PATH, font_size)
    max_width = im.width - 120
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
    band_top = im.height - band_h - 60

    draw.rectangle([0, band_top, im.width, band_top + band_h], fill=(10, 10, 15, 190))

    y = band_top + band_pad
    for line, lh, lw in zip(lines, line_heights, line_widths):
        x = (im.width - lw) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += lh + line_gap

    return Image.alpha_composite(im, overlay).convert("RGB")


def render(*, brief_pack: dict, out_dir: Path) -> dict:
    profile = load_cinco_profile()
    brief = brief_pack["brief"]
    assets_state = {a["id"]: a for a in brief_pack["assets"]}

    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(exist_ok=True)

    frame_paths = []
    concat_lines = []
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

        im = Image.open(source_path).convert("RGB")
        im = crop_to_frame(im)
        im = draw_caption(im, shot["overlay"])
        frame_path = frames_dir / f"frame{i}.jpg"
        im.save(frame_path, quality=92)
        frame_paths.append(frame_path)
        duration = shot["end"] - shot["start"]
        concat_lines.append(f"file '{frame_path.name}'\nduration {duration}\n")
    # ffconcat requires the last file repeated without a duration line.
    concat_lines.append(f"file '{frame_paths[-1].name}'\n")

    concat_path = frames_dir / "concat.txt"
    concat_path.write_text("".join(concat_lines))

    video_path = out_dir / "pinterest-pin.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_path),
            "-vf", "fps=30,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(video_path),
        ],
        check=True,
        capture_output=True,
    )

    result = {
        "engine": "local (Pillow + ffmpeg)",
        "reason": "Blotato Image Slideshow with Text Overlays template was broken as of 2026-09-08 (blank captions, no mediaUrl)",
        "credits_spent": 0,
        "video_path": str(video_path.relative_to(REPO_ROOT)),
        "video_checksum_sha256": br.hash_file(video_path),
        "frame_paths": [str(p.relative_to(REPO_ROOT)) for p in frame_paths],
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
