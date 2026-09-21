# Fine-tune evaluation: base vs LoRA

Base model: `D:\T2520875\thesisP2\ft_work\models\whisper-small`
Adapter: `D:\T2520875\thesisP2\ft_work\curve\adapter_all`
Split: `test.jsonl`, clips scored: 184

All text is compared after `normalize_banglish()` from `finetune/prepare_data.py`.

Decoding: greedy, then Whisper's loop safeguard for both models alike: a clip whose transcript has gzip compression ratio above 2.4 is decoded again with sampling at T = 0.2, 0.4, 0.6, 0.8, 1.0 in turn (seed 0) until it no longer looks like a loop. Fell back: base 9, tuned 54 clips. Still looping after T = 1.0: base 0, tuned 0.

| Metric | Base | Fine-tuned |
|---|---|---|
| WER, per clip median | 95.0% | 83.3% |
| WER, per clip mean | 95.4% | 88.0% |
| WER, whole split | 84.6% | 66.2% |
| CER, per clip median | 73.4% | 58.4% |
| CER, per clip mean | 73.8% | 60.7% |
| Term recall | 66.5% | 84.7% |
| Term precision | 79.2% | 85.0% |
| Term F1 | 72.3% | 84.8% |
| Clips that run away | 1 of 184 | 4 of 184 |

Means are reported for completeness but are dominated by a few clips where a
model falls into a repetition loop and emits far more words than were spoken,
which pushes error rates above 100%. The rank-based tests below are the ones
to read.

- **WER**: fine-tune wins on 119 of 184 clips. Wilcoxon signed-rank p = 4.82e-08, sign test p = 8.38e-05.
- **CER**: fine-tune wins on 142 of 184 clips. Wilcoxon signed-rank p = 7.90e-14, sign test p = 6.76e-14.

Paired test on the mean per-clip WER, for reference: p = 0.0640 (sign-flip Monte Carlo, n=168, 20000 resamples).

Term F1 here is exact matching against a fixed 82-word English lexicon,
reported only so these numbers sit on the same scale as the 73.9% baseline.

## Examples

**BanglaASR7/seg_032.wav**

- reference: so ami ei formula diye lengthy process complete na kore ami kintu shortcut e ei x-or er output ta dekhe nite pari.
- base: so, i am going to write this as 1 and this as 1. so, i am not completing the lengthy process with this formula. i am going to write this in short.
- tuned: so ami ei formula diye lengthy process complete na kore ami kintu short kaite ei exore output ta dhoro.

**BanglaASR7/seg_010.wav**

- reference: eta gelo amar or gate complete.
- base: 1 plus 1, 1. ita gallow amar or gate comptries.
- tuned: eta gelo amr gate complete.

**BanglaASR6/seg_033.wav**

- reference: tar mane, amar duita input thakbe ekta output thakbe, duitar multiplication input er multiplication hoye ami output ta pabo. ekta jodi zero thake jekono output er jekono input er moddhe tahole kintu ami zero as an output peye jabo.
- base: so, this is our and gate. so, we will put two inputs and one output. we will get two inputs and one output. if one is zero, then we will get zero as output. now, we will move to the next fundamental gate.
- tuned: toh amra duita input thakbe, ekta output thakbe, duita multiplication, input er multiplication hoye ami output ta pabo, ekta jodi zero thake jekono input er moddhe, tahole kintu zero as a output peye jabo.

**BanglaASR6/seg_040.wav**

- reference: next, or er jodi logic circuit ta ami dekhate chai, duita input a and b, tahole logic gate ta dekhte hobe, side diye ektu pointy, a plus b equals to x.
- base: next, if we want to see the logic side, we will see two inputs a and b. now, we will see the logic gate.
- tuned: next, orre ei jodi logic sae kitte ani dekhate chai, duita input a and b, tahole logic gate ta dekhte hobe, type diye ektu pointing, a plus b equals to x.

**BanglaASR7/seg_018.wav**

- reference: amake first e and korte hobe. and mane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab er upore ekta whole bar chole ashbe.
- base: input is a, input is a, input is b, then the output will be the first end, end means multiplication, so a into b. now what i will do is not, so a b is a whole
- tuned: tabe, output ki habe amake first a? end korte hobe. andh maane ki chilo? multiplication. so a into b. erpor ami ki korbo? not korbo. so ab eropore ekta whole bar korte hobe.
