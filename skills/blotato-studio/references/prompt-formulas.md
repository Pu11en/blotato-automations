# Prompt formulas

## Product-in-scene formula (source: `amazon-product-studio`)

From [SamurAIGPT/amazon-product-studio](https://github.com/SamurAIGPT/amazon-product-studio) (MIT, verified not a fork, 12 stars but actively maintained, checked via GitHub API 2026-09-09), `src/app/page.js`'s `PRESETS` array. Every one of its 7 presets follows the same sentence structure:

> "A professional product photograph of the product **[placement/surface]**, **[background/setting]**, **[lighting]**, **[mood/style descriptors]**, **[genre tag]**."

Real examples quoted from that file:

- *"...sitting on a clean minimalist white marble block pedestal, soft shadows, warm natural studio light, blurred plants in the background, commercial advertisement style."*
- *"...sitting on a rustic warm wood table, cozy sunny kitchen background, blurred sunlight through a window, green leaves, natural homeware lifestyle style."*
- *"...resting on golden sea sand, beach seashore background, warm sunny afternoon light, blurry turquoise tropical ocean waves, summer commercial vibe."*

Use this as a starting template when writing `sceneDescription` for `product-scene-placement` or similar techniques:

```
A professional product photograph of the product {placement}, {background}, {lighting}, {mood}, {style_tag}.
```

**Known limitation (not the formula's fault):** even with a disciplined prompt like this, Blotato's live `product-scene-placement` template was found on 2026-09-08 to shift the product's color/edges versus the real source photo — see that catalog entry's `known_issues`. A good prompt formula does not guarantee identity preservation; that's a property of the underlying model, which this repo doesn't control. Always route output through human review before calling it an approved brand asset.

## Caption/on-screen-text formula (source: this repo's own live research)

For any technique whose output will be watched muted (Pinterest research in `brands/cinco-h-ranch/pinterest-research/` found ~85% of Pinterest viewers watch without sound): keep captions short (one sentence, under ~12 words per screen), high-contrast against a solid band (not directly over busy photo detail), and never depend on audio to carry the core message.
