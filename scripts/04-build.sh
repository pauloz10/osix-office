#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/work/euro-office-lite"

[[ -d "$SRC" ]] || { echo "Missing source tree. Run make fetch first." >&2; exit 1; }

"$ROOT/scripts/00-doctor.sh"
cd "$SRC"

npm ci

# Generate editor loaders if the upstream submodule is present. This is the
# documented operation performed by upstream setup.ps1.
if [[ -d sdkjs ]]; then
  pushd sdkjs >/dev/null
  if [[ -f package-lock.json ]]; then npm ci; else npm install; fi
  if [[ -f Gruntfile.js ]]; then
    npx grunt develop
  elif [[ -f webpack.config.js ]]; then
    npm run build --if-present
  fi
  popd >/dev/null
fi

# Prefer upstream Linux helpers when they are added. Otherwise require the
# converter sidecars to be supplied by the source checkout / CI vendor step.
if [[ -f scripts/setup.sh ]]; then bash scripts/setup.sh; fi
if [[ -f scripts/get-x2t.sh ]]; then bash scripts/get-x2t.sh; fi

if [[ ! -d src-tauri/binaries ]] || ! find src-tauri/binaries -maxdepth 1 -type f -print -quit | grep -q .; then
  cat >&2 <<'MSG'
OsiX build stopped: x2t converter sidecars are not present.
Upstream currently retrieves these through its release-dependency workflow.
Populate src-tauri/binaries from the matching AGPL source/binaries before building.
See docs/FEDORA_BUILD.md.
MSG
  exit 3
fi

if [[ -f scripts/prepare-dist.sh ]]; then
  bash scripts/prepare-dist.sh
elif [[ -f scripts/prepare-dist.ps1 ]]; then
  echo "Upstream only provides prepare-dist.ps1 at this revision." >&2
  echo "The OsiX Fedora port requires an equivalent staged src-dist tree." >&2
  [[ -d src-dist ]] || exit 4
fi

npx tauri build --bundles rpm,appimage
