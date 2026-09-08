# View-Driven Content Automation Infrastructure

Status: proposed  
Date: 2026-09-08

## Outcome

Build a system that discovers promising content opportunities, runs controlled creative experiments on brand-new channels, learns from performance, and spends more Blotato credits only on formats that show repeatable demand.

The system can optimize for views, but it cannot guarantee them. Its job is to increase the number and speed of useful experiments while preventing low-quality volume, accidental publishing, and unmeasured credit spend.

## Non-negotiable channel safety

The social accounts currently connected to Blotato are out of scope.

- Publishing begins in `dry-run` mode.
- The publish allowlist begins empty.
- Only newly created experiment-channel IDs may enter the allowlist.
- Every channel must have an owner-entered label, niche, platform, and `experiment` environment.
- No workflow may accept an arbitrary account ID at publish time.
- The first ten posts on a new channel require explicit human approval.
- Deleting or disconnecting existing accounts is a separate, manually approved operation.

## Recommended foundation

Use **n8n as the orchestrator**, **Postgres as the experiment ledger**, **Blotato as a replaceable creation/publishing adapter**, and **Discord as the approval and notification surface**.

Why this combination:

- Blotato maintains an official n8n node, and the largest reusable workflow library is in n8n.
- A durable ledger is necessary to connect every generated asset to its hypothesis, prompt version, credit cost, publication, and measured result.
- Discord is already where decisions are being made, so approvals should arrive here rather than in another dashboard.
- Blotato remains behind a seam so the research, scoring, quality, and learning modules are not coupled to one vendor.

```text
Signals and sources
       |
       v
Opportunity Radar ---> Experiment Designer ---> Content Studio
       ^                       |                       |
       |                       v                       v
Learning Engine <------- Experiment Ledger <---- Quality Gate
       ^                       |                       |
       |                       v                       v
Metrics Collector <------ Publisher <---------- Discord approval
                               |
                               v
                   allowlisted new channels only
```

## Deep modules and interfaces

Each module hides substantial behavior behind a small interface. Tests and callers use the same seam.

### 1. Channel Safety

Interface:

- `authorize(channel)` — add a verified new experiment channel to the allowlist.
- `assertPublishAllowed(channelId)` — either returns the channel record or blocks publication.

Implementation hides account discovery, environment labels, deny rules, audit logs, and kill switches. This is the only path to a publishing adapter.

### 2. Opportunity Radar

Interface:

- `proposeOpportunities(window, limit)` — returns ranked, evidence-linked opportunities.

Implementation may inspect audience questions, search demand, public trend signals, competitor formats, comment patterns, and the team's own results. It returns a hypothesis, not a copied post.

### 3. Experiment Designer

Interface:

- `designExperiment(opportunity)` — returns a bounded test with audience, promise, format, variants, budget, and success rule.

Implementation enforces that a batch changes only one or two major variables. It rejects experiments that cannot teach us anything measurable.

### 4. Content Studio

Interface:

- `draft(experiment)` — returns reviewable variants and provenance.
- `render(approvedDraft)` — returns final media plus actual credit usage.

Implementation may use Blotato visual templates, the official Blotato editorial procedures, or external media generators. Generation happens after inexpensive text/storyboard review whenever possible.

### 5. Quality Gate

Interface:

- `review(draft)` — returns `approve`, `revise`, or `reject`, with reasons.

Implementation checks specificity, opening strength, payoff, novelty, factual support, rights risk, platform fit, and brand coherence. Machine grading assists but never substitutes for human approval during calibration.

### 6. Publisher

Interface:

- `publish(approvedAsset, channelId, schedule)` — returns a publication record.

Implementation handles Blotato's asynchronous submit/poll/result protocol, idempotency, retries, platform payloads, and public URLs. It must call Channel Safety first.

### 7. Metrics Collector

Interface:

- `snapshot(publication, age)` — appends normalized metrics at a defined observation age.

Implementation uses Blotato analytics where supported and platform-specific or manual adapters elsewhere. Raw snapshots are retained so later metric corrections do not erase history.

### 8. Learning Engine

Interface:

- `recommendNext(batch)` — returns `scale`, `iterate`, or `stop`, plus the next variable to test.

Implementation compares medians and distributions by niche, topic, hook, format, length, template, channel age, and posting window. One viral outlier cannot automatically promote a format.

## Durable experiment ledger

Start with these records:

| Record | Purpose |
| --- | --- |
| `channels` | Allowlisted experiment channels, platform, niche, creation date, status |
| `opportunities` | Evidence, audience problem/desire, source date, score |
| `experiments` | Hypothesis, controlled variables, budget, success rule |
| `variants` | Hook, script, prompt/template versions, provenance, review state |
| `assets` | Stable media location, checksum, render status, credits used |
| `approvals` | Human decision, reviewer, timestamp, reasons |
| `publications` | Channel, platform, Blotato submission ID, URL, timestamps |
| `metric_snapshots` | Publication age, views, reach, watch/retention, shares, saves, comments |
| `credit_events` | Estimated and actual spend by operation and experiment |
| `learnings` | Decision, confidence, evidence, and next test |

