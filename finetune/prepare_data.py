"""
Step 1 - Data preparation for the Whisper Banglish fine-tuning PoC.

Turns the 9 BanglaASR lecture recordings + their human-timestamped ground-truth
transcripts into a Whisper-ready dataset of (<=30s audio clip, romanized text)
pairs, with a SPEAKER-INDEPENDENT split:

    Train  = BanglaASR1-6  (speaker A)
    Test   = BanglaASR7-9  (speaker B, never seen in training)

Why this design:
- The ground-truth files are already segmented with [M:SS-M:SS] timestamps by the
  annotators, so we do NOT need forced alignment / WhisperX. We parse those
  timestamps directly.
- Human segments are often > 30s. Whisper only sees 30s windows, so we subdivide
  long segments at sentence boundaries, distributing time proportionally by text
  length. Clips therefore end at natural pauses and stay <= MAX_CLIP_S.
- Training targets are deterministically normalized (NOT with an LLM) so spelling
  is consistent. This is label cleaning for training, not evaluation tampering.

Nothing here touches torch/CUDA. Only stdlib + soundfile are used.

Outputs (on F:, outside the git repo):
    F:\thesisP2\ft_work\clips\BanglaASR<n>\seg_###.wav
    F:\thesisP2\ft_work\train.jsonl
    F:\thesisP2\ft_work\test.jsonl
    F:\thesisP2\ft_work\manifest.jsonl   (everything, for inspection)
"""

import argparse
import os
import re
import glob
import json
import random
import shutil
import subprocess
import unicodedata
from pathlib import Path

import soundfile as sf

# ----------------------------------------------------------------------------- config
# Paths resolve in this order: environment variable, then the layout on the
# machine this was written on. Set THESIS_REPO and THESIS_FT_DIR when moving to
# another machine (for example the 5090 box) and nothing else needs editing.
REPO = os.environ.get("THESIS_REPO") or str(Path(__file__).resolve().parents[1])
GT_DIR = os.path.join(REPO, "data", "ground_truth")
OUT_DIR = os.environ.get("THESIS_FT_DIR") or os.path.join(os.path.dirname(REPO), "ft_work")
CLIPS_DIR = os.path.join(OUT_DIR, "clips")

# Legacy fallback for the original nine lectures, which have no Speaker ID in
# their headers. Newer files declare "# Speaker ID: SPKnn" and that wins.
LEGACY_SPEAKERS = {1: "A", 2: "A", 3: "A", 4: "A", 5: "A", 6: "A",
                   7: "B", 8: "B", 9: "B"}
DEFAULT_TEST_SPEAKERS = ["B"]
AUDIO_CACHE = os.path.join(OUT_DIR, "audio_cache")
VIDEO_EXTS = (".mp4", ".MOV", ".mov", ".mkv", ".avi", ".webm", ".MP4")

MAX_CLIP_S = 28.0       # keep clips comfortably under Whisper's 30s window
MIN_CLIP_S = 1.0        # drop anything shorter than this
SENT_CUT_FRACTION = 0.6 # once a group reaches 60% of MAX_CLIP_S, allow a sentence-end cut
COLLAPSE_VOWELS = False # conservative for the PoC; flip on later to test amar/aamar merging

TS_RE = re.compile(r"\[(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\]")
_PUNCT_MAP = {
    "–": "-", "—": "-", "‒": "-", "−": "-",   # dashes
    "‘": "'", "’": "'", "“": '"', "”": '"',   # smart quotes
    "…": "...", "।": ".",                                # ellipsis, Bengali danda
}


