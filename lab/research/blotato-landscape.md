# Blotato landscape and recommended starting path

_Research date: 2026-09-07. “Official” means Blotato-owned documentation or repositories. “Community” means a third-party template listing, even when hosted in n8n’s official template gallery. Product details can change; verify plan limits and the live template catalog inside the account before spending credits._

## Executive recommendation

Do not begin by inventing a large autonomous content factory. The best reusable starting stack is:

1. **Install or inspect Blotato’s official integrations**: the official n8n node, MCP server, and new first-party Claude skills.
2. **Clone one proven workflow with a review gate**, preferably “Post Everywhere” for distribution or a source-to-carousel workflow for creation. Keep human approval before publishing while learning what earns attention.
3. **Build a measurement loop**, not merely a posting loop: idea/source → draft → grade/review → render → approve → publish → read views/reach/engagement → update the hook/format hypothesis.
4. **Run small controlled experiments** (for example, 3 concepts × 2 hooks, one format and audience at a time). Blotato’s recently documented post analytics can rank posts by views, reach, likes, or comments, which makes this much more useful than indiscriminate daily generation.

This direction matches the stated goal: automation should scale content that people already demonstrate they want, rather than scale unvalidated output.

## What Blotato officially supports now

### Core content pipeline

Blotato’s API can publish or schedule text, images, videos, reels, slideshows, carousels, threads, and stories. It can also generate images, videos, slideshows, and carousels from templates. API access is restricted to paying subscribers. The currently documented publishing destinations are X/Twitter, Instagram, LinkedIn, Facebook, TikTok, Pinterest, Threads, Bluesky, and YouTube. [Official API quickstart](https://help.blotato.com/api/start), [official account/platform reference](https://help.blotato.com/api/accounts)

Its reusable end-to-end primitive is:

```text
source extraction/research -> visual template generation -> publishing -> status/result
```

Source inputs include YouTube, TikTok, articles, PDFs, audio, X/Twitter, raw text, and a Perplexity research query. Visual templates can produce videos, carousels, quote cards, and infographics. These jobs are asynchronous and should be polled to a terminal state; successful publishing returns the public post URL. [Official workflow protocol](https://help.blotato.com/api/workflows), [official LLM API reference](https://help.blotato.com/api/llm)

Public image/video URLs may be sent directly when publishing, so an upload step is often unnecessary. Blotato also now documents presigned uploads for local files, avoiding intermediate Google Drive or S3 hosting. [Official quickstart](https://help.blotato.com/api/start), [official MCP tool reference](https://help.blotato.com/api/mcp/tools)

### Current integration surfaces

| Surface | Best use | Verification |
|---|---|---|
| **Blotato UI** | Connect accounts, Brand Kit, browse/test visual templates, edit generated videos, inspect API requests/errors | Official docs recommend browsing templates in the app and using the API Dashboard for payload/error inspection. [Visual guide](https://help.blotato.com/api/n8n/n8n-slideshows-and-carousels) |
| **REST API v2** | Maximum control and versionable custom workflows | Official base URL is `https://backend.blotato.com/v2`; authentication uses the `blotato-api-key` header. [Quickstart](https://help.blotato.com/api/start) |
| **Official n8n node** | Best first orchestration choice for cloning/community workflows | Supports Post Publish/Get, Media Upload, Visual Create/Get, and Source Create/Get. Blotato says n8n Cloud users can enable Verified Community Nodes; self-hosted users can install the package. [Official node guide](https://help.blotato.com/api/n8n/n8n-blotato-node), [official source repository](https://github.com/Blotato-Inc/n8n-nodes-blotato) |
| **Official Make app** | Simpler hosted no-code alternative | Make documents Create Post, Create/Get/Delete Visual, Get Post, Upload Media, and arbitrary API calls. [Make’s Blotato app docs](https://apps.make.com/blotato) |
| **Blotato MCP server** | Natural-language operations from Claude Desktop/Code, Cursor, or another MCP client | Connects at `https://mcp.blotato.com/mcp` with the API-key header. The current official reference lists **35 tools**. [Claude Code setup](https://help.blotato.com/api/claude-code), [MCP tools](https://help.blotato.com/api/mcp/tools) |
| **Official Claude skills** | Reusable editorial and scheduling procedures | Blotato’s public repo currently contains eight skills and was updated in Aug. 2026. It targets Claude’s plugin system; for Codex, inspect and adapt the procedures instead of assuming drop-in compatibility. [Official repository](https://github.com/Blotato-Inc/blotato-skills) |

The official quickstart says Zapier is “coming soon,” so it should not be a foundation until a working public integration is verified. [Official API quickstart](https://help.blotato.com/api/start)

### Notable recent additions (verified in current official docs)

The current MCP reference has expanded to 35 tools, including capabilities that older summaries of Blotato omit:

- **Performance analytics:** list top posts and rank by views, reach, likes, or comments; retrieve metric history for a post. At present the docs say analytics collection covers X/Twitter, Instagram, Facebook, Threads, and Bluesky—not TikTok, LinkedIn, Pinterest, or YouTube. [Official MCP analytics reference](https://help.blotato.com/api/mcp/tools#analytics)
- **Post inventory and calendar control:** list published/scheduled/failed posts; list, inspect, update, or cancel scheduled posts. [Official MCP reference](https://help.blotato.com/api/mcp/tools#content-calendar)
- **Instagram/Facebook engagement:** list and reply to comments; read conversations/messages; send DMs or private comment replies, including buttons and quick replies. [Official MCP comments/messages reference](https://help.blotato.com/api/mcp/tools#comments)
- **DM automations:** create/manage comment- or message-triggered flows with optional Instagram follow gate, email gate, buttons, and webhook, plus run logs and analytics. Replies count against the plan’s active-contact limit. [Official MCP automation reference](https://help.blotato.com/api/mcp/tools#automations)
- **Instagram trial reels, first comments, YouTube playlists and thumbnails, and threaded posting** across X/Twitter, Bluesky, and Threads are represented in the current publish tool. [Official MCP publishing reference](https://help.blotato.com/api/mcp/tools#publishing)
- **Credit visibility:** read remaining credits and current purchase pricing through MCP. Buying returns a Stripe Checkout URL and does not itself charge the account. [Official MCP credit reference](https://help.blotato.com/api/mcp/tools#credits)

These are “recent” in the sense that they appear in official pages updated within roughly the last month and in the expanded current tool reference. Blotato does not expose a clear public product changelog in the sources found, so precise launch dates remain **unclear**.

## First-party reusable assets to use before building from scratch

### Official Claude skills (newest/highest-leverage asset)

The Blotato-owned `blotato-skills` repository provides:

- `content-coach`: beginner front door/orchestrator
- `brand-brief`: captures business, customer, CTA, story, and voice
- `post-writer`: writes and grades a platform post
- `post-grader`: scores a draft and identifies the top three fixes
- `post-scheduler`: schedules through Blotato
- `repurpose`: turns long-form material into a week of content
- `viral-hooks`: 100 hook frameworks
- `generate`: creates a faceless AI video using a still-image quality check and budget check, animates through Kie.ai, then hands off to Blotato

Install instructions for Claude Code are in the repository (`/plugin marketplace add Blotato-Inc/blotato-skills`, then `/plugin install blotato@blotato-skills`). The repository explicitly says the skill files are generated from Blotato help pages. [Official Blotato skills repository](https://github.com/Blotato-Inc/blotato-skills)

**Recommendation for this Codex folder:** clone the repository into a vendor/reference area or record a pinned commit, audit every instruction/script, and port only the useful workflow logic into native Codex skills. The most valuable sequence is `brand-brief -> viral-hooks -> post-writer -> post-grader -> human approval -> post-scheduler`; it directly addresses quality before volume.

### Official n8n/Make workflow library

Blotato’s own automation library currently lists these reusable patterns:

1. beginner source extraction and publishing walkthrough;
2. Google Sheets/Drive “Post Everywhere” to nine platforms;
3. email idea → polished long-form thread;
4. Hacker News → AI clone videos with HeyGen;
5. niche news research → AI avatar videos with Perplexity/ChatGPT/HeyGen;
6. chat-controlled carousel generation and posting;
7. viral Reel analysis/rewrite → branded AI avatar Reel;
8. TikTok → watermark-free cross-posting;
9. TikTok → carousel + long-form threads, with email approval before LinkedIn;
10. Gamma branded presentations/carousels → social publishing.

These are first-party-curated and include downloadable workflow files, but they can depend on paid third-party services and may require credential/node updates. [Official automation templates](https://help.blotato.com/api/templates)

Blotato also publishes focused n8n guides/templates for [faceless videos](https://help.blotato.com/api/n8n/n8n-faceless-videos), [slideshows/carousels](https://help.blotato.com/api/n8n/n8n-slideshows-and-carousels), and a [Google Sheets social scheduler](https://help.blotato.com/blog/build-social-media-scheduler-n8n-make).

## Community workflows worth evaluating

These are downloadable from n8n’s template gallery, but authored by community members; their performance claims, security, API payloads, and credit economics are not verified by Blotato or by this research.

| Candidate | Why it is useful | Caveat |
|---|---|---|
| [YouTube/text → fact-check → multi-format visual → Telegram approval → five platforms](https://n8n.io/workflows/13471-create-and-publish-ai-social-posts-to-multiple-platforms-using-blotato/) | Closest match to a quality-first content factory; includes explicit fact checking and human approval | Complex and uses extra vendors; inspect every credential and HTTP node |
| [Telegram idea → Blotato research → visual → Instagram/LinkedIn](https://n8n.io/workflows/13409-create-an-ai-content-agent-with-telegram-gemini-and-blotato-no-code/) | Clear implementation of the official async Source/Visual/Post pattern | Add approval before publish and robust timeout/error paths |
| [Google Sheets/Drive publishing queue](https://n8n.io/workflows/7187-automate-content-publishing-to-tiktok-youtube-instagram-facebook-via-blotato/) | Low-risk first proof that account IDs, upload, publishing, and status updates work | Distribution only; it does not solve content quality |
| [Scheduled Instagram carousel with GPT + Blotato](https://n8n.io/workflows/9597-create-and-publish-instagram-carousels-automatically-with-gpt-41-and-blotato/) | Narrow format experiment that is easy to benchmark | Fully autonomous by default; add grading/approval |
| [Article → vertical Seedance video → TikTok/Instagram/YouTube](https://n8n.io/workflows/16606-create-vertical-ai-videos-from-web-articles-with-openai-seedance-and-blotato/) | Recent modular example using an external video generator and Blotato for distribution | Extra model costs; article rights and factual accuracy require review |
| [News RSS → HeyGen avatar video → Blotato](https://n8n.io/workflows/8050-generate-and-publish-ai-news-avatar-videos-with-heygen-and-blotato/) | Demonstrates trend selection, scripting, rendering, and optional publishing | “Viral” selection is a prompt claim, not evidence of outcomes; news needs source verification |

A useful warning from conflicting community documentation: some older templates say Blotato’s community node requires self-hosted n8n, while Blotato’s current official guide explicitly supports n8n Cloud through **Verified Community Nodes**. Follow the current official install guide and test in the actual n8n account. [Official n8n node guide](https://help.blotato.com/api/n8n/n8n-blotato-node)

## Suggested project course of action

### Phase 0 — inventory without spending credits

- Record the Blotato plan, remaining credits, connected social accounts/page IDs/boards, active-contact allowance, and expiration/rollover rules as shown in the live account.
- Export or list the live visual-template catalog; template IDs and inputs are account/API-discoverable and can change.
- Decide one audience, one promise, one primary platform, and one measurable success criterion (for example, median 7-day views and saves/replies—not posting volume).
- Create a Brand Brief and a small “do not publish” policy (unsupported claims, duplicate posts, copyright uncertainty, sensitive topics).

### Phase 1 — prove publishing safely

- Clone the official “Post Everywhere” or Sheets scheduler.
- Use one connected test account/platform, one already-approved media asset, and a scheduled/private/unlisted destination where the platform allows it.
- Log request ID, template/prompt version, credits used, publish URL, and failure details.
- Never store API keys inside downloaded workflow JSON; use n8n/Make credentials or environment-backed secrets.

### Phase 2 — quality-gated content experiment

- Start with **carousels or quote/infographic cards**, which are faster to inspect and compare than fully generated video.
- Generate 3 concepts, keep at most 1; generate 2–3 hooks for that concept; grade against audience relevance, specificity, credibility, novelty, clarity, and payoff.
- Render only the approved version. Require human approval in Telegram/email/n8n before publication.
- Use native platform-specific captions rather than identical cross-post copy.

### Phase 3 — close the loop

- After an appropriate observation window, collect views/reach/likes/comments with Blotato analytics where supported; manually import TikTok/YouTube/LinkedIn metrics until Blotato supports them.
- Compare results by hook, topic, template, length, platform, and posting window. Promote formats only after repeated wins, not one outlier.
- Use comments and DMs as qualitative signals for questions, objections, and follow-up topics. Add DM automation only after response language and active-contact economics are reviewed.

### Phase 4 — scale cautiously

- Add video only after a repeatable topic/hook combination wins in cheaper formats.
- Put hard daily/weekly credit caps, per-run idempotency, polling timeouts, and failure alerts around every creation workflow.
- Keep source attribution and transformation rights with every content record; “viral cloning” should extract structure and audience insight, not copy footage, wording, or a creator’s likeness.

## What to capture in this repository

```text
research/          dated platform/docs/community findings
vendor/            pinned, audited upstream templates/skills (or manifests + source URLs)
skills/            local quality, brand, research, grading, and publishing procedures
workflows/         n8n/Make exports with secrets removed
templates/         prompts, rubrics, approval messages, platform payloads
experiments/       hypothesis, variant IDs, credit cost, post URLs, metrics, decision
```

For every imported asset, store: source URL, author/owner, license if stated, retrieval date, upstream version/commit, external dependencies/costs, required credentials, platforms, and an audit note. A public template being downloadable does **not** establish that all bundled media/prompts are licensed for commercial reuse.

## Open questions that require the live account

- Exact credit balance, rollover/expiry behavior, per-template credit cost, and current plan limits.
- Which visual templates and AI models are available on this subscription today.
- Which accounts are connected and whether Instagram/Facebook messaging permissions need reconnection for newer features such as postback buttons.
- Whether analytics history exists for posts created before the newer analytics tooling.
- Whether the user prefers n8n or Make; n8n currently has the richer reusable ecosystem found in this review.

## Bottom line

The most promising “clone first” path is the **official Blotato skills + official n8n node + a community workflow with human approval**, then add the newly documented analytics as a learning loop. Use Blotato as the source/render/publish/measure layer; keep editorial judgment and evidence-based iteration as explicit gates. That spends the accumulated credits on tested creative hypotheses instead of an unmeasured stream of content.
