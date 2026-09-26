---
name: blotato-studio
description: General-purpose tool for making images and videos through Blotato — not tied to any one brand or project. Lists available Blotato techniques (each verified live or explicitly flagged unverified/broken), builds a reviewable zero-cost plan for a chosen technique, and submits exactly one approved, credit-bounded generation call. Add a new technique by adding one small catalog file, not a new script.
---

# Blotato Studio

Drive this through the installed `blotato` CLI. Do not import the package's internals or write a one-off script per use case — that is the pattern this tool exists to replace.

If `blotato` is not on PATH: `python -m pip install -e <path-to-blotato-automations>`.

## Before doing anything: list the catalog

```bash
blotato list              # add --json for machine-readable output
blotato show <model-id>   # media roles, settings, known issues
```

Every entry states honestly whether it is `verified <date>` (we ran it live and confirmed what it actually does), `unverified` (schema captured from Blotato's template listing, never submitted), or `BROKEN` (we ran it and it does not work as documented). Never assume a template works because its Blotato-side description sounds right; only trust `verified_at`. Report an entry's status to the user before spending their credits on it.

## The three steps

1. **`blotato plan`** — zero cost. Takes a catalog model id, a prompt, and media (local paths or URLs). Validates the model's role requirements (e.g. exactly one reference image), checksums local assets, and writes a `plan.json` with a stable `approval_digest`.

   ```bash
   blotato plan --model product-scene-placement \
     --prompt "<the scene>" --reference <path-or-url> --out plan.json
   ```

   Repeat `--reference` for multi-image roles; `--start`/`--end` for frame roles; `--setting name=value` for a model's settings (validated against that model's declared settings).

2. **`blotato approve`** — the human sets the ceiling. Ask the user for a credit ceiling and what to record as the approval reference, then run it with their answer. **Do not invent a ceiling or an approval reference.** Approving a spend is a real decision by a real person about that specific plan.

   ```bash
   blotato approve plan.json --max-credits <N> --reference "<who approved, where recorded>"
   ```

3. **`blotato submit`** — spends credits. Refuses to run if the model is `broken`, there is no positive ceiling, there is no recorded approval, the balance is below the ceiling, a local asset's checksum drifted since planning, or the request would touch a publishing/external-credential field. On success it downloads whatever the job produced — an image, a set of images, or a video — and records the observed credit delta under `outputs/blotato-studio-runs/<digest>/`.

`blotato balance` (free) before step 3 is worth it if the user is near their limit.

## Paths

Relative paths resolve against the workspace: `--workspace <dir>`, else `$BLOTATO_WORKSPACE`, else the current directory. In a fresh Discord turn cwd is not preserved, so pass `--workspace` or absolute paths.

## Adding a new technique

Add one file under `src/blotato/catalog/templates/`, following the shape of `product_scene_placement.py`. Every entry needs:

- `blotato_template_id` — the real id from `blotato inspect` (zero-cost; snapshots the live template catalog)
- `roles` — what media it needs and how many
- `build_inputs(plane)` — turns the generic prompt/media/settings into Blotato's actual `inputs` shape for that specific template
- `verified_at` — only set this after you have actually submitted a live call and confirmed the output matches the documented behavior; leave `None` otherwise
- `known_issues`/`broken` — record what you observed, not what you assumed. See `image_slideshow_text_overlays.py` for how a real, live-discovered bug gets encoded so nobody wastes credits repeating the test.

The registry auto-discovers the file; no other code changes, and `blotato list` picks it up immediately. Add a case to `tests/studio/` covering its role validation.

## Prompt technique reference

`references/prompt-formulas.md` has a researched, source-cited prompt formula for product-in-scene generation (from the open-source `amazon-product-studio` project). Use it as a starting structure, not a guarantee — Blotato's own product-placement template was found to shift color/identity versus the real source photo even with a disciplined prompt (see `product_scene_placement.py`'s `known_issues`).

## What this tool does not do

- No publishing, scheduling, or social-account access, ever.
- No non-Blotato model providers.
- No automatic retries on failure/timeout.
- No credential ever passed as an argument; `BLOTATO_API_KEY` is read from the environment or the workspace `.env` only.
