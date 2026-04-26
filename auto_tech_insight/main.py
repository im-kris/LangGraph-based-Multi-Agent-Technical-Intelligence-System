from auto_tech_insight.config import get_settings
from auto_tech_insight.core.graph import build_graph
import os


def main() -> None:
    settings = get_settings()
    app = build_graph(settings)

    topic = os.getenv("ATI_TOPIC", settings.query)
    workflow = os.getenv("ATI_WORKFLOW", "full")

    result = app.invoke(
        {
            "topic": topic,
            "workflow": workflow,
            "next_step": "scout",
        }
    )

    insights = result.get("insights", [])
    print(f"Done. Workflow={workflow}, topic={topic}")
    print("Published items:", len(insights))

    summary_report = result.get("summary_report")
    if summary_report:
        print("\nSummary Report:")
        print(summary_report)


if __name__ == "__main__":
    main()
