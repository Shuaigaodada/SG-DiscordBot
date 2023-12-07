import os
import sys

base_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts_path: str = os.path.join(base_path, "scripts")
sys.path.append(scripts_path)