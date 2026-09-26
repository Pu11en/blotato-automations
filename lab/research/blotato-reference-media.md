# Blotato reference-media capability audit

Checked against Blotato's official help and API documentation on 2026-09-08. No authenticated calls or credit-spending generations were made because the API key has not been supplied.

## Bottom line

Blotato can ingest an existing product screenshot, logo, image, video, or audio file and place that asset into a slideshow, post, or clip-combination workflow. That is the safe route when the actual product UI or brand asset must remain recognizable. Blotato also accepts reference images for generative workflows, but its public documentation does **not** promise pixel-exact product rendering or a real person's exact likeness after AI generation.

| Need | Documented route | Confidence / limit |
| --- | --- | --- |
| Show the real SaaS UI, logo, or product image | Supply the original public image URL to a template's `imageSource`, or attach/upload the original media when publishing | High confidence the supplied asset is used, but a rendered template may still crop, scale, compress, transition, or overlay it. Do not call the rendered pixels “identical” without comparison. |
| Edit recorded product demos without generating new visuals | Supply original clips to **Combine Clips and Apply Basic Edits** | High confidence. The template explicitly says it is for user-supplied footage and does not need AI-generated visuals. |
| Animate a still product image | Upload the image and choose **Create Animated Image** / an image-to-video model | Supported, but the result is generative. Shape, text, logo, UI, and identity preservation are unpromised and must be tested. |
| Keep one fictional character similar across scenes | **AI Selfie Talking Video with Consistent Character**, using a text description or image URL | Supported for an AI-generated character. The same page explicitly says “not your real face”; it makes no exact-likeness guarantee. |
| Apply brand inspiration automatically | Brand Visuals and Brand Documents through **Create Everything with AI Agent** | Brand Kit provides context/reference material, not an asset-lock or identity-preservation contract. |

## What the official docs establish

### User-supplied assets

