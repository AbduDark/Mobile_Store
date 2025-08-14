#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick run script for PyQt6 version during development
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Run the PyQt6 application
if __name__ == "__main__":
    from main_pyqt6 import main
    main()