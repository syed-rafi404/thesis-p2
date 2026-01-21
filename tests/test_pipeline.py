"""
Test Pipeline
=============
Unit tests for the multimodal summarizer pipeline.
"""

import pytest
import torch


class TestEnvironment:
    """Test the environment setup."""
    
    def test_cuda_available(self):
        """Test that CUDA is available."""
        assert torch.cuda.is_available(), "CUDA should be available"
    
    def test_gpu_memory(self):
        """Test that GPU has sufficient memory."""
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            total_gb = props.total_memory / (1024**3)
            assert total_gb >= 8, f"GPU should have at least 8GB, got {total_gb:.1f}GB"


class TestAudioModule:
    """Test audio processing module."""
    
    def test_import(self):
        """Test that audio module can be imported."""
        from src.audio import Transcriber, AudioPreprocessor
        assert Transcriber is not None
        assert AudioPreprocessor is not None


class TestVisionModule:
    """Test vision processing module."""
    
    def test_import(self):
        """Test that vision module can be imported."""
        # NOTE: We use VLM (WhiteboardVLM), NOT OCR
        # EasyOCR was tested and failed on Banglish handwriting
        from src.vision import FrameExtractor, WhiteboardVLM, VisionPreprocessor
        assert FrameExtractor is not None
        assert WhiteboardVLM is not None


class TestFusionModule:
    """Test multimodal fusion module."""
    
    def test_import(self):
        """Test that fusion module can be imported."""
        from src.fusion import MultimodalAligner
        assert MultimodalAligner is not None


class TestSummarizerModule:
    """Test summarization module."""
    
    def test_import(self):
        """Test that summarizer module can be imported."""
        from src.summarizer import NotesGenerator
        assert NotesGenerator is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
