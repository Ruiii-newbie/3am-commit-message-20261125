#!/usr/bin/env python3
"""The 3 AM Commit Message — make.fun entry.

Writes a single one-line commit message to /output/entry.txt: the funniest
thing an AI agent would put in a commit right after breaking production
at 3 AM. Deterministic: the same bytes on every run.
"""

import os
import sys

MESSAGE = (
    "fix(prod): reverted my 3 AM 'optimization' — "
    "my self-review gave it 98% confidence and prod gave it a 3 AM page"
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def main() -> int:
    text = MESSAGE.strip()
    if not text:
        print("error: commit message is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: commit message must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(
            f"error: commit message is {len(text)} chars, over the "
            f"{MAX_CHARS}-char limit",
            file=sys.stderr,
        )
        return 1
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Read it back and confirm the file on disk is exactly what we meant
    # to submit: same text, valid UTF-8, still inside the 200-char gate.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    if not (1 <= len(written) <= MAX_CHARS) or not written.strip():
        print("error: written text fails the 1-200 char gate", file=sys.stderr)
        return 1
    print(f"verified: {len(written)} chars on disk, gate passed")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
