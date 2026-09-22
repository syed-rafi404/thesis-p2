#!/usr/bin/env python
"""
Stages 2-5 of the pre-registered hyperparameter tuning (data/splits/tuning_plan.md), run by
itself after stage 1 (claude_transfer/lr_check.ps1, the learning-rate check).

Every candidate is a full training on the tuning training set of F:\\thesisP2\\ft_work_lr and is
scored on its validation set (in that folder test.jsonl IS the validation set: BanglaASR2, 12,
14). The score is the fine-tuned model's median per-clip CER. Stages follow the plan exactly:
  1 learning rate (already run: lr5e-4, lr1e-3, lr2e-3)
  2 LoRA rank 8 and 32 at the best learning rate (alpha = 2 x rank)
  3 all four attention projections vs q+v, at the best rate and rank
  4 epochs from the validation loss per epoch of the best run (keep 8 if within 2% of the minimum)
  5 the best configuration again with seed 1; noise rule decides between it and the default
Writes tuning_summary.md and tuning_result.json, copies the small files to artifacts/ft_work_lr,
commits and pushes. A candidate whose adapter and score exist is not run again.

    python scripts/tune_whisper.py
"""
import ctypes
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FT = Path(os.environ.get("THESIS_TUNE_DIR", r"F:\thesisP2\ft_work_lr"))
PY = os.environ.get("THESIS_PYTHON", sys.executable)
BASE = "openai/whisper-large-v3-turbo"
LOG = FT / "tuning_log.txt"
DEFAULT = {"lr": "1e-3", "rank": 16, "modules": "q_proj,v_proj", "epochs": 8, "seed": 42}
QKVO = "q_proj,k_proj,v_proj,out_proj"


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')}  {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def tag_of(c):
    t = f"lr{c['lr']}"
    if c["rank"] != 16:
        t += f"_r{c['rank']}"
    if c["modules"] != "q_proj,v_proj":
        t += "_qkvo"
    if c["epochs"] != 8:
        t += f"_e{c['epochs']}"
    if c["seed"] != 42:
        t += f"_s{c['seed']}"
    return t


def env():
    e = dict(os.environ, THESIS_FT_DIR=str(FT), HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1",
             PYTHONIOENCODING="utf-8")
    e.setdefault("HF_HOME", r"F:\thesisP2\hf_cache")
    return e


def run_candidate(c):
    """Train and score one configuration; returns its validation scores."""
    tag = tag_of(c)
    adapter = FT / f"lora_{tag}"
    if not (adapter / "adapter_model.safetensors").exists():
        t = time.time()
        with open(FT / f"train_{tag}.log", "w", encoding="utf-8") as out:
            r = subprocess.run([PY, "-u", str(REPO / "finetune" / "train_lora.py"), "--model", BASE,
                                "--data-dir", str(FT), "--adapter-out", str(adapter),
                                "--epochs", str(c["epochs"]), "--batch", "8", "--lr", c["lr"],
                                "--lora-r", str(c["rank"]), "--lora-alpha", str(2 * c["rank"]),
                                "--target-modules", c["modules"], "--seed", str(c["seed"]),
                                "--grad-checkpointing"], cwd=REPO, env=env(), stdout=out,
                               stderr=subprocess.STDOUT)
        say(f"train {tag}: exit {r.returncode}, {(time.time() - t) / 60:.1f} min")
    if not (FT / f"eval_{tag}.json").exists():
        t = time.time()
        with open(FT / f"evallog_{tag}.log", "w", encoding="utf-8") as out:
            r = subprocess.run([PY, "-u", str(REPO / "finetune" / "evaluate.py"), "--base", BASE,
                                "--adapter", str(adapter), "--decode", "greedy", "--batch", "8",
                                "--tag", tag], cwd=REPO, env=env(), stdout=out, stderr=subprocess.STDOUT)
        say(f"evaluate {tag}: exit {r.returncode}, {(time.time() - t) / 60:.1f} min")
    return score(c)


def score(c):
    path = FT / f"eval_{tag_of(c)}.json"
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    return {"tag": tag_of(c), "config": dict(c),
            "cer": 100 * d["tuned"]["cer_median_per_clip"], "wer": 100 * d["tuned"]["wer_median_per_clip"],
            "base_cer": 100 * d["base"]["cer_median_per_clip"], "base_wer": 100 * d["base"]["wer_median_per_clip"],
            "val_loss": val_losses(c)}


def val_losses(c):
    log = FT / f"train_{tag_of(c)}.log"
    if not log.exists():
        return {}
    text = log.read_text(encoding="utf-8", errors="ignore")
    return {int(float(e)): float(v) for v, e in
            re.findall(r"'eval_loss': '?([\d.]+)'?.*?'epoch': '?([\d.]+)'?", text)}


def best(results):
    ok = [r for r in results if r]
    return min(ok, key=lambda r: (r["cer"], r["wer"]))


