import tempfile
import unittest
from pathlib import Path

from blotato.digest import compute_approval_digest, digest_for_plan, verify_plan_digest
from blotato.studio.plan import build_plan


def _plan(tmp, **overrides):
    plan = build_plan(
        model_id="product-scene-placement",
        prompt="a cheap and simple test prompt",
        media={"reference": [{"url": "https://example.com/a.jpg"}]},
        workspace=tmp,
    )
    plan.update(overrides)
    return plan


class ComputeDigestTest(unittest.TestCase):
    def test_is_stable_across_key_order(self):
        a = compute_approval_digest(
            model_id="m", prompt="p", media={"x": [1], "a": [2]}, settings={"z": 1, "b": 2}
        )
        b = compute_approval_digest(
            model_id="m", prompt="p", media={"a": [2], "x": [1]}, settings={"b": 2, "z": 1}
        )
        self.assertEqual(a, b)

    def test_changes_with_each_bound_field(self):
        base = dict(model_id="m", prompt="p", media={}, settings={})
        original = compute_approval_digest(**base)
        for field, value in [
            ("model_id", "other"),
            ("prompt", "other"),
            ("media", {"reference": []}),
            ("settings", {"a": 1}),
        ]:
            self.assertNotEqual(
                original, compute_approval_digest(**{**base, field: value}), f"{field} not bound"
            )


class VerifyPlanDigestTest(unittest.TestCase):
    """The digest is the only thing tying a human's credit approval to the
    content that will actually be generated."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_untouched_plan_verifies(self):
        verify_plan_digest(_plan(self.root))

    def test_approval_fields_do_not_invalidate_the_digest(self):
        # `blotato approve` writes these after the digest exists.
        plan = _plan(self.root)
        plan["max_credits_ceiling"] = 25
        plan["approval"] = {"reference": "me", "decided_at": "2026-09-26T00:00:00Z"}
        verify_plan_digest(plan)

    def test_edited_prompt_is_caught(self):
        plan = _plan(self.root)
        plan["prompt"] = "something entirely different and more expensive"
        with self.assertRaises(ValueError):
            verify_plan_digest(plan)

    def test_swapped_model_is_caught(self):
        plan = _plan(self.root)
        plan["model_id"] = "ai-video-with-ai-voice"
        with self.assertRaises(ValueError):
            verify_plan_digest(plan)

    def test_swapped_media_is_caught(self):
        plan = _plan(self.root)
        plan["media"]["reference"][0]["url"] = "https://example.com/substituted.jpg"
        with self.assertRaises(ValueError):
            verify_plan_digest(plan)

    def test_added_settings_are_caught(self):
        plan = _plan(self.root)
        plan["settings"]["sceneDescription"] = "injected"
        with self.assertRaises(ValueError):
            verify_plan_digest(plan)

    def test_missing_digest_is_rejected(self):
        plan = _plan(self.root)
        del plan["approval_digest"]
        with self.assertRaises(ValueError):
            verify_plan_digest(plan)

    def test_missing_bound_field_is_reported_clearly(self):
        plan = _plan(self.root)
        del plan["prompt"]
        with self.assertRaises(ValueError) as caught:
            digest_for_plan(plan)
        self.assertIn("prompt", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
