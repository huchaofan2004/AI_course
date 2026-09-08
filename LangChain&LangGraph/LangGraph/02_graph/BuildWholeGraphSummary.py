from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

'''图的构建流程：
1、定义状态
2、初始化一个StateGraph实例。
3、添加节点。
4、定义边，将所有的节点连接起来。
5、编译图。
6、执行工作流。'''

# 1. 定义状态机对象Obj
'''
TypedDict（推荐方式）: 
TypedDict是Python提供的一种类型提示工具，用于为字典（Dict）的键和值指定精确的类型信息。
状态类GraphStateObj继承TypedDict
'''
class GraphStateObj(TypedDict):
    process_data: dict

# 统一使用 GraphStateObj类对象 做类型注解
def input_node(state: GraphStateObj) -> GraphStateObj:
    print(f"input_node节点执行:  {state.get('process_data')}")
    # 合并原有数据，而非直接覆盖
    new_data = state["process_data"].copy()
    #print(new_data.keys())
    new_data["k1"] = "input_value张三"
    # LangGraph 默认采用「字段级覆盖更新」，不是把整个状态字典替换，只修改你返回的字段，其余字段保留。
    # 写法1
    return {"process_data": new_data}
    # 写法2 返回完整状态字典对象（新状态完全替换旧状态）
    #return state

def process_node(state: GraphStateObj) -> GraphStateObj:
    print(f"process_node节点执行:  {state.get('process_data')}")
    new_data = state["process_data"].copy()
    new_data["process"] = "process_value9527"
    return {"process_data": new_data}

def output_node(state: GraphStateObj) -> GraphStateObj:
    print(f"output_node节点执行:  {state.get('process_data')}")
    # 直接透传当前状态
    return state

# 2. 初始化状态图
graph = StateGraph(GraphStateObj)

# 3. 添加节点
graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

# 4. 定义边：执行顺序：START → input → process → output → END，线性执行。
graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)

# 5. 编译图
app = graph.compile()

# 6. 执行工作流
init_data = {"process_data": {"name": "测试数据", "value": 111111}}
result = app.invoke(init_data)
print(f"\n最后的结果是:{result}")

# ASCII 可视化
print("\n===== 图结构 ASCII =====")
print(app.get_graph().print_ascii())

# Mermaid 源码
print("\n===== Mermaid 代码 =====")
print(app.get_graph().draw_mermaid())