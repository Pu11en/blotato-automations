"""A per-call ceiling bounds one call. These bound their sum."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from blotato import ledger
from blotato.studio import plan as plan_mod
from blotato.studio import submit as submit_mod


class LedgerFileTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_missing_ledger_reads_as_empty(self):
        self.assertEqual(ledger.entries(workspace=self.root), [])
        self.assertEqual(ledger.spent(workspace=self.root), 0)

    def test_records_append_rather_than_overwrite(self):
        for i in range(3):
            ledger.record({"run": "r", "credits_observed_delta": i}, workspace=self.root)
        self.assertEqual(len(ledger.entries(workspace=self.root)), 3)

    def test_every_row_is_timestamped(self):
        ledger.record({"run": "r", "credits_observed_delta": 1}, workspace=self.root)
        self.assertIn("at", ledger.entries(workspace=self.root)[0])

    def test_spent_sums_only_the_named_run(self):
        ledger.record({"run": "a", "credits_observed_delta": 10}, workspace=self.root)
        ledger.record({"run": "b", "credits_observed_delta": 5}, workspace=self.root)
        self.assertEqual(ledger.spent(run="a", workspace=self.root), 10)
        self.assertEqual(ledger.spent(run="b", workspace=self.root), 5)
        self.assertEqual(ledger.spent(workspace=self.root), 15)

    def test_an_unmeasured_call_counts_as_its_full_ceiling(self):
        # Guessing low is how a budget gets blown.
        ledger.record(
            {"run": "a", "credits_observed_delta": None, "assumed_credits": 60},
            workspace=self.root,
        )
        self.assertEqual(ledger.spent(run="a", workspace=self.root), 60)

    def test_a_truncated_line_does_not_hide_the_rest(self):
        ledger.record({"run": "a", "credits_observed_delta": 7}, workspace=self.root)
        path = ledger.ledger_path(workspace=self.root)
        with path.open("a", encoding="utf-8") as handle:
            handle.write('{"run": "a", "credits_obse\n')
        ledger.record({"run": "a", "credits_observed_delta": 3}, workspace=self.root)
        self.assertEqual(ledger.spent(run="a", workspace=self.root), 10)


class BudgetTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_no_budget_means_no_ceiling_on_the_sum(self):
        ledger.record({"run": "a", "credits_observed_delta": 9999}, workspace=self.root)
        ledger.check_budget(run="a", budget=None, ceiling=50, workspace=self.root)

    def test_a_call_that_fits_is_allowed(self):
        ledger.record({"run": "a", "credits_observed_delta": 40}, workspace=self.root)
        already = ledger.check_budget(run="a", budget=100, ceiling=50, workspace=self.root)
        self.assertEqual(already, 40)

    def test_a_call_that_would_exceed_the_budget_is_refused(self):
        ledger.record({"run": "a", "credits_observed_delta": 60}, workspace=self.root)
        with self.assertRaises(ledger.BudgetExceeded):
            ledger.check_budget(run="a", budget=100, ceiling=50, workspace=self.root)

    def test_another_runs_spending_does_not_count_against_this_one(self):
        ledger.record({"run": "other", "credits_observed_delta": 9999}, workspace=self.root)
        ledger.check_budget(run="a", budget=100, ceiling=50, workspace=self.root)

    def test_a_budget_without_a_run_name_is_a_mistake(self):
        with self.assertRaises(ValueError):
            ledger.check_budget(run=None, budget=100, ceiling=10, workspace=self.root)

    def test_a_non_positive_budget_is_rejected(self):
        with self.assertRaises(ValueError):
            ledger.check_budget(run="a", budget=0, ceiling=10, workspace=self.root)


def _approved_plan(tmp):
    plan = plan_mod.build_plan(
        model_id="infographic-whiteboard",
        prompt="a prompt that is comfortably long enough",
        media={},
        workspace=tmp,
    )
    plan["max_credits_ceiling"] = 50
    plan["approval"] = {"reference": "test", "decided_at": "2026-09-26T00:00:00Z"}
    path = Path(tmp) / "plan.json"
    path.write_text(json.dumps(plan))
    return path


def _fake_download(url, path, **kwargs):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(b"x")
    return 1


class SubmitAccountingTest(unittest.TestCase):
    """The hole this closes: a loop calling submit with a 50-credit ceiling
    could spend the whole balance, 50 at a time, every call looking correct."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _run_submit(self, path, **kwargs):
        balances = iter([{"creditsRemaining": 1000}, {"creditsRemaining": 950}])
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", side_effect=lambda k: next(balances)), \
             mock.patch.object(submit_mod.api, "create_video_from_template",
                               return_value={"item": {"id": "j", "status": "done",
                                                      "imageUrls": ["https://cdn/x.jpg"]}}), \
             mock.patch.object(submit_mod, "download", _fake_download):
            return submit_mod.submit(path, workspace=self.root, **kwargs)

    def test_a_paid_call_lands_in_the_ledger(self):
        result = self._run_submit(_approved_plan(self.root), run="demo")
        self.assertEqual(result["credits_observed_delta"], 50)
        rows = ledger.entries(run="demo", workspace=self.root)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["credits_observed_delta"], 50)
        self.assertEqual(rows[0]["model_id"], "infographic-whiteboard")

    def test_spending_accumulates_and_then_the_budget_refuses(self):
        # First call fits inside an 80-credit budget; the second would not.
        self._run_submit(_approved_plan(self.root), run="demo", budget=80)
        self.assertEqual(ledger.spent(run="demo", workspace=self.root), 50)

        second = _approved_plan(self.root)
        second_plan = json.loads(second.read_text())
        second_plan["prompt"] = "a different prompt, so a different digest entirely"
        second_plan["approval_digest"] = __import__(
            "blotato.digest", fromlist=["digest_for_plan"]
        ).digest_for_plan(second_plan)
        second.write_text(json.dumps(second_plan))

        spend = mock.Mock()
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", return_value={"creditsRemaining": 1000}), \
             mock.patch.object(submit_mod.api, "create_video_from_template", spend):
            with self.assertRaises(SystemExit) as caught:
                submit_mod.submit(second, workspace=self.root, run="demo", budget=80)

        spend.assert_not_called()
        self.assertIn("budget", str(caught.exception))
        self.assertEqual(ledger.spent(run="demo", workspace=self.root), 50)

    def test_the_budget_is_checked_before_any_money_moves(self):
        ledger.record({"run": "demo", "credits_observed_delta": 100}, workspace=self.root)
        spend = mock.Mock()
        balance = mock.Mock(return_value={"creditsRemaining": 1000})
        with mock.patch.object(submit_mod.br, "load_api_key", return_value="sk-fake"), \
             mock.patch.object(submit_mod.api, "get_credits", balance), \
             mock.patch.object(submit_mod.api, "create_video_from_template", spend):
            with self.assertRaises(SystemExit):
                submit_mod.submit(_approved_plan(self.root), workspace=self.root,
                                  run="demo", budget=100)
        spend.assert_not_called()
        balance.assert_not_called()

    def test_an_unnamed_run_still_gets_recorded(self):
        self._run_submit(_approved_plan(self.root))
        rows = ledger.entries(workspace=self.root)
        self.assertEqual(len(rows), 1)
        self.assertIsNone(rows[0]["run"])


if __name__ == "__main__":
    unittest.main()
