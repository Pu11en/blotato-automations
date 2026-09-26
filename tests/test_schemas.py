import json
import unittest
from pathlib import Path

import jsonschema

import blotato

# The schemas ship inside the package, so they are found the same way here as
# they would be from an installed wheel.
SCHEMAS = Path(blotato.__file__).resolve().parent / "schemas"
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


if __name__ == "__main__":
    unittest.main()
