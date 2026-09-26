## Purpose

Prevent unapproved spending, unsupported claims, identity distortion, secret exposure, and accidental publication while brand media is generated and reviewed.

## ADDED Requirements

### Requirement: Fail-closed claims gate
The system SHALL classify every factual line and on-screen claim against the selected brand profile before paid generation. Unknown, blocked, or review-required language SHALL stop until explicitly resolved.

#### Scenario: Blocked health claim appears
- **WHEN** a Cinco H Ranch script contains an automated disease, healing, sunscreen, pest-repellent, pain-relief, or other blocked efficacy claim
- **THEN** the system rejects the script before it is sent to Blotato and identifies the blocked text

#### Scenario: All claims are approved
- **WHEN** every factual line maps to an approved brand fact or approved sensory statement
- **THEN** the claims gate records the mappings and allows the job to continue to its spending approval

### Requirement: Source provenance
Every supplied brand image, logo, label, customer asset, or recording SHALL have a stable local copy, checksum, source, capture or retrieval date, and permission status before it can enter a generation job.

#### Scenario: Asset permission is unknown
- **WHEN** a customer image, testimonial, or identifiable person lacks permission evidence
- **THEN** the system excludes that asset from generation

### Requirement: Exact-identity distinction
The system SHALL distinguish exact pass-through or deterministic composition from AI reference editing. It SHALL never describe a generated or animated label, package, face, or logo as exact unless the authoritative original asset remains unmodified in the final composition.

#### Scenario: Reference edit changes a label
- **WHEN** human review finds altered product lettering, container shape, logo, or product appearance
- **THEN** the image is rejected for brand use and cannot be approved for animation

#### Scenario: Exact product asset is required
- **WHEN** the job marks product identity as exact
- **THEN** the system uses the original product asset directly or as a deterministic overlay rather than relying on model reconstruction

### Requirement: Explicit credit ceiling
Every paid run SHALL require a positive user-approved maximum credit amount and SHALL stop before any operation whose estimated cost would exceed either the run ceiling or remaining approved balance.

#### Scenario: Video would exceed remaining budget
- **WHEN** the selected video model's estimate is greater than the run's unspent approved credits
- **THEN** the system refuses the video call and presents lower-cost compatible alternatives

### Requirement: No automatic paid retries
The system SHALL NOT automatically retry a paid image or video generation, even when the previous request failed or produced an unacceptable result.

#### Scenario: Output is rejected for quality
- **WHEN** a reviewer rejects an output
- **THEN** the system records the reasons and requires new approval for any revised paid attempt

### Requirement: Secret-safe evidence
The system SHALL load credentials from the local environment, redact authentication headers and secret-like values from all logs, and prevent credentials from being written into tracked or output artifacts.

#### Scenario: Request record is persisted
- **WHEN** the runner saves a sanitized request
- **THEN** the record contains no API key, authorization token, cookie, or complete secret value

### Requirement: Human media review
The system SHALL create an audit package for every generated video containing playable media, technical metadata, representative frames, claim mappings, identity observations, credit usage, and an approve/revise/reject decision record.

#### Scenario: Video generation succeeds
- **WHEN** a video reaches its successful terminal state
- **THEN** the system creates the audit package and leaves the run awaiting explicit final review

### Requirement: Publishing isolation
The system SHALL contain no callable publishing or scheduling path and SHALL avoid fetching connected social account identifiers in version one.

#### Scenario: Compromised or mistaken input requests a social account
- **WHEN** a job payload includes an account ID, publish time, or post target
- **THEN** validation rejects those fields rather than ignoring or forwarding them

