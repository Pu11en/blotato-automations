## Context

The repository currently contains research, policies, experiment templates, and a brand-specific pipeline, but no executable application or dependency stack. Blotato's current API uses template-specific schemas discovered from `GET /v2/videos/templates`; its older universal model fields are obsolete. The public cost table lists image-edit and image-to-video models, but it does not prove that every account or template exposes every needed source-image field. See [proposal.md](proposal.md) for motivation and the three capability specs for behavioral contracts.

The first implementation must work on modest local hardware, use only the existing Codex plan and Blotato credits for paid AI work, keep all project artifacts in this repository, and preserve exact product identity whenever model generation cannot.

## Goals / Non-Goals

**Goals:**

- Make one reference-image-to-video experiment repeatable from natural-language requests.
- Discover the account's real template contracts before building a generation payload.
- Keep paid calls individually approved, budgeted, recoverable after interruption, and attributable to a run.
- Make a generic skill reusable across future brand profiles while shipping Cinco H Ranch as the first profile.
- Produce enough evidence to decide whether a Blotato output is usable, not merely whether the request returned success.

**Non-Goals:**

- Autonomous content scheduling, publishing, or social-account management.
- A high-volume content factory, n8n deployment, Postgres ledger, or analytics loop.
- Exact founder cloning, lip sync, or promises that generated labels and packaging remain pixel-identical.
- Supporting direct model-provider keys, even when a Blotato integration screen offers them.
- Scraping the product catalog on every run; version one consumes an owner-reviewed profile.

## Decisions

### 1. Separate the Codex skill from the deterministic runner

The natural-language layer will live in `skills/blotato-brand-content/SKILL.md`. It will choose a mode, gather missing inputs, apply approval rules, and explain results. A Python standard-library runner will perform predictable validation, HTTP, polling, downloading, hashing, redaction, and state persistence.

Planned layout:

```text
skills/blotato-brand-content/
  SKILL.md
  agents/openai.yaml
  references/
    modes.md
    blotato-contract.md
    review.md
  scripts/
    blotato_run.py
brands/
  cinco-h-ranch/
    profile.json
    claims.json
schemas/
  brand-profile.schema.json
  blotato-run.schema.json
tests/
  fixtures/
  test_blotato_run.py
outputs/blotato-runs/       # ignored
```

This keeps agent guidance short and puts API details in a conditional reference. A shell-only approach was rejected because sanitizing nested JSON, resuming state, and testing timeout behavior are materially more reliable in a small script. A larger application framework was rejected because the first slice needs no server or database.

### 2. Use a command-shaped state machine

The runner will expose these actions:

- `inspect`: fetch credits and live templates, sanitize and store the snapshot; zero generation spend.
- `plan`: validate the profile, source asset, claims, live schema, model choice, and credit ceiling; zero generation spend.
- `generate-image`: submit exactly the previously approved image plan and poll it.
- `approve-image`: bind a human decision to the generated image checksum.
- `animate-approved-image`: submit exactly the approved video plan and poll it.
- `audit`: create metadata, representative frames/contact sheet, claim mappings, and a review form.
- `status`: display existing run state without creating external work.

State advances monotonically:

```text
INSPECTED -> PLANNED -> IMAGE_RUNNING -> IMAGE_READY
  -> IMAGE_APPROVED -> VIDEO_RUNNING -> VIDEO_READY -> AUDIT_READY

Any generation -> FAILED or TIMED_OUT
Any review -> REJECTED
```

Paid actions cannot be combined into one opaque `run everything` command. This is intentional: the image must be visible before more credits are committed to animation.

### 3. Treat the live template schema as the capability authority

The runner will not build generation payloads from the public price table. `inspect` will save the full authenticated template response and its retrieval time. `plan` will select only a live template whose declared inputs support the requested operation.

For image-to-image, support requires both a source-image input and an edit prompt/model path in the same live contract. Seeing `nano-banana-2/edit` in a cost list is insufficient. If no such contract exists, the run stops as `unsupported` without spending credits.

For image-to-video, the same rule applies: the source image and chosen video model/mode must be accepted by the live template. Model identifiers and template UUIDs are run data, not permanent constants.

An alternative that hard-codes the currently published template fields was rejected because Blotato's static pages already differ from the master model table.

### 4. Make exactness a declared render strategy

Each plan will choose one of three strategies:

- `reference-edit`: the model receives the source image; likeness is experimental and must be reviewed.
- `exact-asset`: the original image is passed through unchanged and Blotato adds layout, captions, or editing.
- `exact-overlay`: a generated background or motion layer is combined locally with the authoritative original product cutout after generation.

The plan must state which pixels are allowed to change. Cinco product labels, logos, and founder identities default to `exact-asset` or `exact-overlay`. Reference editing can be tested on a copy but cannot silently become an approved product representation.

The alternative—assuming that an edit model preserves the product because it accepts a reference—was rejected because acceptance of an input does not guarantee faithful labels, proportions, or identity.

### 5. Store a self-contained run package

Every run will use `outputs/blotato-runs/<timestamp>-<slug>-<short-id>/` and maintain an atomic `state.json`. The package will include:

