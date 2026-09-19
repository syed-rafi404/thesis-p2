# Conversation Summary - February 1-2, 2026
## P2 Thesis Batch Processing Session

---

## 1. Initial Goal
- **Objective**: Run comprehensive batch processing for P2 thesis submission (deadline: 2 days)
- **Original Plan**: 16 videos × 6 intervals × gaze variants = 150 runs

---

## 2. Environment Setup
- **Conda Environment**: `thesis_v2`
- **GPU**: NVIDIA RTX 3090 (24GB VRAM)
- **VLM**: Qwen2.5-VL-7B-Instruct (15.45 GB VRAM in FP16)
- **Whisper**: openai/whisper-large-v3-turbo
- **BanglaASR**: bangla-speech-processing/BanglaASR

---

## 3. Timeline of Events

### Day 1 (Feb 1)
| Time | Event |
|------|-------|
| Start | Created `batch_comprehensive.py` for 150 runs |
| +1h | Realized 150 runs would take 6+ days (too long!) |
| +2h | Pivoted to focused approach: 9 live videos only |
| +3h | Created `batch_live_only.py` - 54 runs (~22-28 hours) |
| +8h | First 8 runs completed |

### Day 2 (Feb 2)
| Time | Event |
|------|-------|
| Morning | 16 runs completed before accidental interruption |
| Resumed | `--resume` flag saved progress, continued from run 17 |
| Current | Processing continues (38 runs remaining) |

---

## 4. Final Configuration

### `batch_live_only.py`
```
Videos: 9 (BanglaASR1-9)
Intervals: 10s, 20s, 30s
Gaze Variants: With & Without
Total Runs: 54
Output: output/live_focused/
```

### Run Order:
1. **Runs 1-27**: No gaze (baseline)
   - BanglaASR1-9 × 3 intervals each
2. **Runs 28-54**: With gaze (novelty demonstration)
   - BanglaASR1-9 × 3 intervals each

---

## 5. Completed Results (16 runs)

| Video | Intervals Done | Keywords | Notes Generated |
|-------|----------------|----------|-----------------|
| BanglaASR1 | 10s, 20s, 30s ✅ | 28-32 | ✅ |
| BanglaASR2 | 10s, 20s, 30s ✅ | 24-31 | ✅ |
| BanglaASR3 | 10s, 20s, 30s ✅ | 28-37 | ✅ |
| BanglaASR4 | 10s, 20s, 30s ✅ | 11-14 | ✅ |
| BanglaASR5 | 10s, 20s, 30s ✅ | **0** ⚠️ | ✅ (audio only) |
| BanglaASR6 | 10s ✅ | 25 | ✅ |

### BanglaASR5 Issue:
- **0 visual keywords** extracted across all intervals
- Likely no visible whiteboard/screen in video
- **System still worked** - generated 3,136+ char notes from audio alone
- Shows **graceful degradation** (a positive finding!)

---

## 6. Key Metrics Explained

### Quality Score (NOVELTY 3) - Custom Formula:
| Component | Weight | How Measured |
|-----------|--------|--------------|
| Keyword Coverage | 40% | VLM keywords found in final notes |
| Structure | 30% | Headings, lists, code blocks |
| Information Density | 30% | Lexical diversity, word count |

### Example Scores:
- BanglaASR1 @ 30s: **90.7/100** (89% keyword coverage)
- BanglaASR5 @ 30s: **55.0/100** (0% coverage - no visual keywords)

### Industry Standard Metrics (to add later):
- **ROUGE** - N-gram overlap (can compute post-hoc)
- **BLEU** - Translation quality (can compute post-hoc)
- Both can be calculated WITHOUT re-running videos!

---

## 7. Gaze Detection Explained

### What It Does:
- Detects instructor **pointing gestures** using YOLOv8-Pose
- Maps gestures to **screen regions**
- Records **timestamps** of attention events

### How It Helps:
- Identifies **emphasized content**
- Provides **priority weighting** for summary
- Adds **temporal context** ("instructor pointed at X at time T")

### Current Comparison:
- Runs 1-27: Gaze OFF (baseline)
- Runs 28-54: Gaze ON (to show benefit)

