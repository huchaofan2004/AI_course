"""
  @Author:huchaofan
  @Time:2026/9/7
  @Desc:mcp案例实战
"""
import json
import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from loguru import logger
from redisvl.cli import mcp

# 案例跑在python3.12版本下

# 加载 .env 文件
load_dotenv()  # 默认加载当前目录下的 .env 文件

# 读取天气环境变量
api_key = os.getenv("Weather_KEY")

# 创建fastmcp实例。用于启动天气服务器SSE服务
# 仅本机能访问
# mcp = FastMCP("WeatherServerSSE", host="127.0.0.1", port=8080)
# 同一 WiFi 下的同事/家人都能访问
mcp = FastMCP("WeatherServerSSE", host="0.0.0.0", port=8000)


@mcp.tool()  # tool calling的加强版
def get_weather(city: str) -> str:
    # 第一步 构建请求url
    url = "https://api.openweathermap.org/data/2.5/weather"

    # 第二步 设置查询参数，包括城市名、API Key、单位和语言
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "zh-cn",
    }

    # 第三步 发送 GET请求 获取天气数据
    response = httpx.get(url, params=params, timeout=30)

    # 第四步 解析响应内容为 JSON 并序列化为字符串返回
    data = response.json()
    logger.info(f"查询{city} 天气结果：{data}")
    # json.dumps() 把一个 Python 对象（比如字典、列表）序列化（或者叫转换）成一个 JSON 格式的字符串
    return json.dumps(data)


if __name__ == "__main__":
    logger.info("启动 MCP SSE 天气服务器，监听 http://0.0.0.0:8000/sse")
    # 运行MCP客户端，使用Server-Sent Events(SSE) 作为传输协议
    mcp.run(transport="sse")
    # mcp.run(transport="stdio")

"""
适配 MCP SSE 的流式处理特性：
200 OK：请求处理完成，服务器立即返回最终结果
202 Accepted：请求已接收并受理，服务器会在后台处理（比如：调用工具、执行 MCP 指令），处理完成后通过 SSE 流式将结果推送给客户端
"""