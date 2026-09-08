# LangGraph概述

## 是什么

### 官网

LangGraph 概述：https://docs.langchain.org.cn/oss/python/langgraph/overview

### 一句话

基于 LangChain 构建的、面向智能体多轮交互 / 状态持久化 / 分支并行执行的图结构工作流框架

>  LangGraph = LangChain + 图编排 + 状态机

### LangChain的困境：

Chain太死板，无法优雅地处理循环和条件分支，不适合复杂任务。

Agent太自由，像个黑箱，难以控制，调试和保证稳定性。

## 能干嘛

彻底打破了“链”的束缚，引入了“图”的结构，让构建复杂AI应用的可能性，从一条直线，变成了一张网

## 去哪下

https://docs.langchain.org.cn/oss/python/langgraph/install

```bash
pip install -U langgraph
```

## 面试图：

构建LangGraph四大要素：State（状态）、Nodes（节点）、Edges（边）、Graph（图）

# HelloWorld快速入门

LangGraph是基于LangChain构建的，无论图结构多复杂，单独每个任务执行链路仍然是线性的，其背后仍然是靠着LangChain的Chain来实现的。

LangChain和LangGraph之间的关系：LangGraph是LangChain工作流的高级编排工具，其中“高级”之处就是LangGraph能按照图结构来编排工作流。

## 可视化

通过 `graph.get_graph()`方法可以获取图的结构信息，包括节点和边的详细信息。





















