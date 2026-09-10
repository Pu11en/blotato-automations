import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "skills" / "blotato-studio" / "scripts"))

from catalog import get_model, list_models, UnknownModelError  # noqa: E402


class CatalogTest(unittest.TestCase):
    def test_lists_all_known_entries(self):
        ids = {m.id for m in list_models()}
        self.assertEqual(
            ids,
            {"product-scene-placement", "image-slideshow-text-overlays", "ai-video-with-ai-voice"},
        )

    def test_broken_model_is_flagged(self):
        model = get_model("image-slideshow-text-overlays")
        self.assertTrue(model.broken)
        self.assertTrue(model.known_issues)

    def test_verified_model_has_timestamp(self):
        model = get_model("product-scene-placement")
        self.assertFalse(model.broken)
        self.assertEqual(model.verified_at, "2026-09-08")

    def test_unverified_model_has_no_timestamp(self):
        model = get_model("ai-video-with-ai-voice")
        self.assertFalse(model.broken)
        self.assertIsNone(model.verified_at)
        self.assertTrue(model.known_issues)

    def test_unknown_model_raises(self):
        with self.assertRaises(UnknownModelError):
            get_model("not-a-real-model")

    def test_list_models_can_exclude_broken(self):
        ids = {m.id for m in list_models(include_broken=False)}
        self.assertNotIn("image-slideshow-text-overlays", ids)

    def test_list_models_can_filter_by_surface(self):
        image_models = list_models(surface="image")
        self.assertTrue(all(m.surface == "image" for m in image_models))
        self.assertIn("product-scene-placement", {m.id for m in image_models})


if __name__ == "__main__":
    unittest.main()
