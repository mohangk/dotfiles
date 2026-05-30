#!/usr/bin/env bash
set -euo pipefail

if ! command -v git >/dev/null 2>&1; then
    echo "Missing required command: git" >&2
    exit 1
fi

bash_it_dir="${HOME}/.bash_it"

if [ -e "${bash_it_dir}" ] && [ ! -d "${bash_it_dir}/.git" ]; then
    echo "${bash_it_dir} exists but is not a git checkout; move it aside and retry." >&2
    exit 1
fi

if [ ! -d "${bash_it_dir}/.git" ]; then
    git clone --depth=1 https://github.com/Bash-it/bash-it.git "${bash_it_dir}"
fi

"${bash_it_dir}/install.sh" --silent --no-modify-config

# Keep the shared interactive shell consistent across machines.
BASH_IT="${bash_it_dir}" bash -lc '
    source "$BASH_IT/bash_it.sh"
    bash-it disable alias directory editor
    bash-it enable plugin base python pyenv virtualenv
    bash-it enable alias general
    bash-it enable completion aliases bash-it system
'
