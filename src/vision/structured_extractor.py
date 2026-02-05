"""
=============================================================================
STRUCTURED VLM EXTRACTOR - Enhanced Whiteboard Content Extraction
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY 1: Structured Visual Content Extraction

IMPROVEMENT OVER BASIC OCR:
Instead of just extracting raw keywords, we categorize content into:
1. DEFINITIONS - Key concepts being defined
2. CODE_SNIPPETS - Java/Python code on whiteboard
3. FORMULAS - Mathematical expressions
4. DIAGRAMS - Diagram labels and annotations
5. EXAMPLES - Example data/values

This structured extraction enables:
- Better context for LLM summarization
- Automatic lecture outline generation
- Topic-aware content organization
=============================================================================
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class ContentType(Enum):
    """Types of whiteboard content."""
    DEFINITION = "definition"
    CODE = "code"
    FORMULA = "formula"
    DIAGRAM = "diagram"
    EXAMPLE = "example"
    KEYWORD = "keyword"  # Generic important term


@dataclass
class ExtractedContent:
    """A piece of extracted content with its type and metadata."""
    text: str
    content_type: ContentType
    confidence: float = 1.0
    frame_index: int = 0
    timestamp: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "type": self.content_type.value,
            "confidence": self.confidence,
            "frame_index": self.frame_index,
            "timestamp": self.timestamp,
        }


@dataclass
class StructuredExtraction:
    """Complete structured extraction from a video."""
    definitions: List[ExtractedContent] = field(default_factory=list)
    code_snippets: List[ExtractedContent] = field(default_factory=list)
    formulas: List[ExtractedContent] = field(default_factory=list)
    diagrams: List[ExtractedContent] = field(default_factory=list)
    examples: List[ExtractedContent] = field(default_factory=list)
    keywords: List[ExtractedContent] = field(default_factory=list)
    
    @property
    def total_items(self) -> int:
        return (len(self.definitions) + len(self.code_snippets) + 
                len(self.formulas) + len(self.diagrams) + 
                len(self.examples) + len(self.keywords))
    
    @property
    def all_keywords(self) -> List[str]:
        """Get flat list of all keywords for ASR biasing."""
        keywords = []
        for item in self.keywords:
            keywords.append(item.text)
        for item in self.definitions:
            # Extract key term from definition
            keywords.append(item.text.split(':')[0].strip() if ':' in item.text else item.text)
        for item in self.code_snippets:
            # Extract class/method names from code
            keywords.extend(re.findall(r'\b(?:class|void|public|private)\s+(\w+)', item.text))
        return list(dict.fromkeys(keywords))  # Deduplicate
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "definitions": [d.to_dict() for d in self.definitions],
            "code_snippets": [c.to_dict() for c in self.code_snippets],
            "formulas": [f.to_dict() for f in self.formulas],
            "diagrams": [d.to_dict() for d in self.diagrams],
            "examples": [e.to_dict() for e in self.examples],
            "keywords": [k.to_dict() for k in self.keywords],
            "summary": {
                "total_items": self.total_items,
                "definitions_count": len(self.definitions),
                "code_count": len(self.code_snippets),
                "formulas_count": len(self.formulas),
                "diagrams_count": len(self.diagrams),
                "examples_count": len(self.examples),
                "keywords_count": len(self.keywords),
            }
        }
    
    def to_context_string(self) -> str:
        """Format for LLM context."""
        parts = []
        
        if self.definitions:
            parts.append("## KEY DEFINITIONS")
            for d in self.definitions[:10]:
                parts.append(f"• {d.text}")
        
        if self.code_snippets:
            parts.append("\n## CODE SNIPPETS")
            for c in self.code_snippets[:5]:
                parts.append(f"```\n{c.text}\n```")
        
        if self.formulas:
            parts.append("\n## FORMULAS")
            for f in self.formulas[:5]:
                parts.append(f"• {f.text}")
        
        if self.keywords:
            parts.append("\n## TECHNICAL TERMS")
            terms = [k.text for k in self.keywords[:20]]
            parts.append(", ".join(terms))
        
        return "\n".join(parts)


class StructuredVLMExtractor:
    """
    Enhanced VLM extractor that categorizes whiteboard content.
    
    Uses pattern matching and heuristics to classify VLM output into:
    - Definitions (term: explanation patterns)
    - Code (syntax patterns, indentation)
    - Formulas (mathematical notation)
    - Diagrams (box/arrow descriptions)
    - Keywords (important standalone terms)
    """
    
    def __init__(self):
        # Patterns for content type detection
        self.definition_patterns = [
            r'^([A-Z][a-zA-Z]+)\s*[-:=]\s*(.+)$',  # Term: Definition
            r'^([A-Z][a-zA-Z]+)\s+is\s+(.+)$',      # Term is Definition
            r'^([A-Z][a-zA-Z]+)\s*→\s*(.+)$',       # Term → Definition
        ]
        
        self.code_patterns = [
            r'public\s+(?:class|void|static)',
            r'private\s+(?:class|void|static)',
            r'def\s+\w+\s*\(',
            r'class\s+\w+\s*[:{]',
            r'import\s+\w+',
            r'System\.out\.print',
            r'\w+\s*=\s*new\s+\w+',
        ]
        
        self.formula_patterns = [
            r'[a-zA-Z]\s*=\s*[a-zA-Z0-9+\-*/()]+',
            r'\d+\s*[+\-*/]\s*\d+',
            r'f\([^)]+\)\s*=',
            r'O\([^)]+\)',  # Big-O notation
            r'∑|∏|∫|√',     # Math symbols
        ]
        
        self.diagram_patterns = [
            r'→|←|↑|↓|↔',   # Arrows
            r'\[.*\].*→',    # Box diagrams
            r'Box\s*\d+',
            r'Node\s*\d+',
        ]
        
        # Programming keywords to extract
        self.programming_keywords = {
            'class', 'object', 'method', 'function', 'variable',
            'public', 'private', 'static', 'void', 'int', 'string',
            'array', 'list', 'loop', 'if', 'else', 'return',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'constructor', 'instance', 'reference', 'memory', 'heap', 'stack',
        }
    
    def _classify_content(self, text: str) -> ContentType:
        """Classify a piece of text into a content type."""
        text_lower = text.lower()
        
        # Check for code
        for pattern in self.code_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return ContentType.CODE
        
        # Check for formula
        for pattern in self.formula_patterns:
            if re.search(pattern, text):
                return ContentType.FORMULA
        
        # Check for definition
        for pattern in self.definition_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return ContentType.DEFINITION
        
        # Check for diagram
        for pattern in self.diagram_patterns:
            if re.search(pattern, text):
                return ContentType.DIAGRAM
        
        # Default to keyword
        return ContentType.KEYWORD
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        keywords = []
        
        # CamelCase words (e.g., BinaryTree, LinkedList)
        keywords.extend(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text))
        
        # ALL CAPS words (e.g., OOP, API)
        keywords.extend(re.findall(r'\b[A-Z]{2,}\b', text))
        
        # Capitalized words (potential terms)
        for word in re.findall(r'\b[A-Z][a-z]{2,}\b', text):
            if word.lower() not in {'the', 'this', 'that', 'with', 'from', 'they', 'have', 'will'}:
                keywords.append(word)
        
        # Programming keywords
        words = set(text.lower().split())
        for kw in self.programming_keywords:
            if kw in words:
                keywords.append(kw.title())
        
        return list(dict.fromkeys(keywords))
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code-like sections from text."""
        code_blocks = []
        
        lines = text.split('\n')
        current_block = []
        in_code = False
        
        for line in lines:
            is_code_line = any(
                re.search(p, line, re.IGNORECASE) 
                for p in self.code_patterns
            )
            
            if is_code_line or (in_code and line.strip().startswith((' ', '\t', '}', ')'))):
                current_block.append(line)
                in_code = True
            else:
                if current_block:
                    code_blocks.append('\n'.join(current_block))
                    current_block = []
                in_code = False
        
        if current_block:
            code_blocks.append('\n'.join(current_block))
        
        return code_blocks
    
    def _extract_definitions(self, text: str) -> List[tuple]:
        """Extract term: definition pairs."""
        definitions = []
        
        for pattern in self.definition_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    term, definition = match[0], match[1]
                    if len(term) > 1 and len(definition) > 5:
                        definitions.append((term, f"{term}: {definition}"))
        
        return definitions
    
    def extract_from_vlm_output(
        self,
        vlm_text: str,
        frame_index: int = 0,
        timestamp: float = 0.0,
    ) -> StructuredExtraction:
        """
        Process VLM output and extract structured content.
        
        Args:
            vlm_text: Raw text from VLM analysis
            frame_index: Index of the frame
            timestamp: Timestamp in seconds
            
        Returns:
            StructuredExtraction with categorized content
        """
        result = StructuredExtraction()
        
        if not vlm_text or len(vlm_text) < 10:
            return result
        
        # Extract definitions
        for term, full_def in self._extract_definitions(vlm_text):
            result.definitions.append(ExtractedContent(
                text=full_def,
                content_type=ContentType.DEFINITION,
                frame_index=frame_index,
                timestamp=timestamp,
            ))
        
        # Extract code blocks
        for code in self._extract_code_blocks(vlm_text):
            if len(code) > 20:
                result.code_snippets.append(ExtractedContent(
                    text=code,
                    content_type=ContentType.CODE,
                    frame_index=frame_index,
                    timestamp=timestamp,
                ))
        
        # Extract keywords
        for keyword in self._extract_keywords(vlm_text):
            if len(keyword) >= 2:
                result.keywords.append(ExtractedContent(
                    text=keyword,
                    content_type=ContentType.KEYWORD,
                    frame_index=frame_index,
                    timestamp=timestamp,
                ))
        
        return result
    
    def merge_extractions(self, extractions: List[StructuredExtraction]) -> StructuredExtraction:
        """Merge multiple frame extractions into one."""
        merged = StructuredExtraction()
        
        seen_definitions = set()
        seen_code = set()
        seen_keywords = set()
        
        for ext in extractions:
            for d in ext.definitions:
                key = d.text.lower()[:50]
                if key not in seen_definitions:
                    seen_definitions.add(key)
                    merged.definitions.append(d)
            
            for c in ext.code_snippets:
                key = c.text[:100]
                if key not in seen_code:
                    seen_code.add(key)
                    merged.code_snippets.append(c)
            
            for k in ext.keywords:
                key = k.text.lower()
                if key not in seen_keywords:
                    seen_keywords.add(key)
                    merged.keywords.append(k)
            
            merged.formulas.extend(ext.formulas)
            merged.diagrams.extend(ext.diagrams)
            merged.examples.extend(ext.examples)
        
        return merged
    
    def print_summary(self, extraction: StructuredExtraction) -> None:
        """Pretty print extraction summary."""
        console.print(Panel.fit(
            f"[bold]Structured VLM Extraction Summary[/bold]\n"
            f"Total items: {extraction.total_items}",
            border_style="green"
        ))
        
        table = Table(title="Content Categories", show_header=True)
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Sample", style="white", max_width=40)
        
        categories = [
            ("Definitions", extraction.definitions),
            ("Code Snippets", extraction.code_snippets),
            ("Formulas", extraction.formulas),
            ("Keywords", extraction.keywords),
        ]
        
        for name, items in categories:
            sample = items[0].text[:40] + "..." if items else "None"
            table.add_row(name, str(len(items)), sample)
        
        console.print(table)


if __name__ == "__main__":
    # Test the structured extractor
    console.print(Panel.fit(
        "[bold]Structured VLM Extractor Test[/bold]",
        border_style="blue"
    ))
    
    # Sample VLM output
    sample_vlm_output = """
    Java Object-Oriented Programming
    
    Class: A blueprint for creating objects
    Object: An instance of a class
    
    public class Student {
        public String name;
        public int id;
    }
    
    Student s1 = new Student();
    
    OOP Pillars:
    - Encapsulation
    - Inheritance
    - Polymorphism
    - Abstraction
    
    Memory: Stack vs Heap
    Reference → Object in Heap
    """
    
    extractor = StructuredVLMExtractor()
    result = extractor.extract_from_vlm_output(sample_vlm_output)
    extractor.print_summary(result)
    
    console.print("\n[bold]All Keywords for ASR:[/bold]")
    console.print(result.all_keywords)
