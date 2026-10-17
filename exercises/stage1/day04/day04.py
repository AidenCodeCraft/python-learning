"""阶段 1 · 第 4 天 · 练习作答文件（函数与容器）

用法：
    1. 先自己写，卡住就写注释说明思路，不要留空。
    2. 跑：python day04.py
    3. 对 exercises/stage1/day04/README.md 的"四、自检清单"。

规则：档① 读改 → 档② 填空 → 档③ 默写，上一档没过不许跳。

★ D4 新规矩（因为 D2/D3 各有 3 处"预测写完不核对"）：
   预测不再只写在注释里 —— 用下面的 check()，它会直接把"对上了吗"打出来。
   把每个 check 的第三个参数（0 / [] 这种占位）换成**你预测的值**，然后跑。
   眼睛会漏，机器不会。
"""

from __future__ import annotations
from itertools import repeat


def check(label: str, actual: object, guess: object) -> None:
    """打印"实际 / 预测 / 对上了吗" —— 对上了才是 True。"""
    print(label, "实际=", actual, "预测=", guess, "对上了吗:", actual == guess)


# ============================================================
# 档① 读改（改的是 demo_reference.py，预测填进 check 的第三个参数）
# ============================================================

def ex01_read_modify_default() -> None:
    """档① 第 1 题：把 demo 的 `add(a, b=10)` 改成 `b=100`。"""

    def add(a: int, b: int = 100) -> int:  # TODO: 默认值改成 100
        return a + b

    check("ex01-add(1)", add(1), 101)        # TODO: 把 0 换成你的预测
    check("ex01-add(1,2)", add(1, 2), 3)   # TODO: 同上


def ex02_read_modify_scope() -> None:
    """档① 第 2 题：取消 `counter = counter + 1` 的注释，看报什么错。

    预测（写在下面）：抛出的异常类型是 ______
    想清楚再取消注释运行；不取消也不会崩（下面用 try 接住了）。
    """
    counter = 0

    def bump() -> None:
        counter = counter + 1        # TODO: 取消注释
        print("ex02: bump 内部读到的 counter =", counter)

    try:
        bump()
    except UnboundLocalError:
        print("ex02: 抛出了 UnboundLocalError")


def ex03_read_modify_mutation() -> None:
    """档① 第 3 题：把 `items = items + [99]` 改成 `items.append(99)`。"""

    def rebind_item(items: list[int]) -> None:
        items.append(99)  # TODO: 改成 items.append(99)

    data2 = [1, 2]
    rebind_item(data2)
    check("ex03-data2", data2, [1, 2, 99])   # TODO: 改成你的预测


def ex04_read_modify_comprehension() -> None:
    """档① 第 4 题：把 `[n * n for n in range(5)]` 改成带条件 `if n % 2`。"""
    result = [n * n for n in range(5) if n % 2]   # TODO: 加 if n % 2
    check("ex04", result, [1, 9])   # TODO: 改成你的预测


# ============================================================
# 档② 填空
# ============================================================

def ex05_fill_default() -> None:
    """档② 第 5 题：让 `greet("Tom")` 输出 `你好, Tom`。"""

    def greet(name: str, greeting: str = "你好") -> str:  # TODO: 改默认值
        return greeting + ", " + name

    print("ex05:", greet("Tom"))


def ex06_fill_multi_return() -> None:
    """档② 第 6 题：让 min_max 返回 (最小值, 最大值)。"""

    def min_max(nums: list[int]) -> tuple[int, int]:
        return min(nums), max(nums)  # TODO

    low, high = min_max([3, 1, 9])
    print("ex06:", low, high)   # 期望 1 9


def ex07_fill_get() -> None:
    """档② 第 7 题：让 user 里没有 "age" 时输出 0。"""
    user: dict[str, object] = {"id": 1, "name": "Tom"}
    print("ex07:", user.get("age", 0))   # TODO: 补第二个参数


