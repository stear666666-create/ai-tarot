from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os

from backend.app.api.divination import router as divination_router
from backend.app.core.config import settings

_env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)

app = FastAPI(
    title="AI Tarot Divination API",
    description="Backend API for AI Tarot + MBTI Divination",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(divination_router, prefix="/api", tags=["divination"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ai-tarot-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
