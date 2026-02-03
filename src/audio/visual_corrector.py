"""
=============================================================================
VISUAL-GUIDED TRANSCRIPT CORRECTOR - Post-Processing for ASR Improvement
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY: Visual-Guided Correction (VGC)

CONCEPT:
After ASR produces a transcript, use visual keywords from VLM to:
1. DETECT: Find technical terms that are likely misheard
2. CORRECT: Replace similar-sounding words with correct visual terms
3. IMPROVE: Increase Technical Term Recall (TTR)

Examples:
- "A Store algorithm" → "A* algorithm" (visual shows "A*")
- "Cohen Southerland" → "Cohen-Sutherland" (visual shows "Cohen-Sutherland")
- "recursive descent" → "recursive descent" (correct, no change)

This is a POST-PROCESSING novelty that works ON TOP of any ASR output.
It can improve both baseline Whisper and Visual-Biased Whisper.
=============================================================================
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from thefuzz import fuzz, process
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@dataclass
class Correction:
    """A single correction made to the transcript."""
    original: str       # Original text in transcript
    corrected: str      # Corrected text (from visual)
    confidence: int     # Match confidence (0-100)
    position: int       # Character position in transcript


class VisualGuidedCorrector:
    """
    Post-processes ASR output using visual keywords for correction.
    
    Works by finding approximate matches between ASR output and visual
    keywords, then replacing likely misheard terms with correct ones.
    """
    
    def __init__(
        self,
        match_threshold: int = 75,      # Minimum fuzzy match to consider
        min_term_length: int = 4,       # Minimum chars to consider for correction
        max_distance: int = 3,          # Max edit distance for word replacement
    ):
        """
        Initialize the corrector.
        
        Args:
            match_threshold: Minimum fuzzy score (0-100) to consider a match
            min_term_length: Minimum characters for a term to be corrected
            max_distance: Maximum edit distance for replacement
        """
        self.match_threshold = match_threshold
        self.min_term_length = min_term_length
        self.max_distance = max_distance
        
        # Stopwords - never try to correct these
        self.stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'and', 'or',
            'but', 'if', 'then', 'else', 'for', 'from', 'to', 'with', 'about',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
            'they', 'what', 'which', 'who', 'where', 'when', 'why', 'how', 'all',
            'some', 'so', 'very', 'just', 'now', 'also', 'here', 'there', 'today',
            'will', 'learn', 'discuss', 'use', 'using', 'used', 'uses', 'compare',
            'algorithm', 'function', 'search', 'line', 'important', 'concepts',
        }
        
        # Known ASR mistakes for technical terms
        self.known_substitutions = {
            "a store": "A*",
            "a-store": "A*",
            "a*": "A*",
        }
    
    def _extract_words(self, text: str) -> List[Tuple[str, int]]:
        """
        Extract words with their positions from text.
        
        Returns:
            List of (word, start_position) tuples
        """
        words = []
        for match in re.finditer(r'\b\w+(?:-\w+)*\b', text):
            word = match.group()
            if len(word) >= self.min_term_length:
                words.append((word, match.start()))
        return words
    
    def _find_best_match(
        self, 
        word: str, 
        visual_keywords: List[str]
    ) -> Optional[Tuple[str, int]]:
        """
        Find the best matching visual keyword for a word.
        
        Returns:
            Tuple of (best_match, score) or None if no good match
        """
        if not visual_keywords:
            return None
        
        word_lower = word.lower()
        
        # Skip stopwords and short words
        if word_lower in self.stopwords:
            return None
        if len(word) < self.min_term_length:
            return None
        
        # Check known substitutions first
        if word_lower in self.known_substitutions:
            return self.known_substitutions[word_lower], 100
        
        # Try fuzzy matching against visual keywords
        best_match = None
        best_score = 0
        
        for keyword in visual_keywords:
            keyword_lower = keyword.lower()
            
            # Skip if keyword is too different in length
            if abs(len(word) - len(keyword)) > 5:
                continue
            
            # Skip if keyword is a stopword
            if keyword_lower in self.stopwords:
                continue
            
            # Calculate similarity - use ratio for same-length, partial for different
            score = fuzz.ratio(word_lower, keyword_lower)
            
            # Must be close but not identical
            if score >= self.match_threshold and score < 100:
                if score > best_score:
                    best_score = score
                    best_match = keyword
        
        if best_match:
            return best_match, best_score
        return None
    
    def correct(
        self,
        transcript: str,
        visual_keywords: List[str],
    ) -> Tuple[str, List[Correction]]:
        """
        Correct transcript using visual keywords.
        
        Args:
            transcript: ASR output text
            visual_keywords: Keywords extracted by VLM
            
        Returns:
            Tuple of (corrected_transcript, list_of_corrections)
        """
        corrections = []
        corrected_text = transcript
        offset = 0  # Track offset as we make replacements
        
        # Extract words from transcript
        words = self._extract_words(transcript)
        
        for word, position in words:
            match_result = self._find_best_match(word, visual_keywords)
            
            if match_result:
                corrected_word, score = match_result
                
                # Only correct if different
                if word.lower() != corrected_word.lower():
                    # Apply correction
                    adjusted_pos = position + offset
                    
                    # Find the word in the current corrected text
                    old_text = corrected_text
                    
                    # Simple replacement (case-preserving)
                    # Replace only at the specific position
                    before = corrected_text[:adjusted_pos]
                    after = corrected_text[adjusted_pos + len(word):]
                    corrected_text = before + corrected_word + after
                    
                    # Track offset change
                    offset += len(corrected_word) - len(word)
                    
                    corrections.append(Correction(
                        original=word,
                        corrected=corrected_word,
                        confidence=score,
                        position=position
                    ))
        
        return corrected_text, corrections
    
    def correct_with_stats(
        self,
        transcript: str,
        visual_keywords: List[str],
    ) -> Dict[str, Any]:
        """
        Correct transcript and return detailed statistics.
        
        Returns:
            Dictionary with corrected text and statistics
        """
        corrected_text, corrections = self.correct(transcript, visual_keywords)
        
        return {
            'original_text': transcript,
            'corrected_text': corrected_text,
            'corrections_count': len(corrections),
            'corrections': [
                {
                    'original': c.original,
                    'corrected': c.corrected,
                    'confidence': c.confidence,
                    'position': c.position
                }
                for c in corrections
            ],
            'original_length': len(transcript),
            'corrected_length': len(corrected_text),
        }
    
    def print_corrections(self, result: Dict[str, Any]) -> None:
        """Pretty print correction results."""
        corrections = result['corrections']
        
        if not corrections:
            console.print("[yellow]No corrections made[/yellow]")
            return
        
        console.print(Panel.fit(
            f"[bold]Visual-Guided Corrections[/bold]\n"
            f"Total corrections: {len(corrections)}",
            border_style="green"
        ))
        
        table = Table(title="Corrections Made", show_header=True)
        table.add_column("Original", style="red")
        table.add_column("→", style="white")
        table.add_column("Corrected", style="green")
        table.add_column("Confidence", style="cyan")
        
        for corr in corrections[:20]:  # Limit display
            table.add_row(
                corr['original'],
                "→",
                corr['corrected'],
                f"{corr['confidence']}%"
            )
        
        if len(corrections) > 20:
            table.add_row("...", "...", "...", "...")
        
        console.print(table)


def test_corrector():
    """Test the Visual-Guided Corrector with sample data."""
    console.print(Panel.fit(
        "[bold]Visual-Guided Corrector Test[/bold]\n"
        "Demo: Correcting ASR mistakes using visual keywords",
        border_style="blue"
    ))
    
    # Sample visual keywords (what's on whiteboard)
    visual_keywords = [
        "A*", "BFS", "DFS", "Heuristic", 
        "Object-Oriented", "Java", "OOP",
        "Cohen-Sutherland", "Clipping"
    ]
    
    # Sample ASR transcript with typical mistakes
    transcript = """
    Today we will learn about the A store algorithm and compare it with 
    breadth first search. The A star algorithm uses a heuristic function.
    We also discuss object oriented programming and Java concepts.
    The Cohen Southerland line clipping algorithm is important.
    """
    
    console.print(f"\n[bold]Visual Keywords:[/bold] {visual_keywords}")
    console.print(f"\n[yellow]Original Transcript:[/yellow]")
    console.print(f"  {transcript[:150]}...")
    
    # Apply correction
    corrector = VisualGuidedCorrector(match_threshold=70)
    result = corrector.correct_with_stats(transcript, visual_keywords)
    
    console.print(f"\n[green]Corrected Transcript:[/green]")
    console.print(f"  {result['corrected_text'][:150]}...")
    
    console.print()
    corrector.print_corrections(result)
    
    return result


if __name__ == "__main__":
    test_corrector()
