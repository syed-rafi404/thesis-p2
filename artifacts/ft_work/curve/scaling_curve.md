# Data-scaling curve, Banglish LoRA fine-tune

Base model, greedy decoding, same held-out speaker: WER median 96.0%, CER median 74.2%, Term F1 68.3%.
Base model, fallback decoding, same held-out speaker: WER median 95.0%, CER median 73.4%, Term F1 72.3%.

A positive z means the fine-tune beats the base model on that metric.

| Training audio | Clips | Decode | WER median | CER median | Term F1 | Wins on CER | CER Wilcoxon | Runaway clips |
|---|---|---|---|---|---|---|---|---|
| 0.30 h | 54 | greedy | 94.0% | 74.3% | 68.7% | 97/184 | z = -2.76, p = 5.8e-03 | 65 |
| 0.30 h | 54 | fallback | 84.6% | 59.5% | 83.5% | 136/184 | z = +6.64, p = 3.2e-11 | 6 |
| 0.60 h | 109 | greedy | 92.6% | 64.5% | 65.9% | 116/184 | z = +0.34, p = 7.4e-01 | 48 |
| 0.60 h | 109 | fallback | 80.6% | 56.6% | 84.7% | 145/184 | z = +8.00, p = 1.3e-15 | 4 |
| 0.93 h | 172 | greedy | 92.9% | 66.2% | 57.8% | 108/184 | z = -0.64, p = 5.2e-01 | 51 |
| 0.93 h | 172 | fallback | 83.3% | 58.4% | 84.8% | 142/184 | z = +7.47, p = 7.9e-14 | 4 |

Every row uses the same held-out speaker and the same recipe; only the amount
of training audio changes. Subsets are nested and drawn with a fixed seed, so
a smaller budget is a strict subset of every larger one.
