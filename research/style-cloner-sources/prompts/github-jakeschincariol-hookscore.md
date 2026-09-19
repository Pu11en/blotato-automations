# Jakeschincariol/youtube-agent-skill: yt-script + hookscore.py + 21 hook formulas

- **Source URL:** https://github.com/Jakeschincariol/youtube-agent-skill
- **Commit:** a2feb2104981a375ffd4f87ee04f4f5344ac43c6 (2026-09-16)
- **Author:** Jake Schincariol
- **License:** MIT
- **Stars / last push (checked 2026-09-18):** 28 stars / 2026-09-16
- **Evidence of success:** Only repo found with an honest calibration note: hookscore was 'measured against 74 real short-form hooks (top-8 and bottom-8 by views across five channels)'; separates bad hooks from real ones but 'separates a creator's own hits from their own misses barely at all'. Author channel not verified.
- **Covers in our flow:** Hook writing (5 options, keep top 2) + deterministic hook grader (specificity, address, stakes, curiosity, brevity; 60% mean + 40% weakest) + voice.md built from 3 of the creator's videos. yt-retention reads a Studio retention CSV.
- **Caveats:** Regex scoring is crude and was calibrated on short-form, not long-form. Treat as a cheap pre-filter, not a retention predictor.

Text below is copied verbatim from the repo (no edits). Fences use five backticks so inner code blocks survive.

## Verbatim: `skills/yt-script/SKILL.md`

`````markdown
---
name: yt-script
description: >-
  Write a YouTube video script from a raw idea - hook options off 21
  formulas, scored, then the full spoken script with the retention beats
  marked. Use whenever the user wants a video script, a hook, an opening
  line, "what should I say", "write my next video", or is about to record
  and does not have the first fifteen seconds yet.
---

# yt-script

One idea into a script somebody finishes.

Two tools live in this folder and both actually run. Use them. Do not eyeball the hook.

```bash
python3 hookscore.py hooks.txt              # rank your hook options
python3 hookscore.py --hook "one line"      # score a single one
```

## Before you write

1. Read `~/.claude/youtube/voice.md` if it exists. That is the user's voice profile: how they talk
   on camera, the words they never use, who they are talking to, what they will not claim. If it
   does not exist, ask for **three of their own videos**, read or transcribe them, infer the voice,
   and write the file. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The shape

**The first 15 seconds is the whole job.** It does three things or the video leaks: confirm the
click the title promised, open a question the viewer cannot close, and prove the payoff exists.

1. **Hook.** Write FIVE against [the 21 formulas](hooks.json), run them through `hookscore.py`,
   keep the top two, and show the user both with their scores. Never hand over one hook.
2. **The turn** (0:15-0:45). Say what the video is going to do, in one sentence, and start doing it.
   No channel intro, no "before we get started", no subscribe pitch. Those are the single most
   common cause of the 0:30 cliff.
3. **The body.** One idea per beat. Mark each beat with what is ON SCREEN, not just what is said -
   a talking head with nothing to look at is a podcast.
4. **The payoff.** Deliver the thing the hook promised, explicitly, and say that you are delivering
   it: "that is the prompt, it is in the description".
5. **The close.** One ask. Not three.

## What to hand back

- the two best hooks with their scored panels
- the script, beat by beat, with `[ON SCREEN: ...]` on every beat
- the runtime estimate at 150 words per minute
- one line naming which formula the winning hook used and why it fits this idea

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

`````

## Verbatim: `skills/yt-script/hookscore.py`

