"""Re-score the baseline models after transliterating Bengali script to Roman.

The first pass (scripts/benchmark_existing_models.py) scores each published model
against our romanized references as it actually writes. Models that answer in
Bengali script score near 100 per cent there, and the obvious objection is that
this penalises them for orthography rather than for recognition.

This answers that objection instead of arguing with it. Every Bengali-script run
in a hypothesis is transliterated to Roman with a deterministic scheme and the
clip is scored again. Nothing about the reference changes.

Two transliterations are tried and **the better score of the two is reported**,
so the result is an upper bound on how well each model could do if orthography
were free:

* ITRANS as the library emits it.
* The same with the inherent word-final "a" dropped. Bengali script writes a
  consonant that carries an unwritten "a" which speakers of Bengali do not
  pronounce at the end of a word, so a literal transliteration produces
  "dekhechilama" where a Banglish writer types "dekhechilam".

This is deliberately generous. If a model still scores badly after being handed
the best of two transliterations, the gap is not about the alphabet.

Run after benchmark_existing_models.py:

    F:\\thesisP2\\envs\\thesis_ft\\Scripts\\python.exe ^
      scripts\\rescore_baselines_transliterated.py

Writes output/baseline_benchmark_translit.json and prints the table.
"""
import argparse
import importlib.util
import json
import os
import re
import statistics
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
OUT = REPO / "output"
SCRATCH_LIBS = Path(os.environ.get("THESIS_SCRATCH_LIBS", ""))

# indic_transliteration is installed into a scratch directory on purpose, so the
# fine-tuning environment on the 3060 is not touched. See CLAUDE.md.
if SCRATCH_LIBS and SCRATCH_LIBS.exists():
    sys.path.insert(0, str(SCRATCH_LIBS))

sys.path.insert(0, str(REPO / "finetune"))


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_ev = _load_module(REPO / "finetune" / "evaluate.py", "ev")
_prep = _load_module(REPO / "finetune" / "prepare_data.py", "prep")
normalize = _prep.normalize_banglish
wer, cer = _ev.wer, _ev.cer

BENGALI_RUN = re.compile(r"[\u0980-\u09FF]+(?:[\u0980-\u09FF\s\u200c\u200d]*[\u0980-\u09FF])?")


def make_translit():
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate

    def to_roman(text):
        return transliterate(text, sanscript.BENGALI, sanscript.ITRANS)

    return to_roman


def romanize(text, to_roman, drop_inherent_a):
    """Replace every Bengali-script run, leaving Latin words untouched."""
    def repl(m):
        out = to_roman(m.group(0))
        if drop_inherent_a:
            out = re.sub(r"([bcdfghjklmnpqrstvwxyz])a\b", r"\1", out, flags=re.I)
        return out
    return BENGALI_RUN.sub(repl, text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", default=str(OUT / "baseline_benchmark.json"))
    ap.add_argument("--split", default=r"F:\thesisP2\ft_work_final5h\test.jsonl")
    ap.add_argument("--out", default=str(OUT / "baseline_benchmark_translit.json"))
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    to_roman = make_translit()
    refs = {}
    for line in open(args.split, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            refs[r["audio"]] = r["text"]

    bench = json.loads(Path(args.bench).read_text(encoding="utf-8"))
    results = {}

    for name, m in bench.get("models", {}).items():
        if "per_clip" not in m:
            continue
        rows = []
        for c in m["per_clip"]:
            ref = refs.get(c["clip"])
            if ref is None:
                continue
            ref_n = normalize(ref)
            plain = normalize(romanize(c["hyp"], to_roman, False))
            clipped = normalize(romanize(c["hyp"], to_roman, True))
            best_cer = min(cer(ref_n, plain), cer(ref_n, clipped))
            best_wer = min(wer(ref_n, plain), wer(ref_n, clipped))
            rows.append({"clip": c["clip"], "cer": best_cer, "wer": best_wer,
                         "cer_raw": c["cer"], "wer_raw": c["wer"],
                         "hyp_roman": clipped[:300]})
        if not rows:
            continue
        results[name] = {
            "clips": len(rows),
            "cer_median_translit": statistics.median(r["cer"] for r in rows),
            "wer_median_translit": statistics.median(r["wer"] for r in rows),
            "cer_median_raw": statistics.median(r["cer_raw"] for r in rows),
            "wer_median_raw": statistics.median(r["wer_raw"] for r in rows),
            "per_clip": rows,
        }

    Path(args.out).write_text(json.dumps(results, indent=1, ensure_ascii=False),
                              encoding="utf-8")

    print("%-46s %10s %10s %10s %10s" % ("model", "CER raw", "CER tr.", "WER raw", "WER tr."))
    for name, r in results.items():
        print("%-46s %9.1f%% %9.1f%% %9.1f%% %9.1f%%" % (
            name[:46], 100 * r["cer_median_raw"], 100 * r["cer_median_translit"],
            100 * r["wer_median_raw"], 100 * r["wer_median_translit"]))
    print("\nOurs, for reference: CER 15.8 / 16.0, WER 42.5 / 41.7 (RESULTS.md 1.8)")
    print("wrote %s" % args.out)


if __name__ == "__main__":
    main()
