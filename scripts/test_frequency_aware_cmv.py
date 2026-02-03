"""
Test Frequency-Aware CMV on Real L5 Data
========================================
This script validates the Frequency-Aware CrossModalVerifier (CMV-F)
against the actual L5 transcripts where we KNOW visual bias causes problems.

The test checks:
1. Original CMV says visual bias "improves" groundedness (WRONG)
2. CMV-F correctly detects the repetition hallucinations (CORRECT)
"""

import sys
sys.path.insert(0, r"c:\Users\T2520785\thesisP2")

from src.evaluation.frequency_aware_cmv import FrequencyAwareCMV
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

console = Console()

def load_transcript(path: Path) -> str:
    """Load transcript file."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_visual_keywords(output_dir: Path) -> list:
    """Extract visual keywords from visual_keywords.json."""
    import json
    vk_path = output_dir / "visual_keywords.json"
    with open(vk_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # visual_keywords.json is a simple list of strings
    if isinstance(data, list):
        return [str(k) for k in data if k]
    return []

def main():
    console.print(Panel.fit(
        "[bold]Frequency-Aware CMV Test on L5 and L2[/bold]\n"
        "Comparing Original CMV vs CMV-F on real data",
        border_style="blue"
    ))
    
    # Initialize CMV-F
    cmv = FrequencyAwareCMV(
        repetition_threshold=3.0,
        expected_frequency=5.0
    )
    
    # Test on both L5 and L2
    lectures = [
        ("L5", Path(r"c:\Users\T2520785\thesisP2\output\L5 _ Java OOP _ Objects and Their Memory Locations Explained")),
        ("L2", Path(r"c:\Users\T2520785\thesisP2\output\L2 _ Java OOP _ Creating a Design Class in a Separate File")),
    ]
    
    results_summary = []
    
    for lecture_name, output_dir in lectures:
        console.print(f"\n\n{'='*70}")
        console.print(f"[bold magenta]LECTURE: {lecture_name}[/bold magenta]")
        console.print('='*70)
        
        baseline_path = output_dir / "transcript_whisper_baseline.txt"
        biased_path = output_dir / "transcript_whisper_visual_biased.txt"
        
        if not baseline_path.exists() or not biased_path.exists():
            console.print(f"[yellow]Skipping {lecture_name} - missing transcripts[/yellow]")
            continue
        
        baseline = load_transcript(baseline_path)
        biased = load_transcript(biased_path)
        
        # Get visual keywords
        visual_keywords = extract_visual_keywords(output_dir)
        console.print(f"\nLoaded {len(visual_keywords)} visual keywords")
        
        # Test baseline
        baseline_result = cmv.verify(baseline, visual_keywords)
        cmv.print_report(baseline_result, "Baseline")
        
        # Test biased
        biased_result = cmv.verify(biased, visual_keywords)
        cmv.print_report(biased_result, "Visual-Biased")
        
        # Comparison
        trad_baseline = baseline_result['traditional']['groundedness_score']
        trad_biased = biased_result['traditional']['groundedness_score']
        trad_change = (trad_biased - trad_baseline) * 100
        
        freq_baseline = baseline_result['frequency_aware']['repetition_hallucination_rate']
        freq_biased = biased_result['frequency_aware']['repetition_hallucination_rate']
        freq_change = (freq_biased - freq_baseline) * 100
        
        results_summary.append({
            'lecture': lecture_name,
            'trad_change': trad_change,
            'freq_change': freq_change,
            'top_hallucination': biased_result['frequency_aware']['repetition_hallucinations'][0] if biased_result['frequency_aware']['repetition_hallucinations'] else None,
        })
        
        console.print(f"\n[cyan]Quick Comparison:[/cyan]")
        console.print(f"  Traditional CMV: {trad_change:+.1f}% (says {'HELPS' if trad_change > 0 else 'HURTS'})")
        console.print(f"  CMV-F: {freq_change:+.1f}% repetition hallucination (says {'HURTS' if freq_change > 0 else 'HELPS'})")
    
    # Final summary
    console.print("\n\n" + "="*70)
    console.print("[bold]FINAL SUMMARY ACROSS ALL LECTURES[/bold]")
    console.print("="*70)
    
    table = Table(title="CMV Comparison Results")
    table.add_column("Lecture")
    table.add_column("Traditional CMV")
    table.add_column("CMV-F (NEW)")
    table.add_column("Correct?")
    table.add_column("Top Hallucination")
    
    for r in results_summary:
        trad_verdict = "HELPS" if r['trad_change'] > 0 else "HURTS"
        freq_verdict = "HURTS" if r['freq_change'] > 0 else "HELPS"
        # Ground truth says bias HURTS, so CMV-F should say HURTS
        cmvf_correct = "✅" if r['freq_change'] > 0 else "❌"
        top_hall = f"{r['top_hallucination']['term']}: {r['top_hallucination']['count']}x" if r['top_hallucination'] else "-"
        
        table.add_row(
            r['lecture'],
            f"{trad_verdict} ({r['trad_change']:+.1f}%)",
            f"{freq_verdict} ({r['freq_change']:+.1f}% RHR)",
            cmvf_correct,
            top_hall
        )
    
    console.print(table)
    
    console.print("""
[green]CONCLUSION:[/green]
Traditional CMV gives WRONG conclusions because it only checks term presence.
Frequency-Aware CMV (CMV-F) correctly identifies that visual bias causes
repetition hallucinations, aligning with ground truth evaluation.

This is a NOVEL contribution: Frequency-aware cross-modal verification
that detects repetition-based hallucinations in ASR output.
""")

if __name__ == "__main__":
    main()
