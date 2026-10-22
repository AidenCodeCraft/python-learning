# Day 1（10-22 下午）· DB-API 基础：在 Python 里执行 SQL

> **为什么从今天开始**：考试明天不正规（可上网查），没必要再刷题。
> 后端真正的工作方式是"**代码发 SQL**"，这一层越早开始越好。
> 数据库：直接用 SQL 练习时那个 `practice.db`（`exercises/stage2/sql/day01/practice.db`）—— **只读**。
>
> 教材顺序：[README](README.md) → **Day1（本文件）** → [Day2 参数化](day02-parameterized.md) → Day3 事务

---

## 一、DB-API 2.0：Python 访问数据库的标准姿势（五步）

```python
import sqlite3

# ① 连接
conn = sqlite3.connect("practice.db")

# ② 游标
cur = conn.cursor()

# ③ 执行 SQL
cur.execute("SELECT name, salary FROM employees WHERE dept_id = ?", (1,))

# ④ 取结果
rows = cur.fetchall()          # 列表；fetchone() 取一行

# ⑤ 关闭
cur.close()
conn.close()
```

**这五步在 pymysql / psycopg 里完全一样**，只是连接参数和占位符不同：

| | sqlite3（Python 自带） | pymysql（MySQL） | psycopg（PostgreSQL） |
|---|---|---|---|
| 安装 | 不用装 | `pip install pymysql` | `pip install psycopg[binary]` |
| 连接 | `sqlite3.connect("x.db")` | `pymysql.connect(host=..., user=..., password=..., database=...)` | `psycopg.connect("host=... dbname=...")` |
| **占位符** | **`?`** | **`%s`** | **`%s`** |
| 取 dict | `conn.row_factory = sqlite3.Row` | `cursorclass=DictCursor` | `row_factory=dict_row` |
| 异常基类 | `sqlite3.Error` | `pymysql.err.MySQLError` | `psycopg.Error` |

> 今天先用 **sqlite3**（0 安装、和网站无关的本地文件库）把"代码里用 SQL"的手感练出来；
> 明天再切到 **pymysql + MySQL**，你会发现在这两者之间迁移只需改两行。

---

## 二、三个必须知道的知识点

### 1. 参数化：`execute(sql, params)` —— 从第一天就用

```python
# ✅ 正确：SQL 里放占位符，值通过第二个参数传
cur.execute("SELECT name FROM employees WHERE dept_id = ?", (1,))

# ❌ 错误：把值拼进字符串（Day2 会演示它有多危险）
cur.execute(f"SELECT name FROM employees WHERE dept_id = {dept_id}")
```

注意：**参数是元组，哪怕只有一个也要写逗号**：`(1,)` 而不是 `(1)`。

### 2. `with` 和"关闭连接"是两个概念

```python
with sqlite3.connect("x.db") as conn:   # 这个 with 只管"事务提交/回滚"
    ...
# 出了 with，连接**不一定会关闭**！
```

**正确做法**：用 `try/finally` 或 `contextlib.closing` 保证 `close()`：

```python
conn = sqlite3.connect("x.db")
try:
    ...
finally:
    conn.close()
```

### 3. 结果是"行"，不是"字典"

`fetchall()` 默认返回 **tuple 列表**：`[('张伟', 25000.0), ...]`。
想要字典：`conn.row_factory = sqlite3.Row`，然后 `dict(row)`。
想要对象：自己写个转换（Day1 第 6 题就是干这个）。

| 方法 | 返回 | 用在哪 |
|---|---|---|
| `fetchone()` | 一行（tuple/Row）或 `None` | 查单条（最高工资、按 id 查） |
| `fetchall()` | 全部行（list） | 列表页、报表 |
| `fetchmany(n)` | 前 n 行 | 大结果分批 |

---

## 三、练习（8 题，写在 [day01.py](day01.py)）

> 用法：`python day01.py`，每写完一题跑一次，看"对上了吗"。
> **数据库只读**，这 8 题全是查询。

| # | 函数 | 要练什么 |
|---|---|---|
| 1 | `ex01_list_tables()` | 连接 + 查 `sqlite_master`，返回表名列表 |
| 2 | `ex02_list_employees()` | `fetchall` + 排序 |
| 3 | `ex03_by_dept(dept_id)` | **参数化占位符 `?`** |
| 4 | `ex04_top_salary()` | `fetchone` |
| 5 | `ex05_rows_as_dict()` | `row_factory` + `dict(row)` |
| 6 | `ex06_to_objects()` | 结果 → `Employee` 对象（D4 的类） |
| 7 | `ex07_count_by_dept()` | `GROUP BY` → `dict` |
| 8 | `ex08_safe_close()` | `try/finally` + 捕获 `sqlite3.Error` 返回异常类型名 |

### 写不出来时的 5 级提示

1. **思路**：这题是"取一行"还是"取多行"？→ 选 `fetchone` / `fetchall`。
2. **伪代码**：`conn = connect(...)` → `cur.execute(sql, params)` → `rows = cur.fetchall()` → `finally: conn.close()`。
3. **关键 API**：`sqlite3.connect(path)`；`Path(__file__).parent.parent / "sql" / "day01" / "practice.db"`；`sqlite3.Row`。
4. **局部代码**：先把第 2 题跑通，其余都只是换 SQL。
5. **完整答案**：连续两次卡住且主动要，我再给。

### 自检清单（预期值 · 已用参考实现核对）

| 题 | 预期 |
|---|---|
| 1 | `['departments', 'employees']` |
| 2 | 12 行；第一行 `('张伟', 25000.0)`；最后一行 `('冯磊', 17500.0)` |
| 3 | `dept_id=1` → 4 行，第一行 `('张伟', 25000.0)`；`dept_id=999` → `[]` |
| 4 | `('王强', 32000.0)` |
| 5 | 12 条 dict；第一条 `{'id': 1, 'name': '张伟', 'salary': 25000.0}` |
| 6 | 12 个 `Employee` 对象；第一个 `.name == '张伟'` |
| 7 | `{1: 4, 2: 3, 3: 3, 4: 2}`（为什么没有 5 财务部？因为 GROUP BY 的来源是 employees 表） |
| 8 | `'OperationalError'`（错误 SQL 抛的是它，属于 `sqlite3.Error` 子类） |

---

## 四、提交

```text
【Python+SQL Day1 提交】
1. day01.py 跑完的输出（"对上了吗"全 True 吗？哪几行 False）
2. 第 3 题你是怎么写参数化的（贴代码）
3. 第 8 题 try/finally 的写法
4. 卡住的地方
```

## 五、Day1 验收标准

- [ ] `python day01.py` → **全部"对上了吗: True"**
- [ ] 能背出 DB-API 五步（连接→游标→执行→取结果→关闭）
- [ ] 能说出 `?`（sqlite3）和 `%s`（pymysql）的区别
- [ ] 能说出"为什么 `with connect()` 不等于关闭连接"
- [ ] 能说出 `fetchone` / `fetchall` / `fetchmany` 各用在哪
