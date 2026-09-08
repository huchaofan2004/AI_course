"""
  @Author:huchaofan
  @Time:2026/9/8
  @Desc: LangGraph标准版本写法第二版
"""
from typing import TypedDict
from langgraph.constants import END, START
from langgraph.graph import StateGraph


# 1. 定义状态 XxxState
class State(TypedDict):
    content: str


# 2. 初始化图
graph_builder = StateGraph(State)


# 3. 添加节点
def node_a(state: State) -> State:
    return {"content": "处理完成v2"}

graph_builder.add_node("A", node_a)

# 4. 连边（使用 START / END 常量）
graph_builder.add_edge(START, "A")
graph_builder.add_edge("A", END)

# 5. 设置入口（必选）不需要在调用 set_entry_point，START 边已指定入口
# 6. 出口这里用 END 全局常量，无需额外 set_finish_point

# 7. 编译图
graph = graph_builder.compile()

# 8. 执行工作流
res = graph.invoke({"content": "start"})
print(res)