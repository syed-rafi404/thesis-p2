"""
=============================================================================
GROUND TRUTH EVALUATION FOR BanglaASR SERIES
=============================================================================
Computes comprehensive metrics against ground truth:
- Word Error Rate (WER)
- Character Error Rate (CER)
- Term Recall (technical terms)
- Term Precision
- F1 Score
- Fuzzy Similarity
- ROUGE scores
- BLEU scores
=============================================================================
"""

import json
import re
import statistics
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Try imports
try:
    from rapidfuzz import fuzz
    FUZZ_AVAILABLE = True
except ImportError:
    FUZZ_AVAILABLE = False
    print("Warning: rapidfuzz not installed. Run: pip install rapidfuzz")

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False

try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    BLEU_AVAILABLE = True
except ImportError:
    BLEU_AVAILABLE = False

try:
    import jiwer
    WER_AVAILABLE = True
except ImportError:
    WER_AVAILABLE = False
    print("Warning: jiwer not installed. Run: pip install jiwer")

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

# Paths
GROUND_TRUTH_DIR = Path("data/ground_truth")
OUTPUT_BASE = Path("output/live_focused/no_gaze")
RESULTS_DIR = Path("output")

# Technical terms to look for in Banglish programming lectures
TECHNICAL_TERMS = [
    # Python/Programming basics
    'variable', 'string', 'integer', 'int', 'float', 'boolean', 'bool',
    'true', 'false', 'none', 'null', 'type', 'datatype', 'data',
    # Control flow
    'if', 'else', 'elif', 'for', 'while', 'loop', 'break', 'continue',
    # Functions
    'function', 'def', 'return', 'parameter', 'argument', 'call',
    # OOP
    'class', 'object', 'method', 'self', 'init', 'constructor',
    'instance', 'attribute', 'property', 'inheritance',
    # Data structures
    'list', 'array', 'dictionary', 'dict', 'tuple', 'set',
    # Operations
    'print', 'input', 'output', 'value', 'assign', 'equal',
    'add', 'subtract', 'multiply', 'divide', 'modulo',
    # Java specific
    'public', 'private', 'static', 'void', 'main', 'new',
    'extends', 'implements', 'interface', 'abstract',
    # General
    'code', 'program', 'compile', 'run', 'execute', 'error',
    'syntax', 'logic', 'debug', 'test', 'example',
    'name', 'num', 'number', 'age', 'apple', 'fruit',
]


def load_ground_truth(video_name: str) -> str:
    """Load ground truth transcription for a video."""
    # Try different naming patterns
    base_name = video_name.replace('_003', '').replace('_004', '').replace('_007', '')
    patterns = [
        f"{video_name}_ground_truth.txt",
        f"{base_name}_ground_truth.txt",
    ]
    
    for pattern in patterns:
        gt_path = GROUND_TRUTH_DIR / pattern
        if gt_path.exists():
            content = gt_path.read_text(encoding='utf-8')
            # Remove header comments and extract transcription
            lines = content.split('\n')
            transcription_lines = []
            in_transcription = False
            for line in lines:
                if '============' in line:
                    in_transcription = True
                    continue
                if in_transcription and line.strip() and not line.startswith('#'):
                    # Remove timestamps like [0:00-0:30]
                    clean_line = re.sub(r'\[\d+:\d+-\d+:\d+\]', '', line).strip()
                    if clean_line:
                        transcription_lines.append(clean_line)
            return ' '.join(transcription_lines)
    
    return ""


def load_asr_transcript(video_dir: Path) -> str:
    """Load ASR transcript from output directory."""
    # Try different transcript files
    for name in ['transcript_fused.txt', 'transcript_whisper.txt', 'transcript.txt']:
        path = video_dir / name
        if path.exists():
            return path.read_text(encoding='utf-8')
    return ""


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    # Lowercase
    text = text.lower()
    # Remove punctuation except apostrophes
    text = re.sub(r"[^\w\s']", ' ', text)
    # Collapse whitespace
    text = ' '.join(text.split())
    return text


def compute_wer(reference: str, hypothesis: str) -> float:
    """Compute Word Error Rate."""
    if not WER_AVAILABLE:
        return 0.0
    if not reference or not hypothesis:
        return 1.0
    try:
        return jiwer.wer(normalize_text(reference), normalize_text(hypothesis))
    except:
        return 1.0


