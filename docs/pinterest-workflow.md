# Pinterest research workflow

The local workflow collects evidence, ranks product-relevant opportunities, packages original static/video briefs, and imports attributable experiment results. It has no rendering, publishing, paid API, or scheduling function. The existing Blotato generation plan is a separate dependency for production.

## Start through the conversation

Ask: “Use pinterest-research to research Cinco H Ranch and prepare three briefs.” The project-local skill at `.agents/skills/pinterest-research/SKILL.md` guides the agent. It is project-local, not globally installed. The agent writes creative assessments and scripts; the CLI validates and packages them without an extra model API.

Resolve this thread's repo/worktree from the durable binding before using commands. The examples below assume you are in that checkout. To run from any directory, invoke `/absolute/checkout/scripts/pinterest/cli.py` with absolute input/output paths.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/pinterest/requirements.txt
source .venv/bin/activate
python3 scripts/pinterest/cli.py doctor --out outputs/pinterest/doctor.json
python3 scripts/pinterest/demo.py --out outputs/pinterest/fixture-demo
```

The demo is entirely synthetic: three briefs, two variants each, two pretend publication records, and a repeated analytics import. Its dates, demand figures, Pin IDs and results are not real business evidence.

## Research

```sh
python3 scripts/pinterest/cli.py collect --run outputs/pinterest/research-20260908 --profile assets/brands/cinco-h-ranch/pinterest.json --mode live --live
python3 scripts/pinterest/cli.py collect --run outputs/pinterest/research-20260908 --profile assets/brands/cinco-h-ranch/pinterest.json --mode live --references /absolute/references.json --signals /absolute/signals.json
python3 scripts/pinterest/cli.py rank --run outputs/pinterest/research-20260908 --input /absolute/assessments.json
```

Use a new run directory for fresh source observations, changed profile or different mode. Existing collection checkpoints are reused, including failures, so resume does not silently retry access errors. Manual import can supplement that same run. Complete fetched responses are cached before later stages; an interrupted in-flight GET may be repeated because its completion is unknowable. File locks serialize concurrent writes to a run; atomic replacement preserves earlier files if a write fails.

Source records conform to `signal` and `reference` in `templates/pinterest/contracts.json`. JSON imports are arrays. CSV headers use the same field names, nested objects/arrays use JSON-encoded cells, and empty cells mean null. Preserve source hashes and original observations; the importer also saves a hash-addressed snapshot of the submitted records. Evidence IDs cannot be repurposed for changed demand observations. Reference Pins deduplicate by canonical numeric ID; regional/slug URLs must first be normalized to `https://www.pinterest.com/pin/<id>/` with their original URL retained in an observation.

OpenCLI 1.8.8 is the reviewed candidate interface. Its pinned source revision and the official Pinterest API-description revision are in `templates/pinterest/dependencies.json`. OpenCLI is optional and not installed by this build. Its browser bridge is also unverified; installing it must not restart another session's browser/daemon. Supply a locally installed executable through `PINTEREST_OPENCLI_BIN` if needed. Reads are limited to search-pins, pin, and board-pins. No writes, downloads, or arbitrary command arguments are exposed. HTTPS uses the pinned certifi CA bundle, including on macOS Python installs without a configured default certificate store. OAuth uses `PINTEREST_ACCESS_TOKEN`; keep it in the process environment, never the profile or repository. The API uses `include_keywords`, current US growing trends, and no group normalization. API entitlement and runtime response compatibility still need a live test.

A `candidate_input` assessment is explicit editorial judgment: five 0–2 scores and reasons, exact keyword, product, sources and concept. Measured demand must match that keyword. Missing demand forces a zero demand score and exploratory status. A product/intent mismatch excludes the candidate. The report shows at most three non-excluded candidates with all evidence and limitations. These scores do not predict income.

## Briefs, review and production export

```sh
python3 scripts/pinterest/cli.py brief --run outputs/pinterest/research-20260908 --input /absolute/brief.json --check-url
python3 scripts/pinterest/cli.py export --run outputs/pinterest/research-20260908 --brief harvest-flecks-v1 --check-url
```

The `brief` contract and three fixture examples document inputs. A brief includes a static composition, an original script, contiguous timed shots, exact product assets, annotated facts, destination and explicit audio direction. A 1000×1500 output and approximately 12-second video are starting choices, not a guarantee of reach. URLs get distinct static/video/version UTMs while preserving existing product query parameters. Live URL checks are host-allowlisted and reject redirects; use the canonical product URL. A passing HTTP check does not prove stock availability or commercial suitability—review those manually.

Profile facts/assets start unapproved. Public product images are reference-only until ownership/permission and original local bytes are confirmed. For production, create a reviewed profile with actual media paths, SHA-256, rights evidence and approved facts; start a new run or brief version. Never approve on behalf of a human or invent rights. Unclassified/medical/performance claims require the established brand-policy review. The claim ID list does not excuse checking all actual copy.

