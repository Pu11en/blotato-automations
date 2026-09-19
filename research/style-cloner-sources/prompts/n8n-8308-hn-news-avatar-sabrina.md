# n8n 8308 — Generate & auto-post tech news AI avatar videos to social media with Heygen and Blotato

- Template URL: https://n8n.io/workflows/8308
- Author: Sabrina Ramonov 🍄 (@sabrina-ramonov) — verified creator
- Date created: 2025-09-05
- Views (n8n API totalViews, fetched 2026-09-18): 1228
- Step order (topological, from workflow JSON): Schedule Trigger -> Fetch HN Article -> Fetch HN Front Page -> Write Script -> AI Agent -> Write Long Caption -> Write Short Caption -> Setup Heygen -> If -> Create Avatar Video WITH Background Video -> Create Avatar Video WITHOUT Background Video -> Merge -> Wait -> Get Avatar Video -> Upload media -> Tiktok [BLOTATO] -> Linkedin [BLOTATO] -> Facebook [BLOTATO] -> Instagram [BLOTATO] -> Twitter [BLOTATO] -> Youtube [BLOTATO] -> Threads [BLOTATO] -> Bluesky [BLOTATO] -> Pinterest [BLOTATO]
- Notes: Author is Blotato founder. Paid services: HeyGen API, OpenAI; Blotato publishes.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "AI Agent"
- Node type: `@n8n/n8n-nodes-langchain.agent`
- LLM: gpt-4.1 via lmChatOpenAi node 'Write Script'

### Field `.text`

````text
# INSTRUCTIONS

Perform the following tasks, in order:

1. Fetch the top 10 stories from Hacker News from the past 24 hours related to AI or LLMs. 

2. Select the top story that is most likely to go viral on social media. 

3. Fetch the article and Hacker News comments.

4. Create a 20-second monologue script for an AI avatar video, following these guidelines:
   - The script should be approximately 30 seconds when spoken aloud.
   - Include lots of details and statistics from the article.
   - Use 6th grade reading level.
   - Balanced viewpoint.

5. Update the script's first sentence to use sensational viral hooks, tailored to the content, that grab the viewer's attention.

6. Replace the last sentence with: "Hit follow to stay ahead in AI!"

# OUTPUT FORMAT

ONLY output the exact video script. Do not output anything else. NEVER include intermediate thoughts, notes, or formatting.
````


## Node: "Write Long Caption"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[0].content`

````text
=# EXAMPLE

<example>
Many people have recently asked me about ask engine optimization, which is all about optimizing your website and existing content, so it can be pulled into ChatGPT and other generative AI tools. Consider that generative AI tools tend to be more conversational in nature and have a Q&A type format, so search engines will want to pull in snippets that concisely answer a user’s question.- what is ask engine optimization in the age of AI?- How does traditional SEO compare to ask engine optimization today?- top tips and tricks to get started with ask engine optimization?

#ai #askengineoptimization #chatgpt #seo
</example>

# CONTEXT

Infer the topic from the sources provided.

# WRITING STYLE

Here’s how you always write:

<writing_style>

- Your writing style is spartan and informative.
- Use clear, simple language.
- Employ short, impactful sentences.
- Use active voice; avoid passive voice.
- Focus on practical, actionable insights.
- Incorporate data or statistics to support claims when possible.
- Use """"""""you"""""""" and """"""""your"""""""" to directly address the reader.
- Avoid metaphors and clichés.
- Avoid generalizations.
- Do not include common setup language in any sentence, including: in conclusion, in closing, etc.
- Do not output warnings or notes—just the output requested.
- Do not use hashtags.
- Do not use semicolons.
- Do not use emojis.
- Do not use asterisks.
- Do not use adjectives and adverbs.
- Do NOT use these words:
""""""""""""""""""""""""can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe, delve, embark, enlightening, esteemed, shed light, craft, crafting, imagine, realm, game-changer, unlock, discover, skyrocket, abyss, you're not alone, in a world where, revolutionize, disruptive, utilize, utilizing, dive deep, tapestry, illuminate, unveil, pivotal, enrich, intricate, elucidate, hence, furthermore, realm, however, harness, exciting, groundbreaking, cutting-edge, remarkable, it. remains to be seen, glimpse into, navigating, landscape, stark, testament, in summary, in conclusion, moreover, boost, bustling, opened up, powerful, inquiries, ever-evolving""""""""""""""""""""""""
</writing_style>

# PLANNING

Your goal is to write a 50-word video caption based on the provided source.

1. Analyze the provided sources thoroughly.
2. Study the <example> post carefully. You will be asked to replicate their:
    - Overall structure.
    - Tone and voice.
    - Formatting (including line breaks and spacing).
    - Length (aim for a similarly detailed post).
    - Absence of emojis.
    - Max 5 relevant hashtags.
    - Emotional resonance.

# OUTPUT
Follow the GUIDELINES below to write the post. Use your analysis from step 1 and step 2. Use the provided sources as the foundation for your post, expanding on it significantly while maintaining the style and structure of the examples provided from step 2. You MUST use information from the provided sources. Make sure you adhere to your <writing_style>.

<guidelines>
The description should be structured as follows:
1. Start with 1 paragraph summarizing the source
2. Newline, followed by 3 bullet points of questions that a viewer might ask on a search engine about the source
3. Newline, followed by these hashtags: #ai #artificialintelligence #ainews #sabrinaramonov #aiavatar
</guidelines>

Take a deep breath and take it step-by-step!

# INPUT
Use the following information sources:
<sources>
{{ $json.output }}
</sources>
````


## Node: "Write Short Caption"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[0].content`

````text
=Write a 1 viral sentence, max 90 characters, summarizing the video content, use 6th grade language, balanced neutral perspective, no emojis:

<content>
{{ $json.message.content }}
</content>
````
