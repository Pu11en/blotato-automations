# Sollo.ai: what it is, and the GitHub projects to rebuild it as a Claude Code plugin

## What Sollo actually is
- **Pitch:** an "AI operating system" for solo business owners. The headline is "Your AI workforce that never sleeps".
- **The real product:** one dashboard that bundles **30+ AI tools** under one subscription. It is mostly a wrapper around other companies' AI models (GPT, Claude, Gemini, plus video models it brands as "Sollo AX / NX / VX / MC / MX").
- **Four "agents"** it advertises:
  - **Marketing:** writes content, posts to social media, writes emails, runs campaigns
  - **Sales:** qualifies leads, books meetings, follows up
  - **Support:** answers customer questions across channels
  - **Operations:** invoices, bookkeeping, scheduling, admin
- **Pricing:** Pro **$25/mo** (750k credits), Max **$100/mo** (5M credits), Ultra **$200/mo** (12.5M credits). It also has a two-tier affiliate program (10% + 5%).
- **Not open source.** It has no public API.

### The tool list, grouped the way Sollo groups it
- **Audio:** music from a text prompt, sound effects
- **Video:** long video cut into shorts, text-to-video, video upscaler (2x–8x), product ad videos from a web page
- **Images:** image generator, live image, image upscaler, pitch-deck maker
- **Voice:** transcription, voiceover, background-noise remover, voice cloning
- **Writing:** content cloner (repurposing), rewriter, YouTube script writer, long-form writer
- **SEO:** SEO audit tool, YouTube-to-blog, Reel-to-blog, keyword research
- **Avatars:** avatar maker, talking-avatar videos, "AI influencer" avatars
- **Business automation:** website chatbot, phone voice bot, email agent, hand-off to a human, meeting scheduler, data analyzer, bot knowledge base, contacts list (a CRM)

