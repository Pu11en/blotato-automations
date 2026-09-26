# blotato-automations

The shared Blotato layer: a Python package and a CLI for generating images and videos through the [Blotato](https://blotato.com) API.

Pick a technique from a catalog, build a plan for free, approve a credit ceiling, then spend credits on exactly one bounded call. Nothing here publishes, schedules, or touches a social account.

**Other projects depend on this rather than writing their own client.** They get the capabilities plus the guardrails, and can contribute their own techniques without forking — see [`docs/using-from-another-project.md`](docs/using-from-another-project.md).

```toml
dependencies = [
    "blotato-automations @ git+https://github.com/Pu11en/blotato-automations@main",
]
```

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
| `blotato spent` | free, offline | What the ledger says every paid call actually cost |
| `blotato pinterest …` | free | Local Pinterest research workflow (no publishing, no paid calls) |

`blotato list` shows every technique this account can reach, including any contributed by other installed packages. `~0 cr*` means the cost depends on how you use it — `blotato show <id>` explains.

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

### Bounding the total, not just each call

`max_credits_ceiling` bounds **one** call. A script looping over `submit` with a 50-credit ceiling could still drain the balance, 50 at a time, with every individual call looking correct. Name the run and give it a budget:

```bash
blotato submit plan.json --run thumbnails-oct --budget 300
```

Every paid call is appended to `outputs/credits.log` — including failed and timed-out ones, since the credits are gone either way — and `submit` refuses once the run's total would exceed its budget. A call whose cost could not be measured counts as its full ceiling rather than zero; guessing low is how a budget gets blown.

```
$ blotato spent --run thumbnails-oct
2026-09-26T12:17:20Z  thumbnails-oct    50  infographic-whiteboard
2026-09-26T12:19:04Z  thumbnails-oct    50  infographic-newspaper

2 paid call(s), 100 credits for run 'thumbnails-oct'.
```

`max_credits_ceiling` and the approval block are deliberately *outside* the digest — `blotato approve` writes them, and must not invalidate the plan it is approving.

`BLOTATO_API_KEY` is read from the environment only, never accepted as an argument, and redacted from everything written to disk.

## Everything in the catalog has actually been run

```
$ blotato list
ai-video-with-ai-voice         video  verified 2026-09-26  ~45 cr         AI Video with AI Voice
image-slideshow-text-overlays  video  BROKEN              cost unknown   Image Slideshow with Text Overlays
infographic-breaking-news      image  verified 2026-09-26  ~50 cr         Breaking News
infographic-newspaper          image  verified 2026-09-26  ~50 cr         Newspaper Infographic
infographic-whiteboard         image  verified 2026-09-26  ~50 cr         Whiteboard Infographic
product-scene-placement        image  verified 2026-09-08  cost unknown   Product Scene Placement
```

**The rule: an entry is either live-verified or explicitly marked BROKEN.** A technique nobody has run does not get listed — Blotato exposes 37 templates, and the ones here are the ones somebody submitted and looked at. A test enforces this, so the catalog cannot quietly fill up with guesses.

- **verified `<date>`** — we ran it and inspected the output. `observed cost` is what that run actually charged, measured from the balance before and after, not a published price list.
- **BROKEN** — we ran it and it does not work as documented. `submit` refuses it. The entry stays so nobody rediscovers the same failure at credit cost.

`blotato show <id>` prints what a live run actually revealed. Those notes are observations, not guesses:

```
$ blotato show infographic-breaking-news
known issues (observed live, not guessed):
  - Invents a broadcaster and a photorealistic news anchor who does not exist,
    and the 2026-09-26 run rendered a QR code captioned 'Free thumbnail
    cheatsheet' that encodes nothing real.
```

Related templates share a file: the infographic styles all take the same two text inputs and no media, so they live in one `catalog/templates/infographics.py` — the registry accepts an `ENTRIES` tuple as well as a single `ENTRY`.

### Adding a technique

1. `blotato inspect` — free; dumps the live template listing with every template's real id and input schema.
2. Add one small file to `src/blotato/catalog/templates/`, modelled on `product_scene_placement.py`: the template id, the media roles it needs, and a `build_inputs()` mapping the generic plan onto that template's input shape. Copy the bounds from the listing rather than guessing them, so bad input fails for free.
3. **Run it once and look at the output.** Only then set `verified_at` and `observed_credits`.
4. Record what you saw in `known_issues` — `image_slideshow_text_overlays.py` shows how a live-discovered bug gets encoded so nobody burns credits rediscovering it.

Until step 3 happens, the entry does not belong in the catalog.

The architecture follows the open-source [`open-higgsfield`](https://github.com/wide-trace/open-higgsfield) project (MIT), with Blotato as the only backend.

## Layout

```
src/blotato/          the installable package — this is the tool
  cli.py                the `blotato` command
  api.py  runner.py     HTTP client, credit guardrails, redaction, validation
  catalog/              one file per technique
  studio/               plan.py (free) and submit.py (spends credits)
  workflows/pinterest/  local Pinterest research workflow
skills/                 Claude Code skills wrapping the CLI
docs/                   how to operate what is implemented
tests/                  163 tests, no network, no credits
lab/                    research notes, archived experiments — ships nothing
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest tests -q
```

Tests are offline and hermetic: no network, no credits, no fixtures that depend on any particular brand's data. They pass on Windows, macOS and Linux.

`Pillow` is only needed for the optional local (zero-credit) video renderer: `pip install -e ".[render]"`.
