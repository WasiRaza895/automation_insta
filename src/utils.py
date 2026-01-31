"""Utility functions for the Instagram automation system."""

import os
import time
import random
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name):
    """Get a logger instance."""
    return logging.getLogger(name)

def random_delay(min_seconds=30, max_seconds=120):
    """Add a random delay to simulate human behavior."""
    delay = random.uniform(min_seconds, max_seconds)
    logging.info(f"Adding random delay of {delay:.2f} seconds")
    time.sleep(delay)

def ensure_dir(path):
    """Ensure a directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent

def load_env_var(var_name, default=None, required=True):
    """Load an environment variable."""
    value = os.getenv(var_name, default)
    if required and not value:
        raise ValueError(f"Environment variable {var_name} is required but not set")
    return value

def sanitize_filename(filename):
    """Sanitize a filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def format_timestamp():
    """Get a formatted timestamp for logging."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
