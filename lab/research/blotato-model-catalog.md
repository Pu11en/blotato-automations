# Blotato AI model and credit catalog

_Verified 2026-09-08 against Blotato's live, first-party Help Center and pricing pages. Model availability, prices, and template inputs can change; query the authenticated template catalog before building a production workflow._

## Answer in one sentence

Blotato credits currently buy generation from **17 listed image/image-edit endpoints** and **12 listed video modes** spanning Flux, Recraft, Ideogram, Luma, GPT Image, Nano Banana, Seedream, Imagen, Framepack, Kling, Runway, MiniMax, and Veo; Blotato's built-in text tools and built-in ElevenLabs voiceovers are documented separately as not consuming those credits.

The authoritative public cost table is Blotato's [AI Video Credits page](https://help.blotato.com/features/videos/ai-video-credits). Blotato's [Billing & Credits page](https://help.blotato.com/settings/billing-and-credits) says credits are deducted only for AI images and AI videos, not API calls, scheduling/publishing, AI voiceovers, turning source material into posts, or Viral AI Coach.

## Image generation and editing

| Blotato model label | Credits | Billing unit | Practical role |
| --- | ---: | --- | --- |
| Flux Schnell | 1 | image | Cheapest storyboarding and rough visual tests |
| Imagen 4 Fast preview | 7 | image | Current default in several documented visual templates |
| Flux Dev | 10 | image | Higher-quality Flux draft |
| Luma Photon | 10 | image | Alternate still-image generator |
| Flux 1.1 Pro | 15 | image | Higher-quality Flux output |
| Recraft V3 | 15 | image | Blotato labels this the realistic-image choice |
| Nano Banana | 15 | image | General image generation |
| Nano Banana Edit | 15 | image edit | Modify a supplied image |
| Seedream V4.5 Text-to-Image | 15 | image | General image generation |
| Seedream V4.5 Edit | 15 | image edit | Modify a supplied image |
| Flux 1.1 Pro Ultra | 20 | image | Blotato labels this “Best for Images” in template docs |
| GPT Image 1 (`gpt-image-1`) | 25 | image | OpenAI image generation routed through Blotato |
| Ideogram V2 | 30 | image | Older documented text-in-image option |
| Nano Banana 2 | 30 | image | Current recommended model for text rendering and overall image quality |
| Nano Banana 2 Edit | 30 | image edit | Higher-tier image editing |
| Nano Banana Pro | 50 | image | Highest-cost listed still-image tier |
| Nano Banana Pro Edit | 50 | image edit | Highest-cost listed image-edit tier |

Sources: [official model cost table](https://help.blotato.com/features/videos/ai-video-credits), [AI Images guide](https://help.blotato.com/features/ai-images), and [Image Slideshow API template](https://help.blotato.com/api/visuals/5903b592-1255-43b4-b9ac-f8ed7cbf6a5f).

There is a small documentation mismatch worth preserving in the implementation. The master credit table includes Nano Banana 2 and Nano Banana 2 Edit, while the static Image Slideshow and AI Video with AI Voice template pages list most, but not all, of those image options. A newer Instagram-carousel template explicitly exposes Nano Banana 2. Therefore, model selection is **template-dependent**. The current API tells clients to call `GET /v2/videos/templates?fields=id,name,description,inputs` and treat that authenticated response as the live input contract. The old API fields that accepted arbitrary `textToImageModel` and `imageToVideoModel` strings no longer work. See [Create Visual API](https://help.blotato.com/api/create-video) and [Visual Templates](https://help.blotato.com/api/visuals).

## Video generation

Blotato labels these as image-to-video options in its credit table. The first nine have a fixed listed price per generated clip. The three Veo 3.1 Fast modes are metered per second.

| Blotato model/mode | Credits | Billing unit |
| --- | ---: | --- |
| Framepack | 55 | clip |
| Runway Gen-3 | 85 | clip |
| Luma Dream Machine | 170 | clip |
| MiniMax | 170 | clip |
| Kling V1.5 | 210 | clip |
| Kling V1.6 | 210 | clip |
| Google Veo 2 | 835 | clip |
| Veo 3 Fast | 400 | clip |
| Veo 3 | 1,250 | clip |
| Veo 3.1 Fast | 35 without audio / 50 with audio | second |
| Veo 3.1 Fast Image-to-Video | 35 without audio / 50 with audio | second |
| Veo 3.1 Fast First-and-Last-Frame-to-Video | 35 without audio / 50 with audio | second |

Source: [official AI Video Credits table](https://help.blotato.com/features/videos/ai-video-credits).

An eight-second Veo 3.1 Fast generation therefore costs **280 credits without generated audio** or **400 credits with audio**. This is an arithmetic inference from Blotato's per-second rates, not a separately advertised bundle.

The current template API does not promise that every video model can be passed into every template. For example, [AI Video with AI Voice](https://help.blotato.com/api/visuals/5903fe43-514d-40ee-a060-0d6628c5f8fd) exposes `animateAiImages` as a boolean but does not expose a model selector in its published input schema. A workflow should discover the current templates and input enums first, then choose among the models the selected template actually offers.

## Voice and audio

Blotato's built-in voiceovers use ElevenLabs' `eleven_multilingual_v2` model. The public API documents 20 built-in voices: Alice, Aria, Bill, Brian, Callum, Charlie, Charlotte, Chris, Daniel, Eric, George, Jessica, Laura, Liam, Lily, Matilda, River, Roger, Sarah, and Will. The voice follows the language of the supplied script. [Official Voice IDs reference](https://help.blotato.com/api/accounts/voice-ids)

The detailed credit documentation says built-in AI voiceovers **do not use Blotato credits**. This is the clearest operational guidance even though the public pricing page uses broader wording that groups “images, videos, and voice” under AI credits. The app's billing screen should be treated as the final pre-generation authority. [Billing & Credits](https://help.blotato.com/settings/billing-and-credits), [AI Voiceover & Captions](https://help.blotato.com/features/videos/ai-voiceover-captions)

Built-in voices need no separate ElevenLabs key. A **custom or cloned ElevenLabs voice** is different: it requires the user's own ElevenLabs API key and enabled ElevenLabs billing, works in Blotato's web editor, and is not yet a native custom `voiceId` option in the Blotato API. That external dependency does not satisfy this project's Blotato-only-paid-API rule. [Blotato API Keys](https://help.blotato.com/settings/api-keys), [AI Voiceover & Captions](https://help.blotato.com/features/videos/ai-voiceover-captions)

## Text, research, and agents

Blotato supplies AI writing, the AI Agent, AI Twin, source transformation, Remix, Viral AI Coach, and Perplexity-backed web research. The official billing documentation says turning source material into posts and Viral AI Coach do not consume credits; the pricing page advertises unlimited AI writing. The source API includes `perplexity-query` as a native context type. [Billing & Credits](https://help.blotato.com/settings/billing-and-credits), [Pricing](https://www.blotato.com/pricing), [Source API](https://help.blotato.com/api/create-source)

Blotato does **not** publicly document a user-selectable underlying LLM catalog for those text features. Its support documentation mentions third-party providers such as OpenAI and Anthropic, but that is not the same as promising a particular text model or exposing a model selector. Do not encode an assumed GPT or Claude model name into the automation. [Blotato support FAQ](https://help.blotato.com/support/faqs)

AI Twin means text content written in the user's style; it is not a talking-head clone. Blotato also says it does not natively create a realistic human avatar or clone. Its separate consistent-character selfie template generates a synthetic character and may accept a character reference image, but it should not be represented as cloning a real founder. [Support FAQ](https://help.blotato.com/support/faqs), [AI Selfie Talking Video template](https://help.blotato.com/api/visuals/57f5a565-fd17-458b-be43-4a2d8ccaca75)

## What requires an outside API key?

| Capability | Included behind Blotato key/plan? | Outside key required? | Project decision |
| --- | --- | --- | --- |
| Listed image and video generations paid with Blotato credits | Yes | No direct model-provider key documented | Allowed |
| Built-in ElevenLabs multilingual voices | Yes | No | Allowed |
| Custom/cloned ElevenLabs voices | No | User's ElevenLabs key and billing | Do not use |
| “Unlimited” Replicate image generation on Creator/Agency | Blotato can connect it, but usage is billed by Replicate | User's Replicate key and billing | Do not use |
| Blotato text tools and Perplexity context | Native Blotato feature | No separate key documented for the native feature | Allowed |
| Community n8n workflows using OpenAI, HeyGen, Perplexity, Kie, or another provider directly | No | Those workflows request their own provider keys | Do not use unless rewritten |

Blotato explicitly offers the Replicate-key connection as a separate pay-as-you-go arrangement, despite calling the resulting image generation “unlimited” in Blotato. This is not generation paid by accumulated Blotato credits. [Blotato API Keys](https://help.blotato.com/settings/api-keys)

## Current plan and top-up context

The public pricing page currently lists:

| Plan | Monthly price | Included AI credits |
| --- | ---: | ---: |
| Starter | $29 | 1,250/month |
| Creator | $97 | 5,000/month |
| Agency | $499 | 28,000/month |

The billing page says credits roll over each month unless a payment was refunded, and lists top-ups at **$6 per 1,000 credits**. It also says only successful image/video generations are charged. These figures are a dated snapshot and should not be embedded as permanent constants. [Blotato pricing](https://www.blotato.com/pricing), [Billing & Credits](https://help.blotato.com/settings/billing-and-credits), [AI Video Credits](https://help.blotato.com/features/videos/ai-video-credits)

## Best use for Cinco H Ranch Naturals

The useful shortlist is much smaller than the catalog:

1. **No generative model for the product itself.** Preserve real jars, labels, soap bars, ingredients, hands, and ranch footage as uploaded media. The models can invent packaging text, alter labels, or change the product.
2. **Flux Schnell at 1 credit** for disposable storyboards only.
3. **Imagen 4 Fast at 7 credits** for inexpensive background/B-roll concept tests.
4. **Recraft V3 at 15 credits** for realistic non-product atmosphere or ingredient imagery.
5. **Nano Banana 2 at 30 credits** only when baked-in text is actually necessary. For brand accuracy, Blotato's deterministic text overlays are safer than asking an image model to spell label or claim copy.
6. **Framepack at 55 credits** for the first inexpensive motion test. Use it on non-critical imagery, not the hero product label.
7. **Veo 3.1 Fast** only after a hook/storyboard wins. Eight seconds costs 280 credits without audio or 400 with audio, so it is poor for cheap discovery but reasonable for one selected hero shot.
8. **Built-in ElevenLabs voice or the founders' uploaded recording.** Both avoid buying a separate voice API. A real founder recording will usually fit this ranch brand better than an AI narrator.

For the first Cinco prototype, the most defensible stack is therefore: real uploaded product/process footage + Blotato text overlays and editing + a built-in voice if needed. The image/video models should add supporting atmosphere, not manufacture the identity of the brand.

## Implementation check before spending credits

1. Call `GET /v2/credits` to record the starting balance and account email.
2. Call `GET /v2/videos/templates?fields=id,name,description,inputs` and save the exact template/model enum available to this account.
3. Create drafts with `render: false` where the chosen template supports it.
4. Run one cheap Flux Schnell or Imagen 4 Fast storyboard.
5. Review the output and the cost shown in the app before escalating to animation.
6. Never call a publish endpoint during model evaluation.

API references: [Credits API](https://help.blotato.com/api/credits), [Create Visual API](https://help.blotato.com/api/create-video), and [API reference for LLMs](https://help.blotato.com/api/llm).
