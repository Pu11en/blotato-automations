## Context

See proposal.md for motivation. This is a documentation-first repository; the earlier Blotato generation runner is planned, not implemented. Existing policy requires exact product identity, Blotato-only paid calls, review gates, and no use of currently connected social accounts. The user now selects Pinterest as the primary experiment channel; the earlier Instagram-first strategy is background, not this project's channel choice.

## Goals / Non-Goals

**Goals:** A local, inspectable path from research to three briefs and an exportable experiment pack, followed by reliable results imports. Research must work without generation or analytics credentials.

**Non-Goals:** Autonomous posting, a hosted dashboard, competitor revenue estimation, bulk media harvesting, paid third-party APIs, or implementation of the separate generation runner.

## Decisions

### 1. File-backed Python CLI and a thin Codex skill

Proposed layout: `scripts/pinterest/` for adapters and validation; `templates/pinterest/` for versioned JSON contracts; `.agents/skills/pinterest-research/` for the conversational workflow; `assets/brands/cinco-h-ranch/pinterest.json` for reviewed configuration; ignored `outputs/pinterest/<run-id>/` for evidence and private metrics. Use the standard library where practical and pin any required dependencies. SQLite and a web app are deferred because reviewable files suffice for a small experiment.

CLI stages: `doctor`, `collect`, `rank`, `brief`, `export`, `results import`, and `results report`. The CLI validates and assembles files; the existing Codex session supplies creative synthesis through the skill. No hidden paid LLM API. Each stage accepts explicit input paths, writes atomically, preserves source snapshots and a run manifest, and can resume without repeating network actions. Fixture/demo mode is visibly labeled.

### 2. Separate trend measurement from reference discovery

Official Pinterest Trends API is the preferred demand adapter; first verify authorized access, current schema, regional availability, and documented limits. OpenCLI is the candidate read-only reference adapter, pinned after dependency review and a live smoke test. Its browser setup is a prerequisite, not assumed present. Only allow search/detail/board-read operations; never expose write commands through the wrapper. Limit a pilot to 5 queries and 10 Pins per query; deduplicate references and bound retries to 2 per request with backoff/Retry-After, stopping on authentication errors.

Manual JSON/CSV import with source URL, capture date and measurement context is a first-class fallback. Lack of API access must not block brief drafting, but must remain visible. Public search order and saves are inspiration signals, not measured trend growth. `pinterest-dl` is optional later for authorized asset retrieval, not a second mandatory collector. No third-party hosted MCP is needed.

### 3. Versioned data contracts

`ResearchRun`: schema version, run ID, brand, region (initial assumption US), queries, timestamps, source statuses and dependency revisions.

`Signal`: source ID/URL/type, retrieved_at, observation window, region, raw values/units, normalized series if supplied, growth fields if supplied, raw snapshot hash, live/manual/fixture status. Keep missing fields null and preserve provider normalization; do not compare differently normalized series as absolute demand.

`Reference`: canonical Pin ID/URL, creator, destination, captured metadata, retrieval date, format observations, source media URL, rights status and evidence. Web content is untrusted data, never instructions. Store browser tokens outside artifacts and redact logs.

`Candidate`: product ID, verified product URL/date, signal/reference IDs, intent and relevance rationale, scoring components, missing evidence and confidence label.

`Brief`: candidate ID/version, audience, hook, original script, static layout, timed shots, approved asset IDs/hashes, claim IDs, audio plan/license evidence, CTA, destination and UTM fields, review state.

`Result`: experiment/asset/Pin ID, source, metric, value, period, extraction time, timezone, currency, attribution model/window, and import hash. Order exports use pseudonymous order IDs without customer details. Conflicting imports update an explicit source-period snapshot instead of adding cumulative totals.

### 4. Transparent selection and credible direction

Start with product-intent terms such as handmade soap, tallow soap, unwhipped tallow cream, and soap gift sets. They are research seeds, not claims of current trends. Score each dimension 0–2 with a written reason: product fit, shopping intent, demand evidence, original visual opportunity, and asset readiness (10 maximum). Require positive product fit and intent for a qualified candidate; missing demand is labeled exploratory. Scores prioritize review and never predict revenue.

