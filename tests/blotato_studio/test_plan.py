import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STUDIO_SCRIPTS = REPO_ROOT / "skills" / "blotato-studio" / "scripts"
sys.path.insert(0, str(STUDIO_SCRIPTS))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plan_mod = _load("blotato_studio_plan", STUDIO_SCRIPTS / "plan.py")

REAL_ASSET = "brands/cinco-h-ranch/assets/texas-campfire-soap-front.jpg"


class BuildPlanTest(unittest.TestCase):
    def test_builds_valid_plan_for_product_scene_placement(self):
        plan = plan_mod.build_plan(
            model_id="product-scene-placement",
            prompt="A professional product photograph of the product on a wooden shelf.",
            media={"reference": [{"path": REAL_ASSET}]},
        )
        self.assertEqual(plan["model_id"], "product-scene-placement")
        self.assertEqual(len(plan["media"]["reference"]), 1)
        self.assertTrue(plan["approval_digest"].startswith("sha256:"))
        self.assertIsNone(plan["max_credits_ceiling"])

    def test_rejects_wrong_reference_count(self):
        with self.assertRaises(ValueError):
            plan_mod.build_plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": REAL_ASSET}, {"path": REAL_ASSET}]},
            )

    def test_rejects_missing_required_role(self):
        with self.assertRaises(ValueError):
            plan_mod.build_plan(model_id="product-scene-placement", prompt="x" * 20, media={})

    def test_rejects_unaccepted_role(self):
        with self.assertRaises(ValueError):
            plan_mod.build_plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": REAL_ASSET}], "start": [{"path": REAL_ASSET}]},
            )

    def test_rejects_missing_asset_file(self):
        with self.assertRaises(ValueError):
            plan_mod.build_plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": "brands/cinco-h-ranch/assets/does-not-exist.jpg"}]},
            )

    def test_rejects_checksum_mismatch(self):
        with self.assertRaises(ValueError):
            plan_mod.build_plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": REAL_ASSET, "checksum_sha256": "0" * 64}]},
            )

    def test_broken_model_still_plans_but_warns(self):
        # Planning a broken model should not raise (it's zero-cost); only
        # submit.py refuses to spend on a broken model.
        plan = plan_mod.build_plan(
            model_id="image-slideshow-text-overlays",
            prompt="ignored for this template",
            media={"reference": [{"path": REAL_ASSET, "caption": "hello"}]},
        )
        self.assertTrue(plan["broken"])

    def test_accepts_url_media_without_local_file(self):
        plan = plan_mod.build_plan(
            model_id="product-scene-placement",
            prompt="x" * 20,
            media={"reference": [{"url": "https://example.com/already-hosted.jpg"}]},
        )
        self.assertEqual(plan["media"]["reference"][0]["url"], "https://example.com/already-hosted.jpg")


if __name__ == "__main__":
    unittest.main()
