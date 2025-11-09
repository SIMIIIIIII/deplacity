from __future__ import absolute_import
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import deplacity

application = deplacity.create_app()
