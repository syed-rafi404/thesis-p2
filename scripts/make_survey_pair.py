"""Build a blind pair of lecture notes for the reader study.

The survey asks people which note helps them more, so the two pages must differ only in
the thing being tested and must not say which is which. This renders two notes of the same
lecture to self-contained HTML, titles them "Note A" and "Note B", and strips anything in
the text that would give the answer away.

Whatever the pages are named on disk, the reader sees only A and B. Which one is which is
written to a small key file that is not meant to be shared with participants.

    python scripts/make_survey_pair.py --lecture BanglaASR7_004 ^
      --a notes_annotated_banglish_base.md --b notes_annotated_banglish_7b.md ^
      --label-a "off-the-shelf Whisper" --label-b "fine-tuned Whisper"
"""
import argparse
import json
import os
import random
import re
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
sys.path.insert(0, str(REPO / "scripts"))

from notes_page import render                                     # noqa: E402

SEARCH = ["output/live_focused/no_gaze/interval_10s", "output/speaker3_runs", "output/lectures"]

# Anything that would tell a reader which system produced the page.
TELLS = [
    (re.compile(r"(?i)\bfine[- ]tuned\b"), "the speech model"),
    (re.compile(r"(?i)\boff[- ]the[- ]shelf\b"), "the speech model"),
    (re.compile(r"(?i)\bbaseline\b"), "the system"),
    (re.compile(r"(?i)\bwhisper[\w.-]*\b"), "the speech model"),
    (re.compile(r"(?i)\bQwen[\w.:/-]*\b"), "the language model"),
    (re.compile(r"(?i)\bLoRA\b"), "adaptation"),
]


def find_lecture(name):
    for base in SEARCH:
        d = REPO / base / name
        if d.is_dir():
            return d
    raise SystemExit("lecture folder not found: %s" % name)


def deidentify(md):
    """Remove system names, so the page cannot be told apart by its own text."""
    out = md
    # The builder writes a "How these notes were made" footer naming the transcript file,
    # which identifies the condition outright. It goes first, whole line.
    out = re.sub(r"(?im)^.*How these notes were made.*$", "", out)
    out = re.sub(r"(?i)transcript_\w+\.txt", "the transcript", out)
    for pat, repl in TELLS:
        out = pat.sub(repl, out)
    # the generator's own provenance line in every figure caption
    out = re.sub(r"(?i);?\s*names by [^.*\n]+", "", out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lecture", required=True)
    ap.add_argument("--a", required=True, help="markdown file for one side")
    ap.add_argument("--b", required=True, help="markdown file for the other side")
    ap.add_argument("--label-a", default="A")
    ap.add_argument("--label-b", default="B")
    ap.add_argument("--shuffle", action="store_true",
                    help="randomly decide which file becomes Note A")
    ap.add_argument("--out", default=str(REPO / "output" / "survey"))
    args = ap.parse_args()

    d = find_lecture(args.lecture)
    pair = [(args.a, args.label_a), (args.b, args.label_b)]
    if args.shuffle:
        random.shuffle(pair)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    key = {"lecture": args.lecture, "folder": str(d), "shown_as": {}}

    for shown, (fname, label) in zip(["A", "B"], pair):
        src = d / fname
        if not src.exists():
            raise SystemExit("missing %s" % src)
        md = deidentify(src.read_text(encoding="utf-8"))
        md = "# Note %s\n\n" % shown + re.sub(r"\A#[^\n]*\n", "", md, count=1)
        page = render(md, d, title="Note %s" % shown)
        dest = out / ("note_%s.html" % shown)
        dest.write_text(page, encoding="utf-8")
        key["shown_as"]["Note " + shown] = {"file": fname, "condition": label}
        print("Note %-2s <- %-40s (%s)  %d KB"
              % (shown, fname, label, dest.stat().st_size // 1024))

    (out / "KEY_do_not_share.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print("\npages   %s" % out)
    print("key     %s  (which is which; keep this back from participants)"
          % (out / "KEY_do_not_share.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
