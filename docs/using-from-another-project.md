# Using this from another project

This repository is the shared Blotato layer. Other projects (youtube-money, a client repo, a one-off experiment) depend on it instead of writing their own client, and get the capabilities **plus** the guardrails: one bounded paid call, approvals bound to plan content, no double-spend, recorded costs, and honest notes about what each technique actually does.

## Install

```bash
# from the local checkout, while both repos live side by side
pip install -e ../blotato-automations

# or pinned straight from GitHub
pip install "blotato-automations @ git+https://github.com/Pu11en/blotato-automations@main"
```

In a `pyproject.toml`:

```toml
dependencies = [
    "blotato-automations @ git+https://github.com/Pu11en/blotato-automations@main",
]
```

Both give you the importable `blotato` package and the `blotato` command.

## The API

Import from the top-level package. Everything in `blotato.__all__` is supported; anything else is internal and may move.

```python
from blotato import build_plan, submit_plan_file, poll_run, list_models, get_model

# What can this account do, and what does it cost?
for t in list_models(include_broken=False):
    print(t.id, t.surface, t.observed_credits, t.cost_note or "")

# Free: validates inputs, checksums local assets, writes a plan
plan = build_plan(
    model_id="infographic-whiteboard",
    prompt="5 editing habits that save an hour a week",
    media={},
    settings={"footerText": "Subscribe"},
    workspace="/abs/path/to/your/project",
)
```

`build_plan` returns a dict. To spend credits, write it to disk, record an approval, then submit:

```python
import json
from pathlib import Path
from datetime import datetime, timezone

path = Path("plan.json")
plan["max_credits_ceiling"] = 60
plan["approval"] = {
    "reference": "who approved this and where it is recorded",
    "decided_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}
path.write_text(json.dumps(plan))

result = submit_plan_file(path, workspace="/abs/path/to/your/project")
```

`submit_plan_file` raises `SystemExit` with a message rather than spending, if the plan was edited after approval, was already submitted, names a broken technique, has no ceiling or approval, or the balance is below the ceiling. Catch it if you would rather not exit:

```python
try:
    result = submit_plan_file(path, workspace=root)
except SystemExit as refusal:
    log.warning("blotato refused: %s", refusal)
```

### Cap a whole batch, not just one call

A per-call ceiling does not bound a loop. Name the run and give it a budget, and the ledger accumulates across calls:

```python
from blotato import credits_spent

result = submit_plan_file(path, workspace=root, run="thumbnails-oct", budget=300)
print(credits_spent(run="thumbnails-oct", workspace=root))
```

Once the run's total would exceed its budget, `submit_plan_file` refuses **before** contacting the API. Every paid call lands in `<workspace>/outputs/credits.log`, including failures and timeouts.

If a run times out, the credits are gone but the job is not: `result["recover_with"]` names the command, and `poll_run(run_dir)` does the same from Python.

## Credentials and paths

`BLOTATO_API_KEY` is read from the environment, or from a `.env` in the **workspace** directory. It is never accepted as an argument. The real environment wins over `.env`.

The workspace is what relative asset paths and `outputs/` resolve against: the `workspace=` argument, else `$BLOTATO_WORKSPACE`, else the current directory. A library consumer should pass `workspace=` explicitly rather than relying on the caller's cwd.

## Adding your own techniques

A downstream project contributes techniques **without forking this repo**, by declaring a `blotato.techniques` entry point. They then appear in `blotato list`, in `list_models()`, and go through the same plan/approve/submit guardrails.

`pyproject.toml`:

```toml
[project.entry-points."blotato.techniques"]
youtube-money = "youtube_money.blotato_techniques"
```

`youtube_money/blotato_techniques.py`:

```python
from blotato import GenerationPlane, ModelEntry, SettingField


def build_inputs(plane: GenerationPlane) -> dict:
    return {"description": plane.prompt, "footerText": plane.settings.get("cta", "Subscribe")}


ENTRY = ModelEntry(
    id="yt-thumbnail-brief",
    blotato_template_id="...",        # from `blotato inspect`
    surface="image",
    label="YouTube thumbnail brief",
    description="...",
    roles={},                          # or {"reference": (1, 1)}
    settings={"cta": SettingField(kind="text", default="Subscribe")},
    build_inputs=build_inputs,
    verified_at="2026-09-26",          # only after you have run it and looked
    observed_credits=50,               # measured from the balance, not guessed
)
```

Export `ENTRIES = (...)` instead of `ENTRY` to contribute several at once.

The module is imported at lookup time, so keep it cheap — declarations only, no network calls or heavy imports at module scope.

For techniques built at runtime, or in a test, use `register()`:

```python
from blotato import register
register(my_entry, origin="youtube-money")
```

`list_models(origin="youtube-money")` filters to one contributor, and `origins()` lists them all.

### Ids must be unique

If two packages claim the same catalog id, the registry raises `DuplicateModelError` naming both contributors, rather than letting import order decide. Prefix your ids (`yt-...`) to stay out of the way.

### The bar for `verified_at`

Set it only after submitting the technique live and looking at the output. Record what the output actually revealed in `known_issues`, and what it actually charged in `observed_credits`. That convention is the reason this catalog is worth reading — see `infographic-breaking-news` (renders a QR code that encodes nothing) and `ai-selfie-video` (400 credits per scene, ignores the character you describe) for what a useful note looks like.

## Finding new templates

`blotato inspect` costs nothing and writes the account's live template listing — every template's real id and input schema — to `outputs/blotato-inspect/<timestamp>/`. That is where a new entry's `blotato_template_id`, input names and bounds come from. Copy the bounds rather than guessing them, so bad input fails for free instead of costing a call.
