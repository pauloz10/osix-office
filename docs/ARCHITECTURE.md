# OsiX Office architecture

OsiX Office is intentionally an office suite, not an AI product.

## Core rules

- No assistant, chatbot or generative-AI runtime is required or bundled.
- No OpenAI, Ollama, ChatUI, cloud-model or remote inference dependency.
- Documents must remain fully editable while the computer is offline.
- Native Microsoft Office formats are first-class interoperability targets: DOCX, XLSX/XLSM and PPTX.
- ODF formats remain supported.
- No proprietary Microsoft Office or WPS source code, binaries, artwork or reverse-engineered code is copied into OsiX.
- Euro-Office Lite / Euro-Office provides the primary open-source editor base.
- LibreOffice may be invoked as an optional, separately installed compatibility/conversion engine where useful.

## Desktop applications

The planned user-facing suite is:

- OsiX Writer — documents
- OsiX Sheets — spreadsheets, with Excel compatibility as the highest priority
- OsiX Presentation — presentations
- OsiX PDF — PDF viewing/export tools, subject to the capabilities and licences of the selected upstream components

The first Fedora build may ship these capabilities in one desktop shell while the UI is progressively separated into branded launch surfaces.

## Privacy model

Opening, editing, recalculating, saving and exporting local documents must not require an account or network connection. Online features, if ever added in a future branch, must be optional and outside the core offline build.

## Compatibility strategy

OsiX does not attempt to clone Microsoft Office implementation code. Compatibility is achieved through open-source editor engines, public file-format specifications, regression tests and clean-room behavioural testing.