# ----------------------------------------------------------------------------- helpers
def normalize_banglish(text: str, collapse_vowels: bool = COLLAPSE_VOWELS) -> str:
    """Deterministic, auditable normalization for training targets.

    Lowercase, unify punctuation, drop stray non-ASCII (a few Bengali leftovers),
    collapse 3+ char runs. Optionally collapse repeated vowels (amar/aamar)."""
    text = unicodedata.normalize("NFKC", text)
    for k, v in _PUNCT_MAP.items():
        text = text.replace(k, v)
    text = text.lower()
    text = "".join(ch if ord(ch) < 128 else " " for ch in text)   # strip stray non-ascii
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)                     # 3+ repeats -> 2
    if collapse_vowels:
        text = re.sub(r"([aeiou])\1+", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_wav(n: int) -> str:
    """Locate the longest (most complete) extracted 16kHz wav for BanglaASR<n>."""
    best, best_frames = None, -1
    pattern = os.path.join(REPO, "output", "live_focused", "**", "full_audio.wav")
    for p in glob.glob(pattern, recursive=True):
        m = re.search(r"BanglaASR(\d)", p)
        if not m or int(m.group(1)) != n:
            continue
        frames = sf.info(p).frames
        if frames > best_frames:
            best, best_frames = p, frames
    return best


def parse_gt(path: str):
    """Return top-level (start_s, end_s, text) segments from a ground-truth file.

    Text is everything between a [M:SS-M:SS] marker and the next marker, with the
    header comment lines (starting with #) removed."""
    raw = open(path, encoding="utf-8").read()
    # Drop comment/instruction lines FIRST so the header's example timestamps
    # (e.g. "# [0:00-0:30] Assalamualaikum...") never leak in as fake segments.
    raw = "\n".join(ln for ln in raw.splitlines() if not ln.lstrip().startswith("#"))
    matches = list(TS_RE.finditer(raw))
    segs = []
    for i, m in enumerate(matches):
        start = int(m.group(1)) * 60 + int(m.group(2))
        end = int(m.group(3)) * 60 + int(m.group(4))
        body = raw[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(raw)]
        lines = [ln for ln in body.splitlines() if not ln.strip().startswith("#")]
        text = " ".join(lines).strip()
        if text and end > start:
            segs.append((start, end, text))
    return segs


def split_segment(start, end, text, audio_dur, max_s=MAX_CLIP_S):
    """Subdivide a long [start,end] segment into <=max_s clips.

    Greedy over words; time is distributed proportionally to character length.
    Prefers to cut at sentence-ending punctuation once a group is long enough,
    so clips land on natural pauses."""
    text = text.strip()
    if not text:
        return []
    dur = end - start
    if dur <= max_s + 2:
        return [(start, min(end, audio_dur), text)]

    words = text.split()
    total = sum(len(w) + 1 for w in words) or 1

    def t_at(cum):
        return start + (cum / total) * dur

    out, group, group_start_cum, cum = [], [], 0, 0
    for w in words:
        tentative = t_at(cum + len(w) + 1) - t_at(group_start_cum)
        if group and tentative > max_s:
            out.append((t_at(group_start_cum), t_at(cum), " ".join(group)))
            group, group_start_cum = [], cum
        group.append(w)
        cum += len(w) + 1
        if group and w[-1:] in ".?!":
            if (t_at(cum) - t_at(group_start_cum)) >= max_s * SENT_CUT_FRACTION:
                out.append((t_at(group_start_cum), t_at(cum), " ".join(group)))
                group, group_start_cum = [], cum
    if group:
        out.append((t_at(group_start_cum), end, " ".join(group)))

    return [(s, min(e, audio_dur), t) for s, e, t in out if s < audio_dur and t.strip()]



# ----------------------------------------------------------------------------- discovery
def read_speaker(gt_path: str, stem: str) -> str:
    """Speaker ID from the file header, else the legacy per-video mapping."""
    with open(gt_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.lstrip().startswith("#"):
                break
            m = re.match(r"#\s*speaker\s*id\s*:\s*(\S+)", line.strip(), re.IGNORECASE)
            if m:
                return m.group(1)
    m = re.search(r"BanglaASR(\d+)", stem)
    if m:
        return LEGACY_SPEAKERS.get(int(m.group(1)), "UNKNOWN")
    return "UNKNOWN"


def find_audio(stem: str, audio_dir: str = None) -> str:
    """Locate 16 kHz audio for a lecture, extracting it from video if needed.

    Order: an explicit --audio-dir, then audio already extracted by the
    pipeline, then the cache, then ffmpeg on the raw video.
    """
    if audio_dir:
        for ext in (".wav", ".WAV"):
            candidate = os.path.join(audio_dir, stem + ext)
            if os.path.exists(candidate):
                return candidate

    m = re.search(r"BanglaASR(\d+)$", stem)
    if m:
        existing = find_wav(int(m.group(1)))
        if existing:
            return existing

    cached = os.path.join(AUDIO_CACHE, stem + ".wav")
    if os.path.exists(cached):
        return cached

    source = None
    for root, _dirs, files in os.walk(os.path.join(REPO, "data", "raw")):
        for name in files:
            base, ext = os.path.splitext(name)
            if base == stem and ext in VIDEO_EXTS:
                source = os.path.join(root, name)
                break
        if source:
            break
    if not source:
        return None

    os.makedirs(AUDIO_CACHE, exist_ok=True)
    print(f"    extracting audio from {os.path.basename(source)} ...")
    result = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", source,
         "-ac", "1", "-ar", "16000", "-vn", cached],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"    ffmpeg failed: {result.stderr.strip()[:200]}")
        return None
    return cached


