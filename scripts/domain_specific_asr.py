#!/usr/bin/env python3
"""
=============================================================================
DOMAIN-SPECIFIC ASR ENHANCEMENT - Technical Vocabulary Injection
=============================================================================
Master's Thesis - NOVELTY CONTRIBUTION

This approach improves ASR by providing a domain-specific vocabulary
in the initial prompt, NOT by biasing logits (which causes hallucination).

Key Insight:
- Whisper uses initial prompts to guide transcription style
- Including technical vocabulary in the prompt improves recognition
- This is SAFE because it only guides, doesn't force tokens

The approach:
1. Extract technical terms from video title and description
2. Add visual keywords as "vocabulary hints" in the prompt
3. Let Whisper naturally recognize these terms better

This is different from logits bias because:
- Prompt conditioning happens BEFORE generation
- No token forcing during generation
- Natural language guidance, not probability manipulation

=============================================================================
"""

import re
import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import librosa
from thefuzz import fuzz


def extract_domain_vocabulary(visual_keywords: List[str], video_title: str = "") -> List[str]:
    """
    Extract and filter domain-specific vocabulary.
    
    Filter out:
    - UI noise (paths, filenames)
    - Common words
    - Too short terms
    
    Keep:
    - Technical programming terms
    - Concepts from the video title
    """
    # Known technical terms to prioritize
    TECH_TERMS = {
        'class', 'object', 'method', 'function', 'variable', 'array',
        'string', 'integer', 'boolean', 'public', 'private', 'static',
        'void', 'return', 'import', 'java', 'python', 'code', 
        'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
        'constructor', 'instance', 'template', 'design', 'blueprint',
        'tester', 'driver', 'compile', 'execute', 'run', 'save',
        'package', 'module', 'interface', 'abstract', 'override',
        'oop', 'ide', 'jvm', 'jdk', 'api', 'sdk',
    }
    
    # Noise patterns to filter
    NOISE_PATTERNS = [
        r'^[A-Z]:\\',  # Windows paths
        r'^/Users/',   # Unix paths
        r'\.java$',    # File extensions
        r'\.py$',
        r'^jdk\d',     # JDK versions
        r'^Users$',
        r'^Desktop$',
        r'^Documents$',
        r'^Program Files$',
    ]
    
    filtered = []
    seen = set()
    
    # Add title words
    title_words = re.findall(r'\b\w{3,}\b', video_title)
    for word in title_words:
        word_lower = word.lower()
        if word_lower not in seen and len(word) >= 3:
            if word_lower in TECH_TERMS or word[0].isupper():
                filtered.append(word)
                seen.add(word_lower)
    
    # Process visual keywords
    for kw in visual_keywords:
        kw_clean = kw.strip()
        
        # Skip noise patterns
        is_noise = any(re.search(pattern, kw_clean, re.IGNORECASE) for pattern in NOISE_PATTERNS)
        if is_noise:
            continue
        
        # Skip too short
        if len(kw_clean) < 3:
            continue
        
        # Skip if already seen
        if kw_clean.lower() in seen:
            continue
        
        # Check if it's a technical term or proper noun
        if kw_clean.lower() in TECH_TERMS or kw_clean[0].isupper():
            filtered.append(kw_clean)
            seen.add(kw_clean.lower())
    
    return filtered


def create_domain_prompt(vocabulary: List[str], language: str = "bengali") -> str:
    """
    Create an initial prompt that includes domain vocabulary.
    
    The prompt guides Whisper to recognize these terms correctly.
    Keep it SHORT to avoid token limit issues.
    """
    # Only include top 8 most important terms
    top_terms = vocabulary[:8]
    vocab_str = ", ".join(top_terms)
    
    if language == "bengali":
        # Very short prompt to stay within limits
        prompt = f"Banglish lecture. Terms: {vocab_str}."
    else:
        prompt = f"Programming lecture. Terms: {vocab_str}."
    
    return prompt


