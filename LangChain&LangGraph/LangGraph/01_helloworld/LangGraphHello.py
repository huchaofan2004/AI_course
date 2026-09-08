# pip install -U langgraph
# pip install grandalf

from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 状态、节点、边、图

# 1. 定义State对象（官网推荐必选，but可选）
class HelloState(TypedDict):
    name: str
    greeting: str


# 每一个普通方法就叫节点，就是干活的函数
# 2. 定义节点Node（干活的函数）
def greet(helloState: HelloState) -> dict:
    name = helloState["name"]
    return {"greeting": f"Hello, {name}!"}
    # return helloState


def add_emoji(helloState: HelloState) -> dict:
    greeting = helloState["greeting"]
    return {"greeting": greeting + "。。。❤️"}


# 3. 构建图Graph
# 状态图
graph = StateGraph(HelloState)
# 添加节点
graph.add_node("greeting", greet)
graph.add_node("add_emoji", add_emoji)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

# 4. 编译图
app = graph.compile()

# 5. 运行
# invoke() 方法只能接收状态字典作为核心参数
result = app.invoke({"name": "张三"})
print(result)
print()
print(result["greeting"])

# 6. 打印图的边和节点信息 graph.get_graph()
# 打印图的 ascii可视化结构
print(app.get_graph().print_ascii())
print("-" * 20)

# 打印图的Mermaid代码可视化结构并通过processon编辑器查看
print(app.get_graph().draw_mermaid())
