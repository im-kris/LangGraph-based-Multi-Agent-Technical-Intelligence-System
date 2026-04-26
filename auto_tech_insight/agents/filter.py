import re


class FilterAgent:
    def __init__(self):
        pass

    @staticmethod
    def _query_tokens(query: str) -> list[str]:
        tokens = re.findall(r"[a-zA-Z0-9]+", (query or "").lower())
        return [token for token in tokens if len(token) >= 2]

    @staticmethod
    def _is_related(item: dict, tokens: list[str]) -> bool:
        if not tokens:
            return True

        text = f"{item.get('title', '')} {item.get('content', '')}".lower()
        return any(token in text for token in tokens)

    def run(self, state: dict):
        raw_items = state.get("items", [])
        query = state.get("query", "")
        tokens = self._query_tokens(query)

        print(f"⚖️ [Filter] 正在过滤关于 '{query}' 的 {len(raw_items)} 条信息...")

        filtered = [item for item in raw_items if self._is_related(item, tokens)]
        if not filtered:
            filtered = raw_items

        print(f"✅ [Filter] 保留与主题相关的 {len(filtered)} 条信息")

        return {
            "items": [],
            "filtered_content": filtered,
            "next_action": "analyze",
        }