# Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## Fresh Machine Setup

Install the base prerequisites. These are needed for the shared shell, Git, and
tmux setup:

```bash
# Fedora
sudo dnf install -y bash curl git git-lfs gh openssh-clients tmux vim
```

Install `chezmoi` if it is not already available:

```bash
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b "$HOME/.local/bin"
```

Initialize and apply this repo:

```bash
chezmoi init <repo-url>
chezmoi diff
chezmoi apply
```

`chezmoi apply` also runs the repo's `run_once_after_*` bootstrap scripts the
first time they are seen on a machine. See [Automatic Bootstrap](#automatic-bootstrap).

## Tool Inventory

The managed config references these tools. Core tools should exist on every
machine; workstation tools are expected on marmoset and the Fedora minipc but
are guarded in `~/.bashrc` so `pongo` can run without them.

| Tool | Used by | Install/setup |
| --- | --- | --- |
| `bash` | `~/.bashrc`, `~/.bash_profile` | OS package manager |
| `curl` | chezmoi installer | OS package manager |
| `git` | chezmoi source, TPM/Bash-it bootstrap | OS package manager |
| `git-lfs` | `~/.gitconfig` LFS filter | `sudo dnf install git-lfs`; then `git lfs install` |
| `gh` | `~/.gitconfig` GitHub credential helper | `sudo dnf install gh`; then `gh auth login` |
| OpenSSH client | `~/.ssh/config` | `sudo dnf install openssh-clients` |
| `tmux` | `~/.tmux.conf` and TPM | OS package manager |
| `vim` | `GIT_EDITOR=vim` | `sudo dnf install vim` |
| Bash-it | interactive Bash prompt/modules | Installed by `run_once_after_20-install-bash-it.sh` |
| TPM | tmux plugin manager | Installed by `run_once_after_10-install-tpm.sh` |
| Python/virtualenv | Bash-it `python` and `virtualenv` modules | `sudo dnf install python3 python3-virtualenv` |
| pyenv | Bash-it `pyenv` module | Optional; install only where you use pyenv-managed Python |
| `btop` | `~/.config/btop/btop.conf` | `sudo dnf install btop` |
| `htop` | `~/.config/htop/htoprc` | `sudo dnf install htop` |
| Ghostty | `~/.config/ghostty/config.ghostty` | Install Ghostty on workstation machines |
| LM Studio | `~/.lmstudio/settings.json`, `~/.lmstudio/mcp.json`, `~/.bashrc` PATH guard | Install LM Studio on workstation machines; run its CLI installer if needed |
| Node/npm | opencode package dependencies, optional nvm setup | Install with nvm or OS package manager where opencode plugins are used |
| opencode | `~/.config/opencode/package*.json`, `~/.bashrc` PATH guard | Install opencode per upstream instructions; run `npm install` in `~/.config/opencode` if package deps are missing |
| Codex | `~/.codex/config.toml`, `skills/<skill-name>`, optional MCP/plugin config | Install/login separately with `codex login` |
| Claude Code | optional `~/scripts/claude_lm.sh` | Install/login separately; source the helper only when using LM Studio as backend |
| SDKMAN | optional `~/.sdkman` shell init | Install from SDKMAN if needed |
| nvm | optional `~/.nvm` shell init | Install from nvm if needed |
| Go | optional `~/go/bin` PATH | Install Go if needed |
| CUDA | optional `/usr/local/cuda` PATH/LD_LIBRARY_PATH | Install NVIDIA CUDA only on GPU workstations |
| local llama.cpp build | optional `~/Workspace/build-llama-cpp/...` PATH | Build locally only on machines that need it |

## Automatic Bootstrap

These are installed or refreshed by chezmoi run-once scripts:

```text
run_once_after_10-install-tpm.sh
run_once_after_20-install-bash-it.sh
```

`run_once_after_10-install-tpm.sh` requires `git` and `tmux`. It clones TPM into
`~/.tmux/plugins/tpm`, sources `~/.tmux.conf`, and installs the plugins declared
there:

```text
tmux-plugins/tpm
tmux-plugins/tmux-resurrect
tmux-plugins/tmux-continuum
```

`run_once_after_20-install-bash-it.sh` requires `git`. It clones Bash-it into
`~/.bash_it`, does not modify `~/.bashrc`, and enables the standard modules
listed below.

Run either script manually when you want to refresh those generated installs:

```bash
~/.local/share/chezmoi/run_once_after_10-install-tpm.sh
~/.local/share/chezmoi/run_once_after_20-install-bash-it.sh
```

## Secrets

Real secrets live in `~/.secrets` and are not committed.

```bash
cp ~/.local/share/chezmoi/.secrets.tmpl ~/.secrets
chmod 600 ~/.secrets
editor ~/.secrets
```

`~/.bashrc` sources `~/.secrets` with auto-export, so `NAME=value` entries become environment variables for child processes.

## Bash-it

This repo tracks the Bash config, not the Bash-it installation directory.

Chezmoi installs Bash-it with `run_once_after_20-install-bash-it.sh`. To refresh
it manually:

```bash
~/.local/share/chezmoi/run_once_after_20-install-bash-it.sh
```

Currently enabled Bash-it modules on the source machine:

```text
base plugin
python plugin
pyenv plugin
virtualenv plugin
general aliases
aliases completion
bash-it completion
system completion
```

## tmux

This repo treats TPM as a required dependency. Chezmoi installs TPM with
`run_once_after_10-install-tpm.sh`; to refresh it manually after applying
`~/.tmux.conf`:

```bash
~/.local/share/chezmoi/run_once_after_10-install-tpm.sh
```

Inside tmux, `prefix + I` also installs missing plugins.

Plugins declared in `~/.tmux.conf`:

```text
tmux-plugins/tpm
tmux-plugins/tmux-resurrect
tmux-plugins/tmux-continuum
```

## Workstation Tools

`~/.bashrc` is intentionally kept as one readable file. Workstation tools such
as LM Studio, opencode, CUDA, local llama.cpp builds, SDKMAN, nvm, and Go are
guarded so the same file can run on `pongo` when those tools are not installed.

Marmoset and the Fedora minipc should converge on:

```text
~/.lmstudio/settings.json
~/.lmstudio/mcp.json
~/.config/ghostty/config.ghostty
~/.config/opencode/package.json
~/.config/opencode/package-lock.json
```

Generated installs and state remain untracked:

```text
~/.opencode/node_modules
~/.config/opencode/node_modules
~/.lmstudio/.internal
~/.lmstudio/models
~/.lmstudio/conversations
```

Optional local-model helpers are kept under `~/scripts/` and are not loaded by
default. Source them only when needed:

```bash
source ~/scripts/claude_lm.sh
```

## Tool Login Flows

Auth-generated files are intentionally excluded. Recreate them through each tool's login flow:

```text
gcloud auth login
codex login
claude login
gemini login
clasp login, if needed
```

## Codex

This repo tracks only portable Codex preferences:

```text
~/.codex/config.toml
skills/**
```

The shared Codex config captures:

```text
default model and reasoning effort
TUI Vim mode default
enabled Codex plugins
future MCP server definitions
```

Do not track Codex auth, project trust paths, marketplace cache paths, bundled
plugin caches, system skills, logs, histories, shell snapshots, or SQLite state.
Those are generated per machine.

Currently enabled Codex plugins:

```text
github@openai-curated
chrome@openai-bundled
documents@openai-primary-runtime
spreadsheets@openai-primary-runtime
presentations@openai-primary-runtime
```

There are currently no Codex MCP servers configured. Add future MCP servers with
`codex mcp add ...`, then review and commit the resulting
`~/.codex/config.toml` change.

## Skills

External and tool-installed skills should be recorded in `skills/manifest.toml`.
Personally authored skills should live under `skills/<skill-name>/` in this
repo.

System-managed Codex skills and plugin caches are not tracked:

```text
~/.codex/skills/.system
~/.codex/plugins
~/.codex/cache
```

## Validation

Run these after applying:

```bash
bash -n ~/.bashrc
bash -n ~/.bash_profile
tmux source-file ~/.tmux.conf
chezmoi doctor
```

Before pushing changes, scan for secrets:

```bash
gitleaks detect
```

or:

```bash
trufflehog filesystem .
```
