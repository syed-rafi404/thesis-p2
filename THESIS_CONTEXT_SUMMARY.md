# Multimodal Banglish Classroom Summarizer - Complete Project Context

## Executive Summary

This is a **Master's Thesis Project (P2 Phase)** that builds an end-to-end pipeline for processing Bangla/Banglish (Bengali + English code-mixed) lecture videos. The system extracts content from both audio and visual modalities, then generates comprehensive lecture notes automatically. The primary research goal is to improve speech recognition quality for technical lectures by leveraging visual context from whiteboards.

---

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [System Architecture](#system-architecture)
3. [Core Models Used](#core-models-used)
4. [Research Novelties](#research-novelties)
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

## Research Novelties

### Novelty 1: Visual-Biased ASR (LogitsProcessor)

**File**: `src/audio/visual_bias_processor.py`

**Concept**: Whisper often mishears technical terms in Banglish lectures. For example, "A* algorithm" might be transcribed as "A-store algorithm". The VLM extracts clean text from the whiteboard (e.g., "A*", "Heuristic", "Object-Oriented"). We inject these keywords into Whisper's decoding process by adding a bias to logits for tokens that match extracted keywords.

**Implementation**:
```python
class VisualBiasLogitsProcessor(LogitsProcessor):
    def __call__(self, input_ids, scores):
        # Boost probability of visual keyword tokens
        for term, boost_value in self.term_boosts.items():
            if term in self.vocabulary:
                token_id = self.vocabulary[term]
                scores[:, token_id] += boost_value
        return scores
```

**Result**: Mixed results. Some videos showed +10% TTR improvement, others showed -15% degradation. The visual bias sometimes causes Whisper to over-insert keywords in wrong contexts.

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
- Whisper transcription (with and without bias)
- BanglaASR Bengali transcription
- Bengali → Romanized transliteration
- Anti-hallucination post-processing
- LLM lecture note generation
- TTR/WER evaluation metrics
- Model registry (singleton pattern for VRAM management)

### Partially Working ⚠️
- Visual bias: Inconsistent improvement (+10% to -15%)
- Transliteration fusion: Low similarity scores (0.02-0.07)
- Gaze tracking: 0 detections (needs different videos or calibration)

### Not Working ❌
- Temporal visual bias: No improvement, abandoned
- WER comparison: Requires ground truth transcripts (not available)

---

## Evaluation Metrics

### Technical Term Recall (TTR)
- **Definition**: Percentage of whiteboard terms found in transcript
- **Method**: Fuzzy matching (thefuzz library) with threshold > 85
- **Formula**: `TTR = found_terms / total_ground_truth_terms`

### TTR Improvement
- **Definition**: Relative improvement of visual-biased over baseline
- **Formula**: `improvement = (biased_TTR - baseline_TTR) * 100`

### Results Across 5 Videos (Batch Run Jan 25, 2026)

| Video | Baseline TTR | Biased TTR | Improvement | Visual Keywords |
|-------|--------------|------------|-------------|-----------------|
| L1 | 75% | 60% | **-15%** ❌ | 72 |
| L2 | 40%? | 35%? | **-5%** ❌ | 21 |
| L3 | 40% | 50% | **+10%** ✅ | 66 |
| L4 | 30% | 35% | **+5%** ✅ | 84 |
| L5 | 35%? | 30%? | **-5%** ❌ | 106 |

**Conclusion**: 2/5 videos improved, 3/5 degraded. The visual bias is not consistently beneficial.

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

1. **Inconsistent Visual Bias**: The bias helps some videos but hurts others. Needs more investigation into when/why it fails.

2. **Low Fusion Similarity**: Average similarity of 0.02-0.07 means very few Bengali segments are being matched. Either the transliteration quality is poor, or the content overlap is genuinely low.

3. **No Ground Truth**: Cannot calculate true WER without human-annotated transcripts. TTR uses VLM-extracted keywords as proxy ground truth.

4. **Gaze Tracking Non-Functional**: 0 detections across all videos. Either the lecturer doesn't point, or the model needs recalibration.

5. **VRAM Management**: Sequential loading required. Cannot have VLM + Whisper + LLM loaded simultaneously on 24GB GPU.

6. **Hallucination Residue**: Anti-hallucination catches most repetitions but some still slip through.

7. **Dataset Limitations**: Currently using 7 Java OOP lecture videos from one instructor. Not representative of diverse Banglish content.

---

## Future Work for P3 (Defense Phase)

### Immediate Priorities
1. **Create Custom Dataset**: Manually transcribe portions of videos for true WER evaluation
2. **Ablation Studies**: Quantify contribution of each component (suffix stripping, fuzzy matching, etc.)
3. **Human Evaluation**: Rate transcript quality subjectively

### Research Directions
1. **Fix Visual Bias Inconsistency**: Investigate why some videos degrade. Possibly limit bias to high-confidence VLM extractions only.
2. **Better Fusion Algorithm**: Current transliteration fusion has low similarity. Try:
   - Sentence-level alignment instead of word-level
   - Use an LLM to merge transcripts intelligently
3. **Cross-Modal Verification**: Use VLM to verify/correct ASR output post-hoc
4. **Gaze Tracking Alternative**: Use attention heatmaps or video object tracking instead of pose estimation

### Publication Potential
- **Transliteration Fusion**: Novel approach for comparing Bengali/English ASR outputs. Needs better results to be publishable.
- **Visual-Biased ASR**: Good concept but needs consistent improvement to be a strong contribution.
- **Banglish Lecture Dataset**: Creating a benchmark dataset would be a valuable contribution on its own.

---

## Summary for LLM Context

This thesis project builds a multimodal lecture video processing system. The core innovation attempts are:

1. **Visual Bias for ASR** (Novelty 1): Inject whiteboard keywords into Whisper's decoding. Result: Inconsistent, sometimes helps, sometimes hurts.

2. **Transliteration Fusion** (Novelty 2): Convert Bengali to Roman script to compare Whisper and BanglaASR outputs. Result: Works mechanically but low similarity scores.

3. **Temporal Bias** (Failed): Time-align keywords to audio segments. Result: No improvement, abandoned.

4. **Gaze Tracking** (Novelty 3, Non-functional): Detect lecturer pointing at terms. Result: 0 detections.

5. **LLM Summarization** (Works): Generate lecture notes from fused transcript + VLM context. Result: Good quality notes but no measurable research contribution.

**Current Status**: Pipeline works end-to-end but lacks a consistent, quantifiable improvement that can be defended as a research contribution. The student is at P2 phase and needs to demonstrate novelty before P3 defense.

**Key Metrics from Latest Run**:
- 5 videos processed
- 2/5 showed TTR improvement (+5% to +10%)
- 3/5 showed TTR degradation (-5% to -15%)
- 829-2859 unique Bengali words extracted per video
- 0 gaze events detected

**Hardware**: RTX 3090 (24GB VRAM), CUDA 12.4, Windows 11

---

*Document generated: January 27, 2026*
*Total codebase: ~15,000 lines of Python across 25+ modules*
