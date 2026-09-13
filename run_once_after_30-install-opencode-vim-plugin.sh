#!/usr/bin/env bash
set -euo pipefail

# The vim plugin is optional workstation tooling; skip silently on machines
# where opencode is not installed (for example pongo).
if ! command -v opencode >/dev/null 2>&1; then
    echo "opencode not found; skipping vim plugin install"
    exit 0
fi

opencode plugin @leohenon/opencode-vim-plugin --global