def compute_cer(reference: str, hypothesis: str) -> float:
    """Compute Character Error Rate."""
    if not WER_AVAILABLE:
        return 0.0
    if not reference or not hypothesis:
        return 1.0
    try:
        return jiwer.cer(normalize_text(reference), normalize_text(hypothesis))
    except:
        return 1.0


def extract_technical_terms(text: str) -> Dict[str, int]:
    """Extract and count technical terms from text."""
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    term_counts = {}
    
    for term in TECHNICAL_TERMS:
        count = words.count(term.lower())
        if count > 0:
            term_counts[term] = count
    
    return term_counts


def compute_term_metrics(gt_terms: Dict[str, int], asr_terms: Dict[str, int]) -> Dict[str, float]:
    """Compute term recall, precision, F1."""
    # Total terms in GT
    gt_total = sum(gt_terms.values())
    
    # Total correctly recalled (min of GT and ASR for each term)
    recalled = sum(min(gt_terms.get(t, 0), asr_terms.get(t, 0)) for t in gt_terms)
    
    # Total in ASR
    asr_total = sum(asr_terms.values())
    
    # Recall: how many GT terms were captured
    recall = recalled / gt_total if gt_total > 0 else 0
    
    # Precision: how many ASR terms are correct
    precision = recalled / asr_total if asr_total > 0 else 0
    
    # F1
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'recall': recall,
        'precision': precision,
        'f1': f1,
        'gt_terms': gt_total,
        'asr_terms': asr_total,
        'matched': recalled,
    }


def compute_fuzzy_similarity(reference: str, hypothesis: str) -> float:
    """Compute fuzzy string similarity."""
    if not FUZZ_AVAILABLE:
        return 0.0
    if not reference or not hypothesis:
        return 0.0
    return fuzz.ratio(normalize_text(reference), normalize_text(hypothesis)) / 100


def compute_rouge(reference: str, hypothesis: str) -> Dict[str, float]:
    """Compute ROUGE scores."""
    if not ROUGE_AVAILABLE or not reference or not hypothesis:
        return {'rouge1': 0, 'rouge2': 0, 'rougeL': 0}
    
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    
    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure,
    }


def compute_bleu(reference: str, hypothesis: str) -> float:
    """Compute BLEU score."""
    if not BLEU_AVAILABLE or not reference or not hypothesis:
        return 0.0
    
    ref_tokens = normalize_text(reference).split()
    hyp_tokens = normalize_text(hypothesis).split()
    
    if len(ref_tokens) < 4 or len(hyp_tokens) < 4:
        return 0.0
    
    smoothie = SmoothingFunction().method1
    try:
        return sentence_bleu([ref_tokens], hyp_tokens, smoothing_function=smoothie)
    except:
        return 0.0


def evaluate_video(video_name: str, interval: int) -> Dict[str, Any]:
    """Evaluate a single video against ground truth."""
    # Load ground truth
    gt_text = load_ground_truth(video_name)
    if not gt_text:
        return {'error': 'No ground truth found', 'video': video_name, 'interval': interval}
    
    # Load ASR transcript
    video_dir = OUTPUT_BASE / f"interval_{interval:02d}s" / video_name
    asr_text = load_asr_transcript(video_dir)
    if not asr_text:
        return {'error': 'No ASR transcript found', 'video': video_name, 'interval': interval}
    
    # Compute metrics
    wer = compute_wer(gt_text, asr_text)
    cer = compute_cer(gt_text, asr_text)
    
    gt_terms = extract_technical_terms(gt_text)
    asr_terms = extract_technical_terms(asr_text)
    term_metrics = compute_term_metrics(gt_terms, asr_terms)
    
    fuzzy = compute_fuzzy_similarity(gt_text, asr_text)
    rouge = compute_rouge(gt_text, asr_text)
    bleu = compute_bleu(gt_text, asr_text)
    
    return {
        'video': video_name,
        'interval': interval,
        'gt_chars': len(gt_text),
        'asr_chars': len(asr_text),
        'wer': wer,
        'cer': cer,
        'term_recall': term_metrics['recall'],
        'term_precision': term_metrics['precision'],
        'term_f1': term_metrics['f1'],
        'gt_terms_count': term_metrics['gt_terms'],
        'asr_terms_count': term_metrics['asr_terms'],
        'fuzzy_similarity': fuzzy,
        **rouge,
        'bleu': bleu,
    }


