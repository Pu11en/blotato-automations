# Kurzgesagt – In a Nutshell — production/scripting process

- Source: "How to Make a Kurzgesagt Video in 1200 Hours", 2020-02-16, 9.04M views, https://www.youtube.com/watch?v=uFk0mgljtns (official captions via yt-dlp, 2026-09-18). Related: "Can You Trust Kurzgesagt Videos?", https://www.youtube.com/watch?v=JtUAAXe_0VI (not transcribed here).
- Proof of results: 25,600,000 subscribers (yt-dlp, 2026-09-18). An animated, faceless, narrator-led format, the closest match here to our target channels.
- Ready prompt published? No. They describe a process, not a retention formula.

## Verbatim quotes
> [00:35] "We want to explain complicated things in an easily graspable way and make science-y topics fascinating and beautiful. But we also want to tell stories and express how we feel about the universe from time to time."
> [00:35] "Our research begins by reading books or scientific papers and by talking to different experts who point us in the right direction. We want to have a fact-based worldview and our videos are trying to reflect that."
> [01:10] "A script begins with a rough first draft that's then rewritten and edited over and over again. To make sure we don't misrepresent something, We asked experts to fact-check and correct us. Writing is the bottleneck for our videos, and very hard to speed up."
> [01:42] "When the script is ready, we begin sketching out the video. We try to think of visual metaphors, transitions between ideas, and decide which scenes need the most attention. [...] The general idea is to find the right images to the words in the script to explain as clearly as possible, while also having interesting things to look at."

## Pipeline takeaway
Kurzgesagt gives no retention formula. It contributes two things: (1) the script is written before the visuals, and every idea needs a "visual metaphor", so style DNA should record `visual_metaphor_density` and the grader should check that each claim can be pictured; (2) expert fact-checking, so the grader needs a factual-accuracy/citation gate. Harris and Veritasium also publish sources.
