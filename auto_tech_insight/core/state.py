from typing import TypedDict, List, Annotated
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
    
    # 3. 筛选后的高价值内容
    filtered_content: List[dict]

    # 4. 分析后的结构化见解
    insights: List[Insight]
    
    # 5. 最终生成的总结报告
    summary_report: str
    
    # 6. 任务状态追踪（用于决定下一步去哪）
    next_step: str