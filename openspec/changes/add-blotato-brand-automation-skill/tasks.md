## 1. Skill and Data Contracts

- [x] 1.1 Scaffold `skills/blotato-brand-content/` with `SKILL.md`, `agents/openai.yaml`, focused references, and a scripts directory; run the skill creator's `quick_validate.py` and verify the package has no placeholder content.
- [x] 1.2 Add `schemas/brand-profile.schema.json` and `schemas/blotato-run.schema.json` covering profile facts/claims/assets and the complete run state machine; verify valid and intentionally invalid fixtures against both schemas.
- [x] 1.3 Add `brands/cinco-h-ranch/profile.json` and `claims.json` from the approved audit, including source URLs, exact-identity fields, permission metadata, green/yellow/red language, and timestamps; verify the profile passes the schema and representative sunscreen, pest, pain, disease, and healing copy is blocked.

## 2. Safe Runner Foundation

- [x] 2.1 Implement the standard-library runner's configuration, atomic run-directory state, asset hashing, and resume behavior in `skills/blotato-brand-content/scripts/blotato_run.py`; verify an interrupted fixture resumes the stored external request instead of submitting another.
- [x] 2.2 Implement centralized recursive request/response sanitization and environment-only `BLOTATO_API_KEY` loading; verify fake API keys, authorization fields, cookies, and nested secret-like values never appear in console or saved fixture artifacts.
- [x] 2.3 Add strict input validation that rejects publishing fields, account IDs, external-provider credentials, unknown state transitions, inaccessible source assets, and profiles with missing provenance; verify each rejection occurs before an HTTP generation request.

## 3. Live Inspection and Planning

- [ ] 3.1 Implement the zero-generation-cost `inspect` action for Blotato credits and `GET /v2/videos/templates?fields=id,name,description,inputs`, saving a timestamped sanitized snapshot; verify it against success, authentication failure, malformed schema, and rate-limit fixtures.
- [ ] 3.2 Implement capability matching that requires live source-image, prompt, model, and output fields for image editing and image-to-video; verify a price-table-only Nano Banana 2 Edit entry is reported as unsupported while a complete synthetic template is accepted.
- [ ] 3.3 Implement the `plan` action with brand claims mappings, render strategy, source checksum, selected live contracts, cost estimate, positive maximum-credit ceiling, fallbacks, and a stable approval digest; verify any material plan change invalidates the digest.

## 4. Bounded Media Generation

- [ ] 4.1 Implement `generate-image` to revalidate the approved plan and current balance, submit exactly one compatible Blotato request, persist its ID before polling, and download/checksum the result; verify success, failure, timeout, insufficient-credit, and restart cases without automatic paid retries.
- [ ] 4.2 Implement `approve-image` so approve/revise/reject decisions bind to the generated image checksum and actual user approval reference; verify missing, rejected, or stale approval prevents animation.
- [ ] 4.3 Implement `animate-approved-image` to validate the live video template and remaining run ceiling, submit one image-to-video request, poll without duplication, and persist the video plus observed credit delta; verify all generation outcomes with a fake transport.
- [ ] 4.4 Implement `exact-asset` pass-through and optional `exact-overlay` local composition without modifying the authoritative product asset; verify a pixel/hash comparison demonstrates the preserved overlay region and that `reference-edit` outputs are never labeled exact.

## 5. Audit and Skill Experience

- [ ] 5.1 Implement `audit` and `status` output: media download verification, `ffprobe` metadata, representative frame/contact-sheet generation when local tools exist, claims mappings, identity checklist, credits, and approve/revise/reject form; verify a complete fake run produces every required artifact at stable paths.
- [ ] 5.2 Write the skill's concise mode router and conditional references for API contracts, planning, approvals, and review; verify realistic inspect-only, planning-only, image-only, and image-then-video prompts select the correct action without assuming authorization.
- [ ] 5.3 Add `unittest` coverage for the three capability specs and run the complete offline suite plus `git diff --check`; verify all tests pass with no network access or real credentials.

## 6. Controlled Live Validation

- [ ] 6.1 After the user supplies `BLOTATO_API_KEY`, run only authenticated `inspect`, confirm no generation endpoint was called, and preserve the sanitized live schema and starting balance under ignored `outputs/`.
- [ ] 6.2 Present the discovered Nano Banana 2 Edit and image-to-video contracts, exact prompts, source image, and maximum credits for explicit user approval; verify no paid call occurs while approval is absent.
- [ ] 6.3 After separate approval, generate one bounded reference image, deliver it for visual review, and record the actual credit delta; verify animation remains blocked until that exact image is approved.
- [ ] 6.4 After separate image approval, generate one bounded video, create and deliver the full audit package, and verify no social-account or publishing endpoint was called.
