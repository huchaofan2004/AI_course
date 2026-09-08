"""
  @Author:huchaofan
  @Time:2026/9/8
  @Desc:
"""
from typing import TypedDict


# 定义状态对象Obj，等价于业务实体entity，或者叫当前数据快照
class GraphStateObj(TypedDict):
    process_data: dict


if __name__ == "__main__":
    obj = GraphStateObj()

    # 第一种写法：[key]
    obj["k1"] = "v1"  # 类似于 redis的 set k1 v1
    obj["k2"] = "v2"

    print(obj.keys())  # 拿到全部的key
    print(obj.values())  # 拿到全部的value

    # 写法2：get方法
    print(obj.get("k1"))
    print(obj.get("k3"))

    print(obj["k1"])
    # print(obj["k3"]) # keyError: "k3"

    # 遍历键
    for key in obj:
        print(key)

    # 遍历键+值
    for k, v in obj.items():
        print(k, v)
