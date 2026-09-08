# Blotato Automations Lab

This repository is an experiment lab for making content people actually want to watch, then using Blotato to produce, publish, measure, and improve it.

The goal is not maximum posting volume. The goal is to discover repeatable content formats that earn attention and only then automate them.

## Operating model

```text
Audience signal -> content hypothesis -> small batch -> human review
       ^                                      |
       |                                      v
performance notes <- platform analytics <- publish with Blotato
```

Every automation should preserve these stages:

1. **Research:** collect real audience questions, pain points, trends, or proven source material.
2. **Create:** turn one insight into a native post, carousel, or short video.
3. **Review:** require approval until the format has repeatedly met its quality bar.
4. **Distribute:** adapt the idea for each platform instead of blindly duplicating one caption everywhere.
5. **Learn:** record views, retention when available, saves, shares, comments, and the creative variables that produced them.

## Repository map

- `research/` — current Blotato capabilities, official documentation, and evaluated community workflows
- `experiments/` — one folder per content hypothesis, including its brief, workflow, outputs, and results
- `workflows/` — reusable n8n, Make, MCP, or API workflows that passed an experiment
- `templates/` — prompts, review checklists, schemas, and platform adapters
- `assets/` — stable input assets used by experiments (never temporary clipboard files)
- `scripts/` — small API utilities and validation tools

## Recommended first build

Start with a **human-approved content lab**, not a fully autonomous content factory:

1. Submit a topic, link, transcript, or raw idea.
2. Extract the strongest audience-relevant insight.
3. Generate three hooks and one finished content asset.
4. Preview it and explicitly approve, revise, or reject it.
5. Publish to one primary platform and optionally adapt it to one secondary platform.
6. Capture results after fixed intervals and log what changed.

This is small enough to diagnose. Once one format wins consistently, move its approved workflow into `workflows/` and increase automation gradually.

The complete proposed infrastructure, channel-isolation rules, module interfaces, experiment design, and delivery phases are in [`docs/infrastructure-plan.md`](docs/infrastructure-plan.md).

The recommended initial audience, content pillars, workflow to adapt, and first 12-post test are in [`docs/ai-builder-content-system.md`](docs/ai-builder-content-system.md).

The paid-tool restriction, reference-media rules, and mandatory workflow/output audit are in [`docs/tooling-and-output-policy.md`](docs/tooling-and-output-policy.md).

The current evidence for exact assets, image references, consistent characters, Brand Kit behavior, and required live tests is in [`research/blotato-reference-media.md`](research/blotato-reference-media.md).

The current Blotato image, video, voice, and text-model catalog—with credit costs and outside-key exclusions—is in [`research/blotato-model-catalog.md`](research/blotato-model-catalog.md).

The evidence-ranked public output gallery, generation-versus-publishing distinctions, and quality verdict are in [`research/public-blotato-output-examples.md`](research/public-blotato-output-examples.md).

The real-user scan across the local Twitter/X and Reddit scrapers—including production accounts, direct outputs, and rejected promotional claims—is in [`research/real-user-blotato-reddit.md`](research/real-user-blotato-reddit.md).

The first-party website, catalog, brand-story, social-footprint, and claims-risk audit for Cinco H Ranch Naturals is in [`research/cinco-h-ranch-brand-audit.md`](research/cinco-h-ranch-brand-audit.md).

The proposed real-ranch content strategy, claims firewall, six-video test, and Blotato production loop for Cinco H Ranch Naturals are in [`docs/cinco-h-ranch-content-pipeline.md`](docs/cinco-h-ranch-content-pipeline.md).

The implementation-ready plan for the reusable, approval-gated Blotato brand automation skill is in [`openspec/changes/add-blotato-brand-automation-skill/`](openspec/changes/add-blotato-brand-automation-skill/).

## First three experiments

1. **Evidence-backed carousel** — turn a useful source into a concise tutorial carousel.
2. **Short-form explainer** — one strong hook, one idea, visual progression, and a clear payoff.
3. **Proven-content repurpose** — transform your own existing high-performing material into a platform-native variation.

Avoid beginning with generic news summaries, quote cards, or unattended AI-avatar volume. They are easy to automate but weak tests of whether an audience genuinely wants the content.

## Setup order

1. Read [`research/blotato-landscape.md`](research/blotato-landscape.md) and choose the first workflow to test.
2. Connect only the social account(s) needed for that test in Blotato.
3. Create a Blotato API key and store it in a local `.env`; never commit credentials.
4. Pick one orchestration path:
   - **MCP** for interactive experiments controlled through an AI agent.
   - **n8n** for reusable visual workflows, approvals, schedules, retries, and logging.
   - **REST API** for version-controlled custom code and tests.
   - **Make** only if that is already the preferred automation environment.
5. Import or clone one evaluated workflow before designing a new one.
6. Run with drafts or a private/test account first; enable unattended publishing only after validation.

## Quality gate

A piece should not publish unless it passes all of these:

- It serves a named audience and a specific need.
- The opening earns attention without making a false promise.
- It contains an original observation, useful synthesis, or real example.
- The format fits the destination platform.
- Claims are traceable to sources.
- Visuals and voice feel coherent rather than template-generated.
- The call to action follows naturally from the value delivered.

## Experiment record

Create each experiment from [`templates/experiment.md`](templates/experiment.md). Change only one or two major creative variables per batch so the outcome teaches us something.

## Security and cost rules

- Keep API keys and account IDs out of Git.
- Treat imported community workflows as untrusted code until reviewed.
- Put explicit approval before publishing and before expensive generation calls.
- Cap retries and polling loops; Blotato creation operations are asynchronous.
- Log request IDs and terminal status so failed jobs are observable and not accidentally duplicated.

The implemented local Pinterest research, creative brief and experiment-reporting workflow is documented in [`docs/pinterest-workflow.md`](docs/pinterest-workflow.md). Live account connections are separate readiness checks.
