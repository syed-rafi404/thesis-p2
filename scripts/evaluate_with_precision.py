#!/usr/bin/env python3
"""
=============================================================================
BETTER EVALUATION: Penalize Hallucination, Reward Accuracy
=============================================================================
Term Precision + Recall + F1 with hallucination penalty
=============================================================================
"""

import re
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.audio.visual_bias_processor import clean_transcript

def load_ground_truth(path: Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\[\d+:\d+(?::\d+)?-\d+:\d+(?::\d+)?\]', '', content)
    return ' '.join(content.split())

def load_transcript(path: Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def extract_technical_terms() -> list:
    """Technical terms to track"""
    return [
        'class', 'object', 'instance', 'method', 'public', 'private', 'static',
        'void', 'main', 'string', 'int', 'new', 'null', 'design', 'template',
        'blueprint', 'tester', 'driver', 'file', 'code', 'compile', 'execute',
        'run', 'java', 'tutorial', 'separate', 'manipulate', 'variable',
        'memory', 'location', 'reference', 'student', 'create', 'update',
        'store', 'copy', 'print', 'output', 'default', 'access', 'modifier'
    ]

def count_terms(text: str, terms: list) -> dict:
    counts = {}
    text_lower = text.lower()
    for term in terms:
        counts[term] = len(re.findall(rf'\b{re.escape(term)}\b', text_lower))
    return counts

def calculate_metrics(gt_counts: dict, tr_counts: dict) -> dict:
    """
    Calculate precision, recall, and F1 for term counts.
    
    Precision: How accurate are the terms? (penalizes over-generation)
    Recall: How many GT terms were captured?
    F1: Balanced score
    """
    terms = set(gt_counts.keys()) | set(tr_counts.keys())
    
    # Term-level metrics
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    for term in terms:
        gt = gt_counts.get(term, 0)
        tr = tr_counts.get(term, 0)
        
        if gt > 0:
            # Correct matches (capped at GT count)
            tp = min(gt, tr)
            true_positives += tp
            
            # Missed terms
            fn = max(0, gt - tr)
            false_negatives += fn
            
            # Over-generated terms (hallucination)
            fp = max(0, tr - gt)
            false_positives += fp
        else:
            # Term not in GT but in transcript = false positive
            false_positives += tr
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }

def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    terms = extract_technical_terms()
    
    print("=" * 90)
    print("HALLUCINATION-AWARE EVALUATION")
    print("Precision penalizes over-generation, Recall measures coverage, F1 balances both")
    print("=" * 90)
    
    lectures = [
        {
            'name': 'L2 - Design Class',
            'gt': base_path / "data/ground_truth/L2_ground_truth.txt",
            'baseline': base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt",
            'biased': base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt",
        },
        {
            'name': 'L5 - Memory Locations',
            'gt': base_path / "data/ground_truth/L5_ground_truth.txt",
            'baseline': base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_baseline.txt",
            'biased': base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_visual_biased.txt",
        }
    ]
    
    summary = []
    
    for lecture in lectures:
        print(f"\n{'='*90}")
        print(f"LECTURE: {lecture['name']}")
        print("=" * 90)
        
        gt = load_ground_truth(lecture['gt'])
        baseline_raw = load_transcript(lecture['baseline'])
        biased_raw = load_transcript(lecture['biased'])
        
        baseline_clean = clean_transcript(baseline_raw)
        biased_clean = clean_transcript(biased_raw)
        
        gt_counts = count_terms(gt, terms)
        
        results = {}
        for name, text in [
            ('Baseline Raw', baseline_raw),
            ('Baseline Cleaned', baseline_clean),
            ('Biased Raw', biased_raw),
            ('Biased Cleaned', biased_clean)
        ]:
            tr_counts = count_terms(text, terms)
            metrics = calculate_metrics(gt_counts, tr_counts)
            results[name] = metrics
        
        print(f"\n{'Transcript':<20} {'Precision':>10} {'Recall':>10} {'F1':>10} {'TP':>6} {'FP':>6} {'FN':>6}")
        print("-" * 75)
        
        for name in ['Baseline Raw', 'Baseline Cleaned', 'Biased Raw', 'Biased Cleaned']:
            m = results[name]
            print(f"{name:<20} {m['precision']*100:>9.1f}% {m['recall']*100:>9.1f}% {m['f1']*100:>9.1f}% {m['true_positives']:>6} {m['false_positives']:>6} {m['false_negatives']:>6}")
        
        # Calculate improvements
        print(f"\n--- ANTI-HALLUCINATION IMPROVEMENT ---")
        
        # Baseline
        bl_raw = results['Baseline Raw']
        bl_clean = results['Baseline Cleaned']
        print(f"\nBaseline: Raw -> Cleaned")
        print(f"  Precision: {bl_raw['precision']*100:.1f}% -> {bl_clean['precision']*100:.1f}% ({(bl_clean['precision']-bl_raw['precision'])*100:+.1f}%)")
        print(f"  F1 Score:  {bl_raw['f1']*100:.1f}% -> {bl_clean['f1']*100:.1f}% ({(bl_clean['f1']-bl_raw['f1'])*100:+.1f}%)")
        print(f"  FP (halluc): {bl_raw['false_positives']} -> {bl_clean['false_positives']} ({bl_clean['false_positives']-bl_raw['false_positives']:+d})")
        
        # Biased
        bi_raw = results['Biased Raw']
        bi_clean = results['Biased Cleaned']
        print(f"\nBiased: Raw -> Cleaned")
        print(f"  Precision: {bi_raw['precision']*100:.1f}% -> {bi_clean['precision']*100:.1f}% ({(bi_clean['precision']-bi_raw['precision'])*100:+.1f}%)")
        print(f"  F1 Score:  {bi_raw['f1']*100:.1f}% -> {bi_clean['f1']*100:.1f}% ({(bi_clean['f1']-bi_raw['f1'])*100:+.1f}%)")
        print(f"  FP (halluc): {bi_raw['false_positives']} -> {bi_clean['false_positives']} ({bi_clean['false_positives']-bi_raw['false_positives']:+d})")
        
        summary.append({
            'lecture': lecture['name'],
            'baseline_f1_improvement': bl_clean['f1'] - bl_raw['f1'],
            'biased_f1_improvement': bi_clean['f1'] - bi_raw['f1'],
            'baseline_precision_improvement': bl_clean['precision'] - bl_raw['precision'],
            'biased_precision_improvement': bi_clean['precision'] - bi_raw['precision'],
            'baseline_fp_reduction': bl_raw['false_positives'] - bl_clean['false_positives'],
            'biased_fp_reduction': bi_raw['false_positives'] - bi_clean['false_positives'],
        })
    
    # Overall
    print("\n" + "=" * 90)
    print("OVERALL SUMMARY")
    print("=" * 90)
    
    avg_bl_f1 = sum(s['baseline_f1_improvement'] for s in summary) / len(summary)
    avg_bi_f1 = sum(s['biased_f1_improvement'] for s in summary) / len(summary)
    avg_bl_prec = sum(s['baseline_precision_improvement'] for s in summary) / len(summary)
    avg_bi_prec = sum(s['biased_precision_improvement'] for s in summary) / len(summary)
    total_bl_fp = sum(s['baseline_fp_reduction'] for s in summary)
    total_bi_fp = sum(s['biased_fp_reduction'] for s in summary)
    
    print(f"\nAnti-Hallucination Filter Impact:")
    print(f"\n  On Baseline ASR:")
    print(f"    F1 improvement:        {avg_bl_f1*100:+.1f}%")
    print(f"    Precision improvement: {avg_bl_prec*100:+.1f}%")
    print(f"    Hallucinations removed: {total_bl_fp}")
    
    print(f"\n  On Visual-Biased ASR:")
    print(f"    F1 improvement:        {avg_bi_f1*100:+.1f}%")
    print(f"    Precision improvement: {avg_bi_prec*100:+.1f}%")
    print(f"    Hallucinations removed: {total_bi_fp}")
    
    if avg_bi_prec > 0.05:
        print(f"\n✅ Anti-hallucination SIGNIFICANTLY improves precision for biased transcripts")
    if total_bi_fp > 100:
        print(f"✅ Removed {total_bi_fp} hallucinated term occurrences")
    
    print("=" * 90)

if __name__ == "__main__":
    main()
