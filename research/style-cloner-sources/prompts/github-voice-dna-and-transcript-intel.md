# artemnovitckii/content-skills voice-dna prompt + ScrapeCreators transcript-intelligence

- **Source URL:** https://github.com/artemnovitckii/content-skills/tree/main/voice-dna and https://github.com/ScrapeCreators/social-media-research-skills/tree/main/skills/transcript-intelligence
- **Commit:** 1c6e909c975b15d80f6ffcb0e2b60904b7da6656 (2026-06-20) and 64ba7b4dea71e130d2712ffb6c1c1024b3b7c4b2 (2026-08-26)
- **Author:** Artem Novitckii (Skool community 'artemis'); ScrapeCreators (transcript API vendor)
- **License:** MIT (both)
- **Stars / last push (checked 2026-09-18):** 99 stars / 2026-06-20; 2,519 stars / 2026-08-26
- **Evidence of success:** None verified for output quality. ScrapeCreators is a real paid scraping vendor; the skill calls its paid API (do not run).
- **Covers in our flow:** Voice-DNA: a compact extraction prompt from ~20 spoken transcripts (sentence shapes, signature phrases, openers, closers, anti-voice), every claim grounded in a quote. Transcript-intelligence: segmenting transcripts into hook/setup/claim/evidence/payoff/CTA and a cross-transcript pattern table.
- **Caveats:** Voice-DNA collects 'signature phrases verbatim' - fine for a creator's own voice, but for a competitor it invites copying; restrict to structure. Short-form oriented.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Verbatim: `voice-dna/README.md`

`````markdown
# Voice-DNA — teach Claude to write like *you*

The other four skills make good content. This one makes it **yours**.

Voice-DNA is the one skill you can't just download — you build it from your own content in about 2 minutes. You feed Claude ~20 of your real posts or video transcripts, it extracts how you actually sound (your sentence shapes, signature phrases, hooks, tics, and the things you'd *never* say), and saves it as a profile every other skill can read.

---

## How to build it (≈2 minutes)

1. **Gather your last ~20 posts.** Best input = **spoken transcripts of your own short-form videos** (how you actually talk), not just captions. Even 10 is enough to start; more = sharper.
2. **Paste them into Claude** with the prompt below.
3. **Claude returns a `voice-dna.md`** — a profile of how you sound: your sentence shapes, signature phrases, your hooks, your tics, and your anti-voice (what you'd never say).
4. **Save it as a skill** at `~/.claude/skills/voice-dna/SKILL.md` (wrap it with the template below). Now every piece Claude writes for you can read it and match your voice.

---

## The prompt (copy-paste — this is the magic)

```
You are building my VOICE-DNA — a reusable profile of how I actually write and talk, so you can
write in my voice later.

Below are 20 of my real posts / video transcripts. Read ALL of them first. Then build a profile.
Do NOT summarize what they're about — analyze HOW I express myself.

Output a single markdown file with these sections:

## How I sound
3–5 sentences on my overall register, energy, and pacing. Be specific and quote me.

## Sentence shapes
How I build sentences. Length patterns. Do I run thoughts together with "and/but/so," or write
short and clipped? Punctuation habits. Quote 3–4 real examples.

## Signature phrases & tics
The exact words, openers, transitions, and verbal habits that recur across my posts. List them
verbatim with the post they came from. Include filler/slang I actually use.

## How I open (hooks)
The patterns in my first lines. What kind of hook do I reach for? Quote my 5 strongest openers.

## How I close (CTAs / last lines)
How I end things. My real CTA style, word for word.

## Anti-voice (never do this)
Words, phrases, and moves that would instantly sound NOT like me. Be strict.

Rules:
- Ground every claim in a real quote from my posts. No generic adjectives.
- If I write differently when spoken vs. written, note the difference.
- Keep it tight enough to drop into a system prompt.

Here are my posts:
[PASTE 20 POSTS / TRANSCRIPTS HERE]
```

---

## Save it as a skill

Take the markdown Claude returns and save it at `~/.claude/skills/voice-dna/SKILL.md` with this frontmatter on top, so it installs and fires like the other four:

```
---
name: voice-dna
description: Use when writing ANY content in my voice — captions, scripts, posts, emails. Read this
  profile first and match my sentence shapes, signature phrases, hooks, and CTAs. Never write in a
  generic voice when this exists.