def transcribe_with_domain_prompt(
    model,
    processor,
    audio_array,
    sample_rate: int,
    vocabulary: List[str],
    language: str = "bengali"
) -> str:
    """
    Transcribe audio with domain-specific prompt.
    """
    device = next(model.parameters()).device
    
    # Create domain-specific prompt
    initial_prompt = create_domain_prompt(vocabulary, language)
    prompt_ids = processor.get_prompt_ids(initial_prompt, return_tensors="pt").to(device)
    
    # Prepare audio
    inputs = processor(
        audio_array,
        sampling_rate=sample_rate,
        return_tensors="pt"
    )
    input_features = inputs.input_features.to(device)
    
    # Match model dtype
    if next(model.parameters()).dtype == torch.float16:
        input_features = input_features.half()
    
    # Generate with domain prompt
    generate_kwargs = {
        "language": language,
        "task": "transcribe",
        "max_new_tokens": 380,  # Reduced to leave room for prompt
        "prompt_ids": prompt_ids,
        # Anti-hallucination settings
        "condition_on_prev_tokens": False,
        "temperature": 0.0,
        "compression_ratio_threshold": 1.8,
        "logprob_threshold": -0.8,
    }
    
    with torch.no_grad():
        output_ids = model.generate(input_features, **generate_kwargs)
    
    transcript = processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    
    return transcript


def transcribe_baseline(
    model,
    processor,
    audio_array,
    sample_rate: int,
    language: str = "bengali"
) -> str:
    """
    Transcribe audio with generic prompt (baseline).
    """
    device = next(model.parameters()).device
    
    # Generic prompt (no domain vocabulary)
    initial_prompt = "This is a lecture."
    prompt_ids = processor.get_prompt_ids(initial_prompt, return_tensors="pt").to(device)
    
    # Prepare audio
    inputs = processor(
        audio_array,
        sampling_rate=sample_rate,
        return_tensors="pt"
    )
    input_features = inputs.input_features.to(device)
    
    if next(model.parameters()).dtype == torch.float16:
        input_features = input_features.half()
    
    generate_kwargs = {
        "language": language,
        "task": "transcribe",
        "max_new_tokens": 430,
        "prompt_ids": prompt_ids,
        "condition_on_prev_tokens": False,
        "temperature": 0.0,
        "compression_ratio_threshold": 1.8,
        "logprob_threshold": -0.8,
    }
    
    with torch.no_grad():
        output_ids = model.generate(input_features, **generate_kwargs)
    
    return processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()


def evaluate_transcripts(
    baseline: str,
    enhanced: str,
    ground_truth: str,
    vocabulary: List[str]
) -> Dict:
    """Evaluate both transcripts against ground truth."""
    
    gt_lower = ground_truth.lower()
    base_lower = baseline.lower()
    enh_lower = enhanced.lower()
    
    # Check vocabulary term recognition
    def count_vocab_matches(text, vocab):
        count = 0
        for term in vocab:
            term_lower = term.lower()
            if term_lower in text.lower():
                count += 1
        return count
    
    base_vocab = count_vocab_matches(baseline, vocabulary)
    enh_vocab = count_vocab_matches(enhanced, vocabulary)
    
    # Technical terms
    tech_terms = ['class', 'object', 'design', 'method', 'main', 'public', 'static',
                  'void', 'java', 'file', 'tester', 'driver', 'compile', 'run',
                  'template', 'blueprint', 'separate', 'code', 'tutorial']
    
    def count_tech_terms(text):
        return sum(len(re.findall(rf'\b{t}\b', text.lower())) for t in tech_terms)
    
    base_tech = count_tech_terms(baseline)
    enh_tech = count_tech_terms(enhanced)
    gt_tech = count_tech_terms(ground_truth)
    
    # Similarity
    base_sim = fuzz.ratio(gt_lower[:5000], base_lower[:5000])
    enh_sim = fuzz.ratio(gt_lower[:5000], enh_lower[:5000])
    
    return {
        'vocabulary_terms_total': len(vocabulary),
        'baseline_vocab_matched': base_vocab,
        'enhanced_vocab_matched': enh_vocab,
        'vocab_improvement': enh_vocab - base_vocab,
        'baseline_tech_terms': base_tech,
        'enhanced_tech_terms': enh_tech,
        'ground_truth_tech_terms': gt_tech,
        'tech_improvement': enh_tech - base_tech,
        'baseline_similarity': base_sim,
        'enhanced_similarity': enh_sim,
        'similarity_improvement': enh_sim - base_sim
    }


