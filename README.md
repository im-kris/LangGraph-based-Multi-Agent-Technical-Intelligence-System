# LangGraph Multi-Agent Tech Insight / 多智能体技术情报系统

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Framework-LangGraph-orange.svg" alt="Framework">
</p>

一个基于 LangGraph 的多智能体技术情报系统，面向 arXiv 论文做“广度检索 - 人在回路选择 - 深度分析 - 报告输出”。

A LangGraph-based multi-agent research intelligence system for arXiv papers.

当前版本的核心特点是：
- Scout 先做近一周的广度检索，支持多词扩展和并发请求
- 程序在检索后暂停，等待用户手动选择要分析的条目
- Analyst 只对选中的论文做深度分析
- Publisher 输出 Markdown 报告，并保留原文链接
- Scout 会把结果缓存到本地，便于重复选择与离线复用

Current highlights:
- Scout performs a broad sweep over the last week, using multi-term expansion and concurrent requests
- The program pauses after retrieval and waits for the user to pick items to analyze
- Analyst performs deep analysis only on selected papers
- Publisher outputs a Markdown report and keeps the source URLs
- Scout caches results locally for re-selection and offline reuse

## 工作流 / Workflow

```text
Workflow -> Scout -> Select -> Analyst -> Publisher -> Done
```

### 1. Broad Sweep / 广度检索

Scout expands the topic into multiple search variants, queries the arXiv API concurrently, and fetches all matches from the last seven days.

输出形式 / Output format:

```text
[序号] 标题 | 日期 | 分类
```

同时会写入两个本地文件：
- `.cache/auto_tech_insight/arxiv_sweep_<topic>.json`
- `.cache/auto_tech_insight/arxiv_sweep_<topic>.md`

The sweep is also written to two local files:
- `.cache/auto_tech_insight/arxiv_sweep_<topic>.json`
- `.cache/auto_tech_insight/arxiv_sweep_<topic>.md`

### 2. User-in-the-Loop / 人在回路选择

Scout 完成后，程序会暂停等待用户输入选择指令。

After the broad sweep, the program pauses and waits for a selection command.

```text
分析 1, 3, 5
全选
退出
```

### 3. Selective Analysis / 定向分析

Only the items selected by the user are sent to Analyst for structured insight generation.

### 4. Publishing / 报告输出

Publisher renders the final brief and saves it to `tech_report.md`.

## 目录结构 / Project Structure

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

## 安装与运行 / Installation and Run

### 1) 安装依赖 / Install dependencies

```bash
pip install -r requirements.txt
```

### 2) 配置环境变量 / Configure environment variables

在项目根目录创建 `.env`：

Create a `.env` file in the project root:

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

### 3) 启动程序 / Start the app

```bash
python -m auto_tech_insight.main
```

## 配置说明 / Configuration

- `ATI_QUERY`：默认主题词 / default topic
- `ATI_WORKFLOW`：`full` 或 `collect_only` / full or collect-only mode
- `ATI_LOOKBACK_DAYS`：回溯天数，默认 7 / lookback window in days, default 7
- `ATI_ARXIV_PAGE_SIZE`：每页抓取数量，默认 100 / page size, default 100
- `ATI_ARXIV_MAX_PAGES`：最多翻页数，默认 20 / max pages, default 20
- `ATI_CACHE_PATH`：本地缓存路径 / cache file path

## 当前实现要点 / Implementation notes

- 检索逻辑不再受 `top_k` 限制 / retrieval is no longer constrained by `top_k`
- 选择逻辑由用户在终端显式输入决定 / selection is explicitly made by the user in the terminal
- Analyst 只处理选中的摘要 / Analyst only processes selected abstracts
- Publisher 会显示每条 Insight 的原文链接 / Publisher displays each Insight's source URL

## Roadmap / 路线图

- [x] 接入 arXiv 广度检索
- [x] 支持用户在回路选择
- [x] 只对选中条目做深度分析
- [x] 本地缓存扫描结果
- [ ] 支持分页式选择界面
- [ ] 增加更多数据源（RSS / GitHub Trending）
- [ ] 支持消息推送（飞书 / 钉钉 / Discord）

## 贡献 / Contributing

欢迎提 Issue 和 PR，一起继续完善这个多智能体技术情报系统。

Issues and pull requests are welcome. Let's keep improving this multi-agent intelligence system together.