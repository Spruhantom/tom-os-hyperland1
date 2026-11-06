#!/usr/bin/env bash
# ████ Tom OS — assemble the hybrid BIOS+UEFI ISO from build/binary ████
# live-build 3.x on Ubuntu only produces BIOS-only (genisoimage) images, so the
# bootable image is made with grub-mkrescue (xorriso): El Torito BIOS + EFI
# System Partition + isohybrid MBR/GPT. Works with dd, Ventoy, Rufus, QEMU/OVMF.
# Host deps: grub-pc-bin grub-efi-amd64-bin grub-common xorriso mtools
set -Eeuo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
B="$ROOT/build/binary"
OUT="${1:-$ROOT/tomos-26.10-amd64.iso}"

if [[ ! -f "$B/live/filesystem.squashfs" ]]; then
    echo "ERROR: $B/live/filesystem.squashfs is missing. Run ./build.sh successfully first." >&2
    exit 1
fi

shopt -s nullglob
kernels=("$B"/live/vmlinuz-*)
initrds=("$B"/live/initrd.img-*)
shopt -u nullglob

if (( ${#kernels[@]} == 0 || ${#initrds[@]} == 0 )); then
    echo "ERROR: Could not find both a kernel and initrd in $B/live." >&2
    exit 1
fi

K="$(printf '%s\n' "${kernels[@]}" | sort -V | tail -n 1)"
I="$(printf '%s\n' "${initrds[@]}" | sort -V | tail -n 1)"

ln -f "$K" "$B/live/vmlinuz"
ln -f "$I" "$B/live/initrd.img"
touch "$B/live/tomos.marker"
mkdir -p "$B/boot/grub/fonts" "$(dirname -- "$OUT")"

for required in "$ROOT/iso/grub.cfg" "$ROOT/iso/loopback.cfg" "$ROOT/assets/grub-background.png" /usr/share/grub/unicode.pf2; do
    if [[ ! -f "$required" ]]; then
        echo "ERROR: Required ISO asset is missing: $required" >&2
        exit 1
    fi
done

install -m 644 "$ROOT/iso/grub.cfg" "$ROOT/iso/loopback.cfg" "$B/boot/grub/"
install -m 644 "$ROOT/assets/grub-background.png" "$B/boot/grub/tomos.png"
install -m 644 /usr/share/grub/unicode.pf2 "$B/boot/grub/fonts/"

printf 'Tom OS 26.10 "Neon Punk" - amd64 (%s)\n' "$(date -u +%Y%m%d)" > "$B/.disk-info"

# Do not mask grub-mkrescue failures: the old pipeline's 