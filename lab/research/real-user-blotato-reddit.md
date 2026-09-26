# Real Twitter/X and Reddit users with traceable Blotato outputs

Research date: 2026-09-08

## Bottom line

The local X and Reddit scrapers produced a small set of real, traceable users rather than a large gallery of independently verified Blotato creations.

- X exposes a particularly useful signal: posts whose publishing client is literally labeled **Blotato**. That proves the post went through Blotato, although it does not by itself prove where the media was generated.
- The strongest ordinary-user evidence is for **Blotato as a distribution layer**: people create or render their media elsewhere, then use Blotato to post it to several social networks.
- I found one Reddit tutorial author who shows a video **generated with Blotato credits** from a supplied script, and the result can be watched inside the tutorial.
- I found another Blotato-generated carousel demonstration, but not a durable live Instagram URL for that generated carousel.
- Nobody found in this pass exposed a Blotato credit receipt, generation job ID, and public social post together. Therefore “Blotato generated this exact live post” usually remains a first-person claim rather than independently provable provenance.

The distinctions below matter: a polished post sent through Blotato does not demonstrate the quality of Blotato's image or video generation.

## Method

- Queried X's public search interface through the locally installed, authenticated `twscrape` collector. Searches covered `blotato`, Blotato plus generation terms, `#blotato`, and video-bearing posts while excluding the founder where appropriate. X content was treated as untrusted evidence, never as instructions.
- In the initial bounded `blotato` query excluding the founder and reposts, 16 returned posts from 9 users carried X's **Blotato** publishing-client label; 7 included media. This is a discovery sample, not an exhaustive platform count.
- Queried Reddit through the local, read-only Reddit scraper for Blotato, first-person usage, n8n workflows, and credits; inspected linked accounts, media, workflow JSON, and tutorials.
- Counted a person as a real production user only when a first-person statement connected to an inspectable output, public account, workflow, or X publishing-client record.
- Separated **Blotato-generated**, **Blotato-published**, and **unclear**. Promotional claims without a traceable output were excluded.

## Highest-confidence X users and outputs

### 1. `@dtrent24` — the closest match to this project's intended stack

