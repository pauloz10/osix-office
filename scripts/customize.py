#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "work" / "euro-office-lite"
conf_path = work / "src-tauri" / "tauri.conf.json"
brand_path = root / "config" / "branding.json"

if not conf_path.exists():
    raise SystemExit(f"Missing {conf_path}. Run 02-fetch-base.sh first.")

brand = json.loads(brand_path.read_text())
conf = json.loads(conf_path.read_text())

conf["productName"] = brand["product_name"]
conf["mainBinaryName"] = brand["binary_name"]
conf["identifier"] = brand["identifier"]
for w in conf.get("app", {}).get("windows", []):
    w["title"] = brand["window_title"]

bundle = conf.setdefault("bundle", {})
bundle["active"] = True
bundle["targets"] = ["rpm", "appimage"]
bundle["shortDescription"] = brand["description"]
bundle["longDescription"] = (
    "A fully offline, open-source desktop office suite focused on high-fidelity "
    "DOCX, XLSX and PPTX editing on Linux."
)
bundle["license"] = brand["license"]

# Replace the Windows-oriented upstream bundle resources with the exact
# Linux resource set used by Euro-Office Lite's own Linux CI. Tauri treats
# unmatched resource globs (for example binaries/*.dll) as build errors.
bundle["icon"] = [
    "icons/icon.png",
    "icons/128x128.png",
    "icons/128x128@2x.png",
    "icons/32x32.png",
    "icons/256x256.png",
]
bundle["resources"] = [
    "binaries/*.so",
    "binaries/*.so.*",
    "binaries/*.config",
    "binaries/*.dat",
    "binaries/*.js",
    "binaries/x2t",
    "binaries/fonts/*",
    "editors/sdkjs/word/*",
    "editors/sdkjs/cell/*",
    "editors/sdkjs/slide/*",
    "editors/sdkjs/common/Native/*",
    "editors/sdkjs/common/AllFonts.js",
    "editors/sdkjs/common/libfont/engine/*",
    "editors/web-apps/vendor/xregexp/*",
    "templates/*",
]

# Expand desktop associations for common macro-enabled and template Office formats.
existing = bundle.setdefault("fileAssociations", [])
seen = {ext for item in existing for ext in item.get("ext", [])}
extra = [
    (["xlsm"], "application/vnd.ms-excel.sheet.macroEnabled.12", "Macro-enabled spreadsheet"),
    (["xltx"], "application/vnd.openxmlformats-officedocument.spreadsheetml.template", "Spreadsheet template"),
    (["xltm"], "application/vnd.ms-excel.template.macroEnabled.12", "Macro-enabled spreadsheet template"),
    (["xlsb"], "application/vnd.ms-excel.sheet.binary.macroEnabled.12", "Binary spreadsheet"),
    (["docm"], "application/vnd.ms-word.document.macroEnabled.12", "Macro-enabled document"),
    (["dotx"], "application/vnd.openxmlformats-officedocument.wordprocessingml.template", "Document template"),
    (["dotm"], "application/vnd.ms-word.template.macroEnabled.12", "Macro-enabled document template"),
    (["pptm"], "application/vnd.ms-powerpoint.presentation.macroEnabled.12", "Macro-enabled presentation"),
    (["potx"], "application/vnd.openxmlformats-officedocument.presentationml.template", "Presentation template"),
    (["potm"], "application/vnd.ms-powerpoint.template.macroEnabled.12", "Macro-enabled presentation template"),
]
for exts, mime, desc in extra:
    if not any(e in seen for e in exts):
        existing.append({"ext": exts, "mimeType": mime, "description": desc})
        seen.update(exts)

# The pinned upstream config has a Windows-only development junction command.
# It is not needed for production bundling and must not execute on Fedora.
conf.setdefault("build", {}).pop("beforeDevCommand", None)

backup = conf_path.with_suffix(".json.upstream")
if not backup.exists():
    backup.write_text(conf_path.read_text())
conf_path.write_text(json.dumps(conf, indent=2) + "\n")
print(f"Updated {conf_path}")
