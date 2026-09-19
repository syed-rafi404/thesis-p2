# Multimodal Banglish Classroom Summarizer

## Master's Thesis Project (P2 Phase)

A multimodal AI system that processes **Audio (Speech)** and **Visuals (Whiteboard)** from classroom recordings to automatically generate comprehensive lecture notes. Designed specifically for **Banglish** (Bengali + English code-mixed) academic content.

> **Current Status**: P2 Complete - Full evaluation on 9 BanglaASR videos with ground truth

---

## 🎯 Research Contributions

| # | Contribution | Description | Status | Key Metric |
|---|--------------|-------------|--------|------------|
| 1 | **BanglaASR Benchmark** | First ground-truth dataset for Banglish technical lectures | ✅ **Working** | 9 videos, ~73K chars |
| 2 | **Term-Based Evaluation** | Metrics designed for Romanized code-mixed languages | ✅ **Working** | 73.9% Term F1 |
| 3 | **Multimodal Pipeline** | Complete video-to-notes processing system | ✅ **Working** | End-to-end functional |
| 4 | **Anti-Hallucination** | Post-processing to remove ASR repetition loops | ✅ **Working** | Removes excess reps |
| 5 | Visual-Biased ASR | Bias Whisper's logits toward whiteboard keywords | ❌ Failed | Causes hallucinations |
| 6 | Gaze Tracking | Detect lecturer pointing using YOLOv8-Pose | ❌ Failed | 0 detections |

---

## 📊 P2 Evaluation Results (Official)

### Primary Metrics (9 Videos with Ground Truth)

| Metric | Average | Best Video | Best Value |
|--------|---------|------------|------------|
| **Term Recall ↑** | 66.5% | BanglaASR8 (DBMS) | 76.9% |
| **Term Precision ↑** | 83.6% | BanglaASR3 (Conditionals) | 88.2% |
| **Term F1 ↑** | 73.9% | BanglaASR3 (Conditionals) | 79.6% |
| Fuzzy Similarity | 44.8% | BanglaASR3 | 47.0% |
| ROUGE-L | 18.5% | BanglaASR7 | 26.8% |

> **Note**: WER excluded - not suitable for Romanized Banglish due to transliteration variance

### Per-Video Results

| Video | Topic | Term Recall | Term Precision | Term F1 |
|-------|-------|-------------|----------------|---------|
| BanglaASR1 | Python Variables & DataTypes | 62.0% | 81.6% | 70.5% |
| BanglaASR2 | Python Input Functions | 68.7% | 84.7% | 75.8% |
| BanglaASR3 | Python Conditionals (if/elif/else) | 72.6% | **88.2%** | **79.6%** |
| BanglaASR4 | Python Loops (while/for) | 51.7% | 78.7% | 62.4% |
| BanglaASR5 | Python Lists, Tuples, Arrays | 63.0% | 87.3% | 73.2% |
| BanglaASR6 | Digital Logic Design (Gates) | 60.0% | 86.4% | 70.8% |
| BanglaASR7 | DLD Universal & Exclusive Gates | 68.6% | 82.8% | 75.0% |
| BanglaASR8 | DBMS Introduction (SQL) | **76.9%** | 80.6% | 78.7% |
| BanglaASR9 | SQL SELECT Queries | 75.4% | 82.1% | 78.6% |

### Why WER Is Excluded

Traditional Word Error Rate is **not suitable** for Romanized Banglish because:
1. **Transliteration Variance**: Multiple valid spellings ("amra" vs "aamra" vs "amraa")
2. **No Standard Orthography**: Romanized Bengali has no standardized spelling rules
3. **Misleading Results**: High WER doesn't indicate poor content capture

**Better Approach**: Term-based metrics (Recall, Precision, F1) with fuzzy matching

---

## 🖥️ Hardware Requirements

| Component | Specification |
|-----------|---------------|
| **OS** | Windows 11 (tested) / Linux |
| **GPU** | NVIDIA RTX 3090 (24GB VRAM) or equivalent |
| **CUDA** | 12.4+ |
| **Python** | 3.10 |

---

## 🧠 Models Used

| Component | Model | VRAM | Purpose |
|-----------|-------|------|---------|
| **ASR (Whisper)** | `openai/whisper-large-v3-turbo` | ~3 GB | English/Banglish speech-to-text |
| **ASR (Bengali)** | `bangla-speech-processing/BanglaASR` | ~0.5 GB | Pure Bengali (Wav2Vec2 fine-tuned) |
| **VLM** | `Qwen/Qwen2.5-VL-7B-Instruct` | ~15 GB | Whiteboard OCR + keyword extraction |
| **LLM** | `Qwen/Qwen2.5-7B-Instruct` | ~14 GB / ~5 GB (4-bit) | Lecture note generation |
| **Pose** | `YOLOv8n-Pose` | ~0.5 GB | Hand pose for gaze tracking |

