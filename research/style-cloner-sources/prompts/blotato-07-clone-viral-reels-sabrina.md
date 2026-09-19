# Blotato Template 7 — Clone Viral Reels with AI Avatar (n8n + Make versions)

- Template page: https://help.blotato.com/api/templates/7-clone-viral-reels-with-ai-avatar
- JSON source: Google Drive folder linked from that page (https://drive.google.com/drive/folders/1Hyqe_JVSuLZ59JrKTOBbN4GaXwwoAxnk) — file `7_clone_viral_reels_with_ai_avatar_N8N_TEMPLATE.json`; Make blueprints 7.1/7.2 in the same folder contain the identical rewrite prompt (checked).
- Author: Sabrina Ramonov (Blotato founder; n8n verified creator @sabrina-ramonov; bio claims 1.3M+ followers). Tutorial: https://www.youtube.com/watch?v=BdKqEkdvlgQ (n8n), https://youtu.be/YZn6MuUIW0A (Make)
- Date: not stated on page (Blotato template set published ~Sep 2025; page 'last updated' at fetch time 2026-09-18). Not listed on n8n.io gallery, so no view count.
- Paid services: Apify actor `sian.agency/instagram-ai-transcript-extractor`, OpenAI chat model, HeyGen API (paid plan), Airtable (free tier). Blotato publishes.
- Step order (topological): Structured Output Parser -> OpenAI Chat Model -> Approved -> New Reel URL -> Setup -> If Background -> Create Avatar Video WITH Background Video -> Create Avatar Video WITHOUT Background Video -> Merge -> Wait -> Get Avatar Video -> Check Status -> Upload media -> Instagram [BLOTATO] -> Facebook [BLOTATO] -> Pinterest [BLOTATO] -> Youtube [BLOTATO] -> Linkedin [BLOTATO] -> Twitter [BLOTATO] -> Tiktok [BLOTATO] -> Threads [BLOTATO] -> Bluesky [BLOTATO] -> Check Status1 -> Log Error -> Merge1 -> Generate Script, Caption, Overlay -> Insert Draft -> Download IG Reel -> Wait for Avatar Video
- Logical order: Airtable 'New Reel URL' trigger -> Download IG Reel (Apify transcript) -> Generate Script, Caption, Overlay (LLM) -> Insert Draft (Airtable) -> human 'Approved' checkbox trigger -> HeyGen avatar video -> wait/poll -> Blotato upload + 9 platform posts.
- Lineage: this prompt is a cleaned-up descendant of Dr Firas's n8n 4110 rewrite prompt (same STEP 1/2/3 skeleton, same 'maintain structure' idea), with an added avatar-delivery style example.

Prompt copied VERBATIM from the n8n JSON.

## Node: "Generate Script, Caption, Overlay"
- Node type: `@n8n/n8n-nodes-langchain.chainLlm`
- LLM: gpt-4.1-mini via lmChatOpenAi node 'OpenAI Chat Model'

### Field `.text`

````text
Your task is to rewrite an Instagram reel script, caption, and overlay without inventing a new one. You must follow the rules I give you strictly.
````

### Field `.messages.messageValues[0].message`

````text
=# GIVEN INPUT:
- Original Script : {{ $('Download IG Reel').first().json.transcript }}
- Original Caption : {{ $('Download IG Reel').first().json.caption }}
- Original Hashtags : {{ $('Download IG Reel').first().json.hashtags }}

---

# TASKS

STEP 1: Rewrite the original video script using a new topic/context but closely maintain the original script structure and style.

Follow these rules:
- The rewritten script should be about 30 seconds when spoken aloud. Aim for around 60–75 words in length (1500 characters maximum!)
- Keep it in the same niche and on the exact same topic
- Ensure the idea offers fresh value while staying relevant
- Maintain the nature of the topic (e.g., if it’s a list, yours must also be a list; if it’s a plan, yours must also be a plan)
- Be specific at the same level as the original script (e.g., if the original names tools, you must also name specific tools, not generic ones)
- First sentence should create an irresistible curiosity gap to hook viewers
- Similar sentence count and layout
- Ensure the idea is appealing to a broad audience
- Replace the last sentence with this CTA: "Hit follow to stay up to date!"
- Never use any characers like "" or quotations

You can change:
- Use cases
- Descriptions
- Niche-specific keywords
- Use different examples (e.g., new tools, new strategies) while keeping the same structure/type of content
- Add a unique angle or perspective that helps the idea stand out on social media

Your final output should be in monologue style avatar script, following this example. Capitalization and punctuation instruct the avatar how to speak, so study the following example and emulate its structure, capitalization, and punctuation. Never use em dashes, don't be cringe.

<example>
EVERYONE thought seniors would HATE talking to AI, but they're WRONG! Seniors are now trusting AI to check their blood pressure AND it's WORKING! This study tested voice AI agents helping two thousand seniors report blood pressure over the phone, and here's what happened: AI reached 85% of the people, 60% followed instructions and gave an accurate reading in English or Spanish, if anything was off like dizziness or chest pain, AI escalated to a real nurse, and the voice AI agents raised quality scores from 1 star to 4 stars AND AI cut costs by almost 90%. People were super happy, 9 out of 10 gave it high satisfaction scores,  I love this use case, healthcare needs A LOT OF help!
</example>

STEP 2: Rewrite the caption text using the new topic. Follow these rules:

- Same structure and tone
- Same use of #hashtags but space between each hashtag (max 5 hashtags)
- SEO optimized (maximum 500 characters)
- Use 6th grade reading level.

STEP 3: Write 1 viral sentence, max 8 words, summarizing the content, use 6th grade language, balanced neutral perspective, no emojis, no punctuation except `?` or `!`.

---

# OUTPUT FORMAT EXAMPLE (DO NOT return any explanations. Only return the rewritten sections. NEVER include intermediate thoughts, notes, or formatting.) :
- Script : [REWRITTEN SCRIPT]
- Caption : [REWRITTEN CAPTION]
- Overlay : [OVERLAY]
````
