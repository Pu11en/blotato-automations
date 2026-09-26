"""Blotato's text-to-infographic family: 20 styles, one identical contract.

Every one of these templates takes exactly two text inputs -- a `description`
(10-500 chars) and a `footerText` CTA (2-100 chars) -- and returns a single
generated image. No reference media, so nothing gets uploaded and there is no
asset checksum to drift.

They are one file rather than 20 because only the template id and the label
differ; the registry accepts `ENTRIES` for exactly this case. Bounds below
are copied from the live template listing (`blotato inspect`), not guessed.

Verification status is per-style and honest: submitting one style tells you
that style works, not that the other 19 do. `VERIFIED` records which ones
have actually been run.
"""
from ..types import GenerationPlane, ModelEntry, SettingField

DESCRIPTION_MIN, DESCRIPTION_MAX = 10, 500
FOOTER_MIN, FOOTER_MAX = 2, 100
DEFAULT_FOOTER = "Follow for more"

# style slug -> (Blotato label, Blotato template id)
STYLES = {
    "billboard": ("Billboard Infographic", "76b3b959-bdbe-440d-8428-984219353f18"),
    "book-page": ("Book Page Infographic", "b88c8273-6406-48c6-85e7-096119aefe30"),
    "breaking-news": ("Breaking News", "8800be71-52df-4ac7-ac94-df9d8a494d0f"),
    "bus-ad": ("Bus Ad Infographic", "f9c0e470-9288-4958-8cdd-64772ed93c05"),
    "cave-painting": ("Cave Painting Infographic", "82ee75b6-597b-43a8-86bc-e4395e7c9c44"),
    "chalkboard": ("Chalkboard Infographic", "fcd64907-b103-46f8-9f75-51b9d1a522f5"),
    "classroom-chalkboard": (
        "Classroom Chalkboard Infographic",
        "d9495026-3945-44f6-8b44-07c28c492e6d",
    ),
    "constellation": ("Constellation Infographic", "5307053e-046b-4c9b-b1ca-38725d2ddcdd"),
    "egyptian-hieroglyph": (
        "Egyptian Hieroglyph Infographic",
        "a7b0d128-8478-4b34-9647-a0778b6517d0",
    ),
    "futuristic-flyer": ("Futuristic Flyer", "8fa8545e-8955-4a89-a868-cf45023d6cc5"),
    "graffiti-mural": ("Graffiti Mural Infographic", "3598483b-c148-4276-a800-eede85c1c62f"),
    "manga-panel": ("Manga Panel Infographic", "49c61370-a706-4b82-98f7-62d557d1c66d"),
    "movie-theater": ("Movie Theater Infographic", "f8f1ebe4-a9f5-4ec8-be63-21214656cd4b"),
    "newspaper": ("Newspaper Infographic", "07a5b5c5-387c-49e3-86b1-de822cd2dfc7"),
    "steampunk": ("Steampunk Infographic", "7b7104f1-d277-4993-ad3a-e5883c4b776d"),
    "top-secret": ("Top Secret Infographic", "b8707b58-a106-44af-bb12-e30507e561af"),
    "trail-marker": ("Trail Marker Infographic", "29ebb2bd-02b7-4317-8bb8-c30eb938e47c"),
    "tshirt": ("T-Shirt Infographic", "476f8920-8749-4ff7-9c91-470d54c3c03e"),
    "tv-wall": ("TV Wall Infographic", "013904bf-6b3b-43f4-bb1f-f1964a38c29b"),
    "whiteboard": ("Whiteboard Infographic", "ae868019-820d-434c-8fe1-74c9da99129a"),
}

# style slug -> date we actually submitted it live and looked at the output.
VERIFIED = {
    "newspaper": "2026-09-26",
    "whiteboard": "2026-09-26",
    "breaking-news": "2026-09-26",
}

# Each cost 50 credits on 2026-09-26; the family shares one renderer, so the
# unverified styles are expected to match, but that is an expectation.
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

SHARED_ISSUE = (
    "Only some styles in this family have been run live (see each entry's verified_at). "
    "The inputs are identical across all 20, so a plan built for an unverified style is "
    "structurally valid, but nobody has looked at what it renders."
)


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
        known_issues=tuple(issues) + ((SHARED_ISSUE,) if slug not in VERIFIED else ()),
        broken=False,
        verified_at=VERIFIED.get(slug),
        prompt_min_length=DESCRIPTION_MIN,
        prompt_max_length=DESCRIPTION_MAX,
        observed_credits=OBSERVED_CREDITS if slug in VERIFIED else None,
    )


ENTRIES = tuple(_entry(slug, label, tid) for slug, (label, tid) in sorted(STYLES.items()))
