"""D1 复测（阶段 1 · 第 1 天）—— 关掉一切参考，只考"能不能推出来"

规则：
    1. 每题**先在注释里写预测**，再运行 python retest.py。
    2. 本文件**故意不给自检清单**（和 variants.py 不同）—— 直接推，直接把预测发我。
    3. 这四问的答案不在 day01.py / README / demo_reference.py / variants.py 任何一处，
       靠模型推，不靠记忆。错了不要紧，错了我就知道该补哪里。
"""

from __future__ import annotations

import copy
from typing import Any


def q1_deepcopy_version() -> None:
    """复测 1 · 把 v2 的 `.copy()` 换成 `deepcopy`，结论还成立吗？"""
    t: dict[str, Any] = {"tags": ["x"], "id": 1}
    s: dict[str, Any] = copy.deepcopy(t)

    s["tags"].append("y")
    s["id"] = 99

    # 预测：t = ?
    # 预测：s = ?
    print("q1:", t, s)


def q2_alias_version() -> None:
    """复测 2 · 这次不是复制了，是**别名**。逐行预测。"""
    t: dict[str, Any] = {"tags": ["x"], "id": 1}
    s: dict[str, Any] = t

    s["tags"].append("y")
    s["id"] = 99

    # 预测：t = ?
    # 预测：s = ?
    print("q2:", t, s)


def q3_rebind_inside_default() -> None:
    """复测 3 · 默认参数陷阱的变体：注意函数体里用的是 `+` 还是 `.append()`。"""

    def f(x: str, items: list[str] = []) -> list[str]:
        items = items + [x]
        return items

    # 预测：第一次 print = ?
    # 预测：第二次 print = ?
    print("q3:", f("a"))
    print("q3:", f("b"))

    # 追问：为什么这个版本**不会**像 add_task_bad 那样累积？（一句话）
    # 答：


def q4_oral() -> None:
    """复测 4 · 口述题（不写代码，把答案写在注释里）

    ① `q = q + [4]` 和 `q.append(4)` 的区别是什么？
    ② 什么时候该用 `=`，什么时候该用 `.copy()`？
    """
    # ①
    # ②
    print("q4: 见注释")


if __name__ == "__main__":
    q1_deepcopy_version()
    q2_alias_version()
    q3_rebind_inside_default()
    q4_oral()
