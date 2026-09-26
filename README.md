# blotato-automations

A command-line tool for generating images and videos through the [Blotato](https://blotato.com) API.

Pick a technique from a catalog, build a plan for free, approve a credit ceiling, then spend credits on exactly one bounded call. Nothing here publishes, schedules, or touches a social account.

## Quickstart

```bash
git clone https://github.com/Pu11en/blotato-automations.git
cd blotato-automations
python -m pip install -e .
```

Set your key (either works; an exported variable wins over the file):

```bash
export BLOTATO_API_KEY=...        # or put BLOTATO_API_KEY=... in <workspace>/.env
blotato balance                   # free: confirms the key works
```

Then, from **any** directory you want to work in:

```bash
# 1. see what techniques exist, and which are actually proven
blotato list

# 2. build a plan — free, offline, spends nothing
blotato plan \
  --model product-scene-placement \
  --prompt "The soap bar on a sunlit rustic wooden shelf, shallow depth of field." \
  --reference assets/product.jpg \
  --out plan.json

# 3. a human sets the spend ceiling — this step is deliberately not automated
blotato approve plan.json --max-credits 25 --reference "me, 2026-09-26"

# 4. spend credits on one call, poll it, download the result
blotato submit plan.json
```

`submit` writes everything it did to `outputs/blotato-studio-runs/<digest>/` — the plan, the sanitized request, the poll log, the observed credit delta, and every downloaded asset with its checksum.

If a job is still rendering when the poll timeout expires, the credits are already spent, so `submit` records the job id and tells you to run `blotato poll <run-dir>` to collect the result later. Re-running `submit` on a plan that was already paid for is refused rather than charged twice.

## Commands

| Command | Cost | What it does |
|---|---|---|
| `blotato list` | free, offline | Every catalog technique with its honest status |
| `blotato show <id>` | free, offline | One technique's media roles, settings, known issues |
| `blotato balance` | free | Credit balance and account email |
| `blotato inspect` | free | Snapshots Blotato's live template catalog to `outputs/` |
| `blotato plan` | free, offline | Validates inputs, checksums local assets, writes `plan.json` |
| `blotato approve` | free | Records a human's credit ceiling and approval reference |
| `blotato submit` | **spends credits** | One bounded call, polled to completion, downloaded |
| `blotato poll <run-dir>` | free | Resumes an already-paid-for run: finishes polling, downloads its media |
| `blotato pinterest …` | free | Local Pinterest research workflow (no publishing, no paid calls) |

## Where files come from and go

Relative paths resolve against a **workspace** directory: `$BLOTATO_WORKSPACE`, else the directory you ran the command from. Override per-invocation with `--workspace`. Absolute asset paths always work as given. Outputs go to `<workspace>/outputs/`.

You do not have to work inside this checkout — that is the point of installing it.

## What `submit` refuses to do

It exits non-zero rather than spending credits when:

- **the plan no longer matches its `approval_digest`** — an approval is bound to the exact model, prompt, media and settings that were approved, so editing `plan.json` afterwards invalidates it
- **this plan was already submitted** — the run directory is keyed by the digest, so a repeat `submit` is refused and points you at `blotato poll`
- the catalog marks the technique `broken`
- there is no positive `max_credits_ceiling`
- there is no recorded approval reference and timestamp
- the current balance is below the ceiling
- a local asset's checksum drifted between `plan` and `submit`
- the request body contains a publishing, scheduling, social-account, or third-party-credential field

`max_credits_ceiling` and the approval block are deliberately *outside* the digest — `blotato approve` writes them, and must not invalidate the plan it is approving.

`BLOTATO_API_KEY` is read from the environment only, never accepted as an argument, and redacted from everything written to disk.

## The catalog is small and honest

```
$ blotato list
ai-video-with-ai-voice         video  unverified          AI Video with AI Voice
image-slideshow-text-overlays  video  BROKEN              Image Slideshow with Text Overlays
product-scene-placement        image  verified 2026-09-08  Product Scene Placement
```

- **verified `<date>`** — we submitted it live and confirmed what it actually does.
- **unverified** — the schema came from Blotato's template listing; never submitted.
- **BROKEN** — we ran it and it does not work as documented. `submit` refuses it.

Never trust a template because its Blotato-side description sounds right. Only `verified_at` means anything. Growing this catalog is the main way to make the tool more useful — see below.

### Adding a technique

One small file in `src/blotato/catalog/templates/`, modelled on `product_scene_placement.py`. It declares the real Blotato template id (get it from `blotato inspect`), which media roles it needs, and a `build_inputs()` that maps the generic plan onto that template's input shape. Leave `verified_at = None` until you have actually submitted it and looked at the output. Record what you observed in `known_issues` — `image_slideshow_text_overlays.py` shows how a live-discovered bug gets encoded so nobody burns credits rediscovering it.

The architecture follows the open-source [`open-higgsfield`](https://github.com/wide-trace/open-higgsfield) project (MIT), with Blotato as the only backend.

## Layout

```
src/blotato/          the installable package — this is the tool
  cli.py                the `blotato` command
  api.py  runner.py     HTTP client, credit guardrails, redaction, validation
  catalog/              one file per technique
  studio/               plan.py (free) and submit.py (spends credits)
  workflows/pinterest/  local Pinterest research workflow
  schemas/              JSON schemas shipped as package data
skills/blotato-studio/  Claude Code skill wrapping the CLI
docs/                   how to operate what is implemented
tests/                  104 tests, no network, no credits
lab/                    research notes and past experiments — not shipped
openspec/               change proposals (historical record)
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest tests -q
```

Tests are offline and hermetic: no network, no credits, no fixtures that depend on any particular brand's data. They pass on Windows, macOS and Linux.

`Pillow` is only needed for the optional local (zero-credit) video renderer: `pip install -e ".[render]"`.
