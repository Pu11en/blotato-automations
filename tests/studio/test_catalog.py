import unittest

from blotato.catalog import UnknownModelError, get_model, list_models
from blotato.catalog.templates import infographics


class CatalogTest(unittest.TestCase):
    def test_contains_the_hand_written_entries(self):
        ids = {m.id for m in list_models()}
        self.assertLessEqual(
            {"product-scene-placement", "image-slideshow-text-overlays", "ai-video-with-ai-voice"},
            ids,
        )

    def test_broken_model_is_flagged(self):
        model = get_model("image-slideshow-text-overlays")
        self.assertTrue(model.broken)
        self.assertTrue(model.known_issues)

    def test_verified_model_has_timestamp(self):
        model = get_model("product-scene-placement")
        self.assertFalse(model.broken)
        self.assertEqual(model.verified_at, "2026-09-08")

    def test_nothing_in_the_catalog_is_unproven(self):
        # Policy: an entry is either live-verified or explicitly marked broken.
        # Anything we have not run does not get listed at all.
        for model in list_models():
            self.assertTrue(
                model.verified_at or model.broken,
                f"{model.id} has never been run live -- verify it or drop it",
            )

    def test_live_verified_entries_record_what_a_run_cost(self):
        for model_id in ("ai-video-with-ai-voice", "infographic-newspaper"):
            model = get_model(model_id)
            self.assertEqual(model.verified_at, "2026-09-26", model_id)
            self.assertTrue(model.observed_credits, model_id)

    def test_unknown_id_raises(self):
        with self.assertRaises(UnknownModelError):
            get_model("no-such-model")

    def test_surface_filter(self):
        self.assertTrue(all(m.surface == "image" for m in list_models(surface="image")))
        self.assertTrue(all(m.surface == "video" for m in list_models(surface="video")))

    def test_include_broken_false_hides_broken(self):
        ids = {m.id for m in list_models(include_broken=False)}
        self.assertNotIn("image-slideshow-text-overlays", ids)


class CatalogInvariantsTest(unittest.TestCase):
    """Rules that must hold for every entry, including ones added later."""

    def setUp(self):
        self.models = list_models()

    def test_ids_are_unique(self):
        ids = [m.id for m in self.models]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_entry_declares_a_template_id_and_surface(self):
        for m in self.models:
            self.assertTrue(m.blotato_template_id, m.id)
            self.assertIn(m.surface, {"image", "video"}, m.id)

    def test_unverified_or_broken_entries_say_so_in_known_issues(self):
        # An entry nobody has run must not look trustworthy at a glance.
        for m in self.models:
            if m.verified_at is None or m.broken:
                self.assertTrue(m.known_issues, f"{m.id} is unproven but lists no known issues")

    def test_prompt_bounds_are_coherent(self):
        for m in self.models:
            if m.prompt_min_length is not None and m.prompt_max_length is not None:
                self.assertLess(m.prompt_min_length, m.prompt_max_length, m.id)

    def test_role_counts_are_coherent(self):
        for m in self.models:
            for role, (lo, hi) in m.roles.items():
                self.assertLessEqual(lo, hi, f"{m.id}.{role}")
                self.assertGreaterEqual(lo, 0, f"{m.id}.{role}")


class InfographicFamilyTest(unittest.TestCase):
    def test_every_style_is_registered(self):
        ids = {m.id for m in list_models()}
        for slug in infographics.STYLES:
            self.assertIn(f"infographic-{slug}", ids)

    def test_all_styles_share_one_contract(self):
        entries = [get_model(f"infographic-{slug}") for slug in infographics.STYLES]
        self.assertTrue(all(e.roles == {} for e in entries), "infographics need no media")
        self.assertTrue(all(e.surface == "image" for e in entries))
        self.assertEqual({tuple(sorted(e.settings)) for e in entries}, {("footerText",)})

    def test_template_ids_are_distinct(self):
        template_ids = [tid for _, tid in infographics.STYLES.values()]
        self.assertEqual(len(template_ids), len(set(template_ids)))

    def test_build_inputs_maps_prompt_to_description(self):
        from blotato.catalog.types import GenerationPlane

        plane = GenerationPlane(
            model_id="infographic-newspaper",
            prompt="10 ways to edit faster",
            media={},
            settings={"footerText": "Subscribe"},
        )
        self.assertEqual(
            infographics.build_inputs(plane),
            {"description": "10 ways to edit faster", "footerText": "Subscribe"},
        )

    def test_footer_falls_back_to_a_default(self):
        from blotato.catalog.types import GenerationPlane

        plane = GenerationPlane(model_id="x", prompt="p" * 20, media={}, settings={})
        self.assertEqual(infographics.build_inputs(plane)["footerText"], infographics.DEFAULT_FOOTER)

    def test_every_style_records_what_it_cost(self):
        for slug in infographics.STYLES:
            model = get_model(f"infographic-{slug}")
            self.assertEqual(model.observed_credits, infographics.OBSERVED_CREDITS, slug)

    def test_every_listed_style_has_been_run(self):
        self.assertEqual(set(infographics.STYLES), set(infographics.VERIFIED))

    def test_verified_styles_are_a_subset_of_known_styles(self):
        self.assertLessEqual(set(infographics.VERIFIED), set(infographics.STYLES))
        self.assertLessEqual(set(infographics.ISSUES), set(infographics.STYLES))



class AiVideoSceneParsingTest(unittest.TestCase):
    """The prompt-driven path needs no uploaded media, which is the path the
    earlier version of this entry could not reach at all."""

    def setUp(self):
        from blotato.catalog.templates import ai_video_with_ai_voice as mod

        self.mod = mod

    def test_splits_scenes_and_separates_image_prompt_from_script(self):
        scenes = self.mod.parse_scenes("a desk :: line one\n---\na window :: line two")
        self.assertEqual(scenes, [("a desk", "line one"), ("a window", "line two")])

    def test_scene_without_a_script_separator_reuses_the_text(self):
        self.assertEqual(self.mod.parse_scenes("just an image prompt"), [("just an image prompt", "just an image prompt")])

    def test_blank_blocks_are_dropped(self):
        self.assertEqual(len(self.mod.parse_scenes("a\n---\n\n---\nb")), 2)

    def test_a_dashed_line_inside_a_scene_is_not_a_separator(self):
        scenes = self.mod.parse_scenes("an --- inline dash :: narration")
        self.assertEqual(len(scenes), 1)

    def test_build_inputs_prefers_reference_media_when_present(self):
        from blotato.catalog.types import GenerationPlane, MediaItem

        plane = GenerationPlane(
            model_id="ai-video-with-ai-voice",
            prompt="ignored :: ignored",
            media={"reference": [MediaItem(asset_id="a", url="https://x/a.jpg", caption="said")]},
            settings={},
        )
        inputs = self.mod.build_inputs(plane)
        self.assertEqual(inputs["scenes"], [{"mediaSource": "https://x/a.jpg", "script": "said"}])

    def test_build_inputs_passes_every_declared_setting(self):
        from blotato.catalog.types import GenerationPlane

        plane = GenerationPlane(model_id="x", prompt="a :: b", media={}, settings={})
        inputs = self.mod.build_inputs(plane)
        for key in self.mod.ENTRY.settings:
            self.assertIn(key, inputs, f"{key} declared as a setting but never sent")



if __name__ == "__main__":
    unittest.main()
