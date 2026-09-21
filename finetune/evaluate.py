"""
Step 4 - Compare the LoRA fine-tune against the base model on held-out speech.

Decodes the speaker-independent test clips twice, once with the frozen base
model and once with the LoRA adapter applied, then scores both with:

  1. Normalized WER and CER, using the SAME `normalize_banglish()` that built
     the training targets, so the normalizer is auditable and public.
  2. The term metric that produced the reported 73.9% Term F1, imported
     unchanged from `scripts/evaluate_ground_truth.py`. Note what that metric
     is: exact matching against a fixed 82-word English lexicon, algebraically
     a Sorensen-Dice overlap of term counts. It is reported here so the
     fine-tuned numbers sit on the same scale as the baseline, not because it
     is the better metric.
  3. A paired exact test across clips, plus per-clip deltas, so the comparison
     comes with a p-value that was actually computed.

Run (from the repo root, with the fine-tune environment):
    F:\\thesisP2\\envs\\thesis_ft\\Scripts\\python.exe finetune\\evaluate.py
    ... --adapter F:\\thesisP2\\ft_work\\lora_whisper_small
    ... --limit 20            # quick check on a few clips first

Outputs:
    F:\\thesisP2\\ft_work\\eval_<tag>.json    per-clip records and summary
    F:\\thesisP2\\ft_work\\eval_<tag>.md      tables ready to paste into a chapter
"""

import argparse
import importlib.util
import io
import itertools
import json
import math
import os
import statistics
import sys
import zlib
import contextlib
from pathlib import Path

import soundfile as sf
import torch

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
# Override with THESIS_FT_DIR when moving machines; the default sits next to
# the repository, which is the layout on both boxes.
FT_DIR = Path(os.environ.get("THESIS_FT_DIR") or (REPO.parent / "ft_work"))
CLIPS = FT_DIR / "clips"
DEFAULT_BASE = str(FT_DIR / "models" / "whisper-small")
LANG, TASK = "en", "transcribe"

# Whisper's own loop safeguard (Radford et al. 2023, section 4.5): when a
# transcript compresses too well it is a repetition loop, so decode that clip
# again with sampling at rising temperatures. Only the compression-ratio half
# is used; the log-probability half would resample most Banglish clips, not
# just the loops. It reads the hypothesis only, never the reference, and is
# applied identically to the base and the fine-tuned model.
FALLBACK_TEMPERATURES = (0.2, 0.4, 0.6, 0.8, 1.0)
COMPRESSION_RATIO_THRESHOLD = 2.4
FALLBACK_SEED = 0


