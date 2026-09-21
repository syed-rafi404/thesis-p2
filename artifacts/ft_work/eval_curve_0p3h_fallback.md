# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\curve\adapter_0p3h`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 70 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 84.6% |
| WER, per clip mean | 95.4% | 90.6% |
| WER, whole split | 84.6% | 69.5% |
| CER, per clip median | 73.4% | 59.5% |
| CER, per clip mean | 73.8% | 62.7% |
| Term recall | 66.5% | 80.1% |
| Term precision | 79.2% | 87.2% |
| Term F1 | 72.3% | 83.5% |
| Clips that run away | 1 of 184 | 6 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 116 of 184 clips. Wilcoxon signed-rank p = 2.30e-06, sign test p = 4.97e-04.
- **CER**: fine-tune wins on 136 of 184 clips. Wilcoxon signed-rank p = 3.21e-11, sign test p = 6.11e-11.

Paired test on the mean per-clip WER, for reference: p = 0.0982 (sign-flip Monte Carlo, n=170, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lendi process complete na kore amkinto short kite ei exor a outputta dekta.

**BanglaASR6/seg_043.wav**

- reference: ekhane a bar jinishta ki? a bar hocche alternate of a. tar mane ki? tar mane hocche amar input a output a bar. input jodi 0 hoy tahole output hobe 1.
- base: output.
- tuned: ekhane a bar jiniste ki? a bar hocche alternate of a. tar mane ki? tar mane hocche amar input a and output a bar. input jodi zero hoye, tahole output hobe, tar jori zero hoye.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amr gate complicate.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so ajke amra deklam total chapter giz which are universal giz and an nor and ah exclusive gay, x or and x nor.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a, input is b, then the output will be the first end, end means multiplication, so a into b. now what i will do is not, so a b is a whole
- tuned: taude, aortpor kihabe? amake first a, end korte habe, andmani kechi lo, multiplication, so a into b. erpor ami ki korbo? not korbo, so a b eropore ekta whole but a.
