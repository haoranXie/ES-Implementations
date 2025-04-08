import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import main

def test_main_runs():
    try:
        main()
    except Exception as e:
        assert False, f"main() raised an exception: {e}"