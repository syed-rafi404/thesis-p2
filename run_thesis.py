"""
=============================================================================
MULTIMODAL BANGLISH CLASSROOM SUMMARIZER - Master Orchestration
=============================================================================
Master's Thesis Demo - Main Entry Point

This script demonstrates all 3 research novelties working together:

1. **Novelty 1: Visual-Biased ASR**
   - Extracts keywords from whiteboard using VLM
   - Biases Whisper's logits toward these terms during transcription
   - Improves Technical Term Recall (TTR)

2. **Novelty 2: Spatio-Temporal Gaze Tracking**
   - Detects when lecturer points at specific whiteboard terms
   - Creates temporal annotations: "Focused on 'A*' at 10.5s"
   - Enables attention-weighted summarization

3. **Novelty 3: Multimodal Fusion**
   - Combines audio transcript + visual context + gaze events
   - Generates comprehensive lecture notes via LLM

Pipeline Flow:
    lecture.mp4 ──┬── [Audio] ── Whisper+VisualBias ── Transcript
                  │
                  └── [Video] ──┬── VLM ── Keywords & Text Boxes
                                │
                                └── YOLOv8-Pose ── Gaze Events
                                         │
                                         ▼
                              Evaluation (TTR Improvement)
=============================================================================
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

# ============================================================================
# IMPORTS - All thesis modules
# ============================================================================

from src.ingest_video import VideoIngestor
from src.audio.transcriber import BanglishTranscriber
from src.audio.transcriber_specialized import BanglaASRTranscriber
from src.audio.dual_asr_fusion_transliterate import DualASRFusionTransliterate  # NOVELTY 2: Transliteration Fusion
from src.vision.whiteboard_ocr import WhiteboardVLM
from src.vision.structured_extractor import StructuredVLMExtractor, StructuredExtraction  # NOVELTY 1
from src.research.gaze_tracker import GazeTracker
from src.evaluation.evaluator import BanglishEvaluator
from src.evaluation.cross_modal_verifier import CrossModalVerifier
from src.evaluation.quality_evaluator import LectureNoteEvaluator, QualityMetrics  # NOVELTY 3
from src.summarizer.generator import LectureNoteGenerator
from src.model_registry import get_registry
from src.fusion.temporal_context import TemporalVisualContext


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class GazeEvent:
    """Record of a pointing gesture toward a term."""
    timestamp: float
    term: str
    confidence: float


@dataclass
class PipelineResult:
    """Complete result from the thesis pipeline."""
    # Track A: Audio (Dual ASR + Fusion)
    transcript_whisper: str = ""           # Whisper with visual bias
    transcript_whisper_baseline: str = ""  # Whisper without bias
    transcript_bangla: str = ""            # BanglaASR for Bengali parts
    transcript_fused: str = ""             # NOVELTY 2: Fused transcript
    
    # NOVELTY 2: Transliteration Fusion Metrics
    fusion_unique_bengali_words: int = 0   # Unique words from BanglaASR
    fusion_avg_similarity: float = 0.0     # Average transliteration similarity
    fusion_merged_segments: int = 0        # Successfully merged segments
    fusion_total_segments: int = 0         # Total whisper segments
    
    # Track B: Vision (Structured Extraction)
    visual_keywords: List[str] = field(default_factory=list)  # Flat list (backward compat)
    structured_extraction: Optional['StructuredExtraction'] = None  # NOVELTY 1
    temporal_context: Optional['TemporalVisualContext'] = None
    text_boxes: List[Dict[str, Any]] = field(default_factory=list)
    gaze_events: List[GazeEvent] = field(default_factory=list)
    
    # Track C: Evaluation
    ttr_improvement: float = 0.0
    evaluation_details: Dict[str, Any] = field(default_factory=dict)
    quality_metrics: Optional['QualityMetrics'] = None  # NOVELTY 3
    
    # Track D: Final Output
    final_lecture_notes: str = ""         # LLM-generated notes
    
    # Metadata
    processing_time: float = 0.0
    video_duration: float = 0.0


# ============================================================================
# THESIS PIPELINE ORCHESTRATOR
# ============================================================================

class ThesisPipeline:
    """
    Master orchestrator for the Multimodal Banglish Classroom Summarizer.
    
    Coordinates all components:
    - VideoIngestor: Extract audio and frames
    - WhiteboardVLM: Extract text from whiteboard
    - GazeTracker: Detect pointing gestures
    - BanglishTranscriber: Transcribe with visual bias
    - BanglishEvaluator: Measure improvement
    """
    
    def __init__(
        self,
        video_path: str,
        output_dir: str = "output/thesis_run",
        frame_interval: int = 30,
        use_mock_vlm: bool = False,
        skip_gaze: bool = False,
        live_mode: bool = False,  # Enable live-optimized configuration
    ):
        """
        Initialize the thesis pipeline.
        
        Args:
            video_path: Path to lecture video
            output_dir: Directory for all outputs
            frame_interval: Extract frame every N seconds
            use_mock_vlm: Use mock data instead of real VLM (faster testing)
            skip_gaze: Skip gaze tracking (faster testing)
            live_mode: If True, use 4-bit quantized LLM to fit all models in 24GB VRAM
        """
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.frame_interval = frame_interval
        self.use_mock_vlm = use_mock_vlm
        self.skip_gaze = skip_gaze
        self.live_mode = live_mode
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components (lazy loading)
        self.ingestor: Optional[VideoIngestor] = None
        self.vlm: Optional[WhiteboardVLM] = None
        self.gaze_tracker: Optional[GazeTracker] = None
        self.transcriber: Optional[BanglishTranscriber] = None
        self.evaluator: Optional[BanglishEvaluator] = None
        
    def _print_banner(self):
        """Print the thesis banner."""
        mode_str = "[yellow]LIVE MODE (4-bit LLM)[/yellow]" if self.live_mode else "[green]BATCH MODE (FP16)[/green]"
        banner = f"""
