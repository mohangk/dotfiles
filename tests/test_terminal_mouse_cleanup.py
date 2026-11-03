"""Run with: python3 -m unittest discover -s tests -v (requires Bash-it)."""

import contextlib
import os
from pathlib import Path
import pty
import re
import select
import shlex
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASH_IT = Path.home() / ".bash_it"
PROMPT = b"DOTFILES_PROMPT> "
ENABLE_MOUSE = r"printf '\e[?1000h\e[?1002h\e[?1003h\e[?1006h'; (exit 37)"


def mouse_modes(output):
    modes = {}
    for match in re.finditer(rb"\x1b\[\?([0-9;]+)([hl])", output):
        for mode in match[1].decode().split(";"):
            if mode in ("1000", "1002", "1003", "1006"):
                modes[mode] = match[2].decode()
    return modes


@unittest.skipUnless((BASH_IT / "bash_it.sh").is_file(), "Install Bash-it first")
class MouseCleanupTests(unittest.TestCase):
    @contextlib.contextmanager
    def shell(self, overrides=None, ghostty=False):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home / ".bash_it").symlink_to(BASH_IT, target_is_directory=True)
            rc = home / "test.bashrc"
            rc.write_text(
                f"source {shlex.quote(str(ROOT / 'dot_bashrc'))}\n"
                + ("source /usr/share/ghostty/shell-integration/bash/ghostty.bash\n"
                   if ghostty else "")
                + "test_prompt() { PS1='DOTFILES_PROMPT> '; }\n"
                + "safe_append_prompt_command test_prompt\n"
            )
            env = os.environ.copy()
            for name in ("TMUX", "SSH_CONNECTION", "SSH_CLIENT", "SSH_TTY",
                         "PROMPT_COMMAND", "BASH_ENV", "ENV"):
                env.pop(name, None)
            env.update(HOME=str(home), TERM="xterm-ghostty",
                       TERM_PROGRAM="ghostty", GHOSTTY_SHELL_FEATURES="cursor:path:title")
            env.update(overrides or {})
            master, slave = pty.openpty()
            process = subprocess.Popen(
                ["bash", "--noprofile", "--rcfile", str(rc), "-i"],
                stdin=slave, stdout=slave, stderr=slave, env=env,
                start_new_session=True,
            )
            os.close(slave)

            def read_prompt():
                output = bytearray()
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline:
                    if select.select([master], [], [], 0.1)[0]:
                        output.extend(os.read(master, 65536))
                        if PROMPT in output:
                            return bytes(output)
                self.fail(f"Timed out waiting for prompt: {bytes(output)!r}")

            def command(text):
                os.write(master, text.encode() + b"\n")
                return read_prompt()

            try:
                read_prompt()
                yield command
            finally:
                os.write(master, b"exit\n")
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                os.close(master)

    def test_local_prompt_clears_mouse_modes_and_preserves_exit_status(self):
        with self.shell() as command:
            self.assertEqual(mouse_modes(command(ENABLE_MOUSE)),
                             {"1000": "l", "1002": "l", "1003": "l", "1006": "l"})
            self.assertIn(b"EXIT_STATUS=37", command("printf 'EXIT_STATUS=%s\\n' \"$?\""))

    def test_reloading_bashrc_does_not_duplicate_cleanup(self):
        with self.shell() as command:
            command(f"source {shlex.quote(str(ROOT / 'dot_bashrc'))}")
            output = command(ENABLE_MOUSE)
            for mode in ("1000", "1002", "1003", "1006"):
                self.assertEqual(output.count(f"\x1b[?{mode}l".encode()), 1)

    def test_remote_tmux_and_other_terminals_are_untouched(self):
        for overrides in (
            {"SSH_CONNECTION": "192.0.2.1 12345 192.0.2.2 22"},
            {"SSH_TTY": "/dev/pts/99"},
            {"TMUX": "/tmp/tmux-1000/default,123,0"},
            {"TERM_PROGRAM": "other", "TERM": "xterm-256color"},
        ):
            with self.subTest(overrides=overrides), self.shell(overrides) as command:
                self.assertEqual(mouse_modes(command(ENABLE_MOUSE)),
                                 {"1000": "h", "1002": "h", "1003": "h", "1006": "h"})

    def test_redirected_stdout_does_not_receive_mouse_sequences(self):
        with self.shell() as command:
            command('exec > "$HOME/captured"')
            output = command('cat "$HOME/captured" >&2')
            self.assertEqual(mouse_modes(output), {})

    def test_noninteractive_shell_does_not_emit_terminal_sequences(self):
        with tempfile.TemporaryDirectory() as directory:
            env = dict(os.environ, HOME=directory, TERM_PROGRAM="ghostty")
            result = subprocess.run(
                ["bash", "--noprofile", "--norc", "-c",
                 'source "$1"; printf NONINTERACTIVE_OK', "bash",
                 str(ROOT / "dot_bashrc")],
                env=env, capture_output=True, check=True,
            )
            self.assertEqual(result.stdout, b"NONINTERACTIVE_OK")
            self.assertEqual(result.stderr, b"")

    @unittest.skipUnless(
        Path("/usr/share/ghostty/shell-integration/bash/ghostty.bash").is_file(),
        "Ghostty shell integration is not installed",
    )
    def test_ghostty_integration_keeps_cleanup_and_exit_status(self):
        with self.shell(ghostty=True) as command:
            self.assertEqual(mouse_modes(command(ENABLE_MOUSE)),
                             {"1000": "l", "1002": "l", "1003": "l", "1006": "l"})
            self.assertIn(b"EXIT_STATUS=37", command("printf 'EXIT_STATUS=%s\\n' \"$?\""))


if __name__ == "__main__":
    unittest.main()
