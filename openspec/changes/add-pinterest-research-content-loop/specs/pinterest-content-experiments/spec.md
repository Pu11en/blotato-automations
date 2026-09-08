## Purpose

Convert Pinterest research into original reviewable content experiments and measure attributable commercial outcomes.

## ADDED Requirements

### Requirement: Complete original briefs

Each brief SHALL include audience, keyword, source references, an original hook, static layout, timed video storyboard, exact product asset IDs, approved factual claims, destination, CTA, and explicit audio choice. Third-party media MUST remain reference-only unless reuse rights are documented.

#### Scenario: Brief export
- **WHEN** a candidate is selected
- **THEN** the exported Markdown and JSON identify production assets separately from creative references and include an image approval checkpoint before animation

### Requirement: Review and production boundaries

Research and brief creation SHALL default to zero paid spend and SHALL NOT publish. Optional generation SHALL use the existing approved Blotato runner contract and its credit and human-review gates. Changed assets or briefs SHALL invalidate previous approvals.

#### Scenario: No runner or approval
- **WHEN** production is requested without the runner, approved image, or required budget
- **THEN** the system exports the brief and states the unmet prerequisite without starting a paid job

#### Scenario: Visual rejection
- **WHEN** a product label, shape, claim, or sound choice fails review
- **THEN** the asset remains rejected and cannot be marked ready

### Requirement: Tracked experiment identity

Each asset SHALL have a stable experiment ID, version, format, and unique tracking URL linked to a verified product destination. Human publishing records SHALL associate the correct Pin with that asset.

#### Scenario: Destination unavailable
- **WHEN** the product URL is invalid or unavailable
- **THEN** the brief is marked blocked for distribution

#### Scenario: Version changes
- **WHEN** a new hook or asset version is created
- **THEN** the tracking identity changes while the earlier experiment remains intact

### Requirement: Commercial feedback integrity

Results SHALL separate impressions, saves, outbound clicks, sessions, orders, revenue, refunds, and production cost. Reports SHALL record metric windows, timezone, currency, and attribution method; missing data MUST NOT become zero. Re-imports MUST NOT duplicate results.

#### Scenario: Sparse or missing metrics
- **WHEN** metrics are absent or insufficient to compare experiments
- **THEN** the report labels the result insufficient evidence and does not declare a winner

#### Scenario: Repeated export
- **WHEN** the same analytics file is imported twice
- **THEN** reported totals remain unchanged

#### Scenario: Revenue attribution
- **WHEN** an order lacks a credible experiment association
- **THEN** it remains unattributed rather than being assigned from a temporal coincidence
