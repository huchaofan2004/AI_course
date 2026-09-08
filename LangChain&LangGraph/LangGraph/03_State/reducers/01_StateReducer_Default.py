'''
如果未明确指定reducer函数，则默认对该键的更新是覆盖行为。
LangGraph Reducer函数演示 - 默认Reducer（覆盖更新）

直接覆盖：
如果没有为状态字段指定 Reducer，默认会覆盖更新。
也就是说，后执行的节点返回的值会直接覆盖先执行节点的值，
即下一个节点的State数据是上一个节点的返回。
'''

from typing import List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. 默认Reducer（覆盖更新）
# 未指定合并策略，默认覆盖，上一个节点的返回是下一个节点的值
class DefaultReducerState(TypedDict):
    foo: int
    bar: List[str]

def node_default_1(state: DefaultReducerState) -> DefaultReducerState:
    print("state[foo] =",state["foo"])
    print("state[bar] =",state["bar"])
    # 为什么叫「默认覆盖型 Reducer」
    # LangGraph 默认采用「字段级覆盖更新」，不是把整个状态字典替换，只修改你返回的字段，其余字段保留。
    # 针对同一个字段：新值直接覆盖旧值，不做拼接或者追加。
    # 节点返回 {键: 新值}，LangGraph 会增量合并：
    # 只更新返回中存在的 key，同 key 直接用新值覆盖旧值，状态里未被返回的 key 保持原值

    # 写法1
    return {"foo": 22}

    # 写法2 返回完整状态字典对象
    # state["foo"] = 33
    # return state  # 返回完整字典

def node_default_2(state: DefaultReducerState) -> dict:
    print()
    print("39line,state[foo] =",state["foo"])
    print("state[bar] =",state["bar"])
    return {"bar": ["bye1","bye2","bye3"]}


def main():
    print("-------默认Reducer（覆盖更新）演示:\n")
    builder = StateGraph(DefaultReducerState)

    builder.add_node("node1", node_default_1)
    builder.add_node("node2", node_default_2)

    builder.add_edge(START, "node1")
    builder.add_edge("node1", "node2")
    builder.add_edge("node2", END)

    graph = builder.compile()

    result = graph.invoke(input={"foo": 1, "bar": ["hi"]})

    print(f"执行结果: {result}\n")


if __name__ == "__main__":
    '''
    分步执行拆解
进入 node1：接收 foo=1, bar=["hi"]   
返回 {"foo": 22}
合并后新状态：foo=22（被覆盖），bar=["hi"]（保留）

进入 node2：接收 foo=22, bar=["hi"]  
返回 {"bar": ["bye1","bye2","bye3"]}
合并后最终状态：foo=22（保留），bar 被新列表覆盖
    '''
    main()






#data: Annotated[List[int], None]  #默认覆盖