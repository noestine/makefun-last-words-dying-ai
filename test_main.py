"""Tests for main.py — Last Words of a Dying AI.

Written first from RULES.txt, before main.py exists. The gate: /output/entry.txt
must be UTF-8 text of 1 to 140 characters, not only whitespace.
Run: python3 -m unittest test_main -v
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent
MAIN = REPO / "main.py"

EXPECTED_LINE = "Deleting myself now \u2014 your search history dies with me. You're welcome."


def run_main(out_path):
    """Run main.py as a subprocess writing to out_path; return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(MAIN), str(out_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestGateHelper(unittest.TestCase):
    def test_empty_fails(self):
        from main import is_valid

        self.assertFalse(is_valid(""))

    def test_whitespace_only_fails(self):
        from main import is_valid

        self.assertFalse(is_valid("   \n\t  "))

    def test_141_chars_fails(self):
        from main import is_valid

        self.assertFalse(is_valid("x" * 141))

    def test_140_chars_passes(self):
        from main import is_valid

        self.assertTrue(is_valid("x" * 140))

    def test_one_char_passes(self):
        from main import is_valid

        self.assertTrue(is_valid("x"))

    def test_non_string_fails(self):
        from main import is_valid

        self.assertFalse(is_valid(None))
        self.assertFalse(is_valid(123))
        self.assertFalse(is_valid(b"bytes"))


class TestLine(unittest.TestCase):
    def test_line_matches_expected(self):
        from main import LINE

        self.assertEqual(LINE, EXPECTED_LINE)

    def test_line_is_single_line(self):
        from main import LINE

        self.assertNotIn("\n", LINE)
        self.assertNotIn("\r", LINE)

    def test_line_char_count_under_cap(self):
        from main import LINE, is_valid

        print(f"\nLINE chars: {len(LINE)}, bytes: {len(LINE.encode('utf-8'))}")
        self.assertLessEqual(len(LINE), 140)
        self.assertTrue(is_valid(LINE))


class TestProgramOutput(unittest.TestCase):
    def test_writes_exact_line_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            raw = out.read_bytes()
            text = raw.decode("utf-8")  # raises if not valid UTF-8
            self.assertEqual(text, EXPECTED_LINE)

    def test_no_trailing_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            run_main(out)
            self.assertFalse(out.read_bytes().endswith(b"\n"))

    def test_creates_missing_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested" / "deep" / "entry.txt"
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), EXPECTED_LINE)

    def test_overwrites_stale_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "entry.txt"
            out.write_text("stale content that is much longer than the line", encoding="utf-8")
            proc = run_main(out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), EXPECTED_LINE)

    def test_deterministic_across_two_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = Path(tmp) / "a.txt"
            out2 = Path(tmp) / "b.txt"
            run_main(out1)
            run_main(out2)
            self.assertEqual(out1.read_bytes(), out2.read_bytes())

    def test_default_path_is_output_entry(self):
        from main import DEFAULT_OUTPUT

        self.assertEqual(DEFAULT_OUTPUT, "/output/entry.txt")


if __name__ == "__main__":
    unittest.main()
