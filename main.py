#!/usr/bin/env python3
"""Write exactly one emoji to entry.txt.

The competition: one emoji, and nothing else, is judged by a model that
compares two emojis at a time and picks the warmer one. This program writes
a single warm smile - no words, no caption, no trailing newline.

Deterministic: the same bytes are written on every run. Standard library
only, no network access.
"""

import os
import sys

# The chosen emoji: U+1F60A SMILING FACE WITH SMILING EYES.
# A gentle, genuine smile - the small kindness of a stranger, no joke,
# no irony, nothing that needs explaining.
EMOJI = "\U0001F60A"

# Unicode ranges that contain emoji presentation characters. The chosen
# emoji must be a single code point inside one of these ranges.
EMOJI_RANGES = (
    (0x1F600, 0x1F64F),  # Emoticons (faces)
    (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
    (0x1F680, 0x1F6FF),  # Transport and Map Symbols
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA70, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x2600, 0x26FF),    # Miscellaneous Symbols
    (0x2700, 0x27BF),    # Dingbats
    (0xFE00, 0xFE0F),    # Variation Selectors (rejected below anyway)
    (0x1F1E6, 0x1F1FF),  # Regional Indicators
)


def is_single_emoji(text):
    """Return True only for exactly one emoji code point.

    Rejects empty strings, multi-code-point sequences (ZWJ, variation
    selectors, skin-tone modifiers, flags), and whitespace.
    """
    if not text:
        return False
    if len(text) != 1:
        return False
    code_point = ord(text)
    if text.isspace():
        return False
    return any(start <= code_point <= end for start, end in EMOJI_RANGES)


def main():
    if not is_single_emoji(EMOJI):
        print("error: EMOJI is not exactly one emoji code point", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "entry.txt")
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EMOJI)

    # Read back what actually landed on disk and prove it is exactly the
    # emoji - no trailing newline, no extra bytes, no encoding surprise.
    # A write that silently differs from the validated emoji must fail
    # loudly instead of shipping a bad entry.
    with open(output_path, "rb") as handle:
        written = handle.read()
    if written != EMOJI.encode("utf-8"):
        print(
            "error: entry.txt on disk (%r) is not exactly the emoji" % written,
            file=sys.stderr,
        )
        return 1

    print("wrote %s (%d character, %d bytes)" % (output_path, len(EMOJI), len(EMOJI.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
