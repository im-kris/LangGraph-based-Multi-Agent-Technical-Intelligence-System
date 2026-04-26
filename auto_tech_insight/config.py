from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    query: str = os.getenv("ATI_QUERY", "LLM agents")
    top_k: int = int(os.getenv("ATI_TOP_K", "3"))
    notion_token: str = os.getenv("NOTION_TOKEN", "")
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID", "")
    chroma_path: str = os.getenv("CHROMA_PATH", "./chroma_data")


def get_settings() -> Settings:
    return Settings()