def load_audio_from_video(video_path: Path) -> Tuple:
    """Extract audio from video file."""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path),
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            tmp_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        audio_array, sample_rate = librosa.load(tmp_path, sr=16000, mono=True)
        return audio_array, sample_rate
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    print("=" * 80)
    print("DOMAIN-SPECIFIC ASR ENHANCEMENT")
    print("Using Visual Keywords as Vocabulary Hints in Initial Prompt")
    print("=" * 80)
    
    # Load data
    gt_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    with open(gt_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    ground_truth = re.sub(r'\[\d+:\d+(?::\d+)?-\d+:\d+(?::\d+)?\]', '', ground_truth)
    ground_truth = ' '.join(ground_truth.split())
    
    keywords_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
    with open(keywords_path, 'r', encoding='utf-8') as f:
        visual_keywords = json.load(f)
    
    video_title = "L2 - Java OOP - Creating a Design Class in a Separate File"
    
    # Extract domain vocabulary
    print(f"\n📚 Original Visual Keywords: {visual_keywords}")
    
    vocabulary = extract_domain_vocabulary(visual_keywords, video_title)
    print(f"\n🎯 Filtered Domain Vocabulary: {vocabulary}")
    
    # Show the prompts
    print("\n" + "=" * 80)
    print("PROMPT COMPARISON")
    print("=" * 80)
    
    print("\n[BASELINE PROMPT]")
    print("This is a lecture.")
    
    print("\n[DOMAIN-ENHANCED PROMPT]")
    print(create_domain_prompt(vocabulary, "bengali"))
    
    # Load model
    print("\n" + "=" * 80)
    print("LOADING MODEL & AUDIO")
    print("=" * 80)
    
    model_id = "openai/whisper-large-v3-turbo"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"\n🔧 Loading {model_id}...")
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True,
    ).to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    
    # Load audio
    video_path = base_path / "data/raw/L2 _ Java OOP _ Creating a Design Class in a Separate File.mp4"
    print(f"\n🎵 Extracting audio from: {video_path.name}")
    audio_array, sample_rate = load_audio_from_video(video_path)
    
    # Use first 60 seconds for testing
    max_seconds = 60
    max_samples = int(max_seconds * sample_rate)
    if len(audio_array) > max_samples:
        audio_array = audio_array[:max_samples]
    print(f"   Using first {max_seconds} seconds for testing")
    
    # Transcribe
    print("\n" + "=" * 80)
    print("TRANSCRIPTION COMPARISON")
    print("=" * 80)
    
    print("\n🔄 Transcribing with BASELINE prompt...")
    baseline = transcribe_baseline(model, processor, audio_array, sample_rate, "bengali")
    print(f"   Length: {len(baseline)} chars")
    
    print("\n🔄 Transcribing with DOMAIN-ENHANCED prompt...")
    enhanced = transcribe_with_domain_prompt(model, processor, audio_array, sample_rate, vocabulary, "bengali")
    print(f"   Length: {len(enhanced)} chars")
    
    # Evaluate
    print("\n" + "=" * 80)
    print("EVALUATION")
    print("=" * 80)
    
    results = evaluate_transcripts(baseline, enhanced, ground_truth, vocabulary)
    
    print(f"\n{'Metric':<30} {'Baseline':>12} {'Enhanced':>12} {'Change':>12}")
    print("-" * 68)
    print(f"{'Vocabulary Terms Found':<30} {results['baseline_vocab_matched']:>12} {results['enhanced_vocab_matched']:>12} {results['vocab_improvement']:>+12}")
    print(f"{'Technical Terms Count':<30} {results['baseline_tech_terms']:>12} {results['enhanced_tech_terms']:>12} {results['tech_improvement']:>+12}")
    print(f"{'Fuzzy Similarity':<30} {results['baseline_similarity']:>11}% {results['enhanced_similarity']:>11}% {results['similarity_improvement']:>+11}%")
    
    # Verdict
    print("\n" + "=" * 80)
    print("RESULT")
    print("=" * 80)
    
    total_improvement = (
        results['vocab_improvement'] + 
        results['tech_improvement'] + 
        results['similarity_improvement']
    )
    
    if total_improvement > 0:
        print(f"\n✅ SUCCESS! Domain-specific prompting improved transcription:")
        print(f"   +{results['vocab_improvement']} vocabulary terms recognized")
        print(f"   +{results['tech_improvement']} technical terms found")
        print(f"   +{results['similarity_improvement']}% similarity improvement")
    else:
        print(f"\n➖ No significant improvement with domain prompting")
    
    # Show transcripts
    print("\n" + "=" * 80)
    print("TRANSCRIPT SAMPLES (first 400 chars)")
    print("=" * 80)
    
    print(f"\n[BASELINE]")
    print(baseline[:400])
    
    print(f"\n[DOMAIN-ENHANCED]")
    print(enhanced[:400])
    
    # Save
    output = {
        'approach': 'domain_specific_prompt',
        'vocabulary': vocabulary,
        'baseline_transcript': baseline,
        'enhanced_transcript': enhanced,
        'evaluation': results
    }
    
    output_path = base_path / "output/domain_prompt_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_path}")


if __name__ == "__main__":
    main()
