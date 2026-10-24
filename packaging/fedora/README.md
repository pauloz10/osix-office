# Fedora packaging

OsiX uses Tauri v2's native RPM and AppImage bundlers rather than maintaining a second hand-written RPM payload. The Fedora files in this directory document/runtime-check the native dependencies and provide a future location for COPR/spec integration if OsiX is submitted to a Fedora repository.

Runtime expectations include WebKitGTK 4.1, GTK3 and standard desktop integration libraries. The AppImage bundles more dependencies and is intended as the portable fallback.
