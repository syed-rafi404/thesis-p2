# Hyperparameter tuning plan (written and committed 2026-09-22 ~20:40, before any tuning result)

Committed while the first stage was still training and before any validation score existed, so
the choices below cannot have been shaped by the results.

## Data

- **Validation set**: BanglaASR2 (lecturer A), BanglaASR12 (B), BanglaASR14 (C), 34.2 min, chosen
  at random (seed 2026, ~20% of each lecturer's minutes; `data/splits/lr_validation.json`,
  committed before any run). Used only to choose hyperparameters. Train-only in every later split
  (`prepare_data.py --never-test`, applied automatically by `run_p3_experiment.py`), so no
  choice made on it is ever scored on it.
- **Tuning training set**: every other lecture with ground truth on 2026-09-22 (126.8 min).
- The **test set** of the final runs is not touched by tuning.

## Fixed throughout

whisper-large-v3-turbo + LoRA, batch 8, gradient checkpointing (identical learning, less memory),
bf16, greedy decoding, lora_alpha = 2 x rank (keeps the LoRA scaling fixed while the rank
changes). **Default (the recipe behind every published number)**: learning rate 1e-3, rank 16,
q_proj + v_proj, 8 epochs.

## Search, in stages (each stage keeps the best of the one before)

1. Learning rate: 5e-4, 1e-3, 2e-3 (rank 16, q+v, 8 epochs, seed 42).
2. LoRA rank: 8 and 32 at the best learning rate (16 comes from stage 1).
3. Adapted layers: q_proj, k_proj, v_proj, out_proj (all attention projections) at the best
   learning rate and rank, against q+v.
4. Epochs: from the validation loss the trainer records after each epoch of the best run so far.
   If the loss at epoch 8 is within 2% of its minimum, keep 8. Otherwise train once with the
   epoch count at the minimum and keep whichever has the lower validation CER.
5. Stability: the best configuration again with seed 1.

## Selection rule

- Score: median per-clip CER of the fine-tuned model on the validation set (WER breaks ties).
- The best configuration is the one with the lowest score.
- **Noise rule**: if the best beats the default by less than the difference between its own two
  seeds (stage 5), the gain is within run-to-run noise and **the default is kept**.
- The chosen configuration is written to `artifacts/ft_work_lr/tuning_result.json` and used
  unchanged for the 6 h and 10 h runs (`run_p3_experiment.py --tuned`).

## Repeat on the full training data (added 2026-09-22 ~20:50, before any stage-1 result)

When the ~6 h of ground truth is complete, the whole procedure above is repeated, unchanged, on
it: same stages, same values, same score, same noise rule, same three validation lectures.
- First the final test lectures are fixed (the `--split-by video --split-seed 0` split with the
  validation lectures locked out). They are **excluded from tuning entirely**.
- Tuning trains on everything else except the validation lectures and scores on the validation
  lectures, as above.
- **That result supersedes the 2.1 h one**, and the 6 h and 10 h runs use it. The 2.1 h run of
  2026-09-22 night is a rehearsal of the procedure and the fallback if the full data comes too
  late to tune on. The 10 h run reuses the 6 h settings without re-tuning.

## Limits, stated in advance

Tuning uses the ~2.1 h of training lectures available on 2026-09-22, not the full 6 h or 10 h; the
chosen values are applied to the larger runs without re-tuning. One seed per candidate (stages
1-4); noise measured on the winner only.
