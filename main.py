#!/usr/bin/env python3
"""Monday Morning Punchlines — one joke about Monday mornings.

Writes a single original joke line to /output/entry.txt and verifies
the file holds exactly that line: one line, ASCII, 1-200 characters.
"""

import sys
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 200


def build_joke() -> str:
    """Compose the entry line.

    The joke is a self-referential loop: a polite request to Monday
    gets bounced to Friday, whose out-of-office reply sends it straight
    back to Monday. The punchline lands in the last words.
    """
    parts = [
        "I asked Monday to be gentle.",
        "It forwarded my request to Friday,",
        "which replied: 'Out of office until Monday.'",
    ]
    return " ".join(parts)


def find_problems(text: str) -> list[str]:
    """Return every gate failure for a candidate line (empty = valid).

    Mirrors the competition's sealed scorer: UTF-8/ASCII text, 1-200
    characters, not only whitespace, exactly one line.
    """
    problems: list[str] = []
    if not text.strip():
        problems.append("joke is empty or only whitespace")
    if len(text) > MAX_CHARS:
        problems.append(f"joke is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        problems.append("joke must be a single line")
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        problems.append("joke is not plain ASCII")
    return problems


def write_entry(text: str) -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text + "\n", encoding="ascii")
    return OUTPUT_PATH


def verify_entry(path: Path, expected: str) -> list[str]:
    """Read the file back and check it holds exactly the expected line."""
    problems: list[str] = []
    try:
        written = path.read_text(encoding="ascii")
    except OSError as exc:
        return [f"could not read back {path}: {exc}"]
    lines = written.splitlines()
    if len(lines) != 1:
        problems.append(f"expected 1 line, got {len(lines)}")
    elif lines[0] != expected:
        problems.append("written line differs from the joke")
    if lines and len(lines[0]) > MAX_CHARS:
        problems.append(f"written line is {len(lines[0])} chars")
    return problems


def main() -> int:
    joke = build_joke().strip()

    problems = find_problems(joke)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    path = write_entry(joke)

    problems = verify_entry(path, joke)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    byte_count = len(joke.encode("ascii"))
    print(f"wrote {len(joke)} chars ({byte_count} bytes) to {path}")
    print(joke)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
