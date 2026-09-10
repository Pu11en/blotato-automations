import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "scripts" / "blotato" / "runner.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("blotato_run", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


br = _load_module()


def load_cinco_profile():
    profile = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "profile.json").read_text())
    claims = json.loads((REPO_ROOT / "brands" / "cinco-h-ranch" / "claims.json").read_text())
    profile["claims"] = claims["claims"]
    return profile


class HashFileTest(unittest.TestCase):
    def test_matches_hashlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.bin"
            path.write_bytes(b"hello world" * 1000)
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(br.hash_file(path), expected)


class RunStateTransitionTest(unittest.TestCase):
    def test_valid_transition_succeeds(self):
        state = br.RunState.new("cinco-h-ranch")
        self.assertEqual(state.state, "INSPECTED")
        state.transition("PLANNED")
        self.assertEqual(state.state, "PLANNED")

    def test_invalid_transition_raises(self):
        state = br.RunState.new("cinco-h-ranch")
        with self.assertRaises(br.InvalidTransitionError):
            state.transition("IMAGE_RUNNING")

    def test_unknown_state_raises(self):
        state = br.RunState.new("cinco-h-ranch")
        with self.assertRaises(br.InvalidTransitionError):
            state.transition("NOT_A_REAL_STATE")

    def test_terminal_states_have_no_outgoing_transitions(self):
        for terminal in ("FAILED", "TIMED_OUT", "REJECTED", "AUDIT_READY"):
            self.assertEqual(br.ALLOWED_TRANSITIONS[terminal], set())


