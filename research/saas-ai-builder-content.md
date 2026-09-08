# Content automation for an AI/SaaS builder

_Research date: 2026-09-08. “Official” means a platform-owned page, repository, or API document. n8n gallery templates are public and reusable, but most are community-authored. Reddit examples below are firsthand anecdotes, not audited case studies._

## Decision

Build around one audience before choosing one SaaS product:

> **AI builder field notes: real demos, experiments, failures, and exact workflows for solo founders who want to ship useful automations.**

This is a better starting thesis than faceless generic AI news. It lets Drew create from work he is already doing, builds trust through visible artifacts, attracts the people who might later buy a builder/founder product, and turns audience questions into product research. The channel promise can remain stable even while the eventual SaaS changes.

Use **YouTube Shorts as the first controlled distribution surface**, then adapt proven episodes into LinkedIn posts/carousels and TikTok/Reels. This is not a claim that YouTube will always deliver the most views. It is the cleanest first lab because its official analytics expose `shown in feed`, `stayed to watch`, engaged views, average view duration, average percentage viewed, likes, comments, and subscriber change. YouTube says Shorts ranking considers whether people choose to watch, how long they stay, average percentage viewed, likes, and satisfaction signals; it does not favor a particular Short format or require a minimum posting cadence. [YouTube Shorts discovery guidance](https://support.google.com/youtube/answer/11914225), [YouTube Shorts analytics](https://support.google.com/youtube/answer/12220281)

Do **not** optimize for public view count alone. Since March 31, 2025, a public YouTube Shorts view counts whenever a Short starts or replays, with no minimum watch time; `engaged views` remains the better comparison measure for viewers who continued watching. [TeamYouTube view-count announcement](https://support.google.com/youtube/thread/333869549), [YouTube Shorts overview](https://support.google.com/youtube/answer/10059070)

## Why field notes beat generic AI news

| Criterion | AI builder field notes | Faceless generic AI news |
|---|---|---|
| Distinctive input | Drew's actual screen recordings, code, tests, decisions, costs, and failures | The same public stories and model summaries available to thousands of accounts |
| Credibility | Demonstrable: viewers can see the workflow and result | Requires fast fact-checking and often asks viewers to trust synthetic narration/B-roll |
| Product discovery | Comments expose recurring founder problems and desired automations | Attention generally attaches to the news topic, not to a problem Drew can solve |
| Monetization fit | Natural path to templates, tools, a newsletter, services, or a future SaaS | Often attracts broad, low-intent trend traffic |
| Automation fit | AI can extract a real build log, propose hooks, assemble evidence, and repurpose it | Easy to generate at volume, but generation itself supplies little defensibility |
| Main risk | Becoming a self-focused build diary with no viewer payoff | Commodity output, weak trust, copyright/factual risk, and audience mismatch |

The answer is not “never cover AI news.” Use a news item only when it becomes a **testable builder question**, such as “Can the new model actually replace this five-node workflow?” The content is then an experiment with evidence rather than a recap.

YouTube search currently shows strong demand for build/tutorial title families, including a public 2025 “How to Build & Sell AI Agents” tutorial with millions of views and newer “I built a SaaS app with AI” experiments. Those public counts demonstrate audience interest in the broad subject, but they do **not** prove a particular title, automation, or format caused the result; channel size, distribution history, topic, and production differ. [Example AI-agent tutorial](https://www.youtube.com/watch?v=w0H1-b044KY), [example build experiment](https://www.youtube.com/watch?v=bjasrMCTev4)

## Reusable Blotato and n8n assets

### First-party foundations

1. **Official Blotato n8n node.** The open-source community node exposes visual creation/status, media upload, publish/status, and source extraction/status. The npm README documents nine publishing platforms and the asynchronous create/poll pattern. Use credentials, not keys embedded in workflow JSON. [Official repository](https://github.com/Blotato-Inc/n8n-nodes-blotato), [npm package](https://www.npmjs.com/package/@blotato/n8n-nodes-blotato)
2. **Official Blotato skills.** The Blotato-owned repo contains eight reusable editorial procedures: `content-coach`, `brand-brief`, `post-writer`, `post-grader`, `post-scheduler`, `repurpose`, `viral-hooks`, and `generate`. The useful part for this project is the sequence `brand brief -> hooks -> writer -> grader -> human approval -> scheduler`, not blind installation. [Official skills repository](https://github.com/Blotato-Inc/blotato-skills)
3. **Official async workflow contract.** Blotato creation calls are submit/poll/result operations: sources finish as `completed`, visuals as `done`, and posts as `published`; explicit failure states must terminate retries. [Official workflow protocol](https://help.blotato.com/api/workflows)
4. **Current API/MCP surface.** The live MCP reference currently lists 35 tools, including credits, post inventory, analytics, comments/messages, and Instagram/Facebook DM automations. The newer REST analytics page says Blotato collects checkpoints for eight platforms—all supported destinations except LinkedIn—and exposes `GET /v2/analytics` and `GET /v2/posts/{id}/analytics`. The current n8n node does not expose those analytics actions, so an n8n implementation must use HTTP Request nodes. An older official FAQ still says analytics and engagement features are unavailable, and the MCP analytics section lists fewer platforms than the newer REST page. Treat those as documentation-version conflicts and verify the authenticated account. Native YouTube Studio is still required for `shown in feed`, `stayed to watch`, engaged views, average view duration, and average percentage viewed, which are the first experiment's decision metrics. [Current MCP tools reference](https://help.blotato.com/api/mcp/tools), [current REST analytics reference](https://help.blotato.com/api/analytics), [conflicting FAQ](https://help.blotato.com/support/faqs)

The current publish API supports X, LinkedIn, Facebook, Instagram, Pinterest, TikTok, Threads, Bluesky, and YouTube, including synthetic-media disclosure fields for TikTok and YouTube. Scheduling properties must be at the request root or the post may publish immediately. [Official publish reference](https://help.blotato.com/api/api-reference/publish-post)

### Community templates worth borrowing from

These are architectural starting points, not evidence that their output performs:

| Template | Reusable idea | What must change for Drew |
|---|---|---|
| [YouTube/text -> fact-check -> choose visual -> Telegram approval -> five platforms](https://n8n.io/workflows/13471-create-and-publish-ai-social-posts-to-multiple-platforms-using-blotato/) | Closest existing quality-gated content factory | Replace generic topic generation with build artifacts; use Discord approval; keep one platform enabled initially |
| [URL -> Blotato source extraction -> carousel/video -> Instagram/TikTok](https://n8n.io/workflows/13526-generate-ai-videos-and-carousels-with-blotato-for-instagram-and-tiktok/) | Clean official-node submit/poll/publish example | Add evidence extraction, grading, approval, timeouts, cost logging, and the YouTube branch |
| [Chat-controlled carousel to five platforms](https://n8n.io/workflows/8559-create-and-post-social-media-carousels-across-5-platforms-with-ai-and-blotato/) | Confirms copy and template before rendering | Do not enable all five outputs during tests; replace generic quote content with real field-note takeaways |
| [Scheduled GPT carousel -> Blotato -> Instagram](https://n8n.io/workflows/9597-create-and-publish-instagram-carousels-automatically-with-gpt-41-and-blotato/) | Simple hook/copy/render/status loop | Remove autonomous daily posting; its “viral” hook language is a prompt, not validation |
| [Telegram idea/URL -> platform copy + image -> LinkedIn/X/Instagram](https://n8n.io/workflows/16349-create-ai-social-posts-from-telegram-links-with-openai-grok-and-blotato/) | One source becomes genuinely platform-specific copy | Keep as a later repurposing branch after a Short proves the idea |
| [LinkedIn draft -> human approval -> Blotato](https://n8n.io/workflows/6827-ai-generated-linkedin-posts-with-human-approval-using-gpt-4-gotohuman-and-blotato/) | Small, understandable approval gate | Swap the review surface for Discord and log approval/revision history |
| [Technical article -> LinkedIn/X/Reddit/FAQ assets](https://n8n.io/workflows/15458-turn-any-article-into-social-content-with-gemini-olostep-and-google-docs/) | Useful later when a build has a real changelog, tutorial, or case study | It is a repurposer, not a discovery engine; do not manufacture a source article merely to feed it |

Public GitHub references are useful for inspection and recovery: Blotato maintains the [official node repository](https://github.com/Blotato-Inc/n8n-nodes-blotato) and [official skills repository](https://github.com/Blotato-Inc/blotato-skills); a third party publishes a [Veo/Blotato workflow repository](https://github.com/Systemapic-agency/Generate-Auto-post-AI-Videos-to-Social-Media-with-Veo3-and-Blotato-N8N); and a large unofficial mirror contains [raw n8n template JSON](https://github.com/zengfr/n8n-workflow-all-templates). A Reddit author also shared the JSON for a [viral-content research/analysis workflow](https://github.com/shabbirun/redesigned-octo-barnacle/blob/5161bf22d6bca58ff39d4c554f19d843f000b94a/AIO%20social%20media.json). Audit credentials, code nodes, HTTP destinations, licenses, and stale API fields before importing any of them.

n8n's page-level interest signals reinforce what to inspect, not what will succeed socially. At the research snapshot, a product-image/marketing-video template showed about 7,000 n8n page views, a video-ad cloning template about 2,300, a human-approved multi-platform template about 770, and a very recent Hacker News-to-AI-news-Shorts template only a few dozen. These numbers are neither output views nor fair comparisons because publication age and audience differ. [Product marketing template](https://n8n.io/workflows/12462-create-ai-product-images-and-marketing-videos-with-nanobanana-pro-veo-31-and-blotato/), [video-ad cloning template](https://n8n.io/workflows/13015-create-automated-video-ad-clones-with-nanobanana-kling-airtable-and-blotato/), [human-approved publisher](https://n8n.io/workflows/17010-create-and-approve-ai-social-posts-with-openai-telegram-and-blotato/), [Hacker News Shorts template](https://n8n.io/workflows/17311-create-ai-news-shorts-from-hacker-news-with-openai-atlascloud-and-blotato/)

## What the platforms themselves imply about format

- **Show the outcome immediately.** TikTok recommends hook/body/close, vertical high-resolution video, safe-zone awareness, platform-native presentation, and putting the value proposition early; it also cites product-on-screen demonstrations as effective. This is advertiser research, so use it as a testable creative principle rather than a guarantee for organic reach. [TikTok Creative Codes](https://ads.tiktok.com/business/en/blog/creative-best-practices-top-performing-ads)
- **Use real screen evidence.** LinkedIn's B2B guidance specifically suggests short guides to a time-saving hack and demonstrations of new technology, and says video creation is growing faster than other original post formats on LinkedIn. [LinkedIn B2B video guidance](https://www.linkedin.com/business/marketing/blog/content-marketing/13-top-tips-for-compelling-b2b-video-content-on-linkedin)
- **Measure audience quality as well as reach.** LinkedIn's native post analytics include impressions, distinct members reached, profile viewers, followers gained, reactions, comments, reposts, saves, sends, link visits, watch time, and average watch time. [LinkedIn post analytics](https://www.linkedin.com/help/linkedin/answer/a516971/post-analytics-for-your-content)
- **Do not equate frequency with quality.** YouTube says growth in views is not correlated with the time between uploads and advises choosing an appropriate length using both relative and absolute watch time. [YouTube performance FAQ](https://support.google.com/youtube/answer/141805)
- **Research current patterns without cloning creators.** TikTok's public Creative Center exposes trends, high-performing ads, and the point of strongest engagement. It is useful for collecting hook structures and visual grammar, not for copying scripts, footage, voices, or identities. [TikTok Creative Center overview](https://ads.tiktok.com/help/article/creative-center)

## Community evidence: useful but unverified

The following are firsthand reports. None supplied auditable account exports tying results to a particular workflow.

- A SaaS founder reported 2.5M TikTok views and roughly 90% of signups from TikTok, but said that audience churned quickly and often used the product for an unintended homework use case. The same author reported far fewer Reddit views but much stickier customers. The lesson is not that these exact numbers generalize; it is that maximizing raw views can select the wrong audience. [Reddit firsthand report](https://www.reddit.com/r/Entrepreneur/comments/17si8to)
- An n8n author shared a workflow that scrapes recent high-engagement Instagram, LinkedIn, and TikTok posts, transcribes/analyzes them, and generates new ideas. The workflow JSON is public and the Reddit post received substantial interest, but no output-channel analytics were provided. [Reddit workflow post](https://www.reddit.com/r/n8n/comments/1mpy4jg/i_built_a_social_media_automation_workflow_that/)
- A 2026 n8n author said a research/write/design/approval workflow saved about three hours per day and required only minimal editing. The workflow was not public and the engagement screenshot is not independently auditable. This supports the plausibility of production-time savings, not better content performance. [Reddit firsthand report](https://www.reddit.com/r/n8n/comments/1s5uymw/this_workflow_has_saved_us_a_at_least_3hday/)
- A recent discussion about self-improving social automation included a practical warning: one outlier can cause a learner to copy the wrong lesson, so store prompt, format, audience, and publish time, wait for a fixed window, and change one variable at a time. That is community advice, but it is sound experimental discipline. [Reddit discussion](https://www.reddit.com/r/n8n/comments/1vtta5z/has_anyone_built_a_self_improving_social_media/)
- The specific “Google Sheets -> Blotato Instagram visuals” community post described routing among carousel, whiteboard, text, and slideshow templates, then publishing and updating status. It had almost no public engagement and included no destination-account results. It proves that a downloadable implementation exists, not that the generated posts attract views. [Reddit post](https://www.reddit.com/r/n8n/comments/1r4njkv/i_automated_my_instagram_visuals_with_n8n_google/)

## Can any downloadable Blotato workflow be called “proven” by views?

**No—not from the public evidence found.**

- n8n template-page views, imports, and author claims measure interest in the automation, not views on the content it produces.
- GitHub stars/forks and Reddit votes measure developer/community interest, not downstream social performance.
- Blotato's homepage says its founder achieved hundreds of millions of views and a recent founder post claims 30M+ monthly views. Those are first-party aggregate marketing claims, not a public experiment with a pinned workflow, post cohort, native analytics export, denominator, and control. [Blotato homepage](https://www.blotato.com/), [founder LinkedIn post](https://www.linkedin.com/posts/sabrinaramonov_30m-monthly-views-8-platforms-100s-of-activity-7475619516513886208-Wujz)
- Public social view counts can confirm that a post was viewed, but generally cannot prove which workflow generated it or whether automation caused its performance.
- Cross-platform “views” are not directly comparable. YouTube changed Shorts counting to include starts/replays, while LinkedIn distinguishes impressions, members reached, and watch time.

The right response is to borrow implementation patterns and create **our own attributable evidence**.

## Recommended first workflow

Call it `builder-field-note-v1`:

```text
real build artifact
  -> evidence extractor
  -> one viewer problem + one demonstrated outcome
  -> three hook candidates
  -> 20–40 second script + shot list
  -> factual/quality gate
  -> rough preview
  -> Discord approve/revise/reject
  -> Blotato upload/publish to one allowlisted new YouTube channel
  -> native analytics snapshot at 24h and 7d
  -> experiment ledger + next-test proposal
```

### Input contract

Every episode must start with something real: a screen capture, terminal log, before/after timing, test output, small shipped feature, failed attempt, or a reproducible workflow. The intake record should include:

- what problem was attempted;
- who has that problem;
- what changed and what did not;
- a visible proof asset;
- tool/model versions and approximate cost/time;
- claims that need citations or must be removed.

No artifact means no episode. This single rule prevents the pipeline from turning into generic AI copy.

### Episode structure

Use one compact structure, while varying only the hook angle at first:

1. **0–2 seconds — result or failure on screen:** “I made an agent that rejects weak SaaS ideas before I code them.”
2. **2–7 seconds — founder pain/stakes:** why this wastes time or money.
3. **7–25 seconds — actual workflow/demo:** two or three visually distinct steps, with captions.
4. **25–35 seconds — honest result and limitation:** include what failed or remains manual.
5. **close — conversation CTA:** “What founder task should I test next?”

Do not fabricate the example line; use it only if that agent is actually built and shown.

### Quality gate

Reject before rendering when any of these is false:

- The first two seconds make sense without context.
- The viewer problem is specific to builders or solo founders.
- The result is visible, not merely asserted.
- The script makes one main claim and the evidence supports it.
- The episode reveals a constraint, tradeoff, failure, or exact step that generic AI news lacks.
- On-screen text is readable in 9:16 safe zones and works muted.
- The CTA asks for a useful next signal rather than begging for engagement.
- Publishing destination is a newly approved account ID; every existing connected channel remains denied.

## First experiment: 12 real field notes

Keep the visual grammar, length band, narrator, platform, and posting policy constant. Test three content angles with four real examples each:

1. **Outcome demo:** “I built X to do Y; here it is working.”
2. **Failure/postmortem:** “This agent failed at X; here is the exact reason/fix.”
3. **Timed challenge:** “Can an AI agent automate X in 30 minutes?”

Publish manually or through the approval gate to one new YouTube channel. Do not auto-cross-post the first cohort. Snapshot metrics after 24 hours and seven days, but make decisions on the fixed seven-day window.

Record per post: source artifact, audience problem, angle, hook text, script/prompt version, visual template, duration, cost/credits, publish timestamp/URL, shown in feed, public views, engaged views, stayed-to-watch rate, average view duration, average percentage viewed, likes, comments, shares if available, and subscriber change.

Use relative decisions until the channel has a baseline:

- Compare each Short with the cohort median, not a viral benchmark from another channel.
- Require at least three examples of an angle before treating it as a repeatable win.
- Scale an angle only when its median beats the cohort on both **stayed to watch** and **average percentage viewed**, without producing obviously irrelevant comments/subscribers.
- Change one major variable in the next batch: hook family, topic/problem, or presentation—not all three.
- A single spike is a lead for a follow-up test, not a mandate for the whole system.

After an episode wins twice, repurpose it into a LinkedIn field note/carousel using the same evidence. Track saves, sends, profile visits, follower gains, and link visits there; these are stronger signals of a useful builder audience than impressions alone.

## Infrastructure implications

The first build should therefore be smaller than a “content factory”:

- a source/artifact registry;
- an experiment ledger with immutable prompt/script/template versions;
- a Blotato adapter using create/poll/result with timeouts and idempotency;
- an account denylist plus explicit new-channel allowlist;
- a Discord approval/revision record;
- a credit/cost cap before render;
- native-platform metric import, beginning with YouTube Studio;
- a learner that proposes one next change but cannot publish it without approval.

The system's first job is not to create the maximum number of posts. It is to make each real build produce one measurable field note, preserve what happened, and learn which builder problems earn both attention and qualified response. That can later point toward the SaaS worth building.
