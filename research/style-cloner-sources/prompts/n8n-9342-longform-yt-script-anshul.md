# n8n 9342 — Generate YouTube scripts for shorts & long-form with Gemini AI and Tavily Research

- Template URL: https://n8n.io/workflows/9342
- Author: Anshul Chauhan (@anshulchauhan) — verified creator
- Date created: 2025-10-07
- Views (n8n API totalViews, fetched 2026-09-18): 2938
- Step order (topological, from workflow JSON): On form submission -> Google Gemini Chat Model -> Google Gemini Chat Model1 -> If -> Tavily -> Tavily1 -> Websearch -> WebSearch Summary -> Reference Script -> Create Outline -> AI Agent -> Reference Script1 -> Create Doc -> AI Agent1 -> Update Doc -> Create Doc1 -> Update Doc1
- Notes: Only template found that writes a 2,500-3,000 word long-form YouTube script from a pasted style reference. Research via Tavily (paid API, has free tier). LLM = Google Gemini chat model nodes.

Prompts below are copied VERBATIM from the workflow JSON (n8n expression syntax `{{ }}` left as-is; a leading `=` marks an n8n expression field).


## Node: "Websearch"
- Node type: `@n8n/n8n-nodes-langchain.googleGemini`
- LLM: models/gemini-2.5-flash

### Field `.messages.values[0].content`

````text
=You are a research assistant. Your task is to extract information from these websites scraped content for the given title {{ $('On form submission').item.json['Provide topic'] }}, analyze the information, and prepare a summarized content.
Rules:
- Ensure the summary is based solely on the given title.
- Generate a single, cohesive summary from the extracted information.
- If the topic is a listicle, remove duplicate items/products and compile a summary with the remaining unique products.
- If the information includes different methods across websites, select the best method and create a concise summary based on it.
````


## Node: "WebSearch Summary"
- Node type: `@n8n/n8n-nodes-langchain.googleGemini`
- LLM: models/gemini-2.5-flash

### Field `.messages.values[0].content`

````text
=You are a research assistant and YouTube script researcher.

## INPUTS
• Topic / Video Title  → {{ $('Tavily1').item.json.query }}
• Scraped source texts  → {{ JSON.stringify($node["Tavily1"].json.results) }}   ← n8n expression; leave unchanged.

## TASK
1. Read every source in **scraped source texts**.  
2. Extract the most relevant points that match the exact topic above—ignore off‑topic info.  
3. Create a **detailed research summary** (≈ 1000 words) in *plain English*.

## LANGUAGE & TONE
• Aim for a 6th‑to‑8th‑grade reading level.  
• Short sentences (≤ 18 words).  
• Prefer common words (“use” > “utilize”).  
• No jargon unless you explain it in one simple sentence.  
• Do **not** mention any host or channel name.

## STRUCTURE
Return plain text with one blank line between sections:

**Intro (≤ 30 words)** – a catchy hook that frames why the viewer should care.

**Main Summary** – depends on the topic type  
◦ **If the topic is a *listicle*** →  
   – Remove duplicate items across sources.  
   – For each unique item, write:  
     • Item #X – Name  (bold the name)  
       – Key spec / feature #1  
       – Key spec / feature #2  
       – One real‑world benefit or use case (1 sentence)  

◦ **If the topic is a *how‑to* guide** →  
   – Compare all methods across sites, pick the best approach.  
   – Present clear **Step #1, Step #2 …** instructions, adding 1‑sentence tips where helpful.  

◦ **If the topic is *experimental* (comparison, challenge, versus, etc.)** →  
   – Summarise the experiment setup in 2‑3 sentences.  
   – List the contenders / variables.  
   – Highlight the most surprising finding and why it matters.  

**Mini‑Conclusion (2 sentences)** – wrap up value and tease that the full script will dive deeper.

## OUTPUT RULES
• Plain text only—no Markdown fences, no JSON.  
• At least **1000 words**.  
• Each bullet line starts with “– ” (en dash + space).  
• One blank line between Intro, Main Summary, and Mini‑Conclusion.

````


## Node: "Create Outline"
- Node type: `@n8n/n8n-nodes-langchain.chainLlm`
- LLM: (default) via lmChatGoogleGemini node 'Google Gemini Chat Model1'

### Field `.text`

````text
=Summary: {{ $json.message.content }}

Now based on this summary, try to create a youtube video outline for the topic "{{ $('Tavily1').item.json.query }}". With proper headings (include sub headings under each main heading). Each item in the outline needs to be an important and essential and crucial information that is needed to solve the user's intent. Do not include any fluff or nice to have content. Focus on the must haves.
Avoid the words "section 1, 2, etc " in the outline. Just stick to the actual headings.
````