The **Image Slideshow with Text Overlays** template accepts either an upload/image URL or an AI prompt in each `slides[].imageSource`. Blotato explicitly recommends it for product photos and other owned images. This lets us keep the real SaaS screen or product artwork as the scene source instead of asking an image generator to redraw it. [Official template reference](https://help.blotato.com/api/visuals/5903b592-1255-43b4-b9ac-f8ed7cbf6a5f)

The **Combine Clips and Apply Basic Edits** template accepts 1–20 clip URLs and can add titles, captions, music, transitions, silence trimming, duration limits, and an aspect ratio. Its documentation explicitly describes the workflow as bringing one's own footage with no AI-generated visuals required. This is the strongest documented route for product-demo Shorts. [Official clip-combination reference](https://help.blotato.com/api/visuals/c306ae43-1dcc-4f45-ac2b-88e75430ffd8)

The publishing API can attach any publicly accessible image/video URL directly through `mediaUrls`; the optional media endpoint accepts a public URL or base64 image data and stores a Blotato-hosted copy, with a documented 200 MB limit. [API quickstart](https://help.blotato.com/api/start) and [Upload Media](https://help.blotato.com/api/publish-post/upload-media-v2-media)

These routes preserve the supplied asset as the source. The docs do not promise lossless export, fixed crop behavior, or byte/pixel identity in a rendered composition. We should therefore retain the source file, inspect the output, and compare any logo, UI text, and layout before approval.

### Image-to-video

Blotato documents two ways to animate a still: upload a custom image in the editor and select **Create Animated Image**, or enable animation on AI-image scenes. It exposes multiple image-to-video models and spends credits on each generated video clip. The docs describe animation support but do not state that the model will preserve small text, logos, interface geometry, faces, or other exact details. [Custom Assets](https://help.blotato.com/features/videos/custom-assets), [AI video guide](https://help.blotato.com/features/videos/make-your-first-ai-video), and [credit behavior](https://help.blotato.com/support/faqs#what-uses-credits-and-what-doesnt)

Accordingly, do not use image-to-video for a hero product screen where exact UI identity matters until it passes a visual test. Prefer real screen recordings, or keep the screenshot static and add motion through template transitions/text overlays.

### “Consistent Character” is not exact human likeness

The official consistent-character template accepts `characterDescription` as either text or an image-reference URL, then creates a selfie-style video with that character across scenes. However, its own “When to Use” section says it is for a consistent **AI-generated character, not your real face**. [Official consistent-character template](https://help.blotato.com/api/visuals/57f5a565-fd17-458b-be43-4a2d8ccaca75)

There is therefore no contradiction once the terms are separated:

- **Documented:** an input image can guide the generated character and improve cross-scene consistency.
- **Not documented:** exact facial likeness, identity cloning, or faithful recreation of a real person.

For the user's real identity, treat this template as unsupported until a live test proves acceptable resemblance—and even then label it as a tested behavior, not a contractual guarantee. A recorded talking-head clip or user-supplied photo kept as a static source remains the reliable option.

### Brand Kit helps direction, not preservation

Brand Visuals accept PNG, GIF, JPEG/JPG, SVG, WebP, and AVIF up to 10 MB; Brand Documents accept PDF, PowerPoint, and Word files up to 25 MB. Blotato says the AI Agent incorporates these as reference material when generating visuals. It also says Brand Kit automatically applies only to **Create Everything with AI Agent**, not when selecting a specific template or calling `POST /v2/videos/from-templates`; for API template generation it tells users to repeat brand instructions in `prompt`. [Official Brand Kit](https://help.blotato.com/settings/brand-kit)

There is a meaningful documentation conflict: the current OpenAPI schema for `POST /v2/videos/from-templates` exposes optional `useBrandKit` and `brandId` fields, while the Brand Kit page says the endpoint does not auto-apply Brand Kit. [Official Video OpenAPI](https://help.blotato.com/api/openapi-reference/video) The schema documents the fields' existence but not their effect. We must not assume they work until an authenticated A/B test confirms it.

## Allowed paid-content stack

The proposed paid stack can remain:

1. **Codex** for research, scripts, prompts, workflow code, evaluation, and orchestration.
2. **Blotato API** for template rendering, AI images/video where approved, voice/captions available inside Blotato, media hosting, scheduling, publishing, and supported analytics.
3. **Local or free infrastructure only** for source files, screenshots/screen recordings, metadata, databases, queues, and review pages.

No Replicate, Fal, OpenAI Images, ElevenLabs, Runway, or other vendor key should be configured directly. Blotato may use such providers internally; that remains within the Blotato subscription/credit boundary. Blotato's docs also state that voiceover, publishing, scheduling, caption text, uploading owned media, and use of the AI Agent do not consume Blotato AI credits, while text-to-image and image-to-video do. [Official credit FAQ](https://help.blotato.com/support/faqs#what-uses-credits-and-what-doesnt)

## Required live tests after the API key arrives

Run all generations as drafts and do not publish:

1. Call `GET /v2/videos/templates` and save the returned template definitions. The live response is the source of truth because template inputs can change.
2. Run a static-source test with a screenshot containing a small logo, UI labels, numbers, and straight grid lines. Compare source and slideshow output for crop, resolution, compression, and overlay behavior.
3. Run the same image through an image-to-video route. Review the first, middle, and last frames for warped UI, rewritten text, logo drift, and invented elements.
4. Run the consistent-character template twice with the same fictional reference image and fixed scene descriptions. Compare within-run consistency and between-run stability. Separately test a consenting real-person image only if the user wants that experiment; do not claim exact identity.
5. Run an A/B template call using identical prompt/inputs: one with `useBrandKit: false`, one with `useBrandKit: true` plus the chosen `brandId`. Record request JSON, response, credit use, and visible brand differences to resolve the OpenAPI/Brand Kit conflict.
6. Run **Combine Clips** with a short screen recording and confirm no unexpected generative alteration occurs beyond selected crop, captions, transitions, and encoding.
7. For every cloned/community workflow, capture its original URL/version, complete inputs, model/template IDs, credit estimate and actual cost, output files, and a human visual verdict before adoption.

Until those tests pass, the production rule is: **use original product media directly; use AI generation only for backgrounds, metaphors, B-roll, or fictional characters where exact identity is not required.**
