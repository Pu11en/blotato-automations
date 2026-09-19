# n8n 14825 — Turn top Instagram reels into 7 new scripts using Apify, OpenAI, Claude and Google Sheets

- Template URL: https://n8n.io/workflows/14825
- Author: Jonas Frewert (@jonasfrewert) — verified creator
- Date created: 2026-04-06
- Views (n8n API totalViews, fetched 2026-09-18): 358
- Step order (topological, from workflow JSON): When clicking ‘Execute workflow’ -> Run an Actor1 -> Get dataset items1 -> Sort1 -> Limit1 -> Filter -> HTTP Request -> Transcribe a recording -> Combine Transcripts -> Message a model1 -> Format AI Output1 -> Append row in sheet1
- Notes: Only template in the set that sends multiple competitor transcripts to Claude (claude-sonnet-4-5) in one call. Paid: Apify, OpenAI Whisper.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Combine Transcripts"
- Node type: `n8n-nodes-base.code`
- LLM: (not set / inline in HTTP body)

### Field `.jsCode`

````text
const transcripts = items
  .map(item => item.json.text)
  .filter(Boolean)
  .join('\n\n');

return [
  {
    json: {
      transcripts
    }
  }
];
````


## Node: "Message a model1"
- Node type: `@n8n/n8n-nodes-langchain.anthropic`
- LLM: claude-sonnet-4-5-20250929

### Field `.messages.values[0].content`

````text
=You are an expert TikTok content strategist and copywriter.

Analyze the following high-performing video transcripts:

{{ $json.transcripts }}

Based on these, create 7 new viral video scripts.

Requirements:
- Use strong, slightly controversial hooks
- Focus on real problems, solutions, and results
- Keep it engaging and natural (not robotic)
- Make it feel like spoken content (not written captions)
- Do NOT say SEO is dead

Each script should follow:
Hook → Problem → Solution → How to implement

Return clean output with 7 separate scripts.

Return the scripts as clean JSON like this:

[
  {
    "hook": "...",
    "problem": "...",
    "solution": "...",
    "how_to_implement": "..."
  }
]

Return ONLY a valid JSON array.
Do not include any explanation, text, or formatting outside the JSON.
No intro text like "Here are 7 scripts".
Only return the JSON.
````
