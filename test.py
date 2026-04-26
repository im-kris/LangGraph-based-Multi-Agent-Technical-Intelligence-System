import os
from pathlib import Path
from dotenv import dotenv_values, load_dotenv
from langchain_openai import ChatOpenAI

# 1. 强制定位当前脚本所在的目录，并寻找 .env
current_dir = Path(__file__).parent
dotenv_path = current_dir / ".env"

print(f"正在尝试加载配置文件: {dotenv_path}")

if not dotenv_path.exists():
    raise FileNotFoundError(f"没找到 .env 文件！请确保它在: {current_dir}")
else:
    loaded = load_dotenv(dotenv_path=dotenv_path, override=True, encoding="utf-8-sig")
    parsed_values = dotenv_values(dotenv_path, encoding="utf-8-sig")

    for key, value in parsed_values.items():
        if value is not None:
            os.environ[key] = value

    print(f"dotenv 加载结果: {loaded}")
    print(f"解析到的键: {sorted(k for k, v in parsed_values.items() if v is not None)}")

def test_zhipu_connection():
    api_key = os.getenv("ZHIPUAI_API_KEY")
    api_base = os.getenv("ZHIPUAI_BASE_URL")
    model_name = os.getenv("MODEL_NAME")

    # 简单的断言检查
    if not all([api_key, api_base, model_name]):
        print("❌ 错误: 环境变量读取不完整！")
        print(f"API_KEY: {'已获取' if api_key else '未获取'}")
        print(f"BASE_URL: {'已获取' if api_base else '未获取'}")
        print(f"MODEL_NAME: {'已获取' if model_name else '未获取'}")
        return

    # 初始化模型
    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=api_base
    )
    
    print(f"🚀 正在测试智谱 AI ({model_name})...")
    try:
        response = llm.invoke("你好，请回复'连接成功'")
        print("-" * 30)
        print(f"✅ 回复: {response.content}")
        print("-" * 30)
    except Exception as e:
        print(f"❌ 连接出错: {e}")

if __name__ == "__main__":
    test_zhipu_connection()