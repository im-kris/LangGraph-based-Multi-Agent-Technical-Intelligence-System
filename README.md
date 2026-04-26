# LangGraph 多智能体技术情报系统

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Framework-LangGraph-orange.svg" alt="Framework">
</p>

一个基于 LangGraph 的多智能体技术情报系统，面向 arXiv 论文做“广度检索 - 人在回路选择 - 深度分析 - 报告输出”。

## 核心特点

- Scout 先做近一周的广度检索，支持多词扩展和并发请求
- 程序在检索后暂停，等待用户手动选择要分析的条目
- Analyst 只对选中的论文做深度分析
- Publisher 输出 Markdown 报告，并保留原文链接
- Scout 会把结果缓存到本地，便于重复选择与离线复用

## 工作流

```text
Workflow -> Scout -> Select -> Analyst -> Publisher -> Done
```

### 1. 广度检索

Scout 会基于主题词生成多个检索变体，并发调用 arXiv API，抓取最近一周内的所有匹配项。

输出形式：

```text
[序号] 标题 | 日期 | 分类
```

同时会写入两个本地文件：

- `.cache/auto_tech_insight/arxiv_sweep_<topic>.json`
- `.cache/auto_tech_insight/arxiv_sweep_<topic>.md`

### 2. 人在回路选择

Scout 完成后，程序会暂停等待用户输入选择指令，例如：

```text
分析 1, 3, 5
全选
退出
```

### 3. 定向分析

只有被用户选中的条目会进入 Analyst，生成结构化 Insight。

### 4. 报告输出

Publisher 会输出最终技术简报，并写入 `tech_report.md`。

## 目录结构

```text
.
├── auto_tech_insight/
│   ├── agents/
│   │   ├── analyst.py
│   │   ├── filter.py
│   │   ├── publisher.py
│   │   └── scout.py
│   ├── core/
│   │   ├── graph.py
│   │   ├── schema.py
│   │   └── state.py
│   ├── config.py
│   └── main.py
├── requirements.txt
├── tech_report.md
└── README.md
```

## 安装与运行

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 配置环境变量

在项目根目录创建 `.env`：

```env
ZHIPUAI_API_KEY=your_api_key
ZHIPUAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
MODEL_NAME=glm-4-flash

ATI_QUERY=LLM agents
ATI_WORKFLOW=full

ATI_LOOKBACK_DAYS=7
ATI_ARXIV_PAGE_SIZE=100
ATI_ARXIV_MAX_PAGES=20
ATI_CACHE_PATH=.cache/arxiv_sweep_cache.json
```

### 3) 启动程序

```bash
python -m auto_tech_insight.main
```

## 配置说明

- `ATI_QUERY`：默认主题词
- `ATI_WORKFLOW`：`full` 或 `collect_only`
- `ATI_LOOKBACK_DAYS`：回溯天数，默认 7
- `ATI_ARXIV_PAGE_SIZE`：每页抓取数量，默认 100
- `ATI_ARXIV_MAX_PAGES`：最多翻页数，默认 20
- `ATI_CACHE_PATH`：本地缓存路径

## 当前实现要点

- 检索逻辑不再受 `top_k` 限制
- 选择逻辑由用户在终端显式输入决定
- Analyst 只处理选中的摘要
- Publisher 会显示每条 Insight 的原文链接

## 路线图

- [x] 接入 arXiv 广度检索
- [x] 支持用户在回路选择
- [x] 只对选中条目做深度分析
- [x] 本地缓存扫描结果
- [ ] 支持分页式选择界面
- [ ] 增加更多数据源（RSS / GitHub Trending）
- [ ] 支持消息推送（飞书 / 钉钉 / Discord）

## 贡献

欢迎提 Issue 和 PR，一起继续完善这个多智能体技术情报系统。