from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os


class FilterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME"),
            openai_api_key=os.getenv("ZHIPUAI_API_KEY"),
            openai_api_base=os.getenv("ZHIPUAI_BASE_URL"),
        )

    def run(self, state: dict):
        raw_items = state.get("items", [])
        query = state.get("query", "")

        print(f"⚖️ [Filter] 正在过滤关于 '{query}' 的 {len(raw_items)} 条信息...")

        prompt = f"""
        用户关注的主题是：{query}
        以下是抓取到的原始数据：{raw_items}

        请筛选出其中真正有技术含量的、与主题高度相关的条目。
        仅以 Python 列表格式返回索引编号，例如：[0, 2]
        """

        response = self.llm.invoke(
            [
                SystemMessage(content="你是一个严格的技术筛选专家。"),
                HumanMessage(content=prompt),
            ]
        )

        try:
            filtered = [raw_items[i] for i in eval(response.content) if i < len(raw_items)]
        except Exception:
            filtered = raw_items[:1]

        return {
            "items": [],
            "filtered_content": filtered,
            "next_action": "analyze",
        }
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

class FilterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME"),
            openai_api_key=os.getenv("ZHIPUAI_API_KEY"),
            openai_api_base=os.getenv("ZHIPUAI_BASE_URL")
        )

    def run(self, state: dict):
        raw_items = state.get("items", [])
        query = state.get("query", "")
        
        print(f"⚖️ [Filter] 正在过滤关于 '{query}' 的 {len(raw_items)} 条信息...")
        
        # 这里的 Prompt 是核心：让 LLM 充当裁判
        prompt = f"""
        用户关注的主题是：{query}
        以下是抓取到的原始数据：{raw_items}
        
        请筛选出其中真正有技术含量的、与主题高度相关的条目。
        仅以 Python 列表格式返回索引编号，例如：[0, 2]
        """
        
        response = self.llm.invoke([SystemMessage(content="你是一个严格的技术筛选专家。"), 
                                    HumanMessage(content=prompt)])
        
        # 逻辑：根据 LLM 返回的索引，提取数据
        # 注意：实际工程中这里需要加异常处理（防止 LLM 没返回列表）
        try:
            # 简单处理：这里我们假设 LLM 听话地返回了列表
            # 实习简历加分点：提到你在这里用了结构化解析
            filtered = [raw_items[i] for i in eval(response.content) if i < len(raw_items)]
        except:
            filtered = raw_items[:1] # 降级处理：至少保留一条
            
        return {
            "items": [], # 清空原始列表或保持不变
            "filtered_content": filtered,
            "next_action": "analyze" 
        }