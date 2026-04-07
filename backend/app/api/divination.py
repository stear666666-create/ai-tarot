from fastapi import APIRouter, Request
from app.models.schemas import DivinationRequest, DivinationResponse
from app.services.ai_service import ai_service
from app.core.limiter import rate_limiter

router = APIRouter()


@router.post("/divinate", response_model=DivinationResponse)
async def divinate(request: Request, data: DivinationRequest):
    # Get client IP
    client_ip = request.client.host if request.client else "127.0.0.1"

    # Check rate limit
    allowed, remaining = rate_limiter.check_and_increment(client_ip)
    if not allowed:
        return DivinationResponse(
            success=False,
            error="今日免费次数已用完，请明日再来，或观看广告获得更多次数",
            remaining_free=0
        )

    try:
        result = await ai_service.generate_interpretation(
            theme=data.theme,
            mbti=data.mbti,
            question=data.question,
            cards=[c.model_dump() for c in data.cards]
        )

        return DivinationResponse(
            success=True,
            interpretation=result.get("interpretation", ""),
            quote=result.get("quote", ""),
            remaining_free=remaining
        )
    except Exception as e:
        print(f"Error generating interpretation: {e}")
        return DivinationResponse(
            success=False,
            error="AI生成失败，请稍后重试",
            remaining_free=remaining
        )


@router.get("/remaining")
async def get_remaining(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    remaining = rate_limiter.get_remaining(client_ip)
    return {"remaining": remaining}