## State machine

```text
OPPORTUNITY -> DESIGNED -> DRAFTED -> CONTENT_APPROVED -> RENDERED
    -> PUBLISH_APPROVED -> SCHEDULED -> PUBLISHED -> MEASURED -> DECIDED

Any review stage -> REVISE or REJECT
Any external job -> FAILED (with retry eligibility and diagnostic record)
```

Only state transitions can trigger side effects. Replaying an event must not create duplicate renders or posts.

## How we choose niches without caring which niche wins

Do not pick a niche based only on personal preference or one viral example. Score opportunities using:

1. **Demand:** repeated questions, active searches, and existing view volume.
2. **Supply gap:** room to improve on clarity, entertainment, recency, or format.
3. **Repeatability:** at least 50 plausible topics without stretching.
4. **Production fit:** can be made credibly with accessible sources and rights-safe media.
5. **Monetization optionality:** useful later, even though views are the first objective.
6. **Platform fit:** natural match to a platform's consumption behavior.

Select three candidates, document evidence, then test. A starting test should use one primary platform so platform effects do not blur the niche comparison.

## Initial experiment design

### Stage A: cheap concept test

- Three candidate niches.
- Two repeatable content formats per niche.
- Five topics per format.
- Hooks and scripts reviewed before any expensive rendering.

This creates 30 approved-or-rejected concepts, not necessarily 30 rendered posts.

### Stage B: channel test

- Create one new channel for each surviving niche.
- Publish a consistent minimum batch on the same primary platform.
- Measure at fixed ages such as 24 hours, 72 hours, and 7 days.
- Compare median views, view velocity, completion/retention when available, shares, saves, and substantive comments.

### Promotion rule

A niche-format pair is promoted only when it beats the declared baseline across multiple posts. It then earns a larger credit allowance and more automation. Losing pairs are revised once or stopped.

## Credit controls

- Global daily and weekly limits.
- Per-experiment budget fixed before rendering.
- Estimate displayed in the approval message.
- Actual credit event recorded after every generation.
- No unbounded polling or retries.
- Stop automatically when a limit is reached.
- Reserve most credits for winning formats; early discovery should be text/storyboard-heavy.

## Repository layout after implementation

```text
apps/
  worker/                 durable job runner and scheduled metric collection
modules/
  channel-safety/
  opportunity-radar/
  experiment-designer/
  content-studio/
  quality-gate/
  publisher/
  metrics-collector/
  learning-engine/
adapters/
  blotato/
  discord/
  postgres/
  platform-metrics/
workflows/n8n/
schemas/
templates/
experiments/
research/
docs/
```

Do not create all of these as empty scaffolding. Add each module only when its first working slice is built.

## Delivery phases

### Phase 0 — account isolation and inventory

- Confirm the live Blotato plan, credits, templates, and connected accounts.
- Export an inventory without posting.
- Mark all existing account IDs denied.
- Create the empty allowlist and global kill switch.
- Decide which single platform will host the first channel test.

Exit condition: a dry run proves an existing account cannot receive a post.

### Phase 1 — safe publishing spine

- Run n8n with durable storage.
- Add the experiment ledger and secret management.
- Import the official Blotato node.
- Add Discord approval.
- Publish one already-approved test asset to one newly created channel.
- Record submission, final URL, status, and credit use.

Exit condition: one end-to-end post is observable and repeat-safe.

### Phase 2 — opportunity and creative lab

- Build the niche scorecard and collect evidence for three candidates.
- Adapt Blotato's brand brief, hook, writer, and grader procedures.
- Generate cheap concepts and drafts.
- Render only approved variants.

Exit condition: the first bounded batch is ready for new channels.

### Phase 3 — measurement loop

- Collect metrics at fixed observation ages.
- Normalize platform-specific metrics without pretending unavailable metrics are zero.
- Produce batch comparisons and next-test recommendations.

Exit condition: every published post produces an evidence-backed decision.

### Phase 4 — winner scaling

- Increase cadence only for repeatable winners.
- Add a second platform using native adaptation.
- Automate approvals gradually based on a documented confidence threshold.
- Keep random quality audits and the kill switch.

Exit condition: higher throughput does not lower median performance or quality.

## Decisions required before implementation

1. Choose the first platform for new test channels. Short-form video is portable, but YouTube Shorts generally provides better durable discovery and clearer retention data; TikTok or Instagram Reels may provide faster creative feedback.
2. Confirm whether n8n already exists and where it runs. If not, provision it with Postgres rather than building custom orchestration first.
3. Decide whether approvals should happen in this Discord server or a dedicated private approval channel.
4. Inspect the live Blotato account before disconnecting anything; record IDs first so the denylist can be verified.

## First build slice

Build only this vertical path first:

```text
manually entered approved idea
  -> experiment record
  -> draft and quality review
  -> Discord publish approval
  -> Channel Safety allowlist
  -> Blotato publish adapter in dry-run
  -> one new test channel
  -> publication record and metric snapshots
```

This path proves the dangerous and valuable parts—approval, account isolation, publishing, cost tracking, and measurement—before adding automated niche research or high-volume generation.

