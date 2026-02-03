#!/usr/bin/env python3
"""
=============================================================================
VISUAL BIAS DECISION REPORT
=============================================================================
Master's Thesis - Research Analysis

Based on ground truth evaluation of L2 ("Creating a Design Class in a Separate File"),
this report summarizes findings and provides actionable recommendations.

Created: 2024 (Thesis Research)
=============================================================================
"""

import json
from pathlib import Path
from datetime import datetime

REPORT = """
================================================================================
VISUAL BIAS IMPACT ANALYSIS REPORT
================================================================================
Date: {date}
Video: L2 - Java OOP - Creating a Design Class in a Separate File
Duration: 6 minutes 29 seconds
Ground Truth: Manually transcribed by thesis author (6,461 characters)

--------------------------------------------------------------------------------
EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
Finding: Visual bias HURTS ASR accuracy by -12.7% term recall
Cause: Over-boosting of common words causes hallucination loops
Recommendation: DISABLE visual bias for Banglish classroom content

--------------------------------------------------------------------------------
QUANTITATIVE RESULTS
--------------------------------------------------------------------------------

                    BASELINE    VISUAL BIASED    DIFFERENCE
                    --------    -------------    ----------
Term Recall         54.4%       41.7%            -12.7%  ❌
Fuzzy Similarity    49%         42%              -7%     ❌
Unique Words        165         130              -35     ❌
Repetition Ratio    71.5%       76.7%            +5.2%   ❌

--------------------------------------------------------------------------------
CRITICAL HALLUCINATION EVIDENCE
--------------------------------------------------------------------------------
The word "Compile" appears:
  - In ground truth: 9 times (normal usage)
  - In baseline:     3 times (under-recognized but acceptable)
  - In biased:       138 times (15x over-repetition = SEVERE HALLUCINATION)

This single hallucination accounts for ~25% of the biased transcript!

--------------------------------------------------------------------------------
TERM-BY-TERM ANALYSIS (Top 20)
--------------------------------------------------------------------------------
Term          GT Count    Baseline    Biased    Winner
----          --------    --------    ------    ------
class              40          30        18    BASELINE
design             25          13         5    BASELINE
tester             17           2         9    biased
tutorial           12           6         6    TIE
file               12           6        11    biased
code               12           4         1    BASELINE
main               10           7         4    BASELINE
run                10           2         0    BASELINE
compile             9           3       138    HALLUCINATION
method              8           7         3    BASELINE
driver              6           2         2    TIE
java                6           5         5    TIE
separate            5           5         5    TIE
object              5           1         1    TIE
public              5           5         1    BASELINE
manipulate          5           1         0    BASELINE
template            4           3         1    BASELINE
save                4           3         0    BASELINE
static              4           4         4    TIE
access              3           2         1    BASELINE

SCORE: Baseline wins 11 terms, Biased wins 3 terms, Ties 6

--------------------------------------------------------------------------------
ROOT CAUSE ANALYSIS
--------------------------------------------------------------------------------
1. KEYWORD SOURCE PROBLEM:
   Visual keywords extracted: ['Compiler', 'Compilation', 'Tester', 'Java', ...]
   
   "Compiler" and "Compilation" are on the IDE interface (always visible).
   They are NOT the focus of the lecture, just UI noise.
   
2. TOKEN BOOSTING MECHANISM:
   - Whisper tokenizes "Compiler" → tokens include "Compile" subword
   - Bias adds +1.5 to "Compile" token logits every step
   - Once Whisper generates "Compile", it's reinforced by:
     a) Previous token context (autoregressive)
     b) Visual bias boost (added again)
   - Creates self-reinforcing loop → 138 repetitions

3. POST-PROCESSING LIMITATION:
   The anti-hallucination filters (remove_repetitions, remove_ngram_loops)
   run AFTER generation. They can clean up some repetition, but:
   - The damage is already done (other content was never generated)
   - Even aggressive filtering can't recover lost context

--------------------------------------------------------------------------------
ALTERNATIVE STRATEGIES TESTED
--------------------------------------------------------------------------------
Strategy            Recall    Similarity    Hallucination    Result
--------            ------    ----------    -------------    ------
baseline             9.2%        10%              0          BEST
standard_low (0.3)   3.8%         6%              0          Worse
standard_med (0.75)  3.8%         6%              0          Worse
adaptive_decay       3.8%         6%              0          Worse
filtered_keywords    3.8%         6%              0          Worse
combined             3.8%         6%              0          Worse

None of the mitigation strategies improved over baseline.

--------------------------------------------------------------------------------
THESIS IMPLICATIONS
--------------------------------------------------------------------------------
ORIGINAL HYPOTHESIS:
"Visual context from whiteboard can improve Banglish ASR accuracy"

EVIDENCE SAYS:
For code-mixed Banglish with visible UI elements, visual bias HURTS accuracy.

POSSIBLE THESIS PIVOTS:
1. NEGATIVE RESULT: Document that visual bias doesn't work for this domain
   (Still valuable - saves others from trying this approach)

2. DOMAIN-SPECIFIC: Visual bias may work for pure-English technical content
   (The original A* algorithm example might work if lecturer speaks English)

3. KEYWORD SELECTION: The problem is keyword quality, not bias mechanism
   - UI elements (Compiler, Users, Desktop) should be filtered
   - Only whiteboard-written terms should be used
   - Frame-level temporal alignment needed

4. DIFFERENT MODALITY: Instead of ASR bias, use visual context for:
   - Post-ASR correction (find-and-replace misspellings)
   - Summarization enhancement (add missed technical terms)
   - Slide/code segment identification

--------------------------------------------------------------------------------
RECOMMENDATION
--------------------------------------------------------------------------------
For the thesis defense, I recommend:

1. HONEST REPORTING: Present visual bias as a negative result with evidence
   
2. REVISED CONTRIBUTION: Focus on:
   - Multimodal lecture processing pipeline (still novel)
   - Banglish ASR with initial prompt biasing (works well)
   - Visual context for summarization (not ASR)
   
3. FUTURE WORK: Propose improved approaches:
   - Temporal alignment (match keywords to audio segments)
   - Keyword filtering (remove UI noise, keep whiteboard content)
   - Negative bias (prevent common word hallucination)

================================================================================
END OF REPORT
================================================================================
"""

def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Format report with current date
    report = REPORT.format(date=datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # Save as text
    report_path = base_path / "output/visual_bias_decision_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n💾 Report saved to: {report_path}")
    
    # Also save as structured JSON for programmatic access
    json_report = {
        "date": datetime.now().isoformat(),
        "video": "L2 - Java OOP - Creating a Design Class in a Separate File",
        "ground_truth_length": 6461,
        "findings": {
            "baseline_recall": 0.544,
            "biased_recall": 0.417,
            "recall_difference": -0.127,
            "baseline_similarity": 49,
            "biased_similarity": 42,
            "baseline_wins": 11,
            "biased_wins": 3,
            "ties": 6
        },
        "hallucination": {
            "word": "Compile",
            "ground_truth_count": 9,
            "baseline_count": 3,
            "biased_count": 138,
            "over_generation_ratio": 15.3
        },
        "recommendation": "DISABLE_VISUAL_BIAS",
        "thesis_pivot_options": [
            "Present as negative result with evidence",
            "Focus on pipeline and Banglish ASR contributions",
            "Use visual context for summarization instead of ASR",
            "Propose temporal alignment for future work"
        ]
    }
    
    json_path = base_path / "output/visual_bias_decision.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2)


if __name__ == "__main__":
    main()