`````python
#!/usr/bin/env python3
"""hookscore.py - score a YouTube hook before you waste a take on it.

Five properties, 0-100 each, and a verdict that is 60% the mean and 40% the weakest one. The
weakest-link weighting is deliberate: a hook with four strong properties and one dead one is a hook
that leaks at the dead one, and averaging hides that.

    python3 hookscore.py hooks.txt            # one hook per line, ranked
    python3 hookscore.py --hook "one line"    # score a single hook
    python3 hookscore.py --json hooks.txt     # machine-readable

WHAT THIS CAN AND CANNOT TELL YOU. Measured against 74 real short-form hooks (first 15 seconds of
auto-captions, top-8 and bottom-8 by views across five channels): it separates deliberately bad
hooks from real ones well, and it separates a creator's own hits from their own misses barely at
all. Treat a low score as a reason to look again, never a high score as a promise.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json")))["hooks"]

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b", re.I)

def words(t): return re.findall(r"[a-z0-9'%$.]+", t.lower())

def specificity(t):
    w = words(t)
    if not w: return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # proper nouns that are not sentence-initial read as named things
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # a hook that resolves itself has no gap left
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 9-24 words is the band a spoken hook lands in at ~150wpm inside 10 seconds
    if 9 <= n <= 24: return 100
    if n < 9:  return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)

PROPS = [("SPECIFICITY", specificity), ("ADDRESS", address), ("STAKES", stakes),
         ("CURIOSITY", curiosity), ("BREVITY", brevity)]

def classify(t):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t)
    return parts, verdict, name, hits

def band(v): return "STRONG" if v >= 72 else "WORKABLE" if v >= 55 else "WEAK"

def report(t, parts, verdict, name, hits):
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'VERDICT':<12} {verdict:3d}  {band(verdict)}")
    print(f"    formula      {name}" + (f"  ({hits} pattern{'s' if hits != 1 else ''} matched)" if hits else "  (no formula matched - that is usually a summary, not a hook)"))
    low = min(parts, key=parts.get)
    print(f"    weakest      {low} - {FIX[low]}")

FIX = {
 "SPECIFICITY": "swap one adjective for a number, a name or a date",
 "ADDRESS": "say 'you' in the first six words",
 "STAKES": "name what it costs them to keep doing it the current way",
 "CURIOSITY": "cut the half of the sentence that answers itself",
 "BREVITY": "9 to 24 words. Read it out loud and stop where you run out of breath",
}

def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    out = []
    for t in lines:
        parts, verdict, name, hits = score(t)
        out.append({"hook": t.strip(), "properties": parts, "verdict": verdict,
                    "band": band(verdict), "formula": name, "matched": hits})
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([{k: v for k, v in r.items() if k != "matched"} for r in out], indent=1)); return
    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched"])
    if len(out) > 1:
        print(f"\n  winner: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n")

if __name__ == "__main__":
    main()

`````

## Verbatim: `skills/yt-script/hooks.json`

