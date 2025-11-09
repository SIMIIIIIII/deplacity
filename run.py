#!/usr/bin/env python3
"""
Development server runner for the Deplacity Flask app.
Run this from the deplacity directory: python run.py
"""
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import deplacity

if __name__ == "__main__":
    app = deplacity.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
