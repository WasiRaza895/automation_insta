#!/usr/bin/env python3
"""
Run this script to manually trigger one post NOW.
Usage: python run_now.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from main import main

if __name__ == "__main__":
    print("🚀 Starting manual Instagram post...")
    print("=" * 50)
    main()
    print("=" * 50)
    print("✅ Done! Check your Instagram account.")
