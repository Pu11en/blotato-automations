import tempfile
import unittest
from pathlib import Path

from blotato.studio.plan import build_plan

ASSET_REL = "assets/example-product-front.jpg"


class BuildPlanTest(unittest.TestCase):
    """Plans resolve local media against a workspace directory, so every case
    here builds its own throwaway workspace rather than pointing at a checked-in
    asset."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        asset = self.root / ASSET_REL
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset.write_bytes(b"synthetic product photo bytes")

    def tearDown(self):
        self._tmp.cleanup()

    def plan(self, **kwargs):
        kwargs.setdefault("workspace", self.root)
        return build_plan(**kwargs)

    def test_builds_valid_plan_for_product_scene_placement(self):
        plan = self.plan(
            model_id="product-scene-placement",
            prompt="A professional product photograph of the product on a wooden shelf.",
            media={"reference": [{"path": ASSET_REL}]},
        )
        self.assertEqual(plan["model_id"], "product-scene-placement")
        self.assertEqual(len(plan["media"]["reference"]), 1)
        self.assertTrue(plan["approval_digest"].startswith("sha256:"))
        self.assertIsNone(plan["max_credits_ceiling"])

    def test_rejects_wrong_reference_count(self):
        with self.assertRaises(ValueError):
            self.plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": ASSET_REL}, {"path": ASSET_REL}]},
            )

    def test_rejects_missing_required_role(self):
        with self.assertRaises(ValueError):
            self.plan(model_id="product-scene-placement", prompt="x" * 20, media={})

    def test_rejects_unaccepted_role(self):
        with self.assertRaises(ValueError):
            self.plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": ASSET_REL}], "start": [{"path": ASSET_REL}]},
            )

    def test_rejects_missing_asset_file(self):
        with self.assertRaises(ValueError):
            self.plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": "assets/does-not-exist.jpg"}]},
            )

    def test_rejects_checksum_mismatch(self):
        with self.assertRaises(ValueError):
            self.plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": ASSET_REL, "checksum_sha256": "0" * 64}]},
            )

    def test_absolute_asset_path_is_accepted(self):
        plan = self.plan(
            model_id="product-scene-placement",
            prompt="x" * 20,
            media={"reference": [{"path": str(self.root / ASSET_REL)}]},
        )
        self.assertEqual(len(plan["media"]["reference"]), 1)

    def test_broken_model_still_plans_but_warns(self):
        # Planning a broken model must not raise (it is zero-cost); only
        # submit refuses to spend credits on a broken model.
        plan = self.plan(
            model_id="image-slideshow-text-overlays",
            prompt="ignored for this template",
            media={"reference": [{"path": ASSET_REL, "caption": "hello"}]},
        )
        self.assertTrue(plan["broken"])

    def test_accepts_url_media_without_local_file(self):
        plan = self.plan(
            model_id="product-scene-placement",
            prompt="x" * 20,
            media={"reference": [{"url": "https://example.com/already-hosted.jpg"}]},
        )
        self.assertEqual(
            plan["media"]["reference"][0]["url"], "https://example.com/already-hosted.jpg"
        )


if __name__ == "__main__":
    unittest.main()
