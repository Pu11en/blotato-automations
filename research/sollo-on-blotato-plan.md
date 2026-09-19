# Rebuilding Sollo on Blotato: what we already have, and where good content comes from

## The big idea
- **Blotato already covers most of what Sollo sells.** One Blotato key gets you:
  - **17 image models** (from Flux Schnell at 1 credit up to Nano Banana Pro at 50 credits)
  - **12 video modes** (from Framepack at 55 credits up to Veo 3). An 8-second Veo 3.1 Fast clip costs **280 credits**, or 400 with sound.
  - **Free built-in voiceovers** (20 ElevenLabs voices, no credits)
  - **37 ready-made visual templates**, research that turns a topic or link into source material, posting to **9 platforms**, post analytics, comment replies, direct messages (DMs) and DM auto-replies
- **Price:** $29 = 1,250 credits, $97 = 5,000, $499 = 28,000. Extra credits are $6 per 1,000, and unused credits roll over.
- **What actually makes the content good is the "brain" in front of Blotato**, not the models: brand brief → real research → hooks → writing → harsh grading → removing the AI tone → human pick → render → learn from results.
- ✅ **Most of that brain already exists as skills.** Some are in your Blotato folder, some come from Blotato's own official Claude plugin, and some are already installed on this machine. The job is wiring them into one flow, not writing prompts from scratch.

## What's already in your Blotato automations folder
### Tools that work today
- **Blotato Studio skill:** a menu of Blotato techniques. You plan for free, approve a credit limit, then spend. Adding a technique means adding one small file. **3 techniques are in it so far:**
  - **Product scene placement:** works, but ⚠️ it slightly changes the real product's color and edges
  - **AI video with AI voice:** ⚠️ never tested live
  - **Slideshow with text:** ⚠️ broken on Blotato's side (the text boxes come out blank). A free local replacement already works.
- **Brand content skill:** the safety layer.
  - A **brand profile** plus a **claims list**: approved phrases, phrases that need review, and blocked phrases
  - A rule that **AI never redraws the real product, logo or founder**; real photos get laid over the AI background instead
  - Every approval is tied to the exact file approved
  - A review sheet with a frame preview
- **Shared Blotato connection code** with tests. **Pinterest research workflow** that pulls real audience signals into a brief and logs results.
### Research and rules already written
- The full model price list, the 37 live templates, a scan of real Reddit and X users, and an honest verdict on public Blotato results.
- **A 7-point quality gate** every post must pass before publishing:
  - it serves a named audience
  - the opening doesn't overpromise
  - it has an original point
  - it fits the platform
  - its claims have sources
  - it doesn't look template-made
  - its call to action (CTA) feels natural
- **Two prompt formulas:**
  - A product-photo sentence: "product on [surface], [background], [lighting], [mood], [style]"
  - A muted-video rule: about **85% of Pinterest viewers watch with the sound off**, so keep on-screen text under 12 words per screen
### Sister projects we can pull from
- **Image Taste:** turns a 1–10 image mood board into direct references for image generation, then runs a 6-part pass/adjust review.
- **Cinco Vid:** the full video line: research brief → self-checked script → ad image → local render with voice, word-pop captions and trending music → scheduled to TikTok and Pinterest through Blotato.

