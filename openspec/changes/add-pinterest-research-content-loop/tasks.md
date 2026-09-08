## 1. Contracts and connection checks

- [ ] 1.1 Define versioned run, signal, reference, candidate, brief and result schemas in templates/pinterest; verify valid fixtures pass and missing provenance, invalid metric units and unknown versions fail.
- [ ] 1.2 Add a dependency manifest and doctor command documenting licenses, pinned versions, hostnames, authentication and limits; verify it reports absent browser/API credentials without leaking secrets or starting paid calls.
- [ ] 1.3 Validate OpenCLI read-only search/detail and official Trends access using one bounded live sample when available; preserve sanitized evidence or an explicit unavailable status and verified manual-import fallback.

## 2. Research and opportunity selection

- [ ] 2.1 Implement atomic file-backed run storage and manual evidence imports; verify interrupted writes preserve previous evidence and reruns do not duplicate sources.
- [ ] 2.2 Implement the OpenCLI read-only wrapper with the pilot query limits, canonical deduplication and bounded backoff; verify auth failure, rate limits, malformed output and attempts to invoke writes are handled.
- [ ] 2.3 Implement the Trends adapter using the schema validated in 1.3; verify recorded normalized series and growth units are preserved, absent fields stay null, and unsupported responses fall back visibly to manual import.
- [ ] 2.4 Add Cinco H Ranch research configuration, product facts/asset references and the five-factor rubric; verify a relevant candidate passes, an aesthetic-only mismatch fails and insufficient evidence produces fewer than three qualified candidates.

## 3. Creative briefs and experiment export

- [ ] 3.1 Add the project-local research skill and Markdown/JSON brief templates; verify a fixture run produces three distinct original briefs with evidence, static layouts, timed video shots, exact assets, claim annotations, CTA and audio choice.
- [ ] 3.2 Implement destination validation, stable experiment/version IDs and UTM generation; verify existing query parameters survive and rejected destinations block distribution readiness.
- [ ] 3.3 Implement the production request export and hash-bound review states; verify missing runner/budget approval causes export-only behavior and changed assets invalidate approval. Do not implement a second media runner.
- [ ] 3.4 Add preview review requirements for product fidelity, typography, muted clarity, audio rights and media metadata; verify a distorted product or undeclared audio choice fails review.

## 4. Results and learning

- [ ] 4.1 Define documented Pinterest and website CSV/JSON mappings using available authorized sample exports; verify source/account identity, date windows, currency and attribution fields, with missing values distinct from zero.
- [ ] 4.2 Implement idempotent results imports and Pin-to-asset association; verify repeated and overlapping cumulative exports do not inflate totals and unattributed orders remain separate.
- [ ] 4.3 Implement equal-age reports for 7/14/30-day checkpoints with outbound CTR, sessions, attributed orders, net revenue and production costs; verify zero denominators, refunds, mixed currencies and sparse evidence do not yield misleading winners or profit claims.

## 5. Acceptance and handoff

- [ ] 5.1 Run an offline end-to-end fixture from evidence through briefs and results; deliver an inspectable report proving zero paid calls, no publishing, traceable sources and correct repeated-import behavior.
- [ ] 5.2 Run one authorized live research pilot of at most five queries and 50 reference Pins; deliver an evidence report and up to three qualified briefs, explicitly labeling any exploratory alternatives and unavailable demand data.
- [ ] 5.3 Document live production/distribution readiness separately from software completion: approved real media/facts, available existing Blotato runner and budget if used, exact authorized Pinterest account, and website tracking. Verify each item is ready or explicitly pending; do not publish as part of this build.
- [ ] 5.4 Deliver the skill invocation, sample outputs, test evidence and dependency manifest; verify another session can resume the run from its saved files and durable thread binding.
