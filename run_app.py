# run_app.py
# This is the single, correct entry point for your application.

import sys
from pathlib import Path

# This permanently solves all import errors by telling Python where your project lives.
ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))

# Now, we can safely import the main function from your src package.
from src.app import main

if __name__ == "__main__":
    # This calls the main function inside src/app.py to start the application.
    main()