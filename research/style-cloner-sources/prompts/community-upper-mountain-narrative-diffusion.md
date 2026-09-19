# community-upper-mountain-narrative-diffusion

- URL: https://www.reddit.com/r/aitubers/comments/1rczluj/heres_why_your_ai_video_scripts_suck_and_how_to_fix/
- Author: u/Upper-Mountain-3397 (r/aitubers)
- Date: 2026-02-24
- Upvotes/comments: 52 / 14 (archive snapshot via arctic-shift, 2026-09-18; live Reddit was blocked)
- Linked channel + view evidence: NONE. The author does not link a channel. Companion post (https://www.reddit.com/r/aitubers/comments/1r8pjgb/, 49 upvotes, 80 comments, 2026-02-19) claims he tracked 195 AI/faceless channels (63.5M subs). Later posts on his user page advertise his own tool ("OpenSlop").
- Status: COMMUNITY-VALIDATED (moderate), NOT PROVEN. Top of r/aitubers for script posts; commenters vouch ("i can vouch for your passes", "I use a similar process ... 5th-grade level"). Pushback in-thread: one commenter says 5 passes are unnecessary and Gemini 3.1 Pro beats Claude for "gamer" voice; another says GPT got him a 500k+ video (unverified).
- Use for our build: multi-pass writer (structure -> ear-draft -> enrich -> de-AI polish). Pass 1 is story-generation; for us, replace it with "outline from style DNA + new facts".

## Post text (verbatim, markdown escapes removed)

Lots of people have been asking me about my scripting process so figured this deserved its own post

if youre writing scripts in one shot thats your problem. I use a multi-pass method i call "narrative diffusion" - same idea as how stable diffusion generates images. SD doesn't render a final image in one pass, it starts with noise and refines over multiple steps - general shapes first, then finer detail each pass. Same concept for scripts - each pass has one job and builds on the last - difference vs single shot is massive.

**model ranking for scripting (this matters a TON)**

* **claude opus 4.6** - Best by far. holds multi-pass instructions without drifting, 1M context so it never loses track. most script pros in r/writers strongly prefer anthropic over others in general too because of language, tone, style, etc.
* **gpt-5.2** - solid but loses coherence around pass 3-4
* **gemini 3 pro** - Decent for drafts, struggles with polish 4.
* **deepseek/llama/gpt oss** - fine for pass 1-2 if budgets tight  Paying for opus actually saves money btw - one clean run beats three messy gpt runs that need manual fixing.

**the passes**

**pass 1 - structure:**
`Outline a story with a high-concept premise, characters, conflict, twists, and resolution about: [TOPIC]`

Nail the arc before writing anything - skipping this is why scripts feel flat.

**pass 2 - draft:**
`Write a complete story at a 5th-grade reading level based on this outline. Write for the ear not the page. Short sentences. Vary rhythm.`

"5th grade" forces clarity - "for the ear" prevents blog-style prose that sounds awful spoken aloud

**pass 3 - enrich:**
`Rewrite with richer sensory detail. Keep all events and continuity intact. Make it longer.`

"keep events intact" is key or the model can rewrite everything/lose coherence

**pass 4 - polish:**
`Remove: "delve", "dive in", "it's worth noting", "moreover", "journey", "tapestry". Vary sentence length dramatically. Open with tension not context. Kill anything that sounds like AI.`

Biggest single upgrade - this is where you kill all the LLM-isms and giveaways.

**pass 5 (optional) - visuals:**
`For each scene write an image prompt with camera angle, lighting, mood, character refs. Tag as "animate" or "static".`

tells you which scenes need animation vs ken burns - saves a ton of money

try this out, i guarantee your scripts will sound better. sharing all my code + detailed prompts for free soon, stay tuned

## Related comment (same author, r/aitubers 1raho66, 2026-02-21, 5 upvotes)

"i use a multi-pass approach i call "narrative diffusion", basically running the script through 4 passes: structure first (beats, arc, hook), then narration (written for the ear not the page), then visual descriptions, then a polish pass to kill all the AI-isms and vary sentence length. ... for niches, mystery/unsolved and space/science have the best retention from what ive seen across ~195 channels."

## Commenter variable schema (u/General-Oven-1523, same thread, 2 upvotes; full prompt was on sharetext.io/e7imurym, not retrievable)

    ### 1. The Narrative Core (Source of Truth)
    *   **Synopsis:** A structured summary of the user's idea (Introduction -> Body -> Conclusion).
    *   **Key Information Points:** Bullet points of the specific facts, stories, or arguments the user explicitly included.
    *   **The "Why":** Why did the user want to make *this specific* video? (Preserve the original intent).
    *   **Target Avatar:** Define the viewer persona (Age, psychographics, pain points).

    ### 2. SEO & Search Data Layer
    *   **Search Intent:* ... (truncated in archive)
