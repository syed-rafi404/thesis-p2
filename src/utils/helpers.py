"""
Helper Utilities
================
Common utility functions for the thesis project.
"""

import os
import yaml
import logging
import torch
from pathlib import Path
from typing import Optional, Union
from datetime import datetime


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def setup_logging(
    log_dir: str = "experiments/logs",
    level: int = logging.INFO,
    name: str = "thesis"
) -> logging.Logger:
    """
    Set up logging with file and console handlers.
    
    Args:
        log_dir: Directory for log files
        level: Logging level
        name: Logger name
        
    Returns:
        Configured logger
    """
    ensure_dir(log_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def get_device(prefer_cuda: bool = True) -> torch.device:
    """
    Get the best available device.
    
    Args:
        prefer_cuda: Whether to prefer CUDA if available
        
    Returns:
        torch.device object
    """
    if prefer_cuda and torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def format_timestamp(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_gpu_memory_info() -> dict:
    """
    Get GPU memory information.
    
    Returns:
        Dictionary with memory stats
    """
    if not torch.cuda.is_available():
        return {"available": False}
    
    return {
        "available": True,
        "device_name": torch.cuda.get_device_name(0),
        "total_memory_gb": torch.cuda.get_device_properties(0).total_memory / (1024**3),
        "allocated_gb": torch.cuda.memory_allocated(0) / (1024**3),
        "reserved_gb": torch.cuda.memory_reserved(0) / (1024**3),
    }


def clear_gpu_memory():
    """Clear GPU memory cache."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