def ex08_fill_set() -> None:
    """档② 第 8 题：让输出是 `[1, 2, 3]`（去重 + 升序）。"""
    nums = [3, 1, 2, 3, 1]
    print("ex08:", sorted(set(nums)))   # TODO: 用 set 去重、sorted 升序


def ex09_fill_slice() -> None:
    """档② 第 9 题：让 `s` 反转输出 `dcba`。"""
    s = "abcd"
    print("ex09:", s[::-1])   # TODO: 用切片


def ex10_fill_comprehension() -> None:
    """档② 第 10 题：把下面的循环改成**一行列表推导式**，结果仍是 [2, 4, 6]。"""
    # result: list[int] = []
    # for n in range(1, 7):
    #     if n % 2 == 0:
    #         result.append(n)
    result: list[int] = [n for n in range(1, 7) if n % 2 == 0]
    print("ex10:", result)


# ============================================================
# 档③ 默写
# ============================================================

def ex11_repeat(s: str, times: int = 2) -> str:
    """档③ 第 11 题：把 s 重复 times 次返回。repeat("ab") → "abab"；repeat("x", 3) → "xxx"。"""
    # TODO
    return s * times


def ex12_stats(nums: list[int]) -> tuple[int, int, float]:
    """档③ 第 12 题：返回 (最小值, 最大值, 平均值)。
    stats([1, 2, 3, 4]) → (1, 4, 2.5)。空列表返回 (0, 0, 0.0)。
    """
    # TODO
    if not nums:
        return (0, 0, 0.0)
    return (min(nums), max(nums), sum(nums) / len(nums))

def ex13_count_words(text: str) -> dict[str, int]:
    """档③ 第 13 题：统计每个单词出现的次数。
    count_words("a b a") → {"a": 2, "b": 1}
    提示：`text.split()` 切词；字典计数用 `get(word, 0) + 1`。
    """
    # TODO
    words = text.split(" ")
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def ex14_unique_sorted(items: list[int]) -> list[int]:
    """档③ 第 14 题：去重并按升序返回。unique_sorted([3, 1, 3, 2]) → [1, 2, 3]。"""
    # TODO
    return sorted(set(items))


