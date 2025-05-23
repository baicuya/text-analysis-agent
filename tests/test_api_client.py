import requests
import json
import argparse
from typing import Dict, Any

def test_api(port: int = 8000):
    # API 基础 URL
    base_url = f"http://localhost:{port}/api/v1"
    
    # 测试健康检查
    print("\n=== 测试健康检查 ===")
    health_url = f"{base_url}/health"
    health_response = requests.get(health_url)
    print(f"状态码: {health_response.status_code}")
    print(f"响应内容: {health_response.json()}")
    
    # 测试文本分析
    print("\n=== 测试文本分析 ===")
    analyze_url = f"{base_url}/analyze"
    
    # 测试数据
    test_data = {
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
    
    # 发送请求
    analyze_response = requests.post(analyze_url, json=test_data)
    
    # 打印结果
    print(f"状态码: {analyze_response.status_code}")
    if analyze_response.status_code == 200:
        result = analyze_response.json()
        print("\n=== 分析结果 ===")
        print(f"分类: {result['classification']}")
        print(f"实体: {result['entities']}")
        print(f"摘要: {result['summary']}")
        print("===============")
    else:
        print(f"错误: {analyze_response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API 测试客户端")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口号（默认：8000）")
    args = parser.parse_args()
    test_api(args.port) 