def generate_report(results: List[Dict]) -> str:
    """Generate comprehensive evaluation report."""
    # Filter out errors
    valid_results = [r for r in results if 'error' not in r]
    error_results = [r for r in results if 'error' in r]
    
    if not valid_results:
        return "# No valid results to report\n\nAll evaluations failed - please add ground truth transcriptions."
    
    md = []
    md.append("# P2 GROUND TRUTH EVALUATION REPORT")
    md.append("")
    md.append(f"**Generated**: {datetime.now().strftime('%B %d, %Y at %H:%M')}")
    md.append("")
    md.append("**Dataset**: BanglaASR Series (Real Classroom Recordings)")
    md.append("")
    md.append("---")
    md.append("")
    
    # Executive Summary
    md.append("## Executive Summary")
    md.append("")
    md.append("| Metric | Average | Min | Max |")
    md.append("|--------|---------|-----|-----|")
    
    metrics = ['wer', 'cer', 'term_recall', 'term_precision', 'term_f1', 'fuzzy_similarity', 'rougeL', 'bleu']
    metric_names = ['WER ↓', 'CER ↓', 'Term Recall ↑', 'Term Precision ↑', 'Term F1 ↑', 'Fuzzy Similarity ↑', 'ROUGE-L ↑', 'BLEU ↑']
    
    for metric, name in zip(metrics, metric_names):
        values = [r[metric] for r in valid_results]
        avg = statistics.mean(values)
        mn = min(values)
        mx = max(values)
        if metric in ['wer', 'cer']:
            md.append(f"| {name} | {avg:.1%} | {mn:.1%} | {mx:.1%} |")
        else:
            md.append(f"| {name} | {avg:.3f} | {mn:.3f} | {mx:.3f} |")
    
    md.append("")
    md.append(f"> **Evaluated**: {len(valid_results)} runs | **Skipped**: {len(error_results)} (no ground truth)")
    md.append("")
    
    # By Interval
    md.append("---")
    md.append("")
    md.append("## 1. Metrics by Frame Interval")
    md.append("")
    md.append("| Interval | WER ↓ | CER ↓ | Term Recall | Term F1 | ROUGE-L |")
    md.append("|----------|-------|-------|-------------|---------|---------|")
    
    by_interval = defaultdict(list)
    for r in valid_results:
        by_interval[r['interval']].append(r)
    
    for interval in [10, 20, 30]:
        runs = by_interval.get(interval, [])
        if runs:
            wer = statistics.mean([r['wer'] for r in runs])
            cer = statistics.mean([r['cer'] for r in runs])
            recall = statistics.mean([r['term_recall'] for r in runs])
            f1 = statistics.mean([r['term_f1'] for r in runs])
            rouge = statistics.mean([r['rougeL'] for r in runs])
            md.append(f"| {interval}s | {wer:.1%} | {cer:.1%} | {recall:.3f} | {f1:.3f} | {rouge:.3f} |")
    md.append("")
    
    # By Video
    md.append("---")
    md.append("")
    md.append("## 2. Metrics by Video")
    md.append("")
    md.append("| Video | Best Interval | WER | Term Recall | ROUGE-L |")
    md.append("|-------|---------------|-----|-------------|---------|")
    
    by_video = defaultdict(list)
    for r in valid_results:
        by_video[r['video']].append(r)
    
    for video in sorted(by_video.keys()):
        runs = by_video[video]
        best = min(runs, key=lambda x: x['wer'])
        md.append(f"| {video} | {best['interval']}s | {best['wer']:.1%} | {best['term_recall']:.3f} | {best['rougeL']:.3f} |")
    md.append("")
    
    # Complete Results
    md.append("---")
    md.append("")
    md.append("## 3. Complete Results Table")
    md.append("")
    md.append("| # | Video | Int | WER | CER | Recall | Prec | F1 | Fuzzy | ROUGE-L | BLEU |")
    md.append("|---|-------|-----|-----|-----|--------|------|-----|-------|---------|------|")
    
    for i, r in enumerate(sorted(valid_results, key=lambda x: (x['video'], x['interval'])), 1):
        md.append(f"| {i} | {r['video']} | {r['interval']}s | {r['wer']:.1%} | {r['cer']:.1%} | {r['term_recall']:.3f} | {r['term_precision']:.3f} | {r['term_f1']:.3f} | {r['fuzzy_similarity']:.3f} | {r['rougeL']:.3f} | {r['bleu']:.3f} |")
    md.append("")
    
    # Skipped
    if error_results:
        md.append("---")
        md.append("")
        md.append("## 4. Skipped (No Ground Truth)")
        md.append("")
        md.append("| Video | Interval | Reason |")
        md.append("|-------|----------|--------|")
        for r in error_results:
            md.append(f"| {r['video']} | {r['interval']}s | {r['error']} |")
        md.append("")
    
    # Conclusions
    md.append("---")
    md.append("")
    md.append("## 5. Key Findings")
    md.append("")
    
    # Best performing
    if valid_results:
        best_wer = min(valid_results, key=lambda x: x['wer'])
        best_recall = max(valid_results, key=lambda x: x['term_recall'])
        
        avg_wer = statistics.mean([r['wer'] for r in valid_results])
        avg_recall = statistics.mean([r['term_recall'] for r in valid_results])
        
        md.append(f"1. **Average WER**: {avg_wer:.1%}")
        md.append(f"2. **Best WER**: {best_wer['video']} @ {best_wer['interval']}s ({best_wer['wer']:.1%})")
        md.append(f"3. **Average Term Recall**: {avg_recall:.3f}")
        md.append(f"4. **Best Term Recall**: {best_recall['video']} @ {best_recall['interval']}s ({best_recall['term_recall']:.3f})")
    md.append("")
    
    md.append("---")
    md.append("")
    md.append(f"*Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return "\n".join(md)


def main():
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]   GROUND TRUTH EVALUATION - BanglaASR Series              [/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")
    
    # Check dependencies
    deps = []
    if not WER_AVAILABLE:
        deps.append("jiwer")
    if not FUZZ_AVAILABLE:
        deps.append("rapidfuzz")
    
    if deps:
        console.print(f"[yellow]Installing missing dependencies: {', '.join(deps)}...[/yellow]")
        import subprocess
        subprocess.run(["pip", "install"] + deps + ["-q"])
    
    # Find all videos
    results = []
    videos_found = set()
    
    for interval in [10, 20, 30]:
        interval_dir = OUTPUT_BASE / f"interval_{interval:02d}s"
        if not interval_dir.exists():
            continue
        
        for video_dir in sorted(interval_dir.iterdir()):
            if video_dir.is_dir():
                video_name = video_dir.name
                videos_found.add(video_name)
                console.print(f"[cyan]Evaluating {video_name} @ {interval}s...[/cyan]")
                result = evaluate_video(video_name, interval)
                results.append(result)
                
                if 'error' not in result:
                    console.print(f"  ✓ WER: {result['wer']:.1%}, Term Recall: {result['term_recall']:.3f}")
                else:
                    console.print(f"  [yellow]⚠ {result['error']}[/yellow]")
    
    # Check for missing ground truth
    console.print("\n[bold yellow]Ground Truth Status:[/bold yellow]")
    gt_files = list(GROUND_TRUTH_DIR.glob("BanglaASR*_ground_truth.txt"))
    
    for gt_file in gt_files:
        content = gt_file.read_text(encoding='utf-8')
        # Check if it has actual transcription (more than just template)
        if len(content.split('\n')) > 30:
            console.print(f"  [green]✓ {gt_file.name}[/green]")
        else:
            console.print(f"  [yellow]○ {gt_file.name} (template only - needs transcription)[/yellow]")
    
    # Generate report
    console.print("\n[cyan]Generating report...[/cyan]")
    report = generate_report(results)
    
    report_path = RESULTS_DIR / "P2_GROUND_TRUTH_EVALUATION.md"
    report_path.write_text(report, encoding='utf-8')
    console.print(f"  ✓ Report: {report_path}")
    
    # Save JSON
    json_path = RESULTS_DIR / "p2_ground_truth_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    console.print(f"  ✓ JSON: {json_path}")
    
    # Summary
    valid = [r for r in results if 'error' not in r]
    console.print(f"\n[bold]Evaluated: {len(valid)}/{len(results)} runs[/bold]")
    
    if valid:
        console.print(f"\n[bold yellow]Key Metrics:[/bold yellow]")
        console.print(f"  • Average WER: {statistics.mean([r['wer'] for r in valid]):.1%}")
        console.print(f"  • Average Term Recall: {statistics.mean([r['term_recall'] for r in valid]):.3f}")
        console.print(f"  • Average ROUGE-L: {statistics.mean([r['rougeL'] for r in valid]):.3f}")
    
    console.print("\n[bold green]═══════════════════════════════════════════════════════════[/bold green]")
    console.print("[bold green]   EVALUATION COMPLETE!                                    [/bold green]")
    console.print("[bold green]═══════════════════════════════════════════════════════════[/bold green]\n")


if __name__ == "__main__":
    main()
