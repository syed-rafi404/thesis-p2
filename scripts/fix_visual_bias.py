#!/usr/bin/env python3
"""
=============================================================================
VISUAL BIAS FIX STRATEGY - Three-Pronged Approach
=============================================================================
Based on ground truth evaluation showing visual bias HURTS performance:
- Term Recall: 54.4% baseline → 41.7% biased (-12.7%)
- Hallucination: "compile" repeated 138x instead of 9x

This script implements three strategies to fix the visual bias issue:

STRATEGY 1: REDUCED BIAS VALUE
- Lower bias from 2.0 to very low values (0.3-0.5)
- Enough to nudge, not enough to force

STRATEGY 2: ADAPTIVE DECAY
- Use AdaptiveVisualBiasProcessor with strong decay
- After a keyword is used once, reduce its bias dramatically

STRATEGY 3: KEYWORD FILTERING
- Filter out problematic keywords that match common spoken words
- Only keep rare/unique technical terms

Test each strategy using direct transcription to avoid chunking issues.
=============================================================================
"""

import sys
import os
import json
import wave
import time
from pathlib import Path
from collections import Counter

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, LogitsProcessorList
from thefuzz import fuzz


def load_audio_from_video(video_path: Path) -> tuple:
    """Extract audio from video and return numpy array and sample rate."""
    import subprocess
    import tempfile
    import librosa
    
    # Use ffmpeg to extract audio to a temp WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Extract audio at 16kHz mono (Whisper's expected format)
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path),
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            tmp_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        
        # Load with librosa (handles resampling if needed)
        audio_array, sample_rate = librosa.load(tmp_path, sr=16000, mono=True)
        
        return audio_array, sample_rate
        
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_tokens_for_words(tokenizer, words_list):
    """Get token IDs for words with variations."""
    all_token_ids = set()
    
    for word in words_list:
        variations = [
            word,
            word.lower(),
            word.upper(),
            word.capitalize(),
            f" {word}",
            f" {word.lower()}",
            f" {word.capitalize()}",
        ]
        
        for variant in variations:
            encoded = tokenizer.encode(variant, add_special_tokens=False)
            all_token_ids.update(encoded)
    
    return list(all_token_ids)


class StandardBiasProcessor:
    """Standard bias that adds constant value to token logits."""
    
    def __init__(self, bias_token_ids, bias_value=2.0):
        self.bias_token_ids = set(bias_token_ids)
        self.bias_value = bias_value
        self._bias_tensor = None
        
    def __call__(self, input_ids, scores):
        if self._bias_tensor is None:
            vocab_size = scores.shape[-1]
            self._bias_tensor = torch.zeros(vocab_size, device=scores.device, dtype=scores.dtype)
            for tid in self.bias_token_ids:
                if 0 <= tid < vocab_size:
                    self._bias_tensor[tid] = self.bias_value
        
        if self._bias_tensor.device != scores.device:
            self._bias_tensor = self._bias_tensor.to(scores.device)
            
        return scores + self._bias_tensor


class AdaptiveDecayBiasProcessor:
    """
    Strategy 2: Adaptive bias that decays after each use.
    
    After a keyword token is generated, reduce its future bias.
    This prevents runaway repetition.
    """
    
    def __init__(self, bias_token_ids, initial_bias=1.5, decay_factor=0.3, min_bias=0.1):
        self.bias_token_ids = set(bias_token_ids)
        self.initial_bias = initial_bias
        self.decay_factor = decay_factor
        self.min_bias = min_bias
        
        # Track current bias per token
        self.current_bias = {tid: initial_bias for tid in bias_token_ids}
        
        self._bias_tensor = None
        self._vocab_size = None
        
    def __call__(self, input_ids, scores):
        vocab_size = scores.shape[-1]
        
        # Check if any bias tokens were just generated (last token)
        if input_ids.shape[1] > 0:
            last_tokens = input_ids[:, -1].tolist()
            for last_token in last_tokens:
                if last_token in self.current_bias:
                    # Decay this token's bias
                    new_bias = self.current_bias[last_token] * self.decay_factor
                    self.current_bias[last_token] = max(new_bias, self.min_bias)
        
        # Build bias tensor with current values
        bias_tensor = torch.zeros(vocab_size, device=scores.device, dtype=scores.dtype)
        for tid, bias in self.current_bias.items():
            if 0 <= tid < vocab_size:
                bias_tensor[tid] = bias
        
        return scores + bias_tensor
    
    def reset(self):
        """Reset all biases to initial values."""
        self.current_bias = {tid: self.initial_bias for tid in self.bias_token_ids}


