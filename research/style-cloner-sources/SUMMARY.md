# The proven starting kit for the YouTube style cloner

## What was searched, and the honest verdict
- **4 places searched:**
  - **GitHub:** about 30 repos checked
  - **n8n and Blotato templates:** about 400 found, 67 opened
  - **Reddit/X operators:** people actually running channels
  - **Top YouTube creators and strategists**
- **About 50 real prompts and frameworks were saved word-for-word**, each with its source link, author, date and proof.
- ⚠️ **Nobody publishes a complete style-cloning prompt with proven results.** The proof lives in **frameworks from creators with huge, checkable results**, and the usable **prompt shapes come from repos and templates**.
- **So the plan is:** rules from proven creators + prompt shapes from the best repos. Nothing gets invented.

## Part 1: Style DNA extractor (reads 3–5 competitor scripts)
### Prompt shapes to start from
- **writing-dna-skill** (1,965 stars, free to reuse): the most careful style extractor found. **"Copy the writing method, never the content,"** and every style claim has to point to which sample it came from.
- **faceless-youtube-agents** (yashaiguy): the closest match to our whole flow ("the DNA teaches HOW to write, not WHAT"). ⚠️ It asks for "exact opening lines", which pushes toward copying, so we remove that. It has no license, so we can learn from it but not reuse its text.
- **n8n 2648** (26k views): a two-part extraction, first the shared structure of all samples, then voice traits, each with quoted examples.
- **n8n 18255:** picks **which** competitor videos to study, meaning videos that beat that channel's own normal views, not just its most-viewed.
### What the DNA measures (each item comes from a proven creator)
- **How fast the video confirms the title** (within 10 seconds) and **the hook pattern:** Paddy Galloway (about 50B views for clients like MrBeast and Mark Rober), Kallaway (458k subscribers)
- **"But / therefore" links between beats vs "and then":** the South Park creators, used on YouTube by Kallaway
- **How often questions are teased and paid off** (never more than 60–90 seconds without a payoff): George Blackman (Ali Abdaal's scriptwriter), Jake Tran (faceless channel, 1.84M subscribers)
- **Fresh surprises at about 3:00 and 6:00**, heavy explaining later, a short ending: MrBeast's production guide
- **Opening with the viewer's wrong belief:** Veritasium's Derek Muller. His PhD study showed this nearly **doubled test scores** (6.3 → 11 out of 26), and it's the only real experiment in the set.
- **Body shape** (a "puzzle list" where each part needs the one before), **varied sentence length**, **talking to "you"**, **active sentences**: Paddy, Kallaway, Johnny Harris (7.96M subscribers)

## Part 2: Script writer
- **Blotato's own "Clone Viral Reels" prompt** (Sabrina Ramonov, Blotato's founder): the best **"you MUST keep / you MAY change"** rules found. Keep the type of content and its level of detail; change the topic and the facts.
- **claude-youtube** (379 stars, free to reuse): the long-form layout. The hook is split into grab (0–5 seconds), promise (5–15) and stakes (15–30). Every section ends by pointing forward, with a re-hook around 60%.
- **storytelling-skills** (yaxeen, free to reuse): a written **tracker of open questions** so every question that gets opened also gets closed.
- **Several passes, not one shot:** operators on Reddit say one-shot AI scripts come out "shallow and soulless". The working method is structure → a draft written for listening → add specifics → remove the AI tone. Many write the first 12–30 seconds by hand.
- **George Blackman's hook prompt:** **the only prompt a proven creator published himself**. It comes with a banned-word list ("unlock, skyrocket, game-changer…").
- **Write in this order:** title first → check the outline has new points → intro → body → ending (Kallaway).

## Part 3: Script grader
### 8 checks, each from a named proven source
1. Title confirmed within 10 seconds, plus a specific tease within 30 seconds (Paddy, Colin & Samir, and YouTube's own "Intro" metric)
2. Beats linked by "but / therefore", not "and then" (South Park creators)
3. No stretch over 60–90 seconds without a payoff, and every question gets answered (Blackman, Paddy, Tran)
4. Fresh surprises at about 3:00 and 6:00, no early "wrapping up", a short ending after the payoff (MrBeast)
5. The wrong belief is stated before each big answer (Muller)
6. The promise is made by 1:00 and kept by the end, in active sentences (Johnny Harris)
7. Each section needs the one before it; transitions are bridges, not "let's get into it" (Paddy)
8. **Originality check:** the storyline must be clearly different from the competitor's videos **and** from our own earlier scripts, with sourced facts (YouTube policy, Kurzgesagt)
### How it reports
- **Blotato's post-grader style:** harsh scoring ("a 10 doesn't exist"), then the **top 3 fixes**, each quoting the exact line, saying why it hurts, and giving a rewrite.
- **Extra quick checks:**
  - Fabric's "wow per minute" (44k stars) measures how often the video surprises
  - Jake Schincariol's hook scorer is a cheap first filter. ⚠️ Its own author tested it: it catches bad hooks but **can't tell a creator's hits from their misses**.

## Safety rails and gaps
- ⚠️ **YouTube's July 2026 rule** penalises videos that **"mimic existing formats or stories to a degree that the videos feel interchangeable"**. It allows a similar pattern if each video has "a distinct storyline, focus, or concept". So the DNA stores **structure numbers only, never phrases**, and the grader checks that videos don't feel interchangeable.
- ⚠️ **What operators warn about:**
  - Channels get demonetized for **AI voice over slideshows**, and appeals mostly fail
  - Copied scripts get **copyright strikes**
  - Claude **invents quotes**, so every fact needs a source
- ⚠️ **The one proven operator found** (howtoai, 330K+ subscribers) uses Claude with 5 competitor transcripts. Even so, his team is **7 people and each video takes 3 weeks**, and he **still got 3 strikes in 45 days**. The $32k-in-a-month Sollo pitch is an ad.
- ⚠️ **Gaps:**
  - No grader anywhere has been proven against real long-form retention data
  - 4 of the sources have no license, so we learn from them but rewrite the text
  - Blotato's own in-app "YouTube Video Script" prompt is only visible inside your logged-in account. OpenCLI can read it for free.
