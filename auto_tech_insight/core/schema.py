from typing import List

from pydantic import BaseModel, Field


class SourceItem(BaseModel):
    """Single raw research item."""

    title: str = Field(default="", description="Source title")
    url: str = Field(default="", description="Source link")
    content: str = Field(default="", description="Source summary or abstract")
    published_at: str = Field(default="", description="Published date in ISO format")
    category: str = Field(default="", description="arXiv category")


class Insight(BaseModel):
    """Single structured insight."""

    title: str = Field(description="Insight title")
    summary: str = Field(description="Concise summary")
    impact_level: str = Field(description="Impact level: high / medium / low")
    keywords: List[str] = Field(description="Keywords")
    reasoning: str = Field(description="Why it matters")
    url: str = Field(default="", description="Original source link")