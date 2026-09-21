# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run`
Split: `test_7to9.jsonl`, clips scored: 137

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 8, tuned 50 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.7% | 87.9% |
| WER, per clip mean | 96.3% | 95.4% |
| WER, whole split | 85.4% | 72.9% |
| CER, per clip median | 74.1% | 59.8% |
| CER, per clip mean | 74.9% | 66.5% |
| Term recall | 68.9% | 86.7% |
| Term precision | 79.4% | 85.9% |
| Term F1 | 73.8% | 86.3% |
| Clips that run away | 1 of 137 | 5 of 137 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 85 of 137 clips. Wilcoxon signed-rank p = 4.87e-03, sign test p = 6.05e-03.
- **CER**: fine-tune wins on 94 of 137 clips. Wilcoxon signed-rank p = 1.45e-07, sign test p = 1.57e-05.

Paired test on the mean per-clip WER, for reference: p = 0.8997 (sign-flip Monte Carlo, n=131, 20000 resamples).

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

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a, input is b, then the output will be the first end, end means multiplication, so a into b. now what i will do is not, so a b is a whole
- tuned: tabe, output ki habe? amake first a end korte hobe, and mane kechilo multiplication. so a into b. erpor ami ki korbo? not korbo. so ab eropore ekta whole bar korte hobe.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so, ajke amra deklam total charter gates which are universal gates and and nor, and aa exclusive gei, x or and x nor.

**BanglaASR9/seg_040.wav**

- reference: o kintu ekhono jane na je ami max cgpa er id ta jante chacchi.
- base: i am writing my first idea. but now i don't know what i am writing.
- tuned: kintu ekhonno jane na ami je max cgpr id ta jante chacchi.
