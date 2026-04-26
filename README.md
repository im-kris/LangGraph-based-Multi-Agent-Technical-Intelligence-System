# LangGraph Multi-Agent Tech Insight

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Framework-LangGraph-orange.svg" alt="Framework">
</p>

一个基于 LangGraph 构建的轻量级多智能体技术情报系统。

它会自动完成以下流程：
- 从 arXiv 拉取最新论文摘要
- 进行主题相关性筛选
- 生成结构化技术洞察
- 输出 Markdown 报告

## 项目亮点

- 多 Agent 协作链路：Scout -> Filter -> Analyst -> Publisher
- 真实数据源：arXiv Open API
- 强类型数据模型：Pydantic Schema 约束
- 可扩展工作流：基于状态机的节点编排

## 工作流说明

- Scout：根据 topic 从 arXiv 抓取数据
- Filter：筛选出更相关的内容
- Analyst：将内容整理为 Insight 结构化对象
- Publisher：将 Insight 渲染为报告并保存

## 快速开始

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 配置环境变量

在项目根目录创建 `.env` 文件：

```env
ZHIPUAI_API_KEY=your_api_key
ZHIPUAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
MODEL_NAME=glm-4-flash
ATI_QUERY=LLM agents
ATI_TOP_K=3
ATI_WORKFLOW=full
```

可选项：
- ATI_WORKFLOW=full：完整流程（默认）
- ATI_WORKFLOW=collect_only：只采集不分析

### 3) 启动项目

```bash
python -m auto_tech_insight.main
```

运行完成后：
- 终端会输出执行摘要
- 项目根目录会生成 `tech_report.md`

## 示例输出

```text
Done. Workflow=full, topic=LLM agents
Published items: 2
```

## 项目结构

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
│   ├── tools/
│   ├── memory/
│   ├── config.py
│   └── main.py
├── requirements.txt
├── test.py
└── README.md
```

## 常见问题

### 1) ModuleNotFoundError: No module named auto_tech_insight

请在项目根目录运行：

```bash
python -m auto_tech_insight.main
```

### 2) Published items 为 0

通常是状态字段未正确保留或上游筛选为空。
当前版本已将 insights 纳入状态定义，并修复了常见结构化输出问题。

### 3) 终端输出与编辑器代码不一致

请确认文件已保存到磁盘，再执行命令。Python 运行时读取的是磁盘文件。

## Roadmap

- [x] 接入 arXiv 实时检索
- [x] 输出结构化 Insight 报告
- [ ] 引入向量记忆去重（ChromaDB）
- [ ] 增加更多信源（GitHub / RSS）
- [ ] 支持消息平台推送

## 贡献

欢迎提 Issue 和 PR，一起完善这个多智能体技术情报系统。