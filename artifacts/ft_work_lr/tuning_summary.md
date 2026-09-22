# Hyperparameter tuning on the validation lectures (3060, 2026-09-22/23)

Plan committed before any result: `data/splits/tuning_plan.md`. Validation lectures BanglaASR2 (A), BanglaASR12 (B), BanglaASR14 (C), never test. Score: median per-clip CER of the fine-tuned model on the validation set (off-the-shelf Whisper on the same clips: CER 73.2%, WER 96.7%).

| Stage | Run | lr | rank | layers | epochs | seed | val CER | val WER | val loss, last / min |
|---|---|---|---|---|---|---|---|---|---|
| 1 learning rate | lr5e-4 | 5e-4 | 16 | q,v | 8 | 42 | 45.9% | 66.2% | 1.860 / 1.752 |
| 1 learning rate | lr1e-3 | 1e-3 | 16 | q,v | 8 | 42 | 45.4% | 64.8% | 1.928 / 1.736 |
| 1 learning rate | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 42.1% | 67.6% | 1.889 / 1.740 |
| 2 LoRA rank | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 42.1% | 67.6% | 1.889 / 1.740 |
| 2 LoRA rank | lr2e-3_r8 | 2e-3 | 8 | q,v | 8 | 42 | 42.7% | 63.2% | 1.883 / 1.746 |
| 2 LoRA rank | lr2e-3_r32 | 2e-3 | 32 | q,v | 8 | 42 | 117.3% | 179.9% | 4.116 / 2.180 |
| 3 adapted layers | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 42.1% | 67.6% | 1.889 / 1.740 |
| 3 adapted layers | lr2e-3_qkvo | 2e-3 | 16 | q,k,v,o | 8 | 42 | 73.6% | 96.8% | 5.051 / 2.030 |
| 4 epochs | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 42.1% | 67.6% | 1.889 / 1.740 |
| 4 epochs | lr2e-3_e4 | 2e-3 | 16 | q,v | 4 | 42 | 45.9% | 65.9% | 1.704 / 1.704 |
| 5 stability (seed 1) | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 42.1% | 67.6% | 1.889 / 1.740 |
| 5 stability (seed 1) | lr2e-3_s1 | 2e-3 | 16 | q,v | 8 | 1 | 43.8% | 68.3% | 1.924 / 1.749 |

**Decision:** lr2e-3 chosen: 3.3 points of CER better than the default, more than its seed-to-seed difference (1.7).

Chosen for the 6 h and 10 h runs: lr 2e-3, rank 16, q_proj + v_proj, 8 epochs (`run_p3_experiment.py --tuned`).
