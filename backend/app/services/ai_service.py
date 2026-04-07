import json
import httpx
from typing import List, Dict
from app.core.config import settings


class AIService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.client = httpx.AsyncClient(timeout=60.0)

    def build_prompt(self, theme: str, mbti: str, question: str, cards: List[Dict]) -> str:
        """Build the prompt for LLM"""

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

        return prompt

    async def generate_interpretation(self, theme: str, mbti: str, question: str, cards: List[Dict]) -> Dict:
        """Generate interpretation via LLM"""

        prompt = self.build_prompt(theme, mbti, question, cards)

        if self.provider == "zhipu":
            return await self._call_zhipu(prompt)
        elif self.provider == "moonshot":
            return await self._call_moonshot(prompt)
        elif self.provider == "deepseek":
            return await self._call_deepseek(prompt)
        elif self.provider == "volcengine":
            return await self._call_volcengine(prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    async def _call_zhipu(self, prompt: str) -> Dict:
        """Call Zhipu GLM API"""
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": settings.ZHIPU_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        # Parse JSON from response
        try:
            # Clean up markdown code blocks if present
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            # Fallback: return the whole content as interpretation
            return {
                "interpretation": content,
                "quote": "听从内心，答案在你心中。"
            }

    async def _call_moonshot(self, prompt: str) -> Dict:
        """Call Kimi Moonshot API"""
        url = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.MOONSHOT_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": settings.MOONSHOT_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        try:
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            return {
                "interpretation": content,
                "quote": "未来掌握在你自己手中。"
            }

    async def _call_deepseek(self, prompt: str) -> Dict:
        """Call DeepSeek API"""
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": settings.DEEPSEEK_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        try:
            response = await self.client.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            content = result["choices"][0]["message"]["content"].strip()

            try:
                content = content.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(content)
                return parsed
            except json.JSONDecodeError:
                return {
                    "interpretation": content,
                    "quote": "心之所向，素履以往。"
                }
        except Exception as e:
            print(f"DeepSeek API call failed: {e}")
            raise e

    async def _call_volcengine(self, prompt: str) -> Dict:
        """Call Volcengine (ByteDance) API - compatible with OpenAI format"""
        url = f"{settings.VOLCENGINE_ENDPOINT}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.VOLCENGINE_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": settings.VOLCENGINE_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"].strip()

        try:
            content = content.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            return {
                "interpretation": content,
                "quote": "行而不辍，未来可期。"
            }

    async def close(self):
        await self.client.aclose()


ai_service = AIService()
