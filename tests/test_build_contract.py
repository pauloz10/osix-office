import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class FedoraBuildContractTest(unittest.TestCase):
    def test_build_uses_upstream_linux_paths(self):
        s = (ROOT / "scripts" / "04-build.sh").read_text()
        self.assertIn("src/sdkjs/build", s)
        self.assertNotIn("if [[ -d sdkjs ]]", s)
        self.assertIn('GITHUB_REPOSITORY="delmarguillen/euro-office-lite"', s)
        self.assertIn("prepare-dist.sh", s)
        self.assertIn("--bundles rpm,appimage", s)

    def test_fedora_workflow_has_linux_build_dependencies(self):
        s = (ROOT / ".github" / "workflows" / "build-fedora.yml").read_text()
        for item in ("gh ", "rsync", "bc ", "java-17-openjdk-headless", "python3-pillow"):
            self.assertIn(item, s)

    def test_linux_sidecar_resources_are_bundled(self):
        s = (ROOT / "scripts" / "customize.py").read_text()
        self.assertIn('"binaries/*.so"', s)
        self.assertIn('"binaries/*.so.*"', s)
        self.assertIn('"binaries/x2t"', s)

if __name__ == "__main__":
    unittest.main()
