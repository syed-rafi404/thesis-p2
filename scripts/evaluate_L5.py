#!/usr/bin/env python3
"""
=============================================================================
GROUND TRUTH EVALUATION - L5: Objects and Their Memory Locations
=============================================================================
Compare baseline vs visual-biased transcripts against ground truth.
=============================================================================
"""

import re
import json
from pathlib import Path
from collections import Counter
from jiwer import wer
from thefuzz import fuzz

def load_ground_truth(path: Path) -> str:
    """Load and clean ground truth transcription"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\[\d+:\d+(?::\d+)?-\d+:\d+(?::\d+)?\]', '', content)
    return ' '.join(content.split())


def load_transcript(path: Path) -> str:
    """Load ASR transcript"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def extract_technical_terms(text: str) -> set:
    """Extract Java/programming technical terms (expanded for L5)"""
    tech_patterns = [
        # Core OOP
        r'\bclass\b', r'\bobject\b', r'\binstance\b', r'\bStudent\b',
        r'\bmemory\b', r'\blocation\b', r'\breference\b', r'\bvariable\b',
        # Java keywords
        r'\bpublic\b', r'\bprivate\b', r'\bstatic\b', r'\bvoid\b', 
        r'\bmain\b', r'\bString\b', r'\bint\b', r'\bnew\b', r'\bnull\b',
        # Methods/operations
        r'\bmethod\b', r'\bprint\b', r'\bcreate\b', r'\bupdate\b',
        r'\bstore\b', r'\bcopy\b', r'\binitialize\b', r'\bdeclare\b',
        # Concepts
        r'\bdesign\b', r'\btemplate\b', r'\bblueprint\b',
        r'\bidentical\b', r'\bunique\b', r'\bseparate\b',
        # Variables used in lecture
        r'\bs1\b', r'\bs2\b', r'\bs3\b', r'\bname\b', r'\bid\b',
        r'\bDhaka\b', r'\bctg\b', r'\bKhulna\b',
        r'\bBob\b', r'\bCarol\b', r'\bDavid\b',
        # Examples
        r'\bphone\b', r'\bmarker\b', r'\bgari\b', r'\bcar\b',
        r'\bBrac\b', r'\bUniversity\b', r'\bBadda\b',
        # General
        r'\btable\b', r'\bvalue\b', r'\bdefault\b', r'\boutput\b',
        r'\bcompile\b', r'\brun\b', r'\bcode\b', r'\bline\b'
    ]
    found = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found.update([m.lower() for m in matches])
    return found


def count_term_occurrences(text: str, terms: set) -> dict:
    """Count how many times each term appears"""
    counts = {}
    text_lower = text.lower()
    for term in terms:
        counts[term] = len(re.findall(rf'\b{re.escape(term)}\b', text_lower, re.IGNORECASE))
    return counts


def calculate_recall(gt_counts: dict, tr_counts: dict) -> float:
    """Calculate term recall"""
    total_gt = sum(gt_counts.values())
    if total_gt == 0:
        return 0
    total_found = sum(min(tr_counts.get(t, 0), gt_counts[t]) for t in gt_counts)
    return total_found / total_gt


