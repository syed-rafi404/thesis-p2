#!/usr/bin/env python3
"""
=============================================================================
POST-ASR VISUAL CORRECTION - A Novel Multimodal Approach
=============================================================================
Master's Thesis - NOVELTY CONTRIBUTION

Instead of biasing ASR during generation (which causes hallucination),
this approach CORRECTS the transcript AFTER generation using visual keywords.

Key Insight:
- Whisper may mishear technical terms (e.g., "store" instead of "A*")
- Visual keywords from whiteboard provide ground truth spelling
- We find phonetically similar wrong words and correct them

This is SAFE because:
1. We never force wrong content - only fix misspellings
2. We preserve the original structure
3. We only correct words that sound similar to visual keywords

Example:
    Visual keyword: "polymorphism"
    ASR output: "palimorfism" (phonetic mishearing)
    Corrected: "polymorphism"

=============================================================================
"""

import re
import json
import sys
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from thefuzz import fuzz, process
from jiwer import wer


@dataclass
class Correction:
    """A single correction made to the transcript."""
    original: str
    corrected: str
    visual_keyword: str
    confidence: float
    position: int


def get_phonetic_similarity(word1: str, word2: str) -> float:
    """
    Calculate phonetic similarity between two words.
    Uses multiple fuzzy matching algorithms for robustness.
    """
    w1, w2 = word1.lower().strip(), word2.lower().strip()
    
    # Multiple similarity metrics
    ratio = fuzz.ratio(w1, w2)
    partial = fuzz.partial_ratio(w1, w2)
    token_sort = fuzz.token_sort_ratio(w1, w2)
    
    # Weighted average (partial ratio helps with subwords)
    similarity = (ratio * 0.4 + partial * 0.4 + token_sort * 0.2) / 100
    
    return similarity


def extract_words_with_positions(text: str) -> List[Tuple[str, int, int]]:
    """Extract words with their start and end positions."""
    words = []
    for match in re.finditer(r'\b\w+\b', text):
        words.append((match.group(), match.start(), match.end()))
    return words


def is_common_word(word: str) -> bool:
    """Check if word is too common to correct (avoid false positives)."""
    common = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
        'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
        'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
        'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
        'here', 'there', 'where', 'when', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'any', 'if', 'then', 'else', 'while', 'because', 'although',
        # Banglish common words
        'ami', 'amra', 'tumi', 'apni', 'se', 'era', 'ora', 'ta', 'eta',
        'ota', 'keno', 'ki', 'kobe', 'kotha', 'jani', 'boli', 'kori',
        'hoy', 'ache', 'thake', 'nai', 'na', 'ar', 'ebong', 'ba', 'kintu',
        'tahole', 'jodi', 'tobe', 'sei', 'ei', 'oi', 'je', 'jeta', 'seta',
    }
    return word.lower() in common


def correct_transcript_with_visual_keywords(
    transcript: str,
    visual_keywords: List[str],
    similarity_threshold: float = 0.75,  # Minimum similarity to correct
    min_keyword_length: int = 4,  # Don't correct using short keywords
    max_corrections_per_keyword: int = 5,  # Prevent over-correction
) -> Tuple[str, List[Correction], Dict]:
    """
    Correct transcript using visual keywords as spelling reference.
    
    Algorithm:
    1. For each visual keyword (length >= min_keyword_length)
    2. Find all words in transcript that are phonetically similar
    3. If similarity > threshold AND word isn't already correct, replace it
    4. Track all corrections for analysis
    
    Args:
        transcript: Original ASR transcript
        visual_keywords: Keywords extracted from visual analysis
        similarity_threshold: Minimum similarity score to make correction (0-1)
        min_keyword_length: Minimum keyword length to use for correction
        max_corrections_per_keyword: Maximum times to apply one keyword
        
    Returns:
        Tuple of (corrected_transcript, list of corrections, stats)
    """
    corrections = []
    corrected_text = transcript
    stats = {
        'original_length': len(transcript),
        'keywords_used': 0,
        'total_corrections': 0,
        'keywords_skipped_short': 0,
        'keywords_skipped_common': 0,
    }
    
    # Filter keywords
    valid_keywords = []
    for kw in visual_keywords:
        kw_clean = kw.strip()
        if len(kw_clean) < min_keyword_length:
            stats['keywords_skipped_short'] += 1
            continue
        if is_common_word(kw_clean):
            stats['keywords_skipped_common'] += 1
            continue
        valid_keywords.append(kw_clean)
    
    stats['keywords_used'] = len(valid_keywords)
    
    # Extract words from transcript
    words_with_pos = extract_words_with_positions(corrected_text)
    
    # Track which positions have been corrected (avoid double-correction)
    corrected_positions = set()
    
    # For each keyword, find similar words to correct
    keyword_correction_counts = Counter()
    
    for keyword in valid_keywords:
        kw_lower = keyword.lower()
        
        for word, start, end in words_with_pos:
            # Skip if already corrected at this position
            if start in corrected_positions:
                continue
            
            # Skip if word is too short
            if len(word) < 3:
                continue
                
            # Skip common words
            if is_common_word(word):
                continue
            
            # Skip if word is already the keyword
            if word.lower() == kw_lower:
                continue
            
            # Skip if we've made too many corrections with this keyword
            if keyword_correction_counts[keyword] >= max_corrections_per_keyword:
                continue
            
            # Calculate similarity
            similarity = get_phonetic_similarity(word, keyword)
            
            # Length ratio check - avoid correcting very different length words
            len_ratio = min(len(word), len(keyword)) / max(len(word), len(keyword))
            if len_ratio < 0.5:  # Words should be within 2x length of each other
                continue
            
            # Make correction if similar enough
            if similarity >= similarity_threshold:
                correction = Correction(
                    original=word,
                    corrected=keyword,
                    visual_keyword=keyword,
                    confidence=similarity,
                    position=start
                )
                corrections.append(correction)
                corrected_positions.add(start)
                keyword_correction_counts[keyword] += 1
    
    # Apply corrections (sort by position descending to maintain indices)
    corrections.sort(key=lambda c: c.position, reverse=True)
    
    for corr in corrections:
        # Find the word at the position and replace
        before = corrected_text[:corr.position]
        after = corrected_text[corr.position + len(corr.original):]
        corrected_text = before + corr.corrected + after
    
    stats['total_corrections'] = len(corrections)
    stats['corrected_length'] = len(corrected_text)
    
    return corrected_text, corrections, stats


