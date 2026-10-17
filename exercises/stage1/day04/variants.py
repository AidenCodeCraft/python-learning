"""D4 变式题（阶段 1 · 第 4 天）—— 针对 2026-10-17 批改暴露的 3 个洞

用法：
    1. 用 check() 把你**预测的值**填进第三个参数，再运行。
    2. 跑完看"对上了吗"：全 True 才算过。
    3. 对不上的，把原因写进 mistakes/2026-10-17.md。

★ 为什么这三题：D4 你 20 题全对，是因为骨架里有 check() 兜着；
  而微课两个文件你**写完没跑**，结果一个直接崩、一个三处错。
  这三题把"会跑"和"会审"放在一起练。
"""

from __future__ import annotations


def check(label: str, actual: object, guess: object) -> None:
    """打印"实际 / 预测 / 对上了吗" —— 对上了才是 True。"""
    print(label, "实际=", actual, "预测=", guess, "对上了吗:", actual == guess)


# ============================================================
# 变式 1 · 默认参数陷阱（要点 2 / 微课 3 处错里最容易复发的一条）
# ============================================================

def v1_fix_default_arg() -> None:
    """变式 1：把 add_friend 改成"每次调用互不影响"。
    改完下面两个 check 都应该是 True。
    """

    def add_friend(name: str, friends: list[str] | None = None) -> list[str]:  # TODO: 改成正确写法
        if not friends:
            friends = []
        friends.append(name)
        return friends

    check("v1-第一次 add_friend('Tom')", add_friend("Tom"), ["Tom"])
    check("v1-第二次 add_friend('Ann')", add_friend("Ann"), ["Ann"])


# ============================================================
# 变式 2 · 类属性陷阱（微课 B3 / 阶段 0 第 6 题）
# ============================================================

class V2Box:
    # items: list[int] = []   # TODO: 把 items 挪进 __init__，让每个实例各有一份

    def __init__(self) -> None:
        self.name = "box"
        self.items: list[int] = []

    def add(self, x: int) -> None:
        self.items.append(x)


def v2_fix_class_attr() -> None:
    """变式 2：让两个 Box 各自独立（b1 只有 [1]、b2 只有 [2]）。"""
    b1 = V2Box()
    b2 = V2Box()
    b1.add(1)
    b2.add(2)
    check("v2-b1.items", b1.items, [1])
    check("v2-b2.items", b2.items, [2])


# ============================================================
# 变式 3 · dict 计数 + sorted(key=lambda) + 切片（ex13 + ex16 的组合）
# ============================================================

def v3_top_words(words: list[str], n: int) -> list[str]:
    """变式 3：统计词频，按次数**从高到低**取前 n 个词；次数相同按字母升序。

    top_words(["a", "b", "a", "c", "b", "a"], 2) → ["a", "b"]   （a 3 次、b 2 次）
    top_words(["b", "b", "a", "a"], 2)           → ["a", "b"]   （都是 2 次 → 按字母）
    """
    # TODO：先数词频，再排序，再切片
    counts = {}
    for i in words:
        counts[i] = counts.get(i, 0) + 1

    sorted_items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [i for i , c in sorted_items[:n]]


if __name__ == "__main__":
    v1_fix_default_arg()
    v2_fix_class_attr()
    check("v3-1", v3_top_words(["a", "b", "a", "c", "b", "a"], 2), ["a", "b"])
    check("v3-2", v3_top_words(["b", "b", "a", "a"], 2), ["a", "b"])
    check("v3-3", v3_top_words(["x"], 5), ["x"])


# ============================================================
# 自检清单（写完预测再来对）
# ============================================================
# v1-第一次 → ["Tom"]      v1-第二次 → ["Ann"]
#     改法：friends: list[str] | None = None，函数内 if friends is None: friends = []
#     ⚠️ 别用 `friends = friends or []` —— 传空列表进来时也会被换掉，语义不一样。
#
# v2-b1.items → [1]        v2-b2.items → [2]
#     改法：删掉类属性，改成 `def __init__(self): self.items: list[int] = []`
#     ⚠️ 注意 b1.add(1) 里 `self.items.append` 是"就地改"，不会创建实例属性；
#        只有 `self.x = ...` 这种赋值才会。这就是类属性陷阱难发现的原因。
#
# v3-1 → ["a", "b"]        v3-2 → ["a", "b"]        v3-3 → ["x"]
#     思路：counts.get(w, 0) + 1 数词频；给 sort/sorted 的 key 返回一个**元组**：
#           key=lambda kv: (-kv[1], kv[0])  → 次数降序、同次数按字母升序
#           最后切片 [:n]
#     ⚠️ 用 sorted(counts.items(), key=...) 返回的是 (word, count) 列表，
#        别直接返回它 —— 题目要的是**词**组成的列表，还要一步推导或解包。
