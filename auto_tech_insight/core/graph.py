from langgraph.graph import END, StateGraph

from auto_tech_insight.agents.analyst import run_analyst
from auto_tech_insight.agents.filter import FilterAgent
from auto_tech_insight.agents.publisher import run_publisher
from auto_tech_insight.agents.scout import ScoutAgent
from auto_tech_insight.config import Settings
from auto_tech_insight.core.schema import SourceItem
from auto_tech_insight.core.state import AgentState


def build_graph(settings: Settings):
    _ = settings

    scout_agent = ScoutAgent()
    filter_agent = FilterAgent()

    def workflow_node(state: AgentState) -> AgentState:
        """Initialize workflow mode and normalize input topic."""
        topic = state.get("topic") or state.get("query") or "AI"
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
            "filter": "filter",
            "analyze": "analyst",
            "analyst": "analyst",
            "publish": "publisher",
            "publisher": "publisher",
            "end": "end",
        }
        return mapping.get(next_step, "end")

    def scout_node(state: AgentState) -> AgentState:
        scout_result = scout_agent.run({"topic": state.get("topic", "AI")})

        if state.get("workflow") == "collect_only":
            next_step = "end"
        else:
            next_step = scout_result.get("next_step", "filter")

        return {
            "raw_data": scout_result.get("raw_data", []),
            "next_step": next_step,
        }

    def filter_node(state: AgentState) -> AgentState:
        filter_result = filter_agent.run(
            {
                "query": state.get("topic", ""),
                "items": state.get("raw_data", []),
            }
        )

        next_step = filter_result.get("next_step") or filter_result.get("next_action") or "analyst"
        return {
            "filtered_content": filter_result.get("filtered_content", []),
            "next_step": next_step,
        }

    def analyst_node(state: AgentState) -> AgentState:
        filtered_content = state.get("filtered_content", [])

        source_items: list[SourceItem] = []
        for idx, item in enumerate(filtered_content):
            if isinstance(item, SourceItem):
                source_items.append(item)
                continue

            if isinstance(item, dict):
                source_items.append(
                    SourceItem(
                        title=str(item.get("title", f"item-{idx + 1}")),
                        url=str(item.get("url", "mock://generated")),
                        content=str(item.get("content", "")),
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
    graph.add_node("filter", filter_node)
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
            "filter": "filter",
            "analyst": "analyst",
            "publisher": "publisher",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "filter",
        route_next_step,
        {
            "analyst": "analyst",
            "publisher": "publisher",
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
