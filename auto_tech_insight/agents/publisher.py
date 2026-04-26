from typing import List
from ..core.schema import Insight

def run_publisher(insights: List[Insight]):
    """发布者：将深度的见解转化为最终产物"""
    if not insights:
        print("📭 [Publisher] 没有收到任何见解，发布取消。")
        return

    print(f"📢 [Publisher] 正在生成技术简报，共 {len(insights)} 条内容...")
    
    report = "# 🚀 每日技术前沿洞察\n\n"
    for idx, insight in enumerate(insights):
        source_url = getattr(insight, "url", "")
        report += f"### {idx+1}. {insight.title}\n"
        report += f"**核心总结**: {insight.summary}\n\n"
        report += f"**原文链接**: {source_url}\n"
        report += f"**专家点评**: {insight.reasoning}\n"
        report += f"**影响等级**: {insight.impact_level} | **标签**: {', '.join(insight.keywords)}\n"
        report += "---\n"

    # 1. 保存到本地文件
    with open("tech_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print("✅ 报告已生成: tech_report.md")