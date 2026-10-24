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

# Linux x2t ships shared libraries beside the sidecar. Tauri must bundle them
# for a fully offline Fedora installation. Keep the upstream resource list and
# add the Linux-specific patterns used by Euro-Office's own Linux CI.
resources = bundle.setdefault("resources", [])
for pattern in [
    "binaries/*.so",
    "binaries/*.so.*",
    "binaries/x2t",
    "binaries/fonts/*",
]:
    if pattern not in resources:
        resources.append(pattern)

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

# Linux-friendly dev command: the upstream main config currently contains a Windows-specific command.
# It is irrelevant to release bundling, but removing it prevents accidental PowerShell invocation on Fedora.
build = conf.setdefault("build", {})
if "beforeDevCommand" in build:
    build.pop("beforeDevCommand")

backup = conf_path.with_suffix(".json.upstream")
if not backup.exists():
    backup.write_text(conf_path.read_text())
conf_path.write_text(json.dumps(conf, indent=2) + "\n")
print(f"Updated {conf_path}")
