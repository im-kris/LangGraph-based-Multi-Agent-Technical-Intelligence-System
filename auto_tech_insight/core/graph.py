import json
import re
from pathlib import Path

from langgraph.graph import END, StateGraph

from auto_tech_insight.agents.analyst import run_analyst
from auto_tech_insight.agents.publisher import run_publisher
from auto_tech_insight.agents.scout import ScoutAgent
from auto_tech_insight.config import Settings
from auto_tech_insight.core.schema import SourceItem
from auto_tech_insight.core.state import AgentState


def build_graph(settings: Settings):
    scout_agent = ScoutAgent(settings)

    def workflow_node(state: AgentState) -> AgentState:
        topic = state.get("topic") or state.get("query") or settings.query or "AI"
        workflow = state.get("workflow", "full")
        return {
            "topic": topic,
            "workflow": workflow,
            "next_step": "scout",
        }

    def route_next_step(state: AgentState) -> str:
        next_step = str(state.get("next_step", "end")).lower()
        mapping = {
            "scout": "scout",
            "select": "select",
            "analyze": "analyst",
            "analyst": "analyst",
            "publish": "publisher",
            "publisher": "publisher",
            "end": "end",
        }
        return mapping.get(next_step, "end")

    def scout_node(state: AgentState) -> AgentState:
        scout_result = scout_agent.run({"topic": state.get("topic", settings.query)})

        if state.get("workflow") == "collect_only":
            next_step = "end"
        else:
            next_step = scout_result.get("next_step", "select")

        return {
            "raw_data": scout_result.get("raw_data", []),
            "sweep_markdown": scout_result.get("sweep_markdown", ""),
            "cache_path": scout_result.get("cache_path", ""),
            "next_step": next_step,
        }

    def _load_cached_items(state: AgentState) -> list[dict]:
        cache_path = state.get("cache_path", "")
        if cache_path:
            path = Path(cache_path)
            if path.exists():
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    items = payload.get("items", [])
                    if isinstance(items, list):
                        return items
                except Exception:
                    pass
        return list(state.get("raw_data", []))

    def _parse_selection(user_input: str, total: int) -> list[int] | None:
        text = (user_input or "").strip().lower()
        if not text:
            return None

        if any(keyword in text for keyword in ("全选", "all", "全部")):
            return list(range(1, total + 1))

        if any(keyword in text for keyword in ("q", "quit", "exit", "退出", "取消")):
            return []

        text = re.sub(r"^(分析|选择|select)\s*", "", text)
        tokens = re.split(r"[\s,，;；]+", text)

        selected: list[int] = []
        for token in tokens:
            if not token:
                continue
            range_match = re.fullmatch(r"(\d+)\s*[-~]\s*(\d+)", token)
            if range_match:
                start, end = int(range_match.group(1)), int(range_match.group(2))
                if start > end:
                    start, end = end, start
                selected.extend(list(range(start, end + 1)))
                continue
            if token.isdigit():
                selected.append(int(token))
                continue
            return None

        selected = sorted(set(index for index in selected if 1 <= index <= total))
        return selected if selected else None

    def _render_preview(items: list[dict], limit: int = 20) -> str:
        lines = ["# Broad Sweep Results", ""]
        preview_items = items[:limit]
        for index, item in enumerate(preview_items, start=1):
            title = str(item.get("title", "")).replace("|", "\\|")
            published_at = str(item.get("published_at", ""))[:10] or "unknown"
            category = str(item.get("category", "unknown"))
            lines.append(f"{index}. {title} | {published_at} | {category}")
        if len(items) > limit:
            lines.append("")
            lines.append(f"... 还有 {len(items) - limit} 条结果已写入缓存文件")
        return "\n".join(lines)

    def select_node(state: AgentState) -> AgentState:
        items = _load_cached_items(state)
        cache_path = state.get("cache_path", "")

        if not items:
            print("📭 [Select] 没有检索到任何候选项。")
            return {
                "selected_items": [],
                "selected_indices": [],
                "filtered_content": [],
                "next_step": "end",
            }

        print("\n" + _render_preview(items))
        if cache_path:
            print(f"\n📄 完整 Markdown 列表与 JSON 缓存已保存到: {cache_path}")

        while True:
            user_input = input("\n请输入要分析的序号，例如 '分析 1, 3, 5' 或 '全选'：").strip()
            selected_indices = _parse_selection(user_input, len(items))
            if selected_indices is not None:
                break
            print("输入无法识别，请重新输入。")

        if not selected_indices:
            print("已取消选择，流程结束。")
            return {
                "selected_items": [],
                "selected_indices": [],
                "filtered_content": [],
                "next_step": "end",
            }

        selected_items = [items[index - 1] for index in selected_indices]
        print(f"✅ [Select] 已选择 {len(selected_items)} 条，开始深度分析。")

        return {
            "selected_items": selected_items,
            "selected_indices": selected_indices,
            "filtered_content": selected_items,
            "next_step": "analyst",
        }

    def analyst_node(state: AgentState) -> AgentState:
        selected_items = state.get("selected_items") or state.get("filtered_content", [])

        source_items: list[SourceItem] = []
        for idx, item in enumerate(selected_items):
            if isinstance(item, SourceItem):
                source_items.append(item)
                continue

            if isinstance(item, dict):
                source_items.append(
                    SourceItem(
                        title=str(item.get("title", f"item-{idx + 1}")),
                        url=str(item.get("url", "mock://generated")),
                        content="\n".join(
                            part
                            for part in [
                                f"Published: {item.get('published_at', '')}" if item.get("published_at") else "",
                                f"Category: {item.get('category', '')}" if item.get("category") else "",
                                str(item.get("content", "")),
                            ]
                            if part
                        ),
                        published_at=str(item.get("published_at", "")),
                        category=str(item.get("category", "")),
                    )
                )
                continue

            source_items.append(
                SourceItem(
                    title=f"item-{idx + 1}",
                    url="mock://generated",
                    content=str(item),
                )
            )

        insights = run_analyst(source_items)
        return {
            "insights": insights,
            "summary_report": "\n\n".join(i.summary for i in insights),
            "next_step": "publisher",
        }

    def publisher_node(state: AgentState) -> AgentState:
        run_publisher(state.get("insights", []))
        return {"next_step": "end"}

    graph = StateGraph(AgentState)
    graph.add_node("workflow", workflow_node)
    graph.add_node("scout", scout_node)
    graph.add_node("select", select_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("publisher", publisher_node)

    graph.set_entry_point("workflow")
    graph.add_conditional_edges(
        "workflow",
        route_next_step,
        {
            "scout": "scout",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "scout",
        route_next_step,
        {
            "select": "select",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "select",
        route_next_step,
        {
            "analyst": "analyst",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "analyst",
        route_next_step,
        {
            "publisher": "publisher",
            "end": END,
        },
    )
    graph.add_edge("publisher", END)

    return graph.compile()