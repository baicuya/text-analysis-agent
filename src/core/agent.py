import os
import time
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

from .models import TextAnalysisRequest, TextAnalysisResponse

class TextAnalysisAgent:
    """文本分析智能体"""
    def __init__(self):
        self.llm = self._create_llm()
        self.workflow = self._create_workflow()

    def _create_llm(self) -> ChatOpenAI:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        model = os.getenv("OPENAI_MODEL", "qwen-plus")
        print("API KEY:", api_key)
        print("BASE URL:", base_url)
        print("MODEL:", model)
        if not api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        return ChatOpenAI(
            model=model,
            temperature=0,
            api_key=api_key,
            base_url=base_url
        )

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(dict)
        workflow.add_node("classification", self._classification_node)
        workflow.add_node("entity_extraction", self._entity_extraction_node)
        workflow.add_node("summarization", self._summarization_node)
        workflow.set_entry_point("classification")
        workflow.add_edge("classification", "entity_extraction")
        workflow.add_edge("entity_extraction", "summarization")
        workflow.add_edge("summarization", END)
        return workflow.compile()

    def _classification_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="将以下文本分类到以下类别之一：新闻、博客、研究、其他。\n\n文本：{text}\n\n类别：（只输出类别本身，不要理由）"
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        classification = self.llm.invoke([message]).content.strip()
        new_state = dict(state)
        new_state["classification"] = classification
        return new_state

    def _entity_extraction_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="从以下文本中提取所有实体（人物、组织、地点）。以逗号分隔列表形式返回结果。\n\n文本：{text}\n\n实体："
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        entities = self.llm.invoke([message]).content.strip().split(", ")
        new_state = dict(state)
        new_state["entities"] = entities
        return new_state

    def _summarization_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="用一句话总结以下文本。\n\n文本：{text}\n\n摘要："
        )
        message = HumanMessage(content=prompt.format(text=state["text"]))
        summary = self.llm.invoke([message]).content.strip()
        new_state = dict(state)
        new_state["summary"] = summary
        return new_state

    def analyze(self, request: TextAnalysisRequest) -> TextAnalysisResponse:
        start_time = time.time()
        result = self.workflow.invoke({"text": request.text})
        response = TextAnalysisResponse(
            original_text=request.text,
            classification=result.get("classification") if request.include_classification else None,
            entities=result.get("entities") if request.include_entities else None,
            summary=result.get("summary") if request.include_summary else None,
            processing_time=time.time() - start_time,
            metadata={
                "model": os.getenv("OPENAI_MODEL", "qwen-plus"),
                "text_length": len(request.text)
            }
        )
        return response 