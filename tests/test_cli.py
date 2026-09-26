"""The CLI module had a syntax error that the whole suite missed, because
nothing imported it. These tests exercise the argument surface so a broken
command is caught here rather than by a user."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from blotato import cli


def run(argv):
    """Run a CLI command, returning (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 2
    return code, out.getvalue(), err.getvalue()


class ParserTest(unittest.TestCase):
    def test_every_subcommand_builds_and_has_a_handler(self):
        parser = cli.build_parser()
        actions = [a for a in parser._actions if hasattr(a, "choices") and a.choices]
        self.assertTrue(actions, "no subparsers found")
        subcommands = actions[0].choices
        expected = {
            "list", "show", "balance", "inspect", "plan",
            "approve", "submit", "poll", "spent", "pinterest",
        }
        self.assertLessEqual(expected, set(subcommands))
        for name, sub in subcommands.items():
            self.assertTrue(sub.get_default("func"), f"{name} has no handler")

    def test_help_renders_for_every_subcommand(self):
        # Catches a malformed help string or metavar in any parser.
        for name, sub in cli.build_parser()._subparsers._group_actions[0].choices.items():
            self.assertTrue(sub.format_help(), name)


class OfflineCommandTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_list(self):
        code, out, _ = run(["list"])
        self.assertEqual(code, 0)
        self.assertIn("technique(s)", out)

    def test_list_json_is_parseable(self):
        code, out, _ = run(["list", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertTrue(all("origin" in row for row in payload))

    def test_list_usable_only_hides_broken(self):
        _, out, _ = run(["list", "--usable-only"])
        self.assertNotIn("BROKEN", out)

    def test_show(self):
        code, out, _ = run(["show", "infographic-whiteboard"])
        self.assertEqual(code, 0)
        self.assertIn("observed cost", out)

    def test_show_unknown_model_is_a_clean_error(self):
        code, _, err = run(["show", "no-such-thing"])
        self.assertEqual(code, 2)
        self.assertIn("unknown technique", err)

    def test_plan_then_approve_then_spent(self):
        out_path = self.root / "plan.json"
        code, _, _ = run([
            "--workspace", str(self.root), "plan",
            "--model", "infographic-whiteboard",
            "--prompt", "a prompt comfortably longer than ten characters",
            "--out", str(out_path),
        ])
        self.assertEqual(code, 0)
        self.assertTrue(out_path.is_file())

        code, _, _ = run([
            "--workspace", str(self.root), "approve", str(out_path),
            "--max-credits", "50", "--reference", "test",
        ])
        self.assertEqual(code, 0)
        plan = json.loads(out_path.read_text())
        self.assertEqual(plan["max_credits_ceiling"], 50)

        code, out, _ = run(["--workspace", str(self.root), "spent"])
        self.assertEqual(code, 0)
        self.assertIn("no paid calls recorded", out)

    def test_spent_renders_a_recorded_call(self):
        from blotato import ledger

        ledger.record(
            {"run": "demo", "model_id": "infographic-whiteboard",
             "credits_observed_delta": 50},
            workspace=self.root,
        )
        code, out, _ = run(["--workspace", str(self.root), "spent", "--run", "demo"])
        self.assertEqual(code, 0)
        self.assertIn("50", out)
        self.assertIn("1 paid call(s)", out)

    def test_spent_json(self):
        from blotato import ledger

        ledger.record({"run": "demo", "credits_observed_delta": 7}, workspace=self.root)
        code, out, _ = run(["--workspace", str(self.root), "spent", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["credits"], 7)

    def test_missing_plan_file_is_a_clean_error(self):
        code, _, err = run(["submit", str(self.root / "nope.json")])
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)

    def test_missing_credential_is_a_clean_error(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            code, _, err = run(["--workspace", str(self.root), "balance"])
        self.assertEqual(code, 2)
        self.assertIn("BLOTATO_API_KEY", err)


if __name__ == "__main__":
    unittest.main()
