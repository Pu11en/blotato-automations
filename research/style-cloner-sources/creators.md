# Creator frameworks for the style cloner, script writer and grader

Researched 2026-09-18. Verbatim quotes, timestamps and source headers are in `prompts/creator-*.md`. Subscriber counts come from yt-dlp on 2026-09-18. View totals that only the creator reports are marked as claims. Timestamps come from YouTube auto-captions, so the quotes may contain small transcription errors.

Pipeline parts: **DNA** = style-DNA fields pulled from competitor transcripts · **STRUCT** = script structure rules for the writer · **GRADE** = grader rubric.

## Ranked frameworks

### 1. Deliver on the click → intrigue → seamless bridge (Paddy Galloway, echoed by MrBeast, Colin & Samir, Johnny Harris, YouTube Help)
- **Says:** in the first 5–10 s, confirm what the title and thumbnail promised, visually or verbally. Then add a *specific* intrigue sentence ("he discovered something in October of 2017 that changed everything"). Give "the necessary context, not over context". Then flow into the first beat with a bridge ("starting with…"), not a signpost ("let's get into it"). Colin & Samir: context by 7 s and "by 30 seconds [...] a new hook". YouTube's own "Intro" metric is the share of viewers still watching at 30 s, and it says a high score means "the content in the first 30 seconds matched the viewer's expectation of the video's thumbnail and title."
- **Proof:** Paddy claims about 50B lifetime views and about 10B/yr for current clients (MrBeast, Mark Rober, Ryan Trahan, Red Bull); his own channel has 531K subs. MrBeast has 517M subs. Colin & Samir have 1.63M. Johnny Harris has 7.96M.
- **Where:** Sweat Equity podcast 2026-02-17 (youtu.be/dAR3d6xnG0o, 52:21–59:36); Colin & Samir 2025-04-09 (youtu.be/L9CO1FcRHCM, 80:10–82:28); support.google.com/youtube/answer/9314415
- **Ready prompt:** none.
- **Drives:** STRUCT (intro template) · GRADE (`click_confirmation_by_10s`, `specific_intrigue_line`, `context_not_overcontext`, `bridge_not_signpost`) · DNA (`intro_type`: statement+intrigue / multiple questions+promise / cold-open action; `seconds_to_click_confirmation`; `intro_word_count`).

### 2. Minute-mark retention map (MrBeast production guide)
- **Says:** "The first minute of each video is the most important minute". Minutes 1–3: "Stop telling people what they will be watching and start showing them", with "crazy progression" (cover a lot of ground fast). A "re-engagement" at about 3:00 and again at about 6:00. Minutes 3–6 carry "the most exciting and interesting content that is also very simple". Long explanations go in the back half. "Don't ever signal the end [...] unless it's to build hype for the [...] payoff". "No dull moments". "The video endings must always be abrupt to protect retention."
- **Proof:** 517M subs. The guide cites a 60M-click video.
- **Where:** leaked internal PDF, Sept 2024 (simonwillison.net/2024/Sep/15/…; PDF copy at danielscrivner.com). Pages 5–10, 29, 35.
- **Ready prompt:** none.
- **Drives:** STRUCT (the writer places beats by timestamp at about 150 wpm; re-engagement beats at about 3:00/6:00; heavy exposition after about 6:00) · GRADE (`reengagement_at_3m`, `reengagement_at_6m`, `no_dull_stretch > N s`, `no_early_end_signal`, `abrupt_ending_after_payoff`) · DNA (`reengagement_timestamps`, `where_exposition_lives`, `outro_length_s`).
- **Caveat:** written for host-led spectacle videos. For faceless explainers, a "re-engagement" is a surprising fact, a reveal or a twist, not a stunt.

### 3. But/Therefore causal chaining (Trey Parker & Matt Stone; popularised for YouTube by Kallaway)
- **Says:** "if the words and then belong between those beats [...] you got something pretty boring. What should happen between every beat [...] is either the word therefore or but." Kallaway turns this into "a dance between context and conflict": conflicts open loops and context closes them.
- **Proof:** South Park, with multiple Emmys. Kallaway (458K YT subs, claims over 1B views) says his top video uses four but/then loops in its first 30 s.
- **Where:** NYU/MTVU "Stand In" lecture (youtu.be/vGUNqq3jVLg, 00:56); Kallaway "How To Become A Master Storyteller" 2024-11-04 (youtu.be/t5Z-Q1bg1tU, 00:28–02:46)
- **Ready prompt:** none. The most mechanically checkable rule in the set.
- **Drives:** GRADE (`causal_link_ratio` = BUT+THEREFORE links ÷ all beat links; flag every AND-THEN run) · DNA (`but_therefore_ratio`, `conflict_beats_per_minute`) · STRUCT (outline beats must be linked by BUT/THEREFORE).

