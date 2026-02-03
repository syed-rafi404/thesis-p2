"""
=============================================================================
LECTURE NOTE QUALITY EVALUATOR - Measurable Metrics for Output Quality
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY 3: Quality Metrics for Lecture Notes

METRICS:
1. CONTENT COVERAGE - How many visual keywords appear in notes
2. STRUCTURE QUALITY - Presence of headings, lists, code blocks
3. INFORMATION DENSITY - Unique terms per paragraph
4. COMPLETENESS - Coverage of different content types

These metrics provide quantitative evaluation of generated lecture notes,
enabling comparison between different summarization approaches.
=============================================================================
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from thefuzz import fuzz

console = Console()


@dataclass
class QualityMetrics:
    """Quality metrics for lecture notes."""
    # Content Coverage
    keyword_coverage: float      # % of visual keywords in notes
    keywords_found: int
    keywords_total: int
    
    # Structure Quality
    has_headings: bool
    heading_count: int
    has_lists: bool
    list_item_count: int
    has_code_blocks: bool
    code_block_count: int
    
    # Information Density
    word_count: int
    unique_word_count: int
    lexical_diversity: float     # unique_words / total_words
    avg_paragraph_length: float
    
    # Completeness
    paragraph_count: int
    section_count: int
    
    # Overall Score (0-100)
    overall_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content_coverage": {
                "keyword_coverage": self.keyword_coverage,
                "keywords_found": self.keywords_found,
                "keywords_total": self.keywords_total,
            },
            "structure_quality": {
                "has_headings": self.has_headings,
                "heading_count": self.heading_count,
                "has_lists": self.has_lists,
                "list_item_count": self.list_item_count,
                "has_code_blocks": self.has_code_blocks,
                "code_block_count": self.code_block_count,
            },
            "information_density": {
                "word_count": self.word_count,
                "unique_word_count": self.unique_word_count,
                "lexical_diversity": self.lexical_diversity,
                "avg_paragraph_length": self.avg_paragraph_length,
            },
            "completeness": {
                "paragraph_count": self.paragraph_count,
                "section_count": self.section_count,
            },
            "overall_score": self.overall_score,
        }


class LectureNoteEvaluator:
    """
    Evaluates quality of generated lecture notes.
    
    Provides quantitative metrics for:
    - How well the notes cover the source content
    - Structural quality (organization, formatting)
    - Information density and diversity
    """
    
    def __init__(self, fuzzy_threshold: int = 80):
        """
        Initialize the evaluator.
        
        Args:
            fuzzy_threshold: Minimum fuzzy match score for keyword matching
        """
        self.fuzzy_threshold = fuzzy_threshold
    
    def _count_keywords_found(
        self, 
        notes: str, 
        keywords: List[str]
    ) -> tuple[int, List[str]]:
        """Count how many keywords appear in the notes."""
        found = []
        notes_lower = notes.lower()
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            
            # Exact match
            if kw_lower in notes_lower:
                found.append(keyword)
                continue
            
            # Fuzzy match
            score = fuzz.partial_ratio(kw_lower, notes_lower)
            if score >= self.fuzzy_threshold:
                found.append(keyword)
        
        return len(found), found
    
    def _analyze_structure(self, notes: str) -> Dict[str, Any]:
        """Analyze structural elements in the notes."""
        # Count headings (# ## ### etc.)
        headings = re.findall(r'^#{1,6}\s+.+$', notes, re.MULTILINE)
        
        # Count list items (- * 1. etc.)
        list_items = re.findall(r'^[\s]*[-*•]\s+.+$|^[\s]*\d+\.\s+.+$', notes, re.MULTILINE)
        
        # Count code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', notes)
        inline_code = re.findall(r'`[^`]+`', notes)
        
        # Count bold/italic text
        bold_text = re.findall(r'\*\*[^*]+\*\*', notes)
        
        return {
            'headings': headings,
            'heading_count': len(headings),
            'list_items': list_items,
            'list_count': len(list_items),
            'code_blocks': code_blocks,
            'code_block_count': len(code_blocks),
            'inline_code_count': len(inline_code),
            'bold_count': len(bold_text),
        }
    
    def _analyze_density(self, notes: str) -> Dict[str, Any]:
        """Analyze information density."""
        # Extract words
        words = re.findall(r'\b\w+\b', notes.lower())
        unique_words = set(words)
        
        # Count paragraphs (separated by blank lines)
        paragraphs = re.split(r'\n\s*\n', notes)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        # Calculate metrics
        word_count = len(words)
        unique_count = len(unique_words)
        lexical_diversity = unique_count / max(1, word_count)
        
        avg_para_length = sum(len(p.split()) for p in paragraphs) / max(1, len(paragraphs))
        
        return {
            'word_count': word_count,
            'unique_word_count': unique_count,
            'lexical_diversity': lexical_diversity,
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': avg_para_length,
        }
    
    def _calculate_overall_score(
        self,
        keyword_coverage: float,
        structure: Dict[str, Any],
        density: Dict[str, Any],
    ) -> float:
        """Calculate overall quality score (0-100)."""
        # Content Coverage Score (40% weight)
        coverage_score = keyword_coverage * 40
        
        # Structure Score (30% weight)
        structure_score = 0
        if structure['heading_count'] > 0:
            structure_score += 10  # Has organization
        if structure['heading_count'] >= 3:
            structure_score += 5   # Multiple sections
        if structure['list_count'] > 0:
            structure_score += 10  # Uses lists
        if structure['code_block_count'] > 0:
            structure_score += 5   # Has code examples
        structure_score = min(30, structure_score)
        
        # Density Score (30% weight)
        density_score = 0
        
        # Lexical diversity (0.3-0.7 is good)
        ld = density['lexical_diversity']
        if 0.3 <= ld <= 0.7:
            density_score += 10
        elif 0.2 <= ld <= 0.8:
            density_score += 5
        
        # Word count (at least 200 words is reasonable)
        wc = density['word_count']
        if wc >= 500:
            density_score += 10
        elif wc >= 200:
            density_score += 5
        
        # Paragraph structure
        if density['paragraph_count'] >= 3:
            density_score += 10
        elif density['paragraph_count'] >= 2:
            density_score += 5
        
        density_score = min(30, density_score)
        
        return coverage_score + structure_score + density_score
    
    def evaluate(
        self,
        notes: str,
        visual_keywords: List[str],
    ) -> QualityMetrics:
        """
        Evaluate lecture notes quality.
        
        Args:
            notes: Generated lecture notes (Markdown)
            visual_keywords: Keywords extracted from whiteboard
            
        Returns:
            QualityMetrics with all evaluation results
        """
        # Content Coverage
        keywords_found, found_list = self._count_keywords_found(notes, visual_keywords)
        keywords_total = len(visual_keywords)
        keyword_coverage = keywords_found / max(1, keywords_total)
        
        # Structure Analysis
        structure = self._analyze_structure(notes)
        
        # Density Analysis
        density = self._analyze_density(notes)
        
        # Section count (based on h1/h2 headings)
        section_count = len([h for h in structure['headings'] if h.startswith('# ') or h.startswith('## ')])
        
        # Overall Score
        overall_score = self._calculate_overall_score(keyword_coverage, structure, density)
        
        return QualityMetrics(
            keyword_coverage=keyword_coverage,
            keywords_found=keywords_found,
            keywords_total=keywords_total,
            has_headings=structure['heading_count'] > 0,
            heading_count=structure['heading_count'],
            has_lists=structure['list_count'] > 0,
            list_item_count=structure['list_count'],
            has_code_blocks=structure['code_block_count'] > 0,
            code_block_count=structure['code_block_count'],
            word_count=density['word_count'],
            unique_word_count=density['unique_word_count'],
            lexical_diversity=density['lexical_diversity'],
            avg_paragraph_length=density['avg_paragraph_length'],
            paragraph_count=density['paragraph_count'],
            section_count=section_count,
            overall_score=overall_score,
        )
    
    def print_metrics(self, metrics: QualityMetrics) -> None:
        """Pretty print quality metrics."""
        # Determine quality level
        if metrics.overall_score >= 70:
            quality = "[bold green]GOOD[/bold green]"
            border = "green"
        elif metrics.overall_score >= 50:
            quality = "[bold yellow]FAIR[/bold yellow]"
            border = "yellow"
        else:
            quality = "[bold red]NEEDS IMPROVEMENT[/bold red]"
            border = "red"
        
        console.print(Panel.fit(
            f"[bold]Lecture Note Quality Assessment[/bold]\n"
            f"Overall Score: {metrics.overall_score:.1f}/100 - {quality}",
            border_style=border
        ))
        
        # Content Coverage Table
        table1 = Table(title="Content Coverage", show_header=True)
        table1.add_column("Metric", style="cyan")
        table1.add_column("Value", style="green")
        
        table1.add_row("Keyword Coverage", f"{metrics.keyword_coverage*100:.1f}%")
        table1.add_row("Keywords Found", f"{metrics.keywords_found} / {metrics.keywords_total}")
        
        console.print(table1)
        
        # Structure Table
        table2 = Table(title="Structure Quality", show_header=True)
        table2.add_column("Element", style="cyan")
        table2.add_column("Present", style="green")
        table2.add_column("Count", style="yellow")
        
        table2.add_row("Headings", "✓" if metrics.has_headings else "✗", str(metrics.heading_count))
        table2.add_row("Lists", "✓" if metrics.has_lists else "✗", str(metrics.list_item_count))
        table2.add_row("Code Blocks", "✓" if metrics.has_code_blocks else "✗", str(metrics.code_block_count))
        table2.add_row("Sections", "-", str(metrics.section_count))
        
        console.print(table2)
        
        # Density Table
        table3 = Table(title="Information Density", show_header=True)
        table3.add_column("Metric", style="cyan")
        table3.add_column("Value", style="green")
        
        table3.add_row("Word Count", str(metrics.word_count))
        table3.add_row("Unique Words", str(metrics.unique_word_count))
        table3.add_row("Lexical Diversity", f"{metrics.lexical_diversity:.2f}")
        table3.add_row("Paragraphs", str(metrics.paragraph_count))
        table3.add_row("Avg Paragraph Length", f"{metrics.avg_paragraph_length:.1f} words")
        
        console.print(table3)


def compare_notes(
    notes1: str,
    notes2: str,
    visual_keywords: List[str],
    name1: str = "Method A",
    name2: str = "Method B",
) -> Dict[str, Any]:
    """Compare quality of two different lecture note outputs."""
    evaluator = LectureNoteEvaluator()
    
    metrics1 = evaluator.evaluate(notes1, visual_keywords)
    metrics2 = evaluator.evaluate(notes2, visual_keywords)
    
    console.print(Panel.fit(
        f"[bold]Comparing: {name1} vs {name2}[/bold]",
        border_style="blue"
    ))
    
    table = Table(title="Quality Comparison", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column(name1, style="yellow")
    table.add_column(name2, style="green")
    table.add_column("Winner", style="magenta")
    
    comparisons = [
        ("Overall Score", metrics1.overall_score, metrics2.overall_score),
        ("Keyword Coverage", metrics1.keyword_coverage * 100, metrics2.keyword_coverage * 100),
        ("Headings", metrics1.heading_count, metrics2.heading_count),
        ("List Items", metrics1.list_item_count, metrics2.list_item_count),
        ("Word Count", metrics1.word_count, metrics2.word_count),
        ("Lexical Diversity", metrics1.lexical_diversity, metrics2.lexical_diversity),
    ]
    
    for name, v1, v2 in comparisons:
        winner = name1 if v1 > v2 else name2 if v2 > v1 else "Tie"
        table.add_row(name, f"{v1:.1f}", f"{v2:.1f}", winner)
    
    console.print(table)
    
    return {
        name1: metrics1.to_dict(),
        name2: metrics2.to_dict(),
        "winner": name1 if metrics1.overall_score > metrics2.overall_score else name2,
    }


if __name__ == "__main__":
    # Test the evaluator
    console.print(Panel.fit(
        "[bold]Lecture Note Quality Evaluator Test[/bold]",
        border_style="blue"
    ))
    
    # Sample lecture notes
    sample_notes = """
# Java Object-Oriented Programming

## Introduction

Today we will learn about Java OOP concepts. Object-Oriented Programming (OOP) 
is a programming paradigm that organizes code around objects rather than functions.

## Key Concepts

### Classes and Objects

- **Class**: A blueprint for creating objects
- **Object**: An instance of a class
- **Constructor**: Special method to initialize objects

### Example Code

```java
public class Student {
    public String name;
    public int id;
}
```

### OOP Pillars

1. Encapsulation - Bundling data and methods
2. Inheritance - Classes can extend other classes
3. Polymorphism - Multiple forms of behavior
4. Abstraction - Hiding implementation details

## Memory Management

Objects are stored in the heap memory. Reference variables hold the memory address.

```java
Student s1 = new Student();  // Creates object in heap
```
"""
    
    # Sample visual keywords
    keywords = [
        "Java", "OOP", "Class", "Object", "Student",
        "Encapsulation", "Inheritance", "Polymorphism", "Abstraction",
        "Constructor", "Memory", "Heap", "Reference", "String", "Blueprint"
    ]
    
    evaluator = LectureNoteEvaluator()
    metrics = evaluator.evaluate(sample_notes, keywords)
    evaluator.print_metrics(metrics)
