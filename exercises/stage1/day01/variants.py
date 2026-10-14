"""D1 变式题（阶段 1 · 第 1 天）—— 针对 2026-10-14 首次批改暴露的 3 个洞

用法：
    1. 每题**先在注释里写预测**，再运行 python variants.py。
    2. 对不上的，把原因写进 mistakes/2026-10-14.md。
    3. 自检清单在本文件最下面（答案代码不给，只给预期输出）。

规则：不许先看底部自检清单，也不许先看 demo_reference.py。
"""

from __future__ import annotations

from typing import Any


def v1_rebind_vs_mutate() -> None:
    """变式 1 · 直击 ex01：`b = b + [3]` 和 `b.append(3)` 到底差在哪？"""
    a: list[int] = [1, 2]
    b: list[int] = a

    b = b + [3]

    # 预测（先写，再运行）：
    # a  = [1, 2]
    # b  = [1, 2, 3]
    # a is b = False
    print("v1:", a, b, a is b)

    # 追问：如果我想让 [3] 真的加进 a 里，应该把哪一行换成什么？
    # 答：b = b + [3]换成b.append(3)


def v2_shallow_nested() -> None:
    """变式 2 · 直击 demo 6-a/6-b：浅拷贝里"外层复制、内层共享"。"""
    t: dict[str, Any] = {"tags": ["x"], "id": 1}
    s: dict[str, Any] = t.copy()

    s["tags"].append("y")
    s["id"] = 99

    # 预测（先写，再运行）：
    # t = {"tags": ["x", "y"], "id": 1}
    # s = {"tags": ["x", "y"], "id": 99}
    print("v2:", t, s)

    # 解释：为什么 tags 跟着变了，而 id 没变？（两句话）
    # 答：.copy()是浅拷贝只复制外层，id属于外层，["x"]属于内层。外层改变互相不影响，内层属于共享。


def v3_default_arg_dict() -> None:
    """变式 3 · 直击 ex05：把"默认参数陷阱"从 list 换到 dict，你还能认出来吗？"""

    def add(tags: str, cache: dict[str, int] = {}) -> dict[str, int]:
        cache[tags] = len(cache)
        return cache

    # 预测（先写，再运行）：
    # 第一次 print 输出 = v3:{'a' : 0}
    # 第二次 print 输出 = v3:{'a' : 0, 'b' : 1}
    print("v3:", add("a"))
    print("v3:", add("b"))

    # 改成"不会累积"的写法（改函数签名或函数体，只允许用今天学的东西）：
    # 答：
    def add(tags: str, cache: dict[str, int] | None = None) -> dict[str, int]:
            if cache is None:
                 cache = {}
            cache[tags] = len(cache)
            return cache
    
    print("v3:", add("a"))
    print("v3:", add("b"))


if __name__ == "__main__":
    v1_rebind_vs_mutate()
    v2_shallow_nested()
    v3_default_arg_dict()


# ============================================================
# 自检清单（写完预测再来对。先自己判，把对不上的题号记下来）
# ============================================================
# v1 : a = [1, 2]        b = [1, 2, 3]        a is b = False
#      追问：把 `b = b + [3]` 换成 `b.append(3)` —— 就地改，改的就是 a 指向的那个列表
#
# v2 : t = {'tags': ['x', 'y'], 'id': 1}
#      s = {'tags': ['x', 'y'], 'id': 99}
#      为什么：.copy() 只复制最外层 dict；内层列表 `tags` 是**同一个对象**，所以 append 会一起变。
#              而 `id` 是 int（不可变），`s["id"] = 99` 只是把 s 里那个键**改指向**新对象 99，动不到 t。
#
# v3 : 第一次 {'a': 0}
#      第二次 {'a': 0, 'b': 1}     ← 和 list 版本一模一样的坑
#      改法：cache 默认值用 None，函数内 if cache is None: cache = {}