### 4. Open loops and payoffs: setup→tension→payoff, "Soon X, first Y", re-hooks, the focus-group test (George Blackman, Paddy Galloway, Kallaway, Jake Tran, YouTube Creator Insider)
- **Says:** Blackman: the audience must "always [have] something to look forward to in the next 60-90 seconds". Each mini-payoff is split into "Setup / Tension / Payoff", and giving the payoff first cost one of his videos "43% of the audience" in under a minute. Paddy: "soon X first Y [...] your X and your Y both need to be interesting". His "made-up focus group" test: pause at any minute and ask what the viewer expects next. Plan retention devices on a one-page skeleton. Kallaway: "rehooking [...] mini hooks between the end of one point and the beginning of the next." Jake Tran (faceless, 1.84M subs): "the title thumbnail leaves you on an open loop then the hook makes you watch the next part". YouTube's Matt Koval: tease a "big climax" in the hook.
- **Proof:** Blackman was Ali Abdaal's scriptwriter (Ali has 6.69M subs; Blackman claims 1M+ average views per video he wrote). Paddy, Kallaway and Tran as above. Koval is YouTube staff.
- **Where:** writewithai.substack.com/p/write-a-killer-youtube-script-like (2024-03-24); Sweat Equity 60:31–64:36; youtu.be/7I50PECz7SU 15:36; youtu.be/Si5QRdfkdPg 07:48–09:14; youtu.be/b8RT5w-QISY
- **Ready prompt:** YES. Blackman's "Target-Transformation-Stakes" hook prompt, verbatim in `prompts/creator-george-blackman.md`. It includes a banned-word list ("unlock, skyrocket, game-changer, realm…") worth reusing.
- **Drives:** GRADE (`max_gap_between_payoffs_s` ≤ 90; `every_open_loop_closed`; `payoff_not_before_setup`; `rehook_at_each_section_transition`; `focus_group_test` at 1/3/6 min, where an LLM predicts what comes next and passes if it names something specific) · DNA (`open_loops_per_minute`, `avg_loop_span_s`, `rehook_phrases` (patterns only), `foreshadow_density`) · STRUCT (the writer places an explicit loop ledger on the skeleton before drafting prose).

### 5. Misconception-first explaining / common belief → contrarian snapback (Derek Muller; Kallaway)
- **Says:** Muller: "a clear expository summary is worse than no instruction at all [...] you always have to start with the misconceptions". Students given a clear explainer scored 6.0 → 6.3/26, while students given a video that voiced the misconception scored 11/26. Kallaway's hook does the same at small scale: "context lean", then a "scroll stop interjection" ("but…"), then a "contrarian snapback". His intro states "the common take or belief" and then a "contrarian approach".
- **Proof:** Veritasium has 21.3M subs, and this finding comes from Muller's PhD (University of Sydney, 2008), a controlled study and the only experimental evidence in this set. Kallaway as above.
- **Where:** TEDx talk (youtu.be/RQaW2bFieo8, 03:47–05:39); thesis record per-central.org/items/detail.cfm?ID=11344; Kallaway hooks 2024-12-19 (youtu.be/LmXpbP7dD48, 01:21–04:31), script video 07:51–09:38
- **Ready prompt:** none.
- **Drives:** STRUCT (each major section opens with the intuitive/wrong belief, then corrects it) · GRADE (`states_misconception_before_answer` per section; `hook_has_contrast_turn`) · DNA (`hook_pattern`: context-lean / interjection / snapback present? `misconception_sections_share`).

### 6. Promise architecture and active prose (Johnny Harris, ex-Vox)
- **Says:** the title is "a promise I know I'm going to answer". "Reinforce the promise of the thumbnail within the first minute" but answer it by the end. Open by dropping the viewer "into action", not "tell them what you're going to tell them". Write "who did what to whom" with agents doing visible things (from Pinker, *The Sense of Style*). Speak to the viewer ("look at this"). Near the end, "zoom out and reflect" with "conclusion energy". He writes a two-column script: a visual direction for every one or two sentences.
- **Proof:** 7.96M subs; Vox "Borders".
- **Where:** David Perell interview 2025-03-12 (youtu.be/zq4b96m1AvM, 10:43–13:03, 18:11–24:26, 31:25–32:22, 50:10, 60:38)
- **Ready prompt:** none.
- **Drives:** DNA (`opening_type`, `agentive_sentence_share` = active agent+verb sentences ÷ total, `direct_address_rate` ("look at this / you"), `reflective_close` y/n, `visual_cue_per_n_sentences`) · STRUCT (promise stated by 1:00, answered by the end; two-column output: narration | visual) · GRADE (`promise_answered`, `abstract_noun_density` penalty, `visualizable_claims_share`).

