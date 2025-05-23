import pytest
import os
from dotenv import load_dotenv
load_dotenv()  # 确保测试时也加载环境变量

# 直接设置环境变量
os.environ["OPENAI_API_KEY"] = "sk-d62364dd57a94142a3233a7b759cbc37"
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
os.environ["OPENAI_MODEL"] = "qwen-plus"

# 打印环境变量
print("\n=== 环境变量 ===")
print("API KEY:", os.getenv("OPENAI_API_KEY"))
print("BASE URL:", os.getenv("OPENAI_BASE_URL"))
print("MODEL:", os.getenv("OPENAI_MODEL"))
print("================\n")

from src.core.agent import TextAnalysisAgent
from src.core.models import TextAnalysisRequest, TextAnalysisResponse

@pytest.fixture
def agent():
    return TextAnalysisAgent()

def test_analyze_basic(agent):
    req = TextAnalysisRequest(
        text="北京是中国的首都。",
        include_classification=True,
        include_entities=True,
        include_summary=True,
        language="zh"
    )
    resp = agent.analyze(req)
    assert resp.classification in ["新闻", "博客", "研究", "其他"]
    assert isinstance(resp.entities, list)
    assert isinstance(resp.summary, str)
    assert resp.processing_time > 0

def test_analyze_response(agent):
    req = TextAnalysisRequest(
        text="北京是中国的首都。",
        include_classification=True,
        include_entities=True,
        include_summary=True,
        language="zh"
    )
    resp = agent.analyze(req)
    assert isinstance(resp, TextAnalysisResponse)
    assert resp.original_text == req.text
    assert resp.classification in ["新闻", "博客", "研究", "其他"]
    assert isinstance(resp.entities, list)
    assert isinstance(resp.summary, str)
    assert resp.processing_time > 0