"""
  @Author:huchaofan
  @Time:2026/9/7
  @Desc:
"""
import asyncio
import json
import os
from typing import Any, Dict
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient
from loguru import logger
from langchain.agents import create_agent


def load_servers(file_path: str = "mcp.json") -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get("mcpServers", {})


async def run_chat_loop() -> None:
    servers_cfg = load_servers()
    mcp_client = MultiServerMCPClient(servers_cfg)
    tools = await mcp_client.get_tools()
    logger.info(f"已加载 {len(tools)} 个 MCP 工具： {[t.name for t in tools]}")

    llm = init_chat_model(
        model="deepseek-v4-pro",
        api_key=os.getenv("deepseek_api"),
        base_url="https://api.deepseek.com",
        # DeepSeek V4 官方唯一正确关闭思考模式写法
        extra_body={"thinking": {"type": "disabled"}}
    )

    # langchain1.0智能体要求
    agent = create_agent(
        model=llm,  # 带个模型
        tools=tools,  # 带个工具类
        system_prompt=(  # 带个提示词
            "你是AI智能运维助手，必须使用工具回答问题。"
            "可以调用天气、网页抓取工具，准确回答用户问题。"
        )
    )

    logger.info("\n🤖AI智能运维助手已启动，输入 'quit' 退出")
    while True:
        user_input = input("\n你: ").strip()

        if user_input.lower() == "quit":
            break

        try:
            result = await agent.ainvoke({"messages": [("user", user_input)]})
            print(f"\nAI: {result['messages'][-1].content}")
        except Exception as exc:
            logger.error(f"\n异常出错: {exc}")

    logger.info("======》会话已结束，Bye!")


if __name__ == "__main__":
    print("---------启动中---------\n")
    print("测试案例:"
          "① 北京天气如何：正常返回天气数据\n"
          "② MCP文档总结：返回完整文档摘要（警告为依赖提示，不影响）")

    asyncio.run(run_chat_loop())