`````json
{
 "version": "1.0",
 "note": "21 hook formulas for YouTube. A YouTube hook is the first 15 seconds and it does three jobs: confirm the click the title promised, raise a question the viewer cannot close, and prove the payoff exists. A hook that only does the third is a summary and it leaks. Every formula here carries the shape, a worked example, the failure mode, and the patterns hookscore.py classifies transcribed speech against.",
 "rules": [
  "Confirm the title in the first sentence. A hook that ignores its own title is why people leave at 0:08.",
  "One idea. A hook carrying two promises keeps neither.",
  "Specific beats big. '400 to 200,000 in seven months' outperforms 'massive growth'.",
  "Show the artifact inside 20 seconds if you promised one.",
  "Never open with who you are. The subscribe pitch has not been earned yet."
 ],
 "hooks": [
  {
   "id": "the-statistic",
   "name": "The Statistic",
   "shape": "A number the viewer did not know, stated flat, then the consequence.",
   "example": "97% of the people who start a channel quit before video 30. Here is what the other 3% do differently.",
   "fails_when": "Dies if the number is vague or unverifiable. Say the source out loud.",
   "match": [
    "\\b\\d+(\\.\\d+)?\\s?%",
    "\\b\\d+ (out of|in) \\d+\\b",
    "\\b\\d{2,}(,\\d{3})+\\b"
   ]
  },
  {
   "id": "someone-elses-result",
   "name": "Someone Else's Result",
   "shape": "A named person's outcome, then the mechanism.",
   "example": "This channel went from 400 subscribers to 200,000 in seven months on one format. I mapped it.",
   "fails_when": "Do not invent the number. If you cannot name the channel, use a different formula.",
   "match": [
    "\\bthis (channel|guy|creator|account)\\b",
    "\\bwent from .* to\\b",
    "\\bin (a|one|two|three|\\d+) (week|month|year)s?\\b"
   ]
  },
  {
   "id": "the-mistake",
   "name": "The Mistake",
   "shape": "Name the error the viewer is probably making right now.",
   "example": "Your first 30 seconds are why nobody finishes your videos. It is not the topic.",
   "fails_when": "Only works if the mistake is common and the viewer can check it in one second.",
   "match": [
    "\\byou('re| are) (probably |still )?(doing|making)\\b",
    "\\bthe (mistake|reason) (everyone|most people|nobody)\\b",
    "\\bstop (doing )?\\b"
   ]
  },
  {
   "id": "contrarian-flip",
   "name": "Contrarian Flip",
   "shape": "State the accepted advice, then reject it.",
   "example": "Everyone says post daily. I posted once a week for a year and tripled the channel.",
   "fails_when": "Needs evidence in the next 15 seconds or it reads as contrarian for its own sake.",
   "match": [
    "\\beveryone (says|thinks|tells you)\\b",
    "\\bis (actually )?wrong\\b",
    "\\bnobody (tells|talks about)\\b"
   ]
  },
  {
   "id": "the-reveal",
   "name": "The Reveal",
   "shape": "Promise a specific thing will be shown, then show it.",
   "example": "I am going to show you the exact prompt, on screen, that wrote this video.",
   "fails_when": "You have to actually show it, early. A reveal at 8:00 is a retention cliff at 1:00.",
   "match": [
    "\\bI('m| am) going to show you\\b",
    "\\bhere('s| is) (the|exactly)\\b",
    "\\bon screen\\b"
   ]
  },
  {
   "id": "the-superlative",
   "name": "The Superlative",
   "shape": "The single best/worst/fastest of a category.",
   "example": "This is the fastest way to turn one long video into thirty Shorts.",
   "fails_when": "Superlatives are cheap. Earn it by naming what it beat.",
   "match": [
    "\\bthe (best|worst|fastest|easiest|only)\\b",
    "\\bnumber one\\b"
   ]
  },
  {
   "id": "the-clock",
   "name": "The Clock",
   "shape": "Bound the payoff in time.",
   "example": "In the next six minutes you will have a working title, thumbnail and script for your next video.",
   "fails_when": "The clock has to be true. Overrun it and the next video's hook is not believed.",
   "match": [
    "\\bin (the next )?\\d+ (seconds|minutes|hours)\\b",
    "\\bby the end of this video\\b",
    "\\bunder \\d+\\b"
   ]
  },
  {
   "id": "i-tried-it",
   "name": "I Tried It",
   "shape": "First-person experiment with a stated cost.",
   "example": "I let an AI run my channel for 30 days. I did not touch the uploads.",
   "fails_when": "Needs a real cost - time, money, risk - or there is no stake.",
   "match": [
    "\\bI (tried|spent|tested|let|gave)\\b",
    "\\bfor \\d+ (days|weeks|months)\\b",
    "\\bso you don'?t have to\\b"
   ]
  },
  {
   "id": "the-question",
   "name": "The Question",
   "shape": "Ask the exact question the viewer typed into search.",
   "example": "Why do your videos die at 30 seconds when the topic is fine?",
   "fails_when": "Must be the viewer's question, not yours. Pull it from your own comments.",
   "match": [
    "^(why|how|what|when|should|can|do|does|is)\\b",
    "\\?\\s*$"
   ]
  },
  {
   "id": "the-before-after",
   "name": "Before and After",
   "shape": "Two states, one cut between them.",
   "example": "This was my thumbnail. This is my thumbnail now. Same video, four times the click-through.",
   "fails_when": "Only works with a visual. Do not use it on a talking-head-only video.",
   "match": [
    "\\bbefore\\b.*\\bafter\\b",
    "\\bthis was\\b.*\\bthis is\\b",
    "\\bused to\\b"
   ]
  },
  {
   "id": "the-teardown",
   "name": "The Teardown",
   "shape": "Take a real thing apart in public.",
   "example": "I pulled the nine most-viewed AI videos of the month and broke down what the titles share.",
   "fails_when": "Name what you pulled and how many. A teardown of one example is an anecdote.",
   "match": [
    "\\b(broke|break|breaking) (it )?down\\b",
    "\\bteardown\\b",
    "\\banalys(ed|ed|is|e)\\b",
    "\\bI pulled\\b"
   ]
  },
  {
   "id": "the-stack",
   "name": "The Stack",
   "shape": "Two named tools combined into one outcome.",
   "example": "Claude plus your YouTube Studio export gives you next week's upload schedule in one prompt.",
   "fails_when": "Both tools must be nameable and the outcome must need both.",
   "match": [
    "\\b\\w+ (plus|\\+) \\w+\\b",
    "\\bcombine\\b",
    "\\btogether\\b"
   ]
  },
  {
   "id": "the-warning",
   "name": "The Warning",
   "shape": "A cost the viewer is about to pay.",
   "example": "Do not upload another video until you check this one setting.",
   "fails_when": "If the cost is small the hook is a lie. Reserve it.",
   "match": [
    "\\bdo not\\b",
    "\\bdon'?t (upload|post|publish|start)\\b",
    "\\bbefore you\\b",
    "\\bstop\\b"
   ]
  },
  {
   "id": "the-list",
   "name": "The List",
   "shape": "A counted set, with the count in the first line.",
   "example": "Seven things I would do differently if I started a channel in 2026.",
   "fails_when": "The count must be exact and every item must be different in kind.",
   "match": [
    "^\\d+ \\w+",
    "\\b(here are|these are) \\d+\\b"
   ]
  },
  {
   "id": "the-receipt",
   "name": "The Receipt",
   "shape": "Show the artifact first, explain second.",
   "example": "This is the analytics page. This video did 40% of the channel's watch time. Here is why.",
   "fails_when": "Requires a real screenshot. A described receipt is not a receipt.",
   "match": [
    "\\bthis is (the|my)\\b",
    "\\bscreenshot\\b",
    "\\bproof\\b",
    "\\breceipts?\\b"
   ]
  },
  {
   "id": "the-insider",
   "name": "The Insider",
   "shape": "Information from inside a system.",
   "example": "YouTube tells you which videos are underperforming. Almost nobody opens the report.",
   "fails_when": "Do not claim insider access you do not have.",
   "match": [
    "\\b(nobody|almost nobody|most people) (knows?|opens?|uses?)\\b",
    "\\bhidden\\b",
    "\\bburied\\b"
   ]
  },
  {
   "id": "the-impossible",
   "name": "The Impossible Claim",
   "shape": "State something that sounds untrue, then prove it.",
   "example": "You can write, title, thumbnail and schedule a week of videos without opening a single editor.",
   "fails_when": "The proof has to start within 20 seconds or it reads as clickbait.",
   "match": [
    "\\bwithout\\b",
    "\\bnever\\b",
    "\\bin one\\b",
    "\\bzero\\b"
   ]
  },
  {
   "id": "the-comparison",
   "name": "The Comparison",
   "shape": "Two named options, one winner.",
   "example": "I wrote the same video three ways. One of them held 62% and the other two did not.",
   "fails_when": "Say the losing option out loud. A comparison with no loser is an advert.",
   "match": [
    "\\bvs\\.?\\b",
    "\\bversus\\b",
    "\\bwhich (one )?(is|wins)\\b",
    "\\bsame .* (three|two) ways\\b"
   ]
  },
  {
   "id": "the-origin",
   "name": "The Origin",
   "shape": "Where a result actually came from.",
   "example": "Every video on this channel starts in the same 12-line file. Here it is.",
   "fails_when": "Works once per channel. It is a reveal about you, and you only have one.",
   "match": [
    "\\bevery (video|post) .* starts\\b",
    "\\bit all (starts|started)\\b",
    "\\bthe (real )?reason\\b"
   ]
  },
  {
   "id": "the-deadline",
   "name": "The Deadline",
   "shape": "Something is changing on a date.",
   "example": "The old description format stops mattering this month. Here is what replaces it.",
   "fails_when": "Only use with a real, checkable date. This is the fastest formula to lose trust with.",
   "match": [
    "\\b(this|next) (week|month|year)\\b",
    "\\bis changing\\b",
    "\\bno longer\\b",
    "\\bas of\\b"
   ]
  },
  {
   "id": "the-direct-address",
   "name": "The Direct Address",
   "shape": "Name the exact viewer in the first six words.",
   "example": "If you have under a thousand subscribers, this is the only video you need this week.",
   "fails_when": "Narrow beats broad. 'If you make videos' addresses nobody.",
   "match": [
    "^if you\\b",
    "\\bfor (anyone|everyone|people) who\\b",
    "\\byou specifically\\b"
   ]
  }
 ]
}
`````

