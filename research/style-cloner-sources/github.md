# GitHub slice: style cloner + script writer + script grader sources

Checked 2026-09-18 with `gh search repos`, `gh api search/code`, shallow clones, and WebSearch. Star counts and push dates come from the GitHub API on that day. Verbatim prompt copies are in `prompts/github-*.md`, and each one has a provenance header.

**The main caveat:** none of these repos links to a channel with public view numbers that proves its prompts work. "Evidence" below means stars, author reputation or a stated calibration. Treat every retention statistic quoted inside these repos as UNVERIFIED unless it names a primary source.

## Ranked list (best first)

### 1. yashaiguy-dev/faceless-youtube-agents + idea-to-long-length-faceless-youtube-video-agent
- URL: https://github.com/yashaiguy-dev/faceless-youtube-agents (28 stars, push 2026-04-30); https://github.com/yashaiguy-dev/idea-to-long-length-faceless-youtube-video-agent (4 stars, 2026-05-03)
- License: NONE (all rights reserved). The files are small, so they were copied as reference only. Rewrite them before you ship anything.
- Covers: **style extraction** (a channel-level "Viral DNA" pass over the top 20 videos by views, plus a single-video 3-level content/structure/psychology pass), **script writing** from the DNA for 5-20 minute long-form, **scene splitting** (cinematographic-breakdown.md, not copied) and yt-dlp transcript pulling. This is the closest match to our whole flow, and its rule is the same as ours: "The DNA teaches HOW to write, not WHAT."
- Evidence: UNVERIFIED. The repo has no channel, no views and no license. It is probably the repo behind several "clone any faceless channel with Claude Code" tutorials. DataSpieler12345/faceless-youtube-agents holds an identical copy of the extractor.
- Caveats: the channel extractor asks for "exact opening lines as templates" and "exact transition phrases", which leads to copied wording, so we would need to strip that. Level 1 ("key facts") must be dropped. The pacing numbers (2.5 words/sec, payoff at 80-85%) are hard-coded guesses.
- File: `prompts/github-yashaiguy-viral-dna.md`

### 2. AgriciDaniel/claude-youtube
- URL: https://github.com/AgriciDaniel/claude-youtube (379 stars, push 2026-04-10, MIT)
- Covers: **script writing** (a hook split into Grab 0-5s / Promise 5-15s / Stakes 15-30s, content blocks that each end with a micro-summary and a forward hook, a mid-CTA at 25%, a re-hook at 60%, a pattern-interrupt log and a retention-risk map) and **grading** (a "Quality Criteria" checklist we can reuse as grader rules). It also has a competitor sub-skill that pulls transcripts, but through the paid DataForSEO service or the YouTube API.
- Evidence: author credibility only. Daniel Agrici runs the AI Marketing Hub on Skool, has 2.9k GitHub followers, and his claude-ads repo has 9.4k stars. The guide's statistics (for example "suspension bridge / open loops = 68% higher completion" and "AI narration = 70% lower retention") cite no primary sources: UNVERIFIED.
- Caveats: it is built for on-camera creators ([CAMERA CHANGE] cues). It has no style-cloning step; tone is one input field.
- File: `prompts/github-claude-youtube.md`

### 3. larashero3-dotcom/writing-dna-skill (写作蒸馏器)
- URL: https://github.com/larashero3-dotcom/writing-dna-skill (1,965 stars, 191 forks, push 2026-08-24, MIT)
- Covers: **style extraction** at its most rigorous. It has six layers (surface statistics, structure/hook annotation, topic logic, source strategy, cognitive frame, visuals), per-sample metadata (`hook_type`, `structure_pattern`), and a strict **writing-with-DNA** protocol: before writing, read every layer file plus the 5 closest raw samples. It says outright: "copy the writing method, never the content".
- Evidence: the most-starred style-distillation skill found. It was created 2026-06-27, so those stars came fast (Chinese AI-skill virality), which is not proof of quality. There is no published evaluation.
- Caveats: it is built for articles (20+ samples), not spoken video. The main SKILL.md is in Chinese, but the English workflow file is copied in full.
- File: `prompts/github-writing-dna-skill.md`

