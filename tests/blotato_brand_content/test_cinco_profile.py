import hashlib
import json
import re
import unittest
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[2]
BRAND_DIR = REPO_ROOT / "brands" / "cinco-h-ranch"
SCHEMA_PATH = REPO_ROOT / "schemas" / "brand-profile.schema.json"


def load_merged_profile():
    profile = json.loads((BRAND_DIR / "profile.json").read_text())
    claims_doc = json.loads((BRAND_DIR / "claims.json").read_text())
    profile["claims"] = claims_doc["claims"]
    return profile


def matches_any(patterns, text):
    return any(re.search(entry["pattern"], text, re.IGNORECASE) for entry in patterns)


class CincoHRanchProfileTest(unittest.TestCase):
    def setUp(self):
        self.schema = json.loads(SCHEMA_PATH.read_text())
        self.profile = load_merged_profile()

    def test_merged_profile_passes_schema(self):
        jsonschema.validate(self.profile, self.schema)

    def test_every_fact_has_a_source_url(self):
        for fact in self.profile["facts"]:
            self.assertTrue(fact["source_url"].startswith("https://"))

    def test_every_approved_claim_has_a_known_fact_id(self):
        fact_ids = {fact["id"] for fact in self.profile["facts"]}
        for claim in self.profile["claims"]["approved"]:
            self.assertIn(claim["fact_id"], fact_ids)

    def test_sunscreen_copy_is_blocked(self):
        blocked = self.profile["claims"]["blocked"]
        for phrase in [
            "Our sunscreen stick gives you broad-spectrum SPF protection all day.",
            "This balm blocks UVA and UVB rays for water-resistant sun protection.",
        ]:
            self.assertTrue(matches_any(blocked, phrase), phrase)

    def test_pest_copy_is_blocked(self):
        blocked = self.profile["claims"]["blocked"]
        for phrase in [
            "This stick repels mosquitoes and ticks all afternoon.",
            "Keep chiggers and fleas away with our bug balm.",
        ]:
            self.assertTrue(matches_any(blocked, phrase), phrase)

    def test_pain_copy_is_blocked(self):
        blocked = self.profile["claims"]["blocked"]
        for phrase in [
            "Rub it in for fast pain relief after a long day of ranch work.",
            "Our analgesic formula soothes sore, inflamed muscles.",
        ]:
            self.assertTrue(matches_any(blocked, phrase), phrase)

    def test_disease_and_healing_copy_is_blocked(self):
        blocked = self.profile["claims"]["blocked"]
        for phrase in [
            "This cream heals eczema and psoriasis flare-ups.",
            "Customers use it to treat acne, rosacea, and infected wounds.",
        ]:
            self.assertTrue(matches_any(blocked, phrase), phrase)

    def test_assets_exist_and_match_recorded_checksum(self):
        assets = self.profile["assets"]
        self.assertGreater(len(assets), 0, "expected at least one real ingested asset")
        for asset in assets:
            path = REPO_ROOT / asset["path"]
            self.assertTrue(path.is_file(), f"missing asset file: {path}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, asset["checksum_sha256"], asset["asset_id"])
            self.assertEqual(asset["default_render_strategy"], "exact-asset")

    def test_approved_process_copy_is_not_blocked(self):
        blocked = self.profile["claims"]["blocked"]
        safe_phrase = "Made by hand in our Texas kitchen, in small batches, using tallow and lard."
        self.assertFalse(matches_any(blocked, safe_phrase))


if __name__ == "__main__":
    unittest.main()
