"""Blotato's text-to-infographic family: one contract, several styles.

Every template here takes exactly two text inputs -- a `description`
(10-500 chars) and a `footerText` CTA (2-100 chars) -- and returns a single
generated image. No reference media, so nothing gets uploaded and there is
no asset checksum to drift.

They share one file because only the template id and the label differ; the
registry accepts `ENTRIES` for exactly this case. Bounds are copied from the
live template listing (`blotato inspect`), not guessed.

**Only styles we have actually run and looked at are listed.** Blotato
exposes 20 of these; the other 15 are structurally identical but nobody has
seen what they render, so they are not in the catalog. To add one: get its
id from `blotato inspect`, add it to STYLES, run it once, then record the
date in VERIFIED and anything the output revealed in ISSUES.
"""
from ..types import GenerationPlane, ModelEntry, SettingField

DESCRIPTION_MIN, DESCRIPTION_MAX = 10, 500
FOOTER_MIN, FOOTER_MAX = 2, 100
DEFAULT_FOOTER = "Follow for more"

# style slug -> (Blotato label, Blotato template id)
STYLES = {
    "breaking-news": ("Breaking News", "8800be71-52df-4ac7-ac94-df9d8a494d0f"),
    "newspaper": ("Newspaper Infographic", "07a5b5c5-387c-49e3-86b1-de822cd2dfc7"),
    "whiteboard": ("Whiteboard Infographic", "ae868019-820d-434c-8fe1-74c9da99129a"),
}

# style slug -> date we actually submitted it live and looked at the output.
VERIFIED = {
    "newspaper": "2026-09-26",
    "whiteboard": "2026-09-26",
    "breaking-news": "2026-09-26",
}

# Each of these cost exactly 50 credits on 2026-09-26.
OBSERVED_CREDITS = 50

# style slug -> what a live run actually showed, when it was not clean.
ISSUES = {
    "newspaper": (
        "Fabricates masthead metadata: the 2026-09-26 run invented a paper name, a "
        "byline ('BY ALEX CHEN, DIGITAL OBSERVER') and a date ('OCTOBER 26, 2023') that "
        "were in no input. Do not publish as-is if a real byline or date matters.",
    ),
    "breaking-news": (
        "Invents a broadcaster and a photorealistic news anchor who does not exist, and "
        "the 2026-09-26 run rendered a QR code captioned 'Free thumbnail cheatsheet' that "
        "encodes nothing real. Strip or replace the QR code, and consider disclosure "
        "before publishing a synthetic anchor as news-styled content.",
    ),
    "whiteboard": (),
}

def build_inputs(plane: GenerationPlane) -> dict:
    return {
        "description": plane.prompt,
        "footerText": plane.settings.get("footerText", DEFAULT_FOOTER),
    }


def _entry(slug: str, label: str, template_id: str) -> ModelEntry:
    issues = ISSUES.get(slug, ())
    return ModelEntry(
        id=f"infographic-{slug}",
        blotato_template_id=template_id,
        surface="image",
        label=label,
        description=(
            f"Text-to-image infographic in the {label} style. Takes a topic "
            "description and a footer call to action; needs no reference media."
        ),
        roles={},
        settings={
            "footerText": SettingField(
                kind="text",
                default=DEFAULT_FOOTER,
                min_length=FOOTER_MIN,
                max_length=FOOTER_MAX,
            ),
        },
        build_inputs=build_inputs,
        known_issues=tuple(issues),
        broken=False,
        verified_at=VERIFIED.get(slug),
        prompt_min_length=DESCRIPTION_MIN,
        prompt_max_length=DESCRIPTION_MAX,
        observed_credits=OBSERVED_CREDITS if slug in VERIFIED else None,
    )


ENTRIES = tuple(_entry(slug, label, tid) for slug, (label, tid) in sorted(STYLES.items()))
