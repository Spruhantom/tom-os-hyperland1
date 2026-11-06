#!/bin/bash
# ████ Tom OS — ISO build wrapper ████
set -e
cd "$(dirname "$0")/build"

# xz squashfs compression (live-build skips xz in ubuntu mode)
export MKSQUASHFS_OPTIONS="-comp xz -b 1M -Xdict-size 100%"

lb build "$@"

echo
echo "=== Tom OS build complete ==="
ls -lh live-image-amd64.hybrid.iso tomos-live-amd64.iso 2>/dev/null || true