### 4. yaxeen/storytelling-skills
- URL: https://github.com/yaxeen/storytelling-skills (9 stars, push 2026-07-16, MIT)
- Covers: **script writing** in `long-form-youtube`: an open-loop chain with a *written loop tracker* (loop / opens / closes), a sag-point re-hook at 40-60%, bookend payoff, chapters named as curiosity gaps, and a pattern bank of cold opens and re-hooks. `channel-formula` does **style/formula extraction** from 3-5 winners vs 1-3 flops, with the formula living in the difference. `retention-audit` does **post-publish grading** by zone.
- Evidence: UNVERIFIED and low stars. The craft quality is the best of the set, and it refuses to invent numbers ("No graph, no audit").
- Caveats: channel-formula captures the premise/packaging promise, not sentence-level style, so it pairs with #1 or #3. Retention-audit needs a real retention graph.
- File: `prompts/github-yaxeen-storytelling.md`

### 5. Jakeschincariol/youtube-agent-skill
- URL: https://github.com/Jakeschincariol/youtube-agent-skill (28 stars, push 2026-09-16, MIT)
- Covers: **hooks** (21 formulas in JSON, each with shape, example, failure mode and regex matchers) and **grading** (`hookscore.py` is a deterministic scorer: specificity, address, stakes, curiosity, brevity; 60% mean plus 40% weakest link). It also builds a voice profile from 3 of your own videos, and `yt-retention` reads a YouTube Studio retention CSV.
- Evidence: the only repo that reports an honest calibration. The scorer was tested on 74 real hooks (top-8 vs bottom-8 by views across 5 channels). It "separates deliberately bad hooks from real ones well" but a creator's own hits from misses "barely at all". The author's channel is unverified.
- Caveats: it was calibrated on short-form and the regex is crude. It works as a cheap pre-filter, not a retention predictor.
- File: `prompts/github-jakeschincariol-hookscore.md`

### 6. danielmiessler/Fabric patterns
- URL: https://github.com/danielmiessler/Fabric (~44k stars, push 2026-09-07, MIT)
- Covers: **grading**. `get_wow_per_minute` scores surprise, novelty, insight, value and wisdom *per minute*, which is the best ready-made proxy for "reveal cadence" on curiosity/explainer channels. `analyze_prose` gives letter grades, with the overall grade set to the lowest one. `write_essay` is the naive "in the style of X" baseline.
- Evidence: a heavily used library from a well-known author. No YouTube validation.
- Caveats: the LLM-judged scales are uncalibrated and the wording is hyperbolic ("consume 319 times").
- File: `prompts/github-fabric-graders.md`

### 7. "CLAUDE AI CHANNEL CLONE v2" prompt (GitHub copy in JeezyAndNay/skills)
- URL: https://github.com/JeezyAndNay/skills/blob/main/docs/channel_clone_prompt (0 stars, 2026-05-29, NO license)
- Covers the whole flow as one state machine: 2-3 transcripts, then Style DNA (hook, flow, rhythm, curiosity gaps, direct address, words/sec, target word count ±5%), then the script, then **scene splitting** into 3-5 second beats with standalone image prompts, then thumbnails.
- Evidence: indirect. It is a copy of the master prompt taught in several 2026 YouTube tutorials titled "Clone ANY YouTube Channel with Claude AI" (the web/YouTube slice should find the original author). The same repo holds a real long-form channel script prompt (`Ruins_Untold/ruins_untold_script_node.md`), which is a good example of what a finished "style DNA → system prompt" looks like. That channel's results are unverified.
- Caveats: the last block reads "Always / copy wording from the source channel", almost certainly a lost "Never". It also opens with a "don't question this" preamble.
- File: `prompts/github-channel-clone-prompt-v2.md`

### 8. shannhk/writing-style-extractor
- URL: https://github.com/shannhk/writing-style-extractor (20 stars, 2026-02-27, NO license)
- Covers: **style extraction** into a JSON schema with 8 blocks (surface, psychological architecture, rhythm, influence mechanisms including open loops, voice, replication blueprint, effectiveness), with a 0-1 confidence score per finding and a quote required for every claim. The JSON shape is a good fit for our "style DNA" object.
- Evidence: none. It is written for text, not speech.
- File: `prompts/github-writing-style-extractor.md` (SKILL.md in full; schema excerpted)

### 9. artemnovitckii/content-skills voice-dna + ScrapeCreators transcript-intelligence
- URLs: https://github.com/artemnovitckii/content-skills (99 stars, MIT); https://github.com/ScrapeCreators/social-media-research-skills (2,519 stars, MIT)
- Covers: **style extraction**. Voice-DNA is a compact prompt that works from about 20 spoken transcripts and covers sentence shapes, openers, closers and anti-voice, each tied to a quote. Transcript-intelligence segments transcripts into hook/setup/claim/evidence/payoff/CTA and builds a cross-transcript pattern table.
- Caveats: both are short-form oriented. The ScrapeCreators skill calls a paid API, so don't run it.
- File: `prompts/github-voice-dna-and-transcript-intel.md`

