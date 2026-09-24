"""Add up the per-file counters the note builder writes, one file per lecture.

`build_lecture_notes.py` records, in the .json beside every notes page, how many lecturer
quotes it kept, how many it deleted because they were not word for word in the transcript,
how many it gave as a translation, how many it dropped as untranslatable, and how many
references to a box that does not exist survived. Those counters are what the thesis quotes
when it says the checks are counted rather than assumed.

A lecture folder can hold several builds of the same language (a rebuild carries a tag such
as `_final`), so this takes one file per lecture per language, preferring the tagged rebuild,
and prints the totals. Run it from the repo root:

    python scripts/count_note_counters.py
    python scripts/count_note_counters.py --scored-only     # the 13 lectures with answer keys
"""
import argparse
import collections
import glob
import json
import os

ROOTS = ["output/lectures/BanglaASR*/",
         "output/live_focused/no_gaze/interval_10s/*/",
         "output/speaker3_runs/*/"]
SCORED_ROOTS = ROOTS[1:]

LANGS = [("banglish", "notes_annotated_banglish*.json"),
         ("english_via_banglish", "notes_annotated_english_via_banglish*.json"),
         ("english", "notes_annotated_english_[!v]*.json")]

KEYS = ["quotes_kept", "quotes_dropped", "quotes_translated", "quotes_untranslated_dropped",
        "quotes_retranslated", "invalid_box_refs", "inline_quotes_unverified",
        "prompt_placeholders_removed"]


# Builds made only for the two-by-two of RESULTS.md 5.4 (off-the-shelf transcript, no board
# text). They are experiments, not the delivered notes, so they are left out of these totals.
ABLATION_TAGS = ("_base", "_noboard", "_base_noboard", "_32b")

# When a lecture has several deliverable builds, this is the order of preference.
PREFERRED_TAGS = ("_final", "_7b", "")


def one_per_lecture(paths):
    """One deliverable build per lecture: the rebuilt `_final` if there is one, else `_7b`."""
    def rank(path):
        name = os.path.basename(path)
        for i, tag in enumerate(PREFERRED_TAGS):
            if tag and name.endswith(tag + ".json"):
                return i
        return len(PREFERRED_TAGS)

    best = {}
    for p in sorted(paths):
        name = os.path.basename(p)
        if any(name.endswith(tag + ".json") for tag in ABLATION_TAGS):
            continue
        lec = os.path.basename(os.path.dirname(p))
        if lec not in best or rank(p) < rank(best[lec]):
            best[lec] = p
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scored-only", action="store_true",
                    help="only the lectures that have hand-verified board answer keys")
    args = ap.parse_args()
    roots = SCORED_ROOTS if args.scored_only else ROOTS

    for lang, pattern in LANGS:
        paths = []
        for root in roots:
            for p in glob.glob(root + pattern):
                name = os.path.basename(p)
                if lang == "banglish" and "english" in name:
                    continue
                paths.append(p)
        chosen = one_per_lecture(paths)
        if not chosen:
            continue
        total = collections.Counter()
        for path in chosen.values():
            try:
                data = json.load(open(path, encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for key, value in data.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    total[key] += value
        print(f"{lang}: {len(chosen)} lectures")
        for key in KEYS:
            if key in total:
                print(f"  {key:32s} {total[key]}")
        print()


if __name__ == "__main__":
    main()