[bold cyan]╔══════════════════════════════════════════════════════════════════════╗
║     MULTIMODAL BANGLISH CLASSROOM SUMMARIZER                         ║
║     Master's Thesis - Full Pipeline Demo                             ║
╠══════════════════════════════════════════════════════════════════════╣
║  Novelty 1: Structured VLM Whiteboard Extraction                     ║
║  Novelty 2: Smart Dual-ASR Fusion (Whisper + BanglaASR)              ║
║  Novelty 3: Quality-Evaluated Multimodal Summarization               ║
╚══════════════════════════════════════════════════════════════════════╝[/bold cyan]
        Mode: {mode_str}
        """
        console.print(banner)
        
    def run(self) -> PipelineResult:
        """
        Run the complete thesis pipeline.
        
        Returns:
            PipelineResult with all outputs and metrics
        """
        self._print_banner()
        start_time = time.time()
        
        # ================================================================
        # STEP 1: VIDEO INGESTION
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 1: Video Ingestion[/bold]\n"
            "Extracting audio and frames from lecture video",
            border_style="blue"
        ))
        
        self.ingestor = VideoIngestor(
            output_dir=str(self.output_dir / "ingested"),
        )
        
        ingest_result = self.ingestor.process(
            video_path=str(self.video_path),
            frame_interval=self.frame_interval,
        )
        audio_path = ingest_result.audio_path
        frame_paths = [f.frame_path for f in ingest_result.frames]
        video_duration = ingest_result.duration
        
        console.print(f"[green]✓ Extracted:[/green] {len(frame_paths)} frames, audio file")
        console.print(f"[dim]  Duration: {video_duration:.1f}s[/dim]\n")
        
        # ================================================================
        # STEP 2: VISION TRACK (Track B) - NOW WITH TEMPORAL ALIGNMENT
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 2: Vision Track (Whiteboard + Gaze)[/bold]\n"
            "VLM extracts text WITH TEMPORAL ALIGNMENT\n"
            "[cyan]NOVELTY: Keywords mapped to frame timestamps[/cyan]",
            border_style="green"
        ))
        
        # Returns TemporalVisualContext + StructuredExtraction (NOVELTY 1)
        temporal_context, structured_extraction, text_boxes = self._run_vision_track(frame_paths)
        visual_keywords_raw = temporal_context.all_keywords  # Flat list for backward compat
        gaze_events = self._run_gaze_tracking(frame_paths, text_boxes)
        
        # NOVELTY IMPROVEMENT: Filter keywords for better bias consistency
        from src.audio.visual_bias_processor import filter_keywords_for_bias
        visual_keywords, filter_stats = filter_keywords_for_bias(
            keywords=visual_keywords_raw,
            min_length=3,
            min_occurrences=1,
            exclude_single_chars=True,
            technical_terms_boost=True,
        )
        
        console.print(f"[green]✓ Raw Visual Keywords:[/green] {len(visual_keywords_raw)} extracted")
        console.print(f"[green]✓ Filtered Keywords:[/green] {len(visual_keywords)} kept ({filter_stats['removed_count']} removed)")
        console.print(f"[dim]  Top filtered: {filter_stats['top_keywords'][:8]}[/dim]")
        console.print(f"[green]✓ Temporal Frames:[/green] {len(temporal_context)} with keyword mappings")
        console.print(f"[green]✓ Structured Extraction:[/green] {len(structured_extraction.definitions)} defs, {len(structured_extraction.code_snippets)} code, {len(structured_extraction.keywords)} keywords")
        console.print(f"[green]✓ Text Boxes:[/green] {len(text_boxes)} detected")
        console.print(f"[green]✓ Gaze Events:[/green] {len(gaze_events)} pointing gestures\n")
        
        # Free VLM GPU memory before loading Whisper (force registry unload)
        console.print("[dim]  Unloading VLM to free VRAM for Whisper...[/dim]")
        registry = get_registry()
        registry.unload("vlm")  # Force unload from registry
        self.vlm = None
        
        # Print gaze events
        if gaze_events:
            console.print("[bold]Detected Pointing Gestures:[/bold]")
            for event in gaze_events[:5]:  # Show first 5
                console.print(f"  → [cyan]{event.term}[/cyan] at {event.timestamp:.1f}s (conf: {event.confidence:.2f})")
            if len(gaze_events) > 5:
                console.print(f"  ... and {len(gaze_events) - 5} more")
            console.print()
        
        # ================================================================
        # STEP 3: AUDIO TRACK (Track A) - TRIPLE ASR COMPARISON
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 3: Audio Track (Triple ASR Comparison)[/bold]\n"
            "Fair A/B/C test: All use generate() method\n"
            "[cyan]A: No Bias | B: Global Bias (Filtered) | C: Temporal Bias[/cyan]",
            border_style="yellow"
        ))
        
        # STEP 3A: Whisper Baseline (NO visual bias, generate mode)
        console.print("[bold cyan]3A. Whisper Baseline (no bias, generate mode)[/bold cyan]")
        transcript_whisper_baseline = self._run_transcription_generate(
            audio_path, 
            visual_keywords=None  # No bias!
        )
        
        # STEP 3B: Whisper with GLOBAL Visual-bias (FILTERED keywords)
        console.print("[bold cyan]3B. Whisper Global Visual-Biased (filtered keywords)[/bold cyan]")
        transcript_whisper_global = self._run_transcription_generate(
            audio_path, 
            visual_keywords=visual_keywords  # FILTERED keywords for bias
        )
        
        # STEP 3C: Whisper with TEMPORAL Visual-bias (time-aligned keywords)
        console.print("[bold cyan]3C. Whisper Temporal Visual-Biased (NOVELTY)[/bold cyan]")
        transcript_whisper_temporal = self._run_transcription(
            audio_path, 
            temporal_context=temporal_context  # Time-aligned keywords
        )
        
        # STEP 3D: BanglaASR for Bengali recognition
        console.print("[bold cyan]3D. BanglaASR (Bengali Specialized)[/bold cyan]")
        transcript_bangla = self._run_bangla_transcription(audio_path)
        
        # STEP 3E: NOVELTY 2 - Transliteration-Based Dual-ASR Fusion
        console.print("[bold cyan]3E. Transliteration Dual-ASR Fusion (NOVELTY 2)[/bold cyan]")
        dual_asr = DualASRFusionTransliterate()
        fusion_result = dual_asr.fuse(
            whisper_transcript=transcript_whisper_temporal,
            bangla_transcript=transcript_bangla
        )
        transcript_fused = fusion_result.fused_transcript
        
        console.print(f"[green]✓ All transcriptions complete[/green]")
        console.print(f"[dim]  Baseline (no bias):    {len(transcript_whisper_baseline)} chars[/dim]")
        console.print(f"[dim]  Global bias:           {len(transcript_whisper_global)} chars[/dim]")
        console.print(f"[dim]  Temporal bias:         {len(transcript_whisper_temporal)} chars[/dim]")
        console.print(f"[dim]  BanglaASR:             {len(transcript_bangla)} chars[/dim]")
        console.print(f"[bold green]  Transliteration Fusion: {len(transcript_fused)} chars[/bold green]")
        console.print(f"[bold yellow]  ├── Unique Bengali words: {fusion_result.unique_words_from_bangla}[/bold yellow]")
        console.print(f"[bold yellow]  ├── Avg similarity:       {fusion_result.average_similarity:.1%}[/bold yellow]")
        console.print(f"[bold yellow]  ├── Merged segments:      {fusion_result.merged_segments}/{fusion_result.whisper_segments}[/bold yellow]")
        console.print(f"[bold cyan]  ├── Avg Confidence:      {fusion_result.average_confidence:.0%}[/bold cyan]")
        console.print(f"[bold cyan]  ├── High-conf segments:  {fusion_result.high_confidence_segments}[/bold cyan]")
        console.print(f"[bold red]  └── Needs review:        {fusion_result.segments_needing_review}[/bold red]\n")
        
        # Use FUSED transcript as the main output for summarization (NOVELTY 2)
        transcript_whisper = transcript_whisper_temporal  # For evaluation
        transcript_for_summary = transcript_fused  # For LLM summarization
        
        # ================================================================
        # STEP 4: EVALUATION (Track C) - 3-WAY COMPARISON
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 4: Evaluation (3-Way TTR Comparison)[/bold]\n"
            "Measuring: Baseline vs Global vs Temporal",
            border_style="magenta"
        ))
        
        self.evaluator = BanglishEvaluator(fuzzy_threshold=85)
        
        # Use visual keywords as ground truth
        ground_truth = visual_keywords[:20]  # Top 20 terms
        
        # 3-WAY COMPARISON: Baseline vs Global vs Temporal
        comparison = self._run_3way_evaluation(
            ground_truth=ground_truth,
            baseline_transcript=transcript_whisper_baseline,
            global_transcript=transcript_whisper_global,
            temporal_transcript=transcript_whisper_temporal,
        )
        
        # ================================================================
        # STEP 5: LLM SUMMARIZATION (Track D) - MULTIMODAL FUSION
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 5: LLM Summarization (Multimodal Fusion)[/bold]\n"
            "Using: Fused Transcript + Structured VLM Context (NOVELTY 1+2)",
            border_style="cyan"
        ))
        
        # Use structured context for richer LLM prompt
        structured_context = structured_extraction.to_context_string()
        
        final_lecture_notes = self._generate_lecture_notes(
            transcript_whisper=transcript_for_summary,  # Use FUSED transcript
            transcript_bangla=transcript_bangla,
            visual_keywords=visual_keywords,
            gaze_events=gaze_events,
            structured_context=structured_context,  # NEW: Structured VLM content
        )
        
        # ================================================================
        # STEP 5B: QUALITY EVALUATION (NOVELTY 3)
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 5B: Quality Evaluation (NOVELTY 3)[/bold]\n"
            "Measuring: Coverage, Structure, Information Density",
            border_style="yellow"
        ))
        
        quality_evaluator = LectureNoteEvaluator()
        quality_metrics = quality_evaluator.evaluate(
            notes=final_lecture_notes,
            visual_keywords=visual_keywords,
        )
        
        console.print(f"[green]✓ Quality Score: {quality_metrics.overall_score:.1f}/100[/green]")
        console.print(f"[dim]  Keyword Coverage: {quality_metrics.keyword_coverage*100:.0f}%[/dim]")
        console.print(f"[dim]  Lexical Diversity: {quality_metrics.lexical_diversity*100:.0f}%[/dim]")
        console.print(f"[dim]  Headings: {quality_metrics.heading_count} | Lists: {quality_metrics.list_item_count} | Code Blocks: {quality_metrics.code_block_count}[/dim]\n")
        
        # ================================================================
        # STEP 6: SAVE ALL RESULTS
        # ================================================================
        console.print(Panel.fit(
            "[bold]STEP 6: Saving All Results[/bold]",
            border_style="blue"
        ))
        
        self._save_results(
            transcript_whisper=transcript_whisper,
            transcript_whisper_baseline=transcript_whisper_baseline,
            transcript_whisper_global=transcript_whisper_global,
            transcript_fused=transcript_fused,  # NEW: Fused transcript
            fusion_result=fusion_result,  # NEW: Transliteration fusion metrics
            transcript_bangla=transcript_bangla,
            visual_keywords=visual_keywords,
            temporal_context=temporal_context,
            structured_extraction=structured_extraction,  # NEW
            text_boxes=text_boxes,
            gaze_events=gaze_events,
            evaluation=comparison,
            quality_metrics=quality_metrics,  # NEW
            final_notes=final_lecture_notes,
        )
        
        # ================================================================
        # FINAL SUMMARY
        # ================================================================
        processing_time = time.time() - start_time
        
        result = PipelineResult(
            transcript_whisper=transcript_whisper,
            transcript_whisper_baseline=transcript_whisper_baseline,
            transcript_bangla=transcript_bangla,
            transcript_fused=transcript_fused,  # NEW: Smart fusion
            # NOVELTY 2: Transliteration Fusion Metrics
            fusion_unique_bengali_words=fusion_result.unique_words_from_bangla,
            fusion_avg_similarity=fusion_result.average_similarity,
            fusion_merged_segments=fusion_result.merged_segments,
            fusion_total_segments=fusion_result.whisper_segments,
            visual_keywords=visual_keywords,
            temporal_context=temporal_context,
            structured_extraction=structured_extraction,  # NEW: Structured VLM
            text_boxes=text_boxes,
            gaze_events=gaze_events,
            ttr_improvement=comparison['improvement_pct'],
            evaluation_details=comparison,
            final_lecture_notes=final_lecture_notes,
            quality_metrics=quality_metrics,  # NEW: Quality scoring
            processing_time=processing_time,
            video_duration=video_duration,
        )
        
        self._print_final_summary(result)
        
        return result
    
    def _run_vision_track(
        self, 
        frame_paths: List[str]
    ) -> tuple[TemporalVisualContext, StructuredExtraction, List[Dict[str, Any]]]:
        """
        Run VLM on frames to extract whiteboard content with STRUCTURED EXTRACTION.
        
        NOVELTY 1: Instead of just extracting keywords, we categorize content into:
        - Definitions, Code Snippets, Formulas, Keywords
        This enables better context for LLM summarization.
        
        Returns:
            Tuple of (TemporalVisualContext, StructuredExtraction, text_boxes)
        """
        # Create temporal context with sliding window
        temporal_context = TemporalVisualContext(
            window_before_sec=self.frame_interval,
            window_after_sec=self.frame_interval,
        )
        
        # NOVELTY 1: Structured extraction
        structured_extractor = StructuredVLMExtractor()
        all_extractions = []
        
        if self.use_mock_vlm:
            # Mock data for fast testing
            console.print("[yellow]⚠ Using mock VLM data (--mock flag)[/yellow]")
            console.print("[yellow]  For topic-specific keywords, run without --mock[/yellow]")
            
            mock_keywords_per_frame = [
                ["Lecture", "Topic", "Introduction"],
                ["Definition", "Concept", "Example"],
                ["Algorithm", "Step", "Method"],
                ["Function", "Process", "Result"],
                ["Summary", "Conclusion", "Review"],
            ]
            
            for i, frame_path in enumerate(frame_paths):
                timestamp = i * self.frame_interval
                keywords = mock_keywords_per_frame[i % len(mock_keywords_per_frame)]
                temporal_context.add_frame_keywords(frame_path, timestamp, keywords)
            
            text_boxes = [
                {"bbox": [100, 100, 300, 150], "text": "Lecture Topic"},
                {"bbox": [100, 200, 400, 250], "text": "Key Concept"},
                {"bbox": [100, 300, 350, 350], "text": "Example"},
            ]
            
            console.print("[dim]  Mock keywords are generic placeholders.[/dim]")
            console.print(f"[green]✓ Mock temporal context: {len(temporal_context)} frames[/green]")
            
            # Empty structured extraction for mock
            structured_extraction = StructuredExtraction()
            return temporal_context, structured_extraction, text_boxes
        
        # Real VLM processing with structured extraction
        self.vlm = WhiteboardVLM()
        all_text_boxes = []
        
        console.print(f"[cyan]Processing {len(frame_paths)} frames with Qwen2.5-VL...[/cyan]")
        console.print(f"[cyan]  → NOVELTY 1: Structured content extraction (code, definitions, keywords)[/cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing frames with VLM...", total=len(frame_paths))
            
            for i, frame_path in enumerate(frame_paths):
                timestamp = i * self.frame_interval
                try:
                    import re
                    match = re.search(r'_(\d+)s\.', Path(frame_path).name)
                    if match:
                        timestamp = float(match.group(1))
                except:
                    pass
                
                try:
                    # VLM returns raw text content from whiteboard
                    content = self.vlm.analyze_frame(frame_path)
                    
                    if content and len(content) > 10:
                        # Extract keywords for temporal context
                        keywords = self._extract_keywords_from_text(content)
                        temporal_context.add_frame_keywords(frame_path, timestamp, keywords)
                        
                        # NOVELTY 1: Structured extraction
                        frame_extraction = structured_extractor.extract_from_vlm_output(
                            content, frame_index=i, timestamp=timestamp
                        )
                        all_extractions.append(frame_extraction)
                        
                        console.print(f"[dim]  Frame: {Path(frame_path).name} @ {timestamp:.0f}s → {len(keywords)} keywords[/dim]")
                    
                except Exception as e:
                    console.print(f"[yellow]Warning: VLM failed on {Path(frame_path).name}: {e}[/yellow]")
                
                progress.advance(task)
        
        # Merge all extractions
        structured_extraction = structured_extractor.merge_extractions(all_extractions)
        
        # Log results
        stats = temporal_context.get_stats()
        console.print(f"[green]✓ Temporal Visual Context created:[/green]")
        console.print(f"[dim]  Frames: {stats['total_frames']} | Unique keywords: {stats['total_unique_keywords']}[/dim]")
        
        console.print(f"[green]✓ Structured Extraction (NOVELTY 1):[/green]")
        console.print(f"[dim]  Definitions: {len(structured_extraction.definitions)} | Code: {len(structured_extraction.code_snippets)} | Keywords: {len(structured_extraction.keywords)}[/dim]")
        
        return temporal_context, structured_extraction, all_text_boxes
    
    def _run_gaze_tracking(
        self,
        frame_paths: List[str],
        text_boxes: List[Dict[str, Any]],
    ) -> List[GazeEvent]:
        """
        Run gaze tracking on frames to detect pointing gestures.
        
        Returns:
            List of GazeEvent objects
        """
        if self.skip_gaze:
            console.print("[yellow]⚠ Skipping gaze tracking (--skip-gaze flag)[/yellow]")
            return []
        
        if not text_boxes:
            console.print("[yellow]⚠ No text boxes for gaze tracking[/yellow]")
            return []
        
        import cv2
        
        self.gaze_tracker = GazeTracker()
        gaze_events = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Tracking hand gestures...", total=len(frame_paths))
            
            for i, frame_path in enumerate(frame_paths):
                try:
                    frame = cv2.imread(frame_path)
                    if frame is None:
                        continue
                    
                    # Estimate timestamp from frame index
                    timestamp = i * self.frame_interval
                    
                    # Detect focus
                    result = self.gaze_tracker.detect_focus_detailed(frame, text_boxes)
                    
                    if result.focused_term:
                        gaze_events.append(GazeEvent(
                            timestamp=timestamp,
                            term=result.focused_term,
                            confidence=result.confidence,
                        ))
                        
                except Exception as e:
                    console.print(f"[yellow]Warning: Gaze tracking failed: {e}[/yellow]")
                
                progress.advance(task)
        
        return gaze_events
    
    def _run_transcription(
        self,
        audio_path: str,
        temporal_context: Optional[TemporalVisualContext] = None,
    ) -> str:
        """
        Run Whisper transcription with optional TEMPORAL visual bias.
        
        NOVELTY: Uses TemporalVisualContext for segment-aligned keyword biasing.
        Instead of biasing entire audio with all keywords, each segment gets
        only the keywords visible at that timestamp.
        
        Args:
            audio_path: Path to audio file
            temporal_context: Temporal visual context (None for baseline)
            
        Returns:
            Transcription text
        """
        self.transcriber = BanglishTranscriber()
        
        # For temporal bias, always use generate() with temporal processor
        if temporal_context is None or len(temporal_context) == 0:
            # No bias - use generate mode for fair comparison
            result = self.transcriber.transcribe(audio_path=audio_path, visual_context=None)
        else:
            # TEMPORAL bias - use generate() with temporal LogitsProcessor
            result = self.transcriber.transcribe_temporal(
                audio_path=audio_path,
                temporal_context=temporal_context,
            )
        
        return result.text
    
    def _run_transcription_generate(
        self,
        audio_path: str,
        visual_keywords: Optional[List[str]] = None,
    ) -> str:
        """
        Run Whisper transcription using generate() mode (for fair comparison).
        
        This ensures all comparison methods use the same underlying approach.
        
        Args:
            audio_path: Path to audio file
            visual_keywords: Keywords for GLOBAL bias (None for no bias)
            
        Returns:
            Transcription text
        """
        self.transcriber = BanglishTranscriber()
        
        # Always use generate() for fair comparison
        result = self.transcriber.transcribe(
            audio_path=audio_path,
            visual_context=visual_keywords,  # None = no bias, List = global bias
        )
        
        return result.text
    
    def _run_3way_evaluation(
        self,
        ground_truth: List[str],
        baseline_transcript: str,
        global_transcript: str,
        temporal_transcript: str,
    ) -> Dict[str, Any]:
        """
        Run 3-way TTR evaluation: Baseline vs Global vs Temporal.
        
        This provides fair comparison to prove temporal alignment benefit.
        ALSO measures hallucination rates using Cross-Modal Verification.
        
        Args:
            ground_truth: List of visual keywords as ground truth
            baseline_transcript: Transcript with no bias
            global_transcript: Transcript with global (all keywords) bias
            temporal_transcript: Transcript with temporal (time-aligned) bias
            
        Returns:
            Comparison results dictionary
        """
        # Evaluate each transcript for TTR (Technical Term Recall)
        baseline_eval = self.evaluator.evaluate_recall(ground_truth, baseline_transcript)
        global_eval = self.evaluator.evaluate_recall(ground_truth, global_transcript)
        temporal_eval = self.evaluator.evaluate_recall(ground_truth, temporal_transcript)
        
        # NEW: Cross-Modal Verification (Hallucination Detection)
        verifier = CrossModalVerifier(fuzzy_threshold=80)
        baseline_cmv = verifier.verify(baseline_transcript, ground_truth)
        global_cmv = verifier.verify(global_transcript, ground_truth)
        temporal_cmv = verifier.verify(temporal_transcript, ground_truth)
        
        # Calculate improvements
        global_vs_baseline = (global_eval['recall'] - baseline_eval['recall']) * 100
        temporal_vs_baseline = (temporal_eval['recall'] - baseline_eval['recall']) * 100
        temporal_vs_global = (temporal_eval['recall'] - global_eval['recall']) * 100
        
        # Calculate hallucination reduction
        baseline_hr = baseline_cmv['hallucination_rate'] * 100
        global_hr = global_cmv['hallucination_rate'] * 100
        temporal_hr = temporal_cmv['hallucination_rate'] * 100
        
        hr_reduction_global = baseline_hr - global_hr  # Positive = reduced hallucinations
        hr_reduction_temporal = baseline_hr - temporal_hr
        
        # Print 3-way comparison table
        table = Table(title="3-Way Technical Term Recall (TTR) + Hallucination Comparison", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Baseline\n(no bias)", style="white")
        table.add_column("Global Bias\n(all keywords)", style="yellow")
        table.add_column("Temporal Bias\n(time-aligned)", style="green")
        
        table.add_row(
            "Recall",
            f"{baseline_eval['recall']*100:.1f}%",
            f"{global_eval['recall']*100:.1f}%",
            f"{temporal_eval['recall']*100:.1f}%",
        )
        table.add_row(
            "Found / Total",
            f"{len(baseline_eval['found'])} / {len(ground_truth)}",
            f"{len(global_eval['found'])} / {len(ground_truth)}",
            f"{len(temporal_eval['found'])} / {len(ground_truth)}",
        )
        table.add_row(
            "Hallucination Rate",
            f"[red]{baseline_hr:.1f}%[/red]",
            f"[yellow]{global_hr:.1f}%[/yellow]",
            f"[green]{temporal_hr:.1f}%[/green]",
        )
        table.add_row(
            "Groundedness",
            f"{baseline_cmv['groundedness_score']*100:.1f}%",
            f"{global_cmv['groundedness_score']*100:.1f}%",
            f"{temporal_cmv['groundedness_score']*100:.1f}%",
        )
        table.add_row(
            "Found Terms",
            ", ".join(baseline_eval['found'][:5]) + ("..." if len(baseline_eval['found']) > 5 else "") or "None",
            ", ".join(global_eval['found'][:5]) + ("..." if len(global_eval['found']) > 5 else "") or "None",
            ", ".join(temporal_eval['found'][:5]) + ("..." if len(temporal_eval['found']) > 5 else "") or "None",
        )
        
        console.print(table)
        
        # Print improvement summary
        console.print("\n[bold]TTR Improvement Analysis:[/bold]")
        console.print(f"  Global vs Baseline:   [yellow]{global_vs_baseline:+.1f}%[/yellow]")
        console.print(f"  Temporal vs Baseline: [green]{temporal_vs_baseline:+.1f}%[/green]")
        console.print(f"  [bold cyan]Temporal vs Global:   {temporal_vs_global:+.1f}%[/bold cyan] ← NOVELTY IMPACT")
        
        # NEW: Hallucination Analysis
        console.print("\n[bold]Hallucination Reduction Analysis:[/bold]")
        if hr_reduction_global > 0:
            console.print(f"  Global Bias: [green]-{hr_reduction_global:.1f}% hallucinations[/green]")
        else:
            console.print(f"  Global Bias: [red]+{-hr_reduction_global:.1f}% hallucinations[/red]")
        
        if hr_reduction_temporal > 0:
            console.print(f"  Temporal Bias: [green]-{hr_reduction_temporal:.1f}% hallucinations[/green]")
        else:
            console.print(f"  Temporal Bias: [red]+{-hr_reduction_temporal:.1f}% hallucinations[/red]")
        
        # Best method summary
        best_recall = max(baseline_eval['recall'], global_eval['recall'], temporal_eval['recall'])
        best_hr = min(baseline_hr, global_hr, temporal_hr)
        
        if global_eval['recall'] >= best_recall and global_hr <= best_hr:
            console.print(f"\n[bold green]★ Global Bias is the best approach (highest recall, lowest hallucination)[/bold green]")
        elif temporal_eval['recall'] >= best_recall:
            console.print(f"\n[bold green]★ Temporal Bias shows best TTR![/bold green]")
        else:
            console.print(f"\n[yellow]→ Visual biasing provides hallucination reduction benefit[/yellow]")
        
        # Build result dictionary
        comparison = {
            'baseline': baseline_eval,
            'global': global_eval,
            'temporal': temporal_eval,
            'baseline_recall': baseline_eval['recall'],
            'global_recall': global_eval['recall'],
            'temporal_recall': temporal_eval['recall'],
            'global_vs_baseline_pct': global_vs_baseline,
            'temporal_vs_baseline_pct': temporal_vs_baseline,
            'temporal_vs_global_pct': temporal_vs_global,
            # NEW: Hallucination metrics
            'baseline_hallucination_rate': baseline_hr,
            'global_hallucination_rate': global_hr,
            'temporal_hallucination_rate': temporal_hr,
            'hallucination_reduction_global': hr_reduction_global,
            'hallucination_reduction_temporal': hr_reduction_temporal,
            'baseline_cmv': baseline_cmv,
            'global_cmv': global_cmv,
            'temporal_cmv': temporal_cmv,
            # Backward compatibility
            'improvement_pct': temporal_vs_baseline,
        }
        
        return comparison
    
    # NOTE: Old 2-way comparison removed, now using 3-way for fair evaluation
    
    def _run_bangla_transcription(self, audio_path: str) -> str:
        """
        Run BanglaASR transcription for Bengali content.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Bengali transcription text
        """
        try:
            bangla_transcriber = BanglaASRTranscriber()
            result = bangla_transcriber.transcribe(audio_path)
            bangla_transcriber.unload_model()  # Free GPU memory
            raw_text = result.text
            
            # Apply anti-hallucination post-processing to BanglaASR output
            # BanglaASR tends to hallucinate repetitions more than Whisper
            from src.audio.visual_bias_processor import (
                remove_repetitions, remove_phrase_repetitions, 
                remove_hyphenated_repetitions, remove_ngram_loops
            )
            
            cleaned_text = raw_text
            cleaned_text = remove_repetitions(cleaned_text, max_repeats=2)
            cleaned_text = remove_phrase_repetitions(cleaned_text, max_repeats=2)
            cleaned_text = remove_hyphenated_repetitions(cleaned_text, max_repeats=2)
            cleaned_text = remove_ngram_loops(cleaned_text, max_repeats=2)
            
            # Log cleaning stats
            if len(cleaned_text) < len(raw_text) * 0.9:
                reduction_pct = (1 - len(cleaned_text) / len(raw_text)) * 100
                console.print(f"[yellow]  ⚠ BanglaASR hallucination cleaned: {reduction_pct:.1f}% removed[/yellow]")
            
            return cleaned_text
        except Exception as e:
            console.print(f"[yellow]⚠ BanglaASR failed: {e}[/yellow]")
            console.print("[yellow]  Continuing with Whisper output only...[/yellow]")
            return ""
    
    def _generate_lecture_notes(
        self,
        transcript_whisper: str,
        transcript_bangla: str,
        visual_keywords: List[str],
        gaze_events: List[GazeEvent],
        structured_context: str = "",  # NEW: Structured VLM extraction
    ) -> str:
        """
        Generate final lecture notes using LLM (Qwen2.5-7B-Instruct).
        
        NOVELTY 1+2 INTEGRATION:
        - Uses FUSED transcript (Whisper + BanglaASR intelligently merged)
        - Uses STRUCTURED VLM context (categorized definitions, code, keywords)
        
        Returns:
            Markdown formatted lecture notes
        """
        try:
            # Use 4-bit quantized LLM in live mode to fit in 24GB VRAM
            generator = LectureNoteGenerator(use_4bit=self.live_mode)
            generator.load_model()
            
            # Build multimodal context (NOVELTY 1: Structured VLM content)
            if structured_context:
                visual_content = structured_context  # Use structured format
            else:
                visual_content = "\\n".join(visual_keywords) if visual_keywords else "No visual content extracted"
            
            gaze_summary = ""
            if gaze_events:
                gaze_summary = "\\n".join([
                    f"- At {e.timestamp:.0f}s: Professor pointed at '{e.term}'"
                    for e in gaze_events[:10]  # Limit to first 10
                ])
            else:
                gaze_summary = "No pointing gestures detected"
            
            # Build the prompt (ENHANCED with structured context)
            system_prompt = """You are an expert lecture note generator. Create comprehensive, well-structured lecture notes in Markdown format.

