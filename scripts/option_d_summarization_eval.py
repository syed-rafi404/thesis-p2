"""
Option D: Visual-Enhanced Summarization Evaluation

This is an ALTERNATIVE research direction that doesn't depend on visual bias ASR.
The idea: Visual context helps LLM summarization, not ASR.

Hypothesis: Summaries with visual context > Summaries without visual context

This script:
1. Takes a transcript (baseline Whisper - no visual bias)
2. Takes visual context (extracted keywords from whiteboard)
3. Generates two summaries:
   - WITHOUT visual context (just transcript)
   - WITH visual context (transcript + keywords)
4. Compares them using multiple metrics

Run: python scripts/option_d_summarization_eval.py
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_transcript(lecture_folder: str) -> str:
    """Load baseline transcript (not visual-biased)."""
    transcript_path = Path(lecture_folder) / "transcript_whisper_baseline.txt"
    if transcript_path.exists():
        return transcript_path.read_text(encoding='utf-8')
    return None


def load_visual_context(lecture_folder: str) -> dict:
    """Load extracted visual keywords."""
    keywords_path = Path(lecture_folder) / "visual_keywords.json"
    if keywords_path.exists():
        with open(keywords_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_summary_without_visual(transcript: str, llm_client=None) -> str:
    """Generate summary using only transcript."""
    prompt = f"""You are a lecture note generator. Create structured notes from this transcript.

TRANSCRIPT:
{transcript[:8000]}  # Truncate for context window

Generate comprehensive lecture notes in markdown format with:
- Main topics covered
- Key concepts explained
- Important definitions
- Code examples if any
"""
    
    if llm_client:
        return llm_client.generate(prompt)
    else:
        # Mock response for testing
        return "[MOCK] Summary without visual context would go here"


def generate_summary_with_visual(transcript: str, visual_context: dict, llm_client=None) -> str:
    """Generate summary using transcript + visual context."""
    
    # Extract keywords from visual context
    keywords = []
    if visual_context:
        for frame in visual_context.get('frames', []):
            keywords.extend(frame.get('keywords', []))
        keywords = list(set(keywords))  # Deduplicate
    
    prompt = f"""You are a lecture note generator. Create structured notes from this transcript.

IMPORTANT VISUAL CONTEXT FROM WHITEBOARD:
The following terms were written on the whiteboard during the lecture:
{', '.join(keywords[:50])}

Use these visual terms to:
1. Ensure technical terms are spelled correctly
2. Identify the main topics being taught
3. Structure the notes around what the instructor wrote

TRANSCRIPT:
{transcript[:8000]}

Generate comprehensive lecture notes in markdown format with:
- Main topics covered (use whiteboard terms as headers)
- Key concepts explained
- Important definitions (ensure correct spelling from whiteboard)
- Code examples if any
"""
    
    if llm_client:
        return llm_client.generate(prompt)
    else:
        return "[MOCK] Summary with visual context would go here"


def evaluate_summaries(summary_without: str, summary_with: str, visual_keywords: list) -> dict:
    """Compare two summaries."""
    
    # Metric 1: Keyword Coverage
    # How many visual keywords appear in each summary?
    keywords_lower = [k.lower() for k in visual_keywords]
    
    without_coverage = sum(1 for k in keywords_lower if k in summary_without.lower())
    with_coverage = sum(1 for k in keywords_lower if k in summary_with.lower())
    
    # Metric 2: Length (more comprehensive?)
    without_length = len(summary_without.split())
    with_length = len(summary_with.split())
    
    # Metric 3: Structure (count markdown headers)
    without_headers = summary_without.count('#')
    with_headers = summary_with.count('#')
    
    return {
        'keyword_coverage': {
            'without_visual': without_coverage,
            'with_visual': with_coverage,
            'total_keywords': len(visual_keywords),
            'improvement': with_coverage - without_coverage
        },
        'word_count': {
            'without_visual': without_length,
            'with_visual': with_length,
            'difference': with_length - without_length
        },
        'structure': {
            'headers_without': without_headers,
            'headers_with': with_headers
        }
    }


def human_evaluation_template() -> str:
    """Generate template for human evaluation."""
    return """
## Human Evaluation Form

Rate each summary on a scale of 1-5:

### Summary A (Without Visual Context)
- Accuracy: ___/5 (Are technical terms correct?)
- Completeness: ___/5 (Are all topics covered?)
- Organization: ___/5 (Is it well structured?)
- Usefulness: ___/5 (Would this help a student?)

### Summary B (With Visual Context)
- Accuracy: ___/5
- Completeness: ___/5
- Organization: ___/5
- Usefulness: ___/5

### Overall Preference
Which summary is better overall? A / B / Same

### Comments
_________________________________
"""


def main():
    """Run Option D evaluation."""
    print("=" * 60)
    print("OPTION D: Visual-Enhanced Summarization Evaluation")
    print("=" * 60)
    
    # Find lecture folders
    output_dir = Path("output")
    lecture_folders = [
        output_dir / "L2 _ Java OOP _ Creating a Design Class in a Separate File",
        output_dir / "L3 - Java OOP - Intro to Class and Objects",
        output_dir / "L5 _ Java OOP _ Objects and Their Memory Locations Explained",
    ]
    
    results = {}
    
    for folder in lecture_folders:
        if not folder.exists():
            print(f"\n⚠️ Folder not found: {folder.name}")
            continue
            
        print(f"\n📁 Processing: {folder.name}")
        
        # Load data
        transcript = load_transcript(folder)
        visual_context = load_visual_context(folder)
        
        if not transcript:
            print("  ❌ No baseline transcript found")
            continue
            
        if not visual_context:
            print("  ❌ No visual context found")
            continue
        
        # Extract keywords
        keywords = []
        for frame in visual_context.get('frames', []):
            keywords.extend(frame.get('keywords', []))
        keywords = list(set(keywords))
        
        print(f"  ✅ Transcript: {len(transcript)} chars")
        print(f"  ✅ Visual keywords: {len(keywords)}")
        
        # For actual evaluation, you would:
        # 1. Generate summaries with real LLM
        # 2. Have humans rate them
        # 3. Compare metrics
        
        # For now, show what would be compared
        results[folder.name] = {
            'transcript_length': len(transcript),
            'visual_keywords': len(keywords),
            'sample_keywords': keywords[:10],
            'ready_for_evaluation': True
        }
    
    # Print summary
    print("\n" + "=" * 60)
    print("OPTION D READINESS CHECK")
    print("=" * 60)
    
    for name, data in results.items():
        print(f"\n📊 {name}")
        print(f"   Transcript: {data['transcript_length']} chars")
        print(f"   Keywords: {data['visual_keywords']}")
        print(f"   Sample: {', '.join(data['sample_keywords'])}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS FOR OPTION D")
    print("=" * 60)
    print("""
1. Generate summaries with real LLM (Qwen2.5-7B):
   - Run: python scripts/generate_summaries_comparison.py
   
2. Human evaluation (need 3-5 evaluators):
   - Show both summaries (blind, randomized A/B)
   - Use rating form above
   - Calculate inter-annotator agreement
   
3. Automatic metrics:
   - ROUGE score (if reference summary exists)
   - Keyword coverage improvement
   - BERTScore for semantic similarity
   
4. Claim to make:
   "Visual context improves LLM summarization by X% keyword coverage
    and Y preference rate in human evaluation"
""")
    
    # Save results
    output_path = Path("output/option_d_readiness.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📄 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