---

## 8. Output Structure

```
output/live_focused/
├── live_batch_log.json          # Progress tracking
├── no_gaze/
│   ├── interval_10s/
│   │   ├── BanglaASR1/
│   │   │   ├── final_lecture_notes.md
│   │   │   ├── visual_keywords.json
│   │   │   ├── transcript_whisper_baseline.txt
│   │   │   ├── transcript_bangla.txt
│   │   │   ├── transcript_fused.txt
│   │   │   ├── quality_metrics.json
│   │   │   ├── evaluation.json
│   │   │   └── ingested/frames/
│   │   ├── BanglaASR2/
│   │   └── ...
│   ├── interval_20s/
│   └── interval_30s/
└── with_gaze/
    ├── interval_10s/
    ├── interval_20s/
    └── interval_30s/
```

---

## 9. Lessons Learned

### What Went Well:
- ✅ Resume functionality saved 16 runs after interruption
- ✅ GPU memory management (VLM unloading for Whisper)
- ✅ System handles 0-keyword videos gracefully
- ✅ Dual-ASR fusion produces good transcripts

### Issues Encountered:
- ⚠️ Initial 150-run plan was too ambitious for deadline
- ⚠️ Terminal commands in same window can interrupt batch
- ⚠️ Some videos (BanglaASR5) have no visible whiteboard content
- ⚠️ BanglaASR2 took 83 minutes (outlier)

### Process Times Observed:
| Interval | Typical Time |
|----------|--------------|
| 10s | 30-80 min (most frames) |
| 20s | 20-45 min |
| 30s | 15-25 min (fastest) |

---

## 10. Current Status

| Item | Value |
|------|-------|
| Completed | 16/54 runs |
| Remaining | 38 runs |
| Current Run | BanglaASR6 @ 20s |
| ETA | ~20-25 hours |
| Expected Completion | Feb 3, 2026 evening |

---

## 11. Post-Processing Tasks (After Batch Completes)

### Can Be Done Without Re-Running:
1. **ROUGE/BLEU Scoring** - Compare notes vs. transcript
2. **Aggregate Statistics** - Mean/std quality scores
3. **Gaze Impact Analysis** - With vs. without comparison
4. **Visualization Generation** - Charts for thesis
5. **Interval Optimization** - Which interval is best?

### Script Needed:
- Post-processing script to compute ROUGE/BLEU on all 54 outputs
- ~5 minutes to run (text comparison only, no GPU needed)

---

## 12. Thesis Implications

### Include ALL Videos:
- Including BanglaASR5 (0 keywords) shows research rigor
- Demonstrates system robustness
- Provides interesting edge case discussion

### Comparison Points:
1. **Interval Comparison**: 10s vs 20s vs 30s quality trade-offs
2. **Gaze Impact**: With vs without gaze detection
3. **Visual Content Availability**: Rich (ASR1-3) vs Poor (ASR5)
4. **Dual-ASR Benefit**: Whisper vs BanglaASR vs Fusion

### Three Novelties:
1. **NOVELTY 1**: Structured VLM extraction (definitions, code, keywords)
2. **NOVELTY 2**: Transliteration-based dual-ASR fusion
3. **NOVELTY 3**: Quality-evaluated multimodal summarization

---

## 13. Terminal Reference

**Batch process running in terminal ID**: `ecfadcee-be39-4710-877a-b443e2ff9e93`

**To check progress (safe commands):**
```powershell
# Check if process is running
Get-Process python -ErrorAction SilentlyContinue

# Check GPU usage
nvidia-smi --query-gpu=memory.used --format=csv,noheader
```

**DO NOT run commands in the batch terminal!**

---

## 14. Files Created This Session

| File | Purpose |
|------|---------|
| `batch_comprehensive.py` | Original 150-run script (abandoned) |
| `batch_live_only.py` | Focused 54-run script (in use) |
| `output/live_focused/` | All batch outputs |
| `live_batch_log.json` | Progress tracking |
| `CONVERSATION_SUMMARY_FEB2.md` | This file |

---

*Last updated: February 2, 2026*
*Batch processing in progress: 38 runs remaining*
