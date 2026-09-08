# Claims safety, render strategy, and review

## Claims gate

Every brand profile (`brands/<brand>/profile.json`, `brands/<brand>/claims.json`) separates:

1. **Immutable identity facts** — legal name, founders, exact product identity. Never paraphrased away.
2. **Approved factual and sensory phrases** — safe to use as-is, each carrying a fact id back to a source.
3. **Review-required patterns** — plausible but not pre-cleared; a human must sign off per use.
4. **Blocked patterns and topics** — never usable in generated copy or prompts, regardless of phrasing.

Two independent checks apply before any generation prompt is finalized, and neither is sufficient alone:

- **Deterministic gate:** exact blocked-term/pattern matching, and a hard requirement that every factual line in a prompt carries a fact id present in the profile.
- **Semantic review:** paraphrase- and context-aware checking for meanings that evade exact-match blocking (e.g. "keeps bites away" implying a pesticide claim without the word "pesticide").

For Cinco H Ranch specifically, sunscreen, pest-control, pain-relief, disease-treatment, healing, and testimonial-style claims are blocked or review-required in the initial profile — they are regulatory/liability risks regardless of how favorably they'd read.

## Render strategy — declare which pixels may change

Every plan states exactly one strategy:

- **`reference-edit`** — the model receives the source image as a reference; likeness is experimental and every output must be reviewed before it can be treated as representing the real product. Never silently promoted to an approved product representation.
- **`exact-asset`** — the original image passes through unchanged; Blotato only adds layout, captions, or surrounding edit — the product pixels themselves are untouched.
- **`exact-overlay`** — a generated background or motion layer is combined locally, after generation, with the authoritative original product cutout. The original product asset is never itself sent through a lossy generative edit.

Cinco product labels, logos, and founder identity default to `exact-asset` or `exact-overlay`. `reference-edit` can be tested against a copy of an asset, but its output cannot become an approved brand representation without explicit review acknowledging the identity risk.

Accepting an image as a valid model input is not evidence that the model preserves it faithfully — a template accepting a reference image says nothing about whether labels, proportions, or identity survive generation.

## Review requirements before approval

An image or video cannot move to the next generation stage until a human explicitly approves it against:

- Product/label fidelity (embossing, shape, packaging, actual batch variation) for anything not using `exact-asset`/`exact-overlay`.
- Claims mapping — every visible or spoken claim traces to an approved fact id.
- Visual identity rules from the profile (palette, typography, logo use).
- For video: audio rights/sound choice, muted-clarity (the piece reads clearly with sound off), and pacing.
- Media metadata (`ffprobe` output) is sane and matches the expected format/duration.

Approval binds to the specific artifact's checksum. If the artifact changes — even a re-render with the identical prompt — it is a new checksum and needs a new approval.
