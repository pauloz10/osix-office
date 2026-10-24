#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f /etc/fedora-release ]]; then
  echo "This script is intended for Fedora Linux 44 or newer." >&2
  exit 1
fi

sudo dnf -y install   git curl wget file python3 python3-pip   nodejs npm rust cargo   gcc gcc-c++ make cmake ninja-build pkgconf-pkg-config   webkit2gtk4.1-devel openssl-devel   libappindicator-gtk3-devel librsvg2-devel libxdo-devel   gtk3-devel glib2-devel libsoup3-devel   rpm-build rpmdevtools patchelf desktop-file-utils   libarchive unzip zip jq

echo "Fedora/Tauri prerequisites installed."
