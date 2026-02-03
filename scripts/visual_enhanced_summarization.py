#!/usr/bin/env python3
"""
=============================================================================
VISUAL-ENHANCED SUMMARIZATION - Novel Multimodal Fusion
=============================================================================
Master's Thesis - NOVELTY CONTRIBUTION

Instead of modifying ASR (which causes hallucination), we enhance the
SUMMARIZATION stage by injecting visual context.

Key Insight:
- ASR captures what was SPOKEN
- Visual analysis captures what was SHOWN (whiteboard, code, slides)
- Combining both in summarization gives COMPLETE lecture understanding

This approach:
1. Takes baseline ASR transcript (no visual bias)
2. Extracts visual keywords from whiteboard/slides
3. Enhances summary generation by:
   a) Adding visual keywords as context to the summarizer
   b) Injecting missing technical terms from visual analysis
   c) Cross-referencing spoken content with visual content

Benefits:
- No ASR hallucination risk
- Visual context adds information ASR might have missed
- Summary is more complete than either modality alone

=============================================================================
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))


def extract_key_concepts(transcript: str) -> List[str]:
    """Extract key concepts mentioned in the transcript."""
    # Technical terms patterns
    tech_patterns = [
        r'\b(class|object|method|function|variable|array|string|integer)\b',
        r'\b(public|private|static|void|main|return|import)\b',
        r'\b(inheritance|polymorphism|encapsulation|abstraction)\b',
        r'\b(constructor|instance|template|design|blueprint)\b',
        r'\b(compile|execute|run|save|create|manipulate)\b',
        r'\b(file|folder|package|module|library)\b',
        r'\b(tester|driver|code|program|output)\b',
    ]
    
    concepts = set()
    text_lower = transcript.lower()
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        concepts.update(matches)
    
    return list(concepts)


def calculate_visual_coverage(transcript: str, visual_keywords: List[str]) -> Dict:
    """
    Calculate how many visual keywords are mentioned in the transcript.
    
    Returns coverage statistics showing what visual content is missing from speech.
    """
    transcript_lower = transcript.lower()
    
    mentioned = []
    missing = []
    
    for kw in visual_keywords:
        kw_lower = kw.lower()
        # Check if keyword or any word in it appears
        words = kw_lower.split()
        found = any(word in transcript_lower for word in words if len(word) >= 3)
        
        if found:
            mentioned.append(kw)
        else:
            missing.append(kw)
    
    return {
        'total_keywords': len(visual_keywords),
        'mentioned_in_speech': mentioned,
        'missing_from_speech': missing,
        'coverage_ratio': len(mentioned) / len(visual_keywords) if visual_keywords else 0
    }


def create_enhanced_summary_prompt(
    transcript: str,
    visual_keywords: List[str],
    missing_keywords: List[str],
    video_title: str = ""
) -> str:
    """
    Create a prompt for summarization that incorporates visual context.
    
    This is where the multimodal fusion happens!
    """
    prompt = f"""You are summarizing a technical lecture video. The lecture combines spoken explanation with visual content shown on screen.

**Video Title**: {video_title if video_title else "Technical Lecture"}

**What was SPOKEN** (ASR Transcript):
{transcript}

**What was SHOWN on screen** (Visual Analysis):
Keywords visible on whiteboard/IDE: {', '.join(visual_keywords)}

**Visual content NOT mentioned in speech** (important to include):
{', '.join(missing_keywords) if missing_keywords else 'All visual content was mentioned'}

**Instructions**:
1. Create a comprehensive summary that covers BOTH spoken and visual content
2. Include technical terms from the whiteboard even if not clearly heard in speech
3. Structure the summary with clear sections
4. Highlight key programming concepts demonstrated

