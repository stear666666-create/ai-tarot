"""
Vercel Serverless Python entry point
"""
import sys
import os

# Add the project root to path so we can import backend
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(root, "backend", ".env"))

from backend.app.main import app

# Vercel expects the app to be named 'app'
