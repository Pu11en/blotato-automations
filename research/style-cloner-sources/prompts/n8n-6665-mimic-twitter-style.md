# n8n 6665 — Generate AI Tweets Mimicking Any Twitter User's Style with OpenAI

- Template URL: https://n8n.io/workflows/6665
- Author: Piotr Sobolewski (@piotrsobolewski) — verified creator
- Date created: 2025-07-29
- Views (n8n API totalViews, fetched 2026-09-18): 1022
- Step order (topological, from workflow JSON): Manual Trigger -> Set Target & Content -> Get User's Tweets -> Prepare Style Examples -> AI: Mimic Style & Generate Tweet -> Consolidate Generated Tweet -> Publish Generated Tweet (Optional)
- Notes: Plain few-shot style mimicry on gpt-3.5-turbo.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Prepare Style Examples"
- Node type: `n8n-nodes-base.function`
- LLM: (not set / inline in HTTP body)

### Field `.function`

````text
let tweetExamples = "";

if (items.length === 0) {
  tweetExamples = "No example tweets found. Cannot mimic style.";
} else {
  tweetExamples = items.map(item => `- "${item.json.text}"`).join('\n');
}

return [{ json: { tweetExamples: tweetExamples, newTweetContent: items[0].json.newTweetContent } }];
````


## Node: "AI: Mimic Style & Generate Tweet"
- Node type: `n8n-nodes-base.openAi`
- LLM: gpt-3.5-turbo

### Field `.messages[0].content`

````text
You are a highly skilled AI specializing in replicating specific writing styles. Your task is to analyze the provided example tweets and then rewrite new content in that exact style. Pay attention to tone, vocabulary, phrasing, brevity, emoji usage, and any unique quirks. The output should be a standalone tweet.

Example Tweets (from target user):
{{ $json.tweetExamples }}
````

### Field `.messages[1].content`

````text
Rewrite the following content as a tweet, mimicking the style of the examples:

Original Content: {{ $json.newTweetContent }}
````