You have access to multiple sources:
1. TRANSCRIPT - Intelligently merged from Whisper (English) and BanglaASR (Bengali)  
2. STRUCTURED VISUAL CONTENT - Categorized content from whiteboard:
   - DEFINITIONS: Technical terms with explanations
   - CODE SNIPPETS: Programming code examples
   - FORMULAS: Mathematical expressions
   - KEYWORDS: Important technical vocabulary
3. GAZE EVENTS - When the professor pointed at specific terms (emphasis indicators)

CRITICAL INSTRUCTIONS:
- Use STRUCTURED VISUAL CONTENT as the source of truth for:
  * Technical definitions (copy them exactly)
  * Code snippets (format as code blocks)
  * Formulas (use proper notation)
  * Keywords (ensure these appear in your notes)
- The transcript is already fused from multiple ASR systems
- Terms the professor pointed at (GAZE EVENTS) are important - emphasize them
- Output clean, well-structured Markdown lecture notes
- Organize by topic with clear headings
- Add a summary section at the end"""

            user_prompt = f"""Please create comprehensive lecture notes from these sources:

## TRANSCRIPT (Whisper + BanglaASR Fused):
{transcript_whisper[:10000]}{"..." if len(transcript_whisper) > 10000 else ""}

## STRUCTURED VISUAL CONTENT (from whiteboard AI analysis):
{visual_content}