---

[paste the voice-dna.md the prompt produced here]
```

Now `storytelling`, `viral-hooks`, and `anti-ai-writing` all have a real voice to check against instead of falling back to mechanics alone.

---

## Pro tip

Re-run the prompt every few months as your content evolves — your voice drifts, and a fresh 20-post sample keeps the DNA current.

`````

## Verbatim: `skills/transcript-intelligence/SKILL.md`

`````markdown
---
name: transcript-intelligence
description: Use when the user wants to summarize, analyze, or repurpose transcripts from TikTok, Instagram, YouTube, Facebook, X/Twitter, LinkedIn, Rumble, or Reddit video posts. Extracts hooks, claims, quotes, content atoms, themes, and reusable scripts.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.0
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/social-media-research-skills
metadata:
  openclaw:
    requires:
      env:
        - SCRAPECREATORS_API_KEY
    primaryEnv: SCRAPECREATORS_API_KEY
    homepage: https://scrapecreators.com
    tags:
      - social-media
      - research
      - scrapecreators
---

# Transcript Intelligence

## Overview

Turn public video transcripts into useful research and content assets. This skill is for extracting signal from spoken social video: hooks, claims, stories, objections, examples, CTAs, and reusable content angles.

## When to Use

Use this skill when the user asks to:

- summarize a video, reel, short, TikTok, podcast clip, or social video
- analyze a creator's hooks or speaking style
- extract quotes, claims, examples, and CTAs from transcripts
- turn transcripts into social posts, scripts, newsletters, or content ideas
- compare what multiple creators say about a topic

## Transcript Sources

| Platform | Endpoint |
|---|---|
| TikTok | `/v1/tiktok/video/transcript` |
| Instagram | `/v2/instagram/media/transcript` |
| YouTube | `/v1/youtube/video/transcript`, `/v1/youtube/video` |
| Facebook | `/v1/facebook/post/transcript` |
| X/Twitter | `/v1/twitter/tweet/transcript` |
| LinkedIn | `/v1/linkedin/post/transcript` |
| Rumble | `/v1/rumble/video/transcript` |
| Reddit video | `/v1/reddit/post/transcript` |

If a detail endpoint already includes transcript text, use it. If transcript is unavailable, say so and fall back to title/caption/description only.

## Workflow

1. **Collect URLs or discover videos**
   - If URLs are provided, fetch each transcript directly.
   - If a creator/channel is provided, first fetch recent posts/videos, then choose relevant videos.

2. **Extract transcript text**
   - Preserve timestamps if provided.
   - Keep source URL with each transcript.
   - Do not hallucinate missing captions.

3. **Segment the transcript**
   Break into:
   - hook/opening
   - setup/context
   - main claim or lesson
   - evidence/examples
   - payoff
   - CTA

4. **Analyze the content**
   Extract:
   - exact hooks
   - claims and contrarian takes
   - stories
   - frameworks
   - objections addressed
   - emotional language
   - quotable lines
   - content atoms that stand alone

5. **Synthesize across multiple transcripts**
   - Cluster by topic and angle.
   - Count recurring themes.
   - Identify repeated hook formulas.
   - Flag the strongest examples with citations.

## Output Format

```markdown
# Transcript Intelligence Report

## TL;DR
- Main themes:
- Strongest hooks:
- Best reusable ideas:

## Transcript-by-Transcript Notes
### [Video title or URL](url)
- Hook: "..."
- Core idea: ...
- Best quote: "..."
- CTA: ...
- Content atoms:
  1. ...

## Patterns Across the Set
| Pattern | Evidence | Example URLs |
|---|---|---|

## Hooks Swipe File
- "..."
- "..."

## Repurposing Ideas
- LinkedIn post:
- X thread:
- Short-form script:
- Newsletter section:
```

## Common Pitfalls

- Do not summarize from the title alone if the user asked for transcript analysis. Fetch transcripts first.
- Do not lose exact wording. Hooks and quotes are more valuable verbatim.
- Do not treat AI-generated transcript text as perfect. If wording seems garbled, mark it as approximate.
- Do not mix source attribution. Every quote should trace back to a URL.

`````
