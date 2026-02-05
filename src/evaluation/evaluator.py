"""
=============================================================================
BANGLISH EVALUATOR - Technical Term Recall (TTR) + WER Evaluation
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Evaluation Module

Compares 'Standard Whisper' vs 'Visually-Biased Whisper' transcription quality
by measuring:
1. Technical Term Recall (TTR) - fuzzy string matching for domain terms
2. Word Error Rate (WER) - standard ASR quality metric

Metrics:
- TTR = (Found Terms / Total Ground Truth Terms) * 100
- WER = (Substitutions + Insertions + Deletions) / Total Reference Words
- Uses fuzzy matching (thefuzz) with threshold > 85 for flexible TTR matching
=============================================================================
"""

from typing import List, Dict, Any, Optional
from thefuzz import fuzz

# WER calculation
try:
    from jiwer import wer, cer
    JIWER_AVAILABLE = True
except ImportError:
    JIWER_AVAILABLE = False

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class BanglishEvaluator:
    """
    Evaluator for comparing ASR transcription quality on technical terms.
    
    Uses fuzzy string matching to account for minor variations in how
    technical terms might be transcribed (e.g., "A*" vs "A-star").
    """
    
    def __init__(self, fuzzy_threshold: int = 85):
        """
        Initialize the evaluator.
        
        Args:
            fuzzy_threshold: Minimum fuzzy match score (0-100) to consider a term found.
                            Default 85 allows for minor spelling variations.
        """
        self.fuzzy_threshold = fuzzy_threshold
    
    def _normalize(self, text: str) -> str:
        """Normalize text for comparison (lowercase, strip whitespace)."""
        return text.lower().strip()
    
    def calculate_wer(
        self,
        reference: str,
        hypothesis: str
    ) -> Dict[str, float]:
        """
        Calculate Word Error Rate (WER) and Character Error Rate (CER).
        
        WER = (S + I + D) / N
        Where:
            S = Substitutions
            I = Insertions  
            D = Deletions
            N = Total words in reference
        
        Args:
            reference: Ground truth transcript
            hypothesis: ASR output transcript
            
        Returns:
            Dictionary with 'wer' and 'cer' values (0.0 to 1.0+)
            Lower is better. WER > 1.0 possible if more errors than words.
        """
        if not JIWER_AVAILABLE:
            return {'wer': -1.0, 'cer': -1.0, 'error': 'jiwer not installed'}
        
        # Normalize texts
        ref_normalized = self._normalize(reference)
        hyp_normalized = self._normalize(hypothesis)
        
        if not ref_normalized:
            return {'wer': 0.0, 'cer': 0.0} if not hyp_normalized else {'wer': 1.0, 'cer': 1.0}
        
        try:
            wer_score = wer(ref_normalized, hyp_normalized)
            cer_score = cer(ref_normalized, hyp_normalized)
            return {
                'wer': round(wer_score, 4),
                'cer': round(cer_score, 4)
            }
        except Exception as e:
            return {'wer': -1.0, 'cer': -1.0, 'error': str(e)}
    
    def _fuzzy_find(self, term: str, transcript: str) -> tuple[bool, int]:
        """
        Check if a term exists in the transcript using fuzzy matching.
        
        Args:
            term: The technical term to search for
            transcript: The full transcript text
            
        Returns:
            Tuple of (found: bool, best_score: int)
        """
        term_normalized = self._normalize(term)
        transcript_normalized = self._normalize(transcript)
        
        # Try exact substring match first
        if term_normalized in transcript_normalized:
            return True, 100
        
        # Fuzzy match: check partial ratio against sliding windows
        # partial_ratio handles substring matching well
        score = fuzz.partial_ratio(term_normalized, transcript_normalized)
        
        return score >= self.fuzzy_threshold, score
    
    def evaluate_recall(
        self, 
        ground_truth_terms: List[str], 
        transcript: str
    ) -> Dict[str, Any]:
        """
        Evaluate Technical Term Recall (TTR) for a transcript.
        
        Args:
            ground_truth_terms: List of technical terms that should appear
            transcript: The ASR transcript to evaluate
            
        Returns:
            Dictionary with:
            - 'recall': float (0.0 to 1.0)
            - 'found': List of terms that were found
            - 'missed': List of terms that were not found
            - 'scores': Dict mapping each term to its fuzzy match score
        """
        found = []
        missed = []
        scores = {}
        
        for term in ground_truth_terms:
            is_found, score = self._fuzzy_find(term, transcript)
            scores[term] = score
            
            if is_found:
                found.append(term)
            else:
                missed.append(term)
        
        total = len(ground_truth_terms)
        recall = len(found) / total if total > 0 else 0.0
        
        return {
            'recall': recall,
            'found': found,
            'missed': missed,
            'scores': scores,
            'total': total,
            'found_count': len(found),
            'missed_count': len(missed),
        }
    
    def compare_transcripts(
        self,
        ground_truth_terms: List[str],
        baseline_transcript: str,
        biased_transcript: str,
        baseline_name: str = "Standard Whisper",
        biased_name: str = "Visual-Biased Whisper",
    ) -> Dict[str, Any]:
        """
        Compare two transcripts and calculate improvement.
        
        Args:
            ground_truth_terms: List of technical terms
            baseline_transcript: Transcript from standard Whisper
            biased_transcript: Transcript from visually-biased Whisper
            baseline_name: Display name for baseline
            biased_name: Display name for biased version
            
        Returns:
            Comparison results with improvement metrics
        """
        baseline_result = self.evaluate_recall(ground_truth_terms, baseline_transcript)
        biased_result = self.evaluate_recall(ground_truth_terms, biased_transcript)
        
        improvement = biased_result['recall'] - baseline_result['recall']
        improvement_pct = improvement * 100
        
        return {
            'baseline': baseline_result,
            'biased': biased_result,
            'improvement': improvement,
            'improvement_pct': improvement_pct,
            'baseline_name': baseline_name,
            'biased_name': biased_name,
        }
    
    def print_comparison(self, comparison: Dict[str, Any]) -> None:
        """Pretty print the comparison results using Rich."""
        baseline = comparison['baseline']
        biased = comparison['biased']
        
        # Create comparison table
        table = Table(title="Technical Term Recall (TTR) Comparison", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column(comparison['baseline_name'], style="yellow")
        table.add_column(comparison['biased_name'], style="green")
        
        table.add_row(
            "Recall",
            f"{baseline['recall']:.1%}",
            f"{biased['recall']:.1%}"
        )
        table.add_row(
            "Found / Total",
            f"{baseline['found_count']} / {baseline['total']}",
            f"{biased['found_count']} / {biased['total']}"
        )
        table.add_row(
            "Found Terms",
            ", ".join(baseline['found']) or "None",
            ", ".join(biased['found']) or "None"
        )
        table.add_row(
            "Missed Terms",
            ", ".join(baseline['missed']) or "None",
            ", ".join(biased['missed']) or "None"
        )
        
        console.print(table)
        
        # Improvement summary
        imp = comparison['improvement_pct']
        if imp > 0:
            console.print(f"\n[bold green]✓ Improvement: +{imp:.1f}% TTR[/bold green]")
        elif imp < 0:
            console.print(f"\n[bold red]✗ Regression: {imp:.1f}% TTR[/bold red]")
        else:
            console.print(f"\n[bold yellow]→ No change in TTR[/bold yellow]")
        
        # Detailed scores
        console.print("\n[dim]Fuzzy Match Scores:[/dim]")
        for term in baseline['scores']:
            b_score = baseline['scores'][term]
            v_score = biased['scores'][term]
            delta = v_score - b_score
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            console.print(f"  {term}: {b_score} → {v_score} ({delta_str})")


if __name__ == "__main__":
    # Test the evaluator with sample data
    # NOTE: This is just a demo. In real usage, ground_truth comes from VLM whiteboard extraction
    console.print(Panel.fit(
        "[bold]BanglishEvaluator Test[/bold]\n"
        "Demo: Comparing Standard vs Visual-Biased Whisper\n"
        "[dim]Real evaluation uses VLM-extracted terms as ground truth[/dim]",
        border_style="blue"
    ))
    
    # Example ground truth - could be ANY topic:
    # - AI: ["A*", "Heuristic", "BFS"]
    # - Graphics: ["Cohen Sutherland", "Clipping", "Viewport"]
    # - Architecture: ["RISC-V", "Pipeline", "Hazard"]
    # - Data Structures: ["Binary Tree", "AVL", "Red-Black"]
    truth = ["A*", "Heuristic", "BFS"]  # Demo example
    
    # Simulated transcripts
    transcript_bad = "The A-Store algorithm uses a heuristic."  # Standard Whisper (mishears A*)
    transcript_good = "The A* algorithm uses a heuristic."      # Visual-Biased (correct)
    
    console.print("\n[bold]Ground Truth Terms (from VLM):[/bold]", truth)
    console.print(f"\n[yellow]Standard Whisper:[/yellow] \"{transcript_bad}\"")
    console.print(f"[green]Visual-Biased:[/green] \"{transcript_good}\"")
    console.print()
    
    # Run evaluation
    evaluator = BanglishEvaluator(fuzzy_threshold=85)
    comparison = evaluator.compare_transcripts(
        ground_truth_terms=truth,
        baseline_transcript=transcript_bad,
        biased_transcript=transcript_good,
    )
    
    evaluator.print_comparison(comparison)
