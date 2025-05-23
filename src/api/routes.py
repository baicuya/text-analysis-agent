from fastapi import APIRouter, HTTPException
from src.core.agent import TextAnalysisAgent
from src.core.models import TextAnalysisRequest, TextAnalysisResponse, HealthResponse

router = APIRouter()
agent = TextAnalysisAgent()


@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest) -> TextAnalysisResponse:
    """分析文本"""
    try:
        return agent.analyze(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """健康检查"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        dependencies={
            "openai": "connected",
            "database": "connected"
        }
    ) 