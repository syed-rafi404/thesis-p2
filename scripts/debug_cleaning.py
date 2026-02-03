#!/usr/bin/env python3
"""
Quick check: What exactly is clean_transcript removing?
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.visual_bias_processor import clean_transcript

base_path = Path("c:/Users/T2520785/thesisP2")

# Load biased L2 (has the compile hallucination)
biased_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_visual_biased.txt"

with open(biased_path, 'r', encoding='utf-8') as f:
    raw = f.read()

cleaned = clean_transcript(raw)

print("=" * 80)
print("BEFORE CLEANING (first 1000 chars):")
print("=" * 80)
print(raw[:1000])
print("\n...")

print("\n" + "=" * 80)
print("AFTER CLEANING (first 1000 chars):")
print("=" * 80)
print(cleaned[:1000])
print("\n...")

print("\n" + "=" * 80)
print("STATS:")
print("=" * 80)
print(f"Raw length:     {len(raw):,} chars")
print(f"Cleaned length: {len(cleaned):,} chars")
print(f"Removed:        {len(raw) - len(cleaned):,} chars ({(len(raw)-len(cleaned))/len(raw)*100:.1f}%)")

# Count 'compile' specifically
compile_raw = raw.lower().count('compile')
compile_cleaned = cleaned.lower().count('compile')
print(f"\n'compile' occurrences:")
print(f"  Before: {compile_raw}")
print(f"  After:  {compile_cleaned}")
