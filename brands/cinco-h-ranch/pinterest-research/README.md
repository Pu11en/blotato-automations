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

## Round 2: live Pinterest reference data (same day)

The user enabled OpenCLI browser-bridge access (`jackwener/opencli`, installed pinned at the reviewed commit `v1.8.8`/npm `1.8.7` since npm hadn't published `1.8.8` yet, in `~/.local/share/opencli-tool`, outside this repo). `PINTEREST_OPENCLI_BIN` is set in the local `.env`. This unlocked real, read-only reference-Pin collection (Pinterest Trends API access is still separate and still requires `PINTEREST_ACCESS_TOKEN`, not yet configured).

Live run: `outputs/pinterest/research-live-20260908` — 29 real reference Pins across the profile's 3 queries (`tallow soap`, `handmade soap`, `soap gifts`), within the pilot's 5-query/10-pins-per-query cap. Finding: generic `tallow soap`/`handmade soap` search is dominated by DIY recipe/tutorial pins (people wanting to *make* soap), not finished-product buyers. The `soap gifts` query instead surfaced genuine commercial-intent competitor listings — most directly a `hearthropic` "Tallow Soap Gift Set" with a bamboo rack and bag.

- `manual-signals-2026-09-08b-soap-gifts.json` — one editorial signal documenting that finding, citing the real reference Pins as evidence.
- `candidates-2026-09-08b-soap-gifts.json` — `cand-after-the-harvest-gift-pin-v1`, keyword `soap gifts`, referencing 5 real Pin IDs. Still `exploratory` (7/10) since Trends demand data is still unavailable, but "No reference Pins reviewed" is resolved — real reviewed references now back the concept.
- `brief-input-2026-09-08b-gift.json` — same real photo and format, captions reframed toward gifting ("A small-batch gift with a real story...") instead of the original process-focused copy.

Reproduce with the same three-step pattern, pointed at `outputs/pinterest/research-live-20260908` and `--mode live --live` for the initial `collect` (requires `PINTEREST_OPENCLI_BIN` set and Chrome logged into Pinterest with the Browser Bridge extension connected).
