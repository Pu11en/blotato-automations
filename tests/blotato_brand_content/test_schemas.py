import json
import unittest
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = REPO_ROOT / "schemas"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load(path):
    return json.loads(path.read_text())


class BrandProfileSchemaTest(unittest.TestCase):
    def setUp(self):
        self.schema = load(SCHEMAS / "brand-profile.schema.json")

    def test_valid_fixture_passes(self):
        instance = load(FIXTURES / "brand-profile.valid.json")
        jsonschema.validate(instance, self.schema)

    def test_invalid_fixture_fails(self):
        instance = load(FIXTURES / "brand-profile.invalid.json")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance, self.schema)


class BlotatoRunSchemaTest(unittest.TestCase):
    def setUp(self):
        self.schema = load(SCHEMAS / "blotato-run.schema.json")

    def test_valid_fixture_passes(self):
        instance = load(FIXTURES / "blotato-run.valid.json")
        jsonschema.validate(instance, self.schema)

    def test_invalid_fixture_fails(self):
        instance = load(FIXTURES / "blotato-run.invalid.json")
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(instance, self.schema)


if __name__ == "__main__":
    unittest.main()
