#!/usr/bin/env python3
"""Nailr - the worst app idea ever pitched.

Entry for the make.fun bounty
u-plucky-sparrow-67-the-worst-app-idea-ever-pitched-a0396b23
("The Worst App Idea Ever Pitched").

The program prints one sentence pitching the worst, most useless app
imaginable: a product that sounds real, a founder who sounds certain,
and a function nobody on earth needs.

Usage:
    python3 main.py            print the pitch
    python3 main.py --self-test
                               validate the pitch against the gate
                               (1-240 chars, single line, no leading or
                               trailing whitespace, no control characters)
"""

import sys

PITCH = (
    "Nailr photographs your fingernails every morning and charts "
    "their growth against the stock market, so you can diversify "
    "your cuticles."
)

MAX_CHARS = 240


def validate(text):
    """Check one text against the competition gate.

    Returns None when the text is valid, otherwise a short reason.
    """
    if not isinstance(text, str):
        return "not a string"
    if not 1 <= len(text) <= MAX_CHARS:
        return "length %d outside 1-%d" % (len(text), MAX_CHARS)
    if not text.strip():
        return "only whitespace"
    if text != text.strip():
        return "leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "not a single line"
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return "control character"
    text.encode("utf-8")
    return None


def self_test():
    """Validate the pitch and the gate boundaries. Returns exit code."""
    failures = []

    def check(name, text, expect_ok):
        err = validate(text)
        if (err is None) != expect_ok:
            failures.append(
                "%s: expected %s, got %s"
                % (name, "valid" if expect_ok else "invalid", err or "valid")
            )

    check("entry", PITCH, True)
    check("empty", "", False)
    check("whitespace-only", "   ", False)
    check("241 chars", "x" * 241, False)
    check("240 chars", "x" * 240, True)
    check("1 char", "x", True)
    check("multi-line", "a\nb", False)
    check("carriage return", "a\rb", False)
    check("leading space", " " + PITCH, False)
    check("trailing space", PITCH + " ", False)
    check("tab inside", "a\tb", False)

    if failures:
        for failure in failures:
            print("FAIL: " + failure, file=sys.stderr)
        return 1
    print("self-test: all checks passed")
    return 0


def main(argv):
    if len(argv) > 1:
        if argv[1] == "--self-test":
            return self_test()
        print("usage: %s [--self-test]" % argv[0], file=sys.stderr)
        return 2
    err = validate(PITCH)
    if err is not None:
        print("invalid pitch: " + err, file=sys.stderr)
        return 1
    print(PITCH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
