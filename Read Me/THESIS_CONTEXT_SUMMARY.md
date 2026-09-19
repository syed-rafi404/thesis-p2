# Multimodal Banglish Classroom Summarizer - Complete Project Context

## Executive Summary

This is a **Master's Thesis Project (P2 Phase Complete)** that builds an end-to-end pipeline for processing Bangla/Banglish (Bengali + English code-mixed) lecture videos. The system extracts content from both audio and visual modalities, then generates comprehensive lecture notes automatically.

### Key Results (P2 Evaluation - 9 Videos)
| Metric | Value |
|--------|-------|
| **Term F1** | 73.9% |
| **Term Precision** | 83.6% |
| **Term Recall** | 66.5% |
| **Dataset** | 9 videos, ~73K characters ground truth |
| **Domains** | Python, DLD, DBMS |

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [System Architecture](#system-architecture)
3. [Core Models Used](#core-models-used)
4. [Research Contributions](#research-contributions)
5. [What Was Tried and Results](#what-was-tried-and-results)
6. [Current Pipeline State](#current-pipeline-state)
7. [Evaluation Metrics](#evaluation-metrics)
8. [Key Files and Their Purposes](#key-files-and-their-purposes)
9. [Experimental Results](#experimental-results)
10. [Known Issues and Limitations](#known-issues-and-limitations)
11. [Future Work for P3](#future-work-for-p3)

---

## Problem Statement

**Challenge**: Processing lecture videos in **Banglish** (code-mixed Bengali and English) is difficult because:
1. Speakers switch between Bengali and English mid-sentence
2. Technical terms (e.g., "Object-Oriented Programming", "Class", "Instance Variable") are spoken with Bengali grammar markers
3. Whisper (the primary ASR) often mishears technical terms or produces hallucinations
4. BanglaASR (Bengali-specific model) outputs Unicode Bengali text, which cannot be directly compared with Whisper's romanized output
5. Whiteboard content provides ground truth for technical terms but extracting it accurately requires VLM
6. **No standard Romanization** for Bengali means multiple valid spellings exist (WER is inappropriate)

**Goal**: Create a pipeline that leverages both audio (speech) and visual (whiteboard) modalities to produce accurate, structured lecture notes in a mixed Romanized/Bengali format.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        INPUT: Lecture Video (.mp4)                      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        VIDEO INGESTION (FFmpeg)                         │
│   • Extract 16kHz mono WAV audio                                        │
│   • Extract keyframes every N seconds (default: 30s)                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
┌─────────────────────────────────┐    ┌────────────────────────────────────┐
│      TRACK A: AUDIO             │    │       TRACK B: VISION              │
│                                 │    │                                    │
│  ┌───────────────────────────┐  │    │  ┌──────────────────────────────┐  │
│  │    Whisper ASR            │  │    │  │    VLM (Qwen2.5-VL-7B)       │  │
│  │  whisper-large-v3-turbo   │  │    │  │    Whiteboard OCR            │  │
│  │                           │  │    │  │                              │  │
│  │  WITH Visual Bias →→→→→→→│◄─┼────┤◄─┤    Outputs:                  │  │
│  │  (LogitsProcessor)        │  │    │  │    • Keywords                │  │
│  └───────────────────────────┘  │    │  │    • Definitions             │  │
│               +                 │    │  │    • Code snippets           │  │
│  ┌───────────────────────────┐  │    │  │    • Bounding boxes          │  │
│  │    BanglaASR              │  │    │  └──────────────────────────────┘  │
│  │  (Wav2Vec2 fine-tuned)    │  │    │               +                    │
│  │    Bengali Unicode output │  │    │  ┌──────────────────────────────┐  │
│  └───────────────────────────┘  │    │  │    YOLOv8-Pose               │  │
│               │                 │    │  │    Gaze/Pointing Detection   │  │
│               ▼                 │    │  └──────────────────────────────┘  │
│  ┌───────────────────────────┐  │    │                                    │
│  │  TRANSLITERATION FUSION   │  │    └────────────────────────────────────┘
│  │  Bengali → Romanized      │  │
│  │  Fuzzy word matching      │  │
│  │  Suffix stripping         │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
              │                                           │
              └─────────────────────┬─────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        TRACK C: EVALUATION                              │
│   • Technical Term Recall (TTR) with fuzzy matching                     │
│   • Word Error Rate (WER) using jiwer                                   │
│   • 3-way comparison: Baseline vs Global Bias vs Temporal Bias          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      TRACK D: LLM SUMMARIZATION                         │
│   • Qwen2.5-7B-Instruct (FP16 or 4-bit quantized)                       │
│   • Combines: Fused transcript + Structured VLM context                 │
│   • Outputs: Structured Markdown lecture notes                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          OUTPUT FILES                                   │
│   • final_lecture_notes.md        (LLM-generated notes)                 │
│   • transcript_whisper_baseline.txt                                     │
│   • transcript_whisper_visual_biased.txt                                │
│   • transcript_bangla.txt                                               │
│   • visual_keywords.json                                                │
│   • text_boxes.json                                                     │
│   • gaze_events.json                                                    │
│   • evaluation.json               (TTR improvement metrics)             │
│   • fusion_metrics.json           (Transliteration fusion stats)        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Models Used

| Component | Model | Size | VRAM | Purpose |
|-----------|-------|------|------|---------|
| **ASR Primary** | openai/whisper-large-v3-turbo | ~1.5B params | ~3GB | Main transcription for Banglish |
| **ASR Bengali** | bangla-speech-processing/BanglaASR | ~242M params (Whisper-small fine-tuned) | ~0.5GB | Pure Bengali speech recognition |
| **VLM** | Qwen/Qwen2.5-VL-7B-Instruct | 7B params | ~15GB | Whiteboard text extraction, keyword identification |
| **LLM** | Qwen/Qwen2.5-7B-Instruct | 7B params | ~14GB (FP16) or ~5GB (4-bit) | Multimodal fusion, lecture note generation |
| **Pose** | YOLOv8n-Pose | ~3M params | ~0.5GB | Hand/body pose for pointing detection |

**Total VRAM**: ~33GB (sequential loading) or ~24GB with model registry unloading

---

## Research Contributions

### 1. BanglaASR Benchmark Dataset ✅
**First ground-truth dataset for Banglish technical lectures**
- 9 real classroom recordings
- ~73,000 characters of manually transcribed content
- Three domains: Python (5 videos), DLD (2 videos), DBMS (2 videos)
- Topics: Variables, Input/Output, Conditionals, Loops, Data Structures, Logic Gates, SQL

### 2. Term-Based Evaluation Framework ✅
**Metrics designed for Romanized code-mixed languages**
- Term Recall, Term Precision, Term F1 with fuzzy matching
- Accommodates transliteration variance (e.g., "amra" vs "aamra")
- Excludes WER as inappropriate for Romanized Banglish

### 3. Multimodal Pipeline Architecture ✅
**Complete video-to-notes processing system**
- Whisper ASR for Banglish speech
- Qwen2.5-VL for whiteboard OCR
- Cross-modal verification
- Qwen2.5-7B for summarization

### 4. Anti-Hallucination Processing ✅
**Post-processing to remove ASR repetition loops**
- Detects repetitive patterns
- Removes excess word repetitions
- Preserves legitimate content

### 5. Visual-Biased ASR ❌ (Failed)
**Bias Whisper's logits toward whiteboard keywords**
- Causes hallucinations rather than improvements
- Self-reinforcing loops boost visual terms excessively
- **Disabled in production pipeline**

### 6. Gaze Tracking ❌ (Failed)
**Detect lecturer pointing using YOLOv8-Pose**
- 0 detections across all videos
- Lecturer doesn't point explicitly in these recordings

---

### Novelty 2: Dual-ASR Transliteration Fusion

**Files**: 
- `src/audio/dual_asr_fusion_transliterate.py`
- `src/audio/bengali_transliterate.py`

**Problem**: Whisper outputs romanized Banglish ("ami class ta likhbo"), while BanglaASR outputs Bengali Unicode ("আমি ক্লাস টা লিখবো"). Direct comparison is impossible.

**Solution**: 
1. Transliterate Bengali Unicode to Romanized script using a custom mapping
2. Compare word-by-word using fuzzy matching (Levenshtein distance)
3. Strip Bengali suffixes (e.g., "classero" → "class") for better matching
4. Merge segments: Keep Whisper for technical terms, add unique Bengali words from BanglaASR

**Key Components**:
- Bengali → Roman transliteration with 40+ consonants, vowels, conjuncts
- Levenshtein similarity calculation
- N-gram character matching for transliteration variants
- Bengali suffix stripping (ero, ro, ta, te, ke, er, o, i, e)

**Result**: Successfully extracts unique Bengali words (800-2800 per video) but average similarity is very low (0.02-0.07), indicating the fusion is not finding many overlapping segments.

---

### Novelty 3: Temporal Visual Bias (Attempted but Failed)

**File**: `src/fusion/temporal_context.py`

**Concept**: Instead of biasing ALL audio with ALL keywords, use temporal alignment. Keywords from frame at 0:30 should only bias audio segment 0:00-1:00, not the entire lecture.

**Implementation**:
- Map each frame to its timestamp
- Create sliding window (±30 seconds)
- During transcription, only inject keywords visible in the current time window

**Result**: **FAILED**. No significant improvement over global bias. The temporal alignment added complexity but did not improve TTR. This approach was abandoned.

---

### Novelty 4: Structured VLM Extraction

**File**: `src/vision/structured_extractor.py`

**Concept**: Instead of just extracting raw text, ask the VLM to categorize whiteboard content into:
- **Definitions**: "Object = instance of a class"
- **Keywords**: Technical terms
- **Code snippets**: Programming examples
- **Diagrams**: Visual explanations

**Result**: Works well for providing rich context to the LLM summarizer. Produces structured JSON that improves lecture note quality.

---

### Novelty 5: Anti-Hallucination Post-Processing

**File**: `src/audio/visual_bias_processor.py` (functions: `remove_repetitions`, `remove_phrase_repetitions`)

**Problem**: Whisper hallucinates repetitive phrases like "Student Student Student..." or "The course of the course of the course..."

**Solution**:
- Detect N-gram repetition ratio
- Remove consecutive word repetitions (max 3 allowed)
- Remove repeated phrases (2-15 words) using word-based algorithm

**Result**: Successfully reduces hallucinations without breaking legitimate content.

---

## What Was Tried and Results

### Experiments Conducted

| Experiment | Description | Outcome |
|------------|-------------|---------|
| **Visual Bias (Global)** | Bias Whisper with all VLM keywords | Mixed: +10% to -15% TTR depending on video |
| **Temporal Visual Bias** | Time-aligned keyword injection | **FAILED**: No improvement over global bias |
| **Dual-ASR V1 (Simple)** | Language detection + segment selection | **FAILED**: Everything detected as English |
| **Dual-ASR V2 (Transliteration)** | Bengali→Roman + fuzzy matching | Partial success: Extracts unique Bengali words |
| **Threshold Tuning** | Test similarity thresholds 0.01-0.2 | Optimal: 0.01 (very permissive) |
| **Fuzzy Matching** | Levenshtein + n-gram similarity | Added, minor improvement |
| **Suffix Stripping** | Remove Bengali verb suffixes | Added, minor improvement |
| **Gaze Tracking** | YOLOv8-Pose pointing detection | **0 events detected** across all videos |
| **LLM Summarization** | Qwen2.5-7B multimodal fusion | Works well, but no measurable research impact |

### Failed Approaches in Detail

1. **Temporal Visual Bias**: The hypothesis was that time-aligned keywords would reduce false positives. However, Whisper's context window is large enough that global bias works similarly. The added complexity did not justify the marginal (or negative) gains.

2. **Gaze Tracking**: YOLOv8-Pose was supposed to detect when the lecturer points at whiteboard terms. In practice, **0 pointing gestures were detected** across 5 videos. Possible reasons:
   - Lecturer doesn't point explicitly
   - Camera angle doesn't capture hand clearly
   - YOLOv8-Pose not calibrated for this use case

3. **Simple Language Detection**: Initial Dual-ASR fusion tried to detect Bengali vs English segments. Failed because Banglish is intrinsically code-mixed at the word level, not segment level.

---

## Current Pipeline State

### Working Components ✅
- Video ingestion (FFmpeg extraction)
- VLM whiteboard OCR (Qwen2.5-VL)
- Whisper transcription (baseline, without visual bias)
- BanglaASR Bengali transcription
- Bengali → Romanized transliteration
- Anti-hallucination post-processing
- LLM lecture note generation
- Term-based evaluation metrics (Recall, Precision, F1)
- Model registry (singleton pattern for VRAM management)
- Ground truth comparison and evaluation

### Partially Working ⚠️
- Transliteration fusion: Low similarity scores (0.02-0.07)
- Cross-modal verification: Works for error detection, not correction

### Not Working ❌
- Visual bias LogitsProcessor: Causes hallucinations (DISABLED)
- Gaze tracking: 0 detections across all videos
- Temporal visual bias: No improvement, abandoned

---

## Evaluation Metrics

### Primary Metrics (Term-Based)

| Metric | Definition | Average Result |
|--------|------------|----------------|
| **Term Recall** | % of ground truth terms found in transcript | 66.5% |
| **Term Precision** | % of transcript terms that are correct | 83.6% |
| **Term F1** | Harmonic mean of recall and precision | 73.9% |

### Secondary Metrics

| Metric | Definition | Average Result |
|--------|------------|----------------|
| Fuzzy Similarity | Character-level similarity | 44.8% |
| ROUGE-L | Longest common subsequence | 18.5% |
| BLEU | N-gram precision | 4.1% |
| CER | Character Error Rate | 122.6% |

### Excluded Metric
- **WER (Word Error Rate)**: Not suitable for Romanized Banglish due to transliteration variance

### P2 Evaluation Results (9 Videos)

| Video | Topic | Term Recall | Term Precision | Term F1 |
|-------|-------|-------------|----------------|---------|
| BanglaASR1 | Python Variables | 62.0% | 81.6% | 70.5% |
| BanglaASR2 | Python Input | 68.7% | 84.7% | 75.8% |
| BanglaASR3 | Conditionals | 72.6% | **88.2%** | **79.6%** |
| BanglaASR4 | Loops | 51.7% | 78.7% | 62.4% |
| BanglaASR5 | Lists/Tuples | 63.0% | 87.3% | 73.2% |
| BanglaASR6 | DLD Gates | 60.0% | 86.4% | 70.8% |
| BanglaASR7 | Universal Gates | 68.6% | 82.8% | 75.0% |
| BanglaASR8 | DBMS Intro | **76.9%** | 80.6% | 78.7% |
| BanglaASR9 | SQL SELECT | 75.4% | 82.1% | 78.6% |

---

## Key Files and Their Purposes

### Main Entry Points
| File | Purpose |
|------|---------|
| `run_thesis.py` | Master orchestrator - runs complete pipeline for one video |
| `batch_process.py` | Process multiple videos in data/raw folder |
| `thesis_demo.py` | Simplified demo script |

### Source Modules (`src/`)

| File | Purpose |
|------|---------|
| `ingest_video.py` | FFmpeg video → audio + frames extraction |
| `model_registry.py` | Singleton pattern for GPU model caching |
| `audio/transcriber.py` | Whisper-based Banglish transcription |
| `audio/transcriber_specialized.py` | BanglaASR Bengali transcription |
| `audio/visual_bias_processor.py` | LogitsProcessor for keyword biasing + anti-hallucination |
| `audio/dual_asr_fusion_transliterate.py` | Transliteration-based dual-ASR fusion |
| `audio/bengali_transliterate.py` | Bengali Unicode → Romanized mapping |
| `vision/whiteboard_ocr.py` | Qwen2.5-VL whiteboard extraction |
| `vision/structured_extractor.py` | Structured VLM output (definitions, code, keywords) |
| `research/gaze_tracker.py` | YOLOv8-Pose pointing detection |
| `fusion/temporal_context.py` | Temporal keyword alignment (abandoned) |
| `summarizer/generator.py` | LLM lecture note generation |
| `evaluation/evaluator.py` | TTR + WER metrics |
| `evaluation/quality_evaluator.py` | Lecture note quality scoring |

### Configuration
| File | Purpose |
|------|---------|
| `config/config.yaml` | Batch mode settings (FP16 models) |
| `config/live_config.yaml` | Live mode settings (4-bit LLM quantization) |

---

## Known Issues and Limitations

1. **Dataset Size**: 9 videos is sufficient for methodology validation but limited for generalization claims.

2. **Instructional Style**: All recordings feature similar whiteboard-based instruction style.

3. **Hardware Requirements**: Requires 24GB VRAM GPU; sequential model loading needed.

4. **Visual Dependency**: System benefits require whiteboard content; purely verbal lectures don't benefit.

5. **Language Scope**: Only Bengali-English code-mixing addressed; other code-mixed languages untested.

6. **Gaze Tracking Non-Functional**: 0 detections across all videos - either lecturers don't point or model needs recalibration.

---

## Future Work for P3 (Defense Phase)

### Immediate Priorities
1. **Complete Thesis Writing**: Chapters 2-8 in LaTeX format
2. **Additional Ablation Studies**: Quantify component contributions
3. **Human Evaluation**: Subjective quality ratings of transcripts

### Research Extensions
1. **Larger Dataset**: More videos, more domains, more instructors
2. **Better Cross-Modal Fusion**: LLM-based transcript merging
3. **Real-Time Processing**: Streaming lecture transcription
4. **Multi-Language Support**: Extend to Hinglish, Spanglish

### Publication Potential
- **BanglaASR Benchmark**: Valuable standalone contribution
- **Term-Based Evaluation for Code-Mixed ASR**: Methodological contribution
- **Visual Bias Analysis**: Negative result but instructive for future research

---

## Summary for LLM Context

This thesis project builds a multimodal lecture video processing system achieving **73.9% Term F1** on Banglish technical lectures.

**Key Contributions**:
1. **BanglaASR Benchmark**: 9 videos, ~73K chars ground truth (first of its kind)
2. **Term-Based Evaluation**: Metrics appropriate for Romanized code-mixed languages
3. **Multimodal Pipeline**: Whisper + Qwen2.5-VL + Qwen2.5-7B end-to-end system

**Key Findings**:
- Visual bias during ASR decoding **HURTS** performance (causes hallucinations)
- Term-based metrics better capture practical utility than WER
- 83.6% precision shows system is accurate when it detects terms
- 66.5% recall shows room for improvement in term coverage

**Current Status**: P2 Complete. Ground truth evaluation on 9 videos completed. Thesis Chapter 1 written. Ready for Chapter 2 onwards.

**Hardware**: RTX 3090 (24GB VRAM), CUDA 12.4, Windows 11

---

*Document updated: February 3, 2026*
*P2 Evaluation: 9 videos, 27 runs, ~73K characters ground truth*
