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
        self.assertIn('--bundles rpm', s)
        self.assertIn('--bundles appimage', s)
        self.assertIn('APPIMAGE_EXTRACT_AND_RUN=1', s)
        self.assertIn('NO_STRIP=true', s)

    def test_fedora_workflow_has_linux_build_dependencies(self):
        s = (ROOT / ".github" / "workflows" / "build-fedora.yml").read_text()
        for item in ("gh ", "rsync", "bc", "java-25-openjdk-headless", "python3-pillow"):
            self.assertIn(item, s)
        self.assertIn("actions/cache@v4", s)
        self.assertIn("Upload RPM", s)
        self.assertIn('APPIMAGE_EXTRACT_AND_RUN: "1"', s)

    def test_artifact_collection_handles_target_specific_tauri_paths(self):
        s = (ROOT / "scripts" / "06-collect-artifacts.sh").read_text()
        self.assertIn('src-tauri/target', s)
        self.assertNotIn('target/release/bundle', s)

    def test_linux_resource_set_replaces_windows_globs(self):
        s = (ROOT / "scripts" / "customize.py").read_text()
        for item in ('"binaries/*.so"', '"binaries/*.so.*"', '"binaries/x2t"'):
            self.assertIn(item, s)
        self.assertIn('bundle["resources"] = [', s)
        self.assertNotIn('"binaries/*.dll"', s)

if __name__ == "__main__":
    unittest.main()
