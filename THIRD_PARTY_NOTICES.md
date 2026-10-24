# Third-party notices

OsiX Office is designed as a derivative/open-source integration around Euro-Office components.

## Euro-Office Lite

- Upstream: `delmarguillen/euro-office-lite`
- Pinned baseline: `v0.17.39-alpha`, commit prefix `5c4e5fa`
- Licence: AGPL-3.0

## Euro-Office editor components

The upstream application uses Euro-Office `sdkjs` and `web-apps` editor components as submodules. These remain separately attributable to their upstream authors and contributors under their published open-source licences.

## x2t converter

Euro-Office Lite uses the x2t document-conversion sidecar. OsiX requires the matching open-source provenance/source revision to be recorded before release. The build scripts deliberately stop rather than silently downloading an unpinned converter binary.

## LibreOffice

LibreOffice is not copied into OsiX. If installed by the user, it may later be invoked as a separate optional compatibility process. Its own licences and notices remain independent.

## Microsoft and WPS

No proprietary Microsoft Office or WPS Office program source, binaries, artwork, icons or reverse-engineered implementation code are included in OsiX. Microsoft-published format documentation may be used for interoperability.