**Summary**:"""
    
    return prompt


def simulate_enhanced_summary(
    transcript: str,
    visual_keywords: List[str],
    missing_keywords: List[str]
) -> str:
    """
    Simulate an enhanced summary that incorporates visual context.
    
    In production, this would call an LLM. Here we demonstrate the structure.
    """
    # Extract concepts from transcript
    spoken_concepts = extract_key_concepts(transcript)
    
    # Combine with visual keywords
    all_concepts = set(spoken_concepts)
    for kw in visual_keywords:
        for word in kw.lower().split():
            if len(word) >= 3:
                all_concepts.add(word)
    
    # Create structured summary
    summary_parts = []
    
    # Opening
    summary_parts.append("## Lecture Summary\n")
    
    # Main content (from transcript)
    summary_parts.append("### Key Points Covered:\n")
    
    # Extract main topics from transcript (simplified extraction)
    sentences = re.split(r'[.!?]', transcript)
    key_sentences = [s.strip() for s in sentences if len(s.strip()) > 30][:5]
    
    for i, sent in enumerate(key_sentences, 1):
        summary_parts.append(f"{i}. {sent}\n")
    
    # Visual context section (the NOVELTY!)
    if missing_keywords:
        summary_parts.append("\n### Visual Content Shown:\n")
        summary_parts.append("The following technical elements were visible on screen:\n")
        for kw in missing_keywords[:10]:
            summary_parts.append(f"- {kw}\n")
    
    # Technical terms
    summary_parts.append("\n### Technical Concepts:\n")
    sorted_concepts = sorted(all_concepts)[:15]
    summary_parts.append(", ".join(sorted_concepts))
    
    return "".join(summary_parts)


def evaluate_summary_completeness(
    baseline_summary: str,
    enhanced_summary: str,
    ground_truth: str,
    visual_keywords: List[str]
) -> Dict:
    """
    Evaluate how complete the summaries are compared to ground truth.
    """
    gt_lower = ground_truth.lower()
    baseline_lower = baseline_summary.lower()
    enhanced_lower = enhanced_summary.lower()
    
    # Technical terms to check
    tech_terms = [
        'class', 'object', 'design', 'method', 'main', 'public', 'static',
        'void', 'java', 'file', 'tester', 'driver', 'compile', 'run',
        'template', 'blueprint', 'separate', 'code', 'string', 'system',
        'tutorial', 'execute', 'save', 'variable', 'package', 'folder'
    ]
    
    # Add visual keywords to check (they should appear in enhanced summary)
    for kw in visual_keywords:
        for word in kw.lower().split():
            if len(word) >= 4 and word not in tech_terms:
                tech_terms.append(word)
    
    # Count coverage
    def count_terms(text):
        counts = {}
        for term in tech_terms:
            counts[term] = len(re.findall(rf'\b{re.escape(term)}\b', text, re.IGNORECASE))
        return counts
    
    gt_counts = count_terms(gt_lower)
    baseline_counts = count_terms(baseline_lower)
    enhanced_counts = count_terms(enhanced_lower)
    
    # Calculate coverage metrics
    terms_in_gt = [t for t, c in gt_counts.items() if c > 0]
    
    baseline_coverage = sum(1 for t in terms_in_gt if baseline_counts.get(t, 0) > 0)
    enhanced_coverage = sum(1 for t in terms_in_gt if enhanced_counts.get(t, 0) > 0)
    
    # Check visual keyword inclusion
    visual_in_baseline = sum(1 for kw in visual_keywords 
                            if any(w in baseline_lower for w in kw.lower().split() if len(w) >= 3))
    visual_in_enhanced = sum(1 for kw in visual_keywords 
                            if any(w in enhanced_lower for w in kw.lower().split() if len(w) >= 3))
    
    return {
        'total_terms': len(terms_in_gt),
        'baseline_coverage': baseline_coverage,
        'enhanced_coverage': enhanced_coverage,
        'baseline_coverage_pct': baseline_coverage / len(terms_in_gt) if terms_in_gt else 0,
        'enhanced_coverage_pct': enhanced_coverage / len(terms_in_gt) if terms_in_gt else 0,
        'improvement': (enhanced_coverage - baseline_coverage) / len(terms_in_gt) if terms_in_gt else 0,
        'visual_keywords_total': len(visual_keywords),
        'visual_in_baseline': visual_in_baseline,
        'visual_in_enhanced': visual_in_enhanced,
        'visual_improvement': visual_in_enhanced - visual_in_baseline
    }


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    print("=" * 80)
    print("VISUAL-ENHANCED SUMMARIZATION - Novel Multimodal Fusion")
    print("=" * 80)
    
    # Load data
    gt_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    with open(gt_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    ground_truth = re.sub(r'\[\d+:\d+(?::\d+)?-\d+:\d+(?::\d+)?\]', '', ground_truth)
    ground_truth = ' '.join(ground_truth.split())
    
    baseline_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/transcript_whisper_baseline.txt"
    with open(baseline_path, 'r', encoding='utf-8') as f:
        transcript = f.read().strip()
    
    keywords_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
    with open(keywords_path, 'r', encoding='utf-8') as f:
        visual_keywords = json.load(f)
    
    print(f"\n📊 Data Loaded:")
    print(f"  Ground Truth: {len(ground_truth):,} chars")
    print(f"  Transcript: {len(transcript):,} chars")
    print(f"  Visual Keywords: {len(visual_keywords)}")
    
    # Analyze visual coverage
    print("\n" + "=" * 80)
    print("VISUAL COVERAGE ANALYSIS")
    print("=" * 80)
    
    coverage = calculate_visual_coverage(transcript, visual_keywords)
    
    print(f"\n📈 Visual Content Coverage:")
    print(f"  Total visual keywords: {coverage['total_keywords']}")
    print(f"  Mentioned in speech: {len(coverage['mentioned_in_speech'])} ({coverage['coverage_ratio']:.0%})")
    print(f"  Missing from speech: {len(coverage['missing_from_speech'])}")
    
    if coverage['missing_from_speech']:
        print(f"\n⚠ Visual content NOT mentioned verbally:")
        for kw in coverage['missing_from_speech'][:10]:
            print(f"   - {kw}")
    
    # Generate summaries
    print("\n" + "=" * 80)
    print("SUMMARY GENERATION")
    print("=" * 80)
    
    # Baseline summary (transcript only)
    baseline_summary = simulate_enhanced_summary(transcript, [], [])
    
    # Enhanced summary (transcript + visual)
    enhanced_summary = simulate_enhanced_summary(
        transcript, 
        visual_keywords, 
        coverage['missing_from_speech']
    )
    
    print(f"\n📝 Baseline Summary Length: {len(baseline_summary)} chars")
    print(f"📝 Enhanced Summary Length: {len(enhanced_summary)} chars")
    
    # Evaluate
    print("\n" + "=" * 80)
    print("EVALUATION")
    print("=" * 80)
    
    eval_results = evaluate_summary_completeness(
        baseline_summary, enhanced_summary, ground_truth, visual_keywords
    )
    
    print(f"\n{'Metric':<35} {'Baseline':>12} {'Enhanced':>12} {'Change':>12}")
    print("-" * 73)
    print(f"{'Term Coverage (vs Ground Truth)':<35} {eval_results['baseline_coverage_pct']:>11.1%} {eval_results['enhanced_coverage_pct']:>11.1%} {eval_results['improvement']:>+11.1%}")
    print(f"{'Visual Keywords Included':<35} {eval_results['visual_in_baseline']:>12} {eval_results['visual_in_enhanced']:>12} {eval_results['visual_improvement']:>+12}")
    
    # Show the benefit
    print("\n" + "=" * 80)
    print("NOVELTY DEMONSTRATION")
    print("=" * 80)
    
    print(f"""
