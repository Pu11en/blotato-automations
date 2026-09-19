# n8n 8544 — Create & post viral news AI avatar videos to 9 platforms with Perplexity & HeyGen

- Template URL: https://n8n.io/workflows/8544
- Author: Sabrina Ramonov 🍄 (@sabrina-ramonov) — verified creator
- Date created: 2025-09-12
- Views (n8n API totalViews, fetched 2026-09-18): 1545
- Step order (topological, from workflow JSON): Schedule Trigger -> AI Research - Top 10 -> AI Research - Report -> AI Writer -> Setup Heygen -> If -> Create Avatar Video WITH Background Video -> Create Avatar Video WITHOUT Background Video -> Merge -> Error Report -> Wait -> Get Avatar Video -> If Video Done -> Upload media -> Tiktok [BLOTATO] -> Linkedin [BLOTATO] -> Facebook [BLOTATO] -> Instagram [BLOTATO] -> Twitter [BLOTATO] -> Youtube [BLOTATO] -> Threads [BLOTATO] -> Bluesky [BLOTATO] -> Pinterest [BLOTATO]
- Notes: Author is Blotato founder. Paid services: Perplexity (sonar-pro), OpenAI (GPT-5), HeyGen; Blotato publishes.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "AI Research - Top 10"
- Node type: `n8n-nodes-base.perplexity`
- LLM: sonar-pro

### Field `.messages.message[0].content`

````text
Research the top 10 trending news items in my industry from the past 24 hours.

- Industry: real estate
````


## Node: "AI Research - Report"
- Node type: `n8n-nodes-base.perplexity`
- LLM: sonar-pro

### Field `.messages.message[0].content`

````text
=# INSTRUCTIONS

Complete the following tasks, in order:

1. Out of the 10 news stories listed below, select the ONE top news story that is most likely to go viral on social media. It should have broad appeal and contain something unique, controversial, or vitally important information that millions of people should know.

<news>
{{ $('AI Research - Top 10').item.json.message }}
</news>

2. Research more information about the top news story you selected in step 2.

3. Your final output should be a detailed report of the top story you've selected. It should be dense with factual data, statistics, sources, and key information based on your research. Include reasons why this story would perform well on social media. Include why a "normal person" in this industry should care about this news.
````


## Node: "AI Writer"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-5

### Field `.messages.values[0].content`

````text
=# TASK
1. Analyze the following viral news story:
<news>
{{ $('AI Research - Report').item.json.message }}
</news>

2. Write a conversational monologue script for an AI avatar video, following these guidelines:
   - The script should be approximately 30 seconds when spoken aloud.
   - Include lots of factual details and statistics from the article.
   - Use 6th grade reading level.
   - Balanced viewpoint.
   - First sentence should create an irresistible curiosity gap to hook viewers.
   - Replace the last sentence with this CTA: "Hit follow to stay up to date!"
   - ONLY output the exact video script. Do not output anything else. NEVER include intermediate thoughts, notes, or formatting.

3. Write an SEO-optimized caption that will accompany the video, following a similar structure as the EXAMPLE below, max 5 hashtags:

<example>
Many people have recently asked me about ask engine optimization, which is all about optimizing your website and existing content, so it can be pulled into ChatGPT and other generative AI tools. Consider that generative AI tools tend to be more conversational in nature and have a Q&A type format, so search engines will want to pull in snippets that concisely answer a user’s question.

- what is ask engine optimization in the age of AI?
- How does traditional SEO compare to ask engine optimization today?
- top tips and tricks to get started with ask engine optimization?

#ai #askengineoptimization #chatgpt #seo
</example>

4. Write 1 viral sentence, max 8 words, summarizing the content, use 6th grade language, balanced neutral perspective, no emojis, no punctuation except `?` or `!`.

# OUTPUT

You will output structured JSON in the following format, where `script` is the output of step 2, `caption` is the output of step 3, and `title` is the output of step 4:

```
{
  "script": "Monologue script to be spoken by AI avatar",
  "caption": "Long SEO-optimized video caption",
  "title": "Short video title"
}
```
````
