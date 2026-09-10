import dataclasses
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
STUDIO_SCRIPTS = REPO_ROOT / "skills" / "blotato-studio" / "scripts"
sys.path.insert(0, str(STUDIO_SCRIPTS))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


plan_mod = _load("blotato_studio_plan_for_submit_tests", STUDIO_SCRIPTS / "plan.py")
submit_mod = _load("blotato_studio_submit", STUDIO_SCRIPTS / "submit.py")


def _url_plan(model_id="product-scene-placement", prompt="x" * 20):
    return plan_mod.build_plan(
        model_id=model_id,
        prompt=prompt,
        media={"reference": [{"url": "https://example.com/product.jpg"}]},
    )


def _approve(plan, ceiling=500):
    plan["max_credits_ceiling"] = ceiling
    plan["approval"]["reference"] = "test-suite approval"
    plan["approval"]["decided_at"] = "2026-09-10T00:00:00Z"
    return plan


def _write_plan(tmp_path, plan):
    path = Path(tmp_path) / "plan.json"
    path.write_text(json.dumps(plan))
    return path


class SubmitGuardrailTest(unittest.TestCase):
    def test_refuses_without_ceiling(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = _url_plan()
            plan["approval"]["reference"] = "x"
            plan["approval"]["decided_at"] = "2026-09-10T00:00:00Z"
            path = _write_plan(tmp, plan)
            with self.assertRaises(SystemExit):
                submit_mod.submit(path)

    def test_refuses_without_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = _url_plan()
            plan["max_credits_ceiling"] = 500
            path = _write_plan(tmp, plan)
            with self.assertRaises(SystemExit):
                submit_mod.submit(path)

    def test_refuses_broken_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = plan_mod.build_plan(
                model_id="image-slideshow-text-overlays",
                prompt="ignored",
                media={"reference": [{"url": "https://example.com/a.jpg"}]},
            )
            _approve(plan)
            path = _write_plan(tmp, plan)
            with self.assertRaises(SystemExit):
                submit_mod.submit(path)

    def test_refuses_when_balance_below_ceiling(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = _approve(_url_plan(), ceiling=99999)
            path = _write_plan(tmp, plan)
            with mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 10}):
                with self.assertRaises(SystemExit):
                    submit_mod.submit(path)

    def test_refuses_on_local_asset_checksum_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            asset_dir = Path(tmp) / "brands" / "cinco-h-ranch" / "assets"
            asset_dir.mkdir(parents=True)
            asset_path = asset_dir / "fake.jpg"
            asset_path.write_bytes(b"original bytes")

            plan = plan_mod.build_plan(
                model_id="product-scene-placement",
                prompt="x" * 20,
                media={"reference": [{"path": "brands/cinco-h-ranch/assets/fake.jpg"}]},
                repo_root=Path(tmp),
            )
            _approve(plan)
            plan_path = _write_plan(tmp, plan)

            # Simulate drift after planning.
            asset_path.write_bytes(b"tampered bytes")

            with mock.patch.object(submit_mod, "REPO_ROOT", Path(tmp)), \
                 mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
                 mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 99999}):
                with self.assertRaises(SystemExit):
                    submit_mod.submit(plan_path)


class SubmitHappyPathTest(unittest.TestCase):
    def test_full_flow_downloads_image_and_records_credits(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = _approve(_url_plan())
            plan_path = _write_plan(tmp, plan)

            fake_credit_calls = iter([{"creditsRemaining": 1000}, {"creditsRemaining": 950}])

            def fake_get_credits(api_key):
                return next(fake_credit_calls)

            def fake_create_video_from_template(api_key, *, template_id, inputs, title, render):
                self.assertEqual(template_id, "f524614b-ba01-448c-967a-ce518c52a700")
                self.assertIn("productImage", inputs)
                self.assertIn("sceneDescription", inputs)
                return {"item": {"id": "job-123", "status": "done", "imageUrls": ["https://cdn.example.com/out.jpg"]}}

            def fake_urlretrieve(url, path):
                Path(path).write_bytes(b"fake image bytes")

            with mock.patch.object(submit_mod, "REPO_ROOT", Path(tmp)), \
                 mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
                 mock.patch.object(submit_mod.api, "get_credits", side_effect=fake_get_credits), \
                 mock.patch.object(submit_mod.api, "create_video_from_template", side_effect=fake_create_video_from_template), \
                 mock.patch.object(submit_mod.urllib.request, "urlretrieve", side_effect=fake_urlretrieve):
                result = submit_mod.submit(plan_path)

            self.assertEqual(result["final_status"], "done")
            self.assertEqual(result["credits_observed_delta"], 50)
            self.assertIsNotNone(result["media_path"])
            downloaded = Path(tmp) / result["media_path"]
            self.assertTrue(downloaded.is_file())
            self.assertEqual(downloaded.read_bytes(), b"fake image bytes")

            run_dir = Path(tmp) / result["run_dir"]
            self.assertTrue((run_dir / "request.sanitized.json").is_file())
            self.assertTrue((run_dir / "result.json").is_file())

    def test_no_publishing_fields_ever_reach_the_request(self):
        # A model that tried to sneak a publishing-shaped setting into
        # build_inputs would be caught here; verifies the gate actually runs
        # in the submit path, not just in isolated unit tests of runner.py.
        with tempfile.TemporaryDirectory() as tmp:
            plan = _approve(_url_plan())
            plan_path = _write_plan(tmp, plan)

            def fake_get_credits(api_key):
                return {"creditsRemaining": 1000}

            real_model = submit_mod.get_model("product-scene-placement")
            patched_model = dataclasses.replace(
                real_model,
                build_inputs=lambda plane: {
                    "productImage": "x",
                    "sceneDescription": "y",
                    "publish": True,
                },
            )
            with mock.patch.object(submit_mod, "REPO_ROOT", Path(tmp)), \
                 mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
                 mock.patch.object(submit_mod.api, "get_credits", side_effect=fake_get_credits), \
                 mock.patch.object(submit_mod, "get_model", return_value=patched_model):
                with self.assertRaises(submit_mod.br.RunValidationError):
                    submit_mod.submit(plan_path)


if __name__ == "__main__":
    unittest.main()
