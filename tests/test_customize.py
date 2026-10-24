import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


class CustomizeConfigTest(unittest.TestCase):
    def test_expected_branding_contract(self):
        root = Path(__file__).resolve().parents[1]
        brand = json.loads((root / "config" / "branding.json").read_text())
        self.assertEqual(brand["product_name"], "OsiX Office")
        self.assertEqual(brand["binary_name"], "osix-office")
        self.assertEqual(brand["identifier"], "com.osix.office")
        self.assertTrue(brand["license"].startswith("AGPL-3.0"))

    def test_no_ai_dependencies_declared(self):
        root = Path(__file__).resolve().parents[1]
        text = "
".join(
            p.read_text(errors="ignore")
            for p in [root / "README.md", root / "docs" / "ARCHITECTURE.md"]
        ).lower()
        for required in ("no ai", "offline"):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
