# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 1) until it no longer looks like a loop. Fell back: base 9, tuned 64 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 94.9% | 82.0% |
| WER, per clip mean | 95.0% | 90.6% |
| WER, whole split | 84.1% | 67.5% |
| CER, per clip median | 72.7% | 57.6% |
| CER, per clip mean | 73.4% | 63.3% |
| Term recall | 69.8% | 86.1% |
| Term precision | 78.4% | 84.6% |
| Term F1 | 73.8% | 85.4% |
| Clips that run away | 1 of 184 | 8 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 117 of 184 clips. Wilcoxon signed-rank p = 8.46e-06, sign test p = 2.81e-04.
- **CER**: fine-tune wins on 134 of 184 clips. Wilcoxon signed-rank p = 4.17e-11, sign test p = 4.72e-10.

Paired test on the mean per-clip WER, for reference: p = 0.3567 (sign-flip Monte Carlo, n=172, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lengthy process complete na kore, ami kintu short kaite ei exore output ta dhoro.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amr or gate complete.

**BanglaASR6/seg_033.wav**

- reference: tar mane, amar duita input thakbe ekta output thakbe, duitar multiplication input er multiplication hoye ami output ta pabo. ekta jodi zero thake jekono output er jekono input er moddhe tahole kintu ami zero as an output peye jabo.
- base: so, this is our and gate. so, we will put two inputs and one output. we will get two inputs and one output. if one is zero, then we will get zero as output. now, we will move to the next fundamental gate.
- tuned: toh amra duita input thakbe, ekta output thakbe, duita multiplication, input er multiplication hoy ami output ta pabo, ekta jodi zero thake jekono input er moddhe, tahole kintu ami zero as a output peye jabo.

**BanglaASR6/seg_020.wav**

- reference: shetake ami dhorlam x. thikache? so duita input ekta gate er moddhe jacche and ekta output kintu ber hocche. so ei input gula ke ami ekhane ekta chart er moddhe likhlam.
- base: is
- tuned: sheta ke ami dhollam x. thikache? so duita input aa ekta gate ei moddhe chacche and ekta output kintu bear hocche. so ei input gula ke, ami ekhane ekta chart er moddhe chacche.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a, input is b, then the output will be the first end, end means multiplication, so a into b. now what i will do is not, so a b is a whole
- tuned: tabe, output ki habe? amake first a end korte hobe, and mane kechilo multiplication. so a into b. erpor ami ki korbo? not korbo. so ab eropore ekta whole bar korte hobe.
