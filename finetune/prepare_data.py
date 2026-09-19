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

import os
import re
import glob
import json
import shutil
import unicodedata

import soundfile as sf

# ----------------------------------------------------------------------------- config
REPO = r"F:\thesisP2\thesisP2"
GT_DIR = os.path.join(REPO, "data", "ground_truth")
OUT_DIR = r"F:\thesisP2\ft_work"
CLIPS_DIR = os.path.join(OUT_DIR, "clips")

TRAIN_VIDEOS = [1, 2, 3, 4, 5, 6]   # speaker A
TEST_VIDEOS = [7, 8, 9]             # speaker B

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


# ----------------------------------------------------------------------------- main
def main():
    if os.path.isdir(CLIPS_DIR):
        shutil.rmtree(CLIPS_DIR)   # wipe stale clips from previous runs
    os.makedirs(CLIPS_DIR, exist_ok=True)
    manifest, train_rows, test_rows = [], [], []
    stats = {}

    for n in range(1, 10):
        split = "train" if n in TRAIN_VIDEOS else "test"
        speaker = "A" if n in TRAIN_VIDEOS else "B"
        wav = find_wav(n)
        gt_path = os.path.join(GT_DIR, f"BanglaASR{n}_ground_truth.txt")
        if not wav or not os.path.exists(gt_path):
            print(f"  [skip] BanglaASR{n}: wav={bool(wav)} gt={os.path.exists(gt_path)}")
            continue

        audio, sr = sf.read(wav)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio_dur = len(audio) / sr

        vid_dir = os.path.join(CLIPS_DIR, f"BanglaASR{n}")
        os.makedirs(vid_dir, exist_ok=True)

        clip_idx, kept_s = 0, 0.0
        for (seg_s, seg_e, seg_text) in parse_gt(gt_path):
            for (s, e, text) in split_segment(seg_s, seg_e, seg_text, audio_dur):
                if e - s < MIN_CLIP_S:
                    continue
                norm = normalize_banglish(text)
                if not norm:
                    continue
                a0, a1 = int(s * sr), int(e * sr)
                clip = audio[a0:a1]
                if len(clip) < MIN_CLIP_S * sr:
                    continue
                rel = os.path.join(f"BanglaASR{n}", f"seg_{clip_idx:03d}.wav")
                sf.write(os.path.join(CLIPS_DIR, rel), clip, sr, subtype="PCM_16")
                row = {
                    "audio": rel.replace("\\", "/"),
                    "text": norm,
                    "video": n, "speaker": speaker, "split": split,
                    "start": round(s, 2), "end": round(e, 2), "dur": round(e - s, 2),
                }
                manifest.append(row)
                (train_rows if split == "train" else test_rows).append(row)
                clip_idx += 1
                kept_s += (e - s)

        stats[n] = (split, clip_idx, kept_s / 60.0, audio_dur / 60.0)
        print(f"  BanglaASR{n} [{split}/spk {speaker}]: {clip_idx} clips, "
              f"{kept_s/60:.1f}min kept of {audio_dur/60:.1f}min audio")

    def dump(path, rows):
        with open(path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    dump(os.path.join(OUT_DIR, "manifest.jsonl"), manifest)
    dump(os.path.join(OUT_DIR, "train.jsonl"), train_rows)
    dump(os.path.join(OUT_DIR, "test.jsonl"), test_rows)

    tr_min = sum(s[2] for k, s in stats.items() if s[0] == "train")
    te_min = sum(s[2] for k, s in stats.items() if s[0] == "test")
    print("\n=== SUMMARY ===")
    print(f"Train: {len(train_rows)} clips, {tr_min:.1f} min  (speaker A: videos {TRAIN_VIDEOS})")
    print(f"Test : {len(test_rows)} clips, {te_min:.1f} min  (speaker B: videos {TEST_VIDEOS})")
    print(f"Wrote manifests + {len(manifest)} clips to {OUT_DIR}")


if __name__ == "__main__":
    main()