def ex15_merge(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    """档③ 第 15 题：合并两个字典，**b 的同名键覆盖 a**。
    merge({"x": 1}, {"x": 9, "y": 2}) → {"x": 9, "y": 2}
    """
    # TODO
    return {**a, **b}


def ex16_top_n(scores: dict[str, int], n: int) -> list[str]:
    """档③ 第 16 题：按分数从高到低取前 n 个**名字**。
    top_n({"Tom": 90, "Ann": 85, "Bob": 95}, 2) → ["Bob", "Tom"]
    提示：`scores.items()` + `sorted(..., key=lambda kv: kv[1], reverse=True)` + 切片。
    """
    # TODO
    top_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [name for name, score in top_scores]  


def ex17_comprehensions(nums: list[int]) -> tuple[list[int], dict[int, int], set[int]]:
    """档③ 第 17 题：用**推导式**一次算出三样东西：
      ① 偶数的平方组成的 list        例：[1,2,3,4] → [4, 16]
      ② 值 → 值平方 组成的 dict      例：[1,2,3]   → {1: 1, 2: 4, 3: 9}
      ③ 这些数对 5 取余的 set        例：[1,2,3]   → {1, 2, 3}
    """
    # TODO
    evens_squared = [n *n for n in nums  if n % 2 == 0]
    squares_dict = {n: n * n for n in nums } 
    remainders_set = {n % 5 for n in nums}
    return (evens_squared, squares_dict, remainders_set)


def ex18_get_path(data: dict[str, object], path: str, default: object = None) -> object:
    """档③ 第 18 题：按 `"a.b.c"` 这种路径取值；任何一层缺失就返回 default。
    get_path({"a": {"b": {"c": 1}}}, "a.b.c") → 1
    get_path({"a": {}}, "a.b.c") → None
    get_path({"a": {"b": {"c": 1}}}, "a.x", "缺失") → "缺失"
    提示：`path.split(".")` + 循环 + `isinstance(cur, dict)` 判断。
    """
    # TODO
    kyes = path.split(".")
    cur = data
    for key in kyes:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def ex19_fix_errors() -> str:
    """档③ 第 19 题（改错题）：下面 3 个函数各有 1 处错，先找出来，再在下面写正确版本。

    原文：
        # ① 想"每次调用互不影响"
        def add_tag(tag: str, tags: list[str] = []) -> list[str]:
            tags.append(tag)
            return tags

        # ② 想"返回一份副本"
        def copy_tags(tags: list[str]) -> list[str]:
            return tags

        # ③ 想"返回第一个偶数，没有就返回 -1"
        def first_even(nums: list[int]) -> int:
            for n in nums:
                if n % 2 == 0:
                    return n
                return -1

    要求（写对后自测）：
        add_tag("a") → ["a"]；add_tag("b") → ["b"]（不累积）
        copy_tags(x) 返回的对象改不动 x
        first_even([1, 3, 4]) → 4；first_even([1, 3]) → -1
    """
    # TODO: 写正确版本
    # ① 想"每次调用互不影响"
    def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
        if tags is None:
            tags = []
        tags.append(tag)
        return tags
    print(add_tag("a"))
    # ② 想"返回一份副本"
    def copy_tags(tags: list[str]) -> list[str]:
        return sorted(tags)
    print(copy_tags(["b"]))
    # ③ 想"返回第一个偶数，没有就返回 -1"
    def first_even(nums: list[int]) -> int:
        for n in nums:
            if n % 2 == 0:
                return n
        return -1
    print(first_even([1,3]))

def ex20_read_code() -> None:
    """档③ 第 20 题（读代码说结果题）：先写 6 个预测，再运行。

    用 check() 把你的预测填进第三个参数。
    """
    def f(x: int, acc: list[int] = []) -> list[int]:
        acc.append(x)
        return acc

    check("20-1 f(1),f(2)", [f(1), f(2)], [[1, 2],[1, 2]])           # TODO 预测 1

    n = 5

    def g() -> int:
        return n * 2

    check("20-2 g()", g(), 10)                             # TODO 预测 2

    check("20-3", [x * 2 for x in range(4) if x % 2], [2, 6])  # TODO 预测 3

    check("20-4", {k: len(k) for k in ["a", "bb", "ccc"] if len(k) > 1}, {'bb': 2, 'ccc': 3})  # TODO 预测 4

    s = "hello"
    check("20-5 s[1:4],s[::-1]", (s[1:4], s[::-1]), ("ell","olleh"))    # TODO 预测 5

    def h(items: list[int]) -> list[int]:
        items.append(0)
        return items

    data = [1]
    check("20-6 h(data),data", (h(data), data), ([1, 0], [1, 0]) )        # TODO 预测 6


if __name__ == "__main__":
    ex01_read_modify_default()
    ex02_read_modify_scope()
    ex03_read_modify_mutation()
    ex04_read_modify_comprehension()
    ex05_fill_default()
    ex06_fill_multi_return()
    ex07_fill_get()
    ex08_fill_set()
    ex09_fill_slice()
    ex10_fill_comprehension()
    print("ex11:", ex11_repeat("ab"), ex11_repeat("x", 3))
    print("ex12:", ex12_stats([1, 2, 3, 4]), ex12_stats([]))
    print("ex13:", ex13_count_words("a b a"))
    print("ex14:", ex14_unique_sorted([3, 1, 3, 2]))
    print("ex15:", ex15_merge({"x": 1}, {"x": 9, "y": 2}))
    print("ex16:", ex16_top_n({"Tom": 90, "Ann": 85, "Bob": 95}, 2))
    print("ex17:", ex17_comprehensions([1, 2, 3, 4]))
    print("ex18:", ex18_get_path({"a": {"b": {"c": 1}}}, "a.b.c"),
          ex18_get_path({"a": {}}, "a.b.c"),
          ex18_get_path({"a": {"b": {"c": 1}}}, "a.x", "缺失"))
    print("ex19:", ex19_fix_errors())
    ex20_read_code()
