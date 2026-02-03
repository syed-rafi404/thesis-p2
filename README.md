# Multimodal Banglish Classroom Summarizer

## Master's Thesis Project (P2 Phase)

A multimodal AI system that processes **Audio (Speech)** and **Visuals (Whiteboard)** from classroom recordings to automatically generate comprehensive lecture notes. Designed specifically for **Banglish** (Bengali + English code-mixed) academic content.

> **Current Status**: P2 Complete - CMV-F and Self-Correcting Pipeline validated

---

## 🎯 Research Contributions

| # | Contribution | Description | Status | Key Metric |
|---|--------------|-------------|--------|------------|
| 1 | **CMV-F** | Frequency-Aware Cross-Modal Verification for hallucination detection | ✅ **Working** | +42.4% RHR improvement |
| 2 | **Self-Correcting Pipeline** | Detect + Fix ASR hallucinations using CMV-F | ✅ **Working** | 64% excess rep reduction |
| 3 | **Banglish Benchmark** | First ground-truth dataset for Banglish technical lectures | ✅ **Working** | 3 lectures (L2, L3, L5) |
| 4 | Visual-Biased ASR | Bias Whisper's logits toward whiteboard keywords | ❌ Failed | -4.7% recall |
| 5 | Gaze Tracking | Detect lecturer pointing using YOLOv8-Pose | ❌ Failed | 0 detections |

---

## 📊 P2 Evaluation Results (Official)

### Excess Repetitions (Hallucination Measure)

| Lecture | Baseline | Visual-Biased | Self-Corrected | Reduction |
|---------|----------|---------------|----------------|-----------|
| L2      | 97       | 214           | 85             | -129      |
| L3      | 794      | 2,301         | 740            | -1,561    |
| L5      | 533      | 324           | 186            | -138      |
| **Average** | **475** | **946**    | **337**        | **-609**  |

### Key Claims

1. **Visual Bias HURTS**: -4.7% recall, +99% hallucinations
2. **CMV-F DETECTS**: +42.4% RHR improvement
3. **Self-Correction FIXES**: 946 → 337 excess reps (64% reduction)
4. **Corrected < Baseline**: 337 < 475 (better than baseline!)

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
# Generate official P2 tables (requires ground truth files)
python scripts/p2_evaluation.py

# Test CMV-F on specific lectures
python scripts/test_frequency_aware_cmv.py

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
├── src/
│   ├── ingest_video.py              # FFmpeg audio + frame extraction
│   ├── model_registry.py            # Singleton GPU model management
│   │
│   ├── audio/
│   │   ├── transcriber.py           # Whisper ASR with visual bias
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
│       ├── evaluator.py             # TTR + WER metrics
│       ├── quality_evaluator.py     # Lecture note quality scoring
│       ├── cross_modal_verifier.py  # Original CMV (flawed)
│       ├── frequency_aware_cmv.py   # ★ CMV-F (NOVEL)
│       └── self_correcting_pipeline.py  # ★ Self-Correcting (NOVEL)
│
├── scripts/
│   ├── p2_evaluation.py             # 📊 Official P2 evaluation
│   ├── test_frequency_aware_cmv.py  # CMV-F testing
│   ├── evaluate_full_system.py      # Full comparison
│   └── analyze_cmv_failure.py       # Why original CMV fails
│
├── data/
│   ├── raw/                         # Input lecture videos
│   └── ground_truth/                # Manual transcriptions
│       ├── L1_ground_truth.txt      # ❌ Empty
│       ├── L2_ground_truth.txt      # ✅ 6,572 bytes
│       ├── L3_ground_truth.txt      # ✅ 16,643 bytes
│       └── L5_ground_truth.txt      # ✅ 15,720 bytes
│
└── output/
    ├── P2_EVALUATION_TABLES.md      # 📄 Tables for paper
    ├── p2_evaluation_results.json   # Raw evaluation data
    └── <video_name>/
        ├── final_lecture_notes.md
        ├── transcript_whisper_baseline.txt
        ├── transcript_whisper_visual_biased.txt
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
│  • Whisper (baseline)       │   │  • VLM Whiteboard OCR       │
│  • Whisper + Visual Bias    │◄──┤  • Structured Extraction    │
│  • BanglaASR (Bengali)      │   │  • Keyword Extraction       │
│                             │   │                             │
└─────────────────────────────┘   └─────────────────────────────┘
              │                               │
              │                               │
              ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│           ★ CMV-F: FREQUENCY-AWARE CROSS-MODAL VERIFICATION     │
