"""
=============================================================================
SELF-CORRECTING ASR PIPELINE
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - CORE CONTRIBUTION

This is THE contribution that makes the project novel:
    Whisper → CMV-F (detect hallucination) → LLM (correct it)

Instead of just "using APIs", this creates a FEEDBACK LOOP where:
1. ASR generates transcript
2. CMV-F detects repetition hallucinations (frequency analysis)
3. LLM corrects the detected hallucinations using visual context

This is a SYSTEM, not just a pipeline. The components work TOGETHER.
=============================================================================
"""

import re
from typing import Dict, List, Any, Tuple
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Import CMV-F
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.evaluation.frequency_aware_cmv import FrequencyAwareCMV


class SelfCorrectingPipeline:
    """
    A self-correcting ASR pipeline that uses cross-modal verification
    to detect and fix hallucinations.
    
    The novelty is in the FEEDBACK LOOP:
    - Traditional pipeline: ASR → Output
    - Our pipeline: ASR → CMV-F (detect) → LLM (correct) → Output
    
    This is NOT just "gluing APIs together" - it's a verification-correction
    system that doesn't exist in any off-the-shelf solution.
    """
    
    def __init__(
        self,
        repetition_threshold: float = 3.0,
        expected_frequency: float = 5.0,
        correction_mode: str = "replace",  # "replace" or "flag"
    ):
        """
        Initialize the self-correcting pipeline.
        
        Args:
            repetition_threshold: TFD threshold for flagging repetitions
            expected_frequency: Baseline expected term frequency
            correction_mode: "replace" to auto-correct, "flag" to mark only
        """
        self.cmv = FrequencyAwareCMV(
            repetition_threshold=repetition_threshold,
            expected_frequency=expected_frequency,
        )
        self.correction_mode = correction_mode
        
    def detect_hallucinations(
        self,
        transcript: str,
        visual_keywords: List[str],
    ) -> Dict[str, Any]:
        """
        Step 1: Detect hallucinations using CMV-F.
        
        Returns detailed analysis of what's wrong with the transcript.
        """
        return self.cmv.verify(transcript, visual_keywords)
    
    def _build_correction_prompt(
        self,
        transcript: str,
        hallucination_report: Dict[str, Any],
        visual_keywords: List[str],
    ) -> str:
        """
        Build an LLM prompt for correcting detected hallucinations.
        
        This is the CROSS-MODAL CORRECTION step.
        """
        rep_halls = hallucination_report['frequency_aware']['repetition_hallucinations']
        
        # Build the problematic terms list
        problem_terms = []
        for rh in rep_halls:
            problem_terms.append(
                f"- '{rh['term']}' appears {rh['count']} times "
                f"(expected ~{rh['expected']:.0f}, {rh['tfd']:.1f}x over-represented)"
            )
        
        prompt = f"""You are correcting a transcript that has REPETITION HALLUCINATIONS.
The ASR system incorrectly repeated certain words too many times.

VISUAL CONTEXT (what's on the whiteboard):
{', '.join(visual_keywords[:30])}

DETECTED PROBLEMS:
{chr(10).join(problem_terms) if problem_terms else "No major repetition issues detected."}

ORIGINAL TRANSCRIPT:
{transcript}

INSTRUCTIONS:
1. Remove excessive repetitions of the flagged words
2. Keep ONE or TWO natural occurrences of each term
3. Preserve the meaning and flow of the lecture
4. Do NOT add new content - only remove excessive repetitions
5. Keep the Banglish style (mix of Bengali and English)

CORRECTED TRANSCRIPT:"""
        
        return prompt
    
    def correct_with_llm(
        self,
        transcript: str,
        hallucination_report: Dict[str, Any],
        visual_keywords: List[str],
        llm_model=None,
        tokenizer=None,
    ) -> str:
        """
        Step 2: Use LLM to correct detected hallucinations.
        
        If no LLM provided, uses rule-based correction as fallback.
        """
        rep_halls = hallucination_report['frequency_aware']['repetition_hallucinations']
        
        if not rep_halls:
            return transcript  # Nothing to correct
        
        # If LLM is provided, use it
        if llm_model is not None and tokenizer is not None:
            prompt = self._build_correction_prompt(
                transcript, hallucination_report, visual_keywords
            )
            
            inputs = tokenizer(prompt, return_tensors="pt").to(llm_model.device)
            outputs = llm_model.generate(
                **inputs,
                max_new_tokens=len(transcript) + 100,
                temperature=0.3,
                do_sample=True,
            )
            corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the corrected part
            if "CORRECTED TRANSCRIPT:" in corrected:
                corrected = corrected.split("CORRECTED TRANSCRIPT:")[-1].strip()
            
            return corrected
        
        # Fallback: Rule-based correction
        return self._rule_based_correction(transcript, rep_halls)
    
    def _rule_based_correction(
        self,
        transcript: str,
        repetition_hallucinations: List[Dict],
    ) -> str:
        """
        Rule-based correction when LLM is not available.
        
        Strategy: Keep first N occurrences, remove excess.
        """
        corrected = transcript
        
        for rh in repetition_hallucinations:
            term = rh['term']
            expected = max(3, int(rh['expected']))  # Keep at least 3
            
            # Find all occurrences
            pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
            matches = list(pattern.finditer(corrected))
            
            if len(matches) > expected:
                # Remove excess occurrences (keep first 'expected' occurrences)
                # Work backwards to preserve indices
                for match in reversed(matches[expected:]):
                    start, end = match.span()
                    # Remove the word and any trailing space/punctuation
                    if end < len(corrected) and corrected[end] in ' .,':
                        end += 1
                    corrected = corrected[:start] + corrected[end:]
        
        # Clean up multiple spaces
        corrected = re.sub(r'\s+', ' ', corrected)
        corrected = re.sub(r'\s+([.,])', r'\1', corrected)
        
        return corrected.strip()
    
    def process(
        self,
        transcript: str,
        visual_keywords: List[str],
        llm_model=None,
        tokenizer=None,
    ) -> Dict[str, Any]:
        """
        Full self-correcting pipeline.
        
        Returns:
            - original: Original transcript
            - corrected: Corrected transcript
            - hallucination_report: CMV-F analysis
            - corrections_made: List of corrections applied
        """
        # Step 1: Detect
        report = self.detect_hallucinations(transcript, visual_keywords)
        
        # Step 2: Correct
        corrected = self.correct_with_llm(
            transcript, report, visual_keywords, llm_model, tokenizer
        )
        
        # Step 3: Re-verify
        post_correction_report = self.detect_hallucinations(corrected, visual_keywords)
        
        # Calculate improvement
        before_rhr = report['frequency_aware']['repetition_hallucination_rate']
        after_rhr = post_correction_report['frequency_aware']['repetition_hallucination_rate']
        improvement = (before_rhr - after_rhr) * 100
        
        return {
            'original': transcript,
            'corrected': corrected,
            'hallucination_report': report,
            'post_correction_report': post_correction_report,
            'metrics': {
                'rhr_before': before_rhr,
                'rhr_after': after_rhr,
                'rhr_improvement': improvement,
                'hallucinations_detected': len(report['frequency_aware']['repetition_hallucinations']),
            }
        }
    
    def print_report(self, result: Dict[str, Any]) -> None:
        """Print a detailed correction report."""
        console.print(Panel.fit(
            "[bold]Self-Correcting Pipeline Report[/bold]",
            border_style="blue"
        ))
        
        metrics = result['metrics']
        
        console.print(f"\n[cyan]Hallucinations Detected:[/cyan] {metrics['hallucinations_detected']}")
        console.print(f"[cyan]RHR Before Correction:[/cyan] {metrics['rhr_before']*100:.1f}%")
        console.print(f"[cyan]RHR After Correction:[/cyan] {metrics['rhr_after']*100:.1f}%")
        console.print(f"[green]Improvement:[/green] {metrics['rhr_improvement']:+.1f}%")
        
        # Show what was corrected
        rep_halls = result['hallucination_report']['frequency_aware']['repetition_hallucinations']
        if rep_halls:
            console.print(f"\n[yellow]Repetitions Corrected:[/yellow]")
            for rh in rep_halls[:5]:
                console.print(f"  • '{rh['term']}': {rh['count']}x → ~{rh['expected']:.0f}x")
        
        # Word count comparison
        orig_words = len(result['original'].split())
        corr_words = len(result['corrected'].split())
        console.print(f"\n[dim]Word count: {orig_words} → {corr_words} ({corr_words - orig_words:+d})[/dim]")


