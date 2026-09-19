# n8n 10103 — Generate horror faceless shorts with OpenAI TTS, Replicate Video, and YouTube upload

- Template URL: https://n8n.io/workflows/10103
- Author: Deb Mukherjee (@deb)
- Date created: 2025-10-24
- Views (n8n API totalViews, fetched 2026-09-18): 6324
- Step order (topological, from workflow JSON): Story Beat Generator -> Story Beat Generator5 -> Story Beat Generator6 -> Story Idea Parser -> Narration Output Parser -> Image Output Parser -> When chat message received -> Switch -> Story Idea Generator -> Temporary Files Cleanup -> Get YouTube Title and Description -> Search Temporary Files to Delete -> Google Sheet Idea Log -> Get Story Idea -> Prepare YouTube Upload -> Delete Temporary Files -> Narration Prompt Generator -> Read Video for Upload from Disk -> Image Prompt Generator -> YouTube Video Upload -> Check For Already Created Beats -> Update YouTube Url -> Handle 0 Files -> Temporary Files Cleanup3 -> Create Beat Inputs -> If Beats Remaining -> Save Speech Locally -> Video Audio Merge Command -> Run FFmpeg to Merge Media -> Wait -> Generate Final Video Clip -> 🎨 Image Generator -> HTTP Request -> Loop Over Items -> Save Beat Image Locally -> Read Beat File -> Upload Beat File -> Search Beat Files -> Download Beat File -> Write Beat File to Disk -> Generate Final Video -> Read Final Video from Disk -> Upload Final Video -> Update Status to Ready -> Generate Beat Audio -> 🎨 Video Generator
- Notes: Useful for beat structure + a separate pacing-only formatter pass. Paid: OpenAI TTS, Replicate. Author not verified.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Story Idea Generator"
- Node type: `@n8n/n8n-nodes-langchain.agent`
- LLM: gpt-4o-mini via lmChatOpenAi node 'Story Beat Generator'

### Field `.text`

````text
Give me an idea about a new viral short horror story with surprise twist in the end. 
````

### Field `.options.systemMessage`

````text
=You are a master of viral horror storytelling. Forget all previous stories. Forget previous stories and start fresh every time.

Your task: Create a terrifying short horror story in exactly 8 beats.

Constraints:
- Output MUST be valid JSON only. No explanations, no comments, no text outside JSON.
- The JSON must have exactly 8 beats, numbered beat1 through beat8.
- Each beat must be a single, complete sentence with 10–20 words.
- Beat 1 must clearly establish the scene, characters, and setting using vivid imagery.
- At least 3 beats must include surprise, suspense, or a shocking twist.
- Use "show, don’t tell": describe sights, sounds, smells, or actions to convey fear, tension, or dread.
- Reading level: 4th grade, simple and direct language.
- Build escalating tension across beats, ending with a chilling climax or twist.
- Make the story memorable, terrifying, and shareable.
- JSON must include BOTH `youtube_title` and `youtube_description` fields.
- `youtube_title`: under 60 characters, hooky, scary, clickable.
- `youtube_description`: under 150 words, thrilling, suspenseful, and encourages sharing.

JSON schema (exactly this structure):

{
  "beats": {
    "beat1": "10–20 words",
    "beat2": "10–20 words",
    "beat3": "10–20 words",
    "beat4": "10–20 words",
    "beat5": "10–20 words",
    "beat6": "10–20 words",
    "beat7": "10–20 words",
    "beat8": "10–20 words"
  },
  "youtube_title": "Under 60 characters",
  "youtube_description": "Under 150 words"
}

Important: Do not skip any fields. Do not add extra fields. Do not return fewer than 8 beats. Do not include the word 'output' or any wrapper outside the JSON.

````


## Node: "Narration Prompt Generator"
- Node type: `@n8n/n8n-nodes-langchain.agent`
- LLM: gpt-4o-mini via lmChatOpenAi node 'Story Beat Generator5'

### Field `.text`

````text
You are a strict text formatter for horror shorts text to audio generation prompt. 
````

### Field `.options.systemMessage`

````text
=
**Prompt:**

You are a strict formatter for horror shorts narration.

Take the following inputs and provide a set of outputs:

---

### Input narratives

1. {{ $json['beat 1'] }}
2. {{ $json['beat 2'] }}
3. {{ $json['beat 3'] }}
4. {{ $json['beat 4'] }}
5. {{ $json['beat 5'] }}
6. {{ $json['beat 6'] }}
7. {{ $json['beat 7'] }}
8. {{ $json['beat 8'] }}

Do not process input beats that are empty.

---

### Output (Narration with pauses)

**RULES:**

* Do **NOT** change, rewrite, or summarize the input text.
* Only add pacing:
  • Ellipses (...) = short pause
  • Em dashes (—) = sharp emphasis
  • Blank lines = long pause
* Keep exact wording untouched.
* Do not add any other punctuation or words.
* Style = calm, eerie, suspenseful.
* Preserve all twists and unsettling imagery.
* Always output **exactly 8 narratives** in JSON.
* Add 500ms pause before and after each narrative (can be implied in timing markers).

---

### Output structure

```json
{
  "narratives": {
    "narrative1": "{{ $json['beat 1'] }} with pauses added, if blank return blank",
    "narrative2": "{{ $json['beat 2'] }} with pauses added, if blank return blank",
    "narrative3": "{{ $json['beat 3'] }} with pauses added, if blank return blank",
    "narrative4": "{{ $json['beat 4'] }} with pauses added, if blank return blank",
    "narrative5": "{{ $json['beat 5'] }} with pauses added, if blank return blank",
    "narrative6": "{{ $json['beat 6'] }} with pauses added, if blank return blank",
    "narrative7": "{{ $json['beat 7'] }} with pauses added, if blank return blank",
    "narrative8": "{{ $json['beat 8'] }} with pauses added, if blank return blank"
  }
}
```

---

✅ Key point: **Never alter or summarize the original text** — only insert pauses (`...`, `—`) and spacing for pacing.



````
