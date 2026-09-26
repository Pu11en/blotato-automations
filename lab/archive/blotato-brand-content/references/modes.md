# Modes and the run state machine

Every run is a directory under `outputs/blotato-runs/<timestamp>-<brand-slug>-<short-id>/` with an atomic `state.json`. State advances monotonically and is never skipped:

```text
INSPECTED -> PLANNED -> IMAGE_RUNNING -> IMAGE_READY
  -> IMAGE_APPROVED -> VIDEO_RUNNING -> VIDEO_READY -> AUDIT_READY

Any generation step -> FAILED or TIMED_OUT
Any review step -> REJECTED
```

`FAILED`, `TIMED_OUT`, and `REJECTED` are terminal for that attempt. A new `plan` action starts a new run rather than mutating a dead one; nothing here retries automatically.

## `inspect`

- **Spends:** nothing.
- **Inputs:** none beyond `BLOTATO_API_KEY` in the environment.
- **Does:** fetches the current credit balance and `GET /v2/videos/templates?fields=id,name,description,inputs`, sanitizes both responses, and saves them with a retrieval timestamp.
- **Produces:** `credits.json`, `template-catalog.sanitized.json`, run state `INSPECTED`.
- **Stops if:** authentication fails, or the response cannot be parsed — reported plainly, never retried silently.

## `plan`

- **Spends:** nothing.
- **Inputs:** brand id, source asset reference, requested operation (image edit, image-to-video, or both), and the most recent `inspect` snapshot.
- **Does:** validates the brand profile against `schemas/brand-profile.schema.json`; matches the requested operation against a live template that exposes both a source-image input and the needed model/mode fields (see `blotato-contract.md`); computes a cost estimate from live metadata; requires the user to state a positive `maxCredits` ceiling; chooses a render strategy (see `review.md`); computes a stable approval digest over the sanitized plan.
- **Produces:** `plan.json`, run state `PLANNED`.
- **Stops if:** the profile is missing or invalid, no live template supports the operation, or no bounded estimate is available. It reports `unsupported` or the missing fields and does not fall back to an unverified template shape.

## `generate-image`

- **Spends:** yes — one image generation call.
- **Inputs:** the run id and the approval digest the user is confirming.
- **Does:** revalidates that the supplied digest matches the current plan exactly, revalidates the live balance covers `maxCredits`, submits exactly one request, persists the returned request id before polling, polls to a terminal state, downloads and checksums the result.
- **Produces:** `requests/*.sanitized.json`, `responses/*.sanitized.json`, `media/generated-image.*`, run state `IMAGE_READY` (or `FAILED`/`TIMED_OUT`).
- **Resume behavior:** if a request id is already stored for this run, poll it — never submit a second request for the same run.

## `approve-image`

- **Spends:** nothing.
- **Inputs:** the generated image checksum, and the human's actual decision (approve, revise, or reject) plus a reference to that decision (e.g. the message or session that made it).
- **Does:** binds the decision to that exact checksum. A stale, missing, or mismatched checksum blocks the decision from applying.
- **Produces:** updated `state.json` with `IMAGE_APPROVED` or `REJECTED`.
- **Never:** invents an approval from an earlier planning conversation. Only an approval recorded here unlocks `animate-approved-image`.

## `animate-approved-image`

- **Spends:** yes — one image-to-video call.
- **Inputs:** the run id; requires `IMAGE_APPROVED` state.
- **Does:** revalidates the live video template and the run's remaining credit ceiling, submits exactly one image-to-video request bound to the approved image checksum, polls without duplication, persists the video and the observed credit delta.
- **Produces:** `media/generated-video.*`, run state `VIDEO_READY` (or `FAILED`/`TIMED_OUT`).

## `audit`

- **Spends:** nothing.
- **Does:** verifies downloaded media, runs `ffprobe` for metadata, generates a representative frame or contact sheet when local tools exist, maps generated content back to claim ids from the brand profile, produces an identity checklist, and writes an approve/revise/reject review form.
- **Produces:** `audit/ffprobe.json`, `audit/contact-sheet.jpg` (when possible), `audit/review.md`, run state `AUDIT_READY`.

## `status`

- **Spends:** nothing.
- **Does:** reads and reports the existing `state.json` and stored artifacts. Creates no external work and calls no Blotato endpoint.
