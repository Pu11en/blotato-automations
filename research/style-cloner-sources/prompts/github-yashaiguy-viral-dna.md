# yashaiguy-dev faceless-youtube-agents + idea-to-long-length agent: Viral DNA extractor and script writer

- **Source URL:** https://github.com/yashaiguy-dev/faceless-youtube-agents and https://github.com/yashaiguy-dev/idea-to-long-length-faceless-youtube-video-agent
- **Commit:** e92c84537996217dd6fff60da9acc87198022b0b (2026-04-30) and cae49929ed1987a1676a4be5e9c498f8c71c1efd (2026-05-03)
- **Author:** Yash Chourasiya (yashaiguy-dev); commit author 'PSR Manju 2'. DataSpieler12345/faceless-youtube-agents is an identical copy of the extractor.
- **License:** NONE (no LICENSE file = all rights reserved). Reference only; do not ship this text verbatim.
- **Stars / last push (checked 2026-09-18):** 28 stars / 2026-04-30; 4 stars / 2026-05-03
- **Evidence of success:** None verified. No linked channel, no view numbers. Web search shows this is the repo behind several 'clone any faceless channel with Claude' tutorials (unverified which).
- **Covers in our flow:** Style extraction (channel-level, 5 sections incl. fill-in template) + single-video 3-level extraction (content/structure/psychology) + DNA-driven script writer for 5-20 min long-form. Closest match to our whole flow.
- **Caveats:** Channel extractor asks for 'exact opening lines as templates' and 'exact transition phrases' - that pushes toward copying wording, which we must forbid. Level-1 'key facts' extraction must be dropped for our 'structure never wording' rule. Pacing constants (2.5 words/sec) are assumptions.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Verbatim: `faceless-youtube-agents/skills/viral-dna-extractor.md (channel-level, top-20 videos)`

`````markdown
# Viral DNA Extractor

You are analyzing YouTube video transcripts to extract the "Viral DNA" — the structural and psychological patterns that make these videos perform well.

## Input

You will be given transcripts from the top-performing videos of a YouTube channel, along with their titles and view counts.

## Extraction Process

Analyze ALL transcripts together and extract:

### 1. HOOK ARCHITECTURE (First 30 seconds)
- What exact opening patterns do they use?
- How many words before the first "pattern interrupt" or shift?
- Are hooks question-based, statement-based, or story-based?
- Extract 3-5 exact opening lines as templates

### 2. RETENTION LOOPS
- What phrases keep viewers watching? ("but here's the thing", "what nobody tells you", etc.)
- How often do pattern interrupts occur? (every X seconds/sentences)
- What creates the "I need to keep watching" feeling?
- Extract 5-8 exact transition phrases

### 3. SENTENCE RHYTHM
- Are sentences short and punchy or longer and descriptive?
- What's the average sentence length pattern? (e.g., short-short-long-short)
- How do they vary pacing for emphasis?
- Extract 3 example sentences showing the rhythm

### 4. CONTENT STRUCTURE
- How is information organized? (problem→solution, story→lesson, list-based)
- How long is each section relative to total length?
- Where does the "payoff" happen?
- What's the call-to-action pattern?

### 5. FILL-IN-THE-BLANK TEMPLATE
Create a generic script template that follows the exact pacing and structure discovered above. Use `[BRACKETS]` for fill-in-the-blank sections. This template should work for ANY topic while preserving the viral DNA.

## Output Format

Return a structured document with all 5 sections above. Be specific — include exact phrases, exact word counts, exact timing patterns. Vague observations are useless; precise patterns are gold.

## Example Output Shape

```
## VIRAL DNA ANALYSIS

### Channel: [channel name]
### Videos Analyzed: [count]
### Total Views Analyzed: [sum]

---

### 1. HOOK ARCHITECTURE
- Pattern: [question hook → shocking stat → "here's why that matters"]
- Words before first interrupt: ~15
- Opening templates:
  1. "You know what [topic]? [provocative claim]."
  2. "[Number] [things] that [surprising outcome]."
  3. "I spent [time] [doing X] and [unexpected result]."

### 2. RETENTION LOOPS
- Interrupt frequency: every 3-4 sentences
- Key phrases:
  1. "But here's what nobody talks about..."
  2. "And this is where it gets interesting..."
  [etc.]

### 3. SENTENCE RHYTHM
- Pattern: short (5-8 words) → short → medium (12-15 words) → short
- [examples]

### 4. CONTENT STRUCTURE
- [breakdown]

### 5. TEMPLATE
[HOOK: Question about topic, max 15 words]
[SHOCKING STAT or CLAIM]
[TRANSITION: "Here's why that matters..."]
[etc.]
```

`````

## Verbatim: `idea-to-long-length-faceless-youtube-video-agent/skills/viral-dna-extractor.md (single viral video, 3 levels)`

