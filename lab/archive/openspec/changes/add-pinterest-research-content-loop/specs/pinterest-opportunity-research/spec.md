## Purpose

Discover relevant Pinterest opportunities with traceable demand evidence and creative references.

## ADDED Requirements

### Requirement: Evidence provenance

Every signal SHALL retain source URL, retrieval time, source type, region, query, observation period, raw metric definition, and availability status. Normalized indices MUST NOT be presented as absolute search volumes.

#### Scenario: Trend import
- **WHEN** a supported trend response or manual evidence file is imported
- **THEN** the report preserves its measurement context and distinguishes observed values from inference

#### Scenario: Unavailable data
- **WHEN** authentication fails, the schema is unsupported, or evidence is missing
- **THEN** the report marks the source unavailable and does not invent growth values

### Requirement: Read-only reference collection

Research SHALL perform read-only collection, deduplicate by canonical Pin ID or URL, and preserve creator/source attribution. Download permission SHALL be distinct from rights to reuse media.

#### Scenario: Reference found
- **WHEN** a reference Pin is collected
- **THEN** its source and permissible use are recorded, with unknown rights classified as reference-only

#### Scenario: Restricted access
- **WHEN** a source rejects access or rate limits the collector
- **THEN** collection stops or uses bounded retries and reports incomplete coverage without bypassing access controls

### Requirement: Product-relevant shortlist

The system SHALL produce up to three ranked candidates with product destination, evidence, score breakdown, uncertainty, and creative rationale. It MUST label unsupported concepts exploratory and MUST NOT equate public saves or ranking with competitor clicks or sales.

#### Scenario: Insufficient evidence
- **WHEN** only one candidate meets relevance and evidence requirements
- **THEN** the report returns one qualified candidate and explains the shortfall rather than fabricating two

#### Scenario: Aesthetic mismatch
- **WHEN** a popular aesthetic lacks a credible connection to a verified product
- **THEN** the candidate is excluded from the qualified shortlist
