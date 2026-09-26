## Why

The project has researched Blotato's media models and designed a Cinco H Ranch content pipeline, but it does not yet have a repeatable way to turn an approved product image and prompt into a reviewable image-to-image then image-to-video run. A reusable Codex skill can make that workflow consistent, credit-bounded, inspectable, and safe for exact brand assets without introducing another paid API.

## What Changes

- Add a project-local `blotato-brand-content` Codex skill that can inspect the authenticated Blotato template catalog, plan a run, and execute one explicitly approved draft-generation job.
- Add a Blotato adapter that uses only the Blotato API key for paid image and video generation, polls asynchronous jobs to terminal state, and records credit balance and request evidence.
- Support a staged reference-image workflow: source image to a live-template-supported image-edit model, human image approval, approved image to a live-template-supported image-to-video model, then final media audit.
- Add a generic brand-profile contract plus an initial Cinco H Ranch profile containing factual language, prohibited claims, visual-identity rules, and asset provenance requirements.
- Persist each run's inputs, live template snapshot, outputs, metadata, contact sheet, costs, and decisions under an ignored output directory.
- Default to dry-run with a zero-credit ceiling. Require an explicit per-run budget before generation, and never retry a paid generation automatically.
- Exclude publishing from the first version. Existing connected social accounts remain inaccessible to the skill.

## Capabilities

### New Capabilities

- `blotato-brand-content-skill`: Discoverable Codex skill behavior, supported modes, brand-profile selection, inputs, outputs, and authorization boundaries.
- `blotato-media-runner`: Authenticated template discovery and bounded image-edit-to-video execution through Blotato, with asynchronous status handling and durable run evidence.
- `brand-content-safety`: Exact-asset, provenance, claims, credit, review, and no-publish gates applied before and after generation.

### Modified Capabilities

None.

## Impact

- Adds a project-local skill under `skills/blotato-brand-content/` with focused references and deterministic helper scripts.
- Adds machine-readable brand profiles and run schemas without requiring a database or n8n for the first slice.
- Uses the existing `.env` convention for `BLOTATO_API_KEY`; secrets remain untracked and must never appear in logs or saved request artifacts.
- Calls Blotato's credit and visual-template APIs, then only the generation endpoints supported by the selected live template.
- Uses free local inspection tools such as `ffprobe`/`ffmpeg` for output metadata and contact sheets when available.
- Does not publish, schedule, delete remote content, connect accounts, or call any separately billed model-provider API.
