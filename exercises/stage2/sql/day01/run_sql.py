"""SQL 练习运行器（SQLite 版，零安装）

用法（在 exercises/stage2/sql/day01/ 目录下）：

    python run_sql.py                        # ① 建库 + 灌入练习数据（第一次必跑）
    python run_sql.py "SELECT * FROM employees LIMIT 3;"     # ② 跑一条 SQL
    python run_sql.py -f answers.sql         # ③ 跑整个作答文件

说明：
    - 数据库文件 practice.db 就生成在本目录（已 gitignore，不影响提交）
    - 用 SQLite 是为了"今晚 0 分钟环境"；第 4 天会切到 PostgreSQL/MySQL 跑一遍
    - 按分号切语句，所以练习里别在字符串里写分号
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "practice.db"
SCHEMA_PATH = HERE / "schema.sql"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def rebuild() -> None:
    conn = connect()
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
    print(f"[OK] 已重建练习库: {DB_PATH}")
    print('可以开始了，例如： python run_sql.py "SELECT * FROM departments;"')


def run_one(sql: str) -> None:
    sql = sql.strip()
    if not sql:
        return
    conn = connect()
    try:
        cur = conn.execute(sql)
        if cur.description is None:
            conn.commit()
            print(f"[OK] 执行成功（影响 {cur.rowcount} 行）")
            return
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print(" | ".join(cols))
        print("-" * 60)
        for row in rows:
            print(" | ".join("NULL" if row[c] is None else str(row[c]) for c in cols))
        print(f"（{len(rows)} 行）")
    except sqlite3.Error as exc:
        print(f"[SQL 错误] {exc}")
    finally:
        conn.close()


def split_statements(text: str) -> list[str]:
    """按分号切语句；跳过纯注释块。练习够用（不在字符串里写分号）。"""
    statements: list[str] = []
    for chunk in text.split(";"):
        lines = [line for line in chunk.splitlines() if not line.strip().startswith("--")]
        stmt = "\n".join(lines).strip()
        if stmt:
            statements.append(stmt)
    return statements


def run_file(path: Path) -> None:
    statements = split_statements(path.read_text(encoding="utf-8"))
    print(f"共 {len(statements)} 条语句\n")
    for i, stmt in enumerate(statements, 1):
        print(f"===== 第 {i} 条 =====")
        run_one(stmt)
        print()


def main(argv: list[str]) -> int:
    if not argv:
        rebuild()
        return 0
    if not DB_PATH.exists():
        rebuild()
    if argv[0] == "-f":
        if len(argv) < 2:
            print("用法: python run_sql.py -f <文件.sql>")
            return 1
        run_file(Path(argv[1]))
        return 0
    run_one(" ".join(argv))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