🎯 KEY INSIGHT:
   The transcript (ASR) captured {len(coverage['mentioned_in_speech'])} of {coverage['total_keywords']} visual elements.
   
   {len(coverage['missing_from_speech'])} elements were ONLY visible on screen, not spoken:
   {', '.join(coverage['missing_from_speech'][:5])}...
   
   By fusing visual context into summarization, we capture:
   ✓ What the instructor SAID
   ✓ What was SHOWN on screen
   = MORE COMPLETE understanding
""")
    
    # Show prompt that would be used
    print("\n" + "=" * 80)
    print("LLM PROMPT FOR ENHANCED SUMMARIZATION")
    print("=" * 80)
    
    prompt = create_enhanced_summary_prompt(
        transcript[:1000] + "...",  # Truncated for display
        visual_keywords,
        coverage['missing_from_speech'],
        "L2 - Java OOP - Creating a Design Class in a Separate File"
    )
    print(prompt)
    
    # Save results
    output = {
        'approach': 'visual_enhanced_summarization',
        'coverage': coverage,
        'evaluation': eval_results,
        'enhanced_summary': enhanced_summary,
        'prompt_template': create_enhanced_summary_prompt(
            "[TRANSCRIPT]", visual_keywords, coverage['missing_from_speech'], "[TITLE]"
        )
    }
    
    output_path = base_path / "output/visual_enhanced_summary_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
