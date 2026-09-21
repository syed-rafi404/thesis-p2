# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\curve\adapter_0p6h`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 48 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 80.6% |
| WER, per clip mean | 95.4% | 88.0% |
| WER, whole split | 84.6% | 66.6% |
| CER, per clip median | 73.4% | 56.6% |
| CER, per clip mean | 73.8% | 59.0% |
| Term recall | 66.5% | 85.8% |
| Term precision | 79.2% | 83.7% |
| Term F1 | 72.3% | 84.7% |
| Clips that run away | 1 of 184 | 4 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 115 of 184 clips. Wilcoxon signed-rank p = 4.28e-07, sign test p = 8.60e-04.
- **CER**: fine-tune wins on 145 of 184 clips. Wilcoxon signed-rank p = 1.33e-15, sign test p = 1.50e-15.

Paired test on the mean per-clip WER, for reference: p = 0.0098 (sign-flip Monte Carlo, n=165, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lengthy process complete na kore, amkintu short kaite ei exore output ta dirai.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so ajke amra dekhlam total charter gates which are universal gates and nor and aa exclusive gei x or and x nor.

**BanglaASR6/seg_043.wav**

- reference: ekhane a bar jinishta ki? a bar hocche alternate of a. tar mane ki? tar mane hocche amar input a output a bar. input jodi 0 hoy tahole output hobe 1.
- base: output.
- tuned: ekhane a bar jinish te ki? a bar hocche all the net of a. tar mane ki? tar mane hocche amar input a and output a bar. input jodi zero hoe, tahole output hobe.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gello amr gate complete.

**BanglaASR6/seg_040.wav**

- reference: next, or er jodi logic circuit ta ami dekhate chai, duita input a and b, tahole logic gate ta dekhte hobe, side diye ektu pointy, a plus b equals to x.
- base: next, if we want to see the logic side, we will see two inputs a and b. now, we will see the logic gate.
- tuned: next, orehi jo di logic psych itta ani dekhate chai. duita input a and b, tahole logic gate ta dekhte hobe, psych diye e to pointing, a plus b equals to x.
