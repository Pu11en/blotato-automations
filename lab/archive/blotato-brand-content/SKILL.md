---
name: blotato-brand-content
description: Plan and run approval-gated Blotato image and video generation for an approved brand profile, starting with Cinco H Ranch Naturals. Inspects live Blotato credits and templates, builds a reviewable job plan, generates one approved reference image, animates one approved image into video, and produces run audit evidence. Never publishes, schedules, or touches connected social accounts.
---

# Blotato brand content

Turn an approved brand profile and a source product asset into one inspectable, credit-bounded Blotato generation run. This skill never publishes anything; it stops at an audited, human-reviewed image and video.

Read `references/modes.md`, `references/blotato-contract.md`, and `references/review.md` on demand — only load the one that matches the current mode, not all three every time.

## Select a mode before acting

State the selected mode out loud before running anything. The seven modes are:

| Mode | Spends credits | Purpose |
| --- | --- | --- |
| `inspect` | No | Fetch current Blotato credit balance and live `/v2/videos/templates` schema; save a sanitized snapshot. |
| `plan` | No | Validate the brand profile, source asset, claims, and a live template contract; produce a reviewable job plan with a stable approval digest and a positive `maxCredits` ceiling. |
| `generate-image` | Yes | Submit exactly the approved plan's image request and poll it to a terminal state. Requires an unexpired approval digest. |
| `approve-image` | No | Bind a human's actual approve/revise/reject decision to the generated image's checksum. Required before any animation step. |
| `animate-approved-image` | Yes | Submit exactly the approved plan's image-to-video request against the approved image checksum and poll it. |
| `audit` | No | Build run evidence: media checks, `ffprobe` metadata, a contact sheet when local tools exist, claims mappings, and a review form. |
| `status` | No | Report the current state of an existing run without creating any external work. |

See `references/modes.md` for exact inputs, outputs, and the run state machine that enforces this order (`INSPECTED -> PLANNED -> IMAGE_RUNNING -> IMAGE_READY -> IMAGE_APPROVED -> VIDEO_RUNNING -> VIDEO_READY -> AUDIT_READY`, with `FAILED`, `TIMED_OUT`, and `REJECTED` reachable from any generation or review step).

## Non-negotiable boundaries

- **No publishing.** This skill has no access to connected social accounts, scheduling, or post creation, even if asked. Report publishing requests as unsupported and stop after the authorized draft-generation scope.
- **No brand without a profile.** A spending mode without a valid, schema-passing brand profile under `brands/<brand>/` stops before generation and reports the missing fields.
- **No spend without a fresh approval digest.** `generate-image` and `animate-approved-image` refuse to run if the plan, source checksum, template snapshot, prompt, model, or `maxCredits` changed since the digest was issued. Never infer approval from earlier planning conversation; it must be an explicit, current decision.
- **No live template guessing.** Capability comes only from the authenticated `GET /v2/videos/templates` response saved during `inspect`, never from Blotato's public price table. If no live template exposes both a source-image input and the requested operation, `plan` reports the run as unsupported and stops.
- **Exactness is declared, not assumed.** Every plan states one render strategy — `reference-edit`, `exact-asset`, or `exact-overlay` — per `references/review.md`. Cinco product labels, logos, and founder identity default to `exact-asset` or `exact-overlay` unless the user explicitly tests `reference-edit` on a copy.
- **Credentials never leave the environment.** `BLOTATO_API_KEY` is read from the environment only, never accepted as an argument, and is stripped from every saved or displayed artifact along with any other credential-shaped field.

## Where things live

```text
skills/blotato-brand-content/   this skill
brands/<brand-id>/              profile.json, claims.json (tracked, reviewed brand facts)
schemas/                        brand-profile.schema.json, blotato-run.schema.json
outputs/blotato-runs/<run>/     one run's full evidence package (git-ignored)
```
