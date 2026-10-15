"""阶段 1 · 第 2 天 · 练习作答文件（运算符与条件）

用法：
    1. 先自己写，卡住就写注释说明思路，不要留空。
    2. 跑：python day02.py
    3. 对 exercises/stage1/day02/README.md 的"四、自检清单"。

规则：档① 读改 → 档② 填空 → 档③ 默写，上一档没过不许跳。
      每处 TODO 上方都有"预测："位置，**先写预测，再运行**。
"""

from __future__ import annotations


# ============================================================
# 档① 读改（改的是 demo_reference.py，预测写在这里）
# ============================================================

def ex01_read_modify_floor_div() -> None:
    """档① 第 1 题：把 demo 的 1-b 改成 `7 // -2`，预测并运行。"""
    # 预测：7 // -2 = -4
    # 预测：它和 -7 // 2 一样吗？为什么？（一句话）：一样，都是有负数，向下取整都是-4
    print("ex01:", 7 // -2, -7 // 2)


def ex02_read_modify_or_chain() -> None:
    """档① 第 2 题：把 demo 的 3-c 改成 `"最后" or "" or 0 or [] or None`。"""
    # 预测：输出 = 最后
    # 预测：为什么 `or` 返回的不是 True？or / and 返回处理结果操作数
    print("ex02:", "最后" or "" or 0 or [] or None)


def ex03_read_modify_short_circuit() -> None:
    """档① 第 3 题：把 demo 的 4-c 改成 `False and boom()`，看 boom() 有没有被执行。"""
    def boom() -> str:
        print("   >>> ex03 里的 boom() 被执行了")
        return "boom"

    # 预测：下面三行分别输出什么？"boom() 被执行了"会在第几行打印？
    print("ex03-a:", False and boom())  # ex03-a:False
    print("ex03-b:", True or boom())    # ex03-b:True
    print("ex03-c:", True and boom())   # ex03-c:boom
    # 预测：ex03-c:会打印"boom() 被执行了"


# ============================================================
# 档② 填空（把运算符/条件换掉，让输出达到期望）
# ============================================================

def ex04_fill_operator_mod() -> None:
    """档② 第 4 题：期望输出 2。"""
    print("ex04:", 17 % 5)  # TODO: 换一个运算符，让结果是 2


def ex05_fill_operator_pow() -> None:
    """档② 第 5 题：期望输出 1024。"""
    print("ex05:", 2 ** 10)  # TODO: 换一个运算符，让结果是 1024


def ex06_fill_blank_truthy() -> None:
    """档② 第 6 题：用"真假值"判断空串，不许用 `==`。"""
    s: str = ""
    if not s:  # TODO: 改成利用真值判断的写法
        print("ex06: 空")
    else:
        print("ex06: 非空")


def ex07_fill_blank_default() -> None:
    """档② 第 7 题：data 为空时给出默认值，期望 x 输出 "默认"。"""
    data: list[int] = []
    x: object = data or "默认"  # TODO: 换一个逻辑运算符
    print("ex07:", x)


# ============================================================
# 档③ 默写（函数签名已给，写函数体）
# ============================================================

def ex08_grade(score: int) -> str:
    """档③ 第 8 题：≥90 → "A"，≥80 → "B"，≥70 → "C"，≥60 → "D"，其余 → "F"。"""
    # TODO
    if score >= 90:
        return "A"
    elif score < 90 and score >= 80:
        return "B"
    elif score < 80 and score >= 70:
        return "C"
    elif score < 70 and score >= 60:
        return "D"
    else:
        return "F"


def ex09_fizzbuzz(n: int) -> str:
    """档③ 第 9 题：3 的倍数 → "Fizz"，5 的倍数 → "Buzz"，
    同时是 3 和 5 的倍数 → "FizzBuzz"，否则 → str(n)。
    提示：先想清楚"哪个条件必须先判"。
    """
    # TODO
    if (n % 3 == 0) and (n % 5 == 0):
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def ex10_split_seconds(total: int) -> tuple[int, int, int]:
    """档③ 第 10 题：把总秒数拆成 (时, 分, 秒)。只许用 `//` 和 `%`。
    例：3725 → (1, 2, 5)；3600 → (1, 0, 0)；59 → (0, 0, 59)。
    """
    # TODO
    h = total // 3600
    total %= 3600
    m = total // 60
    total %= 60
    s = total
    return (h, m, s)


def ex11_fix_errors(n: int) -> str:
    """档③ 第 11 题（改错题）：下面这段有 3 处错，先找出来，再把改好的版本写进函数体。

    原文（别直接运行，它是 SyntaxError，所以只能写在文档字符串里）：
        if n % 2 = 0:
            return "偶"
        elif n > 0 and n < 10
            return "小正"
        else
            return "其他"

    改好后的行为：4 → "偶"；5 → "小正"；-1 → "其他"。
    """
    # TODO: 把改好的版本写在这里
    if n % 2 == 0:
        return "偶"
    elif n > 0 and n < 10:
        return "小正"
    else:
        return "其他"


def ex12_read_code() -> None:
    """档③ 第 12 题（读代码说结果题）：先写预测，再运行。"""
    def describe(value: object) -> str:
        if not value:
            return "空"
        if value in ("a", "b"):
            return "在元组里"
        return "其他"

    print(describe(""), describe("a"), describe("z"))  # 预测 1:"空" "在元组里" "其他"
    print(0 or "x")                                    # 预测 2:"x"
    print("" and "y")                                  # 预测 3:""
    print(None or [])                                  # 预测 4:[]
    print(7 // -2, -7 % 3, 1 < 5 < 3)                  # 预测 5:-4 2 False


if __name__ == "__main__":
    ex01_read_modify_floor_div()
    ex02_read_modify_or_chain()
    ex03_read_modify_short_circuit()
    ex04_fill_operator_mod()
    ex05_fill_operator_pow()
    ex06_fill_blank_truthy()
    ex07_fill_blank_default()
    print("ex08:", ex08_grade(95), ex08_grade(80), ex08_grade(60), ex08_grade(59))
    print("ex09:", ex09_fizzbuzz(15), ex09_fizzbuzz(9), ex09_fizzbuzz(10), ex09_fizzbuzz(7))
    print("ex10:", ex10_split_seconds(3725), ex10_split_seconds(3600), ex10_split_seconds(59))
    print("ex11:", ex11_fix_errors(4), ex11_fix_errors(5), ex11_fix_errors(-1))
    ex12_read_code()
