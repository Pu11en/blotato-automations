# n8n 18255 — Identify competitor YouTube outlier videos with Bright Data, OpenAI, Sheets and Slack

- Template URL: https://n8n.io/workflows/18255
- Author: Daniel Shashko (@tomax) — verified creator
- Date created: 2026-08-14
- Views (n8n API totalViews, fetched 2026-09-18): 0
- Step order (topological, from workflow JSON): Weekly Channel Scan -> OpenAI Transcript Reader -> OpenAI Brief Writer -> Set Channel Config -> Build Channel Input -> Scrape Channels With Bright Data -> Check Scrape Accepted -> Wait For Snapshot -> Check Snapshot Progress -> Evaluate Scrape Progress -> Videos Ready? -> Download Channel Videos -> Score Video Outliers -> Read Briefed Videos -> Select New Outliers -> Any New Outliers? -> Nothing New This Week -> Read Video Structure -> Rank Video Ideas -> Write Content Brief -> Build Report -> Split Out Idea Rows -> Log Outliers To Sheet -> Post Digest To Slack
- Notes: Paid services: Bright Data (YouTube channel scraper), OpenAI. New (Aug 2026), so view count still 0 in the API.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Score Video Outliers"
- Node type: `n8n-nodes-base.code`
- LLM: (not set / inline in HTTP body)

### Field `.jsCode`

````text
const cfg = $('Set Channel Config').first().json;
const minViews = Number(cfg.min_views) || 0;
const minMultiple = Number(cfg.min_outlier_multiple) || 1.5;
const shortsMax = Number(cfg.shorts_max_seconds) || 0;

