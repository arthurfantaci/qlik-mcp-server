#!/usr/bin/env python3
"""Simple startup script for the MCP server that handles imports correctly"""

import os
import sys

# Add the project directory to Python path so we can import src modules
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Change to the project directory to ensure relative paths work
os.chdir(project_dir)

from src.server import main

if __name__ == "__main__":
    main()