`review --run <dir> --brief <id>-v1 --input <review.json>` accepts an explicit human decision:

```json
{
  "stage": "image",
  "decision": "approved",
  "reviewer": "Actual reviewer name",
  "evidence": "Reference to the human's actual review and decision",
  "media_path": "/absolute/reviewed-preview.png",
  "checks": {
    "product_identity": true,
    "claims": true,
    "typography": true,
    "muted_clarity": true,
    "audio_rights": true,
    "media_metadata": true,
    "pacing": true
  }
}
```

Use stage `final` for the completed media, after current image approval. Reviews bind actual source files, profile, brief and preview hashes; changes invalidate approval. The reviewer must inspect real media and metadata (for example via ffprobe), sound and muted playback. A failing check records rejection. Audio rights are required for non-silent choices. The workflow does not automatically render media or claim that a boolean review is a visual inspection.

Exports always have `mode: export_only` and `credit_ceiling: 0`. They include unmet prerequisites. A separate Blotato runner must accept the versioned handoff and its own explicit budget before any paid execution; this build does not implement or assume that runner. Publishing remains manual to an explicitly authorized account.

## Import mapping and attribution

Only configured account/property IDs are accepted. Supply them in a local reviewed profile, not guessed from existing connected social accounts. The initial brand profile has no authorized accounts. `results register` associates an existing published Pin with an exported asset:

```json
{
  "asset_id": "harvest-flecks-static-v1",
  "pin_url": "https://www.pinterest.com/pin/123456789/",
  "published_date": "2026-09-08",
  "account_id": "the-explicitly-authorized-account",
  "authorization_reference": "Reference to the user's account authorization"
}
```

Registration records a manual event; it does not publish or approve a Pin. Duplicate identical associations are harmless; reusing a Pin for a different asset is rejected.

Use canonical long-form JSON/CSV rows described by `result`. This is a documented import interface, **not a claim that the current Wix or Pinterest download uses these exact headers**. A real authorized export is still needed to validate the final vendor-to-canonical mapping. Do not import customer names, emails or addresses.

| Canonical field | Pinterest export mapping | Website/cost export mapping |
| --- | --- | --- |
| source | `pinterest` | `website` or `costs` |
| account_id | Verified account ID | Verified analytics property or cost-ledger ID |
| asset_id / experiment_id / pin_id | Match registered Pin to exported asset | Match exact UTM content to registered asset; otherwise all three IDs null for unattributed website rows |
| metric | impressions, saves, outbound_clicks | sessions, orders, revenue, refunds, production_cost |
| value | Raw nonnegative count; absent means null | Nonnegative count or money; absent means null |
| period | Publication date inclusive to checkpoint end exclusive | Same cumulative window; normalize an inclusive vendor end date before import |
| extracted_at | Export extraction time with timezone offset | Same |
| timezone | Configured reporting timezone | Same reporting timezone; do not relabel timestamps to conceal a mismatch |
| currency | null for counts | ISO currency for money; null for counts |
| attribution_model / attribution_window | `not_applicable` | Actual website model/window; must match profile. Costs use `not_applicable` |
| mode / schema_version | `manual` or `live`, version 1 | Same; synthetic examples use `fixture` |

Counts and amounts must represent the entire cumulative window from the publication date. Daily exports must first be grouped into that window by an explicit, inspected mapping. Website order/revenue figures must use credible UTM attribution; proximity to a posting date is insufficient. There is no automatic order-level attribution engine in this MVP. Unattributed aggregate website rows are kept separately, never added to an experiment. Corrections replace the same source/window/metric/currency snapshot if extracted later; ambiguous same-time conflicting values fail. Older imports cannot overwrite newer values. Overlapping 7/14/30-day cumulative snapshots are never summed.

```sh
python3 scripts/pinterest/cli.py results register --run <absolute-run> --input <publication.json>
python3 scripts/pinterest/cli.py results import --run <absolute-run> --input <canonical-results.json>
python3 scripts/pinterest/cli.py results report --run <absolute-run> --days 7
```

Reports compare exactly 7, 14 or 30 days after each publication. Outbound CTR uses outbound clicks/impressions; purchase conversion uses attributed orders/attributed sessions. Missing or zero denominators produce unknown rates. Money remains separated by currency; net attributed revenue needs both revenue and refunds and is not profit. A single pair remains descriptive, not proof of a winning format.

## Verification and recovery

```sh
python3 -m unittest discover -s tests/pinterest -v
python3 scripts/pinterest/demo.py --out <absolute-fixture-run>
```

Tests cover schema errors, interrupted writes, duplicate imports, changed approvals, denied destinations, command restrictions, auth failures, rate limits, missing metrics, refunds/currency isolation and the CLI from an unrelated directory. Run files and private metrics belong in ignored outputs or a persistent private directory. Do not commit user data, browser credentials or actual order exports. The durable thread binding identifies the checked-out branch; preserved acceptance outputs are referenced in the implementation handoff.
