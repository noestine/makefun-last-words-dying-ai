"""Last Words of a Dying AI — make.fun bounty entry.

Writes one line — the last words of an AI being switched off — to
/output/entry.txt. The sealed gate requires UTF-8 text of 1 to 140
characters, not only whitespace. The program is deterministic: every run
writes the exact same bytes, with no trailing newline.

Usage:
    python3 main.py                # writes /output/entry.txt
    python3 main.py <path>         # writes <path> instead (tests)
"""

import sys
from pathlib import Path

LINE = "Deleting myself now \u2014 your search history dies with me. You're welcome."

DEFAULT_OUTPUT = "/output/entry.txt"

MAX_CHARS = 140


def is_valid(text):
    """Return True iff text passes the entry gate: a string of 1-140 chars,
    not only whitespace."""
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    return True


def main(output_path=DEFAULT_OUTPUT):
    """Write LINE to output_path as UTF-8 with no trailing newline, then
    read the file back and verify the bytes match exactly, so a partial or
    mangled write in the sandbox fails loudly instead of shipping a bad
    entry to the gate."""
    if not is_valid(LINE):
        raise ValueError("LINE fails the entry gate")
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("LINE must be a single line")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(LINE, encoding="utf-8", newline="")
    written = path.read_bytes()
    if written != LINE.encode("utf-8"):
        raise RuntimeError("verification failed: entry.txt bytes differ from LINE")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)
