#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
conf_path = root / "work" / "euro-office-lite" / "src-tauri" / "tauri.conf.json"
if not conf_path.exists():
    raise SystemExit(f"missing {conf_path}")
conf = json.loads(conf_path.read_text())
assert conf.get("productName") == "OsiX Office"
assert conf.get("mainBinaryName") == "osix-office"
assert conf.get("identifier") == "com.osix.office"
targets = set(conf.get("bundle", {}).get("targets", []))
assert {"rpm", "appimage"} <= targets, targets
print("OsiX Tauri configuration verified.")
