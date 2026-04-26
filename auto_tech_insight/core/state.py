from typing import Annotated, List, TypedDict
import operator

from .schema import Insight


class GraphState(TypedDict, total=False):
    query: str
    top_k: int
    items: list
    insights: list

class AgentState(TypedDict, total=False):
    # 0. 工作流模式（full / collect_only）
    workflow: str

    # 1. 原始输入：比如用户想关注的关键词
    topic: str
    
    # 2. 搜索到的原始数据列表
    # Annotated[..., operator.add] 的意思是：当多个 Agent 往里写数据时，是“追加”而不是“覆盖”
    raw_data: Annotated[List[dict], operator.add]

    # 2.1 扫描阶段生成的 Markdown 列表
    sweep_markdown: str

    # 2.2 扫描结果的本地缓存路径
    cache_path: str
    
    # 3. 用户选择后的内容（仍沿用 filtered_content，避免大范围改动）
    filtered_content: List[dict]

    # 3.1 用户显式选择的条目
    selected_items: List[dict]

    # 3.1 用户选择的序号
    selected_indices: List[int]

    # 4. 分析后的结构化见解
    insights: List[Insight]
    
    # 5. 最终生成的总结报告
    summary_report: str
    
    # 6. 任务状态追踪（用于决定下一步去哪）
    next_step: str