# Fedora build

## Supported baseline

The first native package target is Fedora 44 x86_64. Fedora 45 testing will be added after its final release. Tauri v2 requires WebKitGTK 4.1 on Linux; Fedora provides `webkit2gtk4.1-devel`.

## Normal connected build

```bash
./scripts/01-fedora-prereqs.sh
make fetch
make customize
make test
make build
make package
```

The final files are copied to `dist/`.

## Air-gapped/restricted builder

The installed OsiX application is offline. A source build normally needs network access to obtain source and language/tool dependencies. To build in a restricted environment, mirror those dependencies first.

OsiX supports a locally supplied upstream tree:

```bash
OSIX_UPSTREAM_DIR=/path/to/euro-office-lite make fetch
```

or a source archive:

```bash
OSIX_UPSTREAM_ARCHIVE=/path/to/euro-office-lite-v0.17.39-alpha.tar.gz make fetch
```

Then run `make customize` and `make build`.

## x2t converter

Euro-Office Lite uses the `x2t` sidecar for conversion between OOXML and the editor's internal representation. The pinned upstream release currently obtains converter binaries from its dependency release workflow. OsiX will not silently fetch an unpinned binary during a reproducible build. The matching sidecars must be placed in `work/euro-office-lite/src-tauri/binaries/`, with corresponding AGPL source/provenance retained in release notices.

## Expected output

```text
dist/OsiX-Office_<version>_x86_64.rpm
dist/OsiX-Office_<version>_amd64.AppImage
```

Exact Tauri file naming may vary slightly; `scripts/06-collect-artifacts.sh` collects both formats.