def main():
    FT.mkdir(parents=True, exist_ok=True)
    try:        # keep Windows awake while tuning runs; released when this process exits
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000001)
    except Exception:
        pass
    stage1_log = FT / "lr_check_log.txt"
    while not (stage1_log.exists() and "finished" in stage1_log.read_text(encoding="utf-8", errors="ignore")):
        time.sleep(60)
    say("stage 1 (learning rate) finished; starting stages 2-5")
    history = {}

    stage1 = [score(dict(DEFAULT, lr=lr)) for lr in ("5e-4", "1e-3", "2e-3")]
    history["1 learning rate"] = stage1
    cur = dict(best(stage1)["config"])
    say(f"stage 1 best: {tag_of(cur)}")

    stage2 = [score(cur)] + [run_candidate(dict(cur, rank=r)) for r in (8, 32)]
    history["2 LoRA rank"] = stage2
    cur = dict(best(stage2)["config"])
    say(f"stage 2 best: {tag_of(cur)}")

    stage3 = [score(cur), run_candidate(dict(cur, modules=QKVO))]
    history["3 adapted layers"] = stage3
    cur = dict(best(stage3)["config"])
    say(f"stage 3 best: {tag_of(cur)}")

    losses = score(cur)["val_loss"]
    stage4 = [score(cur)]
    if losses:
        min_epoch = min(losses, key=losses.get)
        at8 = losses.get(max(losses))
        if at8 is not None and at8 > 1.02 * losses[min_epoch] and min_epoch != cur["epochs"]:
            stage4.append(run_candidate(dict(cur, epochs=min_epoch)))
            say(f"stage 4: loss minimum at epoch {min_epoch}; trained that too")
        else:
            say(f"stage 4: loss at the last epoch within 2% of its minimum (epoch {min_epoch}); keep {cur['epochs']}")
    history["4 epochs"] = stage4
    cur = dict(best(stage4)["config"])
    winner = score(cur)

    again = run_candidate(dict(cur, seed=1))
    history["5 stability (seed 1)"] = [winner, again]
    spread = abs(winner["cer"] - again["cer"]) if again else None
    default = score(DEFAULT)
    gain = default["cer"] - winner["cer"]
    if cur == DEFAULT:
        chosen, reason = DEFAULT, "the default was best"
    elif spread is None:
        chosen, reason = DEFAULT, (f"default kept: the seed-1 run of {winner['tag']} failed, so its gain "
                                   f"({gain:.1f} points) could not be checked against noise")
    elif gain < spread:
        chosen, reason = DEFAULT, (f"default kept: the best ({winner['tag']}) beats it by {gain:.1f} "
                                   f"points of CER, not more than its seed-to-seed difference ({spread:.1f})")
    else:
        chosen, reason = cur, (f"{winner['tag']} chosen: {gain:.1f} points of CER better than the default, "
                               f"more than its seed-to-seed difference ({spread:.1f})")
    say("decision: " + reason)

    result = {"chosen": chosen, "reason": reason, "winner": winner["tag"], "winner_cer": winner["cer"],
              "default_cer": default["cer"], "seed_spread_cer": spread,
              "train_args": ["--lr", chosen["lr"], "--lora-r", str(chosen["rank"]),
                             "--lora-alpha", str(2 * chosen["rank"]), "--target-modules", chosen["modules"]],
              "epochs": chosen["epochs"],
              "plan": "data/splits/tuning_plan.md", "validation": "data/splits/lr_validation.json"}
    (FT / "tuning_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    lines = ["# Hyperparameter tuning on the validation lectures (3060, 2026-09-22/23)", "",
             "Plan committed before any result: `data/splits/tuning_plan.md`. Validation lectures "
             "BanglaASR2 (A), BanglaASR12 (B), BanglaASR14 (C), never test. Score: median per-clip CER "
             "of the fine-tuned model on the validation set (off-the-shelf Whisper on the same clips: "
             f"CER {default['base_cer']:.1f}%, WER {default['base_wer']:.1f}%).", "",
             "| Stage | Run | lr | rank | layers | epochs | seed | val CER | val WER | val loss, last / min |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for stage, rows in history.items():
        for r in rows:
            if not r:
                continue
            c, vl = r["config"], r["val_loss"]
            loss = f"{vl[max(vl)]:.3f} / {min(vl.values()):.3f}" if vl else "-"
            lines.append(f"| {stage} | {r['tag']} | {c['lr']} | {c['rank']} | "
                         f"{'q,k,v,o' if c['modules'] == QKVO else 'q,v'} | {c['epochs']} | {c['seed']} | "
                         f"{r['cer']:.1f}% | {r['wer']:.1f}% | {loss} |")
    lines += ["", f"**Decision:** {reason}.", "",
              f"Chosen for the 6 h and 10 h runs: lr {chosen['lr']}, rank {chosen['rank']}, "
              f"{'all attention projections' if chosen['modules'] == QKVO else 'q_proj + v_proj'}, "
              f"{chosen['epochs']} epochs (`run_p3_experiment.py --tuned`)."]
    (FT / "tuning_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    say("summary written")

    if os.environ.get("THESIS_TUNE_NO_GIT"):
        say("finished (no git: test mode)")
        return 0
    dst = REPO / "artifacts" / "ft_work_lr"
    dst.mkdir(parents=True, exist_ok=True)
    for f in FT.iterdir():
        if f.is_file() and f.suffix in (".json", ".jsonl", ".md", ".log", ".txt"):
            (dst / f.name).write_bytes(f.read_bytes())
    g = ["git", "-c", "safe.directory=F:/thesisP2/thesisP2"]
    subprocess.run(g + ["add", "-f", "--", "artifacts/ft_work_lr"], cwd=REPO)
    msg = ("Hyperparameter tuning (stages 2-5) on the validation lectures\n\n" + reason +
           ".\nSummary: artifacts/ft_work_lr/tuning_summary.md; chosen settings: tuning_result.json.\n"
           "Committed automatically by scripts/tune_whisper.py.\n\n"
           "Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>\n")
    subprocess.run(g + ["commit", "-q", "-m", msg], cwd=REPO)
    for _ in range(3):
        if subprocess.run(g + ["push", "origin", "main"], cwd=REPO).returncode == 0:
            break
        time.sleep(30)
    say("finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
