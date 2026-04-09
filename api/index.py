from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import httpx
import json

# ============ Models ============
class CardInfo(BaseModel):
    name: str
    reversed: bool = False

class DivinationRequest(BaseModel):
    theme: str
    mbti: str
    question: Optional[str] = None
    cards: List[CardInfo]

class DivinationResponse(BaseModel):
    success: bool
    interpretation: str = ""
    quote: str = ""
    error: str = ""
    remaining_free: int = 0

# ============ FastAPI App ============
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Config ============
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "zhipu")
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_MODEL = os.getenv("ZHIPU_MODEL", "glm-4")
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY", "")
MOONSHOT_MODEL = os.getenv("MOONSHOT_MODEL", "moonshot-v1-8k")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
FREE_DAILY_LIMIT = int(os.getenv("FREE_DAILY_LIMIT", "1"))

# ============ Rate Limiter (in-memory) ============
import hashlib
from datetime import datetime

storage = {}

def get_rate_key(client_ip: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    ip_hash = hashlib.md5(client_ip.encode()).hexdigest()
    return f"{today}:{ip_hash}"

def check_and_increment(client_ip: str) -> tuple:
    key = get_rate_key(client_ip)
    current = storage.get(key, 0)
    if current >= FREE_DAILY_LIMIT:
        return False, 0
    else:
        storage[key] = current + 1
        return True, FREE_DAILY_LIMIT - (current + 1)

def get_remaining(client_ip: str) -> int:
    key = get_rate_key(client_ip)
    current = storage.get(key, 0)
    return max(0, FREE_DAILY_LIMIT - current)

# ============ AI Service ============
async def generate_interpretation(theme: str, mbti: str, question: str, cards: List[dict]) -> dict:
    cards_desc = []
    for card in cards:
        direction = "正位" if not card["reversed"] else "逆位"
        cards_desc.append(f"- {card['name']} ({direction})")
    cards_text = "\n".join(cards_desc)

    prompt = f"""你现在是一位资深的塔罗占卜师，深谙塔罗牌的象征意义，擅长用温暖共通的语言给求问者提供心灵指引。

求问者的MBTI类型是：{mbti}
占卜主题是：{theme}
{question if question else ''}

抽到的牌：
{cards_text}

请结合这位求问者的MBTI性格特质，给出一段带有共情能力、客观且具有指导意义的解读。

要求：
1. 字数控制在500字左右
2. 语气要温暖共情，符合对方的MBTI性格特质
3. 先解读每张牌的含义，再给出整体分析
4. 最后提炼一句核心箴言（一句话，30字以内），用于分享
5. 不要使用封建迷信词汇，强调这是心理启发和娱乐参考
6. 输出格式必须是JSON：{{"interpretation": "详细解读内容", "quote": "核心箴言"}}
"""

    async with httpx.AsyncClient(timeout=60.0) as client:
        if LLM_PROVIDER == "zhipu":
            return await _call_zhipu(client, prompt)
        elif LLM_PROVIDER == "moonshot":
            return await _call_moonshot(client, prompt)
        elif LLM_PROVIDER == "deepseek":
            return await _call_deepseek(client, prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")

async def _call_zhipu(client, prompt: str) -> dict:
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {"Authorization": f"Bearer {ZHIPU_API_KEY}", "Content-Type": "application/json"}
    data = {"model": ZHIPU_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 2048}
    response = await client.post(url, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    try:
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"interpretation": content, "quote": "听从内心，答案在你心中。"}

async def _call_moonshot(client, prompt: str) -> dict:
    url = "https://api.moonshot.cn/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MOONSHOT_API_KEY}", "Content-Type": "application/json"}
    data = {"model": MOONSHOT_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 2048}
    response = await client.post(url, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    try:
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"interpretation": content, "quote": "未来掌握在你自己手中。"}

async def _call_deepseek(client, prompt: str) -> dict:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    data = {"model": DEEPSEEK_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 2048}
    response = await client.post(url, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    try:
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"interpretation": content, "quote": "心之所向，素履以往。"}

# ============ Routes ============
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "ai-tarot"}

@app.get("/api/remaining")
async def remaining(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    return {"remaining": get_remaining(client_ip)}

@app.post("/api/divinate", response_model=DivinationResponse)
async def divinate(request: Request, data: DivinationRequest):
    client_ip = request.client.host if request.client else "127.0.0.1"
    allowed, remaining = check_and_increment(client_ip)
    if not allowed:
        return DivinationResponse(success=False, error="今日免费次数已用完，请明日再来", remaining_free=0)
    try:
        result = await generate_interpretation(data.theme, data.mbti, data.question, [c.model_dump() for c in data.cards])
        return DivinationResponse(success=True, interpretation=result.get("interpretation", ""), quote=result.get("quote", ""), remaining_free=remaining)
    except Exception as e:
        return DivinationResponse(success=False, error=f"AI生成失败: {str(e)}", remaining_free=remaining)
