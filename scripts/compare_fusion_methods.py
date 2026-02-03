"""
Dual-ASR Fusion Comparison Script

Tests 3 different fusion approaches:
1. V2 Simple (Whisper as base)
2. Transliteration (Bengali → Romanized)
3. LLM-Based (Intelligent merging)

Run on 3 videos and compare results.
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Get test transcripts
def get_test_transcripts(output_folder: Path) -> tuple:
    """Load Whisper and BanglaASR transcripts from output folder."""
    
    whisper_file = output_folder / "transcript_whisper_baseline.txt"
    bangla_file = output_folder / "transcript_bangla.txt"
    
    whisper_text = ""
    bangla_text = ""
    
    if whisper_file.exists():
        whisper_text = whisper_file.read_text(encoding='utf-8')
        print(f"  Whisper: {len(whisper_text)} chars")
    else:
        print(f"  Whisper: NOT FOUND")
    
    if bangla_file.exists():
        bangla_text = bangla_file.read_text(encoding='utf-8')
        print(f"  BanglaASR: {len(bangla_text)} chars")
    else:
        print(f"  BanglaASR: NOT FOUND")
    
    return whisper_text, bangla_text


def test_v2_simple(whisper: str, bangla: str) -> Dict[str, Any]:
    """Test V2 Simple fusion."""
    from src.audio.dual_asr_fusion_v2 import DualASRFusionV2
    import re
    
    start = time.time()
    fusion = DualASRFusionV2()
    
    # V2 expects strings directly
    result = fusion.fuse(whisper, bangla)
    elapsed = time.time() - start
    
    return {
        "method": "V2 Simple",
        "output_length": len(result.fused_transcript),
        "processing_time": elapsed,
        "bengali_char_ratio": result.bengali_char_ratio,
        "english_word_ratio": result.english_word_ratio,
        "banglish_detected": result.banglish_detected,
        "fusion_benefit": result.fusion_benefit,
        "transcript_preview": result.fused_transcript[:300],
    }


def test_transliteration(whisper: str, bangla: str) -> Dict[str, Any]:
    """Test Transliteration-based fusion."""
    from src.audio.dual_asr_fusion_transliterate import DualASRFusionTransliterate
    
    start = time.time()
    fusion = DualASRFusionTransliterate()
    
    # Transliteration fuse() expects strings directly
    result = fusion.fuse(whisper, bangla)
    elapsed = time.time() - start
    
    return {
        "method": "Transliteration",
        "output_length": len(result.fused_transcript),
        "processing_time": elapsed,
        "unique_bangla_words": result.unique_words_from_bangla,  # Already an int
        "avg_similarity": result.average_similarity,
        "transcript_preview": result.fused_transcript[:300],
    }


def test_llm_lite(whisper: str, bangla: str) -> Dict[str, Any]:
    """Test LLM Lite fusion (no model loading)."""
    from src.audio.dual_asr_fusion_llm import DualASRFusionLLMLite
    
    start = time.time()
    fusion = DualASRFusionLLMLite()
    result = fusion.fuse(whisper, bangla)
    elapsed = time.time() - start
    
    return {
        "method": "LLM Lite",
        "output_length": result.fused_char_count,
        "processing_time": elapsed,
        "description": result.fusion_description,
        "transcript_preview": result.fused_transcript[:300],
    }


def test_llm_full(whisper: str, bangla: str) -> Dict[str, Any]:
    """Test Full LLM fusion (loads model)."""
    from src.audio.dual_asr_fusion_llm import DualASRFusionLLM
    
    print("  Loading LLM (this may take a minute)...")
    start = time.time()
    fusion = DualASRFusionLLM(use_4bit=True)  # Use 4-bit to save VRAM
    result = fusion.fuse(whisper, bangla)
    elapsed = time.time() - start
    
    return {
        "method": "LLM Full",
        "output_length": result.fused_char_count,
        "processing_time": elapsed,
        "terms_preserved": len(result.technical_terms_preserved),
        "transcript_preview": result.fused_transcript[:300],
    }


def compare_fusion_methods(output_folder: Path, use_full_llm: bool = False) -> Dict[str, Any]:
    """Compare all fusion methods on one video's transcripts."""
    
    print(f"\n{'='*70}")
    print(f"Testing: {output_folder.name}")
    print(f"{'='*70}")
    
    whisper, bangla = get_test_transcripts(output_folder)
    
    if not whisper:
        print("  SKIPPED - No Whisper transcript")
        return None
    
    results = {}
    
    # Test 1: V2 Simple
    print("\n[1/4] Testing V2 Simple...")
    try:
        results["v2_simple"] = test_v2_simple(whisper, bangla)
        print(f"     Output: {results['v2_simple']['output_length']} chars")
    except Exception as e:
        results["v2_simple"] = {"error": str(e)}
        print(f"     ERROR: {e}")
    
    # Test 2: Transliteration
    print("\n[2/4] Testing Transliteration...")
    try:
        results["transliteration"] = test_transliteration(whisper, bangla)
        print(f"     Output: {results['transliteration']['output_length']} chars")
        print(f"     Unique Bengali words: {results['transliteration']['unique_bangla_words']}")
    except Exception as e:
        results["transliteration"] = {"error": str(e)}
        print(f"     ERROR: {e}")
    
    # Test 3: LLM Lite
    print("\n[3/4] Testing LLM Lite...")
    try:
        results["llm_lite"] = test_llm_lite(whisper, bangla)
        print(f"     Output: {results['llm_lite']['output_length']} chars")
    except Exception as e:
        results["llm_lite"] = {"error": str(e)}
        print(f"     ERROR: {e}")
    
    # Test 4: LLM Full (optional, slower)
    if use_full_llm:
        print("\n[4/4] Testing LLM Full...")
        try:
            results["llm_full"] = test_llm_full(whisper, bangla)
            print(f"     Output: {results['llm_full']['output_length']} chars")
            print(f"     Time: {results['llm_full']['processing_time']:.1f}s")
        except Exception as e:
            results["llm_full"] = {"error": str(e)}
            print(f"     ERROR: {e}")
    else:
        results["llm_full"] = {"skipped": True}
    
    return results


def print_comparison(all_results: Dict[str, Dict]) -> None:
    """Print comparison table."""
    
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    
    print(f"\n{'Video':<40} {'V2':>10} {'Translit':>10} {'LLM Lite':>10}")
    print("-" * 80)
    
    for video, results in all_results.items():
        if results is None:
            continue
        
        v2_len = results.get("v2_simple", {}).get("output_length", "N/A")
        tr_len = results.get("transliteration", {}).get("output_length", "N/A")
        ll_len = results.get("llm_lite", {}).get("output_length", "N/A")
        
        print(f"{video[:38]:<40} {v2_len:>10} {tr_len:>10} {ll_len:>10}")
    
    print()


def main():
    """Run comparison on 3 videos."""
    
    output_base = Path("output")
    
    # Find processed videos
    video_folders = [
        d for d in output_base.iterdir() 
        if d.is_dir() and (d / "transcript_whisper_baseline.txt").exists()
    ]
    
    print(f"Found {len(video_folders)} videos with transcripts")
    
    # Select 3 for testing
    test_videos = video_folders[:3]
    
    print(f"\nWill test on:")
    for v in test_videos:
        print(f"  - {v.name}")
    
    # Run comparisons
    all_results = {}
    for folder in test_videos:
        results = compare_fusion_methods(folder, use_full_llm=False)
        all_results[folder.name] = results
    
    # Print summary
    print_comparison(all_results)
    
    # Save results
    output_file = output_base / "fusion_comparison.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
