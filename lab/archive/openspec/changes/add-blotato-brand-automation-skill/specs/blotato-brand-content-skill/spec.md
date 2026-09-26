## Purpose

Provide a reusable Codex skill that turns approved brand facts and media into inspectable Blotato generation runs while preserving authorization, cost, and publishing boundaries.

## ADDED Requirements

### Requirement: Discoverable project-local skill
The project SHALL provide a `blotato-brand-content` skill whose description routes requests to inspect Blotato capabilities, plan a brand asset, generate a reference-guided image, animate an approved image, or audit an existing run. The skill and all of its maintained resources SHALL live inside this repository.

#### Scenario: Matching request selects the skill
- **WHEN** a user asks to create or evaluate brand content through Blotato
- **THEN** the skill identifies the appropriate supported mode and loads only the references required for that mode

### Requirement: Explicit operating modes
The skill SHALL distinguish non-spending `inspect` and `plan` modes from spending `generate-image` and `animate-approved-image` modes and the non-spending `audit` mode. It SHALL report the selected mode before acting.

#### Scenario: User asks for a plan
- **WHEN** a user requests a concept, prompt, shot list, or cost estimate without authorizing generation
- **THEN** the skill completes a `plan` run without calling a paid generation operation

#### Scenario: User asks for the full media chain
- **WHEN** a user explicitly authorizes image and video generation with a stated credit ceiling
- **THEN** the skill runs the image stage first and pauses for approval before any video-generation call

### Requirement: Brand profiles
The skill SHALL require a machine-readable brand profile for generation. A profile SHALL identify approved facts, blocked and review-required claims, visual identity rules, permitted assets, and provenance requirements. The first supplied profile SHALL represent Cinco H Ranch Naturals without hard-coding its rules into the generic workflow.

#### Scenario: Cinco profile selected
- **WHEN** the user selects Cinco H Ranch Naturals
- **THEN** the skill applies the Cinco facts, claims firewall, and exact-product rules to the plan and every generated output

#### Scenario: Brand profile is missing
- **WHEN** a spending mode is requested for a brand without a valid profile
- **THEN** the skill stops before generation and reports the missing profile fields

### Requirement: Structured job plan
Before a spending operation, the skill SHALL produce a reviewable job plan containing the source asset, prompt, selected live template, model or mode, expected output, maximum credit spend, approval checkpoints, and fallback behavior.

#### Scenario: Plan is ready for approval
- **WHEN** all required inputs and a compatible template are available
- **THEN** the skill displays the complete job plan and does not generate until the user explicitly approves that spending scope

### Requirement: Reviewable result handoff
The skill SHALL finish each mode with a concise status, stable artifact paths, credits estimated and consumed, unresolved risks, and the single next approval or action required.

#### Scenario: Image generation completes
- **WHEN** Blotato returns a successful generated image
- **THEN** the skill saves it locally, links its run evidence, reports actual credit change, and requests image approval without starting animation

### Requirement: No publishing capability in version one
The skill SHALL NOT expose or invoke social account discovery, scheduling, post creation, or publishing operations in its first version.

#### Scenario: User includes publishing in a generation request
- **WHEN** a request asks the version-one skill to publish or schedule the result
- **THEN** the skill completes only the authorized draft-generation scope and reports publishing as unsupported

