#!/usr/bin/env python3
"""
=============================================================================
VISUAL BIAS PARAMETER SWEEP - Cross-Validation for Optimal Bias Value
=============================================================================
This script tests multiple bias_value parameters to find the optimal setting
that maximizes technical term recall without causing hallucination.

Methodology:
1. Run Whisper transcription with different bias values: 0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5
2. Compare each output against ground truth transcription
3. Measure: Technical Term Recall, Hallucination Rate, Fuzzy Similarity
4. Report optimal configuration

Usage:
    python scripts/parameter_sweep_bias.py

Output:
    - Console report with comparison table
    - JSON file with detailed results: output/bias_parameter_sweep.json
=============================================================================
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from collections import Counter
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, LogitsProcessorList
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from jiwer import wer
from thefuzz import fuzz

from src.audio.visual_bias_processor import (
    VisualBiasLogitsProcessor,
    get_tokens_for_words,
    remove_repetitions,
    remove_phrase_repetitions,
    remove_ngram_loops
)

console = Console()


def load_ground_truth(path: Path) -> str:
    """Load and clean ground truth transcription"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', content)
    return ' '.join(content.split())


def load_visual_keywords(path: Path) -> list:
    """Load visual keywords from JSON"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_technical_terms(text: str) -> set:
    """Extract Java/programming technical terms"""
    tech_patterns = [
        r'\bclass\b', r'\bobject\b', r'\bpublic\b', r'\bprivate\b',
        r'\bstatic\b', r'\bvoid\b', r'\bmain\b', r'\bString\b',
        r'\bint\b', r'\bnew\b', r'\bmethod\b', r'\bdesign\b',
        r'\btemplate\b', r'\bblueprint\b', r'\bdriver\b', r'\btester\b',
        r'\bcompile\b', r'\bexecute\b', r'\brun\b', r'\bfile\b',
        r'\bpackage\b', r'\bfolder\b', r'\bJava\b', r'\bIDE\b',
        r'\bOOP\b', r'\bsystem\b', r'\bout\b', r'\bprintln\b',
        r'\baccess\b', r'\bmodifier\b', r'\bcode\b'
    ]
    found = set()
    for pattern in tech_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found.update([m.lower() for m in matches])
    return found


def count_term_occurrences(text: str, terms: set) -> dict:
    """Count how many times each term appears"""
    counts = {}
    text_lower = text.lower()
    for term in terms:
        counts[term] = len(re.findall(rf'\b{re.escape(term)}\b', text_lower, re.IGNORECASE))
    return counts


def calculate_metrics(ground_truth: str, transcript: str, gt_terms: set) -> dict:
    """Calculate all evaluation metrics"""
    gt_counts = count_term_occurrences(ground_truth, gt_terms)
    tr_counts = count_term_occurrences(transcript, gt_terms)
    
    # Technical Term Recall
    total_gt = sum(gt_counts.values())
    total_found = sum(min(tr_counts.get(t, 0), gt_counts[t]) for t in gt_counts)
    recall = total_found / total_gt if total_gt > 0 else 0
    
    # Hallucination: terms in transcript but not proportional to ground truth
    hallucinated = sum(max(0, tr_counts.get(t, 0) - gt_counts[t] * 2) for t in gt_terms)
    
    # Fuzzy similarity
    similarity = fuzz.ratio(ground_truth.lower()[:5000], transcript.lower()[:5000])
    
    # Repetition ratio (hallucination indicator)
    words = transcript.lower().split()
    if len(words) > 10:
        word_counts = Counter(words)
        max_repeat = max(word_counts.values())
        repeat_ratio = max_repeat / len(words) if words else 0
    else:
        max_repeat = 0
        repeat_ratio = 0
    
    return {
        'term_recall': recall,
        'similarity': similarity,
        'hallucinated_terms': hallucinated,
        'max_word_repeat': max_repeat,
        'repeat_ratio': repeat_ratio,
        'transcript_length': len(transcript),
        'term_counts': tr_counts
    }


def transcribe_with_bias(
    model,
    processor, 
    audio_path: Path,
    visual_keywords: list,
    bias_value: float,
    device: str = "cuda"
) -> str:
    """Transcribe audio with specified bias value"""
    import librosa
    
    # Load audio
    audio, sr = librosa.load(str(audio_path), sr=16000)
    
    # Prepare input - ensure float16 for model compatibility
    input_features = processor(
        audio, 
        sampling_rate=16000, 
        return_tensors="pt"
    ).input_features.to(device).half()  # Convert to float16 to match model
    
    # Create bias processor if bias_value > 0
    generate_kwargs = {
        # Use English for Romanized Banglish output (not Bengali script)
        "language": "en",
        "task": "transcribe",
        "condition_on_prev_tokens": False,
        "temperature": 0.0,
        "no_speech_threshold": 0.5,
        "compression_ratio_threshold": 1.8,
        "logprob_threshold": -0.8,
    }
    
    if bias_value > 0 and visual_keywords:
        # Get tokens for keywords
        token_ids = get_tokens_for_words(processor.tokenizer, visual_keywords)
        if token_ids:
            bias_processor = VisualBiasLogitsProcessor(
                bias_token_ids=token_ids,
                bias_value=bias_value
            )
            generate_kwargs["logits_processor"] = LogitsProcessorList([bias_processor])
    
    # Generate
    with torch.no_grad():
        generated_ids = model.generate(input_features, **generate_kwargs)
    
    # Decode
    transcript = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    # Apply anti-hallucination post-processing
    transcript = remove_repetitions(transcript, max_repeats=2)
    transcript = remove_phrase_repetitions(transcript, max_repeats=1)
    transcript = remove_ngram_loops(transcript, ngram_sizes=[3, 4, 5], max_repeats=2)
    
    return transcript


def main():
    console.print("\n[bold cyan]=" * 70)
    console.print("[bold cyan]VISUAL BIAS PARAMETER SWEEP - Finding Optimal Bias Value")
    console.print("[bold cyan]=" * 70 + "\n")
    
    base_path = Path("c:/Users/T2520785/thesisP2")
    
    # Paths
    ground_truth_path = base_path / "data/ground_truth/L2_ground_truth.txt"
    audio_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/ingested/full_audio.wav"
    keywords_path = base_path / "output/L2 _ Java OOP _ Creating a Design Class in a Separate File/visual_keywords.json"
    
    # Check files exist
    for p in [ground_truth_path, audio_path, keywords_path]:
        if not p.exists():
            console.print(f"[red]Error: {p} not found[/red]")
            return
    
    # Load data
    console.print("[yellow]Loading data...[/yellow]")
    ground_truth = load_ground_truth(ground_truth_path)
    visual_keywords = load_visual_keywords(keywords_path)
    gt_terms = extract_technical_terms(ground_truth)
    
    console.print(f"  Ground truth: {len(ground_truth):,} chars")
    console.print(f"  Visual keywords: {len(visual_keywords)}")
    console.print(f"  Technical terms: {len(gt_terms)}")
    
    # Filter keywords (remove noise)
    NOISE_WORDS = {'users', 'desktop', 'taw', 'tawhid', 'jdk1', 'files', 'program', 'editing'}
    filtered_keywords = [
        kw for kw in visual_keywords 
        if kw.lower() not in NOISE_WORDS and len(kw) >= 3
    ]
    console.print(f"  Filtered keywords: {len(filtered_keywords)}")
    console.print(f"    → {filtered_keywords[:10]}...")
    
    # Load Whisper model
    console.print("\n[yellow]Loading Whisper model...[/yellow]")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = WhisperForConditionalGeneration.from_pretrained(
        "openai/whisper-large-v3-turbo",
        torch_dtype=torch.float16
    ).to(device)
    processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3-turbo")
    console.print(f"  ✓ Model loaded on {device}")
    
    # Parameter sweep
    bias_values = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
    results = {}
    
    console.print("\n[bold green]Running Parameter Sweep...[/bold green]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for bias_val in bias_values:
            task = progress.add_task(f"Testing bias={bias_val:.2f}...", total=None)
            
            start_time = time.time()
            transcript = transcribe_with_bias(
                model, processor, audio_path, 
                filtered_keywords, bias_val, device
            )
            elapsed = time.time() - start_time
            
            metrics = calculate_metrics(ground_truth, transcript, gt_terms)
            metrics['elapsed_time'] = elapsed
            metrics['transcript'] = transcript[:500] + "..." if len(transcript) > 500 else transcript
            
            results[str(bias_val)] = metrics
            
            progress.remove_task(task)
            console.print(f"  bias={bias_val:.2f}: recall={metrics['term_recall']:.1%}, "
                         f"similarity={metrics['similarity']}%, "
                         f"max_repeat={metrics['max_word_repeat']}, "
                         f"time={elapsed:.1f}s")
    
    # Create comparison table
    console.print("\n" + "=" * 80)
    console.print("[bold]PARAMETER SWEEP RESULTS[/bold]")
    console.print("=" * 80 + "\n")
    
    table = Table(title="Visual Bias Parameter Comparison")
    table.add_column("Bias Value", style="cyan")
    table.add_column("Term Recall", style="green")
    table.add_column("Similarity", style="blue")
    table.add_column("Max Repeat", style="yellow")
    table.add_column("Hallucination", style="red")
    table.add_column("Length", style="dim")
    
    best_score = -1
    best_bias = 0.0
    
    for bias_val in bias_values:
        r = results[str(bias_val)]
        
        # Score: maximize recall, penalize hallucination
        # Score = recall - (hallucination_penalty) - (repeat_penalty)
        hallucination_penalty = min(r['hallucinated_terms'] / 50, 0.5)
        repeat_penalty = min(r['repeat_ratio'] * 2, 0.3)
        score = r['term_recall'] - hallucination_penalty - repeat_penalty
        
        if score > best_score:
            best_score = score
            best_bias = bias_val
        
        # Highlight best
        style = "bold green" if bias_val == best_bias else None
        
        table.add_row(
            f"{bias_val:.2f}",
            f"{r['term_recall']:.1%}",
            f"{r['similarity']}%",
            str(r['max_word_repeat']),
            str(r['hallucinated_terms']),
            f"{r['transcript_length']:,}",
            style=style
        )
    
    console.print(table)
    
    console.print(f"\n[bold green]★ OPTIMAL BIAS VALUE: {best_bias:.2f}[/bold green]")
    console.print(f"  Term Recall: {results[str(best_bias)]['term_recall']:.1%}")
    console.print(f"  Similarity: {results[str(best_bias)]['similarity']}%")
    console.print(f"  Hallucination: {results[str(best_bias)]['hallucinated_terms']} extra terms")
    
    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'ground_truth_length': len(ground_truth),
        'visual_keywords': filtered_keywords,
        'technical_terms': list(gt_terms),
        'optimal_bias': best_bias,
        'results': results
    }
    
    output_path = base_path / "output/bias_parameter_sweep.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n[dim]Results saved to: {output_path}[/dim]")
    
    # Show recommendation
    console.print("\n" + "=" * 80)
    console.print("[bold cyan]RECOMMENDATION[/bold cyan]")
    console.print("=" * 80)
    
    if best_bias == 0.0:
        console.print("[yellow]⚠ Visual bias is not helping - baseline is best.[/yellow]")
        console.print("   Consider: Better keyword filtering, or visual bias may not suit this content.")
    elif best_bias < 1.0:
        console.print(f"[green]✓ Subtle bias ({best_bias}) works best.[/green]")
        console.print(f"   Update transcriber.py: bias_value={best_bias}")
    else:
        console.print(f"[green]✓ Moderate bias ({best_bias}) is optimal.[/green]")
        console.print(f"   Update transcriber.py: bias_value={best_bias}")
    
    return best_bias, results


if __name__ == "__main__":
    main()
