---
name: blotato-studio
description: General-purpose, catalog-driven tool for making images and videos through Blotato — not tied to any one brand or project. Lists available Blotato techniques (each verified live or explicitly flagged unverified/broken), builds a reviewable zero-cost plan for a chosen technique, and submits exactly one approved, credit-bounded generation call. Add a new technique by adding one small catalog file, not a new script.
---

# Blotato Studio

A reusable "pick a technique, plan it, run it" tool for Blotato image/video generation. Built after repeatedly writing one-off scripts per use case — this replaces that pattern with a small declarative catalog (one file per technique) plus one generic plan/submit flow, following the architecture of the open-source [`open-higgsfield`](https://github.com/wide-trace/open-higgsfield) project (MIT), adapted to Blotato as the sole backend.

## Before doing anything: list the catalog

```python
import sys; sys.path.insert(0, "skills/blotato-studio/scripts")
from catalog import list_models
for m in list_models():
    print(m.id, "BROKEN" if m.broken else ("unverified" if not m.verified_at else "verified " + m.verified_at), "-", m.label)
```

Every entry states honestly whether it's `verified` (we ran it live and confirmed what it actually does), `unverified` (schema captured from Blotato's template listing, never submitted), or `broken` (we ran it and it doesn't work as documented — do not use). Never assume a template works because its Blotato-side description sounds right; only trust `verified_at`.

## The three steps

1. **`scripts/plan.py`** — zero cost. Takes a catalog `model_id`, a prompt, and media (local file paths or URLs). Validates the chosen model's role requirements (e.g. exactly one reference image), checksums local assets, and writes a `plan.json` with a stable `approval_digest`. Refuses nothing here costs credits, but warns loudly if the model is `broken`.
2. **Human sets `max_credits_ceiling` and records an approval** — edit the plan's `max_credits_ceiling` (a positive number) and `approval.reference`/`approval.decided_at` fields. This is a deliberate manual step, not automated, because approving a spend must be a real human decision at the time of that specific plan.
3. **`scripts/submit.py`** — spends credits. Refuses to run if: the model is `broken`, there's no positive `max_credits_ceiling`, there's no recorded approval, the current balance is below the ceiling, any local asset's checksum drifted since planning, or the request would touch a publishing/external-credential field. On success, downloads whatever the job produced — an image, a set of images, or a video — and records the observed credit delta.

## Adding a new technique

Add a file under `scripts/catalog/templates/`, following the shape of `product_scene_placement.py`. Every entry needs:
- `blotato_template_id` — the real id from an authenticated `GET /v2/videos/templates?fields=id,name,description,inputs` call (see `skills/blotato-brand-content/scripts/blotato_inspect.py` for the zero-cost inspect action)
- `roles` — what media it needs and how many
- `build_inputs(plane)` — turns the generic prompt/media/settings into Blotato's actual `inputs` shape for that specific template
- `verified_at` — only set this after you've actually submitted a live call and confirmed the output matches the template's documented behavior; leave `None` otherwise
- `known_issues`/`broken` — record what you actually observed, not what you assumed. See `image_slideshow_text_overlays.py` for how a real, live-discovered bug gets encoded so nobody wastes credits repeating the same test.

## Prompt technique reference

`references/prompt-formulas.md` has a researched, source-cited prompt formula for product-in-scene generation (from the open-source `amazon-product-studio` project). Use it as a starting structure, not a guarantee — Blotato's own product-placement template was found to shift color/identity versus the real source photo even with a disciplined prompt (see `product_scene_placement.py`'s `known_issues`).

## What this tool does not do

- No publishing, scheduling, or social-account access, ever.
- No non-Blotato model providers.
- No automatic retries on failure/timeout.
- No credential ever passed as an argument; `BLOTATO_API_KEY` is read from the environment only (via the shared `scripts/blotato/runner.py`).