> **Note**: Models are loaded/unloaded sequentially via `ModelRegistry` to fit in 24GB VRAM.

---

## 📦 Installation

```powershell
# 1. Create conda environment
conda create -n thesis_v2 python=3.10 -y
conda activate thesis_v2

# 2. Install PyTorch with CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify installation
python verify_stack.py
```

---

## 🚀 Quick Start

### Process a Single Video
```powershell
# Full pipeline (all novelties)
python run_thesis.py "data/raw/lecture.mp4" -o "output/my_lecture"

# Live mode (4-bit LLM for VRAM savings)
python run_thesis.py "data/raw/lecture.mp4" --live --interval 45

# Fast demo (mock VLM)
python run_thesis.py "data/raw/lecture.mp4" --mock --skip-gaze
```

### Run P2 Evaluation
```powershell
# Generate evaluation results
python scripts/p2_evaluation.py

# Evaluate existing transcripts against ground truth
python scripts/evaluate_existing_transcripts.py

# Full system comparison
python scripts/evaluate_full_system.py
```

### Batch Process All Videos
```powershell
python batch_process.py              # All videos in data/raw/
python batch_process.py --limit 3    # First 3 videos only
```

---

## 📁 Project Structure

```
thesisP2/
├── run_thesis.py                    # 🚀 Main pipeline orchestrator
├── batch_process.py                 # Batch processing script
├── verify_stack.py                  # Hardware verification
├── THESIS_P2_PROGRESS_LOG.md        # 📋 P2 progress and results
├── README.md                        # This file
│
├── P2/                              # 📄 Thesis LaTeX documents
│   ├── main.tex                     # Main thesis document
│   └── chapters/
│       └── chapter_1.tex            # Introduction chapter
│
├── P2_REPORT/                       # 📊 P2 evaluation reports
│   ├── EVALUATION_SUMMARY.md        # Summary of 9-video evaluation
│   ├── evaluation_results.json      # Raw metrics data
│   └── dataset_info.json            # Dataset metadata
│
├── src/
│   ├── ingest_video.py              # FFmpeg audio + frame extraction
│   ├── model_registry.py            # Singleton GPU model management
│   │
│   ├── audio/
│   │   ├── transcriber.py           # Whisper ASR (visual bias disabled)
│   │   ├── transcriber_specialized.py  # BanglaASR for Bengali
│   │   ├── visual_bias_processor.py # LogitsProcessor (failed approach)
│   │   ├── dual_asr_fusion_transliterate.py  # Transliteration fusion
│   │   └── bengali_transliterate.py # Bengali → Roman mapping
│   │
│   ├── vision/
│   │   ├── whiteboard_ocr.py        # Qwen2.5-VL whiteboard OCR
│   │   ├── structured_extractor.py  # Structured extraction
│   │   └── preprocessor.py          # Image enhancement
│   │
│   ├── research/
│   │   └── gaze_tracker.py          # YOLOv8-Pose pointing detection
│   │
│   ├── fusion/
│   │   ├── aligner.py               # Audio-visual alignment
│   │   └── temporal_context.py      # Temporal keyword mapping
│   │
│   ├── summarizer/
│   │   └── generator.py             # LLM lecture notes
│   │
│   └── evaluation/
│       ├── evaluator.py             # Term-based metrics + fuzzy matching
│       ├── quality_evaluator.py     # Lecture note quality scoring
│       ├── cross_modal_verifier.py  # Cross-modal verification
│       ├── frequency_aware_cmv.py   # CMV-F (frequency-aware)
│       └── self_correcting_pipeline.py  # Self-Correcting pipeline
│
├── scripts/
│   ├── p2_evaluation.py             # 📊 Official P2 evaluation
│   ├── evaluate_existing_transcripts.py  # Evaluate vs ground truth
│   ├── evaluate_full_system.py      # Full comparison
│   └── analyze_cmv_failure.py       # Why original CMV fails
│
├── data/
│   ├── raw/                         # Input lecture videos
│   └── ground_truth/                # Manual transcriptions
│       ├── BanglaASR1_ground_truth.txt  # ✅ Python Variables
│       ├── BanglaASR2_ground_truth.txt  # ✅ Python Input
│       ├── BanglaASR3_ground_truth.txt  # ✅ Python Conditionals
│       ├── BanglaASR4_ground_truth.txt  # ✅ Python Loops
│       ├── BanglaASR5_ground_truth.txt  # ✅ Lists/Tuples/Arrays
│       ├── BanglaASR6_ground_truth.txt  # ✅ DLD Logic Gates
│       ├── BanglaASR7_ground_truth.txt  # ✅ DLD Universal Gates
│       ├── BanglaASR8_ground_truth.txt  # ✅ DBMS Introduction
│       └── BanglaASR9_ground_truth.txt  # ✅ SQL SELECT
│
└── output/
    ├── P2_EVALUATION_TABLES.md      # 📄 Tables for paper
    ├── p2_evaluation_results.json   # Raw evaluation data
    └── <video_name>/
        ├── final_lecture_notes.md
        ├── transcript_whisper_baseline.txt
        ├── visual_keywords.json
        └── evaluation.json
```

