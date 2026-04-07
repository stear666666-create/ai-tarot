"""
Vercel Serverless Python entry point
"""
import sys
import os

# Add the project root to path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app

# Vercel expects the app to be named 'app'
