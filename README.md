# Dotfiles

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## Fresh Machine Setup

Install the base prerequisites:

```bash
# Fedora
sudo dnf install -y git tmux bash curl
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

Install Bash-it:

```bash
git clone --depth=1 https://github.com/Bash-it/bash-it.git ~/.bash_it
~/.bash_it/install.sh --silent
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
`run_once_after_10-install-tpm.sh`; to install or refresh it manually after
applying `~/.tmux.conf`:

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

## Tool Login Flows

Auth-generated files are intentionally excluded. Recreate them through each tool's login flow:

```text
gcloud auth login
codex login
claude login
gemini login
clasp login, if needed
```

## Skills

External and tool-installed skills should be recorded in `skills/manifest.toml`.
Personally authored skills should live under `skills/personal/<skill-name>/`.

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
