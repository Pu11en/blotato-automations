"""Every test here asserts something about credits: that they are not spent
when they should not be, not spent twice, and not lost when they are."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from blotato.studio import plan as plan_mod
from blotato.studio import submit as submit_mod


def _approved_plan(tmp, **overrides):
    plan = plan_mod.build_plan(
        model_id="product-scene-placement",
        prompt="a cheap and simple test prompt",
        media={"reference": [{"url": "https://example.com/a.jpg"}]},
        workspace=tmp,
    )
    plan["max_credits_ceiling"] = 5
    plan["approval"] = {"reference": "approved the cheap plan", "decided_at": "2026-09-26T00:00:00Z"}
    plan.update(overrides)
    path = Path(tmp) / "plan.json"
    path.write_text(json.dumps(plan))
    return path, plan


def _fake_download(url, path, **kwargs):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(b"bytes")
    return 5


class TamperedPlanTest(unittest.TestCase):
    """An approval is worthless unless it is bound to the plan it approved.
    Before this, editing plan.json after `approve` ran the edited plan under
    the old approval -- including swapping in a different model's template."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _assert_refused_without_paying(self, path):
        spend = mock.Mock(name="create_video_from_template")
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template", spend):
            with self.assertRaises(SystemExit):
                submit_mod.submit(path, workspace=self.root)
        spend.assert_not_called()

    def test_edited_prompt_is_refused(self):
        path, plan = _approved_plan(self.root)
        plan["prompt"] = "TAMPERED: an entirely different, expensive generation"
        path.write_text(json.dumps(plan))
        self._assert_refused_without_paying(path)

    def test_swapped_model_is_refused(self):
        path, plan = _approved_plan(self.root)
        plan["model_id"] = "ai-video-with-ai-voice"
        path.write_text(json.dumps(plan))
        self._assert_refused_without_paying(path)

    def test_substituted_media_is_refused(self):
        path, plan = _approved_plan(self.root)
        plan["media"]["reference"][0]["url"] = "https://example.com/substituted.jpg"
        path.write_text(json.dumps(plan))
        self._assert_refused_without_paying(path)

    def test_raised_ceiling_alone_is_still_accepted(self):
        # The ceiling is intentionally outside the digest: `approve` writes it.
        path, plan = _approved_plan(self.root)
        plan["max_credits_ceiling"] = 500
        path.write_text(json.dumps(plan))
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "j1", "status": "done"}}), \
             mock.patch.object(submit_mod, "download", _fake_download):
            result = submit_mod.submit(path, workspace=self.root)
        self.assertEqual(result["final_status"], "done")


class DoubleSpendTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_resubmitting_the_same_plan_refuses_instead_of_paying_again(self):
        path, _ = _approved_plan(self.root)
        calls = []

        def spend(api_key, **kwargs):
            calls.append(kwargs)
            return {"item": {"id": "job-1", "status": "done", "imageUrls": ["https://cdn/x.jpg"]}}

        patches = lambda: (
            mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"),
            mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}),
            mock.patch.object(submit_mod.api, "create_video_from_template", side_effect=spend),
            mock.patch.object(submit_mod, "download", _fake_download),
        )
        a, b, c, d = patches()
        with a, b, c, d:
            first = submit_mod.submit(path, workspace=self.root)
        self.assertEqual(first["final_status"], "done")

        a, b, c, d = patches()
        with a, b, c, d:
            with self.assertRaises(SystemExit) as caught:
                submit_mod.submit(path, workspace=self.root)

        self.assertEqual(len(calls), 1, "paid twice for the same plan")
        self.assertIn("already submitted", str(caught.exception))
        self.assertIn("blotato poll", str(caught.exception))


class TimeoutRecoveryTest(unittest.TestCase):
    """A poll timeout used to mean the credits were gone and the media was
    unreachable: there was no way to ask about the job again."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _submit_that_times_out(self, path):
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "job-7", "status": "rendering"}}), \
             mock.patch.object(submit_mod.api, "get_video_creation",
                               return_value={"item": {"id": "job-7", "status": "rendering"}}):
            return submit_mod.submit(path, workspace=self.root, poll_interval=0, poll_timeout=0)

    def test_timeout_records_the_job_and_how_to_recover(self):
        path, _ = _approved_plan(self.root)
        result = self._submit_that_times_out(path)
        self.assertTrue(result["timed_out"])
        self.assertEqual(result["job_id"], "job-7")
        self.assertIn("blotato poll", result["recover_with"])

    def test_poll_finishes_the_job_and_downloads_without_spending(self):
        path, _ = _approved_plan(self.root)
        timed_out = self._submit_that_times_out(path)
        run_dir = self.root / timed_out["run_dir"]

        spend = mock.Mock(name="create_video_from_template")
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template", spend), \
             mock.patch.object(submit_mod.api, "get_video_creation",
                               return_value={"item": {"id": "job-7", "status": "done",
                                                      "imageUrls": ["https://cdn/out.jpg?sig=1"]}}), \
             mock.patch.object(submit_mod, "download", _fake_download):
            result = submit_mod.poll(run_dir, workspace=self.root)

        spend.assert_not_called()
        self.assertEqual(result["final_status"], "done")
        self.assertFalse(result["timed_out"])
        self.assertTrue((self.root / result["media_path"]).is_file())

    def test_poll_on_a_directory_that_never_submitted_refuses(self):
        empty = self.root / "outputs" / "blotato-studio-runs" / "nothing-here"
        empty.mkdir(parents=True)
        with self.assertRaises(SystemExit):
            submit_mod.poll(empty, workspace=self.root)


class MultiImageDownloadTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_every_returned_image_is_downloaded(self):
        # Only the first was fetched before, while `all_image_urls` recorded
        # the rest -- so the README's "a set of images" was not true.
        path, _ = _approved_plan(self.root)
        urls = [f"https://cdn/out-{i}.png?sig={i}" for i in range(1, 4)]
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "j", "status": "done", "imageUrls": urls}}), \
             mock.patch.object(submit_mod, "download", _fake_download):
            result = submit_mod.submit(path, workspace=self.root)

        self.assertEqual(len(result["media_paths"]), 3)
        for relative in result["media_paths"]:
            self.assertTrue((self.root / relative).is_file())
        # and the query string never leaks into a filename
        self.assertTrue(all(Path(p).suffix == ".png" for p in result["media_paths"]))

    def test_query_string_does_not_leak_into_a_single_filename(self):
        path, _ = _approved_plan(self.root)
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "j", "status": "done",
                                                      "mediaUrl": "https://cdn/v.mp4?token=x&e=2"}}), \
             mock.patch.object(submit_mod, "download", _fake_download):
            result = submit_mod.submit(path, workspace=self.root)
        self.assertEqual(Path(result["media_path"]).name, "generated.mp4")

    def test_a_failed_download_is_recorded_rather_than_crashing(self):
        path, _ = _approved_plan(self.root)
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 9999}), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "j", "status": "done",
                                                      "mediaUrl": "https://cdn/v.mp4"}}), \
             mock.patch.object(submit_mod, "download", side_effect=OSError("cdn refused")):
            result = submit_mod.submit(path, workspace=self.root)
        # The credits were already spent; the run must still be recorded.
        self.assertEqual(result["final_status"], "done")
        self.assertIn("cdn refused", result["download_error"])
        self.assertTrue((self.root / result["run_dir"] / "result.json").is_file())


if __name__ == "__main__":
    unittest.main()
