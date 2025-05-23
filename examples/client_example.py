#!/usr/bin/env python3
"""
文本分析智能体客户端使用示例

展示如何通过Python客户端调用文本分析API
"""

import asyncio
import requests
import json
from typing import Dict, Any, Optional


class TextAnalysisClient:
    """文本分析API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        """
        初始化客户端
        
        Args:
            base_url: API基础URL
        """
        self.base_url = base_url.rstrip('/')
        
    def analyze_text(
        self,
        text: str,
        include_classification: bool = True,
        include_entities: bool = True,
        include_summary: bool = True,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """
        分析文本
        
        Args:
            text: 要分析的文本
            include_classification: 是否包含分类
            include_entities: 是否包含实体提取
            include_summary: 是否包含摘要
            language: 文本语言
            
        Returns:
            分析结果字典
        """
        url = f"{self.base_url}/analyze"
        payload = {
            "text": text,
            "include_classification": include_classification,
            "include_entities": include_entities,
            "include_summary": include_summary,
            "language": language
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败: {e}")
    
    def get_health(self) -> Dict[str, Any]:
        """获取服务健康状态"""
        url = f"{self.base_url}/health"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"健康检查失败: {e}")
    
    def get_service_info(self) -> Dict[str, Any]:
        """获取服务信息"""
        url = f"{self.base_url}/info"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取服务信息失败: {e}")


def main():
    """主函数 - 演示API使用"""
    
    # 创建客户端
    client = TextAnalysisClient()
    
    print("🚀 文本分析智能体客户端示例")
    print("=" * 50)
    
    # 1. 检查服务健康状态
    print("\n1. 检查服务健康状态...")
    try:
        health = client.get_health()
        print(f"   服务状态: {health['status']}")
        print(f"   版本: {health['version']}")
        print(f"   依赖状态: {health['dependencies']}")
    except Exception as e:
        print(f"   ❌ 健康检查失败: {e}")
        return
    
    # 2. 获取服务信息
    print("\n2. 获取服务信息...")
    try:
        info = client.get_service_info()
        print(f"   服务名称: {info['name']}")
        print(f"   支持的功能: {', '.join(info['capabilities'])}")
        print(f"   支持的语言: {', '.join(info['supported_languages'])}")
    except Exception as e:
        print(f"   ❌ 获取服务信息失败: {e}")
    
    # 3. 测试文本分析
    print("\n3. 文本分析示例...")
    
    test_texts = [
        {
            "text": "Anthropic的MCP（Model Context Protocol）是一个开源的强大工具，允许应用程序与各种系统的API进行无缝交互。",
            "description": "技术文档"
        },
        {
            "text": "今天北京天气晴朗，最高气温25度。市民们纷纷外出游玩，公园里人流如织。",
            "description": "新闻报道"
        },
        {
            "text": "我今天学习了Python编程，感觉非常有趣。打算继续深入学习机器学习相关的知识。",
            "description": "个人博客"
        }
    ]
    
    for i, example in enumerate(test_texts, 1):
        print(f"\n   示例 {i}: {example['description']}")
        print(f"   原文: {example['text']}")
        
        try:
            result = client.analyze_text(example['text'])
            
            print(f"   📊 分析结果:")
            print(f"      分类: {result.get('classification', 'N/A')}")
            print(f"      实体: {', '.join(result.get('entities', [])) if result.get('entities') else 'N/A'}")
            print(f"      摘要: {result.get('summary', 'N/A')}")
            print(f"      处理时间: {result.get('processing_time', 0):.2f}秒")
            
        except Exception as e:
            print(f"   ❌ 分析失败: {e}")
    
    # 4. 批量分析示例
    print("\n4. 批量分析性能测试...")
    test_text = "这是一个性能测试的示例文本。"
    
    import time
    start_time = time.time()
    success_count = 0
    total_requests = 5
    
    for i in range(total_requests):
        try:
            result = client.analyze_text(test_text)
            success_count += 1
        except Exception as e:
            print(f"   请求 {i+1} 失败: {e}")
    
    end_time = time.time()
    print(f"   完成 {success_count}/{total_requests} 个请求")
    print(f"   总耗时: {end_time - start_time:.2f}秒")
    print(f"   平均响应时间: {(end_time - start_time) / total_requests:.2f}秒")
    
    print("\n✅ 示例运行完成！")


if __name__ == "__main__":
    main() 