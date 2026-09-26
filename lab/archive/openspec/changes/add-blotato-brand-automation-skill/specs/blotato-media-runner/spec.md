## Purpose

Execute bounded Blotato image and video generation stages through live template contracts while producing durable, inspectable evidence for every external operation.

## ADDED Requirements

### Requirement: Blotato-only paid dependency
The runner SHALL authenticate paid media operations only with `BLOTATO_API_KEY` and SHALL reject workflows requiring a direct key for Fal, Google, OpenAI, Replicate, Runway, Kling, ElevenLabs, or any other separately billed provider.

#### Scenario: Blotato-routed model is available
- **WHEN** a compatible model is exposed by the authenticated Blotato template catalog
- **THEN** the runner may select it through the Blotato request without requiring the model provider's key

#### Scenario: Template requires an outside credential
- **WHEN** inspection discovers a direct external-provider credential or hostname in the generation path
- **THEN** the runner rejects the path before generation and records the prohibited dependency

### Requirement: Live capability discovery
Before planning or generating, the runner SHALL fetch the current credit balance and authenticated visual-template schemas, save a timestamped snapshot, and validate selected inputs against the live template rather than a hard-coded model list.

#### Scenario: Nano Banana 2 Edit exposes a source-image contract
- **WHEN** the live template schema offers Nano Banana 2 Edit together with documented source-image and prompt inputs
- **THEN** the runner marks reference editing as supported and includes the exact input contract in the job plan

#### Scenario: Reference input is not exposed
- **WHEN** no live template provides the required source-image and prompt inputs for the requested edit model
- **THEN** the runner returns `unsupported` without spending credits and offers exact-asset composition or pass-through as the fallback

### Requirement: Staged reference-image generation
The runner SHALL accept a stable source image, verify its accessibility and checksum, submit at most one approved image-generation request by default, poll it to a documented terminal state, and persist the resulting image before any animation begins.

#### Scenario: Reference edit succeeds
- **WHEN** the approved image request reaches a successful terminal state
- **THEN** the runner stores the source, request metadata, response identifiers, output image, and credit delta in one run directory

#### Scenario: Image request fails
- **WHEN** the image request reaches failure or the polling deadline
- **THEN** the runner records the failure and stops without an automatic paid retry or video request

### Requirement: Approval-gated image-to-video generation
The runner SHALL accept only an image previously marked approved in the same run or explicitly imported with approval evidence before submitting an image-to-video request.

#### Scenario: Approved image is animated
- **WHEN** the user approves the stored image, a compatible image-to-video template is live, and sufficient budget remains
- **THEN** the runner submits one video request, polls it to terminal state, and saves the final media and request evidence

#### Scenario: Image is not approved
- **WHEN** the image approval record is absent, rejected, or does not match the source checksum
- **THEN** the runner refuses to create the video

### Requirement: Bounded asynchronous operations
The runner SHALL use bounded polling with terminal-state handling, persist state after each response, and SHALL NOT interpret an unknown or non-terminal status as success.

#### Scenario: Generation remains in progress
- **WHEN** the polling time limit is reached before a terminal state
- **THEN** the runner marks the run `timed-out`, preserves the external request ID for later inspection, and performs no duplicate submission

### Requirement: Durable run package
Each run SHALL have a stable unique identifier and preserve sanitized requests, template snapshots, asset checksums, state transitions, Blotato IDs, downloaded results, media metadata, credit observations, and approval decisions under the ignored output root.

#### Scenario: Run is resumed
- **WHEN** the skill resumes a run after interruption
- **THEN** the runner reads the existing state and polls the known external job instead of creating another generation

### Requirement: Credit accounting
The runner SHALL record the balance before and after each generation and SHALL distinguish estimated cost from observed account balance change.

#### Scenario: Documented price and observed balance disagree
- **WHEN** the observed credit delta differs from the planned estimate
- **THEN** the runner flags the discrepancy in the audit and uses the observed delta in the run total

