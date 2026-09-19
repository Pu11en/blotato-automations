# Jake Tran — faceless documentary operator (writers trained on templates made from his own hits)

- Source: "YouTube Expert: How I Make $250k/Month With 3 Faceless Channels", Jack Neel podcast, 2025-03-24, https://www.youtube.com/watch?v=Si5QRdfkdPg (yt-dlp transcript, 2026-09-18)
- Proof of results: Jake Tran channel has 1,840,000 subscribers (yt-dlp, 2026-09-18). It is voice-over documentary (corruption, conspiracies, business). He also runs the faceless branded channel "Evil Food Supply". The income figures are his own claims.
- Ready prompt published? No. He describes internal fill-in-the-blank templates but hasn't published them.
- Why it matters: this is a real-world precedent for our pipeline. He analysed his own top videos, pulled out a repeatable structure, and trained writers on it.

## Verbatim quotes
> [07:48] "once they actually click on your video then you have to hook them in with the first like 30 seconds 60 seconds of the video [...] the goal of that is to just uh get them as excited as possible get their emotions as high as possible so that they're actually invested to stick around to the rest of the video um so I think of it as like leaving them on an open loop"
> [08:17] "if you think about the Dark Knight movie it starts out with that famous scene of the Joker doing that bank robbery uh so it leaves you on a giant open loop where you have to watch the rest of the movie to figure out like what's actually happening"
> [09:14] "like the title thumbnail leaves you on an open loop then the hook makes you watch the next part of the video then the next part of the video make sure you watch the next part"
> [18:50] "when you write a blog to try to rank on Google you're trying to jam as many keywords in there as possible [...] whereas on YouTube um you're really trying to write more of a story uh that's like emotional and story driven"
> [19:19] "what I did was I analyzed all my videos I did really well and I realized that most of my videos uh the really successful ones they all follow relatively the same format we have a hook and then we tell the story in a certain way maybe we go through the the Nestle story chronologically or instead of that we sh we just have sections on different interesting things that Nestle has done um so so I broke down my really viral videos I created templates for it [...] almost a fill in the blank kind of thing"
> [20:14] "I was trying to get people to write like me for so long and then eventually I was like let me just try a video where they write closer to how they write but still within my guidelines [...] and it relatively did about the same"
> [33:52] "if it's an idea that has already been covered on YouTube a lot [...] I can't just make the same video so I have to find a new angle to the story"

## Pipeline takeaway
Two findings support our design. (1) Structure templates carry over to other writers, and matching exact voice/wording wasn't needed ("relatively did about the same"). (2) The two structure types he names, "chronological" and "sections on different interesting things", are a natural enum for the style-DNA field `body_structure`.
