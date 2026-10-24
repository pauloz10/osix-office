#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUNDLE_ROOT="$ROOT/work/euro-office-lite/src-tauri/target"
DIST="$ROOT/dist"
mkdir -p "$DIST"
found=0
while IFS= read -r -d '' f; do
  cp -f "$f" "$DIST/"
  echo "Collected: $(basename "$f")"
  found=1
done < <(find "$BUNDLE_ROOT" -type f ( -name '*.rpm' -o -name '*.AppImage' ) -print0 2>/dev/null || true)
((found == 1)) || { echo "No RPM/AppImage artifacts found under $BUNDLE_ROOT" >&2; exit 1; }
