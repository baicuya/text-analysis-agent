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
        "text": "上海是中国的经济中心。",
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