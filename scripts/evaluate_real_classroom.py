"""
Evaluate Real Classroom Video (BanglishTechnical1)
==================================================

This script runs ALL evaluations we've done on L1-L7 on the new real classroom video.
This is to compare performance on screen-recorded slides vs actual classroom environment.

Tests included:
1. Ground truth comparison (term recall, precision, F1)
2. CMV-F (Frequency-Aware Cross-Modal Verification)
3. Self-Correcting Pipeline
4. Hallucination analysis
5. Visual bias impact

Run: python scripts/evaluate_real_classroom.py
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import Counter

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from thefuzz import fuzz

# Paths
OUTPUT_DIR = Path("output/BanglishTechnical1_RealClass")
GT_PATH = Path("data/ground_truth/BanglishTechnical1_ground_truth.txt")


def load_transcript(name: str) -> str:
    """Load a transcript file."""
    path = OUTPUT_DIR / name
    if path.exists():
        return path.read_text(encoding='utf-8')
    return None


def load_ground_truth() -> str:
    """Load ground truth if available."""
    if GT_PATH.exists():
        return GT_PATH.read_text(encoding='utf-8')
    return None


def extract_words(text: str) -> list:
    """Extract words from text."""
    if not text:
        return []
    # Remove timestamps like [0:00-0:30]
    text = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', text)
    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return words


def calculate_excess_repetitions(transcript_words: list, gt_words: list) -> int:
    """Calculate excess word repetitions compared to ground truth."""
    transcript_counts = Counter(transcript_words)
    gt_counts = Counter(gt_words)
    
    excess = 0
    for word, count in transcript_counts.items():
        gt_count = gt_counts.get(word, 1)  # Assume 1 if not in GT
        if count > gt_count:
            excess += count - gt_count
    return excess


def evaluate_term_recall(transcript_words: list, gt_words: list) -> dict:
    """Calculate term recall, precision, F1."""
    transcript_set = set(transcript_words)
    gt_set = set(gt_words)
    
    found = transcript_set.intersection(gt_set)
    
    recall = len(found) / len(gt_set) if gt_set else 0
    precision = len(found) / len(transcript_set) if transcript_set else 0
    f1 = 2 * recall * precision / (recall + precision) if (recall + precision) > 0 else 0
    
    return {
        'recall': recall * 100,
        'precision': precision * 100,
        'f1': f1 * 100,
        'found_terms': len(found),
        'gt_terms': len(gt_set),
        'transcript_terms': len(transcript_set)
    }


def detect_hallucinations(transcript: str) -> dict:
    """Detect repetition patterns in transcript."""
    words = extract_words(transcript)
    word_counts = Counter(words)
    
    # Find suspiciously repeated words (>20 times)
    suspicious = {word: count for word, count in word_counts.most_common(20) 
                  if count > 20 and len(word) > 3}
    
    total_words = len(words)
    excess_words = sum(max(0, count - 10) for count in word_counts.values())
    
    return {
        'total_words': total_words,
        'unique_words': len(word_counts),
        'suspicious_repetitions': suspicious,
        'repetition_rate': excess_words / total_words if total_words > 0 else 0
    }


def run_cmv_f_analysis(transcript: str, visual_keywords: list) -> dict:
    """Run CMV-F (Frequency-Aware Cross-Modal Verification)."""
    words = extract_words(transcript)
    word_counts = Counter(words)
    
    # Check each visual keyword
    results = {}
    for keyword in visual_keywords:
        kw_lower = keyword.lower()
        count = word_counts.get(kw_lower, 0)
        
        # Expected baseline (assume 1-3 mentions per keyword)
        expected = 3
        tfd = count / expected if expected > 0 else 0
        
        if tfd > 3.0:  # Hallucination threshold
            results[keyword] = {
                'count': count,
                'expected': expected,
                'tfd': tfd,
                'is_hallucination': True
            }
    
    # Calculate RHR
    total_excess = sum(r['count'] - r['expected'] for r in results.values() if r['is_hallucination'])
    rhr = total_excess / len(words) if words else 0
    
    return {
        'flagged_terms': results,
        'rhr': rhr * 100,
        'total_flagged': len(results)
    }


def main():
    print("=" * 70)
    print("REAL CLASSROOM VIDEO EVALUATION")
    print("BanglishTechnical1.MOV - Actual classroom environment")
    print("=" * 70)
    
    # Check if output exists
    if not OUTPUT_DIR.exists():
        print(f"\n❌ Output directory not found: {OUTPUT_DIR}")
        print("   Please run the pipeline first:")
        print('   python run_thesis.py "data/raw/BanglishTechnical1.MOV" -o "output/BanglishTechnical1_RealClass" --interval 5')
        return
    
    # List available files
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    files = list(OUTPUT_DIR.glob("*"))
    print(f"   Found {len(files)} files:")
    for f in files[:10]:
        print(f"   - {f.name}")
    if len(files) > 10:
        print(f"   ... and {len(files) - 10} more")
    
    # Load transcripts
    print("\n" + "=" * 70)
    print("LOADING TRANSCRIPTS")
    print("=" * 70)
    
    baseline = load_transcript("transcript_whisper_baseline.txt")
    biased = load_transcript("transcript_whisper_visual_biased.txt")
    gt = load_ground_truth()
    
    print(f"\n📄 Baseline transcript: {'✅ Found' if baseline else '❌ Not found'}")
    print(f"📄 Visual-biased transcript: {'✅ Found' if biased else '❌ Not found'}")
    print(f"📄 Ground truth: {'✅ Found' if gt else '⏳ Waiting for user to provide'}")
    
    if baseline:
        print(f"   Baseline length: {len(baseline)} chars")
    if biased:
        print(f"   Biased length: {len(biased)} chars")
    
    # Hallucination analysis (doesn't need GT)
    print("\n" + "=" * 70)
    print("HALLUCINATION ANALYSIS (No Ground Truth Needed)")
    print("=" * 70)
    
    if baseline:
        print("\n📊 BASELINE TRANSCRIPT:")
        baseline_hall = detect_hallucinations(baseline)
        print(f"   Total words: {baseline_hall['total_words']}")
        print(f"   Unique words: {baseline_hall['unique_words']}")
        print(f"   Repetition rate: {baseline_hall['repetition_rate']*100:.1f}%")
        if baseline_hall['suspicious_repetitions']:
            print("   Suspicious repetitions:")
            for word, count in list(baseline_hall['suspicious_repetitions'].items())[:5]:
                print(f"      '{word}': {count}x")
    
    if biased:
        print("\n📊 VISUAL-BIASED TRANSCRIPT:")
        biased_hall = detect_hallucinations(biased)
        print(f"   Total words: {biased_hall['total_words']}")
        print(f"   Unique words: {biased_hall['unique_words']}")
        print(f"   Repetition rate: {biased_hall['repetition_rate']*100:.1f}%")
        if biased_hall['suspicious_repetitions']:
            print("   Suspicious repetitions:")
            for word, count in list(biased_hall['suspicious_repetitions'].items())[:5]:
                print(f"      '{word}': {count}x")
    
    # Load visual keywords for CMV-F
    visual_keywords_path = OUTPUT_DIR / "visual_keywords.json"
    visual_keywords = []
    if visual_keywords_path.exists():
        with open(visual_keywords_path, 'r', encoding='utf-8') as f:
            vk_data = json.load(f)
            for frame in vk_data.get('frames', []):
                visual_keywords.extend(frame.get('keywords', []))
            visual_keywords = list(set(visual_keywords))
        print(f"\n📷 Visual keywords extracted: {len(visual_keywords)}")
        print(f"   Sample: {', '.join(visual_keywords[:10])}")
    
    # CMV-F Analysis
    if visual_keywords and biased:
        print("\n" + "=" * 70)
        print("CMV-F ANALYSIS (Frequency-Aware Cross-Modal Verification)")
        print("=" * 70)
        
        cmvf_result = run_cmv_f_analysis(biased, visual_keywords)
        print(f"\n📊 Flagged as hallucination: {cmvf_result['total_flagged']} terms")
        print(f"   RHR (Repetition Hallucination Rate): {cmvf_result['rhr']:.1f}%")
        
        if cmvf_result['flagged_terms']:
            print("\n   Flagged terms (TFD > 3.0):")
            for term, data in list(cmvf_result['flagged_terms'].items())[:5]:
                print(f"      '{term}': {data['count']}x (TFD={data['tfd']:.1f})")
    
    # Ground truth evaluation (if available)
    if gt:
        print("\n" + "=" * 70)
        print("GROUND TRUTH EVALUATION")
        print("=" * 70)
        
        gt_words = extract_words(gt)
        print(f"\n📄 Ground truth: {len(gt_words)} words")
        
        if baseline:
            baseline_words = extract_words(baseline)
            baseline_eval = evaluate_term_recall(baseline_words, gt_words)
            baseline_excess = calculate_excess_repetitions(baseline_words, gt_words)
            
            print("\n📊 BASELINE:")
            print(f"   Term Recall: {baseline_eval['recall']:.1f}%")
            print(f"   Precision: {baseline_eval['precision']:.1f}%")
            print(f"   F1 Score: {baseline_eval['f1']:.1f}%")
            print(f"   Excess Repetitions: {baseline_excess}")
        
        if biased:
            biased_words = extract_words(biased)
            biased_eval = evaluate_term_recall(biased_words, gt_words)
            biased_excess = calculate_excess_repetitions(biased_words, gt_words)
            
            print("\n📊 VISUAL-BIASED:")
            print(f"   Term Recall: {biased_eval['recall']:.1f}%")
            print(f"   Precision: {biased_eval['precision']:.1f}%")
            print(f"   F1 Score: {biased_eval['f1']:.1f}%")
            print(f"   Excess Repetitions: {biased_excess}")
        
        if baseline and biased:
            print("\n📊 COMPARISON:")
            recall_diff = biased_eval['recall'] - baseline_eval['recall']
            excess_diff = biased_excess - baseline_excess
            
            print(f"   Recall change: {recall_diff:+.1f}%")
            print(f"   Excess reps change: {excess_diff:+d}")
            
            if recall_diff < 0:
                print("   ⚠️ Visual bias HURTS recall (consistent with L1-L7)")
            else:
                print("   ✅ Visual bias HELPS recall (different from L1-L7!)")
    else:
        print("\n" + "=" * 70)
        print("WAITING FOR GROUND TRUTH")
        print("=" * 70)
        print(f"\nPlease provide ground truth at:")
        print(f"   {GT_PATH}")
        print("\nFormat: Romanized Banglish transcription with timestamps")
        print("Example: [0:00-0:30] Assalamualaikum, aj amra class e...")
    
    # Save results
    results = {
        'video': 'BanglishTechnical1.MOV',
        'type': 'real_classroom',
        'baseline_available': baseline is not None,
        'biased_available': biased is not None,
        'gt_available': gt is not None,
        'visual_keywords_count': len(visual_keywords),
    }
    
    if baseline:
        results['baseline_hallucination'] = detect_hallucinations(baseline)
    if biased:
        results['biased_hallucination'] = detect_hallucinations(biased)
        if visual_keywords:
            results['cmvf'] = run_cmv_f_analysis(biased, visual_keywords)
    
    output_path = OUTPUT_DIR / "real_classroom_evaluation.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Results saved to: {output_path}")
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("""
1. Provide ground truth transcription at:
   data/ground_truth/BanglishTechnical1_ground_truth.txt

2. Re-run this script to get full evaluation:
   python scripts/evaluate_real_classroom.py

3. Compare with L1-L7 results to see if real classroom
   behaves differently from screen-recorded slides.
""")


if __name__ == "__main__":
    main()
