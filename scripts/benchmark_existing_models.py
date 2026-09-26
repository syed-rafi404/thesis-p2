"""Score published Bengali / Bengali-English speech models on our own test clips.

Chapter 2 compares this work with neighbouring systems but had never run any of
them on our data, so the comparison was an argument rather than a table. This
runs them on the same 177 held-out clips, with the same references, the same
normaliser and the same metric functions the headline result uses, so every row
sits on one scale.

Two things make this a fair test rather than a rigged one:

* Each model decodes under **its own** generation config. We do not force our
  language or task tokens onto someone else's model, because a Bengali model was
  trained to emit Bengali and forcing "en/transcribe" would break it for reasons
  that are our fault, not theirs.
* The script reports which alphabet each model wrote in. A model that answers in
  Bengali script scores badly against romanized references no matter how good its
  recognition is, and that has to be visible in the output instead of buried in a
  single error rate.

Run from the repo root with the fine-tune interpreter:

    set HF_HUB_OFFLINE=1
    set TRANSFORMERS_OFFLINE=1
    F:\\thesisP2\\envs\\thesis_ft\\Scripts\\python.exe ^
      scripts\\benchmark_existing_models.py --models-dir F:\\thesisP2\\models --limit 10

Drop --limit for the full pass. Results go to output/baseline_benchmark.json
and .md.
"""
import argparse
import importlib.util
import json
import os
import statistics
import sys
import time
import unicodedata

from pathlib import Path

import soundfile as sf
import torch

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work_final5h"))
CLIPS = FT_DIR / "clips"
OUT = REPO / "output"


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# prepare_data.py imports lecture_numbering as a sibling, so finetune/ has to be
# importable before it is loaded by path.
sys.path.insert(0, str(REPO / "finetune"))


# Reuse the exact helpers behind the headline numbers, so the rows are comparable.
_ev = _load_module(REPO / "finetune" / "evaluate.py", "ev")
_prep = _load_module(REPO / "finetune" / "prepare_data.py", "prep")
normalize = _prep.normalize_banglish
wer, cer = _ev.wer, _ev.cer


def script_of(text):
    """Which alphabet did the model answer in?

    Counts letters by Unicode block. The result decides how a row should be read:
    Bengali script cannot match a romanized reference whatever the model heard.
    """
    bengali = latin = 0
    for ch in text:
        if not ch.isalpha():
            continue
        name = unicodedata.name(ch, "")
        if name.startswith("BENGALI"):
            bengali += 1
        elif name.startswith("LATIN"):
            latin += 1
    total = bengali + latin
    if not total:
        return "empty", 0.0
    frac = bengali / total
    if frac > 0.6:
        return "Bengali script", frac
    if frac > 0.1:
        return "mixed", frac
    return "Latin", frac


