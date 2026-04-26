from pydantic import BaseModel, Field
from typing import List


class SourceItem(BaseModel):
    """单条原始技术信息模型"""
    title: str = Field(default="", description="原始信息标题")
    url: str = Field(default="", description="来源链接")
    content: str = Field(default="", description="原始内容")


class Insight(BaseModel):
    """单条技术见解的模型"""
    title: str = Field(description="技术动态的标题")
    summary: str = Field(description="核心内容的高度凝练总结（100字以内）")
    impact_level: str = Field(description="影响等级：高/中/低")
    keywords: List[str] = Field(description="技术关键词标签")
    reasoning: str = Field(description="为什么这项技术值得关注？它的创新点在哪？")
    url: str = Field(default="", description="原始来源链接")
    url: str = Field(description="原始论文链接")