## Blotato's 37 templates matched to Sollo's tools
- **Carousels (7):** Instagram carousel (made by Nano Banana 2), 2 tutorial carousels, 2 quote-card styles, 2 tweet-card carousels
- **Infographics (21):** whiteboard, newspaper, chalkboard, billboard, manga, breaking news, flyer and more. Each needs just a description and a footer.
- **Video (7):**
  - AI video with voiceover
  - **AI selfie talking video with a consistent character**, which is Sollo's "Persona / Influencer"
  - AI avatar with AI background footage
  - **Combine clips**, which trims silences and adds captions, titles and music (close to Sollo's "Clips")
  - "When X then Y" slideshow
  - Two image-and-text slideshows
- **Images (2):** product scene placement, single quote card
- ⚠️ **Sollo tools Blotato does NOT cover:**
  - music generation
  - voice cloning (needs your own ElevenLabs key)
  - upscaling
  - noise removal
  - auto-cutting a long video into shorts
  - SEO keyword data
  - website chatbot and phone bot
  - CRM (the contacts list)
  - invoicing
  - These need the outside projects from the earlier list.

## The prompt-engineering layer (the main part)
### Step 1: Raw material (AI can't invent real specifics)
- **Blotato's official "brand-brief" skill:** captures business, customer, voice, call to action, and your **"strong opinion / wedge"**, which fuels the best-performing hooks.
- **Your installed LinkedIn interviewer skill:** interviews you into a **Story Bank** of real numbers, turning points and opinions. This is the biggest single fix for generic AI content.
### Step 2: Research
- **Blotato's research feature:** turns a YouTube video, TikTok, article, PDF or research question into source material, and doesn't use credits.
- **Your Pinterest research workflow** for real audience signals.
### Step 3: Hooks
- **Blotato's official "viral-hooks" skill:** **100 hook patterns in 13 groups** (Receipts, Contrarian, Negative Frame, Curiosity Gap…). It writes 3 versions and runs a **first-3-words test**.
- **Your installed LinkedIn hook-extractor skill:** reverse-engineers a competitor's viral post into one of 20 formulas and a blank template.
### Step 4: Write
- **Blotato's "post-writer" and "repurpose" skills.** Repurpose turns one long piece into a week of posts.
- **marketingskills** (51k stars): copywriting and buying-psychology skills.
### Step 5: Grade harshly
- **Blotato's "post-grader" skill:**
  - scores 7 things, with **the hook worth 50%**
  - checks style rules (no em dashes, no filler like "really", "just", "in today's world")
  - returns the top 3 fixes
  - Its own rule: **7 is good, 10 doesn't exist.**
### Step 6: Remove the AI tone
- **humanizer** (50k stars), plus your installed **no-ai-slop** and **LinkedIn humanizer** skills.
### Step 7: Visual prompts
- **Blotato's official "generate" presets:** POV, story, listicle, before/after, problem/solution, brand style. Each uses a **"locked prompt fragment"** so a whole series looks like one channel, plus a set motion prompt for animation.
- **Prompt libraries:** awesome-nanobanana-pro (10k stars) and a skill that picks from **10,000+ Nano Banana Pro prompts**.
- **Your Image Taste project** for mood-board-matched looks.
### Step 8: Pick, render, learn
- **Make 3 ideas and keep 1.** Write 2–3 hooks for it. **Spend credits only on the approved one.**
- **Blotato analytics** ranks posts by views, reach, likes and comments. This works on **X, Instagram, Facebook, Threads and Bluesky**; TikTok, LinkedIn, Pinterest and YouTube metrics have to be copied in by hand.
### Rules baked into every prompt
- Use real numbers, names and moments. **One idea per post.**
- Write for what each platform rewards: **LinkedIn = comments, Instagram = saves, Facebook = shares, TikTok = watching to the end.**
- **Never ask AI to draw text or labels.** Lay text on top instead, because models misspell and change labels.

## What the plugin would look like
- **One plugin, 4 helpers, like Sollo's 4 agents:**
  - **Marketing:** runs Steps 1–8 above and schedules through Blotato
  - **Sales + support:** Blotato's Instagram/Facebook comment replies, DMs, and comment-triggered DM flows with an email capture
  - **Operations:** credit checks, the posting calendar, and a weekly results report
  - **Studio:** your Blotato Studio technique menu, with the brand safety layer
- **Parts to combine:**
  - Blotato's official connector (35 tools)
  - Blotato's official plugin (8 skills, 168 stars, updated August 2026)
  - your Studio and brand-safety skills
  - humanizer and the hook libraries
- 🚫 **No Kie.ai, ever.** Blotato's official "generate" skill animates through Kie.ai, so we keep only its prompt presets and drop its scripts.
- **Blotato-only video, checked live on 2026-09-18 (a free call):**
  - **"AI Video with AI Voice":** 1–20 scenes, each an uploaded image/video or an AI image prompt, with a voiceover line. It lets you pick the image model (13 choices, including Nano Banana 2 and GPT Image 2) and the voice (20 choices). **"Animate AI images" turns the AI stills into moving clips.**
  - **"AI Selfie Talking Video":** a consistent character talking across scenes
  - **"Combine Clips":** stitches clips and adds captions, titles and music
  - Plus the slideshow and image-and-text video templates
- ✅ **The workaround for the API limit: OpenCLI.** Through the API you can't choose the video model or animate your own photo. OpenCLI clicks through Blotato's website in your logged-in Chrome, so the plugin gets **every Blotato video model** (Framepack, Kling, Runway, Luma, MiniMax, Veo) and can **animate your real photos**, all paid with Blotato credits.
  - **Checked 2026-09-18:** OpenCLI is connected to your Chrome and **logged into Blotato** (the Videos page loads).
  - A **Kling "morph" clip** (first frame to last frame) from Sep 9 is already saved in the folder, and a matching test project is in your Blotato account.
  - ⬜ **Still to build:** a small saved "Blotato" command set for OpenCLI (none exists yet): pick a model, upload a photo, animate, and download. Before every click that spends credits, it checks the credit balance and your approved spending limit.
  - ⚠️ **Risk:** if Blotato changes its website, the clicks can break. We keep the API for everything the API can do and use the website only for model choice and animating your own photos.
- ⚠️ **Autopilot:** this needs scheduled runs. Keep your human-approval step until a format has won several times.
