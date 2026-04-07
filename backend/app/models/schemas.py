from pydantic import BaseModel, Field
from typing import List, Optional


class TarotCard(BaseModel):
    id: int | str
    name: str
    reversed: bool
    meaning: Optional[str] = None


class DivinationRequest(BaseModel):
    theme: str = Field(..., description="Divination theme")
    mbti: str = Field(..., description="User MBTI type")
    question: Optional[str] = Field(None, description="User's specific question")
    cards: List[TarotCard] = Field(..., description="Drawn tarot cards")


class DivinationResponse(BaseModel):
    success: bool
    interpretation: Optional[str] = None
    quote: Optional[str] = None  # Key quote for sharing
    error: Optional[str] = None
    remaining_free: int = 1