## GAZE EVENTS (professor emphasis):
{gaze_summary}

---

Generate comprehensive lecture notes in Markdown format. Include:
1. Main topics and subtopics with clear headings
2. All definitions from visual content (formatted properly)
3. Code snippets in proper code blocks
4. Key formulas and equations
5. Important concepts explained
6. Summary section

Output:"""

            # Generate using the model
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            text = generator.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            import torch
            inputs = generator.tokenizer(text, return_tensors="pt").to(generator.model.device)
            
            with torch.no_grad():
                outputs = generator.model.generate(
                    **inputs,
                    max_new_tokens=2048,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=generator.tokenizer.eos_token_id,
                )
            
            generated_ids = outputs[0][inputs.input_ids.shape[1]:]
            notes = generator.tokenizer.decode(generated_ids, skip_special_tokens=True)
            
            generator.unload_model()  # Free GPU memory
            
            console.print(f"[green]✓ Lecture notes generated ({len(notes)} chars)[/green]")
            return notes.strip()
            
        except Exception as e:
            console.print(f"[yellow]⚠ LLM summarization failed: {e}[/yellow]")
            console.print("[yellow]  Returning raw transcript as fallback...[/yellow]")
            return f"# Lecture Notes (Raw Transcript)\\n\\n{transcript_whisper[:5000]}"
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """
        Extract potential technical keywords from VLM output text.
        
        This function extracts:
        - Capitalized words (Algorithm, Tree, etc.)
        - Acronyms (BFS, DFS, RISC, DNA, etc.)
        - Function/formula notation (f(n), O(n), etc.)
        - Special patterns (A*, B+, etc.)
        - Multi-word terms (Binary Tree, Red-Black, etc.)
        - Numbers with context (32-bit, 2D, etc.)
        """
        import re
        
        keywords = []
        
        # 1. Multi-word capitalized terms (Binary Tree, Cohen Sutherland, etc.)
        multi_word = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        keywords.extend(multi_word)
        
        # 2. Single capitalized words (Algorithm, Heuristic, etc.)
        single_cap = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
        keywords.extend(single_cap)
        
        # 3. Acronyms and uppercase terms (BFS, DFS, RISC-V, DNA, RNA, etc.)
        acronyms = re.findall(r'\b[A-Z]{2,}(?:-[A-Z0-9]+)?\b', text)
        keywords.extend(acronyms)
        
        # 4. Function/formula notation (f(n), g(x), O(n), etc.)
        functions = re.findall(r'\b[a-zA-Z]+\([^)]+\)', text)
        keywords.extend(functions)
        
        # 5. Special patterns with symbols (A*, B+, C#, etc.)
        special = re.findall(r'\b[A-Z][*+#]?\b', text)
        keywords.extend([s for s in special if len(s) >= 2])
        
        # 6. Technical terms with numbers (32-bit, 2D, 3D, IPv4, etc.)
        tech_numbers = re.findall(r'\b\d+[A-Za-z-]+\b|\b[A-Za-z]+\d+[A-Za-z]*\b', text)
        keywords.extend(tech_numbers)
        
        # 7. Hyphenated terms (Red-Black, Cohen-Sutherland, etc.)
        hyphenated = re.findall(r'\b[A-Z][a-z]+-[A-Z][a-z]+\b', text)
        keywords.extend(hyphenated)
        
        # 8. Greek letters often used in CS (alpha, beta, lambda, etc.)
        greek = re.findall(r'\b(?:alpha|beta|gamma|delta|epsilon|theta|lambda|sigma|omega)\b', text, re.IGNORECASE)
        keywords.extend(greek)
        
        # Filter: remove very common words that aren't technical
        stop_words = {
            'The', 'This', 'That', 'These', 'Those', 'And', 'But', 'For',
            'With', 'From', 'Into', 'About', 'After', 'Before', 'Above',
            'Below', 'Between', 'Under', 'Over', 'Through', 'During',
            'Here', 'There', 'Where', 'When', 'Which', 'What', 'How',
            'All', 'Each', 'Every', 'Both', 'Few', 'More', 'Most', 'Some',
            'Such', 'Only', 'Same', 'Than', 'Very', 'Just', 'Also',
        }
        
        # Clean and deduplicate
        cleaned = []
        seen = set()
        for kw in keywords:
            kw_clean = kw.strip()
            kw_lower = kw_clean.lower()
            if kw_clean and kw_clean not in stop_words and kw_lower not in seen and len(kw_clean) >= 2:
                cleaned.append(kw_clean)
                seen.add(kw_lower)
        
        return cleaned
    
    def _save_results(
        self,
        transcript_whisper: str,
        transcript_whisper_baseline: str,
        transcript_whisper_global: str,
        transcript_fused: str,  # NEW: Smart fusion result
        fusion_result,  # NEW: Transliteration fusion result object
        transcript_bangla: str,
        visual_keywords: List[str],
        temporal_context: Optional[TemporalVisualContext],
        structured_extraction: Optional[StructuredExtraction],  # NEW
        text_boxes: List[Dict[str, Any]],
        gaze_events: List[GazeEvent],
        evaluation: Dict[str, Any],
        quality_metrics: Optional[QualityMetrics],  # NEW
        final_notes: str,
    ):
        """Save all results to output directory."""
        # Save transcripts - now 4 versions including fused
        (self.output_dir / "transcript_whisper_temporal_biased.txt").write_text(
            transcript_whisper, encoding="utf-8"
        )
        (self.output_dir / "transcript_whisper_baseline.txt").write_text(
            transcript_whisper_baseline, encoding="utf-8"
        )
        (self.output_dir / "transcript_whisper_global_biased.txt").write_text(
            transcript_whisper_global, encoding="utf-8"
        )
        (self.output_dir / "transcript_fused.txt").write_text(
            transcript_fused, encoding="utf-8"
        )
        (self.output_dir / "transcript_bangla.txt").write_text(
            transcript_bangla, encoding="utf-8"
        )
        
        # Save Transliteration Fusion metrics (NOVELTY 2)
        if fusion_result:
            (self.output_dir / "fusion_metrics.json").write_text(
                json.dumps({
                    "method": "Transliteration Fusion",
                    "unique_bengali_words": fusion_result.unique_words_from_bangla,
                    "average_similarity": fusion_result.average_similarity,
                    "whisper_segments": fusion_result.whisper_segments,
                    "bangla_segments": fusion_result.bangla_segments,
                    "merged_segments": fusion_result.merged_segments,
                    "whisper_word_count": fusion_result.whisper_word_count,
                    "bangla_word_count": fusion_result.bangla_word_count,
                    "fused_word_count": fusion_result.fused_word_count,
                }, indent=2), encoding="utf-8"
            )
        
        # Save final lecture notes (the main output!)
        (self.output_dir / "final_lecture_notes.md").write_text(
            final_notes, encoding="utf-8"
        )
        
        # Save visual data - both flat keywords and temporal context
        (self.output_dir / "visual_keywords.json").write_text(
            json.dumps(visual_keywords, indent=2), encoding="utf-8"
        )
        
        # Save temporal visual context
        if temporal_context:
            temporal_context.save(str(self.output_dir / "temporal_visual_context.json"))
        
        # Save structured extraction (NOVELTY 1)
        if structured_extraction:
            (self.output_dir / "structured_extraction.json").write_text(
                json.dumps({
                    "definitions": [{"text": d.text, "type": d.content_type.value} for d in structured_extraction.definitions],
                    "code_snippets": [{"text": c.text, "type": c.content_type.value} for c in structured_extraction.code_snippets],
                    "formulas": [{"text": f.text, "type": f.content_type.value} for f in structured_extraction.formulas],
                    "keywords": [{"text": k.text, "type": k.content_type.value} for k in structured_extraction.keywords],
                }, indent=2), encoding="utf-8"
            )
        
        (self.output_dir / "text_boxes.json").write_text(
            json.dumps(text_boxes, indent=2), encoding="utf-8"
        )
        
        # Save gaze events
        gaze_data = [
            {"timestamp": e.timestamp, "term": e.term, "confidence": e.confidence}
            for e in gaze_events
        ]
        (self.output_dir / "gaze_events.json").write_text(
            json.dumps(gaze_data, indent=2), encoding="utf-8"
        )
        
        # Save 3-way evaluation results
        eval_safe = {
            "baseline_recall": evaluation.get("baseline_recall", 0),
            "global_recall": evaluation.get("global_recall", 0),
            "temporal_recall": evaluation.get("temporal_recall", 0),
            "global_vs_baseline_pct": evaluation.get("global_vs_baseline_pct", 0),
            "temporal_vs_baseline_pct": evaluation.get("temporal_vs_baseline_pct", 0),
            "temporal_vs_global_pct": evaluation.get("temporal_vs_global_pct", 0),
            "baseline_found": evaluation.get("baseline", {}).get("found", []),
            "global_found": evaluation.get("global", {}).get("found", []),
            "temporal_found": evaluation.get("temporal", {}).get("found", []),
        }
        (self.output_dir / "evaluation.json").write_text(
            json.dumps(eval_safe, indent=2), encoding="utf-8"
        )
        
        # Save quality metrics (NOVELTY 3)
        if quality_metrics:
            (self.output_dir / "quality_metrics.json").write_text(
                json.dumps({
                    "overall_score": quality_metrics.overall_score,
                    "keyword_coverage": quality_metrics.keyword_coverage,
                    "lexical_diversity": quality_metrics.lexical_diversity,
                    "keywords_found": quality_metrics.keywords_found,
                    "keywords_total": quality_metrics.keywords_total,
                    "heading_count": quality_metrics.heading_count,
                    "code_block_count": quality_metrics.code_block_count,
                    "list_item_count": quality_metrics.list_item_count,
                    "word_count": quality_metrics.word_count,
                    "paragraph_count": quality_metrics.paragraph_count,
                }, indent=2), encoding="utf-8"
            )
        
        console.print(f"[green]✓ Results saved to:[/green] {self.output_dir}")
    
    def _print_final_summary(self, result: PipelineResult):
        """Print final pipeline summary with NOVELTY metrics."""
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]PIPELINE COMPLETE[/bold green]",
            border_style="green"
        ))
        
        # Summary table
        table = Table(title="Thesis Pipeline Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Video Duration", f"{result.video_duration:.1f} seconds")
        table.add_row("Processing Time", f"{result.processing_time:.1f} seconds")
        table.add_row("Visual Keywords", f"{len(result.visual_keywords)} extracted")
        table.add_row("Gaze Events", f"{len(result.gaze_events)} detected")
        table.add_row("", "")
        table.add_row("Whisper Transcript", f"{len(result.transcript_whisper)} chars")
        table.add_row("BanglaASR Transcript", f"{len(result.transcript_bangla)} chars")
        table.add_row("Fused Transcript (NOVELTY 2)", f"{len(result.transcript_fused)} chars")
        table.add_row("", "")
        
        # Transliteration Fusion metrics (NOVELTY 2)
        table.add_row("[bold]Transliteration Fusion (NOVELTY 2)[/bold]", "")
        table.add_row("  Unique Bengali Words", f"{result.fusion_unique_bengali_words}")
        table.add_row("  Avg Similarity", f"{result.fusion_avg_similarity:.1%}")
        table.add_row("  Merged Segments", f"{result.fusion_merged_segments}/{result.fusion_total_segments}")
        table.add_row("", "")
        
        table.add_row("Final Lecture Notes", f"{len(result.final_lecture_notes)} chars")
        table.add_row("", "")
        
        # Structured extraction stats (NOVELTY 1)
        if result.structured_extraction:
            se = result.structured_extraction
            table.add_row("[bold]Structured VLM (NOVELTY 1)[/bold]", "")
            table.add_row("  Definitions", f"{len(se.definitions)} extracted")
            table.add_row("  Code Snippets", f"{len(se.code_snippets)} extracted")
            table.add_row("  Keywords", f"{len(se.keywords)} extracted")
            table.add_row("", "")
        
        # Quality metrics (NOVELTY 3)
        if result.quality_metrics:
            qm = result.quality_metrics
            score_color = "green" if qm.overall_score >= 70 else "yellow" if qm.overall_score >= 50 else "red"
            table.add_row("[bold]Quality Score (NOVELTY 3)[/bold]", f"[bold {score_color}]{qm.overall_score:.1f}/100[/bold {score_color}]")
            table.add_row("  Keyword Coverage", f"{qm.keyword_coverage*100:.0f}%")
            table.add_row("  Lexical Diversity", f"{qm.lexical_diversity*100:.0f}%")
            table.add_row("  Structure", f"{qm.heading_count} headings, {qm.list_item_count} lists, {qm.code_block_count} code")
            table.add_row("", "")
        
        # TTR result
        if result.ttr_improvement > 0:
            improvement_str = f"[bold green]+{result.ttr_improvement:.1f}%[/bold green]"
        elif result.ttr_improvement < 0:
            improvement_str = f"[bold red]{result.ttr_improvement:.1f}%[/bold red]"
        else:
            improvement_str = f"[yellow]0.0%[/yellow]"
        
        table.add_row("[bold]TTR Improvement[/bold]", improvement_str)
        
        console.print(table)
        
        # Key insight - Updated for 3 novelties
        console.print("\n[bold cyan]Key Findings (3 NOVELTIES):[/bold cyan]")
        console.print(
            f"  1. [bold]NOVELTY 1[/bold]: Structured VLM extraction categorized whiteboard content"
        )
        if result.structured_extraction:
            console.print(
                f"     → {len(result.structured_extraction.definitions)} definitions, "
                f"{len(result.structured_extraction.code_snippets)} code snippets, "
                f"{len(result.structured_extraction.keywords)} keywords"
            )
        console.print(
            f"  2. [bold]NOVELTY 2[/bold]: Transliteration-Based Dual-ASR Fusion"
        )
        console.print(
            f"     → {result.fusion_unique_bengali_words} unique Bengali words extracted via transliteration"
        )
        console.print(
            f"     → {result.fusion_merged_segments}/{result.fusion_total_segments} segments merged"
        )
        console.print(
            f"  3. [bold]NOVELTY 3[/bold]: Quality-Evaluated lecture notes with measurable metrics"
        )
        if result.quality_metrics:
            console.print(
                f"     → Score: {result.quality_metrics.overall_score:.1f}/100 "
                f"(Coverage: {result.quality_metrics.keyword_coverage*100:.0f}%)"
            )
        console.print(
            f"\n[bold green]📝 Final output: final_lecture_notes.md[/bold green]\n"
        )


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """Main entry point with argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Multimodal Banglish Classroom Summarizer - Thesis Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_thesis.py data/raw/lecture.mp4
  python run_thesis.py data/raw/lecture.mp4 --mock --skip-gaze
  python run_thesis.py data/raw/lecture.mp4 -o results/run1 --interval 60
  python run_thesis.py data/raw/lecture.mp4 --live  # 4-bit LLM for 24GB GPU
        """
    )
    
    parser.add_argument(
        "video",
        type=str,
        help="Path to lecture video file (e.g., lecture.mp4)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output/thesis_run",
        help="Output directory (default: output/thesis_run)"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Frame extraction interval in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock VLM data (faster testing, no GPU needed for VLM)"
    )
    
    parser.add_argument(
        "--skip-gaze",
        action="store_true",
        help="Skip gaze tracking (faster testing)"
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable live mode: uses 4-bit quantized LLM to fit all models in 24GB VRAM"
    )
    
    args = parser.parse_args()
    
    # Validate video file
    video_path = Path(args.video)
    if not video_path.exists():
        console.print(f"[red]Error: Video file not found: {video_path}[/red]")
        sys.exit(1)
    
    # Show live mode info
    if args.live:
        console.print(Panel.fit(
            "[bold yellow]🚀 LIVE MODE ENABLED[/bold yellow]\n"
            "Using 4-bit quantized LLM (~4GB) to fit all models in 24GB VRAM:\n"
            "  • Whisper large-v3-turbo: ~3GB (FP16)\n"
            "  • Qwen2.5-VL-7B: ~15GB (FP16)\n"
            "  • Qwen2.5-7B: ~4GB (4-bit quantized)\n"
            "  • YOLOv8-Pose: ~0.5GB\n"
            "  • Total: ~22.5GB ✓",
            border_style="yellow"
        ))
    
    # Run pipeline
    pipeline = ThesisPipeline(
        video_path=str(video_path),
        output_dir=args.output,
        frame_interval=args.interval,
        use_mock_vlm=args.mock,
        skip_gaze=args.skip_gaze,
        live_mode=args.live,
    )
    
    try:
        result = pipeline.run()
        console.print(f"\n[bold green]Success![/bold green] Results saved to: {args.output}")
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Pipeline interrupted by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Pipeline failed: {e}[/red]")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
