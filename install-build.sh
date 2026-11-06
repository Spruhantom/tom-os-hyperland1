#!/usr/bin/env bash
# Online bootstrapper for building Tom OS from Arch Linux / Omarchy.
# Usage: curl -fsSL https://raw.githubusercontent.com/Spruhantom/tom-os-hyperland1/main/install-build.sh | bash
set -Eeuo pipefail

REPO_URL="https://github.com/Spruhantom/tom-os-hyperland1.git"
DEST="${TOMOS_DIR:-"$HOME/tom-os-hyperland1"}"

if [[ ! -r /etc/os-release ]]; then
    echo "ERROR: Cannot identify this Linux distribution." >&2
    exit 1
fi
# shellcheck disable=SC1091
. /etc/os-release
if [[ "${ID:-}" != "arch" && "${ID:-}" != "omarchy" && " ${ID_LIKE:-} " != *" arch "* ]]; then
    echo "ERROR: This online bootstrap command currently supports Arch Linux and Omarchy." >&2
    echo "On Ubuntu/Debian, clone the repository and follow its README instead." >&2
    exit 1
fi

if [[ "$(id -u)" -eq 0 ]]; then
    SUDO=""
elif command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
else
    echo "ERROR: sudo is required to install the build dependencies." >&2
    exit 1
fi

echo "[Tom OS] Installing host build tools..."
if [[ -n "$SUDO" ]]; then
    "$SUDO" pacman -Syu --needed --noconfirm podman git grub xorriso mtools
else
    pacman -Sy --needed --noconfirm podman git grub xorriso mtools
fi

if [[ -e "$DEST" ]]; then
    if [[ ! -d "$DEST/.git" ]]; then
        echo "ERROR: $DEST already exists and is not a Git checkout." >&2
        echo "Move it or set TOMOS_DIR to another directory, then retry." >&2
        exit 1
    fi
    CURRENT_ORIGIN="$(git -C "$DEST" remote get-url origin 2>/dev/null || true)"
    if [[ "$CURRENT_ORIGIN" != "$REPO_URL" && "$CURRENT_ORIGIN" != "https://github.com/Spruhantom/tom-os-hyperland1" ]]; then
        echo "ERROR: $DEST is a Git checkout of a different repository." >&2
        echo "Set TOMOS_DIR to a new directory, then retry." >&2
        exit 1
    fi
    if [[ -n "$(git -C "$DEST" status --porcelain)" ]]; then
        echo "ERROR: $DEST has uncommitted changes. Commit or stash them before updating." >&2
        exit 1
    fi
    echo "[Tom OS] Updating existing checkout..."
    git -C "$DEST" pull --ff-only origin main
else
    echo "[Tom OS] Downloading the Tom OS source..."
    git clone --branch main --depth 1 "$REPO_URL" "$DEST"
fi

cd "$DEST"
chmod +x build.sh make-iso.sh
echo "[Tom OS] Starting the Ubuntu 26.04 container build..."
./build.sh

echo "[Tom OS] Assembling the hybrid BIOS/UEFI ISO..."
./make-iso.sh "$DEST/tomos-26.10-amd64.iso"

echo
echo "Tom OS build finished."
echo "ISO: $DEST/tomos-26.10-amd64.iso"
echo "Checksum: $DEST/tomos-26.10-amd64.iso.sha256"
