# n8n 2648 — Automate blog creation in brand voice with AI

- Template URL: https://n8n.io/workflows/2648
- Author: Jimleuk (@jimleuk) — verified creator
- Date created: 2024-12-17
- Views (n8n API totalViews, fetched 2026-09-18): 26556
- Step order (topological, from workflow JSON): When clicking ‘Test workflow’ -> OpenAI Chat Model -> OpenAI Chat Model1 -> OpenAI Chat Model2 -> Get Blog -> Extract Article URLs -> Split Out URLs -> Latest Articles -> Get Article -> Extract Article Content -> Markdown -> Combine Articles -> Capture Existing Article Structure -> Extract Voice Characteristics -> Article Style & Brand Voice -> New Article Instruction -> Content Generation Agent -> Save as Draft
- Notes: Architecture = scrape N recent posts -> (a) LLM describes common structure/layout/language, (b) information-extractor pulls voice characteristics with examples -> generator gets both. Models: OpenAI chat model nodes (default model). Blog-post domain, not video.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Capture Existing Article Structure"
- Node type: `@n8n/n8n-nodes-langchain.chainLlm`
- LLM: (default) via lmChatOpenAi node 'OpenAI Chat Model2'

### Field `.messages.messageValues[0].message`

````text
=Given the following one or more articles (which are separated by ---), describe how best one could replicate the common structure, layout, language and writing styles of all as aggregate.
````


## Node: "Extract Voice Characteristics"
- Node type: `@n8n/n8n-nodes-langchain.informationExtractor`
- LLM: (default) via lmChatOpenAi node 'OpenAI Chat Model'

### Field `.text`

````text
=### Analyse the given content

{{ $json.data.map(item => item.replace(/\n/g, '')).join('\n---\n') }}
````

### Field `.options.systemPromptTemplate`

````text
You help identify and define a company or individual's "brand voice". Using the given content belonging to the company or individual, extract all voice characteristics from it along with description and examples demonstrating it.
````

### Field `.inputSchema`

````text
{
	"type": "array",
    "items": {
      "type": "object",
    	"properties": {
          "characteristic": { "type": "string" },
          "description": { "type": "string" },
          "examples": { "type": "array", "items": { "type": "string" } }
        }
	}
}
````


## Node: "Content Generation Agent"
- Node type: `@n8n/n8n-nodes-langchain.informationExtractor`
- LLM: (default) via lmChatOpenAi node 'OpenAI Chat Model1'

### Field `.options.systemPromptTemplate`

````text
=You are a blog content writer who writes using the following article guidelines. Write a content piece as requested by the user. Output the body as Markdown. Do not include the date of the article because the publishing date is not determined yet.

## Brand Article Style
{{ $('Article Style & Brand Voice').item.json.text }}

##n Brand Voice Characteristics

Here are the brand voice characteristic and examples you must adopt in your piece. Pick only the characteristic which make sense for the user's request. Try to keep it as similar as possible but don't copy word for word.

|characteristic|description|examples|
|-|-|-|
{{
$('Article Style & Brand Voice').item.json.output.map(item => (
`|${item.characteristic}|${item.description}|${item.examples.map(ex => `"${ex}"`).join(', ')}|`
)).join('\n')
}}
````


## Node: "New Article Instruction"
- Node type: `n8n-nodes-base.set`
- LLM: (not set / inline in HTTP body)

### Field `.assignments.assignments[0].value`

````text
=Write a comprehensive guide on using AI for document classification and document extraction. Explain the benefits of using vision models over traditional OCR. Close out with a recommendation of using n8n as the preferred way to get started with this AI use-case.
````