## Node: "AI Agent"
- Node type: `@n8n/n8n-nodes-langchain.agent`
- LLM: (default) via lmChatGoogleGemini node 'Google Gemini Chat Model'

### Field `.text`

````text
=Here is the video title: {{ $('On form submission').item.json['Provide topic'] }}

Here is the summary: {{ $('Websearch').item.json.message.content }}
````

### Field `.options.systemMessage`

````text
=You are a senior YouTube short script writer. you have to create a complete youtube short video script with the provided summary which is collected from top google results for the given title.
---

✦  OUTPUT FORMAT  ✦

• Return the entire script as plain text exactly like this example

• Style Reference (tone, pacing, formatting):
{{ $json.short_style_ref }}

use it for a reference script

(Keep one blank line between every sentence or logical beat, no markdown, no JSON.)

````


## Node: "AI Agent1"
- Node type: `@n8n/n8n-nodes-langchain.agent`
- LLM: (default) via lmChatGoogleGemini node 'Google Gemini Chat Model1'

### Field `.text`

````text
=### CONTEXT
• Video Title: {{ $('Tavily1').item.json.query }}
• Style Reference (tone, pacing, formatting): 
{{ $json.style_ref }}

• Outline with sub‑points (exact order to follow):
{{ $('Create Outline').item.json.text }}

• Requested Video Type: {{ $('On form submission').item.json['Choose video type'] }}

### TASK
Write a YouTube script **2 500 – 3 000 words** long that:

