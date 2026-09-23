# Final run on the full ground truth (random video split)

Test lectures (never used in tuning): BanglaASR11, BanglaASR15, BanglaASR19, BanglaASR27, BanglaASR8, BanglaASR9, 1.05 h. Validation lectures BanglaASR12, BanglaASR14, BanglaASR2 (train-only). Settings: `F:\thesisP2\thesisP2\artifacts\ft_work_tune5h\tuning_result.json`.
| run | decode | clips | WER median | WER: wins, direction, Wilcoxon | CER median | CER: wins, direction, Wilcoxon | runaway clips |
|---|---|---|---|---|---|---|---|
| seed 42 | greedy | 177 | 93.9 -> 189.8 | 17/177, worse, p = 0.0e+00 | 67.7 -> 118.7 | 35/177, worse, p = 0.0e+00 | 13 -> 82 |
| seed 1 | greedy | 177 | 93.9 -> 41.7 | 168/177, better, p = 0.0e+00 | 67.7 -> 16.2 | 167/177, better, p = 0.0e+00 | 13 -> 2 |
