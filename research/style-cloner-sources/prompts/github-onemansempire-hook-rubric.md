# onemansempire/youtube-hook-writer: fixed hook scoring rubric (autoresearch loop)

- **Source URL:** https://github.com/onemansempire/youtube-hook-writer/blob/main/scoring_rubric.md
- **Commit:** 1436b4c56006c83817d23fe20f54de0b8af4964b (2026-03-26)
- **Author:** onemansempire
- **License:** NONE (no LICENSE). Short quote only; full rubric at the link.
- **Stars / last push (checked 2026-09-18):** 0 stars / 2026-03-26
- **Evidence of success:** None. Interesting method, not results: rubric is frozen, prompt is iterated Karpathy-autoresearch style against 5 fixed test cases.
- **Covers in our flow:** Grading: 5 dimensions x 1-5 anchored scale with observable criteria (pattern interrupt, curiosity gap, specificity/credibility, emotional charge, economy); every score must cite words in the text.
- **Caveats:** LLM-judged, not tied to real retention data.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Short quote

`````markdown
# Hook Scoring Rubric

This rubric is the fixed evaluation metric for the hook writer skill. It is the equivalent of `prepare.py` in autoresearch — **do not modify it during experimentation.** All hooks are scored against this rubric so that experiments are directly comparable.

## How to Score

Score each hook on **5 dimensions**, each on a **1–5 scale**. The final score is the unweighted mean of all five dimensions, reported to two decimal places.

Every score band has **observable criteria** — things you can point to in the text. "I feel like it's creative" is not a valid justification. "The hook names a specific number and an unexpected category" is.
...
## Scoring Output Format

When scoring a hook, produce output in this exact format:

```
HOOK: "<the hook text>"
SCORES:
  pattern_interrupt: <1-5> — <one-sentence justification citing specific words/devices>
  curiosity_gap:     <1-5> — <one-sentence justification naming the open question>
  specificity:       <1-5> — <one-sentence justification listing the concrete details>
  emotional_charge:  <1-5> — <one-sentence justification naming the emotion and its source>
  economy:           <1-5> — <one-sentence justification with word count and any cuttable words>
  TOTAL: <mean to 2 decimal places>/5.00
```

Every justification must reference **observable features of the text**. If you cannot point to specific words or structures to justify a score, lower it.
`````
