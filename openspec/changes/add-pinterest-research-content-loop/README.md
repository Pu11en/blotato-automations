# Pinterest research-to-content build plan

Prepared for Cinco H Ranch Naturals, September 8, 2026. Status: planning complete; implementation has not started.

## What you get

A conversational research skill that finds relevant Pinterest demand and creative references, explains which opportunities fit the store, and creates three original content briefs. Each brief connects to a real product page. A results report shows which experiments earn outbound clicks, attributed orders and revenue.

## Build sequence

| Stage | Deliverable | Completion check |
| --- | --- | --- |
| 1. Connect | Read-only OpenCLI reference search, Pinterest Trends adapter, manual import fallback | One live sample or clearly reported unavailable access; no invented trend data |
| 2. Research | Dated evidence report and ranked opportunities | Every recommendation has sources, product fit and uncertainty |
| 3. Direct | Three briefs with static layouts, timed storyboards and sound choices | Original concepts; exact product assets; factual claims and working destinations |
| 4. Prepare a test | Production request for one concept as a static Pin and short video | Human review, unique tracking links and any generation budget approved |
| 5. Learn | Pinterest and website export imports with 7/14/30-day reports | Clicks, visits, orders and revenue stay distinct; repeat imports cannot inflate results |

The software MVP ends at reviewable briefs/production exports and results reporting. Rendering uses the separate planned Blotato runner when available. Publishing is manual and requires an explicitly authorized account. No paid calls or public posts are included in this planning work.

## First experiment

Start with US product-intent searches such as handmade soap, tallow soap, unwhipped tallow cream and soap gifts. These are seed queries, not claims that they are trending now. Select from the evidence we actually obtain; do not force an unrelated aesthetic onto a product.

Produce three candidate briefs, then select one concept for a static Pin and a roughly 12-second video. Use the same product, promise and destination to make comparison useful. Real product photography stays authoritative. Review label accuracy, composition, text and sound before distribution. One pair gives an initial signal; it does not establish a repeatable winner.

## Tools and cost

- OpenCLI: proposed open-source reference collector, subject to a live smoke test.
- Official Pinterest Trends: preferred demand data; access still needs verification.
- Local Python and files: run storage, validation, experiment tracking and export imports.
- Existing Codex session: evidence interpretation and creative direction through the skill.
- Blotato: optional later production through the existing runner and approved credits.
- pinterest-dl: optional later retrieval of owned/licensed assets, not a mandatory dependency.

No new paid SaaS or direct paid generation provider is introduced. The initial build does not need a hosted app or unattended scheduler.

## Inputs needed for the live pilot

The build can begin using fixtures and manual imports. Live readiness requires the Pinterest access check, approved product facts and original assets, an authorized brand/test account for eventual distribution, and website analytics exports that preserve attribution. Any paid generation also needs the existing runner and an explicit credit ceiling.

## Detailed implementation artifacts

- [Proposal](proposal.md): scope and capabilities.
- [Design](design.md): architecture, data contracts, decisions, limitations and research sources.
- [Tasks](tasks.md): ordered implementation checklist with verification per task.
- [Research requirements](specs/pinterest-opportunity-research/spec.md).
- [Content and measurement requirements](specs/pinterest-content-experiments/spec.md).

The existing media-generation plan remains separate and unchanged. This plan makes Pinterest the primary channel for this experiment.
