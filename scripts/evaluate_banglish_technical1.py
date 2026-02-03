#!/usr/bin/env python3
"""
Comprehensive evaluation of BanglishTechnical1 (Real Classroom Video)
against ground truth, comparing with L2/L3/L5 (Screen Recording) results.
"""

import json
import re
from pathlib import Path
from collections import Counter
from thefuzz import fuzz
from datetime import datetime

# Paths
GT_PATH = Path("data/ground_truth/BanglishTechnical1_ground_truth.txt")
OUTPUT_DIR = Path("output/BanglishTechnical1_RealClass")
BASELINE_PATH = OUTPUT_DIR / "transcript_whisper_baseline.txt"
BIASED_PATH = OUTPUT_DIR / "transcript_whisper_temporal_biased.txt"
FUSED_PATH = OUTPUT_DIR / "transcript_fused.txt"
VISUAL_KEYWORDS_PATH = OUTPUT_DIR / "visual_keywords.json"

def load_ground_truth():
    """Load and clean ground truth."""
    text = GT_PATH.read_text(encoding='utf-8')
    # Remove header comments and timestamps
    lines = []
    in_content = False
    for line in text.split('\n'):
        if line.startswith('# ===='):
            in_content = True
            continue
        if in_content and line.strip():
            # Remove timestamp markers
            clean = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', line).strip()
            if clean:
                lines.append(clean)
    return ' '.join(lines)

def extract_technical_terms(text):
    """Extract technical and meaningful terms from ground truth."""
    # Python/programming related terms
    tech_terms = [
        'python', 'variable', 'variables', 'string', 'integer', 'boolean', 
        'float', 'data', 'type', 'datatype', 'box', 'value', 'store',
        'int', 'str', 'true', 'false', 'name', 'age', 'fruit', 'apple',
        'decimal', 'number', 'dynamic', 'underscore', 'snake', 'camel',
        'casing', 'case', 'sensitive', 'convention', 'rule', 'error',
        'valid', 'isvalid', 'pi', 'environment', 'vscode', 'pycharm',
        'programming', 'code', 'fundamental', 'basic', 'arithmetic',
        'operation', 'capital', 'letter', 'small', 'whole', 'type()',
        'quotation', 'double', 'single', 'meaningful', 'developer'
    ]
    
    # Also find Banglish terms
    banglish_terms = [
        'amra', 'eta', 'holo', 'jeta', 'tumi', 'ami', 'korte', 'dekhi',
        'likhte', 'bujhte', 'rakhte', 'shikhbo', 'bolte', 'dekhbo',
        'porobortite', 'thikache', 'karon', 'jemon', 'dhoro', 'evabe'
    ]
    
    text_lower = text.lower()
    found_tech = []
    for term in tech_terms:
        if term in text_lower:
            count = len(re.findall(r'\b' + term + r'\b', text_lower, re.IGNORECASE))
            if count > 0:
                found_tech.append((term, count))
    
    return found_tech

def count_word_frequencies(text):
    """Count word frequencies in text."""
    # Clean and tokenize
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    words = text.split()
    return Counter(words)

def calculate_excess_repetitions(text, threshold=3):
    """Calculate excess repetitions (hallucination measure)."""
    freq = count_word_frequencies(text)
    total_words = sum(freq.values())
    
    excess = 0
    flagged_terms = []
    
    for word, count in freq.most_common(50):
        if len(word) >= 3:  # Skip very short words
            expected = max(1, total_words / 500)  # Expected frequency
            if count > expected * threshold:
                excess_count = int(count - expected)
                excess += excess_count
                if excess_count > 5:
                    flagged_terms.append((word, count, excess_count))
    
    return excess, flagged_terms[:10]

def term_recall(gt_text, asr_text, terms=None):
    """Calculate term recall against ground truth."""
    if terms is None:
        terms = extract_technical_terms(gt_text)
    
    gt_lower = gt_text.lower()
    asr_lower = asr_text.lower()
    
    found = 0
    missed = []
    found_list = []
    
    for term, gt_count in terms:
        # Check if term exists in ASR output
        asr_count = len(re.findall(r'\b' + term + r'\b', asr_lower, re.IGNORECASE))
        if asr_count > 0:
            found += 1
            found_list.append(term)
        else:
            missed.append(term)
    
    return found, len(terms), found_list, missed

def calculate_fuzzy_similarity(gt_text, asr_text, sample_size=500):
    """Calculate fuzzy similarity on a sample."""
    gt_words = gt_text.split()[:sample_size]
    asr_words = asr_text.split()[:sample_size]
    
    gt_sample = ' '.join(gt_words)
    asr_sample = ' '.join(asr_words)
    
    return fuzz.ratio(gt_sample, asr_sample)

