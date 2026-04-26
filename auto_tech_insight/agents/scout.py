import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus

import feedparser

from auto_tech_insight.config import Settings


class ScoutAgent:
    def __init__(self, settings: Settings):
        self.lookback_days = settings.lookback_days
        self.page_size = settings.arxiv_page_size
        self.max_pages = settings.arxiv_max_pages
        self.cache_dir = Path(settings.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _to_datetime_utc(entry) -> datetime | None:
        parsed = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
        if not parsed:
            return None
        return datetime(*parsed[:6], tzinfo=timezone.utc)

    @staticmethod
    def _extract_category(entry) -> str:
        primary = getattr(entry, "arxiv_primary_category", None)
        if primary is not None:
            term = getattr(primary, "term", "")
            if term:
                return str(term)

        tags = getattr(entry, "tags", None) or []
        for tag in tags:
            term = getattr(tag, "term", None) if not isinstance(tag, dict) else tag.get("term")
            if term:
                return str(term)

        return "unknown"

    @staticmethod
    def _unique_queries(topic: str) -> list[str]:
        normalized = re.sub(r"\s+", " ", (topic or "").strip())
        tokens = [token for token in re.findall(r"[A-Za-z0-9\+\-]+", normalized.lower()) if len(token) >= 2]

        queries: list[str] = []

        def add_query(value: str) -> None:
            cleaned = value.strip()
            if cleaned and cleaned not in queries:
                queries.append(cleaned)

        add_query(normalized)
        if normalized and " " in normalized:
            add_query(f'"{normalized}"')
        for token in tokens:
            add_query(token)
        if len(tokens) > 1:
            add_query(" ".join(tokens))

        return queries or [normalized or "AI"]

    def _search_variant(self, query_text: str) -> list[dict]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=self.lookback_days)
        encoded_query = quote_plus(query_text)
        items: list[dict] = []
        seen_urls: set[str] = set()
        start = 0

        for _ in range(self.max_pages):
            url = (
                "http://export.arxiv.org/api/query?"
                f"search_query=all:{encoded_query}&start={start}&max_results={self.page_size}"
                "&sortBy=submittedDate&sortOrder=descending"
            )
            feed = feedparser.parse(url)
            entries = list(getattr(feed, "entries", []))

            if not entries:
                break

            page_in_window = False
            for entry in entries:
                published_at = self._to_datetime_utc(entry)
                if published_at is not None and published_at < cutoff:
                    continue

                page_in_window = True
                article_url = str(getattr(entry, "link", "")).strip()
                if article_url in seen_urls:
                    continue
                seen_urls.add(article_url)

                items.append(
                    {
                        "source": "arxiv",
                        "query": query_text,
                        "title": str(getattr(entry, "title", "")).strip(),
                        "url": article_url,
                        "content": str(getattr(entry, "summary", "")).strip(),
                        "published_at": published_at.isoformat() if published_at else "",
                        "category": self._extract_category(entry),
                    }
                )

            if not page_in_window:
                break

            start += self.page_size
            time.sleep(0.15)

        return items

    @staticmethod
    def _render_markdown(items: list[dict], topic: str, lookback_days: int) -> str:
        lines = [
            f"# Broad Sweep Results: {topic}",
            "",
            f"近 {lookback_days} 天检索结果，共 {len(items)} 条。",
            "",
        ]
        for index, item in enumerate(items, start=1):
            title = item.get("title", "").replace("|", "\\|")
            published_at = item.get("published_at", "")[:10] or "unknown"
            category = item.get("category", "unknown")
            lines.append(f"{index}. {title} | {published_at} | {category}")
        return "\n".join(lines).strip() + "\n"

    def _write_cache(self, topic: str, items: list[dict], markdown: str) -> Path:
        slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "_", topic).strip("_") or "sweep"
        cache_path = self.cache_dir / f"arxiv_sweep_{slug}.json"
        markdown_path = self.cache_dir / f"arxiv_sweep_{slug}.md"

        payload = {
            "topic": topic,
            "lookback_days": self.lookback_days,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "items": items,
        }

        cache_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        markdown_path.write_text(markdown, encoding="utf-8")
        return cache_path

    def _search_arxiv(self, topic: str) -> tuple[list[dict], str, Path]:
        queries = self._unique_queries(topic)

        all_items: list[dict] = []
        with ThreadPoolExecutor(max_workers=min(6, len(queries))) as executor:
            future_map = {executor.submit(self._search_variant, query_text): query_text for query_text in queries}
            for future in as_completed(future_map):
                all_items.extend(future.result())

        deduped: list[dict] = []
        seen_urls: set[str] = set()
        for item in sorted(all_items, key=lambda data: data.get("published_at", ""), reverse=True):
            url = item.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            deduped.append(item)

        markdown = self._render_markdown(deduped, topic, self.lookback_days)
        cache_path = self._write_cache(topic, deduped, markdown)
        return deduped, markdown, cache_path

    def run(self, state: dict):
        topic = state.get("topic", "AI")
        print(f"🔍 [Scout] 正在搜集关于 '{topic}' 的前沿信息...")

        try:
            raw_data, markdown, cache_path = self._search_arxiv(topic)
            print(f"🗂️ [Scout] 近 {self.lookback_days} 天检索到 {len(raw_data)} 条候选结果")
            print(f"📄 [Scout] Markdown 列表已保存到: {cache_path.with_suffix('.md')}")
            preview_count = min(20, len(raw_data))
            if preview_count:
                print("\n" + "\n".join(markdown.splitlines()[: preview_count + 4]))
        except Exception as exc:
            print(f"⚠️ [Scout] 调用 arXiv API 失败: {exc}")
            raw_data = []
            markdown = ""
            cache_path = self.cache_dir / "arxiv_sweep_failed.json"

        return {
            "raw_data": raw_data,
            "sweep_markdown": markdown,
            "cache_path": str(cache_path),
            "next_step": "select",
        }