def evaluate_correction(
    original_transcript: str,
    corrected_transcript: str,
    ground_truth: str,
    technical_terms: List[str] = None
) -> Dict:
    """
    Evaluate the quality of correction against ground truth.
    """
    if technical_terms is None:
        technical_terms = [
            'class', 'object', 'design', 'method', 'main', 'public', 'static',
            'void', 'java', 'file', 'tester', 'driver', 'compile', 'run',
            'template', 'blueprint', 'separate', 'code', 'string', 'system',
            'tutorial', 'execute', 'save', 'variable', 'access', 'modifier',
            'package', 'folder', 'manipulate', 'curly', 'braces'
        ]
    
    gt_lower = ground_truth.lower()
    orig_lower = original_transcript.lower()
    corr_lower = corrected_transcript.lower()
    
    # Count term occurrences
    gt_counts = {t: len(re.findall(rf'\b{t}\b', gt_lower)) for t in technical_terms}
    orig_counts = {t: len(re.findall(rf'\b{t}\b', orig_lower)) for t in technical_terms}
    corr_counts = {t: len(re.findall(rf'\b{t}\b', corr_lower)) for t in technical_terms}
    
    # Calculate recall
    def calc_recall(counts):
        total_gt = sum(gt_counts.values())
        found = sum(min(counts.get(t, 0), gt_counts[t]) for t in gt_counts if gt_counts[t] > 0)
        return found / total_gt if total_gt > 0 else 0
    
    orig_recall = calc_recall(orig_counts)
    corr_recall = calc_recall(corr_counts)
    
    # Similarity scores
    from thefuzz import fuzz
    orig_sim = fuzz.ratio(gt_lower[:5000], orig_lower[:5000])
    corr_sim = fuzz.ratio(gt_lower[:5000], corr_lower[:5000])
    
    # Per-term improvement
    term_improvements = {}
    for term in technical_terms:
        gt_c = gt_counts[term]
        if gt_c > 0:
            orig_acc = min(orig_counts[term] / gt_c, 1.0)
            corr_acc = min(corr_counts[term] / gt_c, 1.0)
            term_improvements[term] = {
                'ground_truth': gt_c,
                'original': orig_counts[term],
                'corrected': corr_counts[term],
                'improvement': corr_acc - orig_acc
            }
    
    return {
        'original_recall': orig_recall,
        'corrected_recall': corr_recall,
        'recall_improvement': corr_recall - orig_recall,
        'original_similarity': orig_sim,
        'corrected_similarity': corr_sim,
        'similarity_improvement': corr_sim - orig_sim,
        'term_improvements': term_improvements
    }


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Load data
    print("=" * 80)
    print("POST-ASR VISUAL CORRECTION - Novel Multimodal Approach")
    print("=" * 80)
    
    # Ground truth
    gt_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    with open(gt_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    ground_truth = re.sub(r'\[\d+:\d+(?::\d+)?-\d+:\d+(?::\d+)?\]', '', ground_truth)
    ground_truth = ' '.join(ground_truth.split())
    
    # Baseline transcript
    baseline_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt"
    with open(baseline_path, 'r', encoding='utf-8') as f:
        baseline_transcript = f.read().strip()
    
    # Visual keywords
    keywords_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
    with open(keywords_path, 'r', encoding='utf-8') as f:
        visual_keywords = json.load(f)
    
    print(f"\n📊 Data Loaded:")
    print(f"  Ground Truth: {len(ground_truth):,} chars")
    print(f"  Baseline Transcript: {len(baseline_transcript):,} chars")
    print(f"  Visual Keywords: {visual_keywords}")
    
    # Apply correction
    print("\n" + "=" * 80)
    print("APPLYING POST-ASR CORRECTION")
    print("=" * 80)
    
    corrected, corrections, stats = correct_transcript_with_visual_keywords(
        transcript=baseline_transcript,
        visual_keywords=visual_keywords,
        similarity_threshold=0.70,  # 70% similarity required
        min_keyword_length=4,
        max_corrections_per_keyword=5
    )
    
    print(f"\n📝 Correction Stats:")
    print(f"  Keywords used: {stats['keywords_used']}")
    print(f"  Total corrections made: {stats['total_corrections']}")
    print(f"  Keywords skipped (too short): {stats['keywords_skipped_short']}")
    print(f"  Keywords skipped (common word): {stats['keywords_skipped_common']}")
    
    if corrections:
        print(f"\n🔧 Corrections Applied:")
        for c in corrections[:15]:  # Show first 15
            print(f"   '{c.original}' → '{c.corrected}' (similarity: {c.confidence:.0%})")
    
    # Evaluate
    print("\n" + "=" * 80)
    print("EVALUATION AGAINST GROUND TRUTH")
    print("=" * 80)
    
    eval_results = evaluate_correction(
        original_transcript=baseline_transcript,
        corrected_transcript=corrected,
        ground_truth=ground_truth
    )
    
    print(f"\n{'Metric':<25} {'Original':>12} {'Corrected':>12} {'Change':>12}")
    print("-" * 63)
    print(f"{'Term Recall':<25} {eval_results['original_recall']:>11.1%} {eval_results['corrected_recall']:>11.1%} {eval_results['recall_improvement']:>+11.1%}")
    print(f"{'Fuzzy Similarity':<25} {eval_results['original_similarity']:>11}% {eval_results['corrected_similarity']:>11}% {eval_results['similarity_improvement']:>+11}%")
    
    # Show term-level improvements
    print("\n📈 Term-Level Analysis (showing improvements):")
    improvements = [(t, d) for t, d in eval_results['term_improvements'].items() if d['improvement'] != 0]
    improvements.sort(key=lambda x: x[1]['improvement'], reverse=True)
    
    if improvements:
        for term, data in improvements[:10]:
            arrow = "↑" if data['improvement'] > 0 else "↓"
            print(f"   {term:<15}: {data['original']:>3} → {data['corrected']:>3} (GT: {data['ground_truth']}) {arrow} {data['improvement']:+.0%}")
    else:
        print("   No term-level changes detected")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    
    if eval_results['recall_improvement'] > 0:
        print(f"\n✅ SUCCESS! Post-ASR correction improved term recall by {eval_results['recall_improvement']:+.1%}")
        print(f"   Original: {eval_results['original_recall']:.1%} → Corrected: {eval_results['corrected_recall']:.1%}")
    elif eval_results['recall_improvement'] == 0:
        print(f"\n➖ No change in term recall")
    else:
        print(f"\n❌ Correction decreased term recall by {eval_results['recall_improvement']:.1%}")
    
    # Save results
    output = {
        'method': 'post_asr_visual_correction',
        'stats': stats,
        'corrections': [
            {'original': c.original, 'corrected': c.corrected, 'confidence': c.confidence}
            for c in corrections
        ],
        'evaluation': {
            'original_recall': eval_results['original_recall'],
            'corrected_recall': eval_results['corrected_recall'],
            'improvement': eval_results['recall_improvement'],
            'original_similarity': eval_results['original_similarity'],
            'corrected_similarity': eval_results['corrected_similarity'],
        },
        'corrected_transcript': corrected
    }
    
    output_path = base_path / "output/post_asr_correction_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_path}")
    
    # Show sample of corrected transcript
    print("\n" + "=" * 80)
    print("SAMPLE TRANSCRIPTS (first 500 chars)")
    print("=" * 80)
    print(f"\n[ORIGINAL]")
    print(baseline_transcript[:500])
    print(f"\n[CORRECTED]")
    print(corrected[:500])


if __name__ == "__main__":
    main()
