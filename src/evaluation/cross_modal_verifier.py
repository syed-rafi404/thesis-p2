"""
=============================================================================
CROSS-MODAL VERIFIER - Hallucination Detection via Visual Grounding
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY: Cross-Modal Verification (CMV)

CONCEPT:
If Whisper produces a technical term that does NOT appear in the whiteboard
(visual context), it is likely a hallucination. We can:
1. DETECT: Flag ungrounded terms as potential hallucinations
2. MEASURE: Calculate "groundedness score" = grounded_terms / total_terms
3. IMPROVE: Post-process to remove or correct ungrounded terms

This creates a self-checking system:
- VLM extracts visual keywords (ground truth)
- Whisper transcribes audio
- CMV checks if ASR output is "grounded" in visual context
- Ungrounded technical terms → likely hallucinations

Metrics:
- Groundedness Score (GS) = grounded_terms / all_technical_terms
- Hallucination Rate (HR) = 1 - GS
- Higher GS = more trustworthy transcript
=============================================================================
"""

import re
from typing import List, Dict, Any, Set, Tuple
from thefuzz import fuzz
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class CrossModalVerifier:
    """
    Verifies ASR output against visual context to detect hallucinations.
    
    A term in the transcript is "grounded" if it appears in the visual context.
    Ungrounded technical terms are flagged as potential hallucinations.
    """
    
    def __init__(
        self, 
        fuzzy_threshold: int = 80,
        min_term_length: int = 3
    ):
        """
        Initialize the verifier.
        
        Args:
            fuzzy_threshold: Minimum fuzzy match score to consider grounded
            min_term_length: Minimum characters for a term to be checked
        """
        self.fuzzy_threshold = fuzzy_threshold
        self.min_term_length = min_term_length
        
        # Common filler words to ignore (English + Bengali romanized)
        self.stopwords = {
            # English
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
            'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'not', 'only', 'same', 'so',
            'than', 'too', 'very', 'just', 'but', 'and', 'or', 'if', 'then',
            'else', 'for', 'from', 'to', 'with', 'about', 'into', 'through',
            'during', 'before', 'after', 'above', 'below', 'between', 'under',
            'again', 'further', 'once', 'here', 'there', 'also', 'now',
            # Bengali romanized common words
            'ami', 'tumi', 'apni', 'se', 'ora', 'amra', 'tomra', 'apnara',
            'eta', 'ota', 'ki', 'keno', 'kothay', 'kokhon', 'kivabe', 'kemon',
            'ar', 'ba', 'kintu', 'tai', 'jodi', 'tahole', 'akhon', 'ekhane',
            'okhane', 'ache', 'nei', 'hoy', 'hobe', 'kora', 'bola', 'dekha',
            'jete', 'ashe', 'jay', 'dekhun', 'bolchi', 'korchi', 'likhchi',
            'class', 'method', 'function', 'variable', 'object', 'create',
            'okay', 'right', 'now', 'see', 'look', 'basically', 'actually',
            'let', 'lets', 'going', 'like', 'get', 'make', 'use', 'using',
        }
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """
        Extract potential technical terms from text.
        
        Technical terms are:
        - CamelCase words (e.g., BinaryTree)
        - UPPERCASE words (e.g., RISC, OOP)
        - Words with numbers (e.g., UTF8)
        - Multi-word phrases with capital letters
        
        Args:
            text: Input text (transcript)
            
        Returns:
            List of potential technical terms
        """
        terms = []
        
        # Pattern 1: CamelCase (e.g., BinaryTree, LinkedList)
        camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
        terms.extend(camel_case)
        
        # Pattern 2: ALL CAPS words 2+ chars (e.g., OOP, API, RISC)
        upper_words = re.findall(r'\b[A-Z]{2,}\b', text)
        terms.extend(upper_words)
        
        # Pattern 3: Mixed case with numbers (e.g., UTF8, MP3)
        alphanumeric = re.findall(r'\b[A-Za-z]+[0-9]+[A-Za-z0-9]*\b|\b[0-9]+[A-Za-z]+[A-Za-z0-9]*\b', text)
        terms.extend(alphanumeric)
        
        # Pattern 4: Capitalized words (potential proper nouns/terms)
        capitalized = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
        for word in capitalized:
            if word.lower() not in self.stopwords:
                terms.append(word)
        
        # Pattern 5: Programming keywords often in transcripts
        programming_terms = [
            'int', 'string', 'void', 'public', 'private', 'static', 'class',
            'interface', 'extends', 'implements', 'return', 'null', 'true', 
            'false', 'new', 'this', 'super', 'import', 'package', 'final',
            'abstract', 'synchronized', 'volatile', 'native', 'throws',
        ]
        words = text.lower().split()
        for word in words:
            clean = re.sub(r'[^a-z]', '', word)
            if clean in programming_terms and len(clean) >= self.min_term_length:
                terms.append(clean)
        
        # Deduplicate while preserving order
        seen = set()
        unique_terms = []
        for term in terms:
            term_lower = term.lower()
            if term_lower not in seen and len(term) >= self.min_term_length:
                if term_lower not in self.stopwords:
                    seen.add(term_lower)
                    unique_terms.append(term)
        
        return unique_terms
    
    def _is_grounded(self, term: str, visual_context: List[str]) -> Tuple[bool, int, str]:
        """
        Check if a term is grounded in visual context.
        
        Args:
            term: Technical term from transcript
            visual_context: List of visual keywords from VLM
            
        Returns:
            Tuple of (is_grounded, best_score, matched_visual_term)
        """
        term_lower = term.lower()
        best_score = 0
        best_match = ""
        
        for visual_term in visual_context:
            visual_lower = visual_term.lower()
            
            # Exact match
            if term_lower == visual_lower:
                return True, 100, visual_term
            
            # Substring match (term in visual or visual in term)
            if term_lower in visual_lower or visual_lower in term_lower:
                return True, 95, visual_term
            
            # Fuzzy match
            score = fuzz.ratio(term_lower, visual_lower)
            if score > best_score:
                best_score = score
                best_match = visual_term
        
        is_grounded = best_score >= self.fuzzy_threshold
        return is_grounded, best_score, best_match
    
    def verify(
        self, 
        transcript: str, 
        visual_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Verify transcript against visual context.
        
        Args:
            transcript: ASR output text
            visual_keywords: List of keywords extracted by VLM
            
        Returns:
            Verification results with groundedness metrics
        """
        # Extract technical terms from transcript
        transcript_terms = self._extract_technical_terms(transcript)
        
        grounded = []
        ungrounded = []
        term_details = {}
        
        for term in transcript_terms:
            is_gr, score, match = self._is_grounded(term, visual_keywords)
            term_details[term] = {
                'is_grounded': is_gr,
                'score': score,
                'matched_to': match if is_gr else None
            }
            
            if is_gr:
                grounded.append(term)
            else:
                ungrounded.append(term)
        
        total = len(transcript_terms)
        groundedness = len(grounded) / total if total > 0 else 1.0
        hallucination_rate = 1.0 - groundedness
        
        return {
            'groundedness_score': groundedness,
            'hallucination_rate': hallucination_rate,
            'total_terms': total,
            'grounded_count': len(grounded),
            'ungrounded_count': len(ungrounded),
            'grounded_terms': grounded,
            'ungrounded_terms': ungrounded,
            'term_details': term_details,
            'visual_keywords_count': len(visual_keywords),
        }
    
    def compare_transcripts(
        self,
        baseline_transcript: str,
        biased_transcript: str,
        visual_keywords: List[str],
        baseline_name: str = "Standard Whisper",
        biased_name: str = "Visual-Biased Whisper"
    ) -> Dict[str, Any]:
        """
        Compare groundedness of two transcripts.
        
        Args:
            baseline_transcript: Transcript from standard Whisper
            biased_transcript: Transcript from visual-biased Whisper
            visual_keywords: List of visual keywords from VLM
            
        Returns:
            Comparison results
        """
        baseline_result = self.verify(baseline_transcript, visual_keywords)
        biased_result = self.verify(biased_transcript, visual_keywords)
        
        gs_improvement = biased_result['groundedness_score'] - baseline_result['groundedness_score']
        hr_reduction = baseline_result['hallucination_rate'] - biased_result['hallucination_rate']
        
        return {
            'baseline': baseline_result,
            'biased': biased_result,
            'groundedness_improvement': gs_improvement,
            'hallucination_reduction': hr_reduction,
            'baseline_name': baseline_name,
            'biased_name': biased_name,
        }
    
    def print_verification(self, result: Dict[str, Any]) -> None:
        """Pretty print verification results."""
        console.print(Panel.fit(
            f"[bold]Cross-Modal Verification Results[/bold]\n"
            f"Groundedness Score: {result['groundedness_score']:.1%}\n"
            f"Hallucination Rate: {result['hallucination_rate']:.1%}",
            border_style="green" if result['groundedness_score'] > 0.7 else "red"
        ))
        
        if result['grounded_terms']:
            console.print(f"\n[green]✓ Grounded Terms ({len(result['grounded_terms'])}):[/green]")
            for term in result['grounded_terms']:
                detail = result['term_details'][term]
                console.print(f"  • {term} ↔ {detail['matched_to']} (score: {detail['score']})")
        
        if result['ungrounded_terms']:
            console.print(f"\n[red]✗ Potential Hallucinations ({len(result['ungrounded_terms'])}):[/red]")
            for term in result['ungrounded_terms']:
                console.print(f"  • {term}")
    
    def print_comparison(self, comparison: Dict[str, Any]) -> None:
        """Pretty print comparison results."""
        baseline = comparison['baseline']
        biased = comparison['biased']
        
        table = Table(title="Cross-Modal Verification Comparison", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column(comparison['baseline_name'], style="yellow")
        table.add_column(comparison['biased_name'], style="green")
        
        table.add_row(
            "Groundedness Score",
            f"{baseline['groundedness_score']:.1%}",
            f"{biased['groundedness_score']:.1%}"
        )
        table.add_row(
            "Hallucination Rate",
            f"{baseline['hallucination_rate']:.1%}",
            f"{biased['hallucination_rate']:.1%}"
        )
        table.add_row(
            "Terms Checked",
            str(baseline['total_terms']),
            str(biased['total_terms'])
        )
        table.add_row(
            "Grounded Terms",
            str(baseline['grounded_count']),
            str(biased['grounded_count'])
        )
        table.add_row(
            "Ungrounded Terms",
            str(baseline['ungrounded_count']),
            str(biased['ungrounded_count'])
        )
        
        console.print(table)
        
        # Improvement summary
        hr_reduction = comparison['hallucination_reduction'] * 100
        if hr_reduction > 0:
            console.print(f"\n[bold green]✓ Hallucination Reduced by {hr_reduction:.1f}%[/bold green]")
        elif hr_reduction < 0:
            console.print(f"\n[bold red]✗ Hallucination Increased by {-hr_reduction:.1f}%[/bold red]")
        else:
            console.print(f"\n[bold yellow]→ No change in hallucination rate[/bold yellow]")


if __name__ == "__main__":
    # Test the verifier
    console.print(Panel.fit(
        "[bold]CrossModalVerifier Test[/bold]\n"
        "Demo: Detecting hallucinations via visual grounding",
        border_style="blue"
    ))
    
    # Visual context (what's on the whiteboard)
    visual_keywords = [
        "Java", "OOP", "Object-Oriented Programming",
        "class", "inheritance", "polymorphism"
    ]
    
    # Good transcript (grounded in visual context)
    good_transcript = """
    Today we learn about Java OOP concepts. 
    Object-Oriented Programming has four pillars.
    We discuss inheritance and polymorphism in class.
    """
    
    # Bad transcript (hallucinations)
    bad_transcript = """
    Today we learn about Python machine learning.
    TensorFlow has four neural network layers.
    We discuss gradient descent and backpropagation.
    """
    
    console.print(f"\n[bold]Visual Context:[/bold] {visual_keywords}")
    console.print(f"\n[green]Good Transcript:[/green] {good_transcript[:100]}...")
    console.print(f"[red]Bad Transcript:[/red] {bad_transcript[:100]}...")
    
    verifier = CrossModalVerifier()
    
    console.print("\n[bold]Good Transcript Verification:[/bold]")
    good_result = verifier.verify(good_transcript, visual_keywords)
    verifier.print_verification(good_result)
    
    console.print("\n[bold]Bad Transcript Verification:[/bold]")
    bad_result = verifier.verify(bad_transcript, visual_keywords)
    verifier.print_verification(bad_result)
    
    console.print("\n[bold]Comparison:[/bold]")
    comparison = verifier.compare_transcripts(
        bad_transcript, good_transcript, visual_keywords,
        "Hallucinating ASR", "Grounded ASR"
    )
    verifier.print_comparison(comparison)
