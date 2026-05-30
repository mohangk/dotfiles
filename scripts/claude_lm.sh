# Claude against LM Studio's local OpenAI-compatible endpoint.
# Source manually when needed:
#   source ~/scripts/claude_lm.sh

if command -v claude >/dev/null 2>&1; then
    claude-lm() {
        export ANTHROPIC_BASE_URL=http://localhost:1234
        export ANTHROPIC_AUTH_TOKEN=lmstudio
        export CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY="2"
        export CLAUDE_CODE_NO_FLICKER="0"
        export ANTHROPIC_MODEL="gemma-4-26b-a4b"
        export CLAUDE_CODE_AUTO_COMPACT_WINDOW="48000"
        export CLAUDE_AUTOCOMPACT_PCT_OVERRIDE="90"
        export ANTHROPIC_DEFAULT_OPUS_MODEL="google/gemma-4-26b-a4b"
        export ANTHROPIC_DEFAULT_SONNET_MODEL="google/gemma-4-26b-a4b"
        export ANTHROPIC_DEFAULT_HAIKU_MODEL="google/gemma-4-26b-a4b"
        export CLAUDE_CODE_SUBAGENT_MODEL="google/gemma-4-26b-a4b"
        export API_TIMEOUT_MS="30000000"
        export BASH_DEFAULT_TIMEOUT_MS="2400000"
        export BASH_MAX_TIMEOUT_MS="2500000"
        export CLAUDE_CODE_MAX_OUTPUT_TOKENS="8000"
        export CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS="8000"
        export CLAUDE_CODE_ATTRIBUTION_HEADER="0"
        export CLAUDE_CODE_DISABLE_1M_CONTEXT="1"
        export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING="1"
        command claude "$@"
    }
fi
