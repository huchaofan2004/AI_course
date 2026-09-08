"""
LangGraph 图输入输出模式和私有状态传递演示
功能要点：
1. 三层Schema拆分：完整内部状态state_schema / 外部输入input_schema / 对外输出output_schema
2. 外部入参过滤：多余传入key会被自动丢弃，无法篡改内部私有字段
3. 内部私有状态仅节点间可见，最终输出自动裁剪，不暴露中间临时数据
4. 并行双节点执行（RAG检索 + 联网搜索），汇总生成最终回答
"""
from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

# ====================== 1、定义三层状态结构 ======================
# 1. state_schema：整张图运行时完整全局状态，包含所有输入、中间、私有、输出字段
class MyStateFull(TypedDict):
    rag_result:str        # RAG知识库检索中间结果（内部中间值）
    web_search_result:str # 互联网搜索中间结果（内部中间值）
    final_answer:str      # 最终回答（对外输出字段）
    query:str             # 用户提问（唯一允许外部传入的参数）
    # a_new_key:str         # 节点内部生成的私有临时状态，外部不可控、默认不输出
    # phone:str


# 2. input_schema：约束外部调用时，仅能传入的参数集合
# 外部invoke只能传这里定义的key，多传的键会被LangGraph直接过滤扔掉
class InputSchema(TypedDict):
    query:str

# 3. output_schema：约束图执行结束后，对外返回的结果集合
# 内部一堆中间、私有字段都会被隐藏，只返回此处声明的key
class OutputSchema(TypedDict):
    final_answer:str

# ====================== 2、初始化状态图，绑定三层Schema ======================
# state_schema：内部完整容器；input_schema：入参白名单；output_schema：出参白名单
# 不写 input_schema 时：invoke 传什么键，就原样塞进全局 state；输入的校验、筛选规则会默认沿用 state_schema
# 写上 input_schema=InputSchema 后：LangGraph 内置逻辑开启入参筛选。
graph = StateGraph(
    state_schema=MyStateFull,
    input_schema=InputSchema, # 限定外部仅能传入query
    output_schema=OutputSchema
)

# ====================== 3、定义业务节点函数 ======================
# RAG检索节点：读取外部传入query，生成rag结果 + 写入私有状态a_new_key
def rag_search_node(state:MyStateFull):
    # state拿到的是完整MyStateFull全局状态字典
    print("=== rag_search_node 内部完整state ===")
    print(state)
    # 取出用户问题
    query = state["query"]
    # 模拟RAG检索结果
    rag_result = f"关于{query}的rag_result"
    # return字典会自动合并更新到全局state中
    # 同时更新中间结果rag_result 和 私有临时键a_new_key
    # state 里出现 a_new_key 是节点运行后才新增赋值，和 invoke 里写的 a_new_key: xxx 毫无关系。
    return {
        "rag_result": rag_result,
        "a_new_key": "a_new_key_value_66666"
    }

# 联网搜索节点：并行执行，只读取query，写入web检索中间结果
def web_search_node(state:MyStateFull):
    print("\n=== web_search_node 内部完整state ===")
    print(state)
    query = state["query"]
    web_search_result = f"关于{query}的web_search_result"
    # 仅更新自身业务中间值
    return {"web_search_result": web_search_result}

# 汇总回答节点：读取两个检索中间值，拼接生成最终对外答案
def final_answer_node(state:MyStateFull):
    print("\n=== final_answer_node 内部完整state ===")
    print(state)
    # 内部可以读取所有全局状态字段
    rag_result = state["rag_result"]
    web_search_result = state["web_search_result"]
    # 整合两份检索资料生成最终回复
    final_answer = f"LLM基于{rag_result}和{web_search_result}的最终回复"
    # 只更新对外输出字段final_answer
    return {"final_answer": final_answer}

# ====================== 4、挂载节点 & 搭建图执行拓扑 ======================
# 将三个业务函数注册为图中的节点
graph.add_node(rag_search_node)
graph.add_node(web_search_node)
graph.add_node(final_answer_node)

# 拓扑逻辑：
# START起点同时分发任务，并行启动rag和web两个检索节点
graph.add_edge(START, "rag_search_node")
graph.add_edge(START, "web_search_node")
# 两个并行节点全部执行完毕后，才能进入汇总节点
graph.add_edge("rag_search_node", "final_answer_node")
graph.add_edge("web_search_node", "final_answer_node")
# 汇总节点执行完成，流向END结束标识
graph.add_edge("final_answer_node", END)

# 编译图，生成可调用运行的实例
compiled_graph = graph.compile()

# ====================== 5、调用执行 & 验证Schema隔离效果 ======================
# 测试场景：外部故意多传input_schema未定义的a_new_key，验证会被过滤
# invoke() 传入的字典只会提取 InputSchema 中定义的键，其他多余键直接丢弃，不会合并写入全局 State。
#print("【调用invoke，外部额外传入a_new_key，该参数会被自动丢弃】")
res = compiled_graph.invoke({
    "query": "如何使用LangGraph,O(∩_∩)O",
    "phone": "13811112222",# 所有节点打印 state，自始至终都找不到 phone 这个键，证明直接被 input_schema 过滤拦截。
    "a_new_key": "a_new_key_value_xxx"  # input_schema无此字段，外部传入无效
})

# 打印最终返回结果：只会包含output_schema里的final_answer
print("\n【图最终对外返回结果（仅OutputSchema字段）】")
print('最终结果为', res)

# 打印ASCII字符流程图，直观查看并行结构
print("\n【图ASCII拓扑结构】")
print(compiled_graph.get_graph().print_ascii())
print()