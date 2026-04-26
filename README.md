🚀 LangGraph-Multi-Agent-Tech-Insight
这是一个基于 LangGraph 构建的极简、轻量级多智能体自动化系统。 它能够像专业的情报团队一样，自动从 arXiv 发现前沿技术，完成语义过滤、深度分析，并输出结构化的技术报告。

Why this project? > 市面上大多数总结器只是简单的“Prompt + PDF”，而本项目展示了如何通过 State Machine（状态机） 实现多个 Agent 的复杂逻辑编排。

📌 核心特性 (Features)
🤖 多体协作: Scout (采集)、Filter (去噪)、Analyst (推演)、Publisher (发布) 四位一体。

📡 实时情报: 拒绝幻觉，数据源来自真实的 arXiv Open API。

🧩 强类型约束: 全链路采用 Pydantic 定义数据契约，确保 Agent 间传递的是对象而非模糊字符串。

📝 自动报告: 自动生成包含专家点评、影响等级（Impact Level）的 Markdown 周报。

🧱 架构设计 (Architecture)
系统采用 Directed Acyclic Graph (DAG) 有向无环图设计：

Scout Agent: 侦察兵。负责网络请求与 XML 结构化转换。

Filter Agent: 守门人。基于语义相关性评分，剔除 50%+ 的噪音数据。

Analyst Agent: 智囊团。执行逻辑推演，提取创新点并评估技术价值。

Publisher Agent: 书记官。执行数据持久化，输出最终产物。

🛠️ 快速开始 (Quick Start)
1. 克隆与安装
Bash
git clone https://github.com/im-kris/LangGraph-based-Multi-Agent-Technical-Intelligence-System.git
cd LangGraph-based-Multi-Agent-Technical-Intelligence-System
pip install -r requirements.txt
2. 配置 .env
在根目录创建 .env 文件，填入你的密钥：

代码段
ZHIPUAI_API_KEY="your_api_key"
MODEL_NAME="glm-4-flash" # 推荐使用 flash 版本，极低成本完成分析
ATI_TOP_K=3
3. 一键启动
Bash
python -m auto_tech_insight.main
📂 目录结构 (Folder Structure)
Plaintext
.
├── src/
│   ├── agents/          # 各个 Agent 的独立逻辑实现
│   ├── core/            # 核心 Schema 定义与 Graph 构建
│   └── main.py          # 系统统一入口
├── .env                 # 环境变量 (不进入 Git)
├── .gitignore           # 忽略文件配置
└── README.md            # 项目文档
📈 路线图 (Roadmap)
[x] 基于 LangGraph 的多智能体闭环流转

[x] 接入 arXiv 真实数据源

[ ] 接入 ChromaDB 实现长短期记忆（去重）

[ ] 增加多维数据源 (GitHub Trending / RSS)

[ ] 支持飞书、钉钉、Discord Bot 实时推送

🤝 交流与贡献 (Contact)
如果你觉得这个项目对你理解 LangGraph 或 Multi-Agent 架构有帮助，欢迎 Star ⭐️ 鼓励！

Author: im-kris

Project: LangGraph-based-Multi-Agent-System