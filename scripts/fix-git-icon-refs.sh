#!/bin/bash
# Remove macOS "Icon" files (Icon + carriage return) from .git that cause:
#   fatal: bad object refs/Icon?
#   error: ... did not send all necessary objects
# Run from repo root:  bash scripts/fix-git-icon-refs.sh

set -e
cd "$(git rev-parse --show-toplevel)/.git"

# Remove Icon and Icon\r files anywhere under .git
find . -type f \( -name $'Icon\r' -o -name 'Icon' \) -delete 2>/dev/null || true
# Remove any stray refs that are not valid (keep only 'main' in refs/heads, refs/tags, refs/remotes)
for dir in refs/heads refs/tags refs/remotes refs/remotes/origin; do
  [ -d "$dir" ] || continue
  for f in "$dir"/*; do
    [ -e "$f" ] || continue
    base=$(basename "$f")
    if [ "$base" != "main" ] && [ "$base" != "origin" ]; then
      rm -f "$f"
    fi
  done
done

echo "Done. Try: git pull --tags origin main"
