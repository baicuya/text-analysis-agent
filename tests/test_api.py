import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
load_dotenv()  # 确保测试时也加载环境变量

from src.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

def test_analyze():
    data = {
        "text": """
        近日，OpenAI 发布了最新的 GPT-4 模型，该模型在多个基准测试中表现出色。
        微软公司作为 OpenAI 的主要合作伙伴，已经将 GPT-4 集成到了其产品中。
        同时，谷歌也推出了自己的 AI 模型 Gemini，与 OpenAI 展开竞争。
        这场 AI 领域的竞争正在推动整个行业的发展。
        """,
        "include_classification": True,
        "include_entities": True,
        "include_summary": True,
        "language": "zh"
    }
    resp = client.post("/api/v1/analyze", json=data)
    assert resp.status_code == 200
    result = resp.json()
    assert "classification" in result
    assert "entities" in result
    assert "summary" in result
    print("\n=== 分析结果 ===")
    print(f"分类: {result['classification']}")
    print(f"实体: {result['entities']}")
    print(f"摘要: {result['summary']}")
    print("===============")