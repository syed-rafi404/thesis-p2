# Fine-tune evaluation: base vs LoRA

Base model: `openai/whisper-large-v3-turbo`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_turbo_AC_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 14, tuned 11 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 91.8% | 73.1% |
| WER, per clip mean | 96.1% | 78.7% |
| WER, whole split | 81.4% | 52.4% |
| CER, per clip median | 68.9% | 51.2% |
| CER, per clip mean | 69.2% | 55.1% |
| Term recall | 81.5% | 89.3% |
| Term precision | 83.9% | 90.3% |
| Term F1 | 82.7% | 89.8% |
| Clips that run away | 3 of 184 | 3 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 143 of 184 clips. Wilcoxon signed-rank p = 0.00e+00, sign test p = 1.96e-14.
- **CER**: fine-tune wins on 141 of 184 clips. Wilcoxon signed-rank p = 1.55e-15, sign test p = 2.26e-13.

Paired test on the mean per-clip WER, for reference: p = 0.0000 (sign-flip Monte Carlo, n=175, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_040.wav**

- reference: so ami eta x-or jehetu amar eta, so eta ekhane apply kore dicchi.
- base: zho no output ashto 0 and different input value zho no output ashto 1. so eta mi xor jehi to aamari eta so eta ekhanen
- tuned: so eta ami x or jehetu amar eta, so eta ekhane apal kache.

**BanglaASR6/seg_020.wav**

- reference: shetake ami dhorlam x. thikache? so duita input ekta gate er moddhe jacche and ekta output kintu ber hocche. so ei input gula ke ami ekhane ekta chart er moddhe likhlam.
- base: acta output bear ho vye. so, i will add x. so, duita input acta gate mou jayat x and acta output kiintu bear ho vye. so, a input gula ke, i will add a acta chart mou jayat x.
- tuned: sheta ke ami dhorlam x. thikache? so duita input aa ekta gate er moddhe jacche and ekta output kintu ber hocche. so ei input gula ke ami ekhane ekta chart er moddhe jeta chacche.

**BanglaASR6/seg_046.wav**

- reference: so eigula gelo amar kichu fundamental gates.
- base: not way, i can put b hochi. so, a gula gello amal itch fundamental gates.
- tuned: not hoy, arekta input behocche. so ei gula gelo amar kichu fundamental gain.

**BanglaASR9/seg_001.wav**

- reference: so select ki kore? select hocche shudhumatro data amar database er je table shekhan theke data retrieve kore. retrieve kore bolte? jemon dhoro ami student id 401201, ei student id-r full name ba first name, last name dekhte chacci.
- base: so select key, select ho c h e, s u dhu m a t r o d e t a b eze j e table, check a n t e k e data k e retrieve kore. retreat kore b olt e, jamon dharo, a me student id 401201. a student id, full name, first name,
- tuned: so select ki kore? select hocche shudhu matro data er amr database er je table, sheikhan theke data ke retrieve kore. detrit kore bolte, jemon dhoro ami student id 401201.

**BanglaASR6/seg_033.wav**

- reference: tar mane, amar duita input thakbe ekta output thakbe, duitar multiplication input er multiplication hoye ami output ta pabo. ekta jodi zero thake jekono output er jekono input er moddhe tahole kintu ami zero as an output peye jabo.
- base: so, this is our and gate. that means, our due to input and output has the output. due to input and multiplication, i will output. act is 0 in the same way. that is the output. now, i will show the next fundamental gate.
- tuned: toh cholo, etai hocche amar and gate. tar mane amr dui ta input thakbe, ekta output thakbe. duitar multiplication, input er multiplication hoy ami output ta pabo. ekta jodi zero thake jekono output er moddhe jekono input er moddhe tahole kintu ami zero as a output pere jabo.
