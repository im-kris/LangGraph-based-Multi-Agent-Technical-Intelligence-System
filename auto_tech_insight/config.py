from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    query: str = os.getenv("ATI_QUERY", "LLM agents")
    top_k: int = int(os.getenv("ATI_TOP_K", "10"))
    lookback_days: int = int(os.getenv("ATI_LOOKBACK_DAYS", "7"))
    arxiv_page_size: int = int(os.getenv("ATI_ARXIV_PAGE_SIZE", "100"))
    arxiv_max_pages: int = int(os.getenv("ATI_ARXIV_MAX_PAGES", "20"))
    cache_dir: str = os.getenv("ATI_CACHE_DIR", ".cache/auto_tech_insight")
    notion_token: str = os.getenv("NOTION_TOKEN", "")
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID", "")
    chroma_path: str = os.getenv("CHROMA_PATH", "./chroma_data")


def get_settings() -> Settings:
    return Settings()
