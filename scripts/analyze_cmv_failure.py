#!/usr/bin/env python3
"""
=============================================================================
ANALYSIS: Why CMV gives opposite results to ground truth evaluation
=============================================================================
CMV says visual bias HELPS (+17.5% groundedness)
Ground truth says visual bias HURTS (-9.3% term recall)

WHY? Let's find out.
=============================================================================
"""

import re
import sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.evaluation.cross_modal_verifier import CrossModalVerifier

base_path = Path("c:/Users/T2520785/thesisP2")

# Load L2 data
l2_biased = open(base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt").read()
l2_gt = open(base_path / "data/ground_truth/L2_ground_truth.txt").read()

print("=" * 80)
print("WHY CMV AND GROUND TRUTH DISAGREE")
print("=" * 80)

# The biased transcript has "Compile" repeated 138 times
compile_count_biased = l2_biased.lower().count('compile')
compile_count_gt = l2_gt.lower().count('compile')

print(f"\n'compile' appears in:")
print(f"  Visual-Biased ASR: {compile_count_biased} times")
print(f"  Ground Truth:      {compile_count_gt} times")

# Visual keywords include "Compiler"
import json
l2_visual = json.load(open(base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"))
print(f"\nVisual keywords: {l2_visual}")

print("""
EXPLANATION:
============

The visual keywords include "Compiler" (seen on screen).

1. CMV checks: Does "compile" match any visual keyword?
   → Yes! "compile" ≈ "Compiler" (fuzzy match ~85%)
   → CMV says: This is GROUNDED ✓

2. Ground truth says: "compile" should appear 9 times, not 138 times.
   → 138 is HALLUCINATION, even if the word is "grounded"

PROBLEM: CMV doesn't check QUANTITY, only PRESENCE.

If "Compiler" is on the whiteboard, saying "compile compile compile..." 
138 times is counted as 138 "grounded" terms, not 129 hallucinations.
""")

# Let's verify this
verifier = CrossModalVerifier(fuzzy_threshold=80)

# Count how many technical terms are detected
print("\n" + "=" * 80)
print("TECHNICAL TERM EXTRACTION FROM BIASED TRANSCRIPT")
print("=" * 80)

# Manually extract terms the same way CMV does
terms = verifier._extract_technical_terms(l2_biased)
print(f"\nExtracted {len(terms)} technical terms:")
term_counts = Counter(t.lower() for t in terms)
print(f"Top 10: {dict(term_counts.most_common(10))}")

# Now check if CMV sees "Compile" as grounded
compile_grounded, score, match = verifier._is_grounded("Compile", l2_visual)
print(f"\nIs 'Compile' grounded? {compile_grounded} (score: {score}, matched: '{match}')")

print("""
CONCLUSION:
===========

CMV has a fundamental flaw for detecting REPETITION-based hallucinations:
- It checks if terms EXIST in visual context (✓)
- It does NOT check if terms are OVER-represented (✗)

When visual bias causes "compile" to repeat 138x:
- CMV says: "Great! 'compile' matches 'Compiler' on whiteboard"
- Reality: This is a SEVERE hallucination

POTENTIAL FIX:
We could enhance CMV to:
1. Check term FREQUENCY vs expected frequency
2. Flag when a term appears >10x more than average
3. Combine with anti-hallucination filtering

This could be a GENUINE CONTRIBUTION:
"Frequency-Aware Cross-Modal Verification for ASR Hallucination Detection"
""")
