# Licensing and clean-room rules

## Allowed bases

- Euro-Office / Euro-Office Lite: AGPL-3.0. The derivative application must retain AGPL obligations and make corresponding source available when distributed.
- LibreOffice: primarily MPL-2.0, with additional open-source components. Keep it as a separate compatibility engine/process unless a specific file-level licence review is completed before code is copied.
- WordCraft: MIT OR Apache-2.0. Individual code may be reused only with attribution and preservation of its licence notices.
- Microsoft Open XML documentation: use as interoperability documentation. Do not copy Microsoft Office program source or proprietary assets.

## Prohibited sources

- WPS Office source/binaries may not be decompiled, reverse engineered or copied into this project.
- Microsoft Office binaries/source, Ribbon artwork, icons and proprietary fonts are not project source material.
- Do not scrape proprietary application binaries for implementation code.

## Recommended project licence

All new OsiX Office glue code and patches should be published under AGPL-3.0-or-later to remain simple and compatible with the primary Euro-Office-derived application.

## Trademarks

Do not ship the Microsoft, Excel, Word, PowerPoint, WPS, LibreOffice or Euro-Office logos as OsiX Office branding. Compatibility statements should be descriptive only.

## No AI dependency

The core OsiX Office distribution does not bundle or depend on ChatUI, OpenAI SDKs, Ollama, remote model services or generative-AI components. This keeps the base suite offline-focused and reduces unrelated licensing and privacy dependencies.