const median = (arr) => {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

const round = (n, places) => {
  const f = Math.pow(10, places);
  return Math.round(n * f) / f;
};

const DAY = 86400000;
const seen = new Set();
const videos = [];

for (const item of $input.all()) {
  const j = item.json;
  if (j.error || j.warning) continue;

  const videoId = String(j.video_id || j.shortcode || '');
  if (!videoId || seen.has(videoId)) continue;
  seen.add(videoId);

  const posted = Date.parse(String(j.date_posted || ''));
  if (isNaN(posted)) continue;

  // A video published in the last couple of days has not finished collecting
  // its views, so its views-per-day is inflated and it would top every list.
  const ageDays = Math.max((Date.now() - posted) / DAY, 1);
  if (ageDays < 2) continue;

  const views = Number(j.views) || 0;
  if (views < minViews) continue;

  const length = Number(j.video_length) || 0;
  // Shorts play on a different surface with different view counts, so mixing
  // them into one baseline makes both halves of it meaningless.
  const isShort = shortsMax > 0 && length > 0 && length <= shortsMax;

  videos.push({
    video_id: videoId,
    title: String(j.title || '').trim(),
    channel: String(j.youtuber || j.handle_name || '').trim(),
    channel_url: String(j.channel_url_decoded || j.channel_url || '').trim(),
    // The dataset's own `url` carries tracking parameters. The watch form is
    // stable and fits in a sheet cell.
    video_url: 'https://www.youtube.com/watch?v=' + videoId,
    views,
    likes: Number(j.likes) || 0,
    comments: Number(j.num_comments) || 0,
    // `subscribers` came back on the first row of a channel and null on the
    // rest, so it is filled in per channel below rather than trusted per video.
    subscribers: Number(j.subscribers) || 0,
    posted_on: new Date(posted).toISOString().slice(0, 10),
    age_days: Math.round(ageDays),
    length_seconds: length,
    is_short: isShort,
    category: String(j.category || '').trim(),
    views_per_day: round(views / ageDays, 1),
    // The transcript runs to tens of thousands of characters - 68,000 on one
    // row in testing - and only the opening is evidence of how the video hooks
    // a viewer, so it is cut here rather than in the prompt.
    hook: String(j.transcript || '').replace(/\s+/g, ' ').trim().slice(0, 900),
    chapters: (j.chapters || []).map((c) => String(c.title || '').trim()).filter(Boolean).slice(0, 12),
    description: String(j.description || '').replace(/\s+/g, ' ').trim().slice(0, 400),
  });
}

if (!videos.length) {
  throw new Error(
    'No usable videos came back. Check that the channel URLs are right, lower ' +
    'min_views, or raise videos_per_channel.'
  );
}

// --- each channel is its own baseline ---------------------------------------
// Comparing a channel to the other channels would only tell you which one is
// bigger. What makes a video worth studying is beating the channel that made it.
const byChannel = {};
for (const v of videos) {
  const key = v.channel_url || v.channel || 'unknown';
  (byChannel[key] = byChannel[key] || []).push(v);
}

const outliers = [];
let compared = 0;

for (const group of Object.values(byChannel)) {
  const subs = Math.max(...group.map((v) => v.subscribers), 0);

  for (const pool of [group.filter((v) => !v.is_short), group.filter((v) => v.is_short)]) {
    // Below a handful of videos a median is not a baseline, it is one video
    // wearing a hat, and every comparison against it would be noise.
    if (pool.length < 4) continue;

    const baseline = median(pool.map((v) => v.views_per_day));
    const medianLength = median(pool.map((v) => v.length_seconds));
    if (!baseline) continue;

    compared += pool.length;

    for (const v of pool) {
      v.subscribers = v.subscribers || subs;
      v.channel_baseline_vpd = round(baseline, 1);
      v.channel_video_count = pool.length;
      v.outlier_multiple = round(v.views_per_day / baseline, 2);
      // Likes and comments per thousand views say whether the extra views came
      // with extra attention or were just a thumbnail that got clicked.
      v.engagement_per_1k = v.views ? round(((v.likes + v.comments) / v.views) * 1000, 1) : 0;
      v.length_vs_median = medianLength
        ? round(v.length_seconds / medianLength, 2)
        : 0;

      if (v.outlier_multiple >= minMultiple) outliers.push(v);
    }
  }
}

if (!compared) {
  throw new Error(
    'Not enough videos per channel to build a baseline - each channel needs at ' +
    'least four. Raise videos_per_channel or scan channels that post more often.'
  );
}

if (!outliers.length) {
  throw new Error(
    compared + ' videos were compared and none beat its own channel by ' +
    minMultiple + 'x. Lower min_outlier_multiple, or scan channels with more ' +
    'variance in how their videos perform.'
  );
}

// Stamped after the loop so every row carries the final count.
for (const v of outliers) v.compared = compared;

return outliers
  .sort((a, b) => b.outlier_multiple - a.outlier_multiple)
  .map((json) => ({ json }));
````


## Node: "Read Video Structure"
- Node type: `@n8n/n8n-nodes-langchain.informationExtractor`
- LLM: gpt-5.6-terra via lmChatOpenAi node 'OpenAI Transcript Reader'

### Field `.text`

````text
=Read the opening of a YouTube video and report how it is built.

Describe only what is in the text below. Do not judge the video, do not guess at
its performance, and do not invent chapters that are not listed.

`hook_type` is how the opening line works: a question, a promise, a result, a
story, a demo, or none if the text does not open with any of those.
`topics` are two to five plain lower case noun phrases naming what the video is
about: "cold email setup", "invoice parsing", "vector database costs".

Title: {{ $json.title }}
Channel: {{ $json.channel }}
Chapter titles: {{ ($json.chapters || []).join(' | ') || 'none listed' }}
Description: {{ $json.description || 'none' }}

The first minute of the transcript:
{{ $json.hook || 'no transcript available' }}
````

### Field `.jsonSchemaExample`

````text
{
  "hook_type": "question | promise | result | story | demo | none",
  "hook_line": "the single sentence the video opens on, quoted from the text",
  "topics": [
    "cold email setup",
    "invoice parsing"
  ],
  "promise": "what the opening tells the viewer they will get",
  "has_transcript": true
}
````


## Node: "Rank Video Ideas"
- Node type: `n8n-nodes-base.code`
- LLM: (not set / inline in HTTP body)

### Field `.jsCode`

````text
const cfg = $('Set Channel Config').first().json;
const picks = $('Select New Outliers').all().map((i) => i.json);
// The extractor nests its result under `output` on some versions. Reading the
// item directly gives undefined topics on every video, which produces an empty
// digest on a run where every node is green.
const read = $input.all().map((i) => (i.json && i.json.output) || i.json || {});

// The model ignores the enum often enough to plan for - across earlier
// templates it answered "in-office" and "very negative" to three-value schemas.
// Left unnormalised these become extra categories in the sheet.
const HOOK = (v) => {
  const t = String(v || '').toLowerCase();
  if (/question|ask/.test(t)) return 'question';
  if (/promise|teach|show you|how to/.test(t)) return 'promise';
  if (/result|number|outcome|proof/.test(t)) return 'result';
  if (/story|anecdote|narrative/.test(t)) return 'story';
  if (/demo|walkthrough|build/.test(t)) return 'demo';
  return 'unclear';
};

const clean = (s, max) => String(s || '').replace(/\s+/g, ' ').trim().slice(0, max);

// The extractor emits one item per input item in the same order, so index
// alignment is the join key.
const rows = picks.map((v, i) => {
  const r = read[i] || {};
  const topics = (r.has_transcript === false ? [] : (r.topics || []))
    .map((t) => String(t || '').toLowerCase().trim())
    .filter((t) => t.length > 2 && t.length < 45)
    .slice(0, 5);

  const hookType = HOOK(r.hook_type);

  // The angle is assembled from measured fields and the structure the model
  // read out of the transcript. Nothing here is the model's opinion of whether
  // the video is any good, which is what keeps every clause checkable.
  const pace = v.length_vs_median >= 1.3
    ? 'ran longer than this channel usually does'
    : v.length_vs_median && v.length_vs_median <= 0.7
      ? 'ran shorter than this channel usually does'
      : 'ran about their usual length';

  const angle =
    `${v.outlier_multiple}x this channel's median views per day` +
    (topics.length ? `, on ${topics.slice(0, 2).join(' and ')}` : '') +
    `, opening on a ${hookType} hook, and it ${pace}.`;

  return {
    ...v,
    hook_type: hookType,
    hook_line: clean(r.hook_line, 240),
    promise: clean(r.promise, 240),
    topics,
    angle,
  };
});

const tally = (key) => {
  const m = {};
  for (const r of rows) for (const v of [].concat(r[key] || [])) m[v] = (m[v] || 0) + 1;
  return Object.entries(m).sort((a, b) => b[1] - a[1]).map(([name, count]) => ({ name, count }));
};

return [{
  json: {
    scanned_at: new Date().toISOString().slice(0, 10),
    channels: cfg.competitor_channels,
    // How many videos were compared against a baseline, not how many made the
    // list. "48 videos compared, 3 outliers" stays honest about the sample.
    compared_count: Number($('Score Video Outliers').first().json.compared) || rows.length,
    // Everything that beat its channel, which is not the same as everything
    // that got briefed - ideas_per_run caps the second number. Reporting only
    // the briefed count would quietly shrink the finding to the page size.
    outlier_count: $('Score Video Outliers').all().length,
    briefed_count: rows.length,
    best_multiple: rows.length ? Math.max(...rows.map((r) => r.outlier_multiple)) : 0,
    common_topics: tally('topics').slice(0, 5),
    hook_types: tally('hook_type').slice(0, 5),
    outliers: rows,
  },
}];
````


## Node: "Write Content Brief"
- Node type: `@n8n/n8n-nodes-langchain.chainLlm`
- LLM: gpt-5.6-terra via lmChatOpenAi node 'OpenAI Brief Writer'

### Field `.text`

````text
=You are a content strategist reviewing which competitor videos beat their own channel this week, before deciding what to make next.

Channels scanned: {{ $json.channels }}
Videos compared against their channel's own median: {{ $json.compared_count }}
Videos in front of you: {{ $json.briefed_count }}
Best multiple among them: {{ $json.best_multiple }}
Topics that came up across them: {{ JSON.stringify($json.common_topics) }}
Opening hooks used: {{ JSON.stringify($json.hook_types) }}
The videos themselves: {{ JSON.stringify($json.outliers.map(v => ({ title: v.title, channel: v.channel, multiple: v.outlier_multiple, views: v.views, per_day: v.views_per_day, baseline: v.channel_baseline_vpd, engagement: v.engagement_per_1k, hook: v.hook_type, promise: v.promise, topics: v.topics, chapters: v.chapters }))) }}

Write 4 to 6 sentences covering: which one is worth making your own version of and why, what these videos have in common, and the one structural choice worth copying.

A multiple is measured against that channel's own median views per day, so say "beat its channel" rather than "went viral". These are the top few of the week's outliers, not all of them, so write about "the videos here" and never state how many beat their channel in total. If only one or two videos made the list, say the sample is small rather than describing a pattern. Never claim a video made money or gained subscribers - that is not in this data. Plain sentences, no bullet points, no headings.
````


## Node: "OpenAI Transcript Reader"
- Node type: `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- LLM: gpt-5.6-terra


## Node: "OpenAI Brief Writer"
- Node type: `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- LLM: gpt-5.6-terra
