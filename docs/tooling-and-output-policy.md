# Tooling and Output Policy

Status: accepted constraint  
Date: 2026-09-08

## Paid-tool boundary

Content production must use:

- the Codex plan and this agent harness for research, reasoning, writing, orchestration, code, and review;
- Blotato APIs and the existing Blotato credit balance for content generation, transformation, rendering, hosting, scheduling, publishing, and Blotato-supported analytics;
- local/open-source tools that do not incur usage charges;
- free APIs only when their terms, limits, attribution requirements, and fallback behavior are documented.

Do not add a paid direct dependency on OpenAI API, Anthropic API, Perplexity, HeyGen, ElevenLabs, Kie, Fal, Replicate, Runway, image/video generators, voice services, stock-media services, or another SaaS automation API.

Blotato may internally offer models from outside providers. Calling those models **through Blotato's own API and existing credit balance is allowed**. Creating a separate provider account or sending a direct paid request is not.

Every imported workflow must include a dependency manifest. A workflow is rejected if it hides a paid external call behind an HTTP node, custom code, subworkflow, MCP tool, or webhook.

## Identity and reference-media rule

There are three different capabilities, and they must not be conflated.

### Exact asset preservation — supported

When a product UI, logo, screenshot, face, or other identity must remain exact, use the original asset as media. Do not ask an image model to redraw it.

Blotato officially documents:

- `Image Slideshow with Text Overlays`, where `slides[].imageSource` accepts an uploaded image URL;
- `Video of Images and Text with Minimal Style`, where `images[]` accepts source image URLs;
- `Combine Clips and Apply Basic Edits`, where `videoClips[].url` accepts original footage and Blotato adds titles, captions, music, transitions, and aspect-ratio output;
- custom product/UGC images through template inputs such as `scenes[].mediaSource`.

This is the default route for SaaS demonstrations. Product screenshots and screen recordings stay visually authoritative while Blotato performs composition and packaging. [Blotato product-image FAQ](https://help.blotato.com/features/videos/faqs.md#how-do-i-create-a-product-video-with-my-own-images), [Image Slideshow template](https://help.blotato.com/api/visuals/5903b592-1255-43b4-b9ac-f8ed7cbf6a5f.md), [Combine Clips template](https://help.blotato.com/api/visuals/c306ae43-1dcc-4f45-ac2b-88e75430ffd8.md)

### Reference-guided generation — template-dependent and must be tested

The currently published `AI Selfie Talking Video with Consistent Character` template documents `characterDescription` as either text or an image reference URL and provides an API example. It says the template creates a consistent **AI-generated character**, not a clone of a real person. [Consistent-character template](https://help.blotato.com/api/visuals/57f5a565-fd17-458b-be43-4a2d8ccaca75.md)

This conflicts with Blotato's current general FAQ, which says Blotato does not yet have a Midjourney/Leonardo-style character-reference feature and does not offer realistic avatar/clone generation. [Blotato video FAQ](https://help.blotato.com/features/videos/faqs.md#how-do-you-make-ai-videos-with-consistent-characters)

Therefore:

- classify image-reference generation as experimental;
- query the authenticated template catalog when the API key is available;
- run a low-cost test with a non-sensitive synthetic character first;
- do not promise exact likeness or use this for identity-critical product UI;
- compare consistency across scenes and across repeated runs before adoption.

### Brand reference — stylistic, not exact placement

Blotato Brand Kit accepts brand visuals and documents that its AI Agent uses them as references. However, Blotato also says uploading a product image to Brand Visuals does not place that exact product image into a video. Brand Kit guides context and style; direct template inputs place the asset. [Blotato Brand Kit](https://help.blotato.com/settings/brand-kit.md)

## No workflow adoption without an output audit

A downloadable workflow is inspiration until it passes all four audit stages.

### 1. Static workflow audit

Record:

- source URL, author, license, retrieval date, and pinned revision;
- every node, subworkflow, webhook, and network hostname;
- required credentials and whether each dependency is allowed;
- all content-generation and transformation steps;
- prompts, template IDs, model selections, and hard-coded account IDs;
- retry, timeout, approval, cost, and publishing behavior;
- code-node behavior and any secret-like values embedded in the export.

### 2. Transformation map

Produce a plain-language map before execution:

```text
input asset
  -> extraction or transcription
  -> script/hook generation
  -> image selection or generation
  -> image-to-video or clip composition
  -> captions/audio/transitions
  -> final render
  -> publishing (disabled during audit)
```

For each arrow, identify whether Codex, Blotato, a local tool, or a free API performs it.

### 3. Isolated sample run

- Disable every publish node.
- Use non-sensitive sample inputs.
- Execute one node or stage at a time.
- Set the smallest practical credit budget.
- Persist each intermediate and final asset to this repository's ignored output area.
- Record request IDs, actual credits, runtime, status transitions, and errors.

### 4. Visual and media inspection

Before adoption, produce an audit pack containing:

- original inputs;
- every generated image;
- representative frames/contact sheet from each video;
- final playable media;
- `ffprobe` metadata for dimensions, duration, frame rate, codecs, and audio;
- screenshots of overlays and safe-zone placement;
- an identity-preservation comparison for supplied products, logos, UI, or characters;
- a written assessment of visual coherence, artifacts, text accuracy, narration, pacing, and factual fidelity;
- the exact cost per accepted output and cost of discarded attempts.

Human review is required. A workflow cannot be labeled `proven` merely because it completes without an error.

## Approved first media paths

Test in this order after the API key arrives:

1. **Exact SaaS screen-recording path:** local screen recording → Blotato Combine Clips → titles/captions → preview.
2. **Exact product-image path:** original screenshots/images → Blotato image/slideshow template → preview.
3. **Blotato-generated supporting visuals:** product identity remains in original frames; generated B-roll is clearly separate.
4. **Reference-character experiment:** authenticated catalog verification → one inexpensive synthetic-reference test → consistency audit.
5. **Image animation experiment:** animate a copy of an input image and check for logo/UI/identity distortion before any public use.

No publishing is part of these tests.

## Decision rule

When exact identity and generative motion conflict, preserve identity. A clean pan, zoom, crop, caption, transition, or screen recording is preferable to an impressive animation that changes the product, face, logo, or interface.

