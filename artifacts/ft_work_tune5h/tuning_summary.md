# Hyperparameter tuning on the validation lectures (3060, 2026-09-22/23)

Plan committed before any result: `data/splits/tuning_plan.md`. Validation lectures BanglaASR2 (A), BanglaASR12 (B), BanglaASR14 (C), never test. Score: median per-clip CER of the fine-tuned model on the validation set (off-the-shelf Whisper on the same clips: CER 73.8%, WER 97.6%).

| Stage | Run | lr | rank | layers | epochs | seed | val CER | val WER | val loss, last / min |
|---|---|---|---|---|---|---|---|---|---|
| 1 learning rate | lr5e-4 | 5e-4 | 16 | q,v | 8 | 42 | 37.9% | 60.0% | 1.782 / 1.685 |
| 1 learning rate | lr1e-3 | 1e-3 | 16 | q,v | 8 | 42 | 42.2% | 61.9% | 1.811 / 1.667 |
| 1 learning rate | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 33.6% | 54.5% | 1.801 / 1.683 |
| 2 LoRA rank | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 33.6% | 54.5% | 1.801 / 1.683 |
| 2 LoRA rank | lr2e-3_r8 | 2e-3 | 8 | q,v | 8 | 42 | 40.1% | 64.1% | 1.813 / 1.693 |
| 2 LoRA rank | lr2e-3_r32 | 2e-3 | 32 | q,v | 8 | 42 | 126.6% | 200.0% | 4.663 / 4.663 |
| 3 adapted layers | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 33.6% | 54.5% | 1.801 / 1.683 |
| 3 adapted layers | lr2e-3_qkvo | 2e-3 | 16 | q,k,v,o | 8 | 42 | 134.7% | 174.4% | 4.877 / 2.037 |
| 4 epochs | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 33.6% | 54.5% | 1.801 / 1.683 |
| 4 epochs | lr2e-3_e5 | 2e-3 | 16 | q,v | 5 | 42 | 39.4% | 59.6% | 1.666 / 1.656 |
| 5 stability (seed 1) | lr2e-3 | 2e-3 | 16 | q,v | 8 | 42 | 33.6% | 54.5% | 1.801 / 1.683 |
| 5 stability (seed 1) | lr2e-3_s1 | 2e-3 | 16 | q,v | 8 | 1 | 39.1% | 59.6% | 1.815 / 1.681 |

**Decision:** lr2e-3 chosen: 8.6 points of CER better than the default, more than its seed-to-seed difference (5.4).

Chosen for the 6 h and 10 h runs: lr 2e-3, rank 16, q_proj + v_proj, 8 epochs (`run_p3_experiment.py --tuned`).
