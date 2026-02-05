#!/usr/bin/env python3
"""
=============================================================================
TEST: Does CrossModalVerifier detect real hallucinations?
=============================================================================
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.cross_modal_verifier import CrossModalVerifier

# Load transcripts
base_path = Path("c:/Users/T2520785/thesisP2")

# L2 visual keywords (from VLM)
l2_visual_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
l2_baseline_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt"
l2_biased_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt"

# L5 
l5_visual_path = base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/visual_keywords.json"
l5_baseline_path = base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_baseline.txt"
l5_biased_path = base_path / "output/L5 _ Java OOP _ Objects and Their Memory Locations Explained/transcript_whisper_visual_biased.txt"

import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

print("=" * 80)
print("CROSS-MODAL VERIFICATION TEST")
print("Can CMV detect the hallucinations we know exist?")
print("=" * 80)

verifier = CrossModalVerifier(fuzzy_threshold=80)

for lecture_name, visual_path, baseline_path, biased_path in [
    ("L2 - Design Class", l2_visual_path, l2_baseline_path, l2_biased_path),
    ("L5 - Memory Locations", l5_visual_path, l5_baseline_path, l5_biased_path),
]:
    print(f"\n{'='*80}")
    print(f"LECTURE: {lecture_name}")
    print("=" * 80)
    
    # Load visual keywords
    visual_data = load_json(visual_path)
    if isinstance(visual_data, list):
        visual_keywords = visual_data
    elif isinstance(visual_data, dict):
        visual_keywords = visual_data.get('keywords', visual_data.get('all_keywords', []))
    else:
        visual_keywords = []
    
    print(f"\nVisual Keywords ({len(visual_keywords)}): {visual_keywords[:15]}...")
    
    # Load transcripts
    baseline = load_text(baseline_path)
    biased = load_text(biased_path)
    
    # Verify both
    print(f"\n--- BASELINE TRANSCRIPT ---")
    baseline_result = verifier.verify(baseline, visual_keywords)
    print(f"Groundedness Score: {baseline_result['groundedness_score']*100:.1f}%")
    print(f"Hallucination Rate: {baseline_result['hallucination_rate']*100:.1f}%")
    print(f"Total terms checked: {baseline_result['total_terms']}")
    print(f"Grounded terms: {baseline_result['grounded_count']}")
    print(f"Ungrounded terms: {baseline_result['ungrounded_count']}")
    if baseline_result.get('ungrounded_terms'):
        print(f"Ungrounded (potential hallucinations): {baseline_result['ungrounded_terms'][:10]}")
    
    print(f"\n--- VISUAL-BIASED TRANSCRIPT ---")
    biased_result = verifier.verify(biased, visual_keywords)
    print(f"Groundedness Score: {biased_result['groundedness_score']*100:.1f}%")
    print(f"Hallucination Rate: {biased_result['hallucination_rate']*100:.1f}%")
    print(f"Total terms checked: {biased_result['total_terms']}")
    print(f"Grounded terms: {biased_result['grounded_count']}")
    print(f"Ungrounded terms: {biased_result['ungrounded_count']}")
    if biased_result.get('ungrounded_terms'):
        print(f"Ungrounded (potential hallucinations): {biased_result['ungrounded_terms'][:10]}")
    
    # Compare
    print(f"\n--- COMPARISON ---")
    gs_diff = biased_result['groundedness_score'] - baseline_result['groundedness_score']
    print(f"Groundedness change: {gs_diff*100:+.1f}%")
    
    if gs_diff > 0.05:
        print("✅ Visual bias IMPROVES groundedness")
    elif gs_diff < -0.05:
        print("❌ Visual bias HURTS groundedness")
    else:
        print("➖ No significant difference")

print("\n" + "=" * 80)
print("INTERPRETATION")
print("=" * 80)
print("""
CMV checks if technical terms in ASR output appear in visual context.
- High groundedness = ASR terms match what's on whiteboard
- Low groundedness = ASR may be hallucinating terms not on whiteboard

Key question: Does this correlate with actual accuracy (ground truth)?
""")