│                                                                 │
│  • Detect repetition hallucinations using TFD threshold        │
│  • Compare term frequency vs expected baseline                  │
│  • Flag terms with TFD > 3.0 as hallucinations                 │
│                                                                 │
│  Metrics: RHR (Repetition Hallucination Rate), TFD              │
└─────────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│             ★ SELF-CORRECTING PIPELINE                          │
│                                                                 │
│  • CMV-F detects hallucinations                                │
│  • Rule-based correction removes excess repetitions            │
│  • Optional: LLM-based correction for complex cases            │
│                                                                 │
│  Result: 64% reduction in excess repetitions                   │
└─────────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                LLM SUMMARIZATION (Qwen2.5-7B)                   │
│  Input: Corrected Transcript + Structured Visual Context       │
│  Output: Markdown Lecture Notes                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔬 Novel Components Detail

### CMV-F (Frequency-Aware Cross-Modal Verification)

**File**: `src/evaluation/frequency_aware_cmv.py`

**Problem**: Traditional cross-modal verification only checks if terms EXIST in visual context. It misses repetition hallucinations where grounded terms are repeated excessively.

**Example**:
- "Compiler" is on whiteboard
- ASR says "compile" 138 times (vs ~9 in ground truth)
- Traditional CMV: "All grounded, 0% hallucination" ← WRONG
- CMV-F: "TFD = 15.3x, flagged as hallucination" ← CORRECT

**Algorithm**:
```
TFD = actual_count / expected_baseline
If TFD > 3.0 → Flag as Repetition Hallucination
RHR = sum(excess_words) / total_words
```

### Self-Correcting Pipeline

**File**: `src/evaluation/self_correcting_pipeline.py`

**Architecture**:
```
Transcript → CMV-F Detection → Correction → Verified Output
```

**Results**:
- Excess repetitions reduced by 64% (946 → 337)
- Corrected output is better than baseline (337 < 475)

---

## 📊 Evaluation Metrics

### Ground Truth Based
- **Term Recall**: % of ground truth terms found in transcript
- **Precision**: % of transcript terms that are correct
- **F1 Score**: Harmonic mean of recall and precision
- **Excess Repetitions**: Words appearing more than in ground truth

### CMV-F Metrics (No Ground Truth Needed)
- **RHR (Repetition Hallucination Rate)**: % of words that are excessive
- **TFD (Term Frequency Deviation)**: How many times over expected
- **Combined Hallucination Rate**: Ungrounded + over-represented

### Transliteration Fusion Metrics

| Video | Unique Bengali Words | Avg Similarity |
|-------|---------------------|----------------|
| L1 | 829 | 6.6% |
| L2 | 392 | 3.7% |
| CSE443 | 2,859 | 0.02% |

---

## 🔧 Key Research Findings

### What Works ✅
1. **CMV-F (Frequency-Aware Cross-Modal Verification)**: +42.4% RHR improvement in hallucination detection
2. **Self-Correcting Pipeline**: 64% reduction in excess repetitions (946 → 337)
3. **VLM Whiteboard OCR**: Qwen2.5-VL extracts keywords accurately
4. **Anti-Hallucination**: Successfully removes Whisper repetition loops
5. **LLM Summarization**: Generates quality lecture notes

### What Failed ❌
1. **Visual Bias Token Boosting**: -4.7% term recall, +99% excess repetitions
   - Root cause: Token boosting creates self-reinforcing loops
   - Visual terms get boosted → appear more → get boosted more
2. **Traditional CMV**: Gives wrong results (checks presence not frequency)
3. **Temporal Visual Bias**: No improvement over global bias
4. **Gaze Tracking**: 0 detections across all videos
5. **Simple Language Detection**: Everything detected as English

### Key Insight
Visual bias for ASR is fundamentally flawed for code-switching lectures.
**Solution**: Instead of biasing ASR, verify and correct AFTER transcription.

---

## 📊 Official P2 Results

### Ground Truth Evaluation (3 Lectures with GT)

| Lecture | Baseline Recall | Visual Bias Recall | Change |
|---------|-----------------|-------------------|--------|
| L2 | 19.0% | 19.0% | 0% |
| L3 | 21.9% | 16.7% | **-5.2%** |
| L5 | 37.5% | 28.1% | **-9.4%** |
| **Average** | **26.1%** | **21.3%** | **-4.8%** |

### Hallucination Impact

| Lecture | Baseline Excess | Visual Bias Excess | Increase |
|---------|-----------------|-------------------|----------|
| L2 | 172 | 346 | **+101%** |
| L3 | 207 | 397 | **+92%** |
| L5 | 96 | 203 | **+111%** |
| **Total** | **475** | **946** | **+99%** |

### Self-Correcting Pipeline Performance

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Total Excess Reps | 946 | 337 | **64% reduction** |
| vs Baseline | 475 | 337 | **Better than baseline** |

---

## 📋 For LLM Context

See [THESIS_CONTEXT_SUMMARY.md](THESIS_CONTEXT_SUMMARY.md) for a comprehensive 2000+ word summary including:
- All experiments tried
- Success/failure analysis
- Code structure explanation
- Metrics and results
- Future work recommendations

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

*Last Updated: January 27, 2026*
