import os
from urllib.parse import quote_plus

import feedparser

class ScoutAgent:
    def __init__(self):
        self.max_results = int(os.getenv("ATI_TOP_K", "3"))

    def _search_arxiv(self, topic: str) -> list[dict]:
        query = quote_plus(topic)
        url = (
            "http://export.arxiv.org/api/query?"
            f"search_query=all:{query}&start=0&max_results={self.max_results}"
            "&sortBy=submittedDate&sortOrder=descending"
        )

        feed = feedparser.parse(url)
        items: list[dict] = []

        for entry in feed.entries:
            items.append(
                {
                    "source": "arxiv",
                    "title": str(getattr(entry, "title", "")).strip(),
                    "url": str(getattr(entry, "link", "")).strip(),
                    "content": str(getattr(entry, "summary", "")).strip(),
                }
            )

        return items

    def run(self, state: dict):
        """
        Scout 的逻辑：从 arXiv 检索与主题相关的最新论文摘要。
        """
        topic = state.get("topic", "AI")
        print(f"🔍 [Scout] 正在搜集关于 '{topic}' 的前沿信息...")

        try:
            raw_data = self._search_arxiv(topic)
        except Exception as e:
            print(f"⚠️ [Scout] 调用 arXiv API 失败: {e}")
            raw_data = []

        return {
            "raw_data": raw_data,
            "next_step": "filter"  # 告诉中枢，下一步该去筛选了
        }