def discover(gt_dir: str):
    """Every *_ground_truth.txt file, with its lecture stem."""
    found = []
    for path in sorted(glob.glob(os.path.join(gt_dir, "*_ground_truth.txt"))):
        stem = os.path.basename(path).replace("_ground_truth.txt", "")
        found.append((stem, path))
    return found


def cap_hours(rows, hours, seed=0):
    """Deterministically sample clips down to a training budget, for scaling curves."""
    if not hours:
        return rows
    budget = hours * 3600
    shuffled = list(rows)
    random.Random(seed).shuffle(shuffled)
    kept, total = [], 0.0
    for row in shuffled:
        if total >= budget:
            break
        kept.append(row)
        total += row["dur"]
    kept.sort(key=lambda r: (r["video"], r["start"]))
    return kept


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Build Whisper training clips from ground truth")
    ap.add_argument("--gt-dir", default=GT_DIR, help="Folder of *_ground_truth.txt files")
    ap.add_argument("--audio-dir", default=None, help="Folder of pre-extracted 16 kHz wavs")
    ap.add_argument("--out", default=OUT_DIR, help="Where manifests and clips are written")
    ap.add_argument("--test-speakers", default=",".join(DEFAULT_TEST_SPEAKERS),
                    help="Comma-separated speaker IDs held out for testing")
    ap.add_argument("--train-hours", type=float, default=None,
                    help="Cap training audio at this many hours, for a data-scaling curve")
    ap.add_argument("--seed", type=int, default=0, help="Seed for the training cap")
    ap.add_argument("--keep-clips", action="store_true",
                    help="Do not wipe previously extracted clips")
    args = ap.parse_args()

    out_dir = args.out
    clips_dir = os.path.join(out_dir, "clips")
    if os.path.isdir(clips_dir) and not args.keep_clips:
        shutil.rmtree(clips_dir)
    os.makedirs(clips_dir, exist_ok=True)

    test_speakers = {s.strip() for s in args.test_speakers.split(",") if s.strip()}
    lectures = discover(args.gt_dir)
    if not lectures:
        print(f"no ground-truth files in {args.gt_dir}")
        return

    print(f"found {len(lectures)} ground-truth files; test speakers: {sorted(test_speakers)}")

    manifest, stats, speaker_minutes = [], {}, {}

    for stem, gt_path in lectures:
        speaker = read_speaker(gt_path, stem)
        split = "test" if speaker in test_speakers else "train"
        wav = find_audio(stem, args.audio_dir)
        if not wav:
            print(f"  [skip] {stem}: no audio found (looked in --audio-dir, pipeline output, data/raw)")
            continue

        audio, sr = sf.read(wav)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio_dur = len(audio) / sr

        vid_dir = os.path.join(clips_dir, stem)
        os.makedirs(vid_dir, exist_ok=True)

        clip_idx, kept_s = 0, 0.0
        for (seg_s, seg_e, seg_text) in parse_gt(gt_path):
            for (s, e, text) in split_segment(seg_s, seg_e, seg_text, audio_dur):
                if e - s < MIN_CLIP_S:
                    continue
                norm = normalize_banglish(text)
                if not norm:
                    continue
                clip = audio[int(s * sr):int(e * sr)]
                if len(clip) < MIN_CLIP_S * sr:
                    continue
                rel = os.path.join(stem, f"seg_{clip_idx:03d}.wav")
                sf.write(os.path.join(clips_dir, rel), clip, sr, subtype="PCM_16")
                legacy = re.search(r"BanglaASR(\d+)$", stem)
                manifest.append({
                    "audio": rel.replace("\\", "/"),
                    "text": norm,
                    "lecture": stem,
                    "video": int(legacy.group(1)) if legacy else stem,
                    "speaker": speaker,
                    "split": split,
                    "start": round(s, 2), "end": round(e, 2), "dur": round(e - s, 2),
                })
                clip_idx += 1
                kept_s += (e - s)

        stats[stem] = (split, speaker, clip_idx, kept_s / 60.0, audio_dur / 60.0)
        speaker_minutes[speaker] = speaker_minutes.get(speaker, 0.0) + kept_s / 60.0
        print(f"  {stem} [{split}/spk {speaker}]: {clip_idx} clips, "
              f"{kept_s/60:.1f}min kept of {audio_dur/60:.1f}min audio")

    train_rows = [r for r in manifest if r["split"] == "train"]
    test_rows = [r for r in manifest if r["split"] == "test"]

    full_train_hours = sum(r["dur"] for r in train_rows) / 3600
    if args.train_hours:
        train_rows = cap_hours(train_rows, args.train_hours, args.seed)
        print(f"\ncapped training data to {args.train_hours}h "
              f"({len(train_rows)} clips of {full_train_hours:.2f}h available, seed {args.seed})")

    if not test_rows:
        print("\n  WARNING: no test clips. Check --test-speakers against the Speaker IDs above.")

    def dump(path, rows):
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    dump(os.path.join(out_dir, "manifest.jsonl"), manifest)
    dump(os.path.join(out_dir, "train.jsonl"), train_rows)
    dump(os.path.join(out_dir, "test.jsonl"), test_rows)

    split_record = {
        "test_speakers": sorted(test_speakers),
        "train_speakers": sorted({r["speaker"] for r in train_rows}),
        "train_hours_used": sum(r["dur"] for r in train_rows) / 3600,
        "train_hours_available": full_train_hours,
        "test_hours": sum(r["dur"] for r in test_rows) / 3600,
        "train_cap": args.train_hours,
        "seed": args.seed,
        "minutes_per_speaker": {k: round(v, 1) for k, v in sorted(speaker_minutes.items())},
        "lectures": {k: {"split": v[0], "speaker": v[1], "clips": v[2],
                         "minutes_kept": round(v[3], 1), "minutes_audio": round(v[4], 1)}
                     for k, v in stats.items()},
    }
    with open(os.path.join(out_dir, "split.json"), "w", encoding="utf-8") as f:
        json.dump(split_record, f, indent=2)

    print("\n=== SUMMARY ===")
    print(f"Train: {len(train_rows)} clips, {split_record['train_hours_used'] * 60:.1f} min "
          f"(speakers {split_record['train_speakers']})")
    print(f"Test : {len(test_rows)} clips, {split_record['test_hours'] * 60:.1f} min "
          f"(speakers {split_record['test_speakers']})")
    print("Minutes per speaker: " + ", ".join(
        f"{k}={v}" for k, v in split_record["minutes_per_speaker"].items()))
    print(f"Wrote manifests, split.json and {len(manifest)} clips to {out_dir}")


if __name__ == "__main__":
    main()
