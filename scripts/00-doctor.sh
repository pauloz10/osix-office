#!/usr/bin/env bash
set -euo pipefail

need=(git python3 node npm rustc cargo pkg-config)
missing=()
for cmd in "${need[@]}"; do
  command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
done

if [[ -f /etc/fedora-release ]]; then
  echo "Fedora: $(cat /etc/fedora-release)"
else
  echo "WARNING: not running on Fedora; package build is supported on Fedora 44+ only." >&2
fi

if ((${#missing[@]})); then
  printf 'Missing commands: %s
' "${missing[*]}" >&2
  exit 1
fi

if command -v pkg-config >/dev/null 2>&1; then
  if pkg-config --exists webkit2gtk-4.1; then
    echo "WebKitGTK 4.1: $(pkg-config --modversion webkit2gtk-4.1)"
  else
    echo "Missing pkg-config package webkit2gtk-4.1" >&2
    exit 1
  fi
fi

echo "Node: $(node --version)"
echo "npm:  $(npm --version)"
echo "Rust: $(rustc --version)"
echo "Cargo: $(cargo --version)"
echo "Toolchain preflight passed."