```text
plan.json
brand-profile.snapshot.json
template-catalog.sanitized.json
source/manifest.json
requests/*.sanitized.json
responses/*.sanitized.json
media/generated-image.*
media/generated-video.*
audit/ffprobe.json
audit/contact-sheet.jpg
audit/review.md
credits.json
state.json
```

The whole `outputs/` tree remains ignored. Stable inputs that should be reusable across runs live in tracked or ignored brand asset directories according to their rights and sensitivity; the run package records their checksums rather than duplicating secrets.

Atomic state updates and stored external request IDs allow `status` or the original action to resume polling without duplicate submission. A database was rejected for version one because file state is sufficient for a single-user, one-run-at-a-time experiment.

### 6. Bind approval to immutable job details

An approved plan will have a digest over its sanitized JSON. The paid command must receive that digest and will refuse execution if the plan, source checksum, template snapshot, prompt, model, or maximum credits changed. Image approval similarly binds the generated image checksum to the next video plan.

The human's actual approving message or entered decision is recorded as a reference and timestamp, but the skill will not invent approval from an earlier planning conversation. Changing any paid parameter produces a new digest and requires new approval.

### 7. Enforce cost before submission and reconcile afterward

`plan` will calculate an estimate from the live template metadata when available, otherwise mark the estimate unknown and refuse paid execution. The user must approve a positive `maxCredits`. Before each paid call, the runner checks the latest balance and the unspent run ceiling. After completion it fetches the balance again and records both the estimate and observed delta.

There will be no automatic paid retries. A rejected or failed attempt can be replanned, but it receives a new approval digest. Polling an existing request is not a retry and does not create another generation.

### 8. Validate claims before media generation

The generic profile schema will separate:

- immutable identity facts;
- approved factual and sensory phrases;
- review-required patterns;
- blocked patterns and topics;
- exact-asset rules;
- asset permissions and provenance.

The deterministic gate catches exact blocked terms and requires each factual line to carry a fact identifier. Codex performs semantic review for paraphrases and context. Neither check alone is treated as sufficient. Cinco's existing sunscreen, pest, pain, disease, healing, and testimonial risks enter the initial profile as blocked or human-review-only.

### 9. Keep credentials out of both Git and evidence

The runner reads `BLOTATO_API_KEY` from the environment and never accepts it as a command-line argument. A centralized sanitizer removes case-insensitive credential headers, cookies, authorization fields, API-key-shaped fields, and configured secret values before persistence or display. Tests use fake keys and a local fake HTTP transport.

The skill will not enumerate connected accounts because publishing is absent and account discovery creates no value for generation-only work.

### 10. Test behavior at the adapter boundary

Tests will use recorded synthetic fixtures shaped like the credit, template, submission, polling, success, failure, and timeout responses. They will verify:

- reference editing is rejected when the schema lacks the required input;
- plans cannot spend at a zero or exceeded ceiling;
- paid actions require the matching approval digest;
- a known request ID is polled rather than resubmitted after restart;
- failure and timeout do not trigger another generation;
- secrets never appear in saved artifacts;
- unapproved images cannot reach video generation;
- publishing-like fields and endpoints are rejected;
- a successful fake run produces the complete audit package.

One authenticated `inspect` smoke test can run after the API key is supplied because it spends no generation credits. The first paid end-to-end check will be one explicitly approved low-cost image and one explicitly approved low-cost animation.

## Risks / Trade-offs

- **[Blotato exposes edit models but no usable reference-input template]** → Fail as unsupported, save the live evidence, and use `exact-asset` or `exact-overlay`; do not fall back to a direct provider.
- **[A model alters the product or label]** → Require image approval before animation and provide exact-asset strategies.
- **[Credit estimates are missing or stale]** → Refuse generation until a bounded estimate is visible; reconcile with account balances afterward.
- **[Balance changes because another process spends credits concurrently]** → Record timestamps and observed deltas, flag ambiguity, and never infer precise job cost when concurrent spend is detected.
- **[Blotato completes after the local timeout]** → Preserve the request ID and allow later polling; never resubmit automatically.
- **[A deterministic blocked-term list misses a paraphrase]** → Require semantic review and fact IDs in addition to pattern checks.
- **[Project-local skills are not automatically visible globally]** → Keep the canonical source in this repository; installation or linking into shared `CODEX_HOME` is a separate, reversible implementation step.
- **[File-backed state limits concurrency]** → Enforce one writer per run directory and postpone a database until parallel generation is actually needed.

## Migration Plan

1. Add the skill, profile schemas, Cinco profile, runner, fixtures, and tests without changing existing workflows.
2. Validate the skill package and run the offline test suite.
3. Run authenticated `inspect` only and save its sanitized output under `outputs/`.
4. Revise adapter fixtures if the live account schema differs from documentation.
5. With new explicit approval, execute one bounded image generation and review it.
6. With separate approval of that image and remaining credits, animate it once and create the audit package.

Rollback consists of removing the project-local skill and its new supporting files. Existing research and content plans remain valid, and no remote posts or schedules require cleanup because version one cannot create them.

## Open Questions

- Which live Blotato template, if any, exposes a direct source-image contract for Nano Banana 2 Edit on this account? Authenticated `inspect` will answer this without spending credits.
- Which lowest-cost image-to-video model is exposed by that template at implementation time? The live enum and displayed estimate will determine the first candidate rather than a fixed assumption.