---

## 🔬 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: LECTURE VIDEO (.mp4)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│   TRACK A: AUDIO            │   │   TRACK B: VISION           │
│                             │   │                             │
│  • Whisper large-v3-turbo   │   │  • Qwen2.5-VL-7B OCR        │
│  • Anti-hallucination post  │   │  • Structured extraction    │
│  • BanglaASR (Bengali)      │   │  • Keyword identification   │
│                             │   │                             │
└─────────────────────────────┘   └─────────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MULTIMODAL FUSION                            │
│                                                                 │
│  • Cross-modal verification (visual ground truth)               │
│  • Term extraction and fuzzy matching                           │
│  • Temporal alignment of keywords                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                LLM SUMMARIZATION (Qwen2.5-7B)                   │
│  Input: Transcript + Structured Visual Context                  │
│  Output: Markdown Lecture Notes                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Evaluation Metrics

### Term-Based Metrics (Primary)
- **Term Recall**: % of ground truth technical terms found in transcript
- **Term Precision**: % of transcript terms that are correct
- **Term F1 Score**: Harmonic mean of recall and precision

### Secondary Metrics
- **Fuzzy Similarity**: Character-level similarity with transliteration tolerance
- **ROUGE-L**: Longest common subsequence similarity
- **BLEU**: N-gram precision (limited utility for code-mixed)

### Excluded Metric
- **WER**: Word Error Rate excluded due to transliteration variance penalizing valid outputs

---

## 🔬 Key Research Findings

### What Works ✅
1. **Whisper ASR**: Strong baseline for English/Banglish content
2. **VLM Whiteboard OCR**: Qwen2.5-VL extracts keywords accurately
3. **Anti-Hallucination**: Removes Whisper repetition loops effectively
4. **Term-Based Evaluation**: Better captures practical utility than WER
5. **LLM Summarization**: Generates quality lecture notes

### What Failed ❌
1. **Visual Bias Token Boosting**: Causes hallucinations (-4.7% recall)
   - Root cause: Creates self-reinforcing loops
   - Visual terms get boosted → appear more → get boosted more
2. **Gaze Tracking**: 0 detections across all videos
3. **Dual ASR Fusion**: Limited benefit in current implementation

### Key Insight
Visual bias during ASR decoding is fundamentally flawed for code-switching lectures.
**Better approach**: Use visual information for post-hoc verification and cross-modal grounding.

---

## 📊 Dataset: BanglaASR Benchmark

| Property | Value |
|----------|-------|
| **Total Videos** | 9 |
| **Total Ground Truth** | ~73,000 characters |
| **Domains** | Python (5), DLD (2), DBMS (2) |
| **Video Type** | Real classroom recordings |
| **Language** | Banglish (Bengali + English code-mixed) |

### Topics Covered
- **Python**: Variables, Input/Output, Conditionals, Loops, Data Structures
- **DLD**: Logic Gates (AND/OR/NOT), Universal Gates (NAND/NOR)
- **DBMS**: Introduction, SQL SELECT queries

---

## 📋 For LLM Context

See [THESIS_CONTEXT_SUMMARY.md](THESIS_CONTEXT_SUMMARY.md) for a comprehensive summary including:
- All experiments tried
- Success/failure analysis
- Code structure explanation
- Metrics and results
- Future work recommendations

See [P2_REPORT/](P2_REPORT/) for official evaluation results:
- [EVALUATION_SUMMARY.md](P2_REPORT/EVALUATION_SUMMARY.md) - 9-video evaluation summary
- [evaluation_results.json](P2_REPORT/evaluation_results.json) - Raw metrics data

---

## 📄 CLI Reference

```powershell
python run_thesis.py <video_path> [options]

Options:
  -o, --output DIR    Output directory (default: output/<video_name>)
  --interval SEC      Frame extraction interval (default: 30)
  --live              Use 4-bit quantized LLM (saves VRAM)
  --mock              Use mock VLM (faster testing)
  --skip-gaze         Skip gaze tracking
```

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen2-VL) - Vision-language model
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Pose estimation
- [Hugging Face Transformers](https://huggingface.co/transformers/) - Model infrastructure
- [thefuzz](https://github.com/seatgeek/thefuzz) - Fuzzy string matching

---

## 📊 Summary Statement

> *"Our multimodal lecture transcription system achieved **73.9% Term F1** on real Banglish classroom recordings, with **83.6% precision** in technical term detection and **66.5% recall** across 9 videos covering Python, DLD, and DBMS topics. The system uses Whisper for ASR, Qwen2.5-VL for visual extraction, and term-based evaluation metrics designed for Romanized code-mixed languages."*

---

*Last Updated: February 3, 2026*
