#!/usr/bin/env bash
set -euo pipefail

for command in git tmux; do
    if ! command -v "${command}" >/dev/null 2>&1; then
        echo "Missing required command: ${command}" >&2
        exit 1
    fi
done

tmux_conf="${HOME}/.tmux.conf"
plugins_dir="${HOME}/.tmux/plugins"
tpm_dir="${HOME}/.tmux/plugins/tpm"
session_name="chezmoi-tpm-install-$$"
created_session=0

if [ ! -f "${tmux_conf}" ]; then
    echo "Missing ${tmux_conf}; apply dot_tmux.conf before installing TPM plugins." >&2
    exit 1
fi

mkdir -p "${plugins_dir}"

if [ -e "${tpm_dir}" ] && [ ! -d "${tpm_dir}/.git" ]; then
    echo "${tpm_dir} exists but is not a git checkout; move it aside and retry." >&2
    exit 1
fi

if [ ! -d "${tpm_dir}/.git" ]; then
    git clone https://github.com/tmux-plugins/tpm "${tpm_dir}"
fi

cleanup() {
    if [ "${created_session}" -eq 1 ]; then
        tmux kill-session -t "${session_name}" >/dev/null 2>&1 || true
    fi
}
trap cleanup EXIT

if [ -z "${TMUX:-}" ] && ! tmux has-session >/dev/null 2>&1; then
    tmux new-session -d -s "${session_name}"
    created_session=1
fi

tmux source-file "${tmux_conf}"
"${tpm_dir}/bin/install_plugins"
