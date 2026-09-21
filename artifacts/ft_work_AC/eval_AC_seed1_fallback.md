# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work_AC\lora_AC_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 63 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 76.9% |
| WER, per clip mean | 95.4% | 88.8% |
| WER, whole split | 84.6% | 65.4% |
| CER, per clip median | 73.4% | 55.3% |
| CER, per clip mean | 73.8% | 60.9% |
| Term recall | 66.5% | 85.8% |
| Term precision | 79.2% | 84.0% |
| Term F1 | 72.3% | 84.9% |
| Clips that run away | 1 of 184 | 7 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 124 of 184 clips. Wilcoxon signed-rank p = 1.33e-08, sign test p = 2.74e-06.
- **CER**: fine-tune wins on 141 of 184 clips. Wilcoxon signed-rank p = 7.33e-14, sign test p = 2.26e-13.

Paired test on the mean per-clip WER, for reference: p = 0.1233 (sign-flip Monte Carlo, n=172, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lendy process complete na kore, ami kintu short kite ei exor a output ta dekhe.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so ajke amra dekhlam total char ta gits, which are universal gits and and nor, and aa exclusive gei, x or and x nor.

**BanglaASR7/seg_000.wav**

- reference: hello everyone, welcome to the second class of digital logic design. so goto class e amra ki dekhechilam? kichu fundamental gates er amra introductory lesson dekhechilam.
- base: hello everyone, welcome to the second class of digital logic design. so, what did you see in the gauta class? i saw some introductory lessons on the fundamental gate set. so, today we will talk about universal gate.
- tuned: hello everyone, welcome to the second class of digital logic design. so goto class e amra ki dekhechilam? kichhu? fundamental gates er amra introductory lesson dekhechilam. so ajke ashe amar universal gate.

**BanglaASR6/seg_035.wav**

- reference: so ekhon amra dekhbo or gate. and gate er motoi ekhaneo similar pattern follow hobe. amar ekta physical device thakbe sheta hocche or gate. duitar moddhe ekhane duita input jabe and ekta output ber hobe.
- base: so, now we will see or gate and gate's motoi ekhanau similar pattern follow habi. amar aktar physical device kaate sheta hoche or gate, 2ter modde ekhanne 2ter input jabhe and aktar output per habi. suppose input hauche a and output hauche a.
- tuned: so ekhon amra dekhbo or gate. and gate er moto-e ekhaneo similar pattern follow hobe. amar ekta physical device karto e, sheta hocche or gate duitar moddhe ekhane duita input jabe and ekta output per hobe.

**BanglaASR9/seg_036.wav**

- reference: so ekhane amar alada kore complication ba alada kore cgpa ber kore kore average ba sum egula kintu korte hocche na. ami easily eshob functions use kore ami aa value ta jene felte parchi.
- base: so, here i am using these functions easily.
- tuned: so ekhane amar etu alada kore complication ba alada kore cgpa korar bear kore kore, average ba sum egula kintu korte hoche na, ami easily, ish of functions use kore, ami aa value ta jene feldhe pachchi.