def load_rows(split_path, limit):
    rows = []
    for line in open(split_path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        wav = CLIPS / r["audio"]
        if wav.exists():
            r["_wav"] = wav
            rows.append(r)
    if limit:
        rows = rows[:limit]
    return rows


def family_of(model_dir):
    """Whisper encoder-decoder or wav2vec2-style CTC?

    Both families are published for Bengali and a comparison that covered only
    one of them would invite the obvious question, so the loader handles each.
    """
    cfg = json.loads((Path(model_dir) / "config.json").read_text(encoding="utf-8"))
    arch = " ".join(cfg.get("architectures") or []) + " " + str(cfg.get("model_type", ""))
    arch = arch.lower()
    if "whisper" in arch:
        return "whisper"
    if "ctc" in arch or "wav2vec2" in arch or "bert" in arch:
        return "ctc"
    return "whisper"


def decode_model(model_dir, rows, batch_size, device):
    """Transcribe every clip with the model's own decoding defaults."""
    family = family_of(model_dir)
    dtype = torch.float16 if device == "cuda" else torch.float32

    if family == "whisper":
        from transformers import WhisperForConditionalGeneration, WhisperProcessor
        processor = WhisperProcessor.from_pretrained(model_dir)
        model = WhisperForConditionalGeneration.from_pretrained(model_dir, torch_dtype=dtype)
    else:
        from transformers import AutoModelForCTC, AutoProcessor
        processor = AutoProcessor.from_pretrained(model_dir)
        model = AutoModelForCTC.from_pretrained(model_dir, torch_dtype=dtype)
    model = model.to(device).eval()

    hyps = []
    started = time.time()
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        audio = [sf.read(str(r["_wav"]))[0] for r in batch]
        with torch.no_grad():
            if family == "whisper":
                feats = processor.feature_extractor(
                    audio, sampling_rate=16000, return_tensors="pt").input_features
                ids = model.generate(feats.to(device, dtype=model.dtype), max_new_tokens=220)
                text = processor.batch_decode(ids, skip_special_tokens=True)
            else:
                # CTC takes the raw waveform and needs padding, since clips differ
                # in length and there is no encoder that pads to 30 s for us.
                enc = processor(audio, sampling_rate=16000, return_tensors="pt",
                                padding=True)
                logits = model(enc.input_values.to(device, dtype=model.dtype),
                               attention_mask=getattr(enc, "attention_mask", None)
                               if getattr(enc, "attention_mask", None) is None
                               else enc.attention_mask.to(device)).logits
                text = processor.batch_decode(logits.argmax(-1).cpu().numpy())
        hyps.extend(text)
        print("    %d/%d" % (min(i + batch_size, len(rows)), len(rows)), end="\r", flush=True)
    print("    decoded %d clips in %.0f s (%s)     "
          % (len(rows), time.time() - started, family))

    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return hyps


def score(rows, hyps):
    per_clip, beng_frac, scripts = [], [], {}
    for r, h in zip(rows, hyps):
        ref_n, hyp_n = normalize(r["text"]), normalize(h)
        kind, frac = script_of(h)
        beng_frac.append(frac)
        scripts[kind] = scripts.get(kind, 0) + 1
        per_clip.append({
            "clip": r["audio"],
            "wer": wer(ref_n, hyp_n),
            "cer": cer(ref_n, hyp_n),
            "script": kind,
            # The normaliser drops every non-ASCII character, so a Bengali-script
            # answer normalises to almost nothing and scores near 100 per cent
            # however well the model heard the speech. Keeping the surviving
            # length makes that visible instead of leaving a bare error rate.
            "chars_kept": len(hyp_n),
            "ref_chars": len(ref_n),
            # Kept whole, not truncated: rescore_baselines_transliterated.py
            # scores this text again after transliteration, and a cut-off
            # hypothesis would quietly change that result.
            "hyp": h,
        })
    # Same definition as evaluate.py, so the counts mean the same thing.
    runaway = sum(1 for c, r in zip(per_clip, rows)
                  if len(c["hyp"].split()) > 2 * max(1, len(r["text"].split())))
    return {
        "clips": len(per_clip),
        "wer_median": statistics.median(c["wer"] for c in per_clip),
        "cer_median": statistics.median(c["cer"] for c in per_clip),
        "runaway_clips": runaway,
        "bengali_letter_fraction": statistics.mean(beng_frac) if beng_frac else 0.0,
        "script_counts": scripts,
        "chars_kept_ratio": (sum(c["chars_kept"] for c in per_clip)
                             / max(1, sum(c["ref_chars"] for c in per_clip))),
        "per_clip": per_clip,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models-dir", default=r"F:\thesisP2\models")
    ap.add_argument("--split", default=str(FT_DIR / "test.jsonl"))
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--only", default=None, help="run one model directory by name")
    ap.add_argument("--out", default=str(OUT / "baseline_benchmark.json"))
    args = ap.parse_args()

    # These models answer in Bengali script and the Windows console is cp1252,
    # so printing a sample would otherwise kill the run after the work is done.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    device = "cuda" if torch.cuda.is_available() else "cpu"
    rows = load_rows(args.split, args.limit)
    if not rows:
        sys.exit("no clips found; check THESIS_FT_DIR and the split path")
    print("clips: %d   device: %s" % (len(rows), device))

    models_dir = Path(args.models_dir)
    dirs = sorted(d for d in models_dir.iterdir()
                  if d.is_dir() and (d / "config.json").exists())
    if args.only:
        dirs = [d for d in dirs if d.name == args.only]
    if not dirs:
        sys.exit("no downloaded models in %s" % models_dir)

    results = {}
    for d in dirs:
        print("\n%s" % d.name)
        try:
            hyps = decode_model(str(d), rows, args.batch, device)
        except Exception as exc:                                   # noqa: BLE001
            print("    failed: %s" % exc)
            results[d.name] = {"error": str(exc)}
            continue
        s = score(rows, hyps)
        results[d.name] = s
        mix = ", ".join("%s %d" % (k, v) for k, v in sorted(
            s["script_counts"].items(), key=lambda kv: -kv[1]))
        print("    CER %.1f%%  WER %.1f%%  runaway %d" %
              (100 * s["cer_median"], 100 * s["wer_median"], s["runaway_clips"]))
        print("    script: %s   ASCII kept %.0f%% of reference length"
              % (mix, 100 * s["chars_kept_ratio"]))
        print("    sample: %s" % s["per_clip"][0]["hyp"][:110])

    # Models arrive one at a time as their weights finish downloading, so a run
    # adds to the file rather than replacing it. A model run again overwrites
    # its own entry, which is what a re-run is for.
    OUT.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out)
    payload = {"split": args.split, "clips": len(rows), "device": device, "models": {}}
    if out_path.exists():
        try:
            old = json.loads(out_path.read_text(encoding="utf-8"))
            if old.get("clips") == len(rows) and old.get("split") == args.split:
                payload["models"] = old.get("models", {})
            else:
                print("    note: existing file used a different split or clip count, "
                      "starting a new one")
        except (OSError, ValueError):
            pass
    payload["models"].update(results)
    out_path.write_text(json.dumps(payload, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nwrote %s (%d models in file)" % (args.out, len(payload["models"])))


if __name__ == "__main__":
    main()
