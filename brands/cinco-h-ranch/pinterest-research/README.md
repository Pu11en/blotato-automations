# Cinco H Ranch Pinterest research inputs (2026-09-08)

Authored research inputs for the `pinterest-research` skill's collect → rank → brief pipeline. These are tracked because they're real editorial work (sourced evidence and creative judgment), unlike the regenerable `outputs/pinterest/research-*` run directory, which stays git-ignored.

- `manual-signals-2026-09-08.json` — three editorial (not measured-demand) signals: Pinterest's own published video-vs-static engagement benchmarks, the ~85%-watch-muted finding, and a competitor precedent for the homestead/ancestral-tallow angle. No live Pinterest API/OpenCLI access was configured, so this is manual, source-cited evidence, not a demand time series.
- `candidates-2026-09-08.json` — one scored candidate (`cand-after-the-harvest-video-pin-v1`) built from that evidence. Ranked `exploratory` at 7/10 — honest, since there's no measured demand signal or reviewed reference Pin, only editorial evidence and product/visual fit.
- `brief-input-2026-09-08.json` — the resulting creative brief: a 12-second, 9:16, muted-first, caption-driven video using the real After the Harvest product photo across all 4 shots, factual captions traced to two approved product-page claims.

Reproduce the run with:
```sh
python3 scripts/pinterest/cli.py collect --run outputs/pinterest/research-20260908 --profile assets/brands/cinco-h-ranch/pinterest.json --mode manual --signals brands/cinco-h-ranch/pinterest-research/manual-signals-2026-09-08.json
python3 scripts/pinterest/cli.py rank --run outputs/pinterest/research-20260908 --input brands/cinco-h-ranch/pinterest-research/candidates-2026-09-08.json
python3 scripts/pinterest/cli.py brief --run outputs/pinterest/research-20260908 --input brands/cinco-h-ranch/pinterest-research/brief-input-2026-09-08.json
```

## Production note

The brief was executed via `skills/blotato-brand-content/scripts/render_pinterest_video_local.py`, **not** Blotato's "Image Slideshow with Text Overlays" template. That template was tested live on 2026-09-08 and found broken: it correctly crops/resizes the real uploaded photo but never renders the `textOverlay` text (blank white boxes) and never produces a `mediaUrl` (only per-slide static `imageUrls`), even for a single slide. The local renderer (Pillow + ffmpeg) reuses the same real, unaltered photo and produces a correct 1080x1920 12s h264 video at zero Blotato credit cost. Revisit the Blotato template periodically in case it's fixed upstream.
