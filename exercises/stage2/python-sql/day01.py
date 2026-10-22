"""Python 中使用 SQL · Day 1（DB-API 基础）· 作答文件

用法：
    cd exercises/stage2/python-sql
    python day01.py

数据库：用 ../sql/day01/practice.db（12 员工 / 5 部门，其中财务部没有员工）。
⚠️ 这个库**只读**，不要改它（写操作在 Day2/Day3 用副本）。

规则：每题先自己写，卡住就写注释说明思路；写完跑 python day01.py，
     每一行会打印"对上了吗"，看 False 就回去改。
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "sql" / "day01" / "practice.db"


def check(label: str, actual: object, expect: object) -> None:
    print(f"{label:<28} 实际={actual!r:<38} 预期={expect!r:<38} 对上了吗: {actual == expect}")


# ============================================================
# 第 1 题 · 连接数据库 + 列出所有表
# ============================================================

def ex01_list_tables() -> list[str]:
    """返回数据库里所有表名，按字母序。"""
    # TODO: connect → cursor → execute(sqlite_master 查询) → fetchall → close
    return []


# ============================================================
# 第 2 题 · 查询 + fetchall
# ============================================================

def ex02_list_employees() -> list[tuple[str, float]]:
    """返回 12 个员工的 (name, salary)，按 id 升序。"""
    # TODO
    return []


# ============================================================
# 第 3 题 · 参数化查询（第一个 ?）
# ============================================================

def ex03_by_dept(dept_id: int) -> list[tuple[str, float]]:
    """按 dept_id 查员工 (name, salary)，按 id 升序。

    要求：SQL 里用 `?` 占位，dept_id 作为参数传给 execute 的第二个参数
    （不要用 f-string 拼进去 —— 为什么？Day2 会讲）。
    """
    # TODO
    return []


# ============================================================
# 第 4 题 · fetchone
# ============================================================

def ex04_top_salary() -> tuple[str, float] | None:
    """返回工资最高的员工 (name, salary)；用 fetchone 取第一行。"""
    # TODO
    return None


# ============================================================
# 第 5 题 · 结果转 dict
# ============================================================

def ex05_rows_as_dict() -> list[dict[str, object]]:
    """把员工查成 [{"id":..., "name":..., "salary":...}, ...]，按 id 升序。

    提示：conn.row_factory = sqlite3.Row，然后 dict(row)
    """
    # TODO
    return []


# ============================================================
# 第 6 题 · 结果转对象（D4 学的类）
# ============================================================

class Employee:
    def __init__(self, emp_id: int, name: str, salary: float) -> None:
        self.id = emp_id
        self.name = name
        self.salary = salary

    def __repr__(self) -> str:
        return f"Employee({self.id}, {self.name!r}, {self.salary})"


def ex06_to_objects() -> list[Employee]:
    """把员工查询结果转成 Employee 对象列表（按 id 升序）。"""
    # TODO
    return []


# ============================================================
# 第 7 题 · 聚合查询
# ============================================================

def ex07_count_by_dept() -> dict[int, int]:
    """统计每个部门的员工数，返回 {dept_id: count}。

    注意：没有员工的部门（财务部）不会出现在结果里 —— 为什么？
    """
    # TODO
    return {}


# ============================================================
# 第 8 题 · 异常与连接关闭
# ============================================================

def ex08_safe_close() -> str:
    """用 try/finally 保证连接一定关闭；故意执行一条错误 SQL，
    捕获异常并返回**异常类型名**（例如 "OperationalError"）。
    """
    # TODO
    return ""


if __name__ == "__main__":
    check("ex01 表名", ex01_list_tables(), ["departments", "employees"])

    rows = ex02_list_employees()
    check("ex02 行数", len(rows), 12)
    check("ex02 第一行", rows[0] if rows else None, ("张伟", 25000.0))
    check("ex02 最后一行", rows[-1] if rows else None, ("冯磊", 17500.0))

    check("ex03 研发部人数", len(ex03_by_dept(1)), 4)
    check("ex03 研发部第一人", ex03_by_dept(1)[0] if ex03_by_dept(1) else None, ("张伟", 25000.0))
    check("ex03 不存在的部门", ex03_by_dept(999), [])

    check("ex04 工资最高", ex04_top_salary(), ("王强", 32000.0))

    d = ex05_rows_as_dict()
    check("ex05 行数", len(d), 12)
    check("ex05 第一条", d[0] if d else None, {"id": 1, "name": "张伟", "salary": 25000.0})

    objs = ex06_to_objects()
    check("ex06 对象数", len(objs), 12)
    check("ex06 第一个类型", type(objs[0]).__name__ if objs else None, "Employee")
    check("ex06 第一个名字", objs[0].name if objs else None, "张伟")

    check("ex07 按部门人数", ex07_count_by_dept(), {1: 4, 2: 3, 3: 3, 4: 2})

    check("ex08 异常类型", ex08_safe_close(), "OperationalError")
