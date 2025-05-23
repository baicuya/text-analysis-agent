#!/usr/bin/env python3
"""
文本分析智能体 - 兼容性入口文件

这个文件保留了原始的简单使用方式，同时可以启动新的FastAPI服务。
"""

import os
import sys
from typing import TypedDict, List

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
load_dotenv()

# 兼容原版本的State定义
class State(TypedDict):
    text: str
    classification: str
    entities: List[str]
    summary: str


def create_simple_agent():
    """创建简单的文本分析智能体（原版本兼容）"""
    
    # 从环境变量获取配置
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
    base_url = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    model = os.getenv("OPENAI_MODEL", "qwen-plus")
    
    llm = ChatOpenAI(
        model=model,
        temperature=0,
        api_key=api_key,
        base_url=base_url
    )

    def classification_node(state: State):
        """文本分类节点"""
        prompt = PromptTemplate(
            input_variables=["text"],
            template="将以下文本分类到以下类别之一：新闻、博客、研究、其他。\n\n文本：{text}\n\n类别：（只输出类别本身，不要理由）"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        classification = llm.invoke([message]).content.strip()
        return {"classification": classification}

    def entity_extraction_node(state: State):
        """实体提取节点"""
        prompt = PromptTemplate(
            input_variables=["text"],
            template="从以下文本中提取所有实体（人物、组织、地点）。以逗号分隔列表形式返回结果。\n\n文本：{text}\n\n实体："
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        entities = llm.invoke([message]).content.strip().split(", ")
        return {"entities": entities}

    def summarize_node(state: State):
        """文本摘要节点"""
        summarization_prompt = PromptTemplate.from_template(
            """用一句话总结以下文本。\n\n文本：{text}\n\n摘要："""
        )
        chain = summarization_prompt | llm
        response = chain.invoke({"text": state["text"]})
        return {"summary": response.content}

    # 创建工作流
    workflow = StateGraph(State)
    workflow.add_node("classification_node", classification_node)
    workflow.add_node("entity_extraction", entity_extraction_node)
    workflow.add_node("summarization", summarize_node)
    
    workflow.set_entry_point("classification_node")
    workflow.add_edge("classification_node", "entity_extraction")
    workflow.add_edge("entity_extraction", "summarization")
    workflow.add_edge("summarization", END)
    
    return workflow.compile()


def run_simple_example():
    """运行简单示例（原版本兼容）"""
    print("🤖 文本分析智能体 - 简单模式")
    print("=" * 40)
    
    # 创建智能体
    app = create_simple_agent()
    
    # 测试文本
    sample_text = """
    我们最近更新了 2.5 Pro 版本，以帮助开发者构建更丰富、更互动的 Web 应用。很高兴看到用户和开发者的积极反馈，我们将继续根据用户反馈进行改进。

除了在学术基准测试中表现出色外，全新 2.5 Pro 目前在热门编程排行榜WebDev Arena中以 1415 的 ELO 得分领跑。此外，它在LMArena的所有排行榜中也都名列前茅，该排行榜评估人类在各个维度上的偏好。此外，凭借其 100 万个 token 上下文窗口，2.5 Pro 拥有一流的长上下文和视频理解性能。

自从整合了我们与教育专家共同构建的模型系列 LearnLM 以来，2.5 Pro 现已成为领先的学习模型。在评估其教学法和有效性的正面比较中，教育工作者和专家在各种场景中都更青睐 Gemini 2.5 Pro。此外，它在构建学习型 AI 系统的五项学习科学原则中，每一项都超越了顶级模型。

请参阅我们更新的Gemini 2.5 Pro 模型卡和Gemini 技术页面以了解更多信息。
    """
    
    print(f"📝 分析文本: {sample_text.strip()}")
    print("\n🔄 正在分析...")
    
    # 执行分析
    state_input = {"text": sample_text.strip()}
    result = app.invoke(state_input)
    
    # 输出结果
    print("\n📊 分析结果:")
    print(f"分类结果: {result['classification']}")
    print(f"实体列表: {result['entities']}")
    print(f"摘要内容: {result['summary']}")


def start_api_server():
    """启动FastAPI服务器"""
    print("🚀 启动文本分析API服务器...")
    
    try:
        from src.main import app
        import uvicorn
        
        # 从环境变量获取配置
        host = os.getenv("APP_HOST", "0.0.0.0")
        port = int(os.getenv("APP_PORT", "8000"))
        debug = os.getenv("APP_DEBUG", "false").lower() == "true"
        
        uvicorn.run(
            "src.main:app",
            host=host,
            port=port,
            reload=debug
        )
    except ImportError as e:
        print(f"❌ 无法启动API服务器: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        sys.exit(1)


def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "server":
            start_api_server()
        elif sys.argv[1] == "simple":
            run_simple_example()
        elif sys.argv[1] == "help":
            print("使用方法:")
            print("  python main.py simple   - 运行简单示例")
            print("  python main.py server   - 启动API服务器")
            print("  python main.py help     - 显示帮助信息")
        else:
            print(f"未知命令: {sys.argv[1]}")
            print("使用 'python main.py help' 查看帮助")
    else:
        # 默认行为：先尝试简单示例，然后提示用户
        print("🤖 文本分析智能体")
        print("=" * 30)
        print("选择运行模式:")
        print("1. 简单示例 (python main.py simple)")
        print("2. API服务器 (python main.py server)")
        print()
        
        choice = input("请选择 [1/2]: ").strip()
        
        if choice == "1":
            run_simple_example()
        elif choice == "2":
            start_api_server()
        else:
            print("无效选择，运行简单示例...")
            run_simple_example()


if __name__ == "__main__":
    main()