def filter_keywords_strict(keywords: list, common_words: set = None) -> list:
    """
    Strategy 3: Filter keywords aggressively.
    
    Remove keywords that:
    - Are too short (< 4 chars)
    - Match common spoken words
    - Are path components (Users, Desktop, etc.)
    """
    if common_words is None:
        common_words = {
            # Common words that cause hallucination
            'compile', 'compiler', 'compilation', 'compiled',
            'program', 'programs', 'programming',
            'file', 'files',
            'code', 'coding',
            'the', 'is', 'are', 'was', 'were',
            'this', 'that', 'these', 'those',
            'a', 'an',
            'and', 'or', 'but', 'if',
            'to', 'for', 'of', 'in', 'on', 'at',
            'it', 'its',
            'we', 'you', 'they', 'he', 'she',
            'will', 'would', 'could', 'should',
            'have', 'has', 'had',
            'do', 'does', 'did',
            'be', 'been', 'being',
            # Path/UI words
            'users', 'desktop', 'documents',
            'editing', 'working',
            # Generic words
            'welcome', 'hello', 'hi',
        }
    
    filtered = []
    for kw in keywords:
        kw_lower = kw.lower()
        
        # Skip too short
        if len(kw) < 4:
            continue
            
        # Skip common words
        if kw_lower in common_words:
            continue
            
        # Keep unique/technical terms
        filtered.append(kw)
    
    return filtered


def transcribe_with_strategy(
    model, processor, audio_array, sample_rate,
    strategy: str,
    keywords: list = None,
    bias_value: float = 2.0,
    language: str = "en"
) -> tuple:
    """
    Transcribe audio with a specific bias strategy.
    
    Returns: (transcript, stats)
    """
    device = next(model.parameters()).device
    
    # Prepare audio features
    inputs = processor(
        audio_array,
        sampling_rate=sample_rate,
        return_tensors="pt"
    )
    input_features = inputs.input_features.to(device)
    
    # Match model dtype
    if hasattr(model, 'dtype'):
        input_features = input_features.to(model.dtype)
    elif next(model.parameters()).dtype == torch.float16:
        input_features = input_features.half()
    
    logits_processor = None
    filtered_keywords = keywords or []
    
    if strategy == "baseline":
        # No bias
        pass
        
    elif strategy == "standard_low":
        # Strategy 1: Very low bias (0.3)
        if keywords:
            token_ids = get_tokens_for_words(processor.tokenizer, keywords)
            logits_processor = LogitsProcessorList([
                StandardBiasProcessor(token_ids, bias_value=0.3)
            ])
            
    elif strategy == "standard_medium":
        # Standard bias but lower (0.75)
        if keywords:
            token_ids = get_tokens_for_words(processor.tokenizer, keywords)
            logits_processor = LogitsProcessorList([
                StandardBiasProcessor(token_ids, bias_value=0.75)
            ])
            
    elif strategy == "adaptive_decay":
        # Strategy 2: Adaptive decay
        if keywords:
            token_ids = get_tokens_for_words(processor.tokenizer, keywords)
            processor_obj = AdaptiveDecayBiasProcessor(
                token_ids, 
                initial_bias=1.5, 
                decay_factor=0.3, 
                min_bias=0.1
            )
            logits_processor = LogitsProcessorList([processor_obj])
            
    elif strategy == "filtered_keywords":
        # Strategy 3: Filtered keywords with standard bias
        if keywords:
            filtered_keywords = filter_keywords_strict(keywords)
            if filtered_keywords:
                token_ids = get_tokens_for_words(processor.tokenizer, filtered_keywords)
                logits_processor = LogitsProcessorList([
                    StandardBiasProcessor(token_ids, bias_value=1.5)
                ])
                
    elif strategy == "combined":
        # All three strategies combined
        if keywords:
            filtered_keywords = filter_keywords_strict(keywords)
            if filtered_keywords:
                token_ids = get_tokens_for_words(processor.tokenizer, filtered_keywords)
                processor_obj = AdaptiveDecayBiasProcessor(
                    token_ids,
                    initial_bias=0.75,  # Lower initial
                    decay_factor=0.2,   # Strong decay
                    min_bias=0.05
                )
                logits_processor = LogitsProcessorList([processor_obj])
    
    # Generate
    generate_kwargs = {
        "language": language,
        "task": "transcribe",
        "max_new_tokens": 440,  # Reduced to fit within 448 limit with start tokens
    }
    
    if logits_processor:
        generate_kwargs["logits_processor"] = logits_processor
    
    with torch.no_grad():
        output_ids = model.generate(input_features, **generate_kwargs)
    
    transcript = processor.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
    
    stats = {
        "strategy": strategy,
        "keywords_used": len(filtered_keywords) if strategy in ["filtered_keywords", "combined"] else len(keywords or []),
        "filtered_keywords": filtered_keywords if strategy in ["filtered_keywords", "combined"] else keywords,
        "transcript_length": len(transcript),
    }
    
    return transcript, stats


