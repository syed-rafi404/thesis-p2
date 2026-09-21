# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_v1_repro_5090\lora_run`
Split: `test.jsonl`, clips scored: 137

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 8, tuned 23 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.7% | 77.4% |
| WER, per clip mean | 96.3% | 87.8% |
| WER, whole split | 85.4% | 60.7% |
| CER, per clip median | 74.1% | 58.5% |
| CER, per clip mean | 74.9% | 62.4% |
| Term recall | 68.9% | 89.3% |
| Term precision | 79.4% | 82.5% |
| Term F1 | 73.8% | 85.8% |
| Clips that run away | 1 of 137 | 2 of 137 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 89 of 137 clips. Wilcoxon signed-rank p = 5.77e-08, sign test p = 5.81e-04.
- **CER**: fine-tune wins on 109 of 137 clips. Wilcoxon signed-rank p = 7.64e-14, sign test p = 1.74e-12.

Paired test on the mean per-clip WER, for reference: p = 0.3411 (sign-flip Monte Carlo, n=126, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lengthy process complete na kore ann kintu shortcut e ei exor er output ta dekhi.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amar or gate complete.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so ajke amra dekhlam total char ta gates which are universal gates and nor and aa exclusive gate, x or and x nor.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a, input is b, then the output will be the first end, end means multiplication, so a into b. now what i will do is not, so a b is a whole
- tuned: tabe ki hobe? abake first a end korte hobe. and baani ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so a, b eropore ekta whole bar korte hobe.

**BanglaASR8/seg_038.wav**

- reference: so ajker class e amra dekhlam aa dbms ki, dbms kivabe kaj kore, dbms er table kivabe create korte hoy through sql. so next class e amra aro kichu operations gula dekhbo.
- base: last time.
- tuned: so ajker class e amra dekhlam dbms ki dbms ki babe kaaj kore, dbms er trivial kivabe create korte hoy chou sqr. so next class e amra aro kichu operations kula dekhmai.