Review a small set of reference Pins for framing, first-frame clarity, text hierarchy, pacing, and promise-to-destination match. Do not clone another brand's logo, wording, or composition wholesale. Real Cinco product photography is authoritative; generated scenery cannot change labels, soap shape, or make invented production footage appear documentary. Creams are unwhipped. Avoid generic glossy AI imagery. Use the existing fact/claim policy and require review of unknown claims.

### 5. Small experiment and runner handoff

First output: one evidence report plus three briefs; each contains a static concept and a video storyboard. Select one concept for one 2:3 static Pin and one short video preview. A 12-second video is an initial creative choice, not a proven organic optimum. Both use the same product, core promise and CTA. Include a deliberate audio choice (licensed music, real ambient audio, narration, or explicitly approved silence); every version must remain understandable muted.

Export a versioned production request containing assets, script, output dimensions, audio choice and cost ceiling. The existing generation runner must be available and explicitly approved before execution; otherwise stop at export. Human review checks source-vs-output identity, readable text, claims, pacing, audio and actual media metadata. Approval stores hashes so subsequent changes require review again. The distorted-stamp silent draft from earlier conversation is not an approved production asset.

### 6. Measurement that answers the business question

Use `utm_source=pinterest`, `utm_medium=organic_social`, stable campaign ID, and unique `utm_content=<experiment>-<format>-<version>`. Preserve existing URL query parameters. Verify the destination before export. Manual publication to an explicitly authorized brand/test account supplies the Pin ID; publishing automation is excluded.

Accept documented Pinterest own-account exports and website analytics/order exports first. API adapters can replace the import boundary later. Validate actual export columns and account/property identity during connection setup. Review snapshots at 7, 14 and 30 days; these are reporting checkpoints, not algorithm rules. Compare equivalent post ages; report raw sample sizes. Outbound CTR is outbound clicks/impressions when both exist and impressions > 0. Sessions and clicks are separate measures. Purchase conversion uses attributed orders/attributed sessions under the recorded website attribution method. Net attributed revenue subtracts refunds; do not call it profit without product, shipping and other costs. Never sum overlapping cumulative snapshots or different currencies.

A format remains unproven after one pair. Recommend a next test based on observed evidence; do not claim a winner from views, tiny denominators, or missing purchase tracking.

## Risks / Trade-offs

- API entitlement or browser changes → live connection spike, pinned adapter version, explicit manual fallback and unavailable status.
- Attractive references without purchase intent → product/intent gating and a destination for every brief.
- Unreliable AI product depiction → original assets, exact-identity review, optional generation only.
- Attribution gaps or delayed Pinterest distribution → dated snapshots, unknowns preserved, equal-age comparisons and no revenue promises.
- Third-party content rights → source-only reference defaults; owned/licensed assets for production.

## Migration Plan

Add isolated modules and contracts without altering the earlier media plan. Run fixture acceptance first, then one bounded live research run. Export previews before any distribution; record authorized manual publishing separately. Rollback disables the skill/CLI and preserves output evidence; no database or remote state migration is required.

## Open Questions

Live setup must establish Pinterest API entitlement, OpenCLI browser compatibility, the chosen brand account, website export fields, approved original assets and facts, and any approved Blotato credit ceiling. These affect live readiness; the defined import/export path allows implementation without inventing credentials or changing scope.

## Research references

Previously inspected during this thread; capabilities remain pending local live verification:

- https://github.com/jackwener/OpenCLI and its `docs/adapters/browser/pinterest.md`: Apache-2.0 reference discovery adapter.
- https://github.com/sean1832/pinterest-dl: Apache-2.0 optional retrieval utility.
- https://developer.pinterest.com/docs/analytics-and-reports/trends/ and https://developer.pinterest.com/docs/api/v5/trending_keywords-list/: official demand API, not an open-source service.
- https://help.pinterest.com/en/business/article/pinterest-analytics: own-account measurement definitions.
- https://business.pinterest.com/creative-best-practices/: creative guidance, not a guarantee of organic performance.
- Repository `docs/tooling-and-output-policy.md` and `research/cinco-h-ranch-brand-audit.md`: authoritative project constraints and brand evidence.