def evaluate_transcript(transcript: str, ground_truth: str, keywords: list) -> dict:
    """Evaluate a transcript against ground truth."""
    
    # Term recall for technical terms
    tech_terms = ['class', 'object', 'design', 'method', 'main', 'public', 'static',
                  'void', 'java', 'file', 'tester', 'driver', 'compile', 'run',
                  'template', 'blueprint', 'separate', 'code', 'string', 'system']
    
    gt_lower = ground_truth.lower()
    tr_lower = transcript.lower()
    
    gt_counts = {t: len(list(re.finditer(rf'\b{t}\b', gt_lower))) for t in tech_terms}
    tr_counts = {t: len(list(re.finditer(rf'\b{t}\b', tr_lower))) for t in tech_terms}
    
    # Recall = correctly found / total in ground truth
    total_gt = sum(gt_counts.values())
    found = sum(min(tr_counts.get(t, 0), gt_counts[t]) for t in gt_counts if gt_counts[t] > 0)
    recall = found / total_gt if total_gt > 0 else 0
    
    # Hallucination detection - terms appearing more than 3x their ground truth count
    hallucinated = 0
    for term in tech_terms:
        if gt_counts[term] > 0 and tr_counts[term] > gt_counts[term] * 3:
            hallucinated += tr_counts[term] - gt_counts[term]
    
    # Similarity
    similarity = fuzz.ratio(gt_lower[:5000], tr_lower[:5000])
    
    # Word count and unique words
    words = transcript.split()
    unique_words = len(set(w.lower() for w in words))
    
    return {
        "term_recall": recall,
        "similarity": similarity,
        "hallucinated_count": hallucinated,
        "word_count": len(words),
        "unique_words": unique_words,
        "diversity": unique_words / len(words) if words else 0
    }


import re

