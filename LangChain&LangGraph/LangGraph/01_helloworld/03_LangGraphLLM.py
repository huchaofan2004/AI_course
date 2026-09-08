"""
LangGraph 简单案例HelloWorld
    构建一个最小的有向图，流程是：START -> 模型节点 -> END
    状态、节点、边、图

"""
import os
from typing import TypedDict, Annotated
from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph


# 1. 定义状态State
class AtgiguState(TypedDict):
    # messages 是一个消息列表，Annotated + add_messages 表示支持自动追加消息（不是覆盖）
    messages: Annotated[list, add_messages]
    #          类型     类型本身  附加信息
    # list：声明字段的类型是列表
    # add_messages：附加的"元数据"：定义了当多个节点同时写入 messages 字段时如何合并数据


# 2. 定义大模型
llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen_api"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


# 3. 定义节点函数Nodes
def model_node(state: AtgiguState):
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}


# 4. 构建图结构
# 初始化图，指定State类型
graph = StateGraph(AtgiguState)

graph.add_node("model", model_node)

graph.add_edge(START, "model")
graph.add_edge("model", END)

# 5. 编译
app = graph.compile()

# 6. 运行
result = app.invoke({"messages": "请用一句话解释什么是 LangGraph"})
print(result)

# 模型的回答
print("模型回答：", result["messages"][-1].content)
print()

# 打印图ascii可视化结构
print(app.get_graph().print_ascii())