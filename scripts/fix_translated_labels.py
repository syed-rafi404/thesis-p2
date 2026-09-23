#!/usr/bin/env python
"""
=============================================================================
FINISH THE JOB THE TRANSLATOR LEFT: BANGLISH LABELS IN THE ENGLISH NOTES
=============================================================================
`--language english_via_banglish` writes each section in Banglish and then
translates it. The translation keeps the Markdown structure, which is what it
is asked to do, but that structure includes the Banglish section labels: every
one of the 13 files still carried between 8 and 13 of "Ek line e:",
"Mone rakho:" and "Extra jana kotha". A page billed as English showed Banglish
headings (RESULTS.md 5.4).

The labels are a small fixed set written by our own prompt, not free text from
the model, so they are mapped here rather than by asking the model again. No
model runs; nothing but these labels and the shouted summary line changes.

THE SHOUTED SUMMARY LINE
------------------------
Three files returned the one-line summary in capitals ("THE SECTIONS COVER THE
CONCEPT OF PYTHON VARIABLES..."). Lower-casing it wholesale would destroy
"Python", "TTL", "MTU" and "DBMS". Instead each word's casing is taken from how
that same word is written elsewhere in the same file, which is evidence from
the document rather than a guess, and anything with no evidence is lower-cased.

Usage:
    python scripts/fix_translated_labels.py --dry-run
    python scripts/fix_translated_labels.py --apply
=============================================================================
"""

import argparse
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_common as nc                                          # noqa: E402
import notes_page                                                  # noqa: E402

# Both spellings: the 13 scored lectures carry a tag ("..._7b.md"), the 30
# demonstration lectures are written by run_lecture.py with no tag at all.
PATTERN = "notes_annotated_english_via_banglish*.md"

# Longest first, so "Extra jana kotha (lecture e bola hoy ni)" is matched before
# the bare "Extra jana kotha".
LABELS = [
    ("Extra jana kotha (lecture e bola hoy ni)", "Background (not said in the lecture)"),
    ("Extra jana kotha", "Background (not said in the lecture)"),
    ("Nijeke jachai koro", "Check yourself"),
    ("Nijeke jachai", "Check yourself"),
    ("Ek line e", "In one line"),
    ("Mone rakho", "Remember"),
    ("Bujhe nao", "Understand"),
    ("Uttor", "Answers"),
]


def fix_labels(text):
    """Replace each Banglish label with its English wording. Returns (text, count)."""
    total = 0
    for banglish, english in LABELS:
        # Only where the label is used AS a label: at line start, after a
        # heading marker, a list bullet or bold marks, so the same words inside
        # a sentence or a quote are left alone. One label sat inside a list
        # item ("- **Extra jana kotha:**") and the bullet has to be allowed.
        pat = re.compile(r"(?m)^(\s*(?:[-*+]\s+|\d+\.\s+)?(?:#{1,6}\s*)?\**\s*)"
                         + re.escape(banglish) + r"\b")
        text, n = pat.subn(lambda m: m.group(1) + english, text)
        total += n
    return text, total


def casing_from_document(text, shouted_lines):
    """Evidence about each word from the rest of this file.

    Three buckets, because they need different treatment:
      acronyms  - written in capitals in ordinary text (TTL, MTU, DBMS, SQL)
      lowercase - ever written in lower case, so an ordinary word
      proper    - only ever written capitalised, so a name (Python)

    The shouted lines themselves are excluded, or every word in them would
    count as evidence that it is an acronym.
    """
    # Headings title-case ordinary words, and every sentence capitalises its
    # first word, so neither is evidence of a proper noun. Only a capital in
    # the middle of a sentence tells us anything.
    lines = [l for l in text.split("\n")
             if l not in shouted_lines and not l.lstrip().startswith("#")]
    acronyms, lower_n, capital_n = set(), collections.Counter(), collections.Counter()
    for line in lines:
        for m in re.finditer(r"[A-Za-z][A-Za-z0-9_'-]*", line):
            word = m.group(0)
            before = line[:m.start()].rstrip()
            sentence_start = not before or before[-1] in ".!?:;*>-|"
            if len(word) > 1 and word.upper() == word:
                acronyms.add(word)
            elif word[:1].islower():
                lower_n[word.lower()] += 1
            elif not sentence_start:
                capital_n[word] += 1
    # Whichever form the file uses more often wins. "Python" written ten times
    # as prose and once lowercase inside a code fence is still a proper noun,
    # which a plain "was it ever lowercase?" test would get wrong.
    proper, lowercase = {}, set()
    for word, n in capital_n.items():
        if n > lower_n.get(word.lower(), 0):
            proper[word.lower()] = word
    for word, n in lower_n.items():
        if word not in proper:
            lowercase.add(word)
    return acronyms, lowercase, proper


def unshout(line, evidence):
    """Undo an all-capitals line, using only what the rest of the file shows."""
    acronyms, lowercase, proper = evidence

    def one(m):
        word = m.group(0)
        if word in acronyms:                 # TTL, MTU, DBMS
            return word
        if word.lower() in lowercase:        # an ordinary word: cover, what, lists
            return word.lower()
        if word.lower() in proper:           # a name the file always capitalises
            return proper[word.lower()]
        return word.lower()

    out = re.sub(r"[A-Za-z][A-Za-z0-9_'-]*", one, line)
    return out[:1].upper() + out[1:]


def is_shouted(line):
    s = line.strip()
    return (len(s) > 25 and s.upper() == s and re.search(r"[A-Z]{6}", s)
            and not s.startswith("|"))


def fix_shouting(text):
    """Sentence-case any long all-capitals line. Returns (text, count)."""
    shouted = [l for l in text.split("\n") if is_shouted(l)]
    evidence = casing_from_document(text, set(shouted))
    out, n = [], 0
    for line in text.split("\n"):
        if is_shouted(line):
            indent = line[:len(line) - len(line.lstrip())]
            out.append(indent + unshout(line.strip(), evidence))
            n += 1
        else:
            out.append(line)
    return "\n".join(out), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the files (default: dry run)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    # The 13 scored lectures sit in their own run folders; the 30 demonstration
    # lectures are all under output/lectures. Both need the same treatment, and
    # scanning only the first left the demonstration pages in Banglish.
    dirs = [info["run_dir"] for info in nc.discover_lectures().values()]
    lectures = nc.REPO / "output" / "lectures"
    if lectures.is_dir():
        dirs += [d for d in sorted(lectures.iterdir()) if d.is_dir()]
    files = []
    for d in dirs:
        files += sorted(d.glob(PATTERN))
    if not files:
        sys.exit("no english_via_banglish notes found")

    labels = shouts = pages = 0
    for md in files:
        text = original = md.read_text(encoding="utf-8")
        text, n_lab = fix_labels(text)
        text, n_shout = fix_shouting(text)
        labels += n_lab
        shouts += n_shout
        mark = "" if text == original else "  <- changed"
        print(f"{md.parent.name:<16} labels {n_lab:>3}   shouted lines {n_shout}{mark}")
        if apply and text != original:
            md.write_text(text, encoding="utf-8")
            title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), md.stem)
            md.with_suffix(".html").write_text(
                notes_page.render(text, md.parent, title=title), encoding="utf-8")
            pages += 1

    print(f"\n{len(files)} files: {labels} labels, {shouts} shouted lines")
    print(f"{'rewrote ' + str(pages) + ' markdown files and their HTML' if apply else 'dry run, nothing written (pass --apply)'}")


if __name__ == "__main__":
    main()
