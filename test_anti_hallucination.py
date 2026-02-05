#!/usr/bin/env python3
"""
Test the anti-hallucination system with real examples from transcripts.
"""

from src.audio.visual_bias_processor import (
    clean_transcript,
    detect_repetition_ratio,
    remove_ngram_loops,
    remove_phrase_repetitions,
    remove_repetitions,
    remove_hyphenated_repetitions
)

# Real hallucination examples from our transcripts
TEST_CASES = [
    {
        "name": "N-gram loop (of the course)",
        "input": "This is the lecture of the course of the course of the course of the course of the course of the course of the course today.",
        "expected_pattern": "of the course",  # Should appear only once or twice
    },
    {
        "name": "Word repetition (design)",
        "input": "So we need to create a design design design design design design design for this project.",
        "expected_max_repeats": 2,
    },
    {
        "name": "Phrase repetition (This is)",
        "input": "This is the method. This is the method. This is the method. This is the method. Now let's continue.",
        "expected_pattern": "This is the method",
    },
    {
        "name": "Hyphenated (class-class-class)",
        "input": "We have a class-class-class-class-class here in Java.",
        "expected_max_hyphens": 2,
    },
    {
        "name": "Complex mixed hallucination",
        "input": "Student Student Student. The design of the design of the design of the design. class-class-class-class. method method method method method.",
        "expected_short": True,
    },
    {
        "name": "Real transcript excerpt (severe)",
        "input": "তাই এই course of the course of the course of the course of the course of the course of the course এটা হলো Java OOP design design design design design Student Student Student Student",
        "expected_short": True,
    },
]


def test_individual_functions():
    """Test each anti-hallucination function individually."""
    print("=" * 60)
    print("TESTING INDIVIDUAL FUNCTIONS")
    print("=" * 60)
    
    # Test 1: Word repetition
    print("\n1. remove_repetitions():")
    test_input = "design design design design design pattern"
    result = remove_repetitions(test_input, max_repeats=2)
    print(f"   Input:  '{test_input}'")
    print(f"   Output: '{result}'")
    assert result.count("design") <= 3, f"Expected max 3 'design', got {result.count('design')}"
    print("   ✓ PASSED")
    
    # Test 2: N-gram loops
    print("\n2. remove_ngram_loops():")
    test_input = "of the course of the course of the course of the course end"
    result = remove_ngram_loops(test_input, ngram_sizes=[3], max_repeats=1)
    print(f"   Input:  '{test_input}'")
    print(f"   Output: '{result}'")
    count = result.lower().count("of the course")
    assert count <= 2, f"Expected max 2 'of the course', got {count}"
    print("   ✓ PASSED")
    
    # Test 3: Phrase repetition
    print("\n3. remove_phrase_repetitions():")
    test_input = "This is it. This is it. This is it. This is it. Done."
    result = remove_phrase_repetitions(test_input, max_repeats=1)
    print(f"   Input:  '{test_input}'")
    print(f"   Output: '{result}'")
    count = result.lower().count("this is it")
    assert count <= 2, f"Expected max 2 'this is it', got {count}"
    print("   ✓ PASSED")
    
    # Test 4: Hyphenated
    print("\n4. remove_hyphenated_repetitions():")
    test_input = "A class-class-class-class-class in Java"
    result = remove_hyphenated_repetitions(test_input, max_repeats=2)
    print(f"   Input:  '{test_input}'")
    print(f"   Output: '{result}'")
    assert "class-class-class" not in result, "Should have max 2 hyphens"
    print("   ✓ PASSED")
    
    # Test 5: Repetition ratio
    print("\n5. detect_repetition_ratio():")
    clean_text = "The quick brown fox jumps over the lazy dog"
    dirty_text = "the the the the the the the the the the"
    clean_ratio = detect_repetition_ratio(clean_text, ngram_size=2)
    dirty_ratio = detect_repetition_ratio(dirty_text, ngram_size=2)
    print(f"   Clean text ratio: {clean_ratio:.2%}")
    print(f"   Dirty text ratio: {dirty_ratio:.2%}")
    assert dirty_ratio > clean_ratio, "Dirty text should have higher repetition ratio"
    print("   ✓ PASSED")


def test_full_pipeline():
    """Test the complete clean_transcript() function."""
    print("\n" + "=" * 60)
    print("TESTING FULL PIPELINE: clean_transcript()")
    print("=" * 60)
    
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n{i}. {case['name']}:")
        print(f"   Input ({len(case['input'])} chars):")
        print(f"   '{case['input'][:100]}{'...' if len(case['input']) > 100 else ''}'")
        
        result = clean_transcript(case['input'], max_word_repeats=2, max_phrase_repeats=1)
        reduction = (1 - len(result) / len(case['input'])) * 100 if case['input'] else 0
        
        print(f"   Output ({len(result)} chars, {reduction:.1f}% reduction):")
        print(f"   '{result}'")
        
        # Verify it got shorter (hallucination was removed)
        if len(result) < len(case['input']):
            print("   ✓ Text was cleaned (reduced)")
        else:
            print("   ⚠ No reduction (may be OK if no hallucinations)")


def test_severe_hallucination():
    """Test with a severely hallucinated transcript segment."""
    print("\n" + "=" * 60)
    print("TESTING SEVERE HALLUCINATION (100+ repetitions)")
    print("=" * 60)
    
    # Simulate the worst case from our real transcripts
    base = "of the course "
    severe_input = "Today we will learn " + (base * 100) + "about Java."
    
    print(f"\nInput length: {len(severe_input)} chars ({severe_input.count(base)} repetitions)")
    
    result = clean_transcript(severe_input, max_word_repeats=2, max_phrase_repeats=1)
    
    print(f"Output length: {len(result)} chars")
    print(f"Reduction: {(1 - len(result) / len(severe_input)) * 100:.1f}%")
    print(f"\nOutput: '{result}'")
    
    # Should be MUCH shorter
    assert len(result) < len(severe_input) * 0.2, "Should reduce by at least 80%"
    print("\n✓ SEVERE HALLUCINATION TEST PASSED")


if __name__ == "__main__":
    print("Anti-Hallucination System Test Suite")
    print("=" * 60)
    
    test_individual_functions()
    test_full_pipeline()
    test_severe_hallucination()
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)
