r"""
Step 1 - Data preparation for the Whisper Banglish fine-tuning PoC.

Turns the 9 BanglaASR lecture recordings + their human-timestamped ground-truth
transcripts into a Whisper-ready dataset of (<=30s audio clip, romanized text)
pairs, with a SPEAKER-INDEPENDENT split:

    Train  = BanglaASR1-5  (speaker A, data/raw/Speaker1)
    Test   = BanglaASR6-9  (speaker B, data/raw/Speaker2, never seen in training)

The first version of this split put BanglaASR6 in training as speaker A. It is
speaker B: the user sorted the videos by lecturer, and speaker embeddings agree
(scripts/verify_speakers.py). That split leaked the test speaker into training.
It is kept only to reproduce the superseded numbers: --speaker-map v1.

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

from lecture_numbering import new_number, old_number, scheme_of

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
# A = data/raw/Speaker1, B = data/raw/Speaker2, C = data/raw/Speaker3.
LEGACY_SPEAKERS = {1: "A", 2: "A", 3: "A", 4: "A", 5: "A",
                   6: "B", 7: "B", 8: "B", 9: "B",
                   10: "C", 11: "C", 12: "C", 13: "C"}
# Superseded: put BanglaASR6 (speaker B) in training. Reproduction only.
LEGACY_SPEAKERS_V1 = {1: "A", 2: "A", 3: "A", 4: "A", 5: "A", 6: "A",
                      7: "B", 8: "B", 9: "B"}
SPEAKER_MAPS = {"v2": LEGACY_SPEAKERS, "v1": LEGACY_SPEAKERS_V1}
DEFAULT_TEST_SPEAKERS = ["B"]
AUDIO_CACHE = os.path.join(OUT_DIR, "audio_cache")          # old lecture numbers
AUDIO_CACHE_NEW = os.path.join(OUT_DIR, "audio_cache_new")  # lectures that only have new numbers
VIDEO_EXTS = (".mp4", ".MOV", ".mov", ".mkv", ".avi", ".webm", ".MP4")

MAX_CLIP_S = 28.0       # keep clips comfortably under Whisper's 30s window
MIN_CLIP_S = 1.0        # drop anything shorter than this
SENT_CUT_FRACTION = 0.6 # once a group reaches 60% of MAX_CLIP_S, allow a sentence-end cut
COLLAPSE_VOWELS = False # conservative for the PoC; flip on later to test amar/aamar merging

TS_RE = re.compile(r"\[(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\]")
LOOKS_LIKE_TS = re.compile(r"\[\s*\d{1,2}\s*:\s*\d{2}\s*\S{0,3}\s*\d{1,2}\s*:\s*\d{2}\s*\]")
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
        m = re.search(r"BanglaASR(\d+)", p)      # \d+: BanglaASR10 is not BanglaASR1
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
    # A timestamp TS_RE cannot read ("[  1:34-1:53]", "[0: 17-0:45]") is not a segment
    # boundary, so its text silently joins the previous segment and that clip's text no
    # longer matches its audio. Parsing is left as it was (the published manifests depend on
    # it); the warning makes the problem visible. validate_ground_truth.py --fix repairs it.
    unread = [ln.strip() for ln in raw.splitlines()
              if LOOKS_LIKE_TS.search(ln) and not TS_RE.search(ln)]
    if unread:
        print(f"  WARNING {os.path.basename(path)}: {len(unread)} timestamp(s) not recognised, "
              f"their text is merged into the previous segment (first: {unread[0][:28]}). "
              f"Run scripts/validate_ground_truth.py --fix")
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
def read_speaker(gt_path: str, stem: str, legacy_map: dict = LEGACY_SPEAKERS) -> str:
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
        return legacy_map.get(int(m.group(1)), "UNKNOWN")
    return "UNKNOWN"


def raw_video(name: str) -> str:
    """The one video in data/raw called `name`, or None.

    Two different files with the same name stop the run: after the 2026-09-22
    renumbering a machine with the old data/raw layout (Speaker2/BanglaASR6.mp4,
    an old-numbered lecture) and the new one (live_classroom/BanglaASR6.mp4, a
    different lecture) would otherwise give whichever os.walk met first.
    """
    found = []
    for root, _dirs, files in os.walk(os.path.join(REPO, "data", "raw")):
        for f in files:
            base, ext = os.path.splitext(f)
            if base == name and ext in VIDEO_EXTS:
                found.append(os.path.join(root, f))
    if len({os.path.getsize(p) for p in found}) > 1:
        raise SystemExit(f"two different videos are called {name}: {found}. Keep only the "
                         f"new-numbering copy (data/raw/live_classroom) and move the other away.")
    return found[0] if found else None


def find_audio(stem: str, audio_dir: str = None, scheme: str = "old") -> str:
    """Locate 16 kHz audio for a lecture, extracting it from video if needed.

    Order: an explicit --audio-dir, then audio already extracted by the
    pipeline, then the cache, then ffmpeg on the raw video.

    scheme says which numbering `stem` uses (lecture_numbering.py): "old" for the
    run folders and the frozen ground truth, "new" for data/ground_truth since
    2026-09-22. --audio-dir, the pipeline's run folders and AUDIO_CACHE hold OLD
    numbers; data/raw holds NEW names. Each source is looked up by its own
    number, so a lecture never picks up another lecture's recording; a lecture
    with no old number skips the old-numbered sources entirely.
    """
    m = re.search(r"BanglaASR(\d+)$", stem)
    n = int(m.group(1)) if m else None
    old = old_number(n, scheme) if n is not None else None
    old_stem = f"BanglaASR{old}" if old is not None else None
    raw_stem = f"BanglaASR{new_number(n, scheme)}" if n is not None else stem

    lookup = old_stem if n is not None else stem
    if audio_dir and lookup:
        for ext in (".wav", ".WAV"):
            candidate = os.path.join(audio_dir, lookup + ext)
            if os.path.exists(candidate):
                return candidate

    if old is not None:
        existing = find_wav(old)
        if existing:
            return existing

    cached = (os.path.join(AUDIO_CACHE, old_stem + ".wav") if old_stem
              else os.path.join(AUDIO_CACHE_NEW, raw_stem + ".wav"))
    if os.path.exists(cached):
        return cached

    source = raw_video(raw_stem)
    if not source:
        return None

    os.makedirs(os.path.dirname(cached), exist_ok=True)
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


def check_against_raw_folders(labels: dict, scheme: str = "new"):
    """Warn when speaker labels disagree with how data/raw is sorted into folders.

    The user files videos by lecturer (data/raw/Speaker1, Speaker2, ...). A split
    that trained on video 6 went unnoticed because nothing compared the two.
    Only folders named Speaker* count: since 2026-09-22 data/raw is sorted into
    live_classroom/ and screen_recorded/, which say nothing about the lecturer.
    labels: lecture stem -> speaker label. Returns the number of conflicts.
    """
    raw = os.path.join(REPO, "data", "raw")
    folder_of = {}
    for root, _dirs, files in os.walk(raw):
        if os.path.normpath(root) == os.path.normpath(raw):
            continue
        if not os.path.basename(root).lower().startswith("speaker"):
            continue
        for name in files:
            base, ext = os.path.splitext(name)
            if ext in VIDEO_EXTS:
                folder_of[base] = os.path.basename(root)
    by_folder, by_label = {}, {}
    for stem, label in labels.items():
        m = re.search(r"BanglaASR(\d+)$", stem)
        raw_name = f"BanglaASR{new_number(int(m.group(1)), scheme)}" if m else stem
        folder = folder_of.get(raw_name)
        if folder is None:
            continue
        by_folder.setdefault(folder, set()).add(label)
        by_label.setdefault(label, set()).add(folder)
    conflicts = 0
    for folder, found in sorted(by_folder.items()):
        if len(found) > 1:
            conflicts += 1
            print(f"  WARNING: data/raw/{folder} holds lectures labelled {sorted(found)}")
    for label, found in sorted(by_label.items()):
        if len(found) > 1:
            conflicts += 1
            print(f"  WARNING: speaker {label} spans data/raw folders {sorted(found)}")
    if conflicts:
        print("  Speaker labels disagree with the data/raw folders. Fix the labels "
              "before trusting any speaker-independent result.")
    return conflicts


def discover(gt_dir: str):
    """Every *_ground_truth.txt file: (lecture stem, path, flagged).

    The user marks a file as not ready by putting text in front of its name, for
    example "[Needs recheck]BanglaASR9_ground_truth.txt". Such a file is flagged,
    and main() leaves it out until the marker is removed.
    """
    found = []
    for path in sorted(glob.glob(os.path.join(gt_dir, "*_ground_truth.txt"))):
        name = os.path.basename(path)
        m = re.search(r"(BanglaASR\d+)_ground_truth\.txt$", name)
        stem = m.group(1) if m else name.replace("_ground_truth.txt", "")
        flagged = bool(m) and not name.startswith(m.group(1))
        found.append((stem, path, flagged))
    return found


def gt_minutes(gt_path: str) -> float:
    """Minutes of transcribed speech in a ground-truth file, from its timestamps."""
    return sum(e - s for s, e, _ in parse_gt(gt_path)) / 60.0


def choose_test_lectures(info, fraction, seed, max_exact=16, never=frozenset()):
    """Random whole lectures for the test set, about `fraction` of each lecturer's minutes.

    info: [(stem, speaker, minutes)]. Per lecturer, among all ways of putting some
    but not all of their lectures in the test set, keep those whose test minutes
    are closest to the target (within 10% of it) and pick one at random with the
    seed. So every lecturer with two or more lectures is on both sides, no video
    is cut in two, and the test share stays near the fraction even with a few
    long lectures. A lecturer with a single lecture stays in training.

    never: lectures that may only be trained on. They count towards the
    lecturer's minutes but are never picked; since they stay in training, all
    of the remaining lectures may then be picked. With `never` empty the choice
    is exactly what it was before the option existed.
    """
    import itertools
    rng = random.Random(seed)
    by_speaker = {}
    for stem, speaker, minutes in info:
        by_speaker.setdefault(speaker, []).append((stem, minutes))
    test = set()
    for speaker in sorted(by_speaker):
        everything = sorted(by_speaker[speaker])
        items = [it for it in everything if it[0] not in never]
        max_r = len(items) if len(items) < len(everything) else len(items) - 1
        if max_r < 1:
            continue
        target = fraction * sum(m for _, m in everything)
        if len(items) <= max_exact:
            subsets = [c for r in range(1, max_r + 1)
                       for c in itertools.combinations(items, r)]
            best = min(abs(sum(m for _, m in c) - target) for c in subsets)
            near = [c for c in subsets
                    if abs(sum(m for _, m in c) - target) <= best + 0.1 * target]
            chosen = rng.choice(near)
        else:
            shuffled = list(items)
            rng.shuffle(shuffled)
            chosen, taken = [], 0.0
            for stem, m in shuffled[:-1]:
                if taken >= target:
                    break
                chosen.append((stem, m))
                taken += m
        test.update(stem for stem, _ in chosen)
    return test


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
    ap.add_argument("--only-speakers", default=None,
                    help="Comma-separated speakers to use at all; others are left out. "
                         "The section 1.0 headline used A,B, before speaker C existed")
    ap.add_argument("--speaker-map", default="v2", choices=sorted(SPEAKER_MAPS),
                    help="Speakers for files without a Speaker ID header. v1 is the "
                         "superseded split that put BanglaASR6 in training")
    ap.add_argument("--split-by", choices=("speaker", "video"), default="speaker",
                    help="speaker (default, every published result): --test-speakers are held "
                         "out. video (the user's plan for the 10 h data): random whole lectures, "
                         "about --test-fraction of each lecturer's minutes, go to test")
    ap.add_argument("--test-fraction", type=float, default=0.2)
    ap.add_argument("--split-seed", type=int, default=0)
    ap.add_argument("--test-lectures", default=None,
                    help="With --split-by video: comma-separated lectures for the test set, "
                         "instead of the random choice")
    ap.add_argument("--never-test", default=None,
                    help="With --split-by video: comma-separated lectures that may only be "
                         "trained on (e.g. the validation lectures used to choose the learning "
                         "rate, data/splits/lr_validation.json), so no choice made on them is "
                         "ever scored on them")
    args = ap.parse_args()
    scheme = scheme_of(args.gt_dir)

    out_dir = args.out
    clips_dir = os.path.join(out_dir, "clips")
    if os.path.isdir(clips_dir) and not args.keep_clips:
        shutil.rmtree(clips_dir)
    os.makedirs(clips_dir, exist_ok=True)

    test_speakers = {s.strip() for s in args.test_speakers.split(",") if s.strip()}
    only_speakers = ({s.strip() for s in args.only_speakers.split(",") if s.strip()}
                     if args.only_speakers else None)
    lectures = discover(args.gt_dir)
    if not lectures:
        print(f"no ground-truth files in {args.gt_dir}")
        return

    for stem, path, flagged in lectures:
        if flagged:
            print(f"  [skip] {os.path.basename(path)}: marked not ready by its file name; "
                  f"remove the marker to use it")
    lectures = [(stem, path) for stem, path, flagged in lectures if not flagged]

    print(f"found {len(lectures)} ground-truth files ({scheme} lecture numbering); "
          + (f"test speakers: {sorted(test_speakers)}" if args.split_by == "speaker"
             else f"random video split, {args.test_fraction:.0%} of each lecturer, seed {args.split_seed}"))
    # The fallback table is in OLD numbers (it would call new BanglaASR10 lecturer C), so it
    # only applies to the frozen ground truth; new files must carry a Speaker ID header.
    fallback_speakers = SPEAKER_MAPS[args.speaker_map] if scheme == "old" else {}
    labels = {stem: read_speaker(p, stem, fallback_speakers) for stem, p in lectures}
    check_against_raw_folders(labels, scheme)

    test_lectures = set()
    if args.split_by == "video":
        usable = [(stem, labels[stem], gt_minutes(p)) for stem, p in lectures
                  if labels[stem] != "UNKNOWN"
                  and (not only_speakers or labels[stem] in only_speakers)]
        usable = [u for u in usable if u[2] > 0]
        never = {s.strip() for s in (args.never_test or "").split(",") if s.strip()}
        if never:
            print("train-only (never test): " + ", ".join(sorted(never)))
        if args.test_lectures:
            test_lectures = {s.strip() for s in args.test_lectures.split(",") if s.strip()}
            clash = test_lectures & never
            if clash:
                raise SystemExit(f"--test-lectures includes lectures marked --never-test: {sorted(clash)}")
        else:
            test_lectures = choose_test_lectures(usable, args.test_fraction, args.split_seed, never=never)
        print("test lectures: " + ", ".join(sorted(test_lectures)))

    manifest, stats, speaker_minutes = [], {}, {}

    for stem, gt_path in lectures:
        speaker = read_speaker(gt_path, stem, fallback_speakers)
        if speaker == "UNKNOWN":
            # Never guess: an unlabelled lecture silently joining training is how
            # a test speaker leaks in. Add "# Speaker ID:" to the file instead.
            print(f"  [skip] {stem}: no Speaker ID header and no known speaker; not used")
            continue
        if only_speakers and speaker not in only_speakers:
            print(f"  [skip] {stem}: speaker {speaker} not in --only-speakers")
            continue
        if args.split_by == "video":
            split = "test" if stem in test_lectures else "train"
        else:
            split = "test" if speaker in test_speakers else "train"
        wav = find_audio(stem, args.audio_dir, scheme)
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

        stats[stem] = (split, speaker, clip_idx, kept_s / 60.0, audio_dur / 60.0, wav)
        speaker_minutes[speaker] = speaker_minutes.get(speaker, 0.0) + kept_s / 60.0
        print(f"  {stem} [{split}/spk {speaker}]: {clip_idx} clips, "
              f"{kept_s/60:.1f}min kept of {audio_dur/60:.1f}min audio  <- "
              f"{os.path.basename(os.path.dirname(wav))}/{os.path.basename(wav)}")

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

    if args.split_by == "video":
        heard = {r["speaker"] for r in train_rows}
        for speaker in sorted({r["speaker"] for r in test_rows} - heard):
            print(f"\n  WARNING: lecturer {speaker} is only in the test set, so the test mixes "
                  f"heard and unseen lecturers. Add a lecture of theirs to training.")
    split_record = {
        "split_by": args.split_by,
        "numbering": scheme,
        "test_speakers": (sorted(test_speakers) if args.split_by == "speaker"
                          else sorted({r["speaker"] for r in test_rows})),
        "train_speakers": sorted({r["speaker"] for r in train_rows}),
        "train_hours_used": sum(r["dur"] for r in train_rows) / 3600,
        "train_hours_available": full_train_hours,
        "test_hours": sum(r["dur"] for r in test_rows) / 3600,
        "train_cap": args.train_hours,
        "seed": args.seed,
        "speaker_map": args.speaker_map,
        "only_speakers": sorted(only_speakers) if only_speakers else None,
        "minutes_per_speaker": {k: round(v, 1) for k, v in sorted(speaker_minutes.items())},
        "lectures": {k: {"split": v[0], "speaker": v[1], "clips": v[2],
                         "minutes_kept": round(v[3], 1), "minutes_audio": round(v[4], 1)}
                     for k, v in stats.items()},
    }
    if args.split_by == "video":
        split_record.update({
            "test_fraction": args.test_fraction, "split_seed": args.split_seed,
            "test_lectures": sorted(test_lectures),
            "test_minutes_per_speaker": {
                s: round(sum(r["dur"] for r in test_rows if r["speaker"] == s) / 60, 1)
                for s in sorted({r["speaker"] for r in test_rows})},
        })
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
