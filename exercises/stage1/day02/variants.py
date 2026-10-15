"""D2 变式题（阶段 1 · 第 2 天）—— 针对 2026-10-15 批改暴露的 3 个洞

用法：
    1. 每题**先在注释里写预测**，再运行 python variants.py。
    2. 对不上的，把原因写进 mistakes/2026-10-15.md。
    3. 自检清单在本文件最下面（只给预期输出，不给答案代码）。

规则：不许先看底部自检清单。
"""

from __future__ import annotations


def v1_and_or_values() -> None:
    """变式 1 · 直击你今天错了 4 次的那条规则：and / or 返回的是操作数本身。"""
    print("v1-a:", 1 and 2)
    print("v1-b:", 0 and 2)
    print("v1-c:", [] or None or "x")
    print("v1-d:", "" or 0)
    print("v1-e:", not [])

    # 预测（5 行，先写再运行）：
    # v1-a = 2
    # v1-b = 0
    # v1-c = "x"
    # v1-d = 0
    # v1-e = True
    # 追问：这 5 行里，哪几行的结果不是 `True` / `False`？1,2,3,4


def v2_split_and_merge() -> None:
    """变式 2 · ex10 的迁移：把"秒→时/分/秒"换成"分钟→天/时/分"，并加上反向合并。
    只许用 `//` 和 `%`。
    """

    def split_minutes(total_minutes: int) -> tuple[int, int, int]:
        """1500 → (1, 1, 0)；1440 → (1, 0, 0)；59 → (0, 0, 59)。"""
        h = total_minutes // 1440
        total_minutes %= 1440
        m = total_minutes // 60 
        total_minutes %= 60
        s = total_minutes
        return (h, m, s)

    def merge_minutes(days: int, hours: int, minutes: int) -> int:
        """反向：把 (天, 时, 分) 合回总分钟数。merge(1, 1, 0) → 1500。"""
        # TODO
        return days * 3600 + hours * 60 + minutes

    # 预测：split_minutes(1500) = (0, 25, 0)   split_minutes(1440) = (0, 24, 0)   split_minutes(59) = (0, 0, 59)
    # 预测：merge_minutes(1, 1, 0) = 3660
    print("v2-split:", split_minutes(1500), split_minutes(1440), split_minutes(59))
    print("v2-merge:", merge_minutes(1, 1, 0))


def v3_classify() -> None:
    """变式 3 · ex08 + ex09 的迁移：先判最严的条件，而且别忘 `== 0`。"""

    def classify(n: int) -> str:
        """15 的倍数 → "15x"；5 的倍数 → "5x"；3 的倍数 → "3x"；否则 → "none"。
        例：45 → "15x"；25 → "5x"；9 → "3x"；7 → "none"。
        """
        # TODO
        if n % 15 == 0:
            return "15x"
        elif n % 5 == 0:
            return "5x"
        elif n % 3 == 0:
            return "3x"
        else:
            return "none"

    # 预测：classify(45) = 15x  classify(25) = 5x  classify(9) = 3x  classify(7) = none
    print("v3:", classify(45), classify(25), classify(9), classify(7))


def v4_truthiness() -> None:
    """变式 4 · 直击 ex06：只用真值判断，**不许用 `==`，也不许用 `is`**。"""
    a: str = ""
    b: str = "0"
    c: int = 0
    d: list[int] = []
    e: list[int] = [0]
    f: object = None

    # 预测（6 行，先写再运行）：
    # v4-a = "空"   v4-b = "有值"   v4-c = "空"   v4-d = "空"   v4-e = "有值"   v4-f = "空"
    print("v4-a:", "空" if not a else "有值")
    print("v4-b:", "空" if not b else "有值")
    print("v4-c:", "空" if not c else "有值")
    print("v4-d:", "空" if not d else "有值")
    print("v4-e:", "空" if not e else "有值")
    print("v4-f:", "空" if not f else "有值")


if __name__ == "__main__":
    v1_and_or_values()
    v2_split_and_merge()
    v3_classify()
    v4_truthiness()


# ============================================================
# 自检清单（写完预测再来对。先自己判，把对不上的题号记下来）
# ============================================================
# v1-a: 2          v1-b: 0          v1-c: x        v1-d: 0        v1-e: True
#       追问：v1-a / v1-b / v1-c / v1-d 都不是 True/False —— 因为 and/or 返回操作数本身，
#             所以它们的**类型**可以是 int、str、list 等。
#
# v2-split: (1, 1, 0) (1, 0, 0) (0, 0, 59)
#           total_minutes // 1440；剩下用 % 1440；再 // 60 和 % 60。
# v2-merge: 1500        （days * 1440 + hours * 60 + minutes）
#
# v3: 15x 5x 3x none
#     两个坑：① 每个判断都要写 `== 0`，不能只写 `n % 15`；
#             ② 15 那一支必须最先判（命中即停），否则永远轮不到。
#
# v4: 空 有值 空 空 有值 空
#     最容易答错的是 `"0"`（非空字符串 → 真值）和 `[0]`（非空列表 → 真值）。
