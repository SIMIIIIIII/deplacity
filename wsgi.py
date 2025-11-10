import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import create_app from __init__.py
from __init__ import create_app

application = create_app()