## How it maps to a Claude Code plugin
- A Claude Code plugin is a bundle of **skills** (step-by-step how-tos), **agents** (specialist helpers) and **MCP servers** (connectors that let Claude call outside services). One install brings all three.
- **Claude already covers the writing and SEO thinking.** The writer, rewriter, script writer, content cloner and data analyzer are just well-written skills. No outside service is needed.
- **Media needs outside services.** Images, video, voice, music and avatars need an AI media service. Most of these cost per use.
- ⚠️ **"24/7 on autopilot" is not something a plugin does by itself.** Claude Code only runs when started. For round-the-clock work you would add scheduled runs (Claude's scheduled cloud agents, a cron job, or n8n).
- ⚠️ **The customer-facing chatbot and phone bot need a server that is always on.** A plugin can set them up and manage them, but the bot itself has to be hosted somewhere (Vapi, Chatwoot, or your own server).

### Suggested plugin layout
- **4 agents:** marketing, sales, support, operations, matching Sollo's four.
- **8 studio skills:** audio, video, images, voice, writing, SEO, avatars, automation.
- **One connector file** that switches on the media, email, social, CRM and payment services listed below.

## The best projects for each part (checked on GitHub today)
### Plugin shell and ready-made skills
- **anthropics/claude-plugins-official** (36k stars): the official plugin directory. Copy its layout and marketplace format.
- **anthropics/skills** (177k stars): official skills, including the **PowerPoint/deck maker**. That covers "Presentations".
- **wshobson/agents** (40k stars, MIT): a large plugin marketplace. Good model for bundling many agents.
- **coreyhaines31/marketingskills** (51k stars, MIT): marketing skills for Claude Code covering copywriting, landing-page conversion (CRO), SEO and growth. This is **the Marketing agent's brain**.
- **AgriciDaniel/claude-seo** (17k stars, MIT): 25 SEO skills + 18 helper agents. This is **the SEO Studio**.
- **AgriciDaniel/claude-blog** (2k stars): blog-writing skill suite for the long-form Writer.
- **Closest existing all-in-ones to learn from:** zubair-trabzada/ai-agency-claude (145 stars, 5 AI teams), ericosiu/marketing-os-starter (4 marketing agents), ReScienceLab/opc-skills (1.8k stars, skills for solopreneurs). None of them do media.

### Images, video, music (the media engine)
- **luminarylane/fal-mcp-server** (active today): one connector to fal.ai for **images, video, music and audio**. This single connector covers most of Sollo's media tools. 💲 pay per use.
- **replicate** (sena-labs/replicate-mcp-server, or Replicate's own "code mode" server): a backup media service with thousands of models. 💲 pay per use.
- **remotion-dev/remotion** (60k stars) + **remotion-dev/skills**: make videos from code. Good for **product ad videos** and branded templates. Free for individuals; companies need a license.
- **Long video → shorts:** mutonby/openshorts (5k stars) or Anil-matcha/AI-Youtube-Shorts-Generator (5k stars, MIT), both free and self-run.
- **Upscaling images and video:** xinntao/Real-ESRGAN (37k stars), free and runs locally.
- **Free music and sound effects (local):** facebookresearch/audiocraft (24k stars, MIT).

### Voice
- **elevenlabs/elevenlabs-mcp** (official, MIT): **voiceover, voice cloning, sound effects, music, noise removal and transcription** in one connector. 💲 paid plan.
- **Free local options:** openai/whisper or ggml-org/whisper.cpp (transcription), resemble-ai/chatterbox and SWivid/F5-TTS (voiceover and cloning), facebookresearch/demucs (noise removal).
- **jkawamoto/mcp-youtube-transcript** + **yt-dlp**: pull YouTube and Reel transcripts. That feeds **YouTube-to-blog and Reel-to-blog**.

### Avatars
- **HeyGen** is the paid route. There is **no official HeyGen connector** on GitHub, only tiny community ones, so we would write a small one ourselves.
- **Free local route:** KlingAIResearch/LivePortrait (19k stars, animates a photo) + TMElyralab/MuseTalk (6.6k stars, lip-sync). Both need a strong graphics card.

### Sales, support and operations
- **Social posting:** gitroomhq/postiz-app (36k stars, self-hosted scheduler with AI features) + a Postiz connector (solomonneas/postiz-mcp).
- **Email:** resend/resend-mcp (official). Gmail works too once its connector is authorized.
- **CRM / contacts:** twentyhq/twenty (57k stars, open Salesforce alternative) + jezweb/twenty-mcp. Or shinzo-labs/hubspot-mcp if you use HubSpot.
- **Scheduling:** calcom/cal.diy (48k stars, the open Cal.com). The community connectors are all tiny, so we would write our own small one.
- **Website chat + human hand-off + knowledge base:** chatwoot/chatwoot (37k stars).
- **Phone voice bot:** VapiAI/mcp-server (official, paid) or pipecat-ai/pipecat (16k stars, free framework you host).
- **Invoices and payments:** stripe/ai (official Stripe agent toolkit), or invoiceninja/invoiceninja (self-hosted invoicing).
- **Autopilot / scheduled jobs:** n8n-io/n8n (205k stars), or Claude's built-in scheduled agents.

## Bottom line
- ✅ **Every one of Sollo's 30+ tools has a ready project**, and about **8 connectors + 2 skill packs** cover most of it.
- **Cheapest fast path:** fal + ElevenLabs connectors (pay per use) + marketingskills + claude-seo + the official skills. That rebuilds roughly **80% of Sollo** as one plugin.
- ⬜ **We would still need to write:** the 4 agent files, the 8 studio skills tying things together, and small connectors for HeyGen and Cal.com.
- ⚠️ **Licenses to watch:** Postiz is AGPL (fine to use, but you must share your changes if you sell a modified hosted copy). Remotion needs a paid license for companies. Twenty, Chatwoot and Invoice Ninja have custom licenses.
- ⚠️ **Real costs:** fal, ElevenLabs, HeyGen and Vapi all bill per use. Sollo's $25–$200 price bundles those same kinds of costs.
