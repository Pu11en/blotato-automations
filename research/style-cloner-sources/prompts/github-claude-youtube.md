# AgriciDaniel/claude-youtube: retention-engineered script sub-skill + retention scripting guide

- **Source URL:** https://github.com/AgriciDaniel/claude-youtube
- **Commit:** 84c3fa6805200632fadb4fe2795ef265511271c7 (2026-04-10)
- **Author:** Daniel Agrici (AI Marketing Hub on Skool, youtube.com/@AgriciDaniel, 2.9k GitHub followers; also author of claude-ads, 9.4k stars)
- **License:** MIT
- **Stars / last push (checked 2026-09-18):** 379 stars / 2026-04-10
- **Evidence of success:** Author credibility via other popular Claude skill repos. No evidence the script template itself was tested on a channel. Guide cites stats (e.g. 'suspension bridge = 68% higher completion', 'AI narration = 70% lower retention') with no primary sources - treat as UNVERIFIED.
- **Covers in our flow:** Script writing (hook grab/promise/stakes, forward hooks, pattern-interrupt log, mid-CTA at 25%, re-hook at 60%) and a built-in grading checklist ('Quality Criteria'). Competitor sub-skill pulls transcripts via DataForSEO (paid) or YouTube API.
- **Caveats:** Written for face-on-camera creators ([CAMERA CHANGE] cues). No style-cloning step: tone is a single input field.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Verbatim: `skills/claude-youtube/sub-skills/script.md`

`````markdown
# Retention-Engineered Script

This sub-skill generates a full video script engineered for maximum audience retention, using proven structural patterns — hook-promise-stakes openings, pattern interrupts, forward hooks, and strategic CTAs — all calibrated to the target video length and audience type.

## Inputs Required

| Input | Required | Description |
|-------|----------|-------------|
| Topic | Yes | Video subject matter |
| Target length | Yes | Desired video duration in minutes |
| Channel type | Yes | Educational, entertainment, vlog, review, tutorial, commentary, etc. |
| Audience persona | Yes | Who is watching (age range, knowledge level, why they clicked) |
| Key points | Yes | Core information/arguments to cover (bullet list) |
| Tone | No | Casual, professional, energetic, conversational (default: conversational) |
| CTA goal | No | Subscribe, product, community, or custom (default: subscribe) |

## Reference Files

- `references/retention-scripting-guide.md`
- `references/algorithm-guide.md`

## Parallel Agents

Not required. This skill runs as a single sequential workflow.

## Execution Steps

1. **Load references**: Read `references/retention-scripting-guide.md` and `references/algorithm-guide.md` fully before writing.
2. **Calculate structure**: Based on target length, compute section durations. Hook: 0:00-0:30. Intro: 0:30-2:00. Mid-CTA: ~25% mark. Retention re-hook: ~60% mark. Outro: final 60 seconds. Remaining time divided among content blocks.
3. **Map key points to chapters**: Assign the provided key points to content blocks. Order them by engagement potential — strongest points early and late, weaker points in the middle (surrounded by pattern interrupts).
4. **Write the hook block**: Produce the 3-part hook (Grab, Promise, Stakes) targeting >70% retention at the 30-second mark.
5. **Write the intro**: Bridge from hook to content. Establish context, stakes, and viewer outcome.
6. **Write content blocks**: Each block opens with a pattern interrupt, delivers value, ends with a micro-summary and forward hook to the next section.
7. **Insert pattern interrupts**: Place one every 60-90 seconds. Mark each with its type tag.
8. **Place CTAs**: Soft mid-CTA at ~25%, hard CTA in outro.
9. **Write outro**: Hard CTA, end screen cue, next video tease.
10. **Annotate retention risks**: Scan the full script for drop-off danger zones. Mark each with a warning symbol and mitigation note.
11. **Add pacing notes**: Insert editor directions throughout.

## Output Template

```
## Script Metadata

- **Topic**: [topic]
- **Target length**: [X] minutes ([Y] words at ~150 words/minute)
- **Channel type**: [type]
- **Audience**: [persona summary]
- **Estimated word count**: [total words]

---

## HOOK (0:00 — 0:30) | Target: >70% retention at 0:30

### Grab (0:00 — 0:05)
[Opening line — the single most important sentence in the video]

[PACING: Deliver fast. No intro graphics. Start mid-thought or mid-action.]

