# P2 REPORT FOLDER

**Created**: February 03, 2026

This folder contains all important P2 progress reports and evaluation results.

---

## 📁 Contents

| File | Description |
|------|-------------|
| [EVALUATION_SUMMARY.md](EVALUATION_SUMMARY.md) | Main evaluation results (Term Recall, Precision, F1) |
| [CONVERSATION_PROGRESS.md](CONVERSATION_PROGRESS.md) | Full progress log from this work session |
| [evaluation_results.json](evaluation_results.json) | Raw evaluation data (9 videos × 3 intervals) |
| [dataset_info.json](dataset_info.json) | Ground truth dataset information |

---

## 🎯 Key Results (For Report/Poster)

| Metric | Value | Meaning |
|--------|-------|---------|
| **Term Recall** | 66.5% | System captures 2/3 of technical terms |
| **Term Precision** | 83.6% | When a term is detected, it's correct 84% of the time |
| **Term F1** | 73.9% | Balanced precision-recall score |

---

## 📊 Dataset

- **Videos**: 9 BanglaASR real classroom recordings
- **Topics**: Python, DLD, DBMS/SQL
- **Ground Truth**: ~73,000 characters manually transcribed
- **Evaluation Runs**: 27 (9 videos × 3 frame intervals)

---

## ⚠️ Excluded Metrics

WER (Word Error Rate) is **excluded** because it's not suitable for Romanized Banglish evaluation due to transliteration variance.

---

*Navigate to individual files for detailed information.*
