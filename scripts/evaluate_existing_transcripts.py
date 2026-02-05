#!/usr/bin/env python3
"""
=============================================================================
GROUND TRUTH EVALUATION - Compare existing transcripts against ground truth
=============================================================================
This script compares the ALREADY GENERATED transcripts (baseline vs visual-biased)
against the manual ground truth to measure the real impact of visual bias.

Usage:
    python scripts/evaluate_existing_transcripts.py

Output:
    - Console report with comparison
    - JSON file: output/L2_evaluation_results.json
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
    content = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', content)
    return ' '.join(content.split())


def load_transcript(path: Path) -> str:
    """Load ASR transcript"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def extract_technical_terms(text: str) -> set:
    """Extract Java/programming technical terms"""
    tech_patterns = [
        r'\bclass\b', r'\bobject\b', r'\bpublic\b', r'\bprivate\b',
        r'\bstatic\b', r'\bvoid\b', r'\bmain\b', r'\bString\b',
        r'\bint\b', r'\bnew\b', r'\bmethod\b', r'\bdesign\b',
        r'\btemplate\b', r'\bblueprint\b', r'\bdriver\b', r'\btester\b',
        r'\bcompile\b', r'\bexecute\b', r'\brun\b', r'\bfile\b',
        r'\bpackage\b', r'\bfolder\b', r'\bJava\b', r'\bIDE\b',
        r'\bOOP\b', r'\bsystem\b', r'\bout\b', r'\bprintln\b',
        r'\baccess\b', r'\bmodifier\b', r'\bcode\b', r'\bcurly\b',
        r'\bbraces\b', r'\bvariable\b', r'\bloop\b', r'\bsave\b',
        r'\bmanipulate\b', r'\bpanel\b', r'\bview\b', r'\btutorial\b',
        r'\bseparate\b', r'\bexample\b'
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
    
    # Find words repeated excessively (more than 10 times)
    excessive = {w: c for w, c in word_counts.items() if c > 10}
    
    return {
        'total_words': len(words),
        'unique_words': len(word_counts),
        'repetition_ratio': 1 - (len(word_counts) / len(words)) if words else 0,
        'excessive_repeats': excessive
    }


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Paths
    gt_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    baseline_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt"
    biased_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt"
    
    print("=" * 80)
    print("GROUND TRUTH EVALUATION: L2 - Creating a Design Class")
    print("=" * 80)
    
    # Load texts
    ground_truth = load_ground_truth(gt_path)
    baseline = load_transcript(baseline_path)
    biased = load_transcript(biased_path)
    
    print(f"\n📊 Text Lengths:")
    print(f"  Ground Truth:     {len(ground_truth):>6,} chars")
    print(f"  Whisper Baseline: {len(baseline):>6,} chars")
    print(f"  Whisper Biased:   {len(biased):>6,} chars")
    
    # Extract technical terms
    gt_terms = extract_technical_terms(ground_truth)
    print(f"\n🔧 Technical Terms Found in Ground Truth: {len(gt_terms)}")
    
    # Count occurrences
    gt_counts = count_term_occurrences(ground_truth, gt_terms)
    baseline_counts = count_term_occurrences(baseline, gt_terms)
    biased_counts = count_term_occurrences(biased, gt_terms)
    
    # Calculate recall
    baseline_recall = calculate_recall(gt_counts, baseline_counts)
    biased_recall = calculate_recall(gt_counts, biased_counts)
    
    # Similarity
    baseline_sim = fuzz.ratio(ground_truth.lower()[:5000], baseline.lower()[:5000])
    biased_sim = fuzz.ratio(ground_truth.lower()[:5000], biased.lower()[:5000])
    
    # Hallucination detection
    baseline_hall = detect_hallucination(baseline)
    biased_hall = detect_hallucination(biased)
    
    print("\n" + "=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    
    print(f"\n{'Metric':<30} {'Baseline':<15} {'Visual Biased':<15} {'Difference':<15}")
    print("-" * 75)
    print(f"{'Term Recall':<30} {baseline_recall:>12.1%} {biased_recall:>14.1%} {(biased_recall-baseline_recall)*100:>+12.1f}%")
    print(f"{'Fuzzy Similarity':<30} {baseline_sim:>12}% {biased_sim:>14}% {biased_sim-baseline_sim:>+12}%")
    print(f"{'Repetition Ratio':<30} {baseline_hall['repetition_ratio']:>12.1%} {biased_hall['repetition_ratio']:>14.1%} {(biased_hall['repetition_ratio']-baseline_hall['repetition_ratio'])*100:>+12.1f}%")
    print(f"{'Unique Words':<30} {baseline_hall['unique_words']:>12} {biased_hall['unique_words']:>14} {biased_hall['unique_words']-baseline_hall['unique_words']:>+12}")
    
    # Per-term breakdown
    print("\n" + "=" * 80)
    print("TERM-BY-TERM ANALYSIS (Top 20 by ground truth frequency)")
    print("=" * 80)
    
    sorted_terms = sorted(gt_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    print(f"\n{'Term':<15} {'GT':>8} {'Baseline':>10} {'Biased':>10} {'BL Acc':>10} {'Bias Acc':>10} {'Winner':>10}")
    print("-" * 75)
    
    baseline_wins = 0
    biased_wins = 0
    ties = 0
    
    for term, gt_count in sorted_terms:
        bl_count = baseline_counts[term]
        bi_count = biased_counts[term]
        
        bl_acc = min(bl_count / gt_count, 1.0) if gt_count > 0 else 0
        bi_acc = min(bi_count / gt_count, 1.0) if gt_count > 0 else 0
        
        if bi_acc > bl_acc:
            winner = "BIASED ✓"
            biased_wins += 1
        elif bl_acc > bi_acc:
            winner = "BASELINE"
            baseline_wins += 1
        else:
            winner = "TIE"
            ties += 1
        
        print(f"{term:<15} {gt_count:>8} {bl_count:>10} {bi_count:>10} {bl_acc:>9.0%} {bi_acc:>10.0%} {winner:>10}")
    
    print("-" * 75)
    print(f"{'WINS':<15} {'':<8} {baseline_wins:>10} {biased_wins:>10} {'':>10} {'':>10} {'TIES: ' + str(ties):>10}")
    
    # Hallucination check
    print("\n" + "=" * 80)
    print("HALLUCINATION CHECK (excessive word repetition)")
    print("=" * 80)
    
    if baseline_hall['excessive_repeats']:
        print(f"\n⚠ Baseline has excessive repeats:")
        for word, count in sorted(baseline_hall['excessive_repeats'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   '{word}': {count} times")
    else:
        print("\n✓ Baseline: No excessive repetition detected")
    
    if biased_hall['excessive_repeats']:
        print(f"\n⚠ Visual Biased has excessive repeats:")
        for word, count in sorted(biased_hall['excessive_repeats'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   '{word}': {count} times")
    else:
        print("\n✓ Visual Biased: No excessive repetition detected")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    
    if biased_recall > baseline_recall + 0.05:
        print("\n✅ Visual Bias HELPS: Improves term recall significantly")
        verdict = "VISUAL_BIAS_HELPS"
    elif baseline_recall > biased_recall + 0.05:
        print("\n❌ Visual Bias HURTS: Baseline is better")
        verdict = "VISUAL_BIAS_HURTS"
    else:
        print("\n➖ No significant difference between baseline and biased")
        verdict = "NO_DIFFERENCE"
    
    if biased_hall['excessive_repeats'] and len(biased_hall['excessive_repeats']) > len(baseline_hall['excessive_repeats']):
        print("⚠ WARNING: Visual bias causes more repetition/hallucination")
        verdict += "_WITH_HALLUCINATION"
    
    # Save results
    results = {
        'ground_truth_length': len(ground_truth),
        'baseline_length': len(baseline),
        'biased_length': len(biased),
        'technical_terms': list(gt_terms),
        'baseline_recall': baseline_recall,
        'biased_recall': biased_recall,
        'recall_difference': biased_recall - baseline_recall,
        'baseline_similarity': baseline_sim,
        'biased_similarity': biased_sim,
        'baseline_hallucination': baseline_hall,
        'biased_hallucination': biased_hall,
        'term_comparison': {
            term: {
                'ground_truth': gt_counts[term],
                'baseline': baseline_counts[term],
                'biased': biased_counts[term]
            } for term in gt_terms
        },
        'verdict': verdict,
        'baseline_wins': baseline_wins,
        'biased_wins': biased_wins,
        'ties': ties
    }
    
    output_path = base_path / "output/L2_evaluation_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_path}")


if __name__ == "__main__":
    main()
