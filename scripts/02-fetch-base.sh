#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
source "$ROOT/UPSTREAM.lock"
WORK="$ROOT/work"
SRC="$WORK/euro-office-lite"

mkdir -p "$WORK"

if [[ -d "$SRC/.git" ]]; then
  actual="$(git -C "$SRC" rev-parse --short=7 HEAD)"
  echo "Base source already exists at $SRC ($actual)"
  exit 0
fi

if [[ -n "${OSIX_UPSTREAM_DIR:-}" ]]; then
  echo "Using local upstream source: $OSIX_UPSTREAM_DIR"
  cp -a "$OSIX_UPSTREAM_DIR" "$SRC"
  exit 0
fi

if [[ -n "${OSIX_UPSTREAM_ARCHIVE:-}" ]]; then
  echo "Using local upstream archive: $OSIX_UPSTREAM_ARCHIVE"
  mkdir -p "$SRC"
  tar -xf "$OSIX_UPSTREAM_ARCHIVE" -C "$SRC" --strip-components=1
  exit 0
fi

echo "Fetching pinned upstream: $UPSTREAM_TAG ($UPSTREAM_COMMIT)"
git clone --recursive --branch "$UPSTREAM_TAG" "$UPSTREAM_REPOSITORY" "$SRC"
actual="$(git -C "$SRC" rev-parse HEAD)"
case "$actual" in
  "$UPSTREAM_COMMIT"*) ;;
  *) echo "WARNING: tag resolved to $actual, expected prefix $UPSTREAM_COMMIT" >&2 ;;
esac
