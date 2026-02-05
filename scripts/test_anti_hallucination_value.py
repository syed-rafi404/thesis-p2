#!/usr/bin/env python3
"""
=============================================================================
TEST: Does Anti-Hallucination Filtering Improve ASR Quality?
=============================================================================
Compare raw Whisper output vs cleaned output against ground truth.
=============================================================================
"""

import re
import sys
from pathlib import Path
from collections import Counter
from thefuzz import fuzz

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.visual_bias_processor import clean_transcript

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
    """Extract Java/programming technical terms"""
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
        r'\bcompile\b', r'\bexecute\b', r'\brun\b',
        # Concepts
        r'\bdesign\b', r'\btemplate\b', r'\bblueprint\b',
        r'\btester\b', r'\bdriver\b', r'\bfile\b', r'\bcode\b',
        r'\bpackage\b', r'\bfolder\b', r'\bJava\b', r'\bOOP\b',
        r'\btutorial\b', r'\bseparate\b', r'\bexample\b',
        r'\bmanipulate\b', r'\baccess\b', r'\bmodifier\b'
    ]
    found = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found.update([m.lower() for m in matches])
    return found


def count_term_occurrences(text: str, terms: set) -> dict:
    counts = {}
    text_lower = text.lower()
    for term in terms:
        counts[term] = len(re.findall(rf'\b{re.escape(term)}\b', text_lower, re.IGNORECASE))
    return counts


def calculate_recall(gt_counts: dict, tr_counts: dict) -> float:
    total_gt = sum(gt_counts.values())
    if total_gt == 0:
        return 0
    total_found = sum(min(tr_counts.get(t, 0), gt_counts[t]) for t in gt_counts)
    return total_found / total_gt


def count_repetitions(text: str) -> dict:
    """Count word repetitions"""
    words = text.lower().split()
    word_counts = Counter(words)
    excessive = {w: c for w, c in word_counts.items() if c > 10}
    return {
        'total_words': len(words),
        'unique_words': len(word_counts),
        'repetition_ratio': 1 - (len(word_counts) / len(words)) if words else 0,
        'excessive': excessive
    }