def cmv_f_analysis(asr_text, visual_keywords, threshold=3.0):
    """CMV-F (Frequency-Aware Cross-Modal Verification) analysis."""
    freq = count_word_frequencies(asr_text)
    total_words = sum(freq.values())
    
    # Check visual keywords frequency
    visual_kw_lower = [kw.lower() for kw in visual_keywords]
    
    grounded = 0
    hallucinated = []
    over_represented = []
    
    for kw in visual_kw_lower:
        kw_simple = kw.split()[0] if ' ' in kw else kw  # Take first word
        count = freq.get(kw_simple, 0)
        expected = total_words / 200  # Baseline expectation
        
        if count > 0:
            grounded += 1
            tfd = count / max(expected, 1)
            if tfd > threshold:
                over_represented.append((kw_simple, count, tfd))
    
    # Calculate repetition hallucination rate
    rhr_words = 0
    for word, count in freq.most_common(100):
        if len(word) >= 3 and count > (total_words / 100):
            rhr_words += count
    
    rhr = (rhr_words / total_words * 100) if total_words > 0 else 0
    
    return {
        'grounded_keywords': grounded,
        'total_visual_keywords': len(visual_keywords),
        'over_represented': over_represented[:5],
        'repetition_hallucination_rate': round(rhr, 2)
    }

