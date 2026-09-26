"""Blotato template: Product Scene Placement (image).

Live-verified 2026-09-08. WARNING: this template regenerates the product
rather than compositing the exact source pixels -- a live test showed a
color/edge shift versus the real product photo (see
outputs/blotato-runs/20260908-180421-... for the comparison). Treat every
output as a stylized reinterpretation, never as an approved exact-asset
representation, until a human reviews it against the real product.
"""
from ..types import GenerationPlane, ModelEntry, SettingField


def build_inputs(plane: GenerationPlane) -> dict:
    ref = plane.media["reference"][0]
    return {
        "productImage": ref.url,
        "sceneDescription": plane.prompt,
    }


ENTRY = ModelEntry(
    id="product-scene-placement",
    blotato_template_id="f524614b-ba01-448c-967a-ce518c52a700",
    surface="image",
    label="Product Scene Placement",
    description=(
        "Places one reference product photo into an AI-generated scene "
        "described by the prompt. Output is a single static image."
    ),
    roles={"reference": (1, 1)},
    settings={
        "sceneDescription": SettingField(kind="text", default="", min_length=10, max_length=500),
    },
    build_inputs=build_inputs,
    known_issues=(
        "Regenerates the product rather than preserving exact pixels -- verified "
        "2026-09-08 to shift color/edges versus the real source photo. Route every "
        "output through human review before treating it as an approved brand asset; "
        "never label it 'exact-asset'.",
    ),
    verified_at="2026-09-08",
)
