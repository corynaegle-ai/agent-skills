#!/usr/bin/env bash
set -euo pipefail

# Install selected skills without replacing existing files or symlinks.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$REPO/scripts/install-skills.py" "$@"
