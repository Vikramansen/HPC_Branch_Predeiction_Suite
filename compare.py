#!/usr/bin/env python3
"""
Branch Predictor Comparison Script

This is a wrapper around prediction.py for backward compatibility
with the README documentation.
"""

import sys
import os

# Import main from prediction module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prediction import main

if __name__ == "__main__":
    main()
