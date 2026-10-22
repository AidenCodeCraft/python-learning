"""Python 中使用 SQL · Day 2（参数化与 SQL 注入）· 作答文件

用法：
    cd exercises/stage2/python-sql
    python day02.py

数据库：
  - 只读用 ../sql/day01/practice.db
  - 写操作用副本 .tmp/practice_copy.db（脚本会自动复制）
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
READONLY_DB = ROOT.parent / "sql" / "day01" / "practice.db"
WORK_DIR = ROOT / ".tmp"
WORK_DB = WORK_DIR / "practice_copy.db"


def check(label: str, actual: object, expect: object) -> None:
    print(f"{label:<30} 实际={actual!r:<34} 预期={expect!r:<34} 对上了吗: {actual == expect}")


def _connect(db: Path = READONLY_DB) -> sqlite3.Connection:
    """连接（只读库/副本都用它）；调用方自己负责 close。"""
    return sqlite3.connect(db)


# ============================================================
# 第 1 题 · 参数化最简形式
# ============================================================

def ex01_find_by_name(name: str) -> list[str]:
    """返回名字等于 name 的员工姓名列表（按 id 升序）。

    要求：`WHERE name = ?`，name 作为参数传入。
    """
    # TODO
    return []


# ============================================================
# 第 2 题 · 【故意不安全】演示 SQL 注入
# ============================================================

def ex02_injection_demo(attack: str) -> int:
    """【这是故意写的不安全代码，只为演示，生产代码禁止这样写】

    用 f-string 把 attack 拼进 SQL：
        f"SELECT name FROM employees WHERE name = '{attack}'"
    返回查询结果的行数。

    用它跑 attack = "' OR '1'='1" → 应该返回 12（全部员工！）
    """
    # TODO
    return 0


# ============================================================
# 第 3 题 · 参数化挡住注入
# ============================================================

def ex03_injection_blocked(attack: str) -> int:
    """参数化版本：同样的 attack，应该返回 0 行。

    原因：参数化后，驱动把整串当成"一个普通字符串值"，
    `' OR '1'='1` 会被当成"名字叫这个的人"去匹配，不会再被解析成 SQL。
    """
    # TODO
    return 0


# ============================================================
# 第 4 题 · 参数化 + 多行
# ============================================================

def ex04_find_by_dept(dept_id: int) -> list[str]:
    """按 dept_id 查员工姓名（按 id 升序）。"""
    # TODO
    return []


# ============================================================
# 第 5 题 · LIKE 的参数化
# ============================================================

def ex05_search(keyword: str) -> list[str]:
    """模糊搜索：返回 name 里包含 keyword 的员工姓名（按 id 升序）。

    提示：SQL 里写 `WHERE name LIKE ?`，参数传 `f"%{keyword}%"`。
    """
    # TODO
    return []


# ============================================================
# 第 6 题 · executemany 批量插入（写副本库）
# ============================================================

def ex06_insert_many() -> int:
    """把 3 条员工插进副本库的 employees 表，返回这 3 条的总数（3）。

    要求：
      1. 先确保 WORK_DB 存在（把 READONLY_DB 复制过去，见文件顶部常量）
      2. 用 executemany 一次插入：
           ("测试甲", 1, 10000.0, "2025-01-01", None)
           ("测试乙", 2, 12000.0, "2025-01-02", 4)
           ("测试丙", 3, 15000.0, "2025-01-03", 6)
         注意 id 是主键自增？—— practice.db 的 employees.id **不是自增**，
         所以插入时必须手动给 id（用 MAX(id)+1 起）。
      3. 插入后 commit，返回插入的行数
    """
    # TODO
    return 0


# ============================================================
# 第 7 题 · 列名不能参数化 → 白名单
# ============================================================

ALLOWED_COLUMNS = {"id", "name", "salary"}


def ex07_safe_order_column(column: str) -> str:
    """排序时如果列名来自用户输入，必须用**白名单**校验。

    规则：column 在 ALLOWED_COLUMNS 里 → 返回 column
          否则 → 抛 ValueError("非法的排序列")
    """
    # TODO
    return ""


# ============================================================
# 第 8 题 · executemany + 事务回滚
# ============================================================

def ex08_rollback_works() -> int:
    """验证"事务里插入后回滚，数据真的没进去"。

    步骤（在副本库上）：
      1. 复制库（如果还没有）
      2. START TRANSACTION（sqlite3 里：conn.execute("BEGIN")）
      3. executemany 插入 3 条
      4. conn.rollback()
      5. 查询这个"测试"员工数量（应为 0）
    返回第 5 步查到的数量。
    """
    # TODO
    return -1


if __name__ == "__main__":
    check("ex01 find_by_name('张伟')", ex01_find_by_name("张伟"), ["张伟"])
    check("ex01 find_by_name('不存在')", ex01_find_by_name("不存在"), [])

    check("ex02 注入攻击行数", ex02_injection_demo("' OR '1'='1"), 12)
    check("ex03 参数化后行数", ex03_injection_blocked("' OR '1'='1"), 0)

    names = ex04_find_by_dept(1)
    check("ex04 研发部人数", len(names), 4)
    check("ex04 研发部第一个", names[0] if names else None, "张伟")

    check("ex05 search('张')", ex05_search("张"), ["张伟"])

    inserted = ex06_insert_many()
    check("ex06 插入行数", inserted, 3)

    check("ex07 allow('salary')", ex07_safe_order_column("salary"), "salary")
    try:
        ex07_safe_order_column("id; DROP TABLE employees")
        check("ex07 非法列名", "没抛异常", "ValueError")
    except ValueError:
        check("ex07 非法列名", "ValueError", "ValueError")

    check("ex08 回滚后行数", ex08_rollback_works(), 0)
