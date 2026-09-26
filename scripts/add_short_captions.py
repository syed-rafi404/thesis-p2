"""Give every long caption a short form for the List of Figures and Tables.

A caption explains the figure to a reader who is looking at it, so it can be several
sentences. The List of Figures is an index, and a 986 character entry there is not an
index entry, it is the caption printed twice. LaTeX takes the short form from the
optional argument: \\caption[short]{long}.

The short form is the caption's first sentence, cut at a word boundary if it is still
long. Captions that are already short, or that already carry an optional argument, are
left alone.

    python scripts/add_short_captions.py "Thesis Defense P3/drafts/thesis"
"""
import glob
import io
import os
import re
import sys

LIMIT = 105          # anything longer than this gets a short form
SHORT_MAX = 92       # and the short form is cut to about this


def find_captions(text):
    """Yield (start, end, inner) for each \\caption{...} with balanced braces."""
    for m in re.finditer(r"\\caption(\[)?\{", text):
        if m.group(1):                      # already has an optional argument
            continue
        i = m.end() - 1                     # at the opening brace
        depth, j = 0, i
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        yield m.start(), j + 1, text[i + 1:j]


def shorten(caption):
    flat = " ".join(caption.split())
    # first sentence, but do not split on a decimal point or an initial
    m = re.search(r"(?<![0-9A-Z])\.(?:\s|$)", flat)
    short = flat[:m.start()] if m else flat
    # strip markup that does not belong in a list entry
    short = re.sub(r"\\cite\{[^}]*\}", "", short)
    short = re.sub(r"\\ref\{[^}]*\}", "", short)
    short = re.sub(r"\\(textbf|textit|emph|texttt)\{([^}]*)\}", r"\2", short)
    short = " ".join(short.split()).rstrip(" ,;:")
    if len(short) > SHORT_MAX:
        cut = short[:SHORT_MAX].rsplit(" ", 1)[0]
        short = cut.rstrip(" ,;:")
    return short


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(root, "chapters", "*.tex")) +
                   glob.glob(os.path.join(root, "appendix", "*.tex")))
    total = 0
    for f in files:
        text = io.open(f, encoding="utf-8").read()
        edits = []
        for start, end, inner in find_captions(text):
            if len(" ".join(inner.split())) <= LIMIT:
                continue
            short = shorten(inner)
            if not short:
                continue
            edits.append((start, end, "\\caption[%s]{%s}" % (short, inner)))
        for start, end, new in reversed(edits):
            text = text[:start] + new + text[end:]
        if edits:
            io.open(f, "w", encoding="utf-8").write(text)
            print("%-28s %d captions shortened" % (os.path.basename(f), len(edits)))
            total += len(edits)
    print("total:", total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
