# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\lora_run_seed1`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 41 clips. Still looping after T = 1.0: base 0, tuned 1.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 82.4% |
| WER, per clip mean | 95.4% | 89.5% |
| WER, whole split | 84.6% | 67.8% |
| CER, per clip median | 73.4% | 59.4% |
| CER, per clip mean | 73.8% | 61.4% |
| Term recall | 66.5% | 84.7% |
| Term precision | 79.2% | 86.9% |
| Term F1 | 72.3% | 85.8% |
| Clips that run away | 1 of 184 | 4 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 112 of 184 clips. Wilcoxon signed-rank p = 1.03e-06, sign test p = 3.92e-03.
- **CER**: fine-tune wins on 136 of 184 clips. Wilcoxon signed-rank p = 1.10e-12, sign test p = 6.11e-11.

Paired test on the mean per-clip WER, for reference: p = 0.1840 (sign-flip Monte Carlo, n=167, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lengthy process complete na kore, ami khinto short kaite ei exore output ta diekbe.

**BanglaASR7/seg_045.wav**

- reference: pari. so ajke amra dekhlam total char ta gates which are universal gates - nand and nor and exclusive gate- x-or and x-nor. thank you.
- base: the camera x or the k easily not correct in the x naught the required filter value. so, ach camera declam total chapter gates which are universal gates and and nor andexclusive gate x or and x nor.
- tuned: so, ajke amra deklam total charter gates which are universal gates and and nor, and uh exclusive gei x or and x nor.

**BanglaASR6/seg_020.wav**

- reference: shetake ami dhorlam x. thikache? so duita input ekta gate er moddhe jacche and ekta output kintu ber hocche. so ei input gula ke ami ekhane ekta chart er moddhe likhlam.
- base: is
- tuned: sheta ke ami dhorlam x. thikache? so duita input aa ekta geite maode jacche and ekta output kintu bear hocche. so ei input gula ke, ami ekhane ekta chart a moddhe holo.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amr gate concrete.

**BanglaASR9/seg_020.wav**

- reference: tahole eita run korle ki hobe? o from student info search korbe, id equal to eita. so id equals to eitar department ta ki? math. toh ekhane amake output dekhabe only math.
- base: done. then what will be the method of this? from student info search id equals to eta. so id equals to eta is the map of my department. so here i will show the output of the math. so this is my type selector.
- tuned: dhani, tahole, eta run korle ki hobe? o, from student info, search korbe, id equals to eta. so, id equals to eta er amr department ta ki math? toh ekhane amake output dekhabe only math.
