#!/bin/bash
# ████ Tom OS — assemble the hybrid BIOS+UEFI ISO from build/binary ████
# live-build 3.x on Ubuntu only produces BIOS-only (genisoimage) images, so the
# bootable image is made with grub-mkrescue (xorriso): El Torito BIOS + EFI
# System Partition + isohybrid MBR/GPT. Works with dd, Ventoy, Rufus, QEMU/OVMF.
# Host deps: grub-pc-bin grub-efi-amd64-bin grub-common xorriso mtools
set -euo pipefail
cd "$(dirname "$0")"
B=build/binary
OUT=${1:-tomos-26.10-amd64.iso}
test -f $B/live/filesystem.squashfs
K=$(ls $B/live/vmlinuz-* | sort -V | tail -1); I=$(ls $B/live/initrd.img-* | sort -V | tail -1)
ln -f "$K" $B/live/vmlinuz; ln -f "$I" $B/live/initrd.img
touch $B/live/tomos.marker
mkdir -p $B/boot/grub/fonts
install -m644 iso/grub.cfg iso/loopback.cfg $B/boot/grub/
install -m644 assets/grub-background.png $B/boot/grub/tomos.png
install -m644 /usr/share/grub/unicode.pf2 $B/boot/grub/fonts/
printf 'Tom OS 26.10 "Neon Punk" - amd64 (%s)\n' "$(date -u +%Y%m%d)" > $B/.disk-info 2>/dev/null || true
grub-mkrescue -o "$OUT" $B -- -volid TOMOS_2610 -joliet on 2>&1 | grep -v "^xorriso : UPDATE" || true
test -s "$OUT"
sha256sum "$OUT" > "$OUT.sha256"
ls -lh "$OUT"
