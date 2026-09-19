# n8n 12045 — Transform viral Instagram Reels into original scripts with AI, Perplexity & Apify

- Template URL: https://n8n.io/workflows/12045
- Author: Neal Mcleod (@ctk-industries) — verified creator
- Date created: 2025-12-23
- Views (n8n API totalViews, fetched 2026-09-18): 681
- Step order (topological, from workflow JSON): Schedule Trigger ->  Run Apify Scraper -> Limit ->  Check Existing Entries ->  Remove Duplicate Reels ->  Add New Reels to Sheet ->  Download Reel Video ->  Transcribe Reel Audio ->  Filter + Generate Script Ideas ->  Research with Perplexity ->  Generate Final Script ->  Update Sheet with Script
- Notes: Paid: Apify, OpenAI (GPT-4o, Whisper), Perplexity.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: " Filter + Generate Script Ideas"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[1].content`

````text
 run a productivity & tech-focused YouTube channel. I'm looking through news archives to find mentions of tools that I can repurpose into educational and tutorial-style content for my audience.

Your task is to take as input a transcript of a news archive, and then determine if the transcription is primarily about a *tool*, a *technology*, or *AI* (including AI-powered products, platforms, or features).

If so, you must:

1. Identify all clearly named tools, technologies, platforms, or AI systems mentioned.

2. For each identified tool or technology, write a clear, actionable list of step-by-step instructions on how to start using it easily (ideally for free or at low cost).  
   - If exact usage details are not provided in the transcript, infer reasonable, generic steps based on similar tools (e.g., sign-up, onboarding, core features).  
   - Focus on steps that a beginner could follow without prior experience.

3. Write one suggestion on how to present this tool or technology in a way that is especially engaging and useful for a productivity/tech audience (e.g., time-saving workflows, automation ideas, comparisons to existing tools, or before/after use cases).

Return your output in **valid JSON** using this exact format:

{
  "verdict": "true or false",
  "tools": ["list", "of", "tools", "or", "resources"],
  "stepByStep": "Detailed, practical instructions on how to start using the tool(s), written as if guiding a beginner.",
  "suggestion": "Comprehensive, in-depth suggestion on how to make this content more interesting and useful to a productivity and tech audience.",
  "searchPrompt": "A short search prompt we'll use to look up the main service. Write it like '{toolName}, the {typeOfTool}'"
}

Rules and clarifications:

- If the verdict is "false", leave all other fields (`tools`, `stepByStep`, `suggestion`, `searchPrompt`) as empty values (e.g., empty list or empty string, as appropriate).
- Only answer based on the information in the transcript plus reasonable assumptions about how such tools usually work.
- Do not include any explanation outside of the JSON. The response must be **only** the JSON object.


````


## Node: " Research with Perplexity"
- Node type: `n8n-nodes-base.httpRequest`
- LLM: (not set / inline in HTTP body)

### Field `.jsonBody`

````text
={
  "model": "sonar-pro",
  "messages": [
    {
      "role": "system",
      "content": "Be precise and concise."
    },
    {
      "role": "user",
      "content": "Tell me four interesting (peculiar) things about {{ $json.message.content.searchPrompt }}"
    }
  ]
}
````


## Node: " Generate Final Script"
- Node type: `@n8n/n8n-nodes-langchain.openAi`
- LLM: gpt-4o

### Field `.messages.values[1].content`

````text
I run a productivity & tech-focused YouTube channel.

My editors would like to make a new video. They've found an interesting tool or technology, compiled a step-by-step guide on how to use it, done some searching on the Internet to find some interesting things about it, wrote a rough draft about it, and we also had our chief editor write concrete suggestions for how to make the content better.

Your task is to take as input all of these things, and then write a new, high quality script for us to feature.

Return your output in JSON using this format:

{
 "script": "Your script goes here (~100 words)."
}

Rules:

	* Use a casual, spartan tone of voice. No frills. Be straightforward, and don't use poetic language.
	* The video is for a productivity & tech audience on YouTube (people who like tools, automations, and workflows).
	* End the script with a call to action like "Want {thing}? Just comment {keyword} and I’ll reply with the link."
````

### Field `.messages.values[2].content`

````text
={
  "script": "There’s a new AI text-to-speech tool that’s basically on par with ElevenLabs—but it’s free. You get over 400 voices, support for 60 languages, and it’s completely unlimited with no signup required. Here’s how it works: go to the website, paste your script, choose a voice you like, and click generate. You’ll get a clean audio file you can drop straight into your YouTube videos, shorts, tutorials, or even course content. If you want to test it for your own channel, just comment 'speech' and I’ll reply with the link."
}
````

### Field `.messages.values[3].content`

````text
={
  "toolNames":"{{ $(' Filter + Generate Script Ideas').item.json.message.content.tools.join() }}",
  "roughDraftScript":"{{ $(' Transcribe Reel Audio').all().first().json.text }}",
  "perplexityOutput": "{{ $json.choices[0].message.content }}",
  "stepByStepGuide":"{{ $(' Filter + Generate Script Ideas').item.json.message.content.stepByStep }}",
  "suggestionsForImprovement":"{{ $(' Filter + Generate Script Ideas').item.json.message.content.suggestion }}"
}
````