### Promise (0:05 — 0:15)
[What the viewer will get from watching. Specific, tangible outcome.]

### Stakes (0:15 — 0:30)
[Why it matters. What they lose by clicking away. Emotional or practical consequence.]

⚠️ RETENTION RISK: [If applicable — e.g., "Generic promise language. Make the outcome hyper-specific."]

---

## INTRO (0:30 — 2:00) | Context + Credibility

[CAMERA CHANGE]

[Context paragraph: Why this topic, why now, why from this creator.]

[Viewer outcome restatement: "By the end of this video, you'll..."]

[PACING: Moderate. Establish trust but don't linger. Viewers who survived the hook want content.]

---

## CONTENT BLOCK 1: [Chapter Title] (2:00 — X:XX)

[GRAPHIC: Chapter title card]
[Pattern interrupt: opening line that resets attention]
[Core content — spoken-word style: short sentences, direct address ("you"), rhetorical questions.]
[B-ROLL CUE: Describe what should appear on screen]
[Micro-summary: One sentence recap] → [Forward hook: "But that's only half the picture..."]
⚠️ RETENTION RISK: [If applicable — e.g., "Dense info block. Break with visual at 4:30."]

---

## CONTENT BLOCK 2: [Chapter Title] (X:XX — X:XX)

[SOUND EFFECT: Transition sting]
[Pattern interrupt] → [Content delivery] → [UNEXPECTED STAT]
[Micro-summary] → [Forward hook]

---

## MID-CTA (~25% mark, approximately X:XX)

[CAMERA CHANGE] [Soft CTA — conversational, tied to content just delivered. 10-15 seconds max.]
> "If you're finding this useful, hit subscribe — I break down [niche topic] like this every [cadence]."

---

## CONTENT BLOCKS 3+: [Chapter Titles] (X:XX — X:XX)

[Continue pattern: interrupt → content → B-ROLL → micro-summary → forward hook]

## RETENTION RE-HOOK (~60% mark, approximately X:XX)

[CAMERA CHANGE] [Why the remaining content is the most valuable part.]
⚠️ RETENTION RISK: [60% mark is a common drop-off cliff. This re-hook must feel like a second hook.]

---

## OUTRO (final 60 seconds, X:XX — end)

### Hard CTA (15 seconds)
[Direct call-to-action tied to the video's value delivery.]

> "[Specific CTA: subscribe, comment a specific thing, check link in description]"

### End Screen Cue (15 seconds)
[GRAPHIC: End screen overlay]

> "If you liked this, you'll want to watch [related video topic] — I'll put it right here."

[Point to end screen card position]

### Next Video Tease (15 seconds)
[Brief, compelling preview of the suggested next video. Create a mini curiosity gap.]

[PACING: Keep energy up through the final second. No "thanks for watching" wind-down.]

---

## Pattern Interrupt Log

| Timestamp | Type | Description |
|-----------|------|-------------|
| X:XX | [CAMERA CHANGE] | [Brief note] |
| X:XX | [B-ROLL CUE] | [Brief note] |
| X:XX | [GRAPHIC] | [Brief note] |
| X:XX | [SOUND EFFECT] | [Brief note] |
| X:XX | [UNEXPECTED STAT] | [Brief note] |

**Total pattern interrupts**: [X] | **Average interval**: [X] seconds

## Retention Risk Map

| Timestamp | Risk Level | Issue | Mitigation |
|-----------|------------|-------|------------|
| X:XX | ⚠️ High | [Description] | [Solution] |
| X:XX | ⚠️ Medium | [Description] | [Solution] |

## Editor Notes

- [Pacing guidance for specific sections]
- [Music/sound design suggestions]
- [Cut rhythm recommendations]
- [Thumbnail moment candidates with timestamps]
```

## Quality Criteria

- Word count must match target length at ~150 words per minute (within 10% tolerance)
- The hook must contain all three elements: Grab (0-5s), Promise (5-15s), Stakes (15-30s)
- Pattern interrupts must appear every 60-90 seconds — verify by checking the interrupt log timestamps
- Every content block must end with both a micro-summary AND a forward hook
- Mid-CTA must appear at approximately the 25% mark, not earlier
- Retention re-hook must appear at approximately the 60% mark
- All production cue tags must use the exact bracket format: [CAMERA CHANGE], [B-ROLL CUE], [GRAPHIC], [SOUND EFFECT], [UNEXPECTED STAT]
- At least 3 retention risk points must be identified and marked with mitigations
- The script must read as natural spoken language, not written prose — short sentences, contractions, direct address
- The outro must never contain filler phrases like "thanks for watching" or "don't forget to" — maintain energy to the final second

`````

## Verbatim: `skills/claude-youtube/references/retention-scripting-guide.md`

`````markdown
# Retention & Scripting Guide

## Table of Contents

- [Hook Framework](#hook-framework)
- [Hook Benchmarks](#hook-benchmarks)
- [Pattern Interrupts](#pattern-interrupts)
- [Energy Patterns](#energy-patterns)
- [Optimal Video Length by Format](#optimal-video-length-by-format)
- [Retention Graph Diagnosis](#retention-graph-diagnosis)
- [Algorithmic Promotion Thresholds](#algorithmic-promotion-thresholds)
- [CTA Placement & Conversion](#cta-placement--conversion)
- [Key Constraints & Gotchas](#key-constraints--gotchas)

---

## Hook Framework

### Viewer Loss Data

- **55%** of viewers lost in the first 60 seconds
- **20%** lost in the first 10 seconds
- Videos with a **value proposition in the first 15 seconds** = 18% higher retention at the 1-minute mark

### Hook Structure (First 30 Seconds)

| Timestamp | Purpose | Action |
|-----------|---------|--------|
| 0:00-0:05 | Attention grab | Visual/verbal pattern break, bold claim, or unexpected moment |
| 0:05-0:15 | Clarify promise | State exactly what the viewer will get |
| 0:15-0:30 | Stakes/context | Why this matters, what they'll miss |

---

## Hook Benchmarks

| Metric | Threshold | Assessment |
|--------|-----------|------------|
| Retention at 10-15s | Below 50% | Hook is failing |
| Retention at 30s | 70%+ | Solid |
| Retention at 30s | 80%+ | Exceptional |

- **Never open with** "Hey guys welcome back" -- causes instant, measurable drop-off

---

## Pattern Interrupts

### Impact Data

- Pattern interrupt in **first 5 seconds** = **23% higher retention**
- Strategic breaks at drop-off points = **15-22% re-engagement** (Wistia)
- Adobe tutorials using pattern interrupts = **43% higher completion**

### Recommended Frequency

| Format | Interrupt Frequency |
|--------|-------------------|
| Pre-recorded | Every 30 seconds |
| Live | Every 2-3 minutes |
| Shorts | Every 2-3 seconds |

### Interrupt Types

- Camera angle change
- Sound effects / music shift
- Text pop-ups / lower thirds
- Unexpected facts or stats
- Format shifts (talking head to B-roll, screen share to whiteboard)

---

## Energy Patterns

Source: AIR Media-Tech, 5 documented patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Gradual Slowdown** | High energy open, gradually decreasing | Short content, impact pieces |
| **Calm-Burst Oscillation** | 15-25s calm, then energy burst every 2-3 min | Educational, tutorials |
| **Anchor Pattern** | Return to core thesis every 2-3 min | Long-form essays, explainers |
| **Strategic Pauses** | Deliberate silence/slowdown before key points | Storytelling, dramatic content |
| **Progressive Energy** | High first 3 min, stabilize, mix variety after min 8 | Vlogs, entertainment |

---

## Optimal Video Length by Format

| Format | Optimal Length | Notes |
|--------|---------------|-------|
| Tutorials | 7-15 min | Step-by-step pacing |
| Entertainment / Vlogs | 8-12 min | Energy management critical |
| Educational | 15-25 min | Anchor pattern recommended |
| Gaming (edited) | 10-20 min | Pattern interrupts essential |
| Product reviews | 8-15 min | Front-load verdict for retention |
| Podcasts | 30-90 min | Calm-Burst Oscillation works well |
| Shorts | 15-30s | Peak completion rate range |

### Length vs Performance

- **5-10 min** = peak retention at **31.5%**
- **Shorts** account for **75% of views** on the platform
- Videos **20+ min** capture **57% of total watch time**
- **8-minute threshold** unlocks mid-roll ads = ~**50% revenue increase**

---

## Retention Graph Diagnosis

| Pattern | Visual Shape | Diagnosis | Fix |
|---------|-------------|-----------|-----|
| **Sharp cliff** | 20%+ lost in first 15s | Hook failure | Rebuild 0:00-0:15 |
| **Steady decline** | Gradual downward slope | Normal/expected | Optimize pacing |
| **Mid-video valley** | Dip at 40-60% mark | Pacing issue | Add pattern interrupt or reorder content |
| **Spikes/bumps** | Upward blips | Rewatch moments | Create more of these intentionally |
| **Suspension bridge** | High retention through open loops | Excellent scripting | **68% higher completion** |
| **Sawtooth** | Zigzag from pattern interrupts | Active re-engagement | **43% higher completion** |

---

## Algorithmic Promotion Thresholds

- Videos outperforming channel average retention by **15%+** receive **2.3x more algorithmic promotion**
- A **10 percentage point retention improvement** = **25%+ impression increase**
- **AI narration** = **70% lower retention** vs human-fronted content

---

## CTA Placement & Conversion

### Viewer Reach Data

- Only **16%** of viewers reach the final 10% of a video
- At **~1 min mark**: ~60% of viewers still watching
- At **~4 min mark**: ~35% of viewers still watching

### Best Practices

| Strategy | Impact |
|----------|--------|
| Place CTA after first value delivery (1-3 min) | Catches majority of viewers |
| Embedded CTAs (visual + verbal) | **380% conversion increase** over verbal-only |
| With CTA: 1 sub per 33 views | **2.5x better** than without CTA (1 per 83 views) |
| "Join the family" vs "subscribe" | **150% growth boost** |

### Dual CTA Strategy

- **First CTA** at ~1 min = reaches ~60% of viewers
- **Second CTA** at ~4 min = reaches ~35% of viewers
- Never save the only CTA for the end (only 16% see it)

---

## MrBeast Principles (Validated at Scale)

Source: MrBeast interviews (100M+ views per video average)

### The 100-Video Rule
Your first videos will be terrible. Commit to making 100 videos and improving one
specific thing each time -- script, editing, camera presence, pacing. Micro-improvements
compound exponentially. Do not expect results before video ~50.

### Deliver on the Promise Immediately
The title and thumbnail set a promise. In the first 5-10 seconds, **instantly assure
the viewer you are delivering on that promise**. No vlog intros, no "hey guys",
no talking about your day. Deliver what they clicked for, then promise even more
to exceed expectations.

### Ruthless Pacing & Final Payoff
- Remove every dull moment. Have critical friends roast your video to find dead spots.
- Use different camera angles and fast cuts to maintain visual stimulation.
- Ensure a **strong payoff at the end** (reveal, winner, result) so viewers have a
  compelling reason to stay until the last second -- this directly boosts AVD.
- The algorithm replaces "algorithm" with "audience" -- if people click and watch, YouTube promotes it.

### Auto-Play Era (2025+)
Videos now auto-play on the YouTube homepage. The first 5 seconds serve as an
extension of your thumbnail -- you must visually convince people to stay while
the video is already playing. This makes the 0:00-0:05 hook more critical than ever.

### Outlier Analysis Method
Don't rely on guesswork. Look for outlier videos from smaller channels that
suddenly get 10x-1000x their normal views. Analyse what made that specific video
work. Study A/B thumbnail tests from successful creators in your niche.

---

## Key Constraints & Gotchas

- **55% of viewers leave in the first 60 seconds** -- the hook is the single highest-leverage optimization
- **"Hey guys welcome back"** is a measurable retention killer -- avoid channel-first openings entirely
- **AI narration drops retention by 70%** -- always prefer human-fronted content unless the channel is explicitly AI-themed
- **Only 16% reach the final 10%** of a video -- any CTA placed only at the end is seen by a fraction of viewers
- **8-minute mark unlocks mid-roll ads** but do not pad content to reach it -- retention loss from padding costs more than mid-roll revenue gains
- **Pattern interrupt frequency differs by format** -- every 30s for pre-recorded is aggressive but data-supported; live content needs longer intervals (2-3 min)
- **15%+ above channel average retention** is the threshold for algorithmic boost -- optimize your best-performing content types, not underperformers
- **Shorts optimal length is 15-30s** for completion rate, even though 3-minute Shorts are now allowed `[2025]`
- **The suspension bridge pattern (open loops)** delivers the highest completion rate improvement (68%) -- prioritize open-loop scripting over other techniques

`````
