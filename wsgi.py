import os
import sys

# Get the parent directory (the directory containing the project)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Get the project name (directory name)
project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# Import create_app as a module
module = __import__(project_name)
application = module.create_app()
