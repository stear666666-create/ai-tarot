import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 明确指定 .env 路径，确保无论从哪里启动都能正确加载
_env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)


class Settings(BaseSettings):
    APP_NAME: str = "AI Tarot Divination"
    DEBUG: bool = bool(os.getenv("DEBUG", "True"))

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "zhipu")  # zhipu, moonshot, deepseek, volcengine
    ZHIPU_API_KEY: str = os.getenv("ZHIPU_API_KEY", "")
    ZHIPU_MODEL: str = os.getenv("ZHIPU_MODEL", "glm-4")
    MOONSHOT_API_KEY: str = os.getenv("MOONSHOT_API_KEY", "")
    MOONSHOT_MODEL: str = os.getenv("MOONSHOT_MODEL", "moonshot-v1-8k")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    VOLCENGINE_API_KEY: str = os.getenv("VOLCENGINE_API_KEY", "")
    VOLCENGINE_MODEL: str = os.getenv("VOLCENGINE_MODEL", "ep-20250528XXXXXX-coding")
    VOLCENGINE_ENDPOINT: str = os.getenv("VOLCENGINE_ENDPOINT", "https://ark.cn-beijing.volces.com/api/v3")

    # Rate Limiting
    FREE_DAILY_LIMIT: int = int(os.getenv("FREE_DAILY_LIMIT", "1"))

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
