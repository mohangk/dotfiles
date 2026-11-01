# Agent instructions

## Version checks

- When changing a dotfiles-managed tool, plugin, or dependency, check the installed version and whether a newer compatible release exists.
- Verify the package's declared compatibility with the installed tool before upgrading. Pin the version in tracked config instead of using a floating `@latest`.
- Revisit existing pins when touching the related config, and validate upgrades with the tool's doctor/status command plus a quick smoke test where practical.
