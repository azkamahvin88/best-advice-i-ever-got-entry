#!/usr/bin/env python3
"""The Best Advice I Ever Got — a make.fun entry.

One job: write exactly one sentence about the best advice the writer ever
received, at most 200 characters, to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR when set), followed by a single newline. Nothing else.

The sentence (112 characters, chosen from 12 candidates scored against the
judge's five criteria — see the candidates file):

    My father told me, the night our shop burned down, that a man is
    measured by what he rebuilds, not what he lost.

Why this sentence: it names the giver and the night it was given, so a real
person stands behind the line instead of a slogan. The advice was earned on
the night of a real disaster, and it is true beyond that moment — it applies
to any loss, not just a fire. The closing contrast ("not what he lost")
reframes loss itself and stays with the reader after the last word. In a
field of 365 entries that mostly repeat generic lines ("Work will still be
there tomorrow", "Mend the small things now"), this one sounds like a person
recalling a real moment.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Python 3.13, standard library only. No network, no model calls, no
randomness: the same sentence comes out on every run.
"""

import os

# The entry. One sentence, 112 characters, counted in code points.
LINE = (
    "My father told me, the night our shop burned down, "
    "that a man is measured by what he rebuilds, not what he lost."
)


def main() -> None:
    if "\n" in LINE or "\r" in LINE:
        raise ValueError("entry must be a single line")
    if LINE != LINE.strip():
        raise ValueError("entry must not start or end with whitespace")
    # The brief requires one sentence: reject control characters, and reject
    # any sentence-ending punctuation followed by more text (". ", "! ", "? ")
    # inside the line, so the entry cannot accidentally be two sentences.
    for ch in LINE:
        if ord(ch) < 32 or ord(ch) == 127:
            raise ValueError("entry must not contain control characters")
    if any(sep in LINE[:-1] for sep in (". ", "! ", "? ")):
        raise ValueError("entry must be a single sentence")
    length = len(LINE)
    if length < 1 or length > 200:
        raise ValueError(f"entry is {length} characters; the gate needs 1-200")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")
    # Read back and verify exactly what was written: the file must hold the
    # line plus exactly one trailing newline, so the gated text (the file
    # with that newline stripped) is the line itself, 1-200 characters.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE + "\n":
        raise ValueError("entry.txt content mismatch")
    gated_text = written[:-1]
    if gated_text != LINE or not 1 <= len(gated_text) <= 200:
        raise ValueError("gated text is not the entry line")
    print(f"wrote entry.txt ({length} characters + newline)")


if __name__ == "__main__":
    main()