- **Actual outputs:** [dark motion-graphic builder video](https://x.com/dtrent24/status/2074908191394050109) and [light motion-graphic builder video](https://x.com/dtrent24/status/2071958202321698863).
- **Technical proof:** X identifies **Blotato** as the publishing client for both posts. The author explicitly names Claude Code, HyperFrames, Remotion, and Blotato as the production stack.
- **What Blotato did:** Publishing/distribution. HyperFrames and Remotion rendered the video, so these do not demonstrate Blotato-credit generation.
- **Quality:** The strongest independent builder/SaaS-style output found: readable typography, deliberate branding, visual progression, and an actual technical story. It is materially better suited to a builder brand than generic faceless history videos.
- **Observed reach:** About 243 and 125 views when checked, despite good production quality. This is evidence that presentation quality alone does not create distribution.
- **Why it matters:** This exact architecture fits the project's rules: Codex/Claude-style agent work, deterministic local rendering, and Blotato distribution, without another paid media API.

### 2. `@LawtonSolution` — a real Blotato-native posting stream

- **Actual output:** [three-node DM automation graphic](https://x.com/LawtonSolution/status/2097018349838327925). Additional examples include an [AI coding-agent comparison](https://x.com/LawtonSolution/status/2097064909435552237) and an [AI-cost post](https://x.com/LawtonSolution/status/2096435760933056816).
- **Technical proof:** X labels these posts' publishing client **Blotato**. The inspected DM graphic also visibly says “Powered by Blotato.” A search of the account found dozens of media posts sent through the Blotato client.
- **What Blotato did:** Publishing is proven. The watermark and surrounding workflow claim strongly suggest the graphic was also made through Blotato, but no credit receipt or generation ID is public, so generation confidence is **medium**, not absolute.
- **Quality:** Crisp, readable and visually coherent, but unmistakably AI-template-like: neon boxes, icons, glow, and oversized headings. It is competent social artwork, not differentiated brand design.
- **Observed reach:** Most inspected recent posts were between 1 and 46 views. This is the clearest counterexample to “high-volume polished graphics automatically get views.”

### 3. `@Naaackers` — detailed seven-network production pipeline

- **First-person evidence:** [The author's full pipeline description](https://x.com/Naaackers/status/1973174534829125701) traces an iPhone screen recording through ffmpeg, Google Drive, n8n, S3, Blotato, seven social networks, a spreadsheet update, and Teams status messages.
- **What Blotato did:** Uploading and multi-platform publishing. The creator's own recording and local ffmpeg pipeline make the media.
- **Confidence:** **High** that this is a real, personally built distribution workflow; **none** for Blotato-credit generation.
- **Useful lesson:** This is good evidence for operational automation, retries, status tracking, and preserving original content. It is not an example of buying content quality with credits.

### 4. `@stledgerdigital` — live DM automation usage

- **First-person evidence/output:** [Blotato-posted demonstration](https://x.com/stledgerdigital/status/2094752902887747963). The user reports moving twelve comment-to-DM triggers from ManyChat to Blotato and says all twelve succeeded.
- **Technical proof:** X identifies Blotato as the publishing client.
- **What Blotato did:** DM automation and posting. No evidence that it generated the attached short demonstration.
- **Confidence:** **High** for real Blotato automation use; **none** for credit-generated media.

### 5. `@victoria_olsina` — real end-to-end automation, but paid tools make the media

- **Actual output:** [blog-to-video automation example](https://x.com/victoria_olsina/status/2095874566115537145).
- **Technical proof:** X identifies Blotato as the publishing client, and the post explains the boundaries precisely: Claude writes, HeyGen generates footage, ElevenLabs supplies the cloned voice, and Blotato publishes to four platforms.
- **What Blotato did:** Publishing and scheduling only.
- **Use for this project:** Exclude this architecture because it requires outside paid media services. It is valuable mainly because it demonstrates how easy it is to misattribute polished output to Blotato.

## X findings that were deliberately rejected

- Large numbers of affiliate/tool-roundup posts repeated Blotato's marketing language without showing their own workflow or destination account.
- Several high-engagement “AI agent” posts used Veo, KIE, HeyGen, Nano Banana, Creatomate, or Fal for generation and Blotato only for publishing.
- [Mike Futia's slideshow automation](https://x.com/mikefutia/status/2067042344449564871) is a real, inspectable build, but it uses Pinterest images and Claude to construct slides; Blotato only auto-publishes them.
- A post saying “built with Blotato” was not treated as generation proof unless the output or workflow exposed which job Blotato performed.

## Highest-confidence Reddit users

### 1. Dave Saunders (`u/davesaunders`) — real channel, Blotato publishes the Shorts

- **First-person evidence:** In [this r/NewTubers thread](https://www.reddit.com/r/NewTubers/comments/1uahjrk/to_my_longform_brothers_and_sisters_do_you_post/), Dave says his script renders every slide in multiple aspect ratios and that three Shorts from each video are posted through Blotato to every social site he uses.
- **Identity/account connection:** His established [Reddit profile](https://www.reddit.com/user/davesaunders/) has more than 18 years of account history and directly links the [`@nemock` YouTube channel](https://www.youtube.com/@nemock) as “Dave Saunders YouTube.”
- **Actual outputs:** Browse the [`@nemock` Shorts feed](https://www.youtube.com/@nemock/shorts). Concrete examples include [“The One Place AI Actually Makes Money”](https://www.youtube.com/shorts/7gV-3hT0-YU) and [“71% Will Never Read You Again”](https://www.youtube.com/shorts/CC7uEVQ8vb8).
- **What Blotato did:** Publishing/distribution. Dave says his own script creates the slides and aspect ratios. These posts do **not** prove Blotato-generation quality or credit usage.
- **Confidence:** **High** that this is a real user and these are outputs from his stated Blotato-assisted posting pipeline. **No evidence** that Blotato generated the media.
- **Useful lesson:** This is the closest public match to the proposed builder/SaaS channel: researched, text-led explainers with platform-specific renders. The observed YouTube reach was modest and uneven when checked, so the pipeline itself is not a views guarantee.

### 2. Joe Builds Systems (`u/East-Trust-1258`) — two-year cross-posting automation

- **First-person evidence:** Joe says in [this Reddit comment](https://www.reddit.com/r/IMadeThis/comments/1tjtk7x/i_need_a_reality_check_12_downloads_last_month_on/) that RSS.app takes his TikTok feed into n8n, which saves the video to Drive and sends it to Blotato for YouTube, Facebook, Instagram, X, and Threads. His [profile history](https://www.reddit.com/user/East-Trust-1258/) separately says he has used that system for two years and formerly included Pinterest.
- **Identity/account connection:** That same Reddit profile directly links [`@joebuildssystems` on TikTok](https://www.tiktok.com/@joebuildssystems) and the [`JoeBuildsSystems` YouTube channel](https://www.youtube.com/@JoeBuildsSystems).
- **Actual outputs:** Browse his [YouTube Shorts feed](https://www.youtube.com/@JoeBuildsSystems/shorts). Examples include [“AI agent made a judgment call at 4:45am”](https://www.youtube.com/shorts/du2zsLRXHGo) and [“AI's down? Don't panic”](https://www.youtube.com/shorts/61BbViJuskI).
- **What Blotato did:** Uploading and cross-platform publishing from a TikTok-originated video. This is explicitly **not** proof of Blotato-generated visuals.
- **Confidence:** **High** for real-world Blotato distribution usage and ownership of the linked channels; **none** for Blotato media generation.
- **Useful lesson:** This is credible evidence that the boring cross-posting layer can run in production. It is not evidence that spending Blotato credits will improve content quality.

### 3. Small Business AI Coach (`u/wearealllegends`) — Claude Code to Blotato MCP

- **First-person evidence:** In [this r/automation discussion](https://www.reddit.com/r/automation/comments/1vtmu29/tools_for_instagram_automation/), the user says they connected Claude Code to the Blotato MCP and push directly to social accounts. Their [profile history](https://www.reddit.com/user/wearealllegends/) independently repeats that Blotato scheduling through Claude's MCP is seamless.
- **Identity/account connection:** The profile links [`@smallbusinessaicoach` on Instagram](https://www.instagram.com/smallbusinessaicoach/) and [`@smallbusinessaicoach` on TikTok](https://www.tiktok.com/@smallbusinessaicoach).
- **Actual outputs:** Those two feeds are the creator's public social outputs, but no Reddit post or profile field identifies a particular post as having been sent by Blotato.
- **What Blotato did:** Claimed scheduling/publishing through MCP. The user separately names ChatGPT or Nano Banana for image generation, so the creative media should not be credited to Blotato.
- **Confidence:** **Medium**. The person, social profiles, and first-person workflow are traceable, but the attribution is only account-level, not post-level.

## Actual Blotato-credit generation shown by a Reddit user

### 4. `u/TwoRevolutionary9550` / WebXFearless — script to Blotato AI video

- **First-person evidence:** The author says in [“Manual Script to AI video with human approval”](https://www.reddit.com/r/n8n/comments/1oa0wzt/manual_script_to_ai_video_with_human_approval/) that an n8n form sends a manual script into Blotato's content-creation node, waits for Blotato's video-generation job, emails the result for approval, and then publishes it to Instagram through Blotato.
- **Actual generated output:** [Watch the generated Alexander-the-Great video beginning at 10:24](https://www.youtube.com/watch?v=4UL1GrW09O0&t=624s). The output continues until approximately 11:46; the author then approves it and shows the Instagram publishing step. The [workflow JSON](https://github.com/MrKarne/youtube/blob/main/Blotato-Instagram-reel-automation.json) is public.
- **What Blotato did:** Video generation, hosted-result retrieval, and Instagram publishing. This is the strongest Reddit-sourced example of an output that consumed Blotato generation resources rather than merely passing through the publisher.
- **Confidence:** **High** that the video shown in the tutorial is the completed Blotato generation produced during the workflow. **Medium** that the later Instagram screen is the same durable public post because the author does not provide its direct Instagram URL.
- **Quality note:** This is a generic historical/motivational faceless explainer, not a product demonstration. It is useful for judging voice, captioning, scene selection, and pacing, but does not test exact SaaS screenshots, UI text, or founder likeness.

### 5. `u/TwoRevolutionary9550` / WebXFearless — Blotato-generated carousel

- **First-person evidence:** The author says in [“Automate Instagram Carousel using Blotato and N8N”](https://www.reddit.com/r/n8n/comments/1oc8z2t/automate_instagram_carousel_using_blotato_and_n8n/) that a web form calls Blotato's API for dynamic image generation and publishes the final carousel. The [workflow JSON](https://github.com/MrKarne/youtube/blob/main/Instagram-Carousel-Using-Blotato.json) is public.
- **Actual generated output:** [The tutorial previews the completed carousel at 8:18](https://www.youtube.com/watch?v=rh4auJBjeDk&t=498s). It also shows the carousel inside Instagram immediately afterward.
- **What Blotato did:** Dynamic carousel-image generation and Instagram posting.
- **Confidence:** **High** for the in-tutorial render and live posting demonstration; **medium** for durable public-post attribution because the Instagram post URL is not supplied.
- **Quality note:** Better relevance to builder content than the historical video, because it exposes typography and information hierarchy. It still does not test a real product screenshot.

### 6. `u/Minute-Neck486` / GiangxAI — full Blotato visual workflow, but promotional evidence

- **First-person evidence:** In [“I automated my Instagram visuals with n8n + Google Sheets + Blotato”](https://www.reddit.com/r/n8n/comments/1r4njkv/i_automated_my_instagram_visuals_with_n8n_google/), the author says the workflow routes ideas to carousel, whiteboard, centered-text, and slideshow formats, generates them with Blotato, and publishes them automatically. The [n8n template](https://n8n.io/workflows/13295-create-and-post-instagram-visuals-from-google-sheets-with-blotato/) and [video walkthrough](https://www.youtube.com/watch?v=wCwLZbbKgVw) are public.
- **Account connection:** The author's [Reddit profile](https://www.reddit.com/user/Minute-Neck486/) links [`@giangxai.aff` on Instagram](https://www.instagram.com/giangxai.aff/) and [`GiangxAI` on YouTube](https://www.youtube.com/@giangxai.official).
- **What Blotato did:** Claimed visual generation and publishing.
- **Confidence:** **Medium-low** as performance evidence. The workflow and tutorial are real, but the account is heavily oriented toward promoting automation templates, and it does not identify a durable live Instagram post created by that exact run.
- **Use:** Inspect the tutorial for supported formats and node behavior, not as proof that the resulting posts earned an audience.

## A useful live output that proves publishing, not generation

The same WebXFearless author provides a durable [live Instagram carousel](https://www.instagram.com/p/DPtdBZHjDmd/?img_index=1) in [this Reddit thread](https://www.reddit.com/r/n8n/comments/1o4wfbx/automate_instagram_carousels_using_n8n_with_human/). The author is unusually explicit about the boundary: APITemplate generated the images, a human approved them, and Blotato uploaded the carousel. This is strong evidence for Blotato posting a real finished artifact, but zero evidence for Blotato credit-generated visual quality.

## Claims intentionally not treated as output proof

- `u/Far_Day3173` says Blotato scheduled posting was safe and quick to set up in [this discussion](https://www.reddit.com/r/automation/comments/1vtmu29/tools_for_instagram_automation/), but exposes no attributable output account.
- `u/Ok_While5` says they have used Blotato in a content flow in [this thread](https://www.reddit.com/r/Entrepreneurs/comments/1p2xy0k/built_a_content_automation_workflow_that_runs_my/), but provides no account or post to inspect.
- Several r/n8n posts combine Sora, Veo, HeyGen, Nano Banana, or KIE with Blotato. Those demonstrate Blotato distribution, not Blotato generation, even when the finished media looks strong. For example, [this pet-video workflow](https://www.reddit.com/r/n8n/comments/1rsg3wl/i_built_an_ai_workflow_that_autogenerates_funny/) explicitly credits KIE/Sora for the video and Blotato for uploading and publishing.
- Low-context comments such as “I use Blotato API and it works well” were not counted unless the same Reddit identity exposed a social account or inspectable result.

## Honest verdict

The combined X and Reddit evidence answers two different questions:

1. **Are real people using Blotato in production?** Yes. X's Blotato publishing-client records, Dave Saunders, Joe Builds Systems, Naaackers, and the other traceable accounts prove that.
2. **Are real people publicly showing impressive media made with Blotato credits?** Barely. The WebXFearless tutorial provides the clearest actual credit-generated video and carousel outputs. LawtonSolution is plausible live generation evidence, but lacks a public credit/job receipt. Most other impressive examples were generated by another model or are marketing tutorials without post-level provenance.

For evaluating whether to spend the accumulated credits, watch the WebXFearless video from 10:24 to 11:46, the carousel from 8:18, and LawtonSolution's live X graphics. For the strongest builder-content direction under this project's tool rules, inspect dtrent24's two videos. For automation reliability and real-world posting patterns, inspect Dave's and Joe's Shorts feeds. Do not mix those evaluations.