# =============================================================================
# TEST FUNCTION
# =============================================================================

def test_self_correcting_pipeline():
    """Test the self-correcting pipeline on L2 data."""
    from pathlib import Path
    import json
    
    console.print(Panel.fit(
        "[bold]Self-Correcting Pipeline Test[/bold]\n"
        "Testing on L2 visual-biased transcript",
        border_style="blue"
    ))
    
    # Load L2 data
    output_dir = Path(r"c:\Users\T2520785\thesisP2\output\L2 _ Java OOP _ Creating a Design Class in a Separate File")
    
    biased_path = output_dir / "transcript_whisper_visual_biased.txt"
    with open(biased_path, 'r', encoding='utf-8') as f:
        biased = f.read()
    
    vk_path = output_dir / "visual_keywords.json"
    with open(vk_path, 'r', encoding='utf-8') as f:
        visual_keywords = json.load(f)
    
    console.print(f"Loaded transcript: {len(biased)} chars")
    console.print(f"Visual keywords: {len(visual_keywords)}")
    
    # Run pipeline
    pipeline = SelfCorrectingPipeline(
        repetition_threshold=3.0,
        expected_frequency=5.0,
    )
    
    result = pipeline.process(biased, visual_keywords)
    pipeline.print_report(result)
    
    # Show sample of correction
    console.print(f"\n[bold]Sample of Original:[/bold]")
    console.print(f"[dim]{result['original'][:300]}...[/dim]")
    
    console.print(f"\n[bold]Sample of Corrected:[/bold]")
    console.print(f"[green]{result['corrected'][:300]}...[/green]")
    
    return result


if __name__ == "__main__":
    test_self_correcting_pipeline()
