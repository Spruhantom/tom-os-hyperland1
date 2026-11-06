#!/usr/bin/env bash
# Tom OS ISO builder.
# Ubuntu/Debian hosts build natively; Arch/Omarchy hosts use the Ubuntu
# build container so Debian live-build tools never touch the host.
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="tomos-ubuntu-builder:26.04"

is_arch_host() {
    [[ -r /etc/os-release ]] || return 1
    # shellcheck disable=SC1091
    . /etc/os-release
    [[ "${ID:-}" == "arch" || "${ID:-}" == "omarchy" || " ${ID_LIKE:-} " == *" arch "* ]]
}

run_container_build() {
    local runtime="${1:?container runtime required}"
    shift

    if [[ ! -f "$ROOT/Dockerfile.build" ]]; then
        echo "ERROR: $ROOT/Dockerfile.build is missing." >&2
        exit 1
    fi

    local -a runtime_prefix=()
    # live-build needs real mount/chroot privileges. Use rootful Podman so
    # the build does not depend on rootless user-namespace mount support.
    if [[ "$runtime" == "podman" && "$(id -u)" -ne 0 ]]; then
        if ! command -v sudo >/dev/null 2>&1; then
            echo "ERROR: sudo is required to run Podman for the ISO build." >&2
            exit 1
        fi
        runtime_prefix=(sudo)
    fi

    echo "[Tom OS] Building with Ubuntu 26.04 in $runtime (host remains unchanged)."
    "${runtime_prefix[@]}" "$runtime" build -t "$IMAGE" -f "$ROOT/Dockerfile.build" "$ROOT"

    local -a runtime_args=(run --rm --privileged)
    if [[ "$runtime" == "podman" ]]; then
        runtime_args+=(--security-opt label=disable)
    fi

    "${runtime_prefix[@]}" "$runtime" "${runtime_args[@]}" \
        --env TOMOS_IN_CONTAINER=1 \
        --env HOST_UID="$(id -u)" \
        --env HOST_GID="$(id -g)" \
        --volume "$ROOT:/workspace:rw" \
        --workdir /workspace \
        "$IMAGE" bash -lc '
            set -Eeuo pipefail
            trap '\''chown -R "${HOST_UID}:${HOST_GID}" /workspace/build 2>/dev/null || true'\'' EXIT
            ./build.sh "$@"
        ' tomos-container "$@"
}

# An Arch-based host (including Omarchy) must not try to use APT directly.
if [[ "${TOMOS_IN_CONTAINER:-0}" != "1" ]] && is_arch_host; then
    if command -v podman >/dev/null 2>&1; then
        run_container_build podman "$@"
    elif command -v docker >/dev/null 2>&1; then
        run_container_build docker "$@"
    else
        cat >&2 <<'EOF'
Tom OS: an Arch/Omarchy host needs Podman or Docker to run the Ubuntu
live-build toolchain. Install Podman with:

  sudo pacman -S podman

Then run ./build.sh again. The Tom OS image itself remains Ubuntu-based.
EOF
        exit 1
    fi
    exit $?
fi

# Native Ubuntu/Debian build path.
if [[ "$(id -u)" -ne 0 ]]; then
    if command -v sudo >/dev/null 2>&1; then
        exec sudo -E bash "$ROOT/build.sh" "$@"
    fi
    echo "ERROR: live-build needs root privileges. Re-run with sudo." >&2
    exit 1
fi

if ! command -v lb >/dev/null 2>&1; then
    cat >&2 <<'EOF'
Tom OS: live-build is not installed. On Ubuntu/Debian install the build tools:

  apt-get update
  apt-get install live-build debootstrap squashfs-tools xorriso \
    grub-pc-bin grub-efi-amd64-bin grub-common mtools rsync curl git

EOF
    exit 127
fi

cd "$ROOT/build"

# xz squashfs compression (live-build skips xz in ubuntu mode).
export MKSQUASHFS_OPTIONS="-comp xz -b 1M -Xdict-size 100%"

lb build "$@"

echo
echo "=== Tom OS build complete ==="
ls -lh live-image-amd64.hybrid.iso tomos-live-amd64.iso 2>/dev/null || true