def main():
    print("=" * 70)
    print("BANGLISH TECHNICAL 1 - REAL CLASSROOM VIDEO EVALUATION")
    print("=" * 70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Load data
    gt_text = load_ground_truth()
    baseline_text = BASELINE_PATH.read_text(encoding='utf-8')
    biased_text = BIASED_PATH.read_text(encoding='utf-8')
    fused_text = FUSED_PATH.read_text(encoding='utf-8')
    visual_keywords = json.loads(VISUAL_KEYWORDS_PATH.read_text(encoding='utf-8'))
    
    print(f"Ground Truth: {len(gt_text):,} chars")
    print(f"Baseline ASR: {len(baseline_text):,} chars")
    print(f"Visual-Biased ASR: {len(biased_text):,} chars")
    print(f"Fused Transcript: {len(fused_text):,} chars")
    print(f"Visual Keywords: {len(visual_keywords)}")
    print()
    
    # Extract terms from ground truth
    tech_terms = extract_technical_terms(gt_text)
    print(f"Technical Terms in Ground Truth: {len(tech_terms)}")
    print(f"Terms: {[t[0] for t in tech_terms[:15]]}...")
    print()
    
    # ==================== TERM RECALL ====================
    print("=" * 70)
    print("TABLE 1: TERM RECALL (% of Ground Truth Terms Captured)")
    print("=" * 70)
    
    baseline_found, total_terms, baseline_list, baseline_missed = term_recall(gt_text, baseline_text, tech_terms)
    biased_found, _, biased_list, biased_missed = term_recall(gt_text, biased_text, tech_terms)
    fused_found, _, fused_list, fused_missed = term_recall(gt_text, fused_text, tech_terms)
    
    baseline_recall = baseline_found / total_terms * 100
    biased_recall = biased_found / total_terms * 100
    fused_recall = fused_found / total_terms * 100
    bias_impact = biased_recall - baseline_recall
    
    print(f"{'Transcript':<25} {'Found':<8} {'Total':<8} {'Recall':<10} {'Impact':<10}")
    print("-" * 70)
    print(f"{'Baseline':<25} {baseline_found:<8} {total_terms:<8} {baseline_recall:>6.1f}% {'-':<10}")
    print(f"{'Visual-Biased':<25} {biased_found:<8} {total_terms:<8} {biased_recall:>6.1f}% {bias_impact:>+6.1f}%")
    print(f"{'Fused':<25} {fused_found:<8} {total_terms:<8} {fused_recall:>6.1f}% {fused_recall - baseline_recall:>+6.1f}%")
    print()
    print(f"Missed by Baseline: {baseline_missed[:5]}")
    print()
    
    # ==================== EXCESS REPETITIONS ====================
    print("=" * 70)
    print("TABLE 2: EXCESS REPETITIONS (Hallucination Measure)")
    print("=" * 70)
    
    baseline_excess, baseline_flagged = calculate_excess_repetitions(baseline_text)
    biased_excess, biased_flagged = calculate_excess_repetitions(biased_text)
    fused_excess, fused_flagged = calculate_excess_repetitions(fused_text)
    
    print(f"{'Transcript':<25} {'Excess Reps':<15} {'Top Offenders':<40}")
    print("-" * 70)
    print(f"{'Baseline':<25} {baseline_excess:<15} {str(baseline_flagged[:3]):<40}")
    print(f"{'Visual-Biased':<25} {biased_excess:<15} {str(biased_flagged[:3]):<40}")
    print(f"{'Fused':<25} {fused_excess:<15} {str(fused_flagged[:3]):<40}")
    print()
    
    excess_increase = ((biased_excess - baseline_excess) / max(baseline_excess, 1)) * 100
    print(f"Bias Impact: {excess_increase:+.1f}% excess repetitions")
    print()
    
    # ==================== CMV-F ANALYSIS ====================
    print("=" * 70)
    print("TABLE 3: CMV-F (Frequency-Aware Cross-Modal Verification)")
    print("=" * 70)
    
    baseline_cmv = cmv_f_analysis(baseline_text, visual_keywords)
    biased_cmv = cmv_f_analysis(biased_text, visual_keywords)
    fused_cmv = cmv_f_analysis(fused_text, visual_keywords)
    
    print(f"{'Transcript':<25} {'RHR':<10} {'Grounded':<12} {'Over-Rep Keywords':<30}")
    print("-" * 70)
    print(f"{'Baseline':<25} {baseline_cmv['repetition_hallucination_rate']:>6.1f}%  {baseline_cmv['grounded_keywords']}/{baseline_cmv['total_visual_keywords']:<9} {str([x[0] for x in baseline_cmv['over_represented']]):<30}")
    print(f"{'Visual-Biased':<25} {biased_cmv['repetition_hallucination_rate']:>6.1f}%  {biased_cmv['grounded_keywords']}/{biased_cmv['total_visual_keywords']:<9} {str([x[0] for x in biased_cmv['over_represented']]):<30}")
    print(f"{'Fused':<25} {fused_cmv['repetition_hallucination_rate']:>6.1f}%  {fused_cmv['grounded_keywords']}/{fused_cmv['total_visual_keywords']:<9} {str([x[0] for x in fused_cmv['over_represented']]):<30}")
    print()
    
    rhr_improvement = biased_cmv['repetition_hallucination_rate'] - baseline_cmv['repetition_hallucination_rate']
    print(f"CMV-F RHR Impact: {rhr_improvement:+.1f}% (higher = more hallucinations detected)")
    print()
    
    # ==================== FUZZY SIMILARITY ====================
    print("=" * 70)
    print("TABLE 4: FUZZY SIMILARITY TO GROUND TRUTH")
    print("=" * 70)
    
    baseline_sim = calculate_fuzzy_similarity(gt_text, baseline_text)
    biased_sim = calculate_fuzzy_similarity(gt_text, biased_text)
    fused_sim = calculate_fuzzy_similarity(gt_text, fused_text)
    
    print(f"{'Transcript':<25} {'Similarity':<15}")
    print("-" * 40)
    print(f"{'Baseline':<25} {baseline_sim:>6}%")
    print(f"{'Visual-Biased':<25} {biased_sim:>6}%")
    print(f"{'Fused':<25} {fused_sim:>6}%")
    print()
    
    # ==================== COMPARISON WITH L2/L3/L5 ====================
    print("=" * 70)
    print("COMPARISON: Real Classroom vs Screen Recordings (L2/L3/L5)")
    print("=" * 70)
    
    l2_l3_l5_avg = {
        'term_recall_baseline': 26.1,
        'term_recall_biased': 21.3,
        'bias_impact_recall': -4.7,
        'excess_baseline': 475,
        'excess_biased': 946,
        'excess_increase': 99,
        'cmv_f_rhr_improvement': 42.4
    }
    
    print(f"{'Metric':<35} {'L2/L3/L5 (Screen)':<20} {'BanglishTech1 (Real)':<20} {'Diff':<10}")
    print("-" * 85)
    print(f"{'Term Recall (Baseline)':<35} {l2_l3_l5_avg['term_recall_baseline']:>6.1f}% {baseline_recall:>18.1f}% {baseline_recall - l2_l3_l5_avg['term_recall_baseline']:>+8.1f}%")
    print(f"{'Term Recall (Biased)':<35} {l2_l3_l5_avg['term_recall_biased']:>6.1f}% {biased_recall:>18.1f}% {biased_recall - l2_l3_l5_avg['term_recall_biased']:>+8.1f}%")
    print(f"{'Bias Impact on Recall':<35} {l2_l3_l5_avg['bias_impact_recall']:>+6.1f}% {bias_impact:>+18.1f}% {'BETTER' if bias_impact > l2_l3_l5_avg['bias_impact_recall'] else 'SIMILAR':<10}")
    print(f"{'Excess Reps (Baseline)':<35} {l2_l3_l5_avg['excess_baseline']:>6} {baseline_excess:>18} {baseline_excess - l2_l3_l5_avg['excess_baseline']:>+8}")
    print(f"{'Excess Reps (Biased)':<35} {l2_l3_l5_avg['excess_biased']:>6} {biased_excess:>18} {biased_excess - l2_l3_l5_avg['excess_biased']:>+8}")
    print(f"{'CMV-F RHR Improvement':<35} {l2_l3_l5_avg['cmv_f_rhr_improvement']:>+6.1f}% {rhr_improvement:>+18.1f}% {'SIMILAR' if abs(rhr_improvement) < 10 else 'DIFFERENT':<10}")
    print()
    
    # ==================== SUMMARY ====================
    print("=" * 70)
    print("SUMMARY & FINDINGS")
    print("=" * 70)
    
    findings = []
    
    # Finding 1: Bias impact on recall
    if bias_impact < 0:
        findings.append(f"✅ Visual bias HURTS recall: {bias_impact:+.1f}% (consistent with L2/L3/L5)")
    else:
        findings.append(f"⚠️ Visual bias HELPS recall: {bias_impact:+.1f}% (INCONSISTENT with L2/L3/L5)")
    
    # Finding 2: Excess repetitions
    if excess_increase > 50:
        findings.append(f"✅ Visual bias increases hallucinations: +{excess_increase:.0f}% (consistent with L2/L3/L5)")
    elif excess_increase > 0:
        findings.append(f"⚠️ Visual bias slightly increases hallucinations: +{excess_increase:.0f}%")
    else:
        findings.append(f"❌ Visual bias REDUCES hallucinations: {excess_increase:.1f}% (INCONSISTENT)")
    
    # Finding 3: CMV-F effectiveness
    if rhr_improvement > 5:
        findings.append(f"✅ CMV-F detects hallucinations: +{rhr_improvement:.1f}% RHR in biased")
    else:
        findings.append(f"⚠️ CMV-F shows minimal difference: {rhr_improvement:+.1f}% RHR")
    
    # Finding 4: Baseline quality
    if baseline_recall > 50:
        findings.append(f"✅ High baseline quality: {baseline_recall:.1f}% term recall")
    elif baseline_recall > 30:
        findings.append(f"⚠️ Moderate baseline quality: {baseline_recall:.1f}% term recall")
    else:
        findings.append(f"❌ Low baseline quality: {baseline_recall:.1f}% term recall")
    
    for finding in findings:
        print(finding)
    
    print()
    print("=" * 70)
    print("RECOMMENDATION")
    print("=" * 70)
    
    # Calculate consistency score
    consistent_count = sum(1 for f in findings if '✅' in f)
    total_findings = len(findings)
    
    if consistent_count >= 3:
        print("📊 VERDICT: Results are CONSISTENT with L2/L3/L5 findings")
        print("   → Visual bias approach confirmed to hurt ASR accuracy across video types")
        print("   → CMV-F approach validated for real classroom environments")
    elif consistent_count >= 2:
        print("📊 VERDICT: Results are MOSTLY CONSISTENT with L2/L3/L5")
        print("   → Some differences may be due to audio quality/environment")
    else:
        print("📊 VERDICT: Results DIFFER from L2/L3/L5 findings")
        print("   → May indicate video-type-specific behavior")
    
    print()
    
    # ==================== SAVE RESULTS ====================
    results = {
        'video': 'BanglishTechnical1.MOV',
        'type': 'Real Classroom',
        'date': datetime.now().isoformat(),
        'ground_truth_chars': len(gt_text),
        'technical_terms_count': len(tech_terms),
        'metrics': {
            'term_recall': {
                'baseline': round(baseline_recall, 1),
                'visual_biased': round(biased_recall, 1),
                'fused': round(fused_recall, 1),
                'bias_impact': round(bias_impact, 1)
            },
            'excess_repetitions': {
                'baseline': baseline_excess,
                'visual_biased': biased_excess,
                'fused': fused_excess,
                'increase_percent': round(excess_increase, 1)
            },
            'cmv_f': {
                'baseline_rhr': baseline_cmv['repetition_hallucination_rate'],
                'biased_rhr': biased_cmv['repetition_hallucination_rate'],
                'rhr_improvement': round(rhr_improvement, 1)
            },
            'fuzzy_similarity': {
                'baseline': baseline_sim,
                'visual_biased': biased_sim,
                'fused': fused_sim
            }
        },
        'comparison_with_l2_l3_l5': {
            'consistent': consistent_count >= 3,
            'findings': findings
        }
    }
    
    output_file = OUTPUT_DIR / 'ground_truth_evaluation.json'
    output_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Results saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    results = main()
