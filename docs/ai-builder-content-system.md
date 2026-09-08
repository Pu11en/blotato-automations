# AI Builder Content System

Status: proposed content direction  
Date: 2026-09-08

## Recommendation

Do not choose a random consumer niche yet, and do not make generic faceless AI news the main channel.

Start with one audience and one durable promise:

> **Audience:** builders, technical founders, and ambitious non-technical people using AI to create products and automations.  
> **Promise:** real AI builds, exact workflows, honest failures, and useful results—without pretending every weekend project is a million-dollar SaaS.

The niche is **practical AI building in public**. It fits what Drew already does, supplies original proof that generic content factories cannot reproduce, and creates a direct feedback loop for discovering a future SaaS business.

The product does not need to be chosen first. Audience questions, repeated friction, requested templates, and successful demonstrations become product-discovery inputs.

## Why this beats generic automation

Blotato and n8n have many workflows labeled “viral,” but the public templates generally document workflow mechanics—not independently verified view performance. They can automate production and distribution; they do not contain a defensible point of view or proof that an audience cares.

The content advantage should therefore come from source material no template can invent:

- a real thing built;
- a surprising result;
- a difficult failure and its fix;
- an honest time/cost comparison;
- a reusable workflow someone can copy;
- a user problem discovered while building.

LinkedIn's own 2025 video study supports a human, expert-led approach: its analyzed campaigns showed lifts for visible real people, subject-matter experts, authentic emotion, and contrarian expert perspectives. It also found that human-experience scripts outperformed abstract and product-led messaging. [LinkedIn, _The Art & Science of Video Storytelling_](https://business.linkedin.com/content/dam/business/marketing-solutions/global/en_US/site/pdf/wp/2025/the-art-and-science-of-video.pdf)

