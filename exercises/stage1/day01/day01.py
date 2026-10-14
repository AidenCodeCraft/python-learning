"""阶段 1 · 第 1 天 · 练习作答文件

用法：
    1. 先自己写，卡住就写注释说明思路，不要留空。
    2. 跑：python day01.py
    3. 对 exercises/stage1/day01/README.md 的"四、自检清单"。

规则：档① → 档② → 档③，上一档没过不许跳。
      不要去看 demo_reference.py 的答案，除非你已经卡了两次。
"""

from __future__ import annotations

import copy


def ex01_read_modify_alias() -> None:
    """档① 第 1 题：把别名改成 q = q + [4]，预测并打印 p、q、p is q。"""
    p: list[int] = [1, 2, 3]
    q: list[int] = p
    # TODO: 把下面这行换成 q = q + [4]，先预测输出再运行
    q.append(4)
    print("ex01:", p, q, p is q)


def ex02_read_modify_copy() -> None:
    """档① 第 2 题：把 t = r.copy() 改成 t = r，预测并打印 r 和 t。"""
    r: list[int] = [1, 2, 3]
    t: list[int] = r.copy()
    t.append(4)
    print("ex02:", r, t)


def ex03_read_modify_deepcopy() -> None:
    """档① 第 3 题：把 outer.copy() 改成 copy.deepcopy(outer)，预测并打印 outer。"""
    outer: list[list[int]] = [[1, 2], [3]]
    shallow: list[list[int]] = outer.copy()
    shallow[0].append(99)
    print("ex03:", outer)


def ex04_fill_blank_independent() -> None:
    """档② 第 4 题：让 b 与 a 完全独立（a 是嵌套列表）。"""
    a: list[list[int]] = [[1, 2], [3]]
    b: list[list[int]] = a          # TODO: 换掉这一行，期望 print(a) == [[1, 2], [3]]
    b[0].append(99)
    print("ex04:", a)


def ex05_fill_blank_default_arg() -> None:
    """档② 第 5 题：让每次调用都返回新列表。"""
    def collect(item: str, box: list[str] | None = None) -> list[str]:
        if box is None:              # TODO: 这里现在是对的，先读懂；把你原来会写的写法注释掉对比
            box = []
        box.append(item)
        return box

    print("ex05:", collect("a"), collect("b"))


def ex06_fill_blank_copy_int() -> None:
    """档② 第 6 题：让改 n 不影响 m。"""
    m: list[int] = [5]
    n: list[int] = m                 # TODO: 换掉这一行
    n.append(6)
    print("ex06:", m, n)


def ex07_swap() -> None:
    """档③ 第 7 题：不借助第三个变量交换 a、b。写两种写法。"""
    a: int = 1
    b: int = 2
    # 写法 1（你 C/Java 的直觉）：
    # TODO

    # 写法 2（Python 风格）：
    # TODO

    print("ex07:", a, b)


def ex08_bool_is_int() -> None:
    """档③ 第 8 题：验证 bool 是 int 的子类；打印 True + True。"""
    # TODO
    print("ex08:")


def ex09_shallow_dict() -> None:
    """档③ 第 9 题：字典列表的浅拷贝陷阱。"""
    tasks: list[dict[str, object]] = [
        {"id": 1, "status": "todo"},
        {"id": 2, "status": "done"},
    ]
    # TODO 1: 打印 tasks[0] == {"id": 1, "status": "todo"} 和 tasks[0] is tasks[0]
    # TODO 2: snapshot = tasks.copy()，改 snapshot[0]["status"]，打印 tasks，解释为什么原列表也变
    # TODO 3: 写一种让 snapshot 真正独立的方式
    print("ex09:", tasks)


def ex10_comprehensive() -> None:
    """档③ 第 10 题：三种复制方式 + 别名对照。"""
    a: list[int] = [1, 2, 3]
    # TODO 1: 用 .copy() / list(...) / 切片 三种方式生成 b，各自 print(b is a)
    # TODO 2: b.append(4) 后确认 a 没变
    # TODO 3: 改成 b = a 再 append，确认 a 变了
    # TODO 4: 在下面注释里写一句话：什么时候用 =，什么时候用 .copy()
    print("ex10:", a)


if __name__ == "__main__":
    ex01_read_modify_alias()
    ex02_read_modify_copy()
    ex03_read_modify_deepcopy()
    ex04_fill_blank_independent()
    ex05_fill_blank_default_arg()
    ex06_fill_blank_copy_int()
    ex07_swap()
    ex08_bool_is_int()
    ex09_shallow_dict()
    ex10_comprehensive()
