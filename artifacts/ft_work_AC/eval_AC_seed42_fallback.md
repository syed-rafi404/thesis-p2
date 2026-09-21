# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_AC_seed42`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 57 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 78.5% |
| WER, per clip mean | 95.4% | 92.4% |
| WER, whole split | 84.6% | 63.7% |
| CER, per clip median | 73.4% | 53.7% |
| CER, per clip mean | 73.8% | 64.7% |
| Term recall | 66.5% | 84.0% |
| Term precision | 79.2% | 81.1% |
| Term F1 | 72.3% | 82.5% |
| Clips that run away | 1 of 184 | 5 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 123 of 184 clips. Wilcoxon signed-rank p = 7.36e-09, sign test p = 5.69e-06.
- **CER**: fine-tune wins on 142 of 184 clips. Wilcoxon signed-rank p = 8.44e-15, sign test p = 6.76e-14.

Paired test on the mean per-clip WER, for reference: p = 0.9872 (sign-flip Monte Carlo, n=171, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amr or gate complete.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so ajke amra deklam total char ta gates, which are universal gates and, and nor, and aa exclusive gay, x or and x nor.

**BanglaASR9/seg_035.wav**

- reference: pachta. toh divided by 5 kore je result ta ashbe sheitai kintu ami ei query theke peye jabo.
- base: after some time, we will add the total to the 5. we will add 5 to 5 and we will get the result.
- tuned: toh dvaret by five kore jire jalte ashbe, setai kintu ami ek veri theke peye jabo.

**BanglaASR6/seg_040.wav**

- reference: next, or er jodi logic circuit ta ami dekhate chai, duita input a and b, tahole logic gate ta dekhte hobe, side diye ektu pointy, a plus b equals to x.
- base: next, if we want to see the logic side, we will see two inputs a and b. now, we will see the logic gate.
- tuned: ne, arel jodi logic sai kitta ami dekhte chai, duita input a and b, tahole logic gate ta dekhte hobe type diye ektu pointing. a plus b equals to x.

**BanglaASR9/seg_036.wav**

- reference: so ekhane amar alada kore complication ba alada kore cgpa ber kore kore average ba sum egula kintu korte hocche na. ami easily eshob functions use kore ami aa value ta jene felte parchi.
- base: so, here i am using these functions easily.
- tuned: so ekhane amar etu alada kore complication ba alada kore cgpa er kola ber kore kore, average ba sum eigora kintu korte hocche na, easily, ish of functions u use kore ami aa value ta jene feldhe pacchi.okay.
