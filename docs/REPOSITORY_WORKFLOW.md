# Repository workflow

OsiX development uses a small patch/customisation layer around a pinned Euro-Office Lite revision until the OsiX GitHub fork is available.

Branches planned for the hosted fork:

- `main` — releasable OsiX code
- `fedora-main` — Fedora/RPM/AppImage integration before merge
- `compat/xlsx` — spreadsheet compatibility work

The upstream remote should remain configured as `upstream` so changes from Euro-Office Lite can be reviewed and merged rather than copied manually.

Release tags use `v<version>` and trigger the Fedora package workflow.
