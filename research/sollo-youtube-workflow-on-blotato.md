# The Sollo YouTube workflow, and how we copy it with Claude + Blotato

## What the video actually shows
- **The video:** "EXPOSING How Much YouTube Pays in 2026", a 1:44 Short from the channel **One Person Business** (44.6k subscribers, about 77k views, posted Sep 4, 2026).
- **The claim:** a faceless AI channel made **$32,000 in 28 days** from 4.9M long-form views and 900k watch hours.
- ⚠️ **Treat that number as an ad.** Sollo pays affiliates 10% + 5%, and the video ends by sending viewers to a tutorial. The dashboard shown can't be checked.
- **The format:** long-form **"curiosity" animation videos**, meaning an animated scene over a narrated voice, like a faceless explainer channel. The creator copied a competitor channel whose video got 7M views.

## Their exact 7 steps
1. **Ideas:** screenshot a successful competitor's channel page and ask Claude for similar video ideas. Pick one.
2. **Facts:** ask Claude for unique facts on that topic "that people don't know".
3. **Script:** in Sollo, paste the title and the facts. Then **paste the competitor's video links and "clone their style of writing" in one click**, choose how you want to make money, and generate.
4. **Scenes:** paste the script into Sollo's **scene generator**, which makes **up to 150 animated-style images** in one click. They download numbered in order.
5. **Voice:** paste the script and pick a voice.
6. **Thumbnail:** make one in Sollo.
7. **Edit:** drop the numbered images and the voice into **CapCut** and assemble. They say it takes about 5 minutes.

### The only step that matters for quality
- **Step 3, "clone their style", is the whole trick.** Everything else is plumbing. It means reading the competitor's scripts and copying their structure: how the hook opens, how often a new question is teased, how long sentences are, and when the reveals land.
- That is a prompt-engineering job, and **Claude does it better than a one-click button** if we write it down properly.

## The same workflow with Claude + Blotato (no Kie, no CapCut)
### Steps 1–2: Ideas and facts (free)
- **Claude** reads the competitor channel (a screenshot or their video list) and suggests ideas.
- **Blotato's research feature** turns a topic or question into sourced material at no credit cost. ✅ Facts come with sources, so the channel doesn't spread made-up "facts".
### Step 3: Style cloning (free, the main build)
- **Pull 3–5 competitor scripts.** Blotato's research feature reads YouTube links for free, or we use yt-dlp, which is already installed.
- **Claude writes a "style DNA" card** for that channel:
  - hook in the first 15 seconds
  - how often a new open question is teased
  - sentence length and word level
  - narrator personality
  - where the reveals and the call to action (CTA) land
- **The script writer follows that card** using your facts, then a **grader** checks it: hook strength (Blotato's grader weights the hook at 50%), a retention beat every 30–45 seconds, no filler, no AI tone (humanizer / no-ai-slop).
- ⚠️ **We copy structure, never wording.** Copying their words is plagiarism and a copyright risk.
### Step 4: Scenes (Blotato credits)
- **Claude splits the script into scenes** and writes one image prompt per scene. Each prompt starts with the same **"locked style" sentence** (the trick from Blotato's official presets), so all 150 images look like one channel.
- **Blotato's "AI Video with AI Voice" template** takes **up to 20 scenes per video**, each with an AI image prompt plus that scene's voiceover line. It adds word-highlight captions and supports 16:9 for YouTube. It lets you pick from 13 image models.
- **A 150-scene video = about 8 of those videos**, stitched with Blotato's **"Combine Clips"** template (up to 20 clips).
### Step 5: Voice (free)
- **Built into the same template:** 20 ElevenLabs voices at **no credit cost**.
### Step 6: Thumbnail
- **Nano Banana 2 or Pro** through Blotato. It is the best of Blotato's image models at drawing text.
- For a specific model or editing your own photo, use **OpenCLI driving Blotato's website** (already connected and logged in).
### Step 7: Assemble and post (free)
- **No CapCut needed.** Combine Clips makes the finished video, and Blotato posts it to YouTube with the thumbnail and playlist.

## What a 150-scene video would cost in Blotato credits
- **Flux Schnell:** 1 credit per image → **about 150 credits**. This is good for testing the pipeline, but rough quality.
- **Flux Dev:** 10 per image → **about 1,500 credits**
- **Nano Banana 2:** 30 per image → **about 4,500 credits**, the best quality
- **Voice, captions, stitching and posting:** no credits
- **For scale:** the $97 plan gives 5,000 credits a month, and extra credits are $6 per 1,000. So one Nano Banana 2 video is about $27 of credits, and one Flux Dev video is about $9.
- ⚠️ **Moving clips (Kling, Veo) for every scene would cost far too much** (Kling is 210 credits per clip). Use them only for 1–3 hero moments, through OpenCLI.
- ⚠️ These costs are my estimate from Blotato's price list. **Blotato hasn't confirmed them yet.** The AI video template has **never been run live** in your folder, so the first real test should be a small one.

## Risks to know
- ⚠️ **YouTube's "inauthentic content" rule** (renamed from "repetitious content" in July 2025) can demonetize channels that pump out samey mass-produced AI videos. Original research, a consistent narrator and real storytelling are what keep a channel paid, which is why the style and grading steps matter.
- ⚠️ **The per-video scene limit (20) is new ground.** Stitching 8 videos is a guess until tested; the fallback is the free local assembler Cinco Vid already has.
- ⚠️ **Character consistency:** the AI template can't take a reference image for AI scenes. A recurring character needs the locked style sentence or OpenCLI image editing.