## Verbatim: `skills/yt-retention/SKILL.md`

`````markdown
---
name: yt-retention
description: >-
  Read a YouTube Studio audience-retention export and find where viewers
  actually leave, then say what to change. Use for "why do people stop
  watching", "my retention is bad", a pasted retention chart or CSV, or "fix
  my pacing".
---

# yt-retention

The retention graph is the only honest feedback YouTube gives you. Almost nobody exports it.

```bash
python3 retention.py retention.csv --duration 600
python3 retention.py retention.csv --transcript transcript.srt
```

Getting the file: Studio -> a video -> Analytics -> Engagement -> the audience-retention chart ->
the download icon -> "Audience retention".

## Three different problems

- **HOOK LEAK** - what is lost in the first 30 seconds. Under 25% is healthy. This is always the
  first thing to fix and it is always the first fifteen seconds of script, never the edit.
- **CLIFFS** - single steep drops. A cliff is a moment: a topic change with no signposting, a
  sponsor read, a long setup. With `--transcript` the tool prints what was being said there, which
  is what makes the report actionable instead of interesting.
- **SLIDE** - the steady bleed across the middle. A flat slide is pacing. The fix is cutting, not
  rewriting.

## What to hand back

Name the single biggest leak and one change for it. Not a list of five. Then, only if asked, the
rest. And if the hook leak is healthy and the slide is flat, say the video is fine and the problem
is packaging - send them to `/yt-package`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**

`````