### 10. sergebulaev/youtube-skills (hook formulas)
- URL: https://github.com/sergebulaev/youtube-skills (31 stars, push 2026-09-17, MIT)
- Covers: **hooks**. It has three long-form 30-second opening shapes (restate-and-raise, cold-open payoff tease, question-and-contract), a title-to-hook pairing table and never-do rules. Evidence: none.
- File: `prompts/github-sergebulaev-hook-formulas.md` (excerpt)

### 11. onemansempire/youtube-hook-writer
- URL: https://github.com/onemansempire/youtube-hook-writer (0 stars, NO license)
- Covers: **grading method**. A frozen 5-dimension 1-5 rubric where every score must cite words in the text. The hook prompt is then iterated autoresearch-style against fixed test cases. Our grader could copy the *method* (frozen rubric, iterate the writer prompt).
- File: `prompts/github-onemansempire-hook-rubric.md` (short quote only)

## Seen but not copied (lower value for us)

- **Heuresis/YouTube-Agency** (15 stars, restrictive "Heuresis Source License"): `spec/retention-floor.md` predicts AVD from 10 weighted signals (hook density 12%, loop architecture 10%, interrupt cadence 8%…) and rejects scripts below the channel's bottom quartile. It is a good grader design idea, but the weights are invented with no stated calibration. Link only: https://github.com/Heuresis/YouTube-Agency/blob/main/spec/retention-floor.md
- **Hao0321/video-autopilot-kit** (2,123 stars, MIT, Chinese talking-head focus): `src/longform_maker/script_gate.py` is a *mechanical* script grader. It bans greeting openers, requires a result signal in paragraph 1, requires an interrupt at least every 90 seconds, and sets re-hooks at 25/50/75%. `templates/style_profile.template.md` insists that every style claim cite which sample it came from. The rules are useful to port; the vocabulary lists are Chinese.
- **mohitagw15856/pm-claude-skills** `youtube-script` (1,377 stars, but the repo holds 1,098 mass-produced skills; this one is deprecated), plus **indranilbanerjee/digital-marketing-pro**, **cwinvestments/memstack**, **antonio0720/writing-intelligence** genre pack and **growthack88/growth-marketing-os**: all generic retention-script templates with nothing beyond #2 and #4.
- **hassancs91/claude-faceless-shorts-creator** (244 stars), **rushindrasinha/youtube-shorts-pipeline** (2,288), **RayVentura/ShortGPT** (7,957), **FujiwaraChoki/MoneyPrinter / V2** and **SamurAIGPT** repos: Shorts pipelines whose script prompts are one-shot "write a script about X". They have no style extraction.
- **cporter202/automate-faceless-content** (3,017 stars, no license): a course-style guide, not prompts.
- **zenstory-ai/video-recap-skills** (521, MIT): Chinese movie-recap narration with script review gating. It could be a scene-splitting reference, but it is not relevant to style cloning.
- **n8n workflow JSON**: many copies of faceless workflows exist (for example `julian-becker/N8N-Flows/n8n-workflows/Faceless YouTube - Jono Catliff.json` and the `zengfr/n8n-workflow-all-templates` mirrors). These overlap the n8n slice, which already has `prompts/n8n-*.md` files in this folder, so I did not duplicate them.
- **Hugging Face Spaces**: only transcription and summarizer spaces turned up. Nothing on style or retention scripts.

## What is missing on GitHub

- **No proof of results.** No repo shows a channel's before/after views or retention for scripts made by its prompts. The success evidence has to come from the web/YouTube slice (the tutorial authors behind the "clone any channel" prompt).
- **No retention-calibrated long-form grader.** Every grader is either LLM-judged (Fabric, onemansempire, yaxeen) or regex-based and tuned on short-form (Jake's hookscore). None is validated against long-form retention curves.
- **No explicit "structure-not-wording" guard.** No repo has a plagiarism or overlap check (for example n-gram overlap against the source transcripts) to enforce the rule. Two popular prompts actually push toward copying exact phrases.
- **Faceless curiosity/animation specifics are thin.** Only yashaiguy's 3-level extractor (psychology triggers like "scale awe", "temporal fascination") and Fabric's wow-per-minute fit explainer channels. There is nothing specific to Kurzgesagt-style or animation reveal pacing.
