from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    """文本分析请求模型"""
    text: str = Field(..., description="要分析的文本内容")
    include_classification: bool = Field(True, description="是否包含文本分类")
    include_entities: bool = Field(True, description="是否包含实体提取")
    include_summary: bool = Field(True, description="是否包含文本摘要")
    language: str = Field("zh", description="文本语言")


class TextAnalysisResponse(BaseModel):
    """文本分析响应模型"""
    original_text: str = Field(..., description="原始文本")
    classification: Optional[str] = Field(None, description="文本分类结果")
    entities: Optional[List[str]] = Field(None, description="提取的实体列表")
    summary: Optional[str] = Field(None, description="文本摘要")
    processing_time: float = Field(..., description="处理时间（秒）")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    version: str = Field(..., description="服务版本")
    dependencies: Dict[str, str] = Field(..., description="依赖服务状态") 