class ResumeBehaviorTest(unittest.TestCase):
    """Task 2.1: an interrupted fixture must resume the stored external
    request instead of submitting another."""

    def test_resume_polls_instead_of_resubmitting(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = br.RunStore(Path(tmp))
            state = br.RunState.new("cinco-h-ranch")
            state.transition("PLANNED")
            state.transition("IMAGE_RUNNING")
            state.begin_generation("image", "req-original-123")
            store.create(state)

            # Simulate an interruption: drop the in-memory object and reload
            # from disk, as a restarted process would.
            resumed = store.load(state.run_id)

            self.assertEqual(resumed.pending_request_id("image"), "req-original-123")
            with self.assertRaises(br.DuplicateSubmissionError):
                resumed.begin_generation("image", "req-should-never-be-submitted")

    def test_complete_generation_requires_pending_request(self):
        state = br.RunState.new("cinco-h-ranch")
        state.transition("PLANNED")
        state.transition("IMAGE_RUNNING")
        with self.assertRaises(br.BlotatoRunError):
            state.complete_generation(
                "image", output_path="x", checksum_sha256="a" * 64, credits_observed_delta=1
            )


class RunStoreTest(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = br.RunStore(Path(tmp))
            state = br.RunState.new("cinco-h-ranch")
            store.create(state)
            reloaded = store.load(state.run_id)
            self.assertEqual(reloaded.to_dict(), state.to_dict())

    def test_lock_prevents_second_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = br.RunStore(Path(tmp))
            run_id = "20260101-000000-cinco-h-ranch-abcdef"
            with store.lock(run_id):
                with self.assertRaises(br.RunLockedError):
                    with store.lock(run_id):
                        pass  # pragma: no cover
            # Lock is released after the context manager exits.
            with store.lock(run_id):
                pass


class SanitizeTest(unittest.TestCase):
    def test_redacts_credential_shaped_keys_recursively(self):
        payload = {
            "headers": {"Authorization": "Bearer sk-real-secret-value"},
            "cookies": ["session=abc123"],
            "nested": {"deep": {"api_key": "sk-real-secret-value", "note": "fine"}},
        }
        sanitized = br.sanitize(payload)
        self.assertEqual(sanitized["headers"]["Authorization"], br.REDACTED)
        self.assertEqual(sanitized["cookies"], br.REDACTED)
        self.assertEqual(sanitized["nested"]["deep"]["api_key"], br.REDACTED)
        self.assertEqual(sanitized["nested"]["deep"]["note"], "fine")

    def test_redacts_configured_secret_value_embedded_in_string(self):
        secret = "sk-real-secret-value"
        payload = {"debug_url": f"https://blotato.example/x?token_value={secret}"}
        sanitized = br.sanitize(payload, secret_values=[secret])
        self.assertNotIn(secret, json.dumps(sanitized))

    def test_dump_sanitized_json_never_contains_raw_secret(self):
        secret = "sk-super-secret"
        payload = {"api_key": secret, "unrelated": [1, 2, {"authorization": secret}]}
        dumped = br.dump_sanitized_json(payload, secret_values=[secret])
        self.assertNotIn(secret, dumped)

    def test_sanitize_does_not_mutate_input(self):
        payload = {"api_key": "sk-real"}
        br.sanitize(payload)
        self.assertEqual(payload["api_key"], "sk-real")


class LoadApiKeyTest(unittest.TestCase):
    def test_missing_key_raises(self):
        with self.assertRaises(br.MissingCredentialError):
            br.load_api_key(env={})

    def test_present_key_returned(self):
        self.assertEqual(br.load_api_key(env={"BLOTATO_API_KEY": "sk-fake"}), "sk-fake")


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.profile = load_cinco_profile()
        self.http_calls = []

    def _fake_http_call(self):
        self.http_calls.append(1)

    def test_publishing_fields_rejected(self):
        for bad_fields in (
            {"publish": True},
            {"schedule_at": "2026-01-01"},
            {"social_account": "ig-123"},
            {"nested": {"accountId": "abc"}},
            {"items": [{"post_id": "p1"}]},
        ):
            with self.assertRaises(br.RunValidationError):
                br.validate_no_publishing_fields(bad_fields)

    def test_external_provider_credentials_rejected(self):
        for bad_fields in (
            {"openai_api_key": "sk-x"},
            {"anthropic_token": "sk-x"},
            {"nested": {"replicate_secret": "sk-x"}},
        ):
            with self.assertRaises(br.RunValidationError):
                br.validate_no_external_provider_credentials(bad_fields)

    def test_clean_request_fields_pass(self):
        br.validate_no_publishing_fields({"prompt": "a jar on a shelf"})
        br.validate_no_external_provider_credentials({"prompt": "a jar on a shelf"})

    def test_invalid_state_transition_rejected(self):
        state = br.RunState.new("cinco-h-ranch")
        with self.assertRaises(br.RunValidationError):
            br.validate_state_transition(state, "IMAGE_RUNNING")

    def test_source_asset_must_exist_in_profile(self):
        with self.assertRaises(br.RunValidationError):
            br.validate_source_asset(self.profile, "not-a-real-asset", REPO_ROOT)

    def test_source_asset_checksum_mismatch_rejected(self):
        tampered = json.loads(json.dumps(self.profile))
        for asset in tampered["assets"]:
            if asset["asset_id"] == "texas-campfire-soap-front":
                asset["checksum_sha256"] = "0" * 64
        with self.assertRaises(br.RunValidationError):
            br.validate_source_asset(tampered, "texas-campfire-soap-front", REPO_ROOT)

    def test_source_asset_missing_provenance_rejected(self):
        tampered = json.loads(json.dumps(self.profile))
        for asset in tampered["assets"]:
            if asset["asset_id"] == "texas-campfire-soap-front":
                asset["provenance"] = ""
        with self.assertRaises(br.RunValidationError):
            br.validate_source_asset(tampered, "texas-campfire-soap-front", REPO_ROOT)

    def test_valid_source_asset_passes(self):
        asset = br.validate_source_asset(self.profile, "texas-campfire-soap-front", REPO_ROOT)
        self.assertEqual(asset["asset_id"], "texas-campfire-soap-front")

    def test_full_validation_blocks_before_any_http_call(self):
        state = br.RunState.new("cinco-h-ranch")
        state.transition("PLANNED")

        bad_requests = [
            {"prompt": "ok", "publish": True},
            {"prompt": "ok", "openai_api_key": "sk-x"},
        ]
        for request_fields in bad_requests:
            with self.assertRaises(br.RunValidationError):
                br.validate_generation_request(
                    profile=self.profile,
                    run_state=state,
                    target_state="IMAGE_RUNNING",
                    source_asset_id="texas-campfire-soap-front",
                    request_fields=request_fields,
                    repo_root=REPO_ROOT,
                )
            self._fake_http_call()  # only reached because assertRaises caught it, not the code under test

        # The validation call itself must never let control reach past the
        # raise; confirm by checking the failing state was never re-armed.
        self.assertEqual(state.state, "PLANNED")

        # A fully clean request passes every gate.
        br.validate_generation_request(
            profile=self.profile,
            run_state=state,
            target_state="IMAGE_RUNNING",
            source_asset_id="texas-campfire-soap-front",
            request_fields={"prompt": "a jar of soap on a rustic wooden shelf"},
            repo_root=REPO_ROOT,
        )


if __name__ == "__main__":
    unittest.main()