def main():
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Load ground truth
    gt_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    with open(gt_path, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    ground_truth = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', ground_truth)
    ground_truth = ' '.join(ground_truth.split())
    
    # Load visual keywords
    keywords_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
    with open(keywords_path, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
    
    print("=" * 80)
    print("VISUAL BIAS FIX STRATEGY TEST")
    print("=" * 80)
    print(f"\n🎯 Original Keywords: {keywords}")
    print(f"📝 Ground Truth Length: {len(ground_truth)} chars")
    
    # Load model
    print("\n🔧 Loading Whisper model...")
    model_id = "openai/whisper-large-v3-turbo"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        low_cpu_mem_usage=True,
    ).to(device)
    
    processor = AutoProcessor.from_pretrained(model_id)
    
    # Load audio - from video file
    video_path = base_path / "data/raw/L2 _ Java OOP _ Creating a Design Class in a Separate File.mp4"
    print(f"🎵 Extracting audio from: {video_path.name}")
    audio_array, sample_rate = load_audio_from_video(video_path)
    print(f"   Duration: {len(audio_array) / sample_rate:.1f} seconds")
    
    # We'll transcribe just the first 30 seconds for quick testing
    # (Full audio would take too long for iterative testing)
    max_seconds = 60  # 1 minute for more representative results
    max_samples = int(max_seconds * sample_rate)
    if len(audio_array) > max_samples:
        audio_array = audio_array[:max_samples]
        print(f"   (Using first {max_seconds} seconds for testing)")
    
    # Test all strategies
    strategies = [
        "baseline",           # No bias
        "standard_low",       # Very low bias (0.3)
        "standard_medium",    # Medium bias (0.75)
        "adaptive_decay",     # Adaptive decay
        "filtered_keywords",  # Filtered keywords
        "combined",           # All strategies combined
    ]
    
    results = []
    
    print("\n" + "=" * 80)
    print("RUNNING STRATEGIES")
    print("=" * 80)
    
    for strategy in strategies:
        print(f"\n🔄 Testing: {strategy}...")
        start_time = time.time()
        
        transcript, stats = transcribe_with_strategy(
            model, processor, audio_array, sample_rate,
            strategy=strategy,
            keywords=keywords,
            language="en"
        )
        
        elapsed = time.time() - start_time
        
        # Evaluate
        metrics = evaluate_transcript(transcript, ground_truth, keywords)
        
        result = {
            "strategy": strategy,
            "transcript": transcript,
            "transcript_length": len(transcript),
            "time_seconds": elapsed,
            **stats,
            **metrics
        }
        results.append(result)
        
        print(f"   ✓ Done in {elapsed:.1f}s")
        print(f"   📊 Recall: {metrics['term_recall']:.1%}, Similarity: {metrics['similarity']}%, "
              f"Hallucination: {metrics['hallucinated_count']}")
    
    # Summary table
    print("\n" + "=" * 80)
    print("RESULTS COMPARISON")
    print("=" * 80)
    
    print(f"\n{'Strategy':<20} {'Recall':>10} {'Similarity':>12} {'Hallucin':>10} {'Unique':>8} {'Diversity':>10}")
    print("-" * 75)
    
    for r in results:
        print(f"{r['strategy']:<20} {r['term_recall']:>9.1%} {r['similarity']:>11}% "
              f"{r['hallucinated_count']:>10} {r['unique_words']:>8} {r['diversity']:>9.1%}")
    
    # Find best strategy
    print("\n" + "=" * 80)
    print("OPTIMAL STRATEGY SELECTION")
    print("=" * 80)
    
    # Score = recall * 100 - hallucination * 0.5 + similarity * 0.1
    for r in results:
        r['score'] = r['term_recall'] * 100 - r['hallucinated_count'] * 0.5 + r['similarity'] * 0.1
    
    best = max(results, key=lambda x: x['score'])
    baseline = next(r for r in results if r['strategy'] == 'baseline')
    
    print(f"\n★ BEST STRATEGY: {best['strategy']}")
    print(f"  Score: {best['score']:.2f}")
    print(f"  Term Recall: {best['term_recall']:.1%}")
    print(f"  Similarity: {best['similarity']}%")
    print(f"  Hallucination: {best['hallucinated_count']}")
    
    if best['strategy'] != 'baseline':
        improvement = best['term_recall'] - baseline['term_recall']
        print(f"\n  📈 Improvement over baseline: {improvement:+.1%} term recall")
    else:
        print(f"\n  ⚠ Baseline is still the best - visual bias not helping")
    
    # Save results
    output_path = base_path / "output/fix_strategy_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_path}")
    
    # Print transcripts for comparison
    print("\n" + "=" * 80)
    print("SAMPLE TRANSCRIPTS (first 300 chars)")
    print("=" * 80)
    
    for r in results:
        print(f"\n[{r['strategy']}]")
        print(f"{r['transcript'][:300]}...")


if __name__ == "__main__":
    main()
