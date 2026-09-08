# Cinco H Ranch Naturals brand profile

`profile.json` and `claims.json` together form one logical brand profile validated against `schemas/brand-profile.schema.json`: merge `claims.json`'s `claims` object into `profile.json` under the `claims` key before validating or loading. They are kept as separate files so the claims firewall can be reviewed and changed independently of identity/facts/assets.

Sourced from `research/cinco-h-ranch-brand-audit.md` (audit snapshot 2026-09-08). Every fact and claim traces to a first-party URL from that audit; nothing here paraphrases the audit's Tier 3 / claim-risk-inventory language into an approved phrase.

`profile.json`'s `assets` array is intentionally empty. No product photos, phone clips, or label art have been ingested into this repository yet. Per the audit's "What a future system should ingest from the owner" section, `plan` and every spending mode must fail closed until real, rights-cleared assets are added here with accurate `provenance`/`rights`/`checksum_sha256` — never fabricate placeholder assets to unblock a run.
