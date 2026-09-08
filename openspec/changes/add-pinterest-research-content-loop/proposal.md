## Why

Cinco H Ranch needs Pinterest content that earns qualified website visits and purchases, with credible visual direction and accurate products. The repository has a proposed media runner but no repeatable way to validate Pinterest demand, turn reference Pins into original briefs, or learn which content produces commercial results.

## What Changes

- Add a local Pinterest research skill and file-backed CLI: collect timestamped trend evidence and reference Pins, rank relevant opportunities, and produce three reviewable briefs.
- Use official Pinterest Trends where access works, OpenCLI for read-only reference discovery, and documented manual imports when either is unavailable.
- Separate measured demand, creative inspiration, and untested commercial hypotheses; preserve provenance and reuse permissions.
- Export original static/video production briefs with exact product assets, destinations, tracking links, claims checks, and explicit audio direction.
- Import own-account and website results to compare clicks, attributed orders, revenue, and production cost.
- Keep generation optional through the existing planned Blotato runner; exclude automatic publishing and paid direct provider dependencies.

## Capabilities

### New Capabilities

- `pinterest-opportunity-research`: Evidence collection, provenance, product relevance, and explainable opportunity selection.
- `pinterest-content-experiments`: Original creative briefs, review gates, tracked destinations, and commercial feedback.

### Modified Capabilities

None. The earlier unimplemented `add-blotato-brand-automation-skill` plan remains separate; this change defines a file interface to it without changing its requirements.

## Impact

Proposed additions are a project-local skill, Python CLI modules, JSON schemas, fixtures/tests, and a Cinco H Ranch research profile. No production application exists yet. Live integrations require separately verified Pinterest access and website analytics exports. Existing paid-tool, identity-preservation, and account-isolation policies remain applicable. This planning change does not execute paid generation or publish content.
