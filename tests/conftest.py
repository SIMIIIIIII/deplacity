"""
Pytest configuration file to set up the Python path for tests.
"""
import sys
import os

# Add parent directory to path so tests can import deplacity package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(parent_dir))
