import json
import os
import re
from typing import List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from ..core.schema import Insight, SourceItem


def _extract_json_object(text: str) -> str:
    """Extract a JSON object from plain text or fenced code blocks."""
    cleaned = (text or "").strip()
    if not cleaned:
        return ""

    # Prefer fenced JSON/code blocks when present.
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    # If there is extra prose, keep the outermost JSON object.
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start : end + 1]

    return cleaned

def run_analyst(items: List[SourceItem]) -> List[Insight]:
    """分析师核心逻辑：将抓取的原始信息转化为深度见解"""
    
    # 1. 初始化强逻辑模型（建议用智谱 glm-4 或更高）
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME", "glm-4"),
        openai_api_key=os.getenv("ZHIPUAI_API_KEY"),
        openai_api_base=os.getenv("ZHIPUAI_BASE_URL")
    )

    results: List[Insight] = []
    
    # 3. 逐条分析（实际工程中可以使用 asyncio.gather 并行处理提升效率）
    for item in items:
        messages = [
            SystemMessage(
                content=(
                    "你是一位资深技术专家。"
                    "请严格只返回一个 JSON 对象，"
                    "不得输出任何解释文字或 Markdown。"
                )
            ),
            HumanMessage(
                content=(
                    "请分析以下技术动态，并按字段返回 JSON：\n"
                    "- title: 技术动态标题\n"
                    "- summary: 100字以内总结\n"
                    "- impact_level: 高/中/低\n"
                    "- keywords: 字符串数组\n"
                    "- reasoning: 值得关注的原因\n\n"
                    f"输入标题：{item.title}\n"
                    f"输入内容：{item.content}"
                )
            ),
        ]

        try:
            response = llm.invoke(messages)
            raw_text = getattr(response, "content", "")
            json_text = _extract_json_object(raw_text)

            data = json.loads(json_text)
            if not data.get("url"):
                data["url"] = item.url
            insight = Insight.model_validate(data)
            results.append(insight)
        except Exception as e:
            print(f"⚠️ 分析条目 {item.title} 时出错: {e}")
            
            # 降级兜底：确保返回值仍满足 Insight 模型，避免流程中断
            results.append(
                Insight(
                    title=item.title,
                    summary=(item.content or "")[:100],
                    impact_level="中",
                    keywords=["fallback"],
                    reasoning="结构化解析失败，使用兜底策略生成基础见解。",
                    url=item.url,
                )
            )
            
    return results