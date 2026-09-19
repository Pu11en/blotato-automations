# Community slice: Reddit, X, HN, IndieHackers (style cloner / script writer / grader)

Researched 2026-09-18. Live Reddit (www/old, JSON and WebFetch) returned 403 to us, so Reddit threads were read from the arctic-shift archive (`arctic-shift.photon-reddit.com/api/...`). Archive upvote counts are snapshots and may be lower than live. X posts were read via the fxtwitter API. Nothing was posted, voted or bought.

Evidence tiers:
- **Proven**: first-person claim tied to an inspectable channel with real views.
- **Community-validated**: high upvotes relative to the sub, plus commenters confirming it works.
- **Unverified / promotional**: no channel, or selling something. Kept only when the prompt text is useful.

Headline: I found **no community post that is both proven and publishes a full style-DNA prompt**. The one proven operator (Grundström) shares a thin prompt. The best-validated prompts come from r/aitubers posters who show no channel. The strongest community signal is about **what fails** (one-shot AI scripts, inauthentic-content demonetization), and it lines up with the creator frameworks in `creators.md`.

## Ranked findings

### 1. Leo Grundström (@grundstromleo): Claude Project trained on 5 competitor transcripts. PROVEN operator, thin prompt
- Post: https://x.com/grundstromleo/status/1988678974692532635 (2025-11-12, 296 likes, 809 bookmarks, 22K views). Saved: `prompts/community-grundstromleo-claude-project-transcripts.md`.
- Evidence: runs "howtoai", 330K+ subs and 13M+ views by his own account (https://x.com/grundstromleo/status/1958855014157303921, 542 likes). He also sells a course.
- Method: a meta-prompt makes Claude write Project instructions. Upload 5 transcripts of competitors' most viral videos as .txt files. Then write act by act, pasting a same-topic competitor transcript.
- Keep: transcripts as style exemplars; writing act by act. Drop: the same-topic competitor transcript (that is content reuse, not style).
- Key caveat, in his words: "a single video takes over 3 weeks to create with our team of 7 people." Even so, the channel took 3 strikes in 45 days in 2025.

### 2. u/Upper-Mountain-3397: "narrative diffusion" multi-pass writer. COMMUNITY-VALIDATED (moderate)
- https://www.reddit.com/r/aitubers/comments/1rczluj/ (2026-02-24, 52 upvotes, 14 comments; the highest-scored script post found in r/aitubers). Saved: `prompts/community-upper-mountain-narrative-diffusion.md`.
- Passes: structure → ear-first draft at 5th-grade level ("write for the ear not the page", short sentences, varied rhythm) → enrich while keeping events intact → de-AI polish with a banned-word list, "open with tension not context" → optional visual tags.
- Validation: several commenters vouch for it. Dissent: one says a single well-built prompt is enough and prefers Gemini; another claims a 500K-view video with GPT. No channel linked. The author later promotes his own tool (OpenSlop).
- Companion data post: https://www.reddit.com/r/aitubers/comments/1r8pjgb/ (49 upvotes, 80 comments). He tracked 195 AI or faceless channels. Space/science, mystery and animated storytelling do best; motivation and AI-advice niches are "basically dead". Channels that use AI only minimally still have the highest average subs. "what carries them is audio ... thats where retention comes from not the images".

### 3. Hamza Khalid (@humzaakhalid): "Clone any faceless channel with Claude". UNVERIFIED / PROMOTIONAL, closest match to our flow
- https://x.com/humzaakhalid/status/2071162846566854980 (~352K views, 943 bookmarks). Saved: `prompts/community-humzakhalid-clone-channel.md`.
- His competitor-structure breakdown prompt asks for sentence length, a 60-second hook breakdown, emotional triggers, and CTA format and placement. That is almost exactly our style-DNA field list. Stated rule: "studying this channel's structure ... not copying their words or ideas."
- The author has no channel; the post plugs The Claude Kit.

### 4. r/PartneredYoutube inauthentic-content threads: policy reality check. COMMUNITY-VALIDATED (strong)
- https://www.reddit.com/r/PartneredYoutube/comments/1ssybb3/ (2026-04-22, **100 upvotes, 202 comments**). OP reviews channels that were removed from YPP. "every channel I've seen ... they were obviously breaking youtube's policies. Usually copyright/trademark issues or a static image background with a voiceover for a majority of the video." The top comment (41) agrees: "adding a cheap voiceover to a slideshow of images ... doesn't [count as original]. Same for those history channel style videos with public domain footage and a robotic narrator."
- Counter-case in the same thread: @ianilanotv (180K subs, 300M short-form views, writes his own scripts and appears on camera) was falsely flagged, then remonetized 6 days later. "I used generative AI in 2-3 videos when Sora first released. My audience hated it."
- https://www.reddit.com/r/PartneredYoutube/comments/1si1xbi/ (36 upvotes, 65 comments): "it doesn't have to be all of your content. It just has to be a portion of your channel that is contributing significant traffic". Example given: good long-form videos, but viral AI Shorts got the channel dinged.
- https://www.reddit.com/r/PartneredYoutube/comments/1sn0ihk/ (31 upvotes, 105 comments): the complaint thread. Top replies (61, 22) say the flagged channels were mostly low-effort: "An AI voice, simple animations using game assets and a low effort script."
- https://www.reddit.com/r/PartneredYoutube/comments/1o56u7a/: AI script + AI voice + AI images storytelling channel denied for reused content. The useful reply: "Reused Content has nothing to do with AI ... Your account wasn't denied BECAUSE of AI, rather how you used it."

### 5. r/aitubers "you can get away with AI on everything except script". COMMUNITY-VALIDATED (moderate)
- https://www.reddit.com/r/aitubers/comments/1v0qxqa/ (2026-07-19, 14 upvotes, 31 comments). "no matter what I tried the scripts are horrible ... very generic and often doesn't deliver the true points ... shallow." He keeps at most 20% of the AI draft.
- Fixes suggested in replies: "build a style guide ... phrases to avoid ... ask it to proactively recommend improvements after the first draft" (u/Mrconfuddled). "giving ChatGPT some of your existing writing and asking it to analyze your writing style first ... then ... just give it an outline" instead of long rule lists (u/Business_Echo8123). A third commenter reports: "Most of the times it ends up creating tongue twisters ... Or very generic storyline obscuring actual payoff!"
- Same theme: https://www.reddit.com/r/aitubers/comments/1s45iiq/ (22 comments). Scripts were "factual ... tight and concise but they had 0 soul". Another commenter: "treating the script like performance direction ... If every paragraph has the same sentence rhythm and emotional weight, the voiceover ends up sounding like it is reading at the audience". A third: "Claude loves mixing quotes and embellishing truth", so fact-check everything.

### 6. r/NewTubers "Most documentary style YouTube intros lose viewers too early". COMMUNITY-VALIDATED (moderate)
- https://www.reddit.com/r/NewTubers/comments/1tfgfh6/ (2026-05-17, 43 upvotes, 26 comments). "A lot of creators explain the topic too early ... Good documentary scripting usually delays certainty and keeps introducing new unanswered questions."
- Best replies: "dropping the audience mid-scene ... then pulling back to explain", and "specificity is the hook, not the summary". Another: "opening with the most damning detail then immediately pulling back before resolving it". A third warns: "Delayed content can feel scammy" when the promise is never paid off. The distinction the OP settles on: "delaying information" versus "deepening the story" ("every few minutes the situation becomes larger, stranger").

### 7. Retention-graph-to-script mapping + 12-second opening. UNVERIFIED, useful for the GRADER
- https://www.reddit.com/r/aitubers/comments/1vdrpdu/ (3 upvotes) and https://www.reddit.com/r/aitubers/comments/1vp2zb4/ (7 upvotes). Saved: `prompts/community-brilliant-shift-retention-graph-to-script.md`.
- Maps each kind of retention drop to a script cause. Examples: an early drop means an unclear hook; a drop in the setup means background came before the conflict; a drop after a reveal means the reveal answered the question without opening a new one; a slow steady decline means repetitive sections; a drop just before the end means the payoff was predictable.
- The opening template covers 0–3s interrupt, 3–7s promise, and 7–12s stakes. The poster wrote the first 30 seconds himself.

### 8. Haris Mazhar (@fyreinteractive, FacelessOS): "6-dimension analysis". PROMOTIONAL, no prompt text
- https://x.com/fyreinteractive/status/2065120765062811649 (2026-06-11, 707 likes, 47K views, 1,096 bookmarks; the guide is gated behind "comment SCRIPTS + follow + RT"). His blog (https://fyreinteractive.co/blog/best-faceless-youtube-script-tools-2026/) ranks his own product first and gives no channel links.
- The one idea worth taking is his list of analysis fields: **hook structure, pacing map, curiosity-gap architecture, foreshadowing, audience vocabulary, visual-script sync**. He also says transcript + title + thumbnail beats transcript alone, and pushes for concrete figures ("3,847 participants, 34.7% reduction") in place of vague "researchers found".

### 9. u/zhacker: transcript → "same style, different event". PROMOTIONAL
- r/FacelessVideos 1s93y15 (2026-03-31). Saved: `prompts/community-zhacker-transcript-restyle.md`. The views are a third party's (Farzan Films Short, ~3.8M). The workflow is a Frameloop funnel with UTM links and slideshow output.
- Useful bits: cause-and-effect chaining ("every single sentence is a direct reaction to the last"), and a 3-second hook test: "Is there some open question now in my mind which can only be resolved by watching the rest?"

### 10. @woody_research: "$41k/month with Claude". UNVERIFIED, red flags
- Saved: `prompts/community-woody-research-41k-claude.md`. No channel, and the title's $41k contradicts the body's $9,400. Only its before/after story is relevant: 200 views became 40K once "the writing" changed.

### Excluded or low value
- r/aitubers 1rsvnq4 "2 prompts that increased retention" (0 upvotes, AI-written, Notion-vault funnel; commenters mock it). r/ChatGPTPromptGenius "Ultimate YouTube Script Generator MEGA PROMPT" 1lp0pap (9 upvotes, 4 comments, no results shown). r/aitubers 1srwjcf "100k views, 65% retention" (39 upvotes, but it plugs a Telegram TTS bot; one reply calls it an advertisement).
- X "N Claude prompts to start a faceless channel" listicles (@gudanglifehack, @harshitagu72595, @rio_in_ai, @wanneracademy comment-gated NexLev MCP prompts, @zeuuss_01). Engagement bait with no channel.
- Sollo-style and other affiliate "AI YouTube automation" ads, and Gumroad prompt packs: not used.
- IndieHackers: "5 min/day faceless channel" (dinosaur Shorts, 80K views, 60% view-through, uses the Shortsfaceless tool) and "Micro SaaS HQ" (125 subs). Weak and tool-driven.
- Hacker News: no operator threads with script method. Show HN 45949988 is a cautionary data point: 20 videos, a $2–4 CPM and 47 subs.

## Lessons from operators

**What drives retention**
1. **The first 12–30 seconds decide the video, and the best operators write them by hand or grade them hardest.** Put specific stakes first ("Edison robbed Tesla of $50k", not "a young boy went to America"). Drop viewers mid-scene, then pull back. Match the thumbnail and title promise inside the first 12 seconds. (r/aitubers 1vp2zb4, 1se9t2j; r/NewTubers 1tfgfh6.)
2. **Delay certainty, but keep deepening the story.** Open a new question before closing the old one, and make the situation "larger, stranger" every few minutes. Padding that never pays off reads as scammy, and viewers leave before a predictable ending. (1tfgfh6, 1vdrpdu.)
3. **Chain every sentence causally.** Each line should be a reaction to the one before (the But/Therefore principle, see `creators.md` #3). Chronological context-dumping is the usual drop point in the setup. (zhacker breakdown, 1vdrpdu.)
4. **Write for the ear and the narrator.** Aim for a 5th-grade reading level. Vary sentence length dramatically; a uniform rhythm makes even good TTS "read at" the audience. Audio carries retention more than visuals do in faceless formats. (1rczluj, 1s45iiq, 1r8pjgb.)
5. **Multi-pass beats one-shot.** Each pass should have one job: structure, then draft, then enrich, then de-AI. Show the model real exemplar writing and ask it to analyze the style first, rather than piling on rules. (1rczluj, 1v0qxqa.)
6. **Grade against the retention graph, one change at a time.** Timestamp every sentence and label each drop by type. (1vdrpdu.)

**What fails**
1. **One-shot generic AI scripts.** Operators call them "shallow", "sauceless", with "0 soul". They repeat the same sentence structures ("It's not X, it's Y", "The key question is:") and words like delve or tapestry, and create tongue twisters. Viewers and moderators now recognise these patterns, and some commenters in r/aitubers accuse posts of being AI on sight. (1v0qxqa, 1s45iiq, 1rsvnq4.)
2. **Inauthentic or reused content (demonetization).** The pattern that gets channels removed from YPP is an AI or robotic voiceover over static images or slideshows, reused IP or footage, and low-effort AI scripts. It only takes the part of a channel that brings in traffic (for example viral AI Shorts). Appeals are usually rejected. Even a real 330K-sub channel with a 7-person team took 3 strikes in 45 days. (PartneredYoutube 1ssybb3, 1si1xbi, 1sn0ihk, 1o56u7a; Grundström.)
3. **Reusing the competitor's content, not just their structure.** r/PartneredYoutube has recurring "someone copied my script almost word for word, ran it through AI voice" DMCA threads (1to02gb, 42 comments; 1ns82gh step-by-step copyright-strike guide). Our cloner must extract only structural features and never pass competitor sentences or topic facts into the writer.
4. **Unverified facts.** "Claude loves mixing quotes and embellishing truth". History and science niches need a fact-check pass with sources. (1s45iiq, 1raho66.)
5. **Weak niche choice.** Fully-AI channels do well in atmosphere and narrative niches (space, mystery, sleep, animated story). They fail in trust or expertise niches (motivation, AI advice). (1r8pjgb, one poster's dataset, unverified.)

## Implications for our build (short)
- **Style DNA fields** backed by this slice: sentence length and rhythm variance; hook type and the first-12-second beat map; open-loop cadence; reveal and re-question pattern; causal-chain density; reading level; banned LLM-isms; narrator persona; CTA placement; audience vocabulary (Haris); visual-script sync (Haris).
- **Writer**: multi-pass (Upper-Mountain), fed style DNA plus new facts only, with no competitor sentences. Keep the hook as a separate, human-reviewed step.
- **Grader**: the retention-drop taxonomy (Brilliant-Shift), the 3-second open-question test (zhacker), an LLM-ism scan, a fact-check flag, and a flag for "slideshow + AI voice" production risk.
