# OsiX Office build report — 24 October 2026

## Repository

- Active branch: `fedora-main`
- Base branch: `main`
- OsiX version: `0.2.0-dev`
- Upstream pin: Euro-Office Lite `v0.17.39-alpha`, commit prefix `5c4e5fa`
- Primary target: Fedora 44 x86_64
- Bundle targets: RPM and AppImage

## Validation completed

- Python unit tests pass.
- OOXML smoke checker detects spreadsheet packages and VBA project presence.
- Shell build scripts pass `bash -n` syntax checks.
- Python project scripts compile with `py_compile`.
- OsiX customization was integration-tested against a simulated upstream Tauri configuration.
- Branding result: `OsiX Office` / `osix-office` / `com.osix.office`.
- RPM + AppImage targets are injected into the Tauri bundle configuration.

## Compile status

The full application has not been compiled inside the ChatGPT build container because that environment cannot resolve `github.com`. The pinned upstream source and matching x2t sidecars therefore cannot be obtained here. The Fedora/GitHub build pipeline is in place and is intended to complete that step on a connected Fedora host or GitHub Actions runner.

This is an environmental network blocker, not a reported compiler failure in the OsiX code.
