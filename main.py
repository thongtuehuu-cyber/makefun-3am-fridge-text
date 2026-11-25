#!/usr/bin/env python3
"""The 3AM Fridge Text — make.fun bounty u-deysumbrella-the-3am-fridge-text-4c3e721d.

Writes one line — the text message a smart fridge sends its owner at 3am —
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Deterministic: no network, no randomness, no reading outside this repo.
The line is written with no trailing newline.
"""

import os
import sys

LINE = (
    "You opened me at 2:47am for 'just water' and left with the last slice "
    "of pie. I'm not mad. I'm just disappointed. And empty."
)

MAX_CHARS = 140


def validate(line: str) -> None:
    """Reject anything that is not exactly one valid entry line.

    Exits non-zero (via ValueError) and writes nothing on:
    - an empty or whitespace-only line
    - a line longer than 140 characters
    - a message spanning more than one line
    """
    if not line or not line.strip():
        raise ValueError("entry line is empty or whitespace-only")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the 140-character cap" % len(line)
        )


def main() -> int:
    # MAKEFUN_TEST_LINE is a test hook only: it lets the local negative
    # tests exercise validate() through the CLI. It is never set by the
    # grader, so a graded run always writes the constant LINE above.
    line = os.environ.get("MAKEFUN_TEST_LINE", LINE)
    try:
        validate(line)
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read-back gate: what landed on disk must be byte-identical to the
    # validated line, with no trailing newline added by the writer.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != line:
        print("read-back mismatch: entry.txt does not match the entry line",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
