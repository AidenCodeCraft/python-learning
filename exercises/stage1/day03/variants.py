"""D3 变式题（阶段 1 · 第 3 天）—— 针对 2026-10-16 批改暴露的 3 个洞

用法：
    1. 每题**先在注释里写预测**，再运行 python variants.py。
    2. 对不上的，把原因写进 mistakes/2026-10-16.md。
    3. 自检清单在本文件最下面（只给预期输出，不给答案代码）。

⚠️ 从今天起：**预测不要只写在注释里** —— 用下面这个 check()，让机器替你划勾。
   D2 教练给过这个工具，你没用；D3 的 demo 因此又错了 3 处预测。
"""

from __future__ import annotations


def check(label: str, actual: object, guess: object) -> None:
    """打印"实际 / 预测 / 对上了吗"三列 —— 眼睛会漏，机器不会。"""
    print(label, "实际=", actual, "预测=", guess, "对上了吗:", actual == guess)


def v1_sum_odd_to(n: int) -> int:
    """变式 1 · 直击 ex08：`total` 才是**累加器**，循环变量只管"走到哪了"。
    求 1~n 中所有**奇数**之和。n <= 0 返回 0。
    例：sum_odd_to(10) → 25（1+3+5+7+9）
    """
    # TODO: 用 for + range + if + 累加器
    count = 0
    if n <= 0:
        return 0
    for i in range(n):
        if i % 2 != 0:
            count += i
    return count


def v2_count_digits(s: str) -> int:
    """变式 2 · 直击 ex09：循环要遍历**传进来的 s**，不是别的序列。
    数出字符串里数字字符（0-9）的个数。**不许用 s.isdigit()**，就用 `in`。
    例：count_digits("a1b2c3") → 3
    """
    # TODO
    count = 0
    number = "0123456789"
    for ch in s:
        if ch in number:
            count += 1
    return count


def v3_find_last(items: list[int], target: int) -> int:
    """变式 3 · 直击 ex10：返回值必须是**下标变量**，硬编码活不过第二个测试。
    返回 target **最后一次**出现的下标；找不到返回 -1。不许用 items.index()。
    例：find_last([1, 3, 5, 3], 3) → 3；find_last([9, 3], 3) → 1；find_last([1, 2], 9) → -1
    """
    # TODO
    count = -1
    for i, t in enumerate(items):
        if t == target:
            count = i
    return count


if __name__ == "__main__":
    check("v1(10)", v1_sum_odd_to(10), 25)
    check("v1(0)", v1_sum_odd_to(0), 0)
    check("v2", v2_count_digits("a1b2c3"), 3)
    check("v3-1", v3_find_last([1, 3, 5, 3], 3), 3)
    check("v3-2", v3_find_last([9, 3], 3), 1)
    check("v3-3", v3_find_last([1, 2], 9), -1)


# ============================================================
# 自检清单（写完预测再来对）
# ============================================================
# v1(10) → 25      v1(0) → 0
#     累加器写法：total = 0；for i in range(1, n + 1): if i % 2: total += i；最后 return total。
#     ⚠️ 别写 `i += 1` —— i 是循环变量，改它没用；也别在循环里 `return 0`。
#
# v2 → 3
#     for ch in s: if ch in "0123456789": count += 1
#     ⚠️ ex09 的错误是"遍历了元音列表"而不是"遍历 s"，所以结果与输入无关。
#
# v3-1 → 3     v3-2 → 1     v3-3 → -1
#     思路：用一个变量记住"最后一次见到的下标"，遍历完再返回它。
#     ⚠️ 如果你写 `return 1`（硬编码），v3-1 和 v3-2 会"碰巧对"，但 v3-3 之外的
#        任何数据都会露馅 —— 这就是 ex10 的病。
