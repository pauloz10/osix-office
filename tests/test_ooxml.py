import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ooxml_smoke", ROOT / "tests" / "ooxml_smoke.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class OoxmlSmokeTest(unittest.TestCase):
    def _make(self, macro=False):
        f = tempfile.NamedTemporaryFile(suffix=".xlsm" if macro else ".xlsx", delete=False)
        f.close()
        p = Path(f.name)
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("[Content_Types].xml", "<Types/>")
            z.writestr("xl/workbook.xml", "<workbook/>")
            if macro:
                z.writestr("xl/vbaProject.bin", b"placeholder")
        self.addCleanup(lambda: p.unlink(missing_ok=True))
        return p

    def test_xlsx(self):
        self.assertEqual(MOD.check(self._make(False)), 0)

    def test_xlsm_macro_detection(self):
        self.assertEqual(MOD.check(self._make(True)), 0)


if __name__ == "__main__":
    unittest.main()