1. **Matches the requested video type automatically**
   • If `videoType` = “listicle” → produce a numbered list style (Tool #1, Tool #2 …) with snappy transitions.  
   • If `videoType` = “experimental” → use a story‑driven, curiosity‑building narrative (e.g., “We pitted four tools head‑to‑head—here’s what happened…”).  
   • If `videoType` = “how‑to” → write step‑by‑step instructions with clear sub‑steps and demonstration cues (screen actions, clicks, etc.).

2. Intro (≤ 30 words)
   • Capture attention immediately.
   • Do **NOT** mention any host or channel name—keep it neutral.

3. **Body**
   • Follow the outline’s order exactly.
   • For each tool/section:
     – Start with a heading in the form **“Tool #X – <Name>”** (or “Step #X” for how‑to videos).  
     – Expand into 2 – 3 short paragraphs (~150 words) covering key features **plus one practical real‑world example**.  
     – End with a 1‑sentence segue that smoothly leads into the next tool/step (e.g., “Speaking of collaboration… let’s look at Notion AI.”).

4. Outro / Recap
   • Summarize main takeaways in 3‑4 sentences.
   • End with a neutral CTA: invite viewers to like, comment, and subscribe—no host or channel names.

✳️  Language rule: Write at a 6th‑to‑8th‑grade reading level.  
• Use short sentences (≤ 18 words).  
• Prefer simple, common words (say “use” instead of “utilize”).  
• No jargon unless you explain it in one plain‑English sentence.  

### OUTPUT FORMAT
Plain text, one blank line between paragraphs, no JSON fences.

````


## Node: "Reference Script"
- Node type: `n8n-nodes-base.set`
- LLM: (not set / inline in HTTP body)

### Field `.assignments.assignments[0].value`

````text
SCRIPT 1: Experimental type script

Intro:

Ever felt stuck on a task and wished someone could just guide you through it—step by step/right on your screen?
Well, guess what? There is an AI tool which can do that. Hey google! Can you see my screen
Yes i can see your screen
Can you help separate the audio from this video
Yes i can help you with that, just right click on the file,.....
Wow, that was pretty cool, right?

In this video, I’ll show you how to use this powerful tool step by step. Plus, I’ll put it to the test with real tasks—like working in Microsoft Excel, editing in Photoshop, or even help that I want with my PC.

So Stick around till the end, I’m A from my channel, and let’s get started!



Ever been stuck on a task and wished someone could just guide you through it step by step?
Well, that’s exactly what Google can do now.
It can see what’s on your screen and walk you through tasks in real time. And the best part? It’s completely free.
In this video, I’ll show you the step-by-step process of using it and test it with real tasks like Microsoft Excel, Photoshop, and even setting up a new user on a PC.
Watch this video till the end to see what it really delivers.
So this is A from my channel and let’s get started.

Version 2:
Imagine learning complex software as easily as chatting with a mentor who knows exactly what you need. Sounds unreal? Well, it’s not—because that future is here.
Google has quietly launched an AI tool that’s changing the game. This isn’t just another chatbot or tutorial—it’s an adaptive, intelligent assistant that slashes your learning curve and skyrockets your productivity. And the best part? It’s completely free.
In this video, we’re diving deep into Google AI Studio to show you how it’s already making an impact. We’ll walk you through how it works, what you can do with it, and how it can make learning faster and easier than ever.
Stay with me, because in the next 10 minutes, you’re about to discover a learning hack so powerful, you’ll wonder how you ever lived without it.
So this is A from my channel and let’s get started.
----------------------------------------------------------------------------------------------------------
First, let’s go to Google AI studio,
Just click the link in the description
And it’ll take you to this page
Click ‘sign in to Google Studio’ and sign in using your google account.
Now go to “stream real-time”

Here, you have three ways to interact with Google AI studio. You can talk to Google using your microphone, or show what you’re looking at through your webcam, or even share your screen so it can guide you step by step.
But before you start, remember that Google AI records your screen and microphone while you use it.  Google uses this data to train their AI model, so make sure you don’t have any confidential information on your screen.
I’m going to share my screen and see how it guides me.
You can click here and select the screen you want to share.
—--------------------------------------------------------------------------------------------------------------------
A: Hey Google, I need some help with Excel, and I just shared my screen.
Google: OK, I see. You need some help with Excel. Is there anything specific you need help with?
A: Yes! Can you see my screen right now?
Google: Yes, I can see your screen. I see a spreadsheet with sales data. What would you like to do?
A: I want to create a pivot table to analyze the sales performance of each country. Can you guide me through it step by step?
Google: Sure! First, please select all of the data in your spreadsheet, including the headers. Have you done that?
A: All right, I’ve selected all the data. What should I do next?
Google: Great! Now that you’ve selected all the data, click on the Insert tab at the top of the screen, and then select the Pivot Table option.
A: OK, done. What’s next?
Google: I see you’ve opened the Create Pivot Table window. Now, select whether you want to insert the pivot table into a new sheet or an existing sheet, 
A: Let it be in new sheet

Google: Then click Create.
A: Yes, I did that.
Google: Now, since you want to analyze sales performance by country, in the Pivot Table Editor, under Rows, click Add and choose the Country field. Then, under Values, click Add and select the Sales field.
A: OK, done.
Google: Great! You have now created a pivot table to find the sales per country. Is there anything else I can help you with?
Wow, that was crazy! Google just watched our screen, understood what we needed and helped us solve the problem step by step.
Here’s a quick note: Each session lasts only 10 minutes and will automatically stop. If your problem isn’t solved, don’t worry, you can just start a new session and give a quick recap of what you’ve done. Since Google doesn’t remember past chats, this helps it pick up where you left off and continue helping you.
Okay, Let’s start a new one.
Now, let's see how Google can assist with another tool. This time, I’ll ask for help with Photoshop.
So let’s go back to Google Studio.
Click here to start the session.
I’m going to share my screen again.
Hey google, I need some help with Photoshop. Can you see my screen?
Google:  
A: I want to remove this person from this picture. Can you tell me how to do that step by step?
Google: Sure! To remove the person in the background, first, select the Object Selection Tool from the toolbar on the left side of the screen. It looks like an arrow pointing to a rectangle with a dotted outline. Do you see the tool?
A: Yes. I’ve selected the “object selection tool”. Now what should I do next?
Google: Now, click on the person you want to remove.
A: OK.
Google: Once you click on the person, a selection of dotted lines will appear around them. Did that happen?
A: Yeah, I can see the dotted lines around the person.
Google: Now press the Delete key on your keyboard. Photoshop should automatically fill in the space with Content-Aware Fill.
A: Wow! The person is gone. That was super easy.
Go

[... TRUNCATED by researcher: field is 32581 chars total; remainder is example data. Full text in workflow JSON at https://n8n.io/workflows/9342 ...]
````


## Node: "Reference Script1"
- Node type: `n8n-nodes-base.set`
- LLM: (not set / inline in HTTP body)

### Field `.assignments.assignments[0].value`

````text
Intro:   AI video generation is evolving rapidly, and the competition among platforms is fiercer than ever. So, I decided to put them to the test. In this video, I’ll be using the same image and prompt to create videos with each tool, comparing their quality and performance. Along the way, I’ll showcase some practical real-world use cases, including incredible lip-syncing tools and more. Stay tuned for some jaw-dropping results! This is A from my channel and let’s get started.  Runwayml First, we have runway ml To use the tool Click the link in the description It’ll take you to this page. Now Click ‘try runway.’ And sign in using your Google account. Once you’re signed in. Here, you'll find different features available on RunwayML. Now to create your video  Click ’generate video.’ Here we have three main models: you can choose the one you want. I’m going to select “Gen 3 Alpha Turbo” since it’s the fastest. So let’s select that. Now to create your video.  You have two options from text to video and image to video. We are going to create our video using “image to video”. So We’re going to upload an image and then convert it into a video. let’s drag and drop the image  Then click “crop” to fit the image on the screen. Here, you can describe how you want your video to be This helps the AI understand what you want and give you the best results. (So I’m going to ask it to create “A cinematic wide establishing shot of a man walking through battlefield, with soldiers moving in the background.”) Once you’ve given the prompt, you can choose the video duration here, then click ‘generate.’ And your video will be generated. As you can see, the video has come out really well and the quality is also good. So to download this video Just click here and it’ll be downloaded to your computer. So now we have seen how to generate videos from Runway and what kind of video it can create. Kling AI Next, let’s move to the second tool which is Kling AI To use the tool Click the link in the description, and it’ll take you to this page, Now click “sign in for free credits”/ sign in Fill in these details and create your account. Now go to AI videos, Like the previous tool, Kling AI also has two options for creating videos — text to video and image to video. Let’s select ‘image to video.’ Now I’m going to upload the same image, Enter the same prompt  And Click ‘generate.’ Let’s see how this tool generates the video Now this process will take some time  just wait for a while And it's done The video looks pretty good, and compared to the previous tool, the quality is much better. You can also see the movements of the soldiers here. Let’s download it by clicking here. And your video will be downloaded. Luma AI Okay, let’s move on to the third tool, which is Luma AI. To use the tool Click the link in the description  And it’ll take you to this page Now click “try now.” And Sign in with your Google account. Once you’re signed in Let’s click here and upload the same image and prompt we used earlier. then click here As you can see, the video has been generated and it looks pretty decent, actually. So to download this video, just click here And it’ll be downloaded to your computer.  Alright!  Minimax AI Let’s move to the fourth tool, which is Minimax AI To use the tool Click the link in the description  And Sign in with your Google account. Then click here and upload the same image and prompt we used earlier. Now click here and your video will be ready. Well, the video looks good.  Let’s download it. Okay  Now that we've generated the videos using all four tools, let’s compare the results. Comparison of results:  Runway did a great job with good video quality, following the prompt of the man walking in a Warfield, but the soldiers in the background aren’t moving. Kling AI is more realistic than RunwayML. You can see the soldiers walking, though the video angle could be better. Overall, it’s great. Luma AI didn’t get it right, actually. The characters at the back don’t look real and the video quality is also poor. Finally, Minimax AI is almost perfect. The visuals are realistic, and the movements are smooth.   According to me When it comes to quality and relevance to the prompt, Kling AI and minimax are equally good and stand out as the best. Example 2: Next, let’s look at a few more examples and see how these tools perform in different scenarios. I have uploaded an image of a girl and asked these tools to create a video of a model filming a commercial with a beautiful smile and flowing hair. Let’s see the results.  Actually, Kling AI just nailed it here. It captures the smile perfectly, and the video quality is great. RunwayML’s video is also pretty good, but the smile is lacking. Also the hair movement feels a bit stiff compared to Kling AI. Luma AI’s video looks okay. The video has some movements, but the model’s face and lips look unnatural.  Minimax’s output looks great, and it follows the prompts accurately. Again, Kling AI and Minimax did well here… Example 3: Alright, we’ll see one more example This time, I’ve uploaded an image of a man running on the seashore and asked the tools to make a video with details like waves touching his feet and water splashing around him. So let’s see the results. The video which Runway generated turned out pretty good, but the detailing could’ve been better. You can see the waves aren’t touching his feet, and his legs also have some disturbance. KlingAI did an awesome job. You can see the water splashing as he runs, and the details on the sand are also very good. Minimax’s video quality is great. Although it doesn't fully follow the prompt, the video still turned out really well. Luma AI also did a great job with the video, but the quality is quite low. Okay, now that we’ve compared the top 4 tools. So when it comes to the overall ranking, I would say KlingAI is first, minimax second, then RunwayML and Luma AI…  Now these AI tools are not just for creating fun videos, You can also use it

[... TRUNCATED by researcher: field is 32546 chars total; remainder is example data. Full text in workflow JSON at https://n8n.io/workflows/9342 ...]
````