def evaluate_transcript(name: str, transcript: str, ground_truth: str, gt_terms: set, gt_counts: dict):
    """Evaluate a transcript against ground truth"""
    tr_counts = count_term_occurrences(transcript, gt_terms)
    recall = calculate_recall(gt_counts, tr_counts)
    similarity = fuzz.ratio(ground_truth.lower(), transcript.lower())
    reps = count_repetitions(transcript)
    
    return {
        'name': name,
        'chars': len(transcript),
        'words': reps['total_words'],
        'unique_words': reps['unique_words'],
        'term_recall': recall,
        'similarity': similarity,
        'repetition_ratio': reps['repetition_ratio'],
        'excessive': reps['excessive']
    }


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    print("=" * 80)
    print("ANTI-HALLUCINATION VALUE TEST")
    print("Does clean_transcript() improve ASR quality?")
    print("=" * 80)
    
    # Test both L2 and L5
    lectures = [
        {
            'name': 'L2',
            'gt': base_path / "data/ground_truth/L2_ground_truth.txt",
            'baseline': base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt",
            'biased': base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt",
        },
        {
            'name': 'L5',
            'gt': base_path / "data/ground_truth/L5_ground_truth.txt",
            'baseline': base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_baseline.txt",
            'biased': base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_visual_biased.txt",
        }
    ]
    
    all_results = []
    
    for lecture in lectures:
        print(f"\n{'='*80}")
        print(f"LECTURE: {lecture['name']}")
        print("=" * 80)
        
        # Load ground truth
        ground_truth = load_ground_truth(lecture['gt'])
        gt_terms = extract_technical_terms(ground_truth)
        gt_counts = count_term_occurrences(ground_truth, gt_terms)
        
        # Load transcripts
        baseline_raw = load_transcript(lecture['baseline'])
        biased_raw = load_transcript(lecture['biased'])
        
        # Apply anti-hallucination cleaning
        baseline_cleaned = clean_transcript(baseline_raw)
        biased_cleaned = clean_transcript(biased_raw)
        
        print(f"\nGround Truth: {len(ground_truth):,} chars, {len(gt_terms)} technical terms")
        
        # Evaluate all versions
        results = {
            'baseline_raw': evaluate_transcript("Baseline (Raw)", baseline_raw, ground_truth, gt_terms, gt_counts),
            'baseline_clean': evaluate_transcript("Baseline (Cleaned)", baseline_cleaned, ground_truth, gt_terms, gt_counts),
            'biased_raw': evaluate_transcript("Biased (Raw)", biased_raw, ground_truth, gt_terms, gt_counts),
            'biased_clean': evaluate_transcript("Biased (Cleaned)", biased_cleaned, ground_truth, gt_terms, gt_counts),
        }
        
        # Print comparison table
        print(f"\n{'Transcript':<25} {'Chars':>8} {'Words':>8} {'Unique':>8} {'TTR':>8} {'Sim':>6} {'RepRatio':>10}")
        print("-" * 85)
        
        for key in ['baseline_raw', 'baseline_clean', 'biased_raw', 'biased_clean']:
            r = results[key]
            print(f"{r['name']:<25} {r['chars']:>8,} {r['words']:>8,} {r['unique_words']:>8} {r['term_recall']*100:>7.1f}% {r['similarity']:>5}% {r['repetition_ratio']*100:>9.1f}%")
        
        # Calculate improvements
        print(f"\n--- ANTI-HALLUCINATION IMPROVEMENT ---")
        
        # Baseline improvement
        bl_recall_diff = results['baseline_clean']['term_recall'] - results['baseline_raw']['term_recall']
        bl_sim_diff = results['baseline_clean']['similarity'] - results['baseline_raw']['similarity']
        bl_rep_diff = results['baseline_clean']['repetition_ratio'] - results['baseline_raw']['repetition_ratio']
        
        print(f"\nBaseline: Raw -> Cleaned")
        print(f"  Term Recall:      {results['baseline_raw']['term_recall']*100:.1f}% -> {results['baseline_clean']['term_recall']*100:.1f}% ({bl_recall_diff*100:+.1f}%)")
        print(f"  Similarity:       {results['baseline_raw']['similarity']}% -> {results['baseline_clean']['similarity']}% ({bl_sim_diff:+d}%)")
        print(f"  Repetition Ratio: {results['baseline_raw']['repetition_ratio']*100:.1f}% -> {results['baseline_clean']['repetition_ratio']*100:.1f}% ({bl_rep_diff*100:+.1f}%)")
        
        # Biased improvement
        bi_recall_diff = results['biased_clean']['term_recall'] - results['biased_raw']['term_recall']
        bi_sim_diff = results['biased_clean']['similarity'] - results['biased_raw']['similarity']
        bi_rep_diff = results['biased_clean']['repetition_ratio'] - results['biased_raw']['repetition_ratio']
        
        print(f"\nBiased: Raw -> Cleaned")
        print(f"  Term Recall:      {results['biased_raw']['term_recall']*100:.1f}% -> {results['biased_clean']['term_recall']*100:.1f}% ({bi_recall_diff*100:+.1f}%)")
        print(f"  Similarity:       {results['biased_raw']['similarity']}% -> {results['biased_clean']['similarity']}% ({bi_sim_diff:+d}%)")
        print(f"  Repetition Ratio: {results['biased_raw']['repetition_ratio']*100:.1f}% -> {results['biased_clean']['repetition_ratio']*100:.1f}% ({bi_rep_diff*100:+.1f}%)")
        
        # Show what was removed
        print(f"\n--- HALLUCINATIONS REMOVED ---")
        
        if results['baseline_raw']['excessive']:
            print(f"\nBaseline excessive words (before): {dict(sorted(results['baseline_raw']['excessive'].items(), key=lambda x: -x[1])[:5])}")
        if results['baseline_clean']['excessive']:
            print(f"Baseline excessive words (after):  {dict(sorted(results['baseline_clean']['excessive'].items(), key=lambda x: -x[1])[:5])}")
        else:
            print(f"Baseline excessive words (after):  None (all cleaned!)")
            
        if results['biased_raw']['excessive']:
            print(f"\nBiased excessive words (before): {dict(sorted(results['biased_raw']['excessive'].items(), key=lambda x: -x[1])[:5])}")
        if results['biased_clean']['excessive']:
            print(f"Biased excessive words (after):  {dict(sorted(results['biased_clean']['excessive'].items(), key=lambda x: -x[1])[:5])}")
        else:
            print(f"Biased excessive words (after):  None (all cleaned!)")
        
        all_results.append({
            'lecture': lecture['name'],
            'baseline_improvement': {
                'term_recall': bl_recall_diff,
                'similarity': bl_sim_diff
            },
            'biased_improvement': {
                'term_recall': bi_recall_diff,
                'similarity': bi_sim_diff
            }
        })
    
    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY: Anti-Hallucination Value")
    print("=" * 80)
    
    avg_bl_recall = sum(r['baseline_improvement']['term_recall'] for r in all_results) / len(all_results)
    avg_bl_sim = sum(r['baseline_improvement']['similarity'] for r in all_results) / len(all_results)
    avg_bi_recall = sum(r['biased_improvement']['term_recall'] for r in all_results) / len(all_results)
    avg_bi_sim = sum(r['biased_improvement']['similarity'] for r in all_results) / len(all_results)
    
    print(f"\nAverage improvement from clean_transcript():")
    print(f"  Baseline: {avg_bl_recall*100:+.1f}% term recall, {avg_bl_sim:+.1f}% similarity")
    print(f"  Biased:   {avg_bi_recall*100:+.1f}% term recall, {avg_bi_sim:+.1f}% similarity")
    
    if avg_bl_recall > 0 or avg_bi_recall > 0:
        print(f"\n[OK] Anti-hallucination filtering IMPROVES transcript quality")
    else:
        print(f"\n[--] Anti-hallucination filtering has minimal effect on these transcripts")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
