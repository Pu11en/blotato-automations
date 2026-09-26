# lab/

Notes, research and past experiments. **Nothing here ships** — no code in `src/blotato/` imports from this directory, and none of it is installed with the package.

The split exists so the repository's front page is the tool, not its history. If something in here turns out to be reusable, it graduates into `src/blotato/` with tests; until then it stays a note.

| Directory | What it holds |
|---|---|
| `research/` | What Blotato can actually do, evaluated community workflows, public output quality, real-user scans |
| `docs/` | The original infrastructure plan, the AI-builder content system, and the Cinco H Ranch content pipeline |
| `experiments/` | One folder per content hypothesis: brief, workflow, outputs, results |
| `templates/` | Experiment and workflow-audit templates |
| `workflows/` | Reusable n8n/Make/API workflows that passed an experiment |
| `inputs/` | Image-taste reference notes |
| `archive/blotato-brand-content/` | The original brand-content skill — see below |
| `archive/openspec/` | Two Cinco H Ranch change proposals and the six openspec agent skills. Both proposals describe work that has since been restructured or deleted, so they are a record, not a plan. |

## archive/blotato-brand-content/

This was the first skill built here. Its scripts are hardcoded to `brands/cinco-h-ranch/profile.json`, which no longer exists in the repository, so **they do not run as written**. It is kept for two things worth not losing:

- `references/blotato-contract.md`, `modes.md`, `review.md` — what was learned about Blotato's template contract and review gates
- `scripts/render_pinterest_video_local.py` — a local, zero-credit Ken Burns video renderer that would be worth generalizing and moving into `src/blotato/`

Its genuinely reusable parts already graduated: the HTTP client and credit guardrails are `src/blotato/api.py` and `runner.py`, and its zero-cost template inspector is `blotato inspect`.

## Cinco H Ranch

The brand's profile, claims and product photos were removed from the working tree — they were 21 MB of one client's assets sitting at the top of a general-purpose tool. Git history still has all of it; `git log --all -- brands/` finds the commits if it is ever needed again.
