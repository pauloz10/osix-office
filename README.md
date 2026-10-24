# OsiX Office — Fedora bootstrap

OsiX Office is a fully offline, open-source desktop office-suite project focused on Microsoft Office interoperability, with Excel/XLSX compatibility as the highest priority.

**This build contains no AI assistant, ChatUI, OpenAI, Ollama or cloud-model dependency.** The core suite is intended to remain usable on an isolated Fedora workstation with no Internet connection.

## Base architecture

Primary editor shell: Euro-Office Lite / Euro-Office-derived components under AGPL-3.0, providing the modern desktop editing base and local document conversion pipeline.

Optional compatibility engine: LibreOffice, kept as a separate installed process/package rather than copied into the primary application. It can be used for conversion checks and selected edge cases, including some VBA-heavy XLSM workflows.

Reference-only products: Microsoft Office and WPS Office. No source code, binary code, reverse-engineering output, artwork, icons or proprietary assets from these products may be copied into OsiX.

WordCraft components may be evaluated only where their MIT/Apache-2.0 licensing and technical value justify inclusion.

## Planned applications

- **OsiX Writer** — DOCX/DOC/ODT/RTF workflows
- **OsiX Sheets** — XLSX/XLS/XLSM/XLSB/ODS/CSV workflows
- **OsiX Presentation** — PPTX/PPT/PPTM/ODP workflows
- **OsiX PDF** — local PDF viewing/export capability where supported by the selected upstream engine

The first builds may expose these through a unified OsiX Office shell while the project evolves.

## What this kit does

1. Installs Fedora/Tauri build prerequisites.
2. Fetches a pinned Euro-Office Lite source release.
3. Applies OsiX Office product branding and Microsoft-format file associations.
4. Configures Tauri to build both RPM and AppImage packages.
5. Builds local Fedora x86_64 packages.
6. Runs structural OOXML smoke tests against representative documents.
7. Keeps AI/cloud dependencies outside the project.

## Build on Fedora

```bash
chmod +x scripts/*.sh
./scripts/01-fedora-prereqs.sh
./scripts/02-fetch-base.sh
./scripts/03-customize.sh
./scripts/04-build.sh
```

Expected bundle locations:

```text
work/euro-office-lite/src-tauri/target/release/bundle/rpm/
work/euro-office-lite/src-tauri/target/release/bundle/appimage/
```

Install the locally built RPM with:

```bash
./scripts/05-install-rpm.sh
```

## Offline use

The installed application is intended for local document editing without cloud services, user accounts, telemetry or AI services. Internet access is needed during a normal source build only to obtain source/dependencies unless you maintain an offline source and dependency cache.

## Excel compatibility goal

OsiX Sheets should open, edit and save XLSX directly rather than converting the workbook to an ODF format. Priority areas include formulas, formatting, tables, named ranges, data validation, charts, filters, freeze panes, print settings, pivot content and XLSM round-trip preservation.

XLSM deserves special treatment: embedded VBA should be preserved wherever the underlying engine permits it, but OsiX will not falsely claim full Microsoft VBA execution compatibility. A separately installed LibreOffice compatibility mode may help with a subset of VBA scenarios.

See:

- `docs/ARCHITECTURE.md`
- `docs/EXCEL_COMPATIBILITY.md`
- `docs/LICENSING.md`
