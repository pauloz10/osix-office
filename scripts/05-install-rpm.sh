#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mapfile -t rpms < <(find "$ROOT/work/euro-office-lite/src-tauri/target/release/bundle/rpm" -type f -name '*.rpm' 2>/dev/null | sort)
if (( ${#rpms[@]} == 0 )); then
  echo "No RPM found. Run 04-build.sh first." >&2
  exit 1
fi
sudo dnf install -y "${rpms[-1]}"