# --------------------------------------------------------------------------- imports
def _load_module(path, name):
    """Import a file by path, muting whatever it prints on import."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def _stub_rich_if_missing():
    """`evaluate_ground_truth.py` imports rich only for console output.

    Stub it when it is absent, but never when it is installed: other libraries
    in this environment import the real rich, and a stub breaks them.
    """
    import types
    try:
        import rich  # noqa: F401
        return
    except ImportError:
        pass
    for name in ("rich", "rich.console", "rich.table", "rich.panel",
                 "rich.progress", "rich.box", "rich.markdown"):
        if name not in sys.modules:
            stub = types.ModuleType(name)
            stub.__getattr__ = lambda _n: type(
                "_Any", (), {"__init__": lambda s, *a, **k: None,
                             "__getattr__": lambda s, n: (lambda *a, **k: None)}
            )
            sys.modules[name] = stub


def load_term_metric():
    """The exact functions behind the reported Term F1, or None if unavailable."""
    try:
        _stub_rich_if_missing()
        return _load_module(REPO / "scripts" / "evaluate_ground_truth.py", "egt")
    except Exception as exc:                      # noqa: BLE001
        print(f"  ! term metric unavailable: {exc}")
        return None


def load_normalizer():
    mod = _load_module(REPO / "finetune" / "prepare_data.py", "prep")
    return mod.normalize_banglish


# --------------------------------------------------------------------------- metrics
def edit_distance(ref_tokens, hyp_tokens):
    prev = list(range(len(hyp_tokens) + 1))
    for i, r in enumerate(ref_tokens, 1):
        cur = [i] + [0] * len(hyp_tokens)
        for j, h in enumerate(hyp_tokens, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1]


def wer(ref, hyp):
    r = ref.split()
    return edit_distance(r, hyp.split()) / len(r) if r else 0.0


def cer(ref, hyp):
    return edit_distance(list(ref), list(hyp)) / len(ref) if ref else 0.0


def _normal_cdf(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def wilcoxon_signed_rank(deltas):
    """Two-sided Wilcoxon signed-rank test, normal approximation with tied ranks.

    Preferred over a test on the mean here: a handful of clips where the model
    falls into a repetition loop produce error rates far above 100%, which
    dominate any mean-based test. Ranks are not moved by their magnitude.
    """
    nz = [d for d in deltas if abs(d) > 1e-12]
    n = len(nz)
    if n < 6:
        return None, n, None
    order = sorted(range(n), key=lambda i: abs(nz[i]))
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(abs(nz[order[j + 1]]) - abs(nz[order[i]])) < 1e-12:
            j += 1
        average = (i + j + 2) / 2
        for k in range(i, j + 1):
            ranks[order[k]] = average
        i = j + 1
    w_plus = sum(r for r, v in zip(ranks, nz) if v > 0)
    mu = n * (n + 1) / 4
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (w_plus - mu) / sigma if sigma else 0.0
    return 2 * (1 - _normal_cdf(abs(z))), n, z


def sign_test(better, total):
    """Two-sided exact binomial test that the model wins on more than half the clips."""
    if total == 0:
        return 1.0
    tail = sum(math.comb(total, k) for k in range(better, total + 1)) / 2 ** total
    return min(1.0, 2 * tail)


def paired_permutation_p(deltas, max_exact=18):
    """Two-sided paired test on the mean delta. Exact when small enough."""
    deltas = [d for d in deltas if abs(d) > 1e-12]
    n = len(deltas)
    if n == 0:
        return 1.0, "no non-zero differences"
    observed = abs(sum(deltas))
    if n <= max_exact:
        hits = sum(
            1 for signs in itertools.product((1, -1), repeat=n)
            if abs(sum(s * d for s, d in zip(signs, deltas))) >= observed - 1e-12
        )
        return hits / 2 ** n, f"exact sign-flip, n={n}"
    import random
    random.seed(0)
    trials = 20000
    hits = sum(
        1 for _ in range(trials)
        if abs(sum(d if random.random() < 0.5 else -d for d in deltas)) >= observed - 1e-12
    )
    return (hits + 1) / (trials + 1), f"sign-flip Monte Carlo, n={n}, {trials} resamples"


# --------------------------------------------------------------------------- decoding
def load_rows(split_file, limit=None):
    rows = []
    with open(FT_DIR / split_file, encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            row["abs"] = str(CLIPS / row["audio"].replace("/", os.sep))
            rows.append(row)
    return rows[:limit] if limit else rows


def compression_ratio(text):
    """gzip compression ratio of a transcript, as Whisper defines it."""
    data = text.encode("utf-8")
    return len(data) / len(zlib.compress(data)) if data else 0.0


def _decode_batches(model, processor, rows, batch_size, device, label, **gen):
    outputs = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start:start + batch_size]
        audio = []
        for row in chunk:
            wave, sr = sf.read(row["abs"])
            if getattr(wave, "ndim", 1) > 1:
                wave = wave.mean(axis=1)
            audio.append(wave)
        feats = processor.feature_extractor(
            audio, sampling_rate=sr, return_tensors="pt"
        ).input_features.to(device, dtype=model.dtype)
        with torch.no_grad():
            ids = model.generate(
                feats, language=LANG, task=TASK, max_new_tokens=200, **gen
            )
        outputs.extend(processor.batch_decode(ids, skip_special_tokens=True))
        done = min(start + batch_size, len(rows))
        print(f"    {label}: {done}/{len(rows)} clips", end="\r", flush=True)
    return outputs


def decode_all(model, processor, rows, batch_size, device, label, decode="greedy",
               seed=FALLBACK_SEED):
    """Greedy decode every clip, in batches.

    With decode="fallback", clips whose transcript compresses above the
    threshold are decoded again at each fallback temperature in turn, until
    they no longer look like a loop. A clip that still loops at the last
    temperature keeps that last attempt, as Whisper does.

    Returns the transcripts and, per clip, the temperature that produced it.
    """
    model.eval()
    outputs = _decode_batches(model, processor, rows, batch_size, device, label,
                              do_sample=False)
    print(f"    {label}: {len(rows)}/{len(rows)} clips done")
    temps = [0.0] * len(rows)
    if decode != "fallback":
        return outputs, temps

    for t in FALLBACK_TEMPERATURES:
        todo = [i for i, h in enumerate(outputs)
                if compression_ratio(h) > COMPRESSION_RATIO_THRESHOLD]
        if not todo:
            break
        torch.manual_seed(seed)
        redo =_decode_batches(model, processor, [rows[i] for i in todo], batch_size,
                               device, f"{label} T={t}", do_sample=True, temperature=t)
        for i, h in zip(todo, redo):
            outputs[i], temps[i] = h, t
        print(f"    {label}: {len(todo)} looping clips re-decoded at T={t}")
    return outputs, temps


def fallback_summary(hyps, temps):
    return {
        "clips_fell_back": sum(1 for t in temps if t > 0),
        "clips_still_looping": sum(1 for h in hyps
                                   if compression_ratio(h) > COMPRESSION_RATIO_THRESHOLD),
    }


def build_model(base_path, adapter_path, device):
    from transformers import WhisperForConditionalGeneration, WhisperProcessor

    processor = WhisperProcessor.from_pretrained(base_path)
    processor.tokenizer.set_prefix_tokens(language=LANG, task=TASK)
    model = WhisperForConditionalGeneration.from_pretrained(
        base_path, torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    model.generation_config.language = LANG
    model.generation_config.task = TASK
    model.generation_config.forced_decoder_ids = None

    if adapter_path:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter_path)
        model = model.merge_and_unload()       # fold LoRA in, so generate() is plain
    return model.to(device), processor


# --------------------------------------------------------------------------- report
def summarise(rows, hyps, normalize, egt):
    per_clip, ref_all, hyp_all = [], [], []
    for row, hyp in zip(rows, hyps):
        ref_n, hyp_n = normalize(row["text"]), normalize(hyp)
        per_clip.append({
            "audio": row["audio"],
            "video": row.get("video"),
            "speaker": row.get("speaker"),
            "reference": ref_n,
            "hypothesis": hyp_n,
            "wer": wer(ref_n, hyp_n),
            "cer": cer(ref_n, hyp_n),
        })
        ref_all.append(ref_n)
        hyp_all.append(hyp_n)

    joined_ref, joined_hyp = " ".join(ref_all), " ".join(hyp_all)
    runaway = sum(
        1 for c in per_clip
        if len(c["hypothesis"].split()) > 2 * max(1, len(c["reference"].split()))
    )
    summary = {
        "clips": len(per_clip),
        "wer_mean_per_clip": sum(c["wer"] for c in per_clip) / max(1, len(per_clip)),
        "cer_mean_per_clip": sum(c["cer"] for c in per_clip) / max(1, len(per_clip)),
        "wer_median_per_clip": statistics.median([c["wer"] for c in per_clip]) if per_clip else 0.0,
        "cer_median_per_clip": statistics.median([c["cer"] for c in per_clip]) if per_clip else 0.0,
        "wer_corpus": wer(joined_ref, joined_hyp),
        "cer_corpus": cer(joined_ref, joined_hyp),
        "runaway_clips": runaway,
        "words_emitted": sum(len(c["hypothesis"].split()) for c in per_clip),
        "words_reference": sum(len(c["reference"].split()) for c in per_clip),
    }
    if egt is not None:
        terms = egt.compute_term_metrics(
            egt.extract_technical_terms(joined_ref), egt.extract_technical_terms(joined_hyp)
        )
        summary.update({
            "term_recall": terms["recall"],
            "term_precision": terms["precision"],
            "term_f1": terms["f1"],
        })
    return per_clip, summary


def rank_stats(base_clips, tuned_clips, key):
    """Per-clip win counts and rank-based p-values for one metric."""
    if not base_clips or not tuned_clips:
        return None
    deltas = [b[key] - t[key] for b, t in zip(base_clips, tuned_clips)]
    better = sum(1 for d in deltas if d > 0)
    wil_p, n, z = wilcoxon_signed_rank(deltas)
    return {
        "metric": key,
        "better": better,
        "total": len(deltas),
        "wilcoxon_p": wil_p if wil_p is not None else float('nan'),
        "wilcoxon_z": z,
        "wilcoxon_n": n,
        "sign_p": sign_test(better, len(deltas)),
    }


def markdown_report(base_sum, tuned_sum, p_value, p_note, examples, args,
                    stats_wer=None, stats_cer=None):
    def pct(d, k):
        return f"{d[k] * 100:.1f}%" if k in d else "n/a"

    lines = [
        "# Fine-tune evaluation: base vs LoRA",
        "",
        f"Base model: `{args.base}`",
        f"Adapter: `{args.adapter}`" if args.adapter else "Adapter: none",
        f"Split: `{args.split}`, clips scored: {base_sum['clips']}",
        "",
        "All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.",
        "",
    ]
    if getattr(args, "decode", "greedy") == "fallback":
        lines += [
            "Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip "
            f"whose transcript has gzip compression ratio above {COMPRESSION_RATIO_THRESHOLD} "
            f"is decoded again with sampling at T = {', '.join(map(str, FALLBACK_TEMPERATURES))} "
            f"in turn (seed {getattr(args, 'fallback_seed', FALLBACK_SEED)}) until it no "
            "longer looks like a loop. "
            f"Fell back: base {base_sum.get('clips_fell_back', 0)}, "
            f"tuned {tuned_sum.get('clips_fell_back', 0)} clips. "
            f"Still looping after T = {FALLBACK_TEMPERATURES[-1]}: "
            f"base {base_sum.get('clips_still_looping', 0)}, "
            f"tuned {tuned_sum.get('clips_still_looping', 0)}.",
            "",
        ]
    else:
        lines += ["Decoding: greedy.", ""]
    lines += [
        "| Metric | Base | Fine-tuned |",
        "|---|---|---|",
        f"| WER, per clip median | {pct(base_sum, 'wer_median_per_clip')} | {pct(tuned_sum, 'wer_median_per_clip')} |",
        f"| WER, per clip mean | {pct(base_sum, 'wer_mean_per_clip')} | {pct(tuned_sum, 'wer_mean_per_clip')} |",
        f"| WER, whole split | {pct(base_sum, 'wer_corpus')} | {pct(tuned_sum, 'wer_corpus')} |",
        f"| CER, per clip median | {pct(base_sum, 'cer_median_per_clip')} | {pct(tuned_sum, 'cer_median_per_clip')} |",
        f"| CER, per clip mean | {pct(base_sum, 'cer_mean_per_clip')} | {pct(tuned_sum, 'cer_mean_per_clip')} |",
        f"| Term recall | {pct(base_sum, 'term_recall')} | {pct(tuned_sum, 'term_recall')} |",
        f"| Term precision | {pct(base_sum, 'term_precision')} | {pct(tuned_sum, 'term_precision')} |",
        f"| Term F1 | {pct(base_sum, 'term_f1')} | {pct(tuned_sum, 'term_f1')} |",
        f"| Clips that run away | {base_sum.get('runaway_clips', 0)} of {base_sum['clips']} "
        f"| {tuned_sum.get('runaway_clips', 0)} of {tuned_sum.get('clips', 0)} |",
        "",
        "Means are reported for completeness but are dominated by a few clips where a",
        "model falls into a repetition loop and emits far more words than were spoken,",
        "which pushes error rates above 100%. The rank-based tests below are the ones",
        "to read.",
        "",]
    for label, stats in (("WER", stats_wer), ("CER", stats_cer)):
        if not stats:
            continue
        lines.append(
            f"- **{label}**: fine-tune wins on {stats['better']} of {stats['total']} clips. "
            f"Wilcoxon signed-rank p = {stats['wilcoxon_p']:.2e}, "
            f"sign test p = {stats['sign_p']:.2e}."
        )
    lines += [
        "",
        f"Paired test on the mean per-clip WER, for reference: p = {p_value:.4f} ({p_note}).",
        "",
        "Term F1 here is exact matching against a fixed 82-word English lexicon,",
        "reported only so these numbers sit on the same scale as the 73.9% baseline.",
        "",
        "## Examples",
        "",
    ]
    for ex in examples:
        lines += [
            f"**{ex['audio']}**", "",
            f"- reference: {ex['reference']}",
            f"- base: {ex['base']}",
            f"- tuned: {ex['tuned']}",
            "",
        ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Compare base Whisper against the LoRA fine-tune")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--adapter", default=str(FT_DIR / "lora_whisper_small"))
    ap.add_argument("--split", default="test.jsonl")
    ap.add_argument("--limit", type=int, default=None, help="Only score this many clips")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--tag", default="whisper_small")
    ap.add_argument("--base-only", action="store_true", help="Score the base model alone")
    ap.add_argument("--decode", default="greedy", choices=("greedy", "fallback"),
                    help="greedy reproduces every earlier number. fallback adds Whisper's "
                         "compression-ratio loop safeguard, to both models alike")
    ap.add_argument("--fallback-seed", type=int, default=FALLBACK_SEED,
                    help="Sampling seed for the fallback, to check the result does not "
                         "hinge on one draw")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device: {device}")
    if device == "cuda":
        print(f"gpu   : {torch.cuda.get_device_name(0)}")

    rows = load_rows(args.split, args.limit)
    print(f"clips : {len(rows)} from {args.split}")

    normalize = load_normalizer()
    egt = load_term_metric()

    print("  decoding with base model ...")
    base_model, processor = build_model(args.base, None, device)
    base_hyps, base_temps = decode_all(base_model, processor, rows, args.batch, device,
                                       "base", args.decode, args.fallback_seed)
    del base_model
    if device == "cuda":
        torch.cuda.empty_cache()

    base_clips, base_sum = summarise(rows, base_hyps, normalize, egt)
    base_sum.update(fallback_summary(base_hyps, base_temps))
    for clip, t in zip(base_clips, base_temps):
        clip["temperature"] = t

    tuned_clips, tuned_sum, p_value, p_note, examples = [], {}, 1.0, "not run", []
    stats_wer = stats_cer = None
    if not args.base_only:
        adapter = Path(args.adapter)
        if not adapter.is_dir():
            sys.exit(f"adapter not found: {adapter}. Train it first, or pass --base-only.")
        print("  decoding with fine-tuned model ...")
        tuned_model, processor = build_model(args.base, str(adapter), device)
        tuned_hyps, tuned_temps = decode_all(tuned_model, processor, rows, args.batch, device,
                                             "tuned", args.decode, args.fallback_seed)
        del tuned_model
        if device == "cuda":
            torch.cuda.empty_cache()

        tuned_clips, tuned_sum = summarise(rows, tuned_hyps, normalize, egt)
        tuned_sum.update(fallback_summary(tuned_hyps, tuned_temps))
        for clip, t in zip(tuned_clips, tuned_temps):
            clip["temperature"] = t
        deltas = [t["wer"] - b["wer"] for b, t in zip(base_clips, tuned_clips)]
        p_value, p_note = paired_permutation_p(deltas)
        stats_wer = rank_stats(base_clips, tuned_clips, "wer")
        stats_cer = rank_stats(base_clips, tuned_clips, "cer")

        ranked = sorted(
            range(len(deltas)), key=lambda i: deltas[i]
        )[:5]                                   # biggest improvements first
        examples = [{
            "audio": base_clips[i]["audio"],
            "reference": base_clips[i]["reference"],
            "base": base_clips[i]["hypothesis"],
            "tuned": tuned_clips[i]["hypothesis"],
        } for i in ranked]

    record = {
        "base_model": args.base,
        "adapter": None if args.base_only else args.adapter,
        "split": args.split,
        "decode": args.decode,
        "fallback_seed": args.fallback_seed if args.decode == "fallback" else None,
        "base": base_sum,
        "tuned": tuned_sum,
        "paired_test": {"p_value": p_value, "method": p_note},
        "rank_tests": {"wer": stats_wer, "cer": stats_cer},
        "per_clip": {
            "base": base_clips,
            "tuned": tuned_clips,
        },
    }
    out_json = FT_DIR / f"eval_{args.tag}.json"
    out_md = FT_DIR / f"eval_{args.tag}.md"
    out_json.write_text(json.dumps(record, indent=2), encoding="utf-8")
    out_md.write_text(
        markdown_report(base_sum, tuned_sum, p_value, p_note, examples, args, stats_wer, stats_cer),
        encoding="utf-8")

    print("\n--- summary ---")
    for key in ("wer_mean_per_clip", "cer_mean_per_clip", "term_f1"):
        b = base_sum.get(key)
        t = tuned_sum.get(key)
        if b is None:
            continue
        line = f"  {key:20} base {b * 100:6.1f}%"
        if t is not None:
            line += f"   tuned {t * 100:6.1f}%   delta {(t - b) * 100:+.1f}"
        print(line)
    if not args.base_only:
        for stats in (stats_wer, stats_cer):
            if stats:
                print(f"  {stats['metric']} wins {stats['better']}/{stats['total']} clips"
                      f"   wilcoxon p={stats['wilcoxon_p']:.2e}   sign p={stats['sign_p']:.2e}")
    print(f"\nwrote {out_json}\nwrote {out_md}")


if __name__ == "__main__":
    main()
