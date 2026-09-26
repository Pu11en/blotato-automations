"""A consuming project must be able to add techniques without forking."""
import unittest

from blotato.catalog import registry
from blotato.catalog.types import GenerationPlane, ModelEntry, SettingField


def _entry(model_id="test-technique"):
    return ModelEntry(
        id=model_id,
        blotato_template_id="tpl-123",
        surface="image",
        label="Test Technique",
        description="Contributed by a consuming project.",
        roles={},
        settings={"tone": SettingField(kind="text", default="plain")},
        build_inputs=lambda plane: {"description": plane.prompt},
        verified_at="2026-09-26",
        observed_credits=1,
    )


class RuntimeRegistrationTest(unittest.TestCase):
    def setUp(self):
        self._saved = dict(registry._EXTRA)
        registry.reset()

    def tearDown(self):
        registry._EXTRA.clear()
        registry._EXTRA.update(self._saved)
        registry.reset()

    def test_a_registered_technique_becomes_visible(self):
        registry.register(_entry())
        self.assertIn("test-technique", {m.id for m in registry.list_models()})
        self.assertEqual(registry.get_model("test-technique").label, "Test Technique")

    def test_registration_records_where_it_came_from(self):
        registry.register(_entry(), origin="youtube-money")
        self.assertEqual(registry.get_model("test-technique").origin, "youtube-money")
        self.assertIn("youtube-money", registry.origins())

    def test_built_in_entries_are_attributed_to_this_package(self):
        self.assertEqual(registry.get_model("infographic-newspaper").origin, "blotato")

    def test_origin_filter_separates_contributed_from_built_in(self):
        registry.register(_entry(), origin="youtube-money")
        contributed = registry.list_models(origin="youtube-money")
        self.assertEqual([m.id for m in contributed], ["test-technique"])
        self.assertNotIn(
            "test-technique", {m.id for m in registry.list_models(origin="blotato")}
        )

    def test_a_contributed_technique_works_end_to_end(self):
        registry.register(_entry())
        from blotato.studio.plan import build_plan

        plan = build_plan(model_id="test-technique", prompt="a prompt long enough", media={})
        self.assertEqual(plan["blotato_template_id"], "tpl-123")
        self.assertTrue(plan["approval_digest"].startswith("sha256:"))

    def test_claiming_a_taken_id_is_an_error_not_a_silent_override(self):
        # Two packages disagreeing about what an id means is a bug worth
        # surfacing, not something to resolve by import order.
        registry.register(_entry(model_id="infographic-newspaper"))
        with self.assertRaises(registry.DuplicateModelError):
            registry.list_models()

    def test_rejects_something_that_is_not_a_model_entry(self):
        with self.assertRaises(TypeError):
            registry.register({"id": "not-an-entry"})


class EntryPointDiscoveryTest(unittest.TestCase):
    """The `blotato.techniques` entry point is the supported way in."""

    def setUp(self):
        registry.reset()

    def tearDown(self):
        registry.reset()

    def test_entry_point_group_is_stable(self):
        # Consuming projects hardcode this string in their pyproject.toml.
        self.assertEqual(registry.ENTRY_POINT_GROUP, "blotato.techniques")

    def test_a_module_exporting_entries_is_read(self):
        import types

        module = types.ModuleType("fake_plugin")
        module.ENTRIES = (_entry("plugin-a"), _entry("plugin-b"))
        found = list(registry._entries_from(module, "fake_plugin"))
        self.assertEqual([e.id for e in found], ["plugin-a", "plugin-b"])

    def test_a_module_exporting_a_single_entry_is_read(self):
        import types

        module = types.ModuleType("fake_plugin")
        module.ENTRY = _entry("plugin-single")
        found = list(registry._entries_from(module, "fake_plugin"))
        self.assertEqual([e.id for e in found], ["plugin-single"])

    def test_a_module_exporting_nothing_is_ignored(self):
        import types

        self.assertEqual(list(registry._entries_from(types.ModuleType("empty"), "empty")), [])

    def test_a_module_exporting_junk_is_rejected_loudly(self):
        import types

        module = types.ModuleType("bad_plugin")
        module.ENTRIES = ({"id": "nope"},)
        with self.assertRaises(TypeError):
            list(registry._entries_from(module, "bad_plugin"))


if __name__ == "__main__":
    unittest.main()