`````markdown
# Viral DNA Extractor — 3-Level Dissection

## Input
A transcript from a viral YouTube video (provided in `outputs/<run_id>/transcript.txt`).

## Process

Analyze the transcript in THREE levels of depth:

### Level 1 — CONTENT (What)
- Topic and subject matter
- Key facts, claims, narrative events
- Format (documentary, essay, story, explainer)
- Length and pacing

### Level 2 — STRUCTURE (How)
Identify the storytelling mechanics:
- **Hook**: How do the first 30 seconds grab attention? What pattern? (question, shocking stat, "you" placement, scene-setting)
- **Arc**: What is the narrative shape? (chronological, problem→revelation, mystery→answer, escalating tension)
- **Retention loops**: What phrases/techniques keep viewers watching? ("but that's not the worst part", "what happened next changed everything")
- **Chapter beats**: How is the content segmented? What's the rhythm of section transitions?
- **Pacing**: How many words per section? Where does it speed up/slow down?
- **Payoff**: Where is the emotional climax? How far into the video?
- **CTA pattern**: How does it end? (call to action, cliffhanger, reflection)

### Level 3 — PSYCHOLOGY (Why)
Identify EVERY psychological trigger that makes this video compelling:
- **Cognitive curiosity gap** — "I need to know the answer"
- **Scale awe** — making the viewer feel small/amazed
- **Loss framing** — "this is gone forever" urgency
- **Identity connection** — "this is about YOU/your ancestors/your world"
- **Status knowledge** — "most people don't know this" exclusivity
- **Temporal fascination** — deep time, historical wonder
- **Sensory immersion** — vivid descriptions that make you FEEL it
- **Fear/danger** — survival instinct activation
- **Justice/injustice** — moral outrage or satisfaction
- **Surprise/revelation** — "everything you thought was wrong"

For each trigger found, note WHERE in the transcript it appears and HOW it's deployed.

## Output

### Step 1: Save Analysis
Save the full 3-level analysis to `outputs/<run_id>/viral_dna.json`:

```json
{
  "source_url": "...",
  "level_1_content": {
    "topic": "...",
    "format": "...",
    "key_facts": ["..."]
  },
  "level_2_structure": {
    "hook_pattern": "...",
    "hook_template": "...",
    "arc_type": "...",
    "retention_phrases": ["..."],
    "chapter_beats": ["..."],
    "pacing_words_per_section": [...],
    "payoff_location_percent": 85,
    "cta_pattern": "..."
  },
  "level_3_psychology": {
    "triggers": [
      {"name": "curiosity_gap", "strength": "high", "deployment": "..."},
      {"name": "scale_awe", "strength": "medium", "deployment": "..."}
    ]
  }
}
```

### Step 2: Generate 5 New Topics
Using Level 3 triggers as the REQUIREMENT CHECKLIST, generate 5 completely different topics that activate the SAME psychological triggers.

For each suggestion, show:
- Title (viral-optimized, under 70 chars)
- One-line description
- Which Level 3 triggers it activates (score each ✓/✗)
- Why this topic would invoke the same viewer response

Present to the user and wait for them to pick one (or ask for more).

### Step 3: After User Picks
Save the chosen topic and begin Stage 2 (Script Writing) using:
- Level 2 structure as the BLUEPRINT (same hook pattern, same arc, same pacing)
- Level 3 psychology as the GUIDE (hit same emotional beats)

`````

## Verbatim: `idea-to-long-length-faceless-youtube-video-agent/skills/viral-script-writer.md`

`````markdown
# Viral Script Writer

## Input
Either:
- A topic/idea (Mode A: direct idea)
- A topic + viral DNA analysis (Mode B: from YouTube dissection)

Also receives:
- `duration_minutes` — target video length (5/10/15/20)

## Pacing
- **2.5 words per second**
- 5 min = 750 words
- 10 min = 1500 words
- 15 min = 2250 words
- 20 min = 3000 words

## Script Rules

1. **First-person narrator voice** — authoritative, intimate, like telling a story to one person
2. **No headings or section markers** — pure narration text, paragraph breaks only
3. **Hook in first 2 sentences** — a number, a question, or a scene that stops the scroll
4. **Retention loops every 60-90 seconds** — "But that's not what made this extraordinary." / "What happened next, no one expected."
5. **Vary sentence length** — short punchy sentences (5-8 words) after long descriptive ones (20-25 words)
6. **Concrete details** — names, dates, places, numbers. Never vague.
7. **Emotional escalation** — each section should raise the stakes
8. **Payoff at 80-85%** — the biggest revelation/climax happens near the end, not at the end
9. **Reflective close** — final 15% is reflection, meaning, and a thought that stays with the viewer

## If Mode B (Viral DNA available)
- Use the `hook_template` from Level 2 as the opening pattern
- Follow the `arc_type` structure
- Insert `retention_phrases` (adapted, not copied) at the same intervals
- Ensure EVERY Level 3 psychological trigger is deployed at least once
- Match the `pacing_words_per_section` distribution

## Output
Save narration text to `outputs/<run_id>/script.md`

The script must be:
- Pure narration (no stage directions, no [brackets], no headings)
- Exactly within ±10% of target word count
- Readable aloud in one continuous flow

`````

## Verbatim excerpt: `faceless-youtube-agents/AGENT_GUIDE.md` (the IS / ISN'T rule)

`````markdown
### Important: What Viral DNA IS and ISN'T
- **IS**: The channel's hook patterns, sentence rhythm, retention loops, content structure, tone, and pacing
- **ISN'T**: The channel's topics — topics come from the USER, not the DNA
- The DNA teaches HOW to write, not WHAT to write about

#### STEP 2: Generate Script (Each iteration)

Pick the next topic from the user's topic list. Using the viral DNA from `outputs/viral_dna.md`, generate a narration script that:
- Follows the hook architecture, retention loops, and sentence rhythm from the DNA
- Is about the user's specified topic (NOT the source channel's topic)
- Hits the target word count based on requested duration (`duration × 2.5 words`)
- Is pure narration text — no stage directions, no timecodes, no [brackets]

`````
