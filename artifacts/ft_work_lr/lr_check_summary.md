# Learning-rate check (validation set, not the test set), 3060, 2026-09-22

Validation lectures BanglaASR2 (A), BanglaASR12 (B), BanglaASR14 (C), fixed and committed before
any run (data/splits/lr_validation.json). Same recipe except the learning rate: whisper-large-v3-turbo
+ LoRA r16, 8 epochs, batch 8, seed 42, gradient checkpointing, greedy decoding. Pick the rate with
the lowest validation CER median; the test set is never used for this.

| run | decode | clips | WER median | WER: wins, direction, Wilcoxon | CER median | CER: wins, direction, Wilcoxon | runaway clips |
|---|---|---|---|---|---|---|---|
| lr 5e-4 | greedy | 102 | 96.7 -> 66.2 | 79/102, better, p = 9.9e-07 | 73.2 -> 45.9 | 76/102, better, p = 2.8e-07 | 8 -> 7 |
| lr 1e-3 | greedy | 102 | 96.7 -> 64.8 | 80/102, better, p = 6.3e-09 | 73.2 -> 45.4 | 78/102, better, p = 5.6e-09 | 8 -> 7 |
| lr 2e-3 | greedy | 102 | 96.7 -> 67.6 | 82/102, better, p = 8.2e-10 | 73.2 -> 42.1 | 80/102, better, p = 5.9e-10 | 8 -> 4 |