### 7. Script order and body rules: packaging → outline → intro → body → outro; value loop; "second-best point first" (Kallaway)
- **Says:** write in that order. Before drafting, check the outline for novelty ("if I don't have unique points in the outline I'm not moving forward"). Each point gets "context / application / framing". Put the "second best body point in that first slot", then the best. Vary sentence length (the Gary Provost passage), write "as if you're talking to one close friend", and keep hook sentences short, "staccato".
- **Proof:** as above. Treat the "second-best first" ordering as his own heuristic; he offers no data for it.
- **Where:** youtu.be/7I50PECz7SU (01:51–16:57); youtu.be/t5Z-Q1bg1tU (02:46–06:29)
- **Ready prompt:** none public (it's in his paid Sandcastles.ai).
- **Drives:** STRUCT (pipeline order: title fixed first; outline novelty gate; point ordering) · DNA (`sentence_length_mean/stdev` per section, `hook_sentence_length`, `second_person_rate`) · GRADE (`novelty_of_points` vs competitor transcripts; `sentence_length_variance` above threshold).

### 8. Puzzle list, not random list (Paddy Galloway)
- **Says:** "every video would follow a listical format, but it was like a puzzle list [...] without this other thing that we're going to talk about next, it wouldn't have made sense [...] instead of [...] random tip random tip random tip". For Mark Rober he names "problem, discovery, explanation" inside build sections, "three separate payoffs", and a "strong why".
- **Where:** Colin & Samir (youtu.be/L9CO1FcRHCM, 33:01); Paddy's Mark Rober breakdown 2021-07-05 (youtu.be/WYXEJ7rDSM0, 05:11–07:56)
- **Drives:** DNA (`body_structure` enum: chronological / puzzle-list / sections / investigation; Jake Tran names "chronologically" and "sections on different interesting things" as his two templates) · GRADE (`sections_causally_linked`) · STRUCT.

### 9. Structure templates carry over; wording does not need to (Jake Tran, faceless documentary)
- **Says:** "I analyzed all my videos I did really well [...] they all follow relatively the same format [...] I created templates [...] almost a fill in the blank". Writers "write closer to how they write but still within my guidelines [...] and it relatively did about the same."
- **Proof:** 1.84M subs, voice-over documentary format. Income is his own claim.
- **Where:** Jack Neel podcast 2025-03-24 (youtu.be/Si5QRdfkdPg, 19:19–20:14)
- **Drives:** product thesis: clone structure, not wording. This is real-world support for our "structure, never wording" rule.

### 10. Supporting / lower priority
- **Kurzgesagt** (25.6M subs, faceless animation): expert fact-checking; "visual metaphors" planned from the script. → GRADE `fact_check_gate`, DNA `visual_metaphor_density`. (youtu.be/uFk0mgljtns)
- **Veritasium "Clickbait is Unreasonably Effective"**: "legitbait" vs "clicktrap"; "the more clickable titles and thumbnails often better represent the content." → GRADE title/hook honesty check. (youtu.be/S2xHZPH5Sng)
- **Dan Harmon Story Circle** (Community, Rick and Morty): 8 steps, YOU→NEED→GO→SEARCH→FIND→TAKE→RETURN→CHANGE. I found no YouTube retention proof. → optional DNA `macro_arc` for biography/company documentaries.
- **Film Booth** (374K subs): scene change at most every 3 s in the intro; don't put logo stingers or channel blurbs in the intro; vary tense and timeline. → DNA `visual_beat_interval_s` (the editing brief, not the script).
- **YouTube Creator Insider, Matt Koval (2020)**: strong hook, pace, visuals, "drama and conflict", "a big climax towards the end [...] talk about this in the beginning". → cross-check for GRADE.
- **YouTube "valued watchtime"** (Goodrow, 2021): satisfaction surveys count, not only minutes watched. → the grader should score payoff *satisfaction*, not only whether it holds attention.
- **Ali Abdaal "HIVE"**: I couldn't verify the verbatim wording (source pages blocked). Use George Blackman instead.

### Excluded / not verified
- **Jordan Welch, Mark Grabowski, Jake Paul**: in this pass I found no primary, verifiable scripting framework from them with results I could check, so none is included. Kallaway's and Paddy's frameworks cover the same ground with better evidence.
- **Kallaway / Paddy / MrBeast "prompts"** on prompt-marketplace sites are third-party imitations, not the creators' own.

## Proposed style-DNA fields (each one sourced)
| Field | Source |
|---|---|
| `intro_type`, `seconds_to_click_confirmation`, `intro_word_count` | Paddy, Colin & Samir, YouTube Help |
| `hook_pattern` (context-lean / but-interjection / snapback) | Kallaway |
| `misconception_sections_share` | Muller |
| `but_therefore_ratio`, `conflict_beats_per_minute` | Parker/Stone, Kallaway |
| `open_loops_per_minute`, `avg_loop_span_s`, `max_gap_between_payoffs_s` | Blackman, Paddy, Tran |
| `reengagement_timestamps`, `where_exposition_lives` | MrBeast |
| `body_structure` enum, `section_count`, `section_transition_style` (bridge vs signpost) | Paddy, Tran |
| `opening_type` (cold-open action / question stack / statement+intrigue) | Harris, Paddy |
| `agentive_sentence_share`, `direct_address_rate`, `sentence_length_mean/stdev`, `hook_sentence_length` | Harris (Pinker), Kallaway (Provost) |
| `reflective_close`, `ending_abruptness_s` (time from final payoff to end) | Harris, MrBeast |
| `visual_metaphor_density`, `visual_cue_per_n_sentences` | Kurzgesagt, Harris |

## Proposed grader rubric (each line has a named source)
1. Click confirmation within 10 s, plus a specific intrigue line within 30 s (Paddy / Colin & Samir / YouTube Help "Intro").
2. BUT/THEREFORE share of beat links (Parker & Stone).
3. No stretch longer than 60–90 s without a payoff; every opened loop is closed; setup comes before payoff (Blackman / Paddy / Tran).
4. Re-engagements at about 3:00 and 6:00; nothing signals the end early; the ending is short after the final payoff (MrBeast).
5. Misconception stated before each major answer; hook has a contrast turn (Muller / Kallaway).
6. The promise is stated by 1:00 and answered by the end; mostly active "who did what to whom" prose (Harris).
7. Sections are causally linked ("puzzle list"), transitions are bridges, not signposts (Paddy).
8. Policy/originality gate (YouTube YPP, below): distinct storyline/focus vs the competitor's videos AND vs our previous scripts; original perspective present; no shock-only beats; facts sourced (Kurzgesagt/Harris fact-check norm).

## Official YouTube policy (the wording that constrains a style cloner)
Source: YouTube channel monetization policies, https://support.google.com/youtube/answer/1311392 (fetched 2026-09-18). Full verbatim text is in `prompts/creator-youtube-official.md`.

- **July 15, 2025 changelog (verbatim):** "We're making a minor update to our "repetitious content" policy to better clarify this includes content that is repetitive or mass-produced. We are also renaming this policy from "repetitious content" to "inauthentic content." This type of content has always been ineligible for monetization under our existing policies, where creators are rewarded for original and authentic content. There is no change to our reused content policy which reviews content like commentary, clips, compilations, and reaction videos."
- **Rene Ritchie (YouTube Head of Editorial & Creator Liaison)**, via TechCrunch 2025-07-09: "a minor update to YouTube's longstanding YPP policies to help better identify when content is mass-produced or repetitive."
- **About July 2026 restructure** (Tubefilter 2026-07-13, described as a clarification): "inauthentic content" is now split into **Generic or Repetitive Content**, **Unsatisfying or Off-putting Content** and **AI Personas Related to Sensitive Topics**.
- **Key current lines for us (verbatim):**
  - "Not be mass-produced, generic, repetitive, or manipulative. It should be made for the enjoyment or education of viewers, rather than for the sole purpose of getting views."
  - "Generic or repetitive content includes content that looks like it's made with a template, or that may feel repetitive to viewers after watching several videos in a row from the same channel."
  - "What's important is that the substance of each video should be materially varied and deliver creative, educational, or other value."
  - Not allowed: "AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"
  - "Unsatisfying or off-putting content refers to content that relies heavily on emotionally manipulative formulas, **mimics existing formats or stories to a degree that the videos feel interchangeable**, or appears designed to shock or surprise viewers for the sole purpose of getting views."
  - "If you use automated tools or templates to help create your content, the final product must still demonstrate your creative vision and provide educational or entertainment value."
  - Allowed: "Content that utilizes creative tools to assist in delivering a unique, well-researched, or creative narrative, like using AI to edit your video scripts [...]"
  - Not allowed: "Content that lacks a clear narrative arc or logical progression"
  - Not allowed: "Content that exclusively features readings of other materials you did not originally create, like text from websites or news feeds" (reused content)
  - AI personas: channels "that use AI-generated personas to deliver information on sensitive topics [...] health, legal issues, finances, or politics" cannot monetize.

**What this means for design:** the policy explicitly permits the same intro/outro and a similar pattern, provided "each video has a distinct storyline, focus, or concept". It explicitly penalises videos that mimic formats "to a degree that the videos feel interchangeable". So the style DNA must hold *structural statistics* (rhythm, loop density, beat map), never reusable phrases or story templates with the nouns swapped. The grader needs an "interchangeability" check: an embedding/LLM comparison of the new script's storyline and angle against the competitor transcripts and against our own previous outputs. It also needs a "narrative arc present" check and a "sourced facts, original perspective" check. Voice-over channels on health, legal, finance or politics must not present an AI persona as a human expert.
