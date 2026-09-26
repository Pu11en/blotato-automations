import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from blotato import runner as br


class HashFileTest(unittest.TestCase):
    def test_matches_hashlib(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.bin"
            path.write_bytes(b"hello world" * 1000)
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(br.hash_file(path), expected)


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


if __name__ == "__main__":
    unittest.main()
