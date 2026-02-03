# P2 EVALUATION SUMMARY

**Generated**: February 03, 2026  
**Dataset**: 9 BanglaASR Real Classroom Recordings

---

## Executive Summary

| Metric | Average | Best Video | Best Value |
|--------|---------|------------|------------|
| **Term Recall ↑** | 66.5% | BanglaASR8 | 76.9% |
| **Term Precision ↑** | 83.6% | BanglaASR3 | 88.2% |
| **Term F1 ↑** | 73.9% | BanglaASR3 | 79.6% |

> **Note**: WER excluded (not suitable for Romanized Banglish)

---

## Results by Video

| # | Video | Topic | Term Recall | Term Precision | Term F1 |
|---|-------|-------|-------------|----------------|---------|
| 1 | BanglaASR1 | Python Variables | 62.0% | 81.6% | 70.5% |
| 2 | BanglaASR2 | Python Input | 68.7% | 84.7% | 75.8% |
| 3 | BanglaASR3 | Conditionals | 72.6% | **88.2%** | **79.6%** |
| 4 | BanglaASR4 | Loops | 51.7% | 78.7% | 62.4% |
| 5 | BanglaASR5 | Lists/Tuples/Arrays | 63.0% | 87.3% | 73.2% |
| 6 | BanglaASR6 | DLD Logic Gates | 60.0% | 86.4% | 70.8% |
| 7 | BanglaASR7 | Universal Gates | 68.6% | 82.8% | 75.0% |
| 8 | BanglaASR8 | DBMS Introduction | **76.9%** | 80.6% | 78.7% |
| 9 | BanglaASR9 | SQL SELECT | 75.4% | 82.1% | 78.6% |

---

## Key Findings

1. **Average Term Recall: 66.5%** - System captures 2/3 of technical terms from noisy Banglish audio
2. **Average Term Precision: 83.6%** - High accuracy when terms are detected
3. **Average Term F1: 73.9%** - Good balance between recall and precision
4. **Best Performing**: BanglaASR3 (Conditionals) with 79.6% F1
5. **Highest Recall**: BanglaASR8 (DBMS) with 76.9% term capture

---

## Why WER Is Excluded

WER (Word Error Rate) is **not suitable** for Romanized Banglish because:

1. **Transliteration Variance**: Multiple valid spellings exist ("amra" vs "amraa" vs "aamra")
2. **No Standard Orthography**: Romanized Bengali lacks standardized spelling rules
3. **Misleading Results**: High WER doesn't indicate poor content capture

**Better Metrics**: Term-based evaluation (Recall, Precision, F1) directly measures technical content capture.

---

## For Report/Poster

Use this summary statement:

> *"Our multimodal lecture transcription system achieved 73.9% Term F1 on real Banglish classroom recordings, with 83.6% precision in technical term detection and 66.5% recall across 9 videos covering Python, DLD, and DBMS topics."*

---

*Report generated: 2026-02-03*
