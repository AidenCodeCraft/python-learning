"""阶段 1 · 第 3 天 · 练习作答文件（循环）

用法：
    1. 先自己写，卡住就写注释说明思路，不要留空。
    2. 跑：python day03.py
    3. 对 exercises/stage1/day03/README.md 的"四、自检清单"。

规则：档① 读改 → 档② 填空 → 档③ 默写，上一档没过不许跳。
⚠️ 如果程序卡住不动，说明写出了死循环 —— 在终端按 `Ctrl + C` 中断，然后找"谁没有前进"。
"""

from __future__ import annotations


# ============================================================
# 档① 读改（改的是 demo_reference.py，预测写在这里）
# ============================================================

def ex01_read_modify_range() -> None:
    """档① 第 1 题：把 demo 的 1-b（`range(2, 10, 3)`）改成 `range(2, 12, 3)`。"""
    # 预测：list(range(2, 12, 3)) = 2,5,8,11
    print("ex01:", list(range(2, 12, 3)))


def ex02_read_modify_while() -> None:
    """档① 第 2 题：把 demo 的 3-a（`while i <= 5`）改成 `while i < 5`。"""
    total = 0
    i = 1
    while i < 5:  # TODO: 改成 while i < 5
        total += i
        i += 1
    # 预测：total = 10    i = 5
    print("ex02:", total, i)


def ex03_read_modify_enumerate() -> None:
    """档① 第 3 题：把 demo 的 2-a 改成 `enumerate(tasks, 1)`（下标从 1 开始）。"""
    tasks = ["写代码", "自测", "提交"]
    for i, t in enumerate(tasks, 1):  # TODO: 加 start 参数
        print("ex03:", i, t)


# ============================================================
# 档② 填空
# ============================================================

def ex04_fill_range_even() -> None:
    """档② 第 4 题：用 **range 的步长**直接打出 2 4 6 8 10（不许用 if 判断偶数）。"""
    for n in range(2, 11, 2):  # TODO: 改 range 的参数，并删掉下面的 if
        # if n % 2 == 0:
        print("ex04:", n)


def ex05_fill_while_sum() -> None:
    """档② 第 5 题：用 while 求 1+2+...+100（期望 5050）。有 1 处要改。"""
    total = 0
    i = 1
    while i <= 100:  # TODO: 边界对不对？（现在的结果是多少？）
        total += i
        i += 1
    print("ex05:", total)   # ex05: 5050


def ex06_fill_break() -> None:
    """档② 第 6 题：找到**第一个**能被 7 整除的数就停下（期望只打印一次 7）。"""
    for n in range(1, 100):
        if n % 7 == 0:
            print("ex06:", n)
            # TODO: 加一行，让循环停在这里
            break


# ============================================================
# 档③ 默写
# ============================================================

def ex07_fix_loop(n: int) -> int:
    """档③ 第 7 题（改错题）：下面这段有 2 处错，先找出来，再写正确版本。

    原文（别直接运行 —— 它会**死循环**）：
        total = 0
        i = 1
        while i <= n:
            total += i
        return total

    要求：返回 1+2+...+n；n <= 0 时返回 0。
    """
    # TODO: 写正确版本
    if n <= 0:
        return 0
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total


def ex08_sum_to(n: int) -> int:
    """档③ 第 8 题：用 **for + range** 求 1+2+...+n（n <= 0 返回 0）。
    和 ex07 是同一个问题 —— 体会两种循环的差别。
    """
    # TODO
    count = 0
    for i in range(1, n + 1):
        if n <= 0:
            return 0
        count += i
    return count


def ex09_count_vowels(s: str) -> int:
    """档③ 第 9 题：数出字符串里元音字母（a e i o u）的个数，忽略大小写。
    例：count_vowels("Hello World") → 3
    """
    # TODO
    count = 0
    vowels = "aeiou"
    for ch in s:
        if ch.lower() in vowels:
            count += 1
    return count


def ex10_find_first(items: list[int], target: int) -> int:
    """档③ 第 10 题：返回 target 第一次出现的下标；找不到返回 -1。
    **不许用 `items.index()`** —— 用 enumerate + break 自己找。
    例：find_first([5, 3, 7, 3], 3) → 1；find_first([1, 2], 9) → -1
    """
    # TODO
    for i, t in enumerate(items):
        if t == target:
            return i
    return -1


def ex11_to_dict(keys: list[str], values: list[int]) -> dict[str, int]:
    """档③ 第 11 题：用 `zip` 把两条序列配成字典。
    例：to_dict(["a", "b"], [1, 2]) → {"a": 1, "b": 2}
    """
    # TODO
    return dict(zip(keys, values))


def ex12_read_code() -> None:
    """档③ 第 12 题（读代码说结果题）：先写 6 个预测，再运行。"""
    # 预测 1: 12-1: 没找到 4
    for n in [1, 3, 5]:
        if n == 4:
            break
    else:
        print("12-1: 没找到 4")

    # 预测 2: 12-2:1 3 5
    for n in range(1, 6):
        if n % 2 == 0:
            continue
        print("12-2:", n)

    # 预测 3: 12-3:[3,2,1] [0,1,2]
    print("12-3:", list(range(3, 0, -1)), list(range(0, 3)))

    # 预测 4: 12-4:10 4
    count = 0
    for i in range(5):
        count += i
    print("12-4:", count, i)

    # 预测 5: [('a',1),('b',2)]
    print("12-5:", list(zip("ab", [1, 2, 3])))

    # 预测 6:12-6:['00','01','10','11']
    outer: list[str] = []
    for i in range(2):
        for j in range(2):
            outer.append(str(i) + str(j))
    print("12-6:", outer)


if __name__ == "__main__":
    ex01_read_modify_range()
    ex02_read_modify_while()
    ex03_read_modify_enumerate()
    ex04_fill_range_even()
    ex05_fill_while_sum()
    ex06_fill_break()
    print("ex07:", ex07_fix_loop(5), ex07_fix_loop(0), ex07_fix_loop(-3))
    print("ex08:", ex08_sum_to(5), ex08_sum_to(0))
    print("ex09:", ex09_count_vowels("Hello World"))
    print("ex10:", ex10_find_first([5, 3, 7, 3], 3), ex10_find_first([1, 2], 9))
    print("ex11:", ex11_to_dict(["a", "b"], [1, 2]))
    ex12_read_code()
