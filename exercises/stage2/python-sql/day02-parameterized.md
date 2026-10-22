# Day 2（10-22 晚上）· 参数化与 SQL 注入

> **今天最重要的 10 分钟**：亲手看到同一串输入 `' OR '1'='1`，在"拼接"和"参数化"下返回**12 行 vs 0 行**的差别。
> 教材：[day02.py](day02.py)（8 题）
> Day1 回顾：[day01-dbapi.md](day01-dbapi.md)

---

## 一、先看后果：拼接 SQL 到底有多危险

### 你的代码（❌ 危险写法）

```python
attack = "' OR '1'='1"
sql = f"SELECT name FROM employees WHERE name = '{attack}'"
cur.execute(sql)
```

### 它实际执行的 SQL 长这样（我实测过）

```sql
SELECT name FROM employees WHERE name = '' OR '1'='1'
```

**`'1'='1'` 永远为真** → `WHERE` 条件整体为真 → **返回全部 12 个员工**。
一个普通输入框，就能让你查到全表数据；更狠的输入（`'; DROP TABLE employees; --`）甚至能删表。

### 参数化写法（✅ 正确）

```python
cur.execute("SELECT name FROM employees WHERE name = ?", (attack,))
```

**返回 0 行** —— 因为参数化之后，驱动把 `"' OR '1'='1"` 当成**一个普通的字符串值**（"名字叫这个的人"），
它不会再被解析成 SQL 结构。

> **一句话原理**：注入能成功，是因为**用户输入改变了 SQL 的结构**；
> 参数化保证"**结构是代码写死的，用户输入只当值**"。

---

## 二、占位符怎么写（两种数据库）

| 数据库 | 占位符 | 例子 |
|---|---|---|
| sqlite3 | **`?`** | `cur.execute("... WHERE dept_id = ?", (1,))` |
| pymysql / psycopg | **`%s`** | `cur.execute("... WHERE dept_id = %s", (1,))` |

**注意**：pymysql 的 `%s` **不是**字符串格式化，不要自己先 `%` 或 f-string 处理；也不要给值加引号。

---

## 三、三个高频位置

### 1. WHERE 的值

```python
cur.execute("SELECT name FROM employees WHERE dept_id = ?", (dept_id,))
```

### 2. LIKE 模糊查询

```python
cur.execute("SELECT name FROM employees WHERE name LIKE ?", (f"%{keyword}%",))
```

> 注意：`%` 要加在**参数里**，不能加到 SQL 字符串里。

### 3. IN 列表（占位符数量要动态生成）

```python
ids = [1, 2, 3]
placeholders = ",".join("?" for _ in ids)          # "?,?,?"
cur.execute(f"SELECT name FROM employees WHERE id IN ({placeholders})", ids)
```

这里的 f-string 只拼**占位符本身**（`?`），**值仍然走参数** —— 这是安全的。
（严格说还可以用 `executemany` 或临时表，先掌握这个写法。）

### 4. 不能参数化的东西：表名 / 列名 / ORDER BY

`ORDER BY ?` 是**错的**（会被当成排序一个常量）。列名只能用**白名单**：

```python
ALLOWED = {"id", "name", "salary"}

def safe_order_column(column: str) -> str:
    if column not in ALLOWED:
        raise ValueError("非法的排序列")
    return column
```

---

## 四、`executemany`：批量插入

```python
rows = [
    (13, "测试甲", 1, 10000.0, "2025-01-01", None),
    (14, "测试乙", 2, 12000.0, "2025-01-02", 4),
]
cur.executemany(
    "INSERT INTO employees (id, name, dept_id, salary, hire_date, manager_id) "
    "VALUES (?, ?, ?, ?, ?, ?)",
    rows,
)
```

- `rowcount` 返回影响行数
- 一条条 `execute` 也能插，但 `executemany` 更快、更不容易写错

---

## 五、练习（8 题，写在 [day02.py](day02.py)）

> 用法：`python day02.py`，看每行"对上了吗"。
> **第 2 题是故意写的不安全代码**，只为演示；其余所有题都必须参数化。

| # | 函数 | 要练什么 |
|---|---|---|
| 1 | `ex01_find_by_name(name)` | 最简参数化 `WHERE name = ?` |
| 2 | `ex02_injection_demo(attack)` | **故意拼接** → 输入 `' OR '1'='1` 返回 12 行 |
| 3 | `ex03_injection_blocked(attack)` | 参数化版本 → 同一输入返回 0 行 |
| 4 | `ex04_find_by_dept(dept_id)` | 参数化 + 排序 |
| 5 | `ex05_search(keyword)` | `LIKE ?`，`%` 放进参数 |
| 6 | `ex06_insert_many()` | 复制库 + `executemany` 插 3 条 |
| 7 | `ex07_safe_order_column(column)` | 列名白名单（不能参数化的东西） |
| 8 | `ex08_rollback_works()` | 插入后 `rollback()` → 查出来是 0 条 |

### 自检清单（预期值 · 已用参考实现核对）

| 题 | 预期 |
|---|---|
| 1 | `ex01("张伟")` → `["张伟"]`；`ex01("不存在")` → `[]` |
| 2 | 拼接出来的 SQL 是 `... WHERE name = '' OR '1'='1'` → **12 行** |
| 3 | 同一输入 → **0 行** |
| 4 | `ex04(1)` → 4 人：张伟、李娜、王强、郑爽 |
| 5 | `ex05("张")` → `["张伟"]` |
| 6 | `executemany` 的 `rowcount = 3` |
| 7 | `"salary"` → `"salary"`；非法列名 → 抛 `ValueError` |
| 8 | 回滚后查"测试"员工数 → `0` |

### 写不出来时的 5 级提示

1. **思路**：SQL 里把**值**换成 `?`，把**值**放进 `execute` 的第二个参数（元组）。
2. **伪代码**：`cur.execute("... WHERE x = ?", (x,))` → `fetchall()`。
3. **关键 API**：只有一个值的元组要写 `(1,)`；LIKE 用 `(f"%{kw}%",)`；`executemany` 第二个参数是"行的列表"。
4. **局部代码**：先做第 1、3、4 题（都是同一种写法），再做 5/6/7/8。
5. **完整答案**：连续两次卡住且主动要，我再给。

---

## 六、提交 + 验收

```text
【Python+SQL Day2 提交】
1. day02.py 跑完的输出（全 True 吗？哪几行 False）
2. 第 2 题拼接出来的完整 SQL 长什么样 + 返回几行
3. 第 3 题为什么返回 0 行（一句话）
4. 第 7 题：为什么列名不能用参数化？
5. 卡住的地方
```

- [ ] `python day02.py` → **全部"对上了吗: True"**
- [ ] 能一句话说清 SQL 注入的原理
- [ ] 能写出 WHERE / LIKE / IN 三种参数化
- [ ] 能说清"哪些东西不能参数化"（表名、列名、ORDER BY → 白名单）
- [ ] 会用 `executemany` 批量插入
