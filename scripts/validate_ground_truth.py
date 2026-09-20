#!/usr/bin/env python
"""
=============================================================================
GROUND TRUTH VALIDATOR
=============================================================================
Checks transcript files against TRANSCRIPTION_GUIDE.md before they become
training data. Run it the moment a transcriber hands a file in: every problem
caught here is label noise that would otherwise be baked into the fine-tune
and be very hard to find afterwards.

Checks performed
----------------
ERRORS   (must fix, the file is not usable as-is)
  * timestamp format is not exactly [M:SS-M:SS]
  * segment longer than 30s, which Whisper cannot see in one window
  * overlapping segments, or end time before start time
  * Bengali script characters
  * empty segment text

WARNINGS (should fix)
  * missing or unknown Speaker ID in the header, needed for a speaker-
    independent split
  * gap between the end of one segment and the start of the next
  * non-ASCII characters, typically smart quotes from Word or Google Docs
  * spellings that contradict the guide's canonical word list
  * Bengali endings glued to English words, e.g. "functionta" for "function ta"
  * unusually low or high speaking rate, which usually means missing speech
  * very few fillers, which usually means the transcriber cleaned them out

Usage
-----
    python scripts/validate_ground_truth.py
    python scripts/validate_ground_truth.py --dir data/ground_truth
    python scripts/validate_ground_truth.py --file new_lecture.txt
    python scripts/validate_ground_truth.py --fix     # safe repairs only

`--fix` only rewrites things that cannot change meaning: smart quotes to
ASCII, stray spaces inside timestamp brackets, trailing whitespace. It never
touches spelling or segmentation, and it writes a .bak copy first.

Exit code is 1 when any file has an error, so this can gate a commit hook.
=============================================================================
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

MAX_SEGMENT_S = 30.0
WARN_SEGMENT_S = 25.0
MIN_WPM, MAX_WPM = 60, 220
MIN_FILLER_RATE = 0.015          # fillers per word seen in the existing files

TS_STRICT = re.compile(r"^\[(\d{1,2}):([0-5]\d)-(\d{1,2}):([0-5]\d)\]")
TS_LOOSE = re.compile(r"^\[\s*(\d{1,2})\s*:\s*(\d{1,2})\s*[-–—]\s*(\d{1,2})\s*:\s*(\d{1,2})\s*\]")

SMART = {"‘": "'", "’": "'", "“": '"', "”": '"',
         "–": "-", "—": "-", "…": "...", " ": " "}

# Canonical spellings from TRANSCRIPTION_GUIDE.md section 4.1
CANONICAL = {
    "amr": "ami", "aami": "ami", "aamra": "amra", "amraa": "amra",
    "etaa": "eta", "seta": "sheta", "shetaa": "sheta",
    "ektaa": "ekta", "akta": "ekta", "ekhta": "ekta",
    "duta": "duita", "duito": "duita",
    "ekhaane": "ekhane", "ekane": "ekhane", "ekhone": "ekhon", "akhon": "ekhon",
    "koree": "kore", "koore": "kore", "korobo": "korbo", "korate": "korte",
    "hoche": "hocche", "hochhe": "hocche", "hoicche": "hocche", "hobey": "hobe",
    "achhe": "ache", "ase": "ache", "zodi": "jodi", "kintuh": "kintu",
    "tahle": "tahole", "tarpor": "tarpore", "modhye": "moddhe", "majhe": "moddhe",
    "theka": "theke", "gulo": "gula", "jinis": "jinish",
    "valo": "bhalo", "bhaalo": "bhalo", "jonne": "jonno", "jonyo": "jonno",
    "naa": "na", "jemne": "jemon", "paari": "pari",
}

ENGLISH_STEMS = (
    "function", "class", "variable", "parameter", "argument", "object", "method",
    "database", "table", "query", "loop", "array", "string", "integer", "boolean",
    "list", "tuple", "index", "value", "output", "input", "program", "code",
)
SUFFIXES = ("ta", "er", "gula", "gulo", "ke", "te", "ra")
GLUED = re.compile(
    r"\b(" + "|".join(ENGLISH_STEMS) + r")(" + "|".join(SUFFIXES) + r")\b", re.IGNORECASE
)

FILLERS = {"um", "uh", "aaa", "ahm", "mane", "je", "tahole", "okay", "hmm", "ah", "aa"}
BENGALI = re.compile(r"[ঀ-৿]")


def mmss_to_seconds(minutes, seconds):
    return int(minutes) * 60 + int(seconds)


def parse_file(path):
    """Return (header dict, segments, raw lines).

    Two layouts are accepted. The guide asks for the text on the same line as
    the timestamp. The nine original files instead put the timestamp on its own
    line with the text underneath, and `finetune/prepare_data.py` already reads
    that form, so both are treated as valid here.
    """
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    header, segments, current = {}, [], None

    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            m = re.match(r"#\s*([A-Za-z ]+?)\s*:\s*(.+)$", stripped)
            if m:
                header[m.group(1).strip().lower()] = m.group(2).strip()
            continue
        if not stripped:
            continue

        marker = TS_STRICT.match(stripped) or TS_LOOSE.match(stripped)
        if marker:
            if current:
                segments.append(current)
            current = {
                "line": number,
                "stamp": stripped[:marker.end()],
                "strict": bool(TS_STRICT.match(stripped)),
                "match": marker,
                "text": stripped[marker.end():].strip(),
                "orphan": False,
            }
        elif current:
            current["text"] = (current["text"] + " " + stripped).strip()
        else:
            segments.append({"line": number, "stamp": None, "strict": False,
                             "match": None, "text": stripped, "orphan": True})
    if current:
        segments.append(current)
    return header, segments, lines


def check_file(path, guide_speakers=None):
    header, segments, _ = parse_file(path)
    errors, warnings = [], []

    def err(line, msg):
        errors.append((line, msg))

    def warn(line, msg):
        warnings.append((line, msg))

    if not path.name.startswith("BanglaASR") or not path.name.endswith("_ground_truth.txt"):
        warn(0, f"file name is not BanglaASR<N>_ground_truth.txt")

    speaker = header.get("speaker id") or header.get("speaker")
    if not speaker:
        warn(0, "no 'Speaker ID' in the header; the speaker-independent split needs it")
    elif speaker.upper().startswith("SPK_UNKNOWN"):
        warn(0, "Speaker ID is SPK_UNKNOWN and must be resolved before training")

    total_words, total_seconds, filler_count, parsed = 0, 0.0, 0, []

    for seg in segments:
        line_no, body = seg["line"], seg["text"]

        if seg["orphan"]:
            err(line_no, "text appears before any [M:SS-M:SS] timestamp")
            continue
        if not seg["strict"]:
            err(line_no, "timestamp has spaces or a non-ASCII dash inside the brackets")

        m = seg["match"]
        start = mmss_to_seconds(m.group(1), m.group(2))
        end = mmss_to_seconds(m.group(3), m.group(4))

        if end <= start:
            err(line_no, f"end time {m.group(3)}:{m.group(4)} is not after start")
            continue
        duration = end - start
        if duration > MAX_SEGMENT_S:
            err(line_no, f"segment is {duration:.0f}s, over the 30s Whisper window")
        elif duration > WARN_SEGMENT_S:
            warn(line_no, f"segment is {duration:.0f}s, close to the 30s limit")

        if not body:
            err(line_no, "timestamp has no text after it")
            continue

        if BENGALI.search(body):
            err(line_no, "contains Bengali script; everything must be romanized")
        non_ascii = {ch for ch in body if ord(ch) > 127}
        if non_ascii:
            shown = ", ".join(f"{ch!r} ({unicodedata.name(ch, 'unknown')})" for ch in list(non_ascii)[:3])
            warn(line_no, f"non-ASCII characters: {shown}")

        words = re.findall(r"[A-Za-z']+", body.lower())
        total_words += len(words)
        total_seconds += duration
        filler_count += sum(1 for w in words if w in FILLERS)

        wrong = sorted({w for w in words if w in CANONICAL})
        if wrong:
            fixes = ", ".join(f"{w} -> {CANONICAL[w]}" for w in wrong[:4])
            warn(line_no, f"spelling not in the guide: {fixes}")

        for match in GLUED.finditer(body):
            warn(line_no, f"Bengali ending glued to an English word: "
                          f"'{match.group(0)}' should be '{match.group(1)} {match.group(2)}'")

        parsed.append((line_no, start, end))

    for (line_a, _, end_a), (line_b, start_b, _) in zip(parsed, parsed[1:]):
        if start_b < end_a:
            err(line_b, f"overlaps the previous segment by {end_a - start_b}s")
        elif start_b > end_a:
            warn(line_b, f"{start_b - end_a}s gap after the previous segment")

    stats = {
        "segments": len(parsed),
        "minutes": total_seconds / 60,
        "words": total_words,
        "wpm": total_words / (total_seconds / 60) if total_seconds else 0,
        "filler_rate": filler_count / total_words if total_words else 0,
        "speaker": speaker or "missing",
    }

    if parsed:
        if stats["wpm"] < MIN_WPM:
            warn(0, f"speaking rate is {stats['wpm']:.0f} words per minute, unusually low; "
                    f"speech may be missing from the transcript")
        elif stats["wpm"] > MAX_WPM:
            warn(0, f"speaking rate is {stats['wpm']:.0f} words per minute, unusually high; "
                    f"timestamps may be wrong")
        if stats["filler_rate"] < MIN_FILLER_RATE:
            warn(0, f"only {stats['filler_rate'] * 100:.1f}% of words are fillers; "
                    f"they may have been cleaned out, which the guide forbids")

    return errors, warnings, stats


def safe_fix(path):
    """Repair only what cannot change meaning. Writes a .bak first."""
    original = path.read_text(encoding="utf-8", errors="replace")
    fixed = original
    for bad, good in SMART.items():
        fixed = fixed.replace(bad, good)

    out_lines = []
    for line in fixed.splitlines():
        m = TS_LOOSE.match(line)
        if m and not TS_STRICT.match(line):
            tidy = f"[{int(m.group(1))}:{int(m.group(2)):02d}-{int(m.group(3))}:{int(m.group(4)):02d}]"
            line = tidy + line[m.end():]
        out_lines.append(line.rstrip())
    fixed = "\n".join(out_lines) + "\n"

    if fixed == original:
        return False
    path.with_suffix(path.suffix + ".bak").write_text(original, encoding="utf-8")
    path.write_text(fixed, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Validate ground-truth transcripts")
    ap.add_argument("--dir", default=str(REPO / "data" / "ground_truth"))
    ap.add_argument("--file", default=None, help="Check a single file")
    ap.add_argument("--fix", action="store_true", help="Apply safe repairs before checking")
    ap.add_argument("--quiet", action="store_true", help="Only show files with problems")
    args = ap.parse_args()

    if args.file:
        paths = [Path(args.file)]
    else:
        folder = Path(args.dir)
        if not folder.is_dir():
            sys.exit(f"no such directory: {folder}")
        paths = sorted(folder.glob("*.txt"))
    if not paths:
        sys.exit("no transcript files found")

    total_errors = total_warnings = 0
    totals = {"segments": 0, "minutes": 0.0, "words": 0}
    speakers = {}

    for path in paths:
        if args.fix and safe_fix(path):
            print(f"{path.name}: applied safe repairs, original saved as {path.name}.bak")

        errors, warnings, stats = check_file(path)
        total_errors += len(errors)
        total_warnings += len(warnings)
        for key in totals:
            totals[key] += stats[key]
        speakers.setdefault(stats["speaker"], []).append(path.name)

        if args.quiet and not errors and not warnings:
            continue

        flag = "FAIL" if errors else ("warn" if warnings else "ok")
        print(f"\n{path.name}  [{flag}]")
        print(f"  speaker {stats['speaker']} | {stats['segments']} segments | "
              f"{stats['minutes']:.1f} min | {stats['wpm']:.0f} wpm | "
              f"fillers {stats['filler_rate'] * 100:.1f}%")

        shown = {}
        for line_no, msg in errors:
            key = re.sub(r"\d+", "N", msg)
            shown.setdefault(key, []).append(line_no)
        for key, lines in shown.items():
            where = f"line {lines[0]}" if len(lines) == 1 else f"{len(lines)} lines, first {lines[0]}"
            print(f"  ERROR  {key}  ({where})")

        shown = {}
        for line_no, msg in warnings:
            key = re.sub(r"\d+", "N", msg)
            shown.setdefault(key, []).append(line_no)
        for key, lines in list(shown.items())[:8]:
            where = "header" if lines[0] == 0 else (
                f"line {lines[0]}" if len(lines) == 1 else f"{len(lines)} lines, first {lines[0]}")
            print(f"  warn   {key}  ({where})")
        if len(shown) > 8:
            print(f"  warn   ... {len(shown) - 8} more kinds of warning")

    print("\n" + "=" * 62)
    print(f"files {len(paths)} | segments {totals['segments']} | "
          f"{totals['minutes'] / 60:.2f} hours | words {totals['words']}")
    print("speakers: " + ", ".join(f"{k} ({len(v)} files)" for k, v in sorted(speakers.items())))
    print(f"errors {total_errors} | warnings {total_warnings}")
    if total_errors:
        print("\nFiles with errors are not safe to train on until fixed.")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
