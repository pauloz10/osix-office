#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/work/euro-office-lite"
TARGET="${OSIX_TARGET:-x86_64-unknown-linux-gnu}"

[[ -d "$SRC" ]] || { echo "Missing source tree. Run make fetch first." >&2; exit 1; }

"$ROOT/scripts/00-doctor.sh"
cd "$SRC"

npm ci

# Follow the upstream Linux build sequence for the pinned Euro-Office revision.
# The editor sources are submodules under src/, not at the repository root.
if [[ -d src/sdkjs/build ]]; then
  pushd src/sdkjs/build >/dev/null
  npm ci
  npx grunt develop --desktop=true
  popd >/dev/null

  WORD_SCRIPTS="src/sdkjs/develop/sdkjs/word/scripts.js"
  if [[ -f "$WORD_SCRIPTS" ]] && ! grep -q 'word/document/editor\.js' "$WORD_SCRIPTS"; then
    sed -i 's/\];$/,\n\t"..\/..\/..\/..\/sdkjs\/word\/document\/editor.js"\n];/' "$WORD_SCRIPTS"
  fi
fi

# Fonts + AllFonts.js are required by x2t / DoctRenderer.
if [[ -x scripts/prepare-fonts.sh ]]; then
  python3 -m pip install --user Pillow >/dev/null 2>&1 || true
  bash scripts/prepare-fonts.sh
fi

# Ensure Linux icons exist for RPM/AppImage bundles.
if [[ -x scripts/generate-icons.sh ]]; then
  bash scripts/generate-icons.sh
fi

# Fetch the pinned upstream x2t dependency. Explicitly point the upstream helper
# at Euro-Office: in GitHub Actions GITHUB_REPOSITORY is otherwise pauloz10/osix-office.
if [[ -x scripts/get-x2t-ci.sh ]]; then
  GITHUB_REPOSITORY="delmarguillen/euro-office-lite" bash scripts/get-x2t-ci.sh "$TARGET"
elif [[ -x scripts/get-x2t.sh ]]; then
  GITHUB_REPOSITORY="delmarguillen/euro-office-lite" bash scripts/get-x2t.sh "$TARGET"
fi

SIDECAR="src-tauri/binaries/x2t-$TARGET"
[[ -f "$SIDECAR" ]] || {
  echo "OsiX build stopped: expected x2t sidecar missing: $SIDECAR" >&2
  exit 3
}
chmod +x "$SIDECAR"
cp -f "$SIDECAR" src-tauri/binaries/x2t
chmod +x src-tauri/binaries/x2t

# Prepare the DoctRenderer resources needed for PDF/export paths. These values
# match upstream's x86_64 Linux build for the pinned generic x2t dependency.
mkdir -p src-tauri/binaries/fonts
cp -f src/fonts/*.ttf src-tauri/binaries/fonts/ 2>/dev/null || true
cp -f src/sdkjs/common/AllFonts.js src-tauri/binaries/AllFonts.js 2>/dev/null || true

if [[ -x scripts/compile-doctrenderer-sdkjs.sh && -x scripts/prepare-doctrenderer.sh ]]; then
  export DOCTRENDERER_SDKJS_TAG="${DOCTRENDERER_SDKJS_TAG:-v8.2.0.147}"
  export DOCTRENDERER_SDKJS_REMOTE="${DOCTRENDERER_SDKJS_REMOTE:-origin}"
  export DOCTRENDERER_SDKJS_COMMIT="${DOCTRENDERER_SDKJS_COMMIT:-cfbea04cffefe72e1797ba4ed488771124d6e252}"
  export DOCTRENDERER_STAGING="${RUNNER_TEMP:-/tmp}/osix-doctrenderer-sdkjs"
  bash scripts/compile-doctrenderer-sdkjs.sh
  DOCTRENDERER_SDKJS="$DOCTRENDERER_STAGING" bash scripts/prepare-doctrenderer.sh
fi

# Stage the slim frontend tree using upstream's Linux-native script.
if [[ -x scripts/prepare-dist.sh ]]; then
  bash scripts/prepare-dist.sh
else
  echo "Pinned upstream is missing scripts/prepare-dist.sh" >&2
  exit 4
fi

# Validate x2t library resolution before spending time compiling Tauri.
if command -v ldd >/dev/null 2>&1; then
  LDD_OUT="$(LD_LIBRARY_PATH="$PWD/src-tauri/binaries" ldd "$SIDECAR" 2>/dev/null || true)"
  echo "$LDD_OUT"
  if grep -q "not found" <<<"$LDD_OUT"; then
    echo "Unresolved x2t shared libraries:" >&2
    grep "not found" <<<"$LDD_OUT" >&2
    exit 5
  fi
fi

# Fedora-first deliverables.
npx tauri build --target "$TARGET" --bundles rpm,appimage
