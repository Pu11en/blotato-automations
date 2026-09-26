import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from blotato import workspace


class WorkspaceRootTest(unittest.TestCase):
    def test_explicit_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(workspace.workspace_root(tmp), Path(tmp).resolve())

    def test_env_var_used_when_no_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {workspace.WORKSPACE_ENV_VAR: tmp}):
                self.assertEqual(workspace.workspace_root(), Path(tmp).resolve())

    def test_falls_back_to_cwd(self):
        env = {k: v for k, v in os.environ.items() if k != workspace.WORKSPACE_ENV_VAR}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(workspace.workspace_root(), Path.cwd().resolve())


class ResolveAssetTest(unittest.TestCase):
    def test_relative_path_resolves_against_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                workspace.resolve_asset("assets/a.jpg", root=tmp),
                Path(tmp).resolve() / "assets/a.jpg",
            )

    def test_absolute_path_passes_through(self):
        with tempfile.TemporaryDirectory() as tmp:
            absolute = Path(tmp).resolve() / "elsewhere.jpg"
            self.assertEqual(workspace.resolve_asset(absolute, root="/some/other/root"), absolute)


class DescribePathTest(unittest.TestCase):
    def test_inside_workspace_is_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp).resolve() / "outputs" / "run" / "x.json"
            self.assertEqual(
                workspace.describe_path(target, root=tmp), str(Path("outputs/run/x.json"))
            )

    def test_outside_workspace_stays_absolute(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            target = Path(other).resolve() / "x.json"
            self.assertEqual(workspace.describe_path(target, root=tmp), str(target))


class LoadEnvTest(unittest.TestCase):
    def test_reads_dotenv_from_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("BLOTATO_API_KEY=from-file\n# comment\n")
            env = {k: v for k, v in os.environ.items() if k != "BLOTATO_API_KEY"}
            with mock.patch.dict(os.environ, env, clear=True):
                self.assertEqual(workspace.load_env(root=tmp)["BLOTATO_API_KEY"], "from-file")

    def test_real_environment_beats_a_stale_dotenv_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("BLOTATO_API_KEY=stale\n")
            with mock.patch.dict(os.environ, {"BLOTATO_API_KEY": "exported"}):
                self.assertEqual(workspace.load_env(root=tmp)["BLOTATO_API_KEY"], "exported")

    def test_exported_key_works_with_no_dotenv_present(self):
        # The old file-only loader returned {} here, so an exported key was
        # invisible and every command failed with MissingCredentialError.
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"BLOTATO_API_KEY": "exported"}):
                self.assertEqual(workspace.load_env(root=tmp)["BLOTATO_API_KEY"], "exported")

    def test_quoted_values_are_unwrapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text('BLOTATO_API_KEY="quoted-key"\n')
            env = {k: v for k, v in os.environ.items() if k != "BLOTATO_API_KEY"}
            with mock.patch.dict(os.environ, env, clear=True):
                self.assertEqual(workspace.load_env(root=tmp)["BLOTATO_API_KEY"], "quoted-key")

    def test_does_not_mutate_os_environ(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".env").write_text("BLOTATO_SENTINEL=xyz\n")
            workspace.load_env(root=tmp)
            self.assertNotIn("BLOTATO_SENTINEL", os.environ)


if __name__ == "__main__":
    unittest.main()
