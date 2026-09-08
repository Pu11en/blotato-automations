# Blotato API contract rules

## The live template schema is the only capability authority

Blotato's public cost/price table lists models such as `nano-banana-2/edit` as available, but it does not prove that this account's live templates expose a usable source-image field for them. Treat the public price table as marketing evidence only.

`inspect` fetches and saves the full authenticated response of:

```
GET /v2/videos/templates?fields=id,name,description,inputs
```

`plan` may only select a template from that saved snapshot. A template counts as supporting an operation when its declared `inputs` include, in the same contract:

- **Image editing:** a source-image input field and a matching edit prompt/model field.
- **Image-to-video:** a source-image input field and a matching video model/mode field.

If no live template satisfies these conditions for the requested operation, `plan` reports the run as `unsupported` and stops before any spend. It never substitutes an assumed schema, and it never calls a separate, non-Blotato model provider as a fallback.

Model identifiers and template UUIDs are per-run data read from the live snapshot, not constants to hard-code — Blotato has changed these before.

## Credits

- Fetch the current balance during `inspect` (zero cost) and again immediately before and after every paid call.
- `plan` computes a cost estimate strictly from live template metadata. If no bounded estimate is available, generation is refused, not approximated.
- The user must state a positive `maxCredits` ceiling before any paid action. There is no default budget.
- After a paid call, record both the pre-call estimate and the actual observed balance delta. If a concurrent process appears to have spent credits during the same window, flag the ambiguity — never assert a precise per-job cost when concurrent spend is suspected.

## No automatic retries

- A failed or timed-out generation is never resubmitted automatically. The user must explicitly replan (which produces a new approval digest) to try again.
- Polling an existing request id is not a retry and never creates a new generation job.
- If Blotato completes a job after the local poll loop times out, the request id remains stored so a later `status`/poll can pick it up — never submit a duplicate request to "check."

## Credentials and secrets

- Read `BLOTATO_API_KEY` from the environment only. Never accept it as a CLI argument, log it, or write it into any saved artifact.
- Before saving or displaying any request or response, run it through a centralized sanitizer that strips (case-insensitively) authorization headers, cookies, API-key-shaped fields, and any other configured secret-like value, recursively through nested JSON.
- This skill never enumerates connected social accounts. Account discovery has no purpose here because publishing is out of scope for this version.

## Out of scope for this version

No publishing, scheduling, post creation, or social-account endpoints are called or exposed, even if explicitly requested. Report such requests as unsupported and stop after the authorized draft-generation scope.
