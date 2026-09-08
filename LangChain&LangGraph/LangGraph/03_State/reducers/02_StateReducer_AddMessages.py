from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import HumanMessage, AIMessage


# 2. add_messages Reducer（消息列表专用）
class AddMessagesState(TypedDict):
    """
    引入的 Annotated 类型，它允许给类型添加额外的元数据。
    messages: Annotated[List, add_messages]
    表示:
    - messages 我的状态里只有一个字段叫 messages，类型是是 List列表类型,
    - add_messages  这里的 add_messages 是一个函数，用于修改 messages 列表
                    每当节点返回对 messages 的“局部更新”时，
                    请用 add_messages 规约器把它合并到旧列表上（追加，而不是覆盖）
    总结：
    节点永远只 return 增量字典，不用手动把旧列表读出来再拼接。
    add_messages 在后台帮你完成“追加”动作；如果换成默认规则，旧消息会被整份替换掉
    """
    # 列表消息场景 → 必须 Annotated[List, add_messages] 安全追加
    messages: Annotated[List, add_messages]



def chat_node_1(state: AddMessagesState) -> dict:
    return {"messages": [AIMessage(content="Hello from node 1")]}


def chat_node_2(state: AddMessagesState) -> dict:
    return {"messages": [AIMessage(content="Hello from node 2")]}


def run_demo():
    print("2. add_messages Reducer（消息列表专用）演示:\n")
    # 1 类似java new一个StateGraph图对象
    builder = StateGraph(AddMessagesState)
    # 2 add(node + edge)
    builder.add_node("chat1", chat_node_1)
    builder.add_node("chat2", chat_node_2)

    builder.add_edge(START, "chat1")
    builder.add_edge(START, "chat2")  # 并行执行
    builder.add_edge("chat1", END)
    builder.add_edge("chat2", END)
    # 3 编译compile
    graph = builder.compile()

    # 初始消息使用标准消息对象
    init_messages = [HumanMessage(content="Hi there!")]
    result = graph.invoke({"messages": init_messages})

    # 格式化输出，只展示核心内容，隐藏多余元数据
    #print("初始状态: {'messages': [('user', 'Hi there!')]}")
    print("执行结果:")
    for msg in result["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        print(f"('{role}', '{msg.content}')")
    print()

    print("*" * 60)

    # 打印图的ascii可视化结构
    print(graph.get_graph().print_ascii())


if __name__ == "__main__":
    run_demo()