def detect_hallucination(text: str) -> dict:
    """Detect excessive repetition (hallucination indicator)"""
    words = text.lower().split()
    word_counts = Counter(words)
    
    excessive = {w: c for w, c in word_counts.items() if c > 15}
    
    return {
        'total_words': len(words),
        'unique_words': len(word_counts),
        'repetition_ratio': 1 - (len(word_counts) / len(words)) if words else 0,
        'excessive_repeats': excessive
    }


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Paths for L5
    gt_path = base_path / "data/ground_truth/L5_ground_truth.txt"
    baseline_path = base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_baseline.txt"
    biased_path = base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_visual_biased.txt"
    
    print("=" * 80)
    print("GROUND TRUTH EVALUATION: L5 - Objects and Memory Locations")
    print("=" * 80)
    
    # Load texts
    ground_truth = load_ground_truth(gt_path)
    baseline = load_transcript(baseline_path)
    biased = load_transcript(biased_path)
    
    print(f"\n📊 Text Lengths:")
    print(f"  Ground Truth:     {len(ground_truth):>6,} chars")
    print(f"  Whisper Baseline: {len(baseline):>6,} chars")
    print(f"  Whisper Biased:   {len(biased):>6,} chars")
    
    # Extract technical terms from ground truth
    gt_terms = extract_technical_terms(ground_truth)
    print(f"\n🔧 Technical Terms Found in Ground Truth: {len(gt_terms)}")
    print(f"   Terms: {sorted(gt_terms)[:20]}...")  # Show first 20
    
    # Count occurrences
    gt_counts = count_term_occurrences(ground_truth, gt_terms)
    baseline_counts = count_term_occurrences(baseline, gt_terms)
    biased_counts = count_term_occurrences(biased, gt_terms)
    
    # Calculate term recall
    baseline_recall = calculate_recall(gt_counts, baseline_counts)
    biased_recall = calculate_recall(gt_counts, biased_counts)
    
    print(f"\n📈 Technical Term Recall (TTR):")
    print(f"  Whisper Baseline: {baseline_recall*100:.1f}%")
    print(f"  Whisper Biased:   {biased_recall*100:.1f}%")
    print(f"  Difference:       {(biased_recall - baseline_recall)*100:+.1f}%")
    
    # Fuzzy similarity
    baseline_sim = fuzz.ratio(ground_truth.lower(), baseline.lower())
    biased_sim = fuzz.ratio(ground_truth.lower(), biased.lower())
    
    print(f"\n🔤 Fuzzy Similarity to Ground Truth:")
    print(f"  Whisper Baseline: {baseline_sim}%")
    print(f"  Whisper Biased:   {biased_sim}%")
    print(f"  Difference:       {biased_sim - baseline_sim:+d}%")
    
    # Hallucination detection
    print(f"\n⚠️ Hallucination Analysis:")
    
    gt_hall = detect_hallucination(ground_truth)
    baseline_hall = detect_hallucination(baseline)
    biased_hall = detect_hallucination(biased)
    
    print(f"\n  Ground Truth:")
    print(f"    Total/Unique words: {gt_hall['total_words']}/{gt_hall['unique_words']}")
    print(f"    Repetition ratio:   {gt_hall['repetition_ratio']:.2%}")
    
    print(f"\n  Whisper Baseline:")
    print(f"    Total/Unique words: {baseline_hall['total_words']}/{baseline_hall['unique_words']}")
    print(f"    Repetition ratio:   {baseline_hall['repetition_ratio']:.2%}")
    if baseline_hall['excessive_repeats']:
        top_5 = sorted(baseline_hall['excessive_repeats'].items(), key=lambda x: -x[1])[:5]
        print(f"    Top excessive:      {dict(top_5)}")
    
    print(f"\n  Whisper Biased:")
    print(f"    Total/Unique words: {biased_hall['total_words']}/{biased_hall['unique_words']}")
    print(f"    Repetition ratio:   {biased_hall['repetition_ratio']:.2%}")
    if biased_hall['excessive_repeats']:
        top_5 = sorted(biased_hall['excessive_repeats'].items(), key=lambda x: -x[1])[:5]
        print(f"    Top excessive:      {dict(top_5)}")
    
    # Term-by-term comparison
    print(f"\n📋 Term-by-Term Comparison (GT vs Baseline vs Biased):")
    print(f"{'Term':<15} {'GT':>5} {'Base':>5} {'Bias':>5} {'B-diff':>7} {'V-diff':>7}")
    print("-" * 55)
    
    for term in sorted(gt_terms):
        gt_c = gt_counts.get(term, 0)
        base_c = baseline_counts.get(term, 0)
        bias_c = biased_counts.get(term, 0)
        if gt_c > 0:
            print(f"{term:<15} {gt_c:>5} {base_c:>5} {bias_c:>5} {base_c-gt_c:>+7} {bias_c-gt_c:>+7}")
    
    # Summary verdict
    print("\n" + "=" * 80)
    print("VERDICT:")
    if biased_recall > baseline_recall + 0.02:
        print("✅ Visual Bias HELPS (+{:.1f}% term recall)".format((biased_recall-baseline_recall)*100))
    elif biased_recall < baseline_recall - 0.02:
        print("❌ Visual Bias HURTS ({:.1f}% term recall)".format((biased_recall-baseline_recall)*100))
    else:
        print("➖ Visual Bias has NEGLIGIBLE effect ({:+.1f}% term recall)".format((biased_recall-baseline_recall)*100))
    
    if biased_hall['repetition_ratio'] > baseline_hall['repetition_ratio'] + 0.05:
        print("❌ Visual Bias increases hallucinations")
    elif biased_hall['repetition_ratio'] < baseline_hall['repetition_ratio'] - 0.05:
        print("✅ Visual Bias reduces hallucinations")
    
    print("=" * 80)
    
    # Save results
    results = {
        'lecture': 'L5 - Objects and Memory Locations',
        'ground_truth_chars': len(ground_truth),
        'baseline': {
            'chars': len(baseline),
            'term_recall': baseline_recall,
            'fuzzy_similarity': baseline_sim,
            'repetition_ratio': baseline_hall['repetition_ratio']
        },
        'biased': {
            'chars': len(biased),
            'term_recall': biased_recall,
            'fuzzy_similarity': biased_sim,
            'repetition_ratio': biased_hall['repetition_ratio']
        },
        'difference': {
            'term_recall': biased_recall - baseline_recall,
            'fuzzy_similarity': biased_sim - baseline_sim
        },
        'gt_term_counts': gt_counts,
        'baseline_term_counts': baseline_counts,
        'biased_term_counts': biased_counts
    }
    
    out_path = base_path / "output/L5_evaluation_results.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Results saved to: {out_path}")


if __name__ == "__main__":
    main()
