# n8n 4110 — Clone viral TikToks with AI avatars & auto-post to 9 platforms using Perplexity & Blotato

- Template URL: https://n8n.io/workflows/4110
- Author: Dr. Firas (@drfiras) — verified creator
- Date created: 2025-05-16
- Views (n8n API totalViews, fetched 2026-09-18): 135324
- Step order (topological, from workflow JSON): Trigger: Get TikTok URL via Telegram -> Download TikTok Video (RapidAPI) -> Extract Video Thumbnail -> Upload Thumbnail to Cloudinary -> Analyze Thumbnail (GPT-4o Vision) -> Extract Overlay Text (GPT-4o) -> Download TikTok Audio -> Transcribe Audio to Script (GPT) -> Generate Unique Template ID -> Save Original Video to Google Sheets -> Suggest Similar Idea (Perplexity) -> Clean Perplexity Response -> Rewrite Script, Caption, Overlay (GPT-4o) -> Split Rewritten Content into Sections -> Generate New Video ID -> Save Rewritten Video to Google Sheets -> Fetch Available Avatars -> Generate Video with Avatar -> Wait for Avatar Rendering (3 min) -> Fetch Avatar Video URL -> Add Overlay Text with JSON2Video -> Wait for Caption Rendering -> Fetch Final Video from JSON2Video -> Update Final Video URL in Sheet -> Send Video URL via Telegram -> Send Final Video Preview -> Assign Social Media IDs -> Upload Video to Blotato -> INSTAGRAM -> YOUTUBE -> TIKTOK -> FACEBOOK -> THREADS -> TWETTER -> LINKEDIN -> BLUESKY -> PINTEREST
- Notes: Paid services in the chain: RapidAPI TikTok downloader, OpenAI (GPT-4o, Whisper), Perplexity, Cloudinary, Captions.ai avatar, JSON2Video. Blotato is only the publisher.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Transcribe Audio to Script (GPT)"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: (not set / inline in HTTP body)


## Node: "Suggest Similar Idea (Perplexity)"
- Node type: `n8n-nodes-base.httpRequest`
- LLM: (not set / inline in HTTP body)

### Field `.jsonBody`

````text
={
  "model": "sonar-reasoning",
  "messages": [
    {
      "role": "user",
      "content": "Suggest a content idea different from this video script: \"{{ $json['Modèle de script vidéo'] }}\". It should be in the same niche and on the exact same topic or content idea but offer fresh value. You must pick one idea from your research that matches the topic idea of the video script exactly but is also different and unique from it so it would stand out on social media. Example: if the video script contains a list of tools, your topic must also be a list of tools in that video script topic but slightly different, maybe different tools etc. If the video's script is about a plan, strategies, or whatever, you must also make your topic about that. So you must maintain the nature of the topic in the video script. You absolutely must be specific as the original video script. You can't just mention generic tools or strategies if the original video script contains specific tools. Etc. That is the level of accuracy and perfect matching of the video script original topic. Make sure it appeals to a broad audience like the example."
    }
  ]
}

````


## Node: "Clean Perplexity Response"
- Node type: `n8n-nodes-base.code`
- LLM: (not set / inline in HTTP body)

### Field `.jsCode`

````text
// Step 1: Pull raw input
let raw = $input.first().json.choices[0].message.content;
// Step 2: Forcefully remove anything between <think> and </think>
let cleaned = raw.replace(/<think>(.|\n)*?<\/think>/gi,
'').trim();
// Optional cleanup: remove leading/trailing blank lines
cleaned = cleaned.replace(/^\s+|\s+$/g, '');
// Done
return [
{
json: {
cleanedResponse: cleaned
}
}
];

````


## Node: "Rewrite Script, Caption, Overlay (GPT-4o)"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[0].content`

````text
=You are rewriting a TikTok video script, caption, and overlay —
not inventing a new one. You must follow this format and obey
these rules strictly.
---
### CONTEXT:
Here is the content idea to use:
{{ $json.cleanedResponse }}

---
### STEP 1: Rewrite the original video script BELOW using the new
topic/context above but maintaiin as stubbornly as possible the
original script structure and style:
Original script: {{ $('Save Original Video to Google Sheets').item.json['Modèle de script vidéo'] }}


🛑 DO NOT CHANGE the original structure or style but
This includes:
- Numbered list
- Sentence breaks
- "I" or first-person narration
- Colloquial/informal tone (like “you're gonna wanna...”)
✂️ You MUST keep:
- first person narration of the orignal script at all costs
- MUST be under 700 characters (yes "Characters" not wordcount)
this is an absolute MUST, no more than 700 characters!!! But never
change the structure or narration style of the original script. It
must be an exact imitation.
✏️ You MAY change:
- Tool names
- Use cases
- Descriptions
- Niche-specific keywords

#Rule: never use any characers like "" in your generated video
script as this will yeild syntax errors.
---
### STEP 2: Rewrite the caption text using the new topic.
Keep:
- Same structure and tone
- Same use of #hashtags but space between each hashtag
- Similar sentence count and layout
Caption:
{{ $('Save Original Video to Google Sheets').item.json.Caption }}

---
### STEP 3: Rewrite the text overlay (short version for the
thumbnail or first screen)
Keep:
- EXACT Same length format, case, structure
- Do NOT invent new words unless absolutely necessary
Overlay:
{{ $('Save Original Video to Google Sheets').item.json['Modèle de texte superposé'] }}
---
### FINAL OUTPUT FORMAT (no markdown formatting):
Text Overlay: [REWRITTEN TEXT OVERLAY]
Video Script: [REWRITTEN SCRIPT]
Caption Text: [REWRITTEN CAPTION TEXT]
DO NOT return any explanations. Only return the rewritten
sections.
````


## Node: "Analyze Thumbnail (GPT-4o Vision)"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o


## Node: "Extract Overlay Text (GPT-4o)"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[0].content`

````text
=Identify the primary text located at the top of the image described above:
{{ $json.content }}

Return only that specific top text as the output.

Do not include any quotation marks.

Focus only on the top section's text in the image and disregard any other content.
````