YouTube says Shorts are ranked using whether viewers choose to watch, average view duration, average percentage viewed, and enjoyment signals—not because a particular format or posting cadence is favored. That means the system should test audience response, not assume “AI video” is an advantage. [YouTube Shorts search and discovery guidance](https://support.google.com/youtube/answer/11914225)

## The five content pillars

### 1. Build proof

Show a working outcome immediately, then explain how it was made.

Examples:

- “I made one Discord message control four coding agents.”
- “This AI agent found the bug, wrote the fix, and proved it worked.”
- “I turned a messy manual process into this automation in one afternoon.”

### 2. Builder experiments

Test a claim that AI creators repeat and publish the result.

Examples:

- “Can an AI agent actually run this business process unattended?”
- “I gave three coding agents the same feature. Here is which one shipped.”
- “I spent 100 Blotato credits testing three content formats.”

### 3. Failure and fix

Start with the costly or ridiculous failure, then show the correction.

Examples:

- “My agents kept overwriting each other's work. This fixed it.”
- “The automation posted to the wrong account—so I built this safety gate.”
- “Vibe coding made the prototype fast and production painfully slow.”

### 4. Workflow teardown

Break down a real system so viewers can understand or copy it.

Examples:

- “The seven steps behind my AI content pipeline.”
- “What this popular n8n workflow gets right—and what I removed.”
- “How one prompt becomes a reviewed post without auto-publishing garbage.”

### 5. Build request

Invite the audience to supply problems, then build the strongest request.

Examples:

- “Give me the most annoying task in your business; I’ll automate one.”
- “Drop your SaaS. I’ll show where an agent fails to use it.”
- “Which of these three tools should I build next?”

This pillar turns attention into product research rather than forcing a SaaS idea prematurely.

## Content ladder

One real build should become a coherent package, not unrelated filler:

| Asset | Job | Default format |
| --- | --- | --- |
| Short demo | Earn discovery | 25–55 seconds, vertical, result first |
| Carousel | Teach the steps | 6–9 frames, one idea per frame |
| X/Threads post | Test the hook and claim | concise proof plus screenshot |
| LinkedIn post/video | Establish builder credibility | human context, lesson, evidence |
| Long-form YouTube | Capture durable search intent | only after a short/topic shows demand |
| Reddit post | Gather candid feedback | manual, community-specific, value first |

Reddit should be used as a research and conversation surface, not fed by an auto-poster. Repeated generic founder promotion is quickly perceived as spam, and community rules differ.

## Workflow to clone and reshape

The closest reusable base is n8n's community template [“Create and publish AI social posts to multiple platforms using Blotato”](https://n8n.io/workflows/13471-create-and-publish-ai-social-posts-to-multiple-platforms-using-blotato/). It already has source ingestion, fact-checking, multiple visual routes, approval, and Blotato publishing.

Use its structure, but make these changes:

1. Replace Telegram intake with a Discord command or a manually approved project brief.
2. Add a **Build Evidence Packet** containing screenshots, screen recordings, Git commit/PR links, test output, the builder's voice note, and facts safe to disclose.
3. Generate three story angles and hooks before generating media.
4. Require approval of the claim and hook before spending visual credits.
5. Prefer real screen evidence and Drew's narration; use Blotato visuals to clarify, package, and repurpose.
6. Remove every publish branch except the single new test channel.
7. Put the Channel Safety allowlist immediately before Blotato.
8. Add publication IDs, credit usage, and metric snapshots to the experiment ledger.
9. Produce platform-native adaptations rather than identical cross-posts.
10. Keep Reddit publication manual.

Useful secondary references:

- [Idea or URL → platform-specific posts](https://n8n.io/workflows/16349-create-ai-social-posts-from-telegram-links-with-openai-grok-and-blotato/) demonstrates a simple source-to-adaptation path.
- [WordPress → platform-specific posts](https://n8n.io/workflows/7395-auto-post-wordpress-articles-to-social-media-with-gemini-ai-and-blotato/) is useful later when a SaaS has documentation or a blog.
- [Blotato's official skills](https://github.com/Blotato-Inc/blotato-skills) supply brand-brief, hook, writer, grader, repurpose, generation, and scheduling procedures.
- Blotato's official API can extract YouTube, TikTok, article, PDF, audio, X, raw text, and Perplexity-query sources, then generate visual templates and publish asynchronously. [Official workflow documentation](https://help.blotato.com/api/workflows)

## What we should not clone as the main strategy

- Daily generic tech-news AI avatars: easy supply, weak differentiation, and no direct connection to Drew's builds.
- Random prompt-to-Veo posting: it tests spectacle rather than a useful audience relationship.
- “Post everywhere” from day one: it hides whether the topic, format, or platform caused the result.
- Product-heavy SaaS ads before product-market evidence: viewers care about the outcome and problem first.
- Automated viral cloning: it creates rights, reputation, and platform-reuse risks and teaches little about original demand.

These workflows can contribute implementation details later, but should not define the channel.

## First series to test

Series name: **I Built It With Agents**

Repeatable episode structure:

1. **0–2 seconds:** show the finished result or failure.
2. **2–7 seconds:** state the constraint or surprising claim.
3. **7–35 seconds:** show three concrete steps or turning points.
4. **35–50 seconds:** reveal the result, cost, time, or limitation.
5. **Final line:** ask for the next build/problem, not a generic follow request.

Initial topics can come from projects already being built, provided each project is explicitly approved for public disclosure. Do not crawl all local repositories automatically.

Candidate episodes:

1. The system that keeps multiple AI coding sessions from colliding.
2. Turning a Discord conversation into a tested feature branch.
3. An agent-readable architecture map generated from a real codebase.
4. A content pipeline that refuses to post to unapproved accounts.
5. Testing whether an off-the-shelf Blotato workflow can produce a watchable asset.

## First 12-post experiment

Use one newly created channel and one primary platform.

| Variable | Values |
| --- | --- |
| Story pillar | build proof, failure/fix, workflow teardown |
| Opening | result-first, painful-problem-first |
| Evidence style | screen demo, diagram/annotated screenshots |
| Fixed elements | audience, presenter identity, visual system, approximate length, CTA |

Create four posts per pillar. Do not render all twelve in advance; publish in batches of three so later scripts can incorporate early evidence.

Primary decision metrics:

- chose-to-view versus swiped away;
- engaged views rather than raw autoplay starts;
- average percentage viewed and average view duration;
- shares, saves, and substantive comments;
- returning viewers after enough history exists.

YouTube explicitly recommends comparing Shorts with Shorts, examining both winners and losers, and avoiding comparison of every post to one viral outlier. [YouTube Shorts analytics guidance](https://support.google.com/youtube/answer/12942217)

## Product-discovery loop

Every comment or request is classified as:

- a repeated pain;
- a requested tutorial;
- a request for the workflow/template;
- an objection or trust gap;
- a willingness-to-pay signal;
- noise.

When the same painful outcome appears repeatedly, create a manual concierge solution before building a SaaS. Content has then done two jobs: earned attention and supplied direct market evidence.

## What to build first

Build the **Builder Evidence Intake** before automated trend research.

Its input is one approved real build and its evidence. Its output is:

1. a truth-checked evidence summary;
2. three content angles;
3. six hooks (two per angle);
4. one short script and storyboard;
5. one carousel outline;
6. a disclosure/risk checklist;
7. an approval message with estimated Blotato cost.

Nothing publishes yet. This gives us a way to evaluate whether the content is genuinely interesting before creating channels or consuming a large credit balance.

