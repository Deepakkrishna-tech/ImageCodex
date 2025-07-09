# run_app.py
"""
The main entry point for the ImageCodeX application.

This script ensures that environment variables are loaded from the .env file
at the very beginning, before any other application code is imported. This
prevents API key errors during the import process.
"""

import os
from dotenv import load_dotenv

# --- CRITICAL: Load environment variables FIRST ---
# This must happen before any imports from the 'src' directory.
load_dotenv()

# Now it is safe to import the main application function
from src.app import main

if __name__ == "__main__":
    # Set the PYTHONPATH for Streamlit if it's not already set
    # This ensures that relative imports within the 'src' directory work correctly.
    os.environ['PYTHONPATH'] = '.'
    main()