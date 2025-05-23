from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.core.agent import TextAnalysisAgent

router = APIRouter()

class TextAnalysisRequest(BaseModel):
    text: str
    include_classification: bool = True
    include_entities: bool = True
    include_summary: bool = True
    language: str = "zh"

class TextAnalysisResponse(BaseModel):
    classification: Optional[str] = None
    entities: Optional[List[str]] = None
    summary: Optional[str] = None

@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """文本分析端点"""
    try:
        agent = TextAnalysisAgent()
        result = agent.analyze(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 