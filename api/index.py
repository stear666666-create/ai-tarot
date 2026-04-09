"""
Vercel Serverless Python entry point
"""
import sys
import os

# Add the project root to path so we can import backend
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)

# For Vercel, environment variables should be set in Vercel dashboard
# No need to load .env file in production
if os.environ.get("VERCEL"):
    # Running on Vercel - env vars are already set
    pass
else:
    # Local development - load .env
    from dotenv import load_dotenv
    env_path = os.path.join(root, "backend", ".env")
    load_dotenv(env_path, override=True)

from backend.app.main import app

# Vercel expects the app to be named 'app'
# This file acts as a serverless function handler
