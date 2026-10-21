# 07 · Python 中使用 SQL · 学习路线图（2026-10-21 制定）

> **学员提问**："后面会安排在 Python 中使用 SQL 的教程和练习吗？后端开发是需要在代码中使用的吧？"
> **答案：会，而且就在下周（10-26 起）。** 你观察得对 —— 目前 SQL 课全是"在 DBX 里手敲"，那只是**学习和排查**用的姿势。
> 真实后端里，SQL 是**代码发出去的**：
>
> ```python
> cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
> ```
>
> 这份文档把"从裸 SQL 到 ORM"的四层路线、时间安排、练习清单写清楚。

---

## 一、为什么"在代码里用 SQL"和"手敲 SQL"是两回事

| 维度 | DBX 里手敲 | 代码里用 |
|---|---|---|
| 谁执行 | 你自己一条条敲 | 程序自动执行 |
| 参数从哪来 | 你手写常量 | 用户输入 / 接口参数 → **必须参数化防注入** |
| 连接管理 | 客户端帮你连 | 你要自己建连接、关连接、用连接池 |
| 事务 | 你手敲 START/COMMIT | 代码里 `commit()/rollback()`，异常时自动回滚 |
| 结果处理 | 肉眼看表格 | `fetchall()` → list[dict] / tuple，再转对象 |
| 出错 | 你看报错 | 要 `try/except` + 决定重试还是回滚 |
| 复杂查询 | 直接写 | 可能用 ORM，也可能手写 SQL（复杂统计） |

**结论**：手敲 SQL 练的是"语法和思路"，代码里用 SQL 练的是"工程化"——两个都要会。

---

## 二、四层路线（从裸 SQL 到 ORM）

```text
L1 裸 SQL in Python      cursor / execute / fetchone / fetchall / with 管理连接
      ↓
L2 参数化与安全          %s 占位符（绝不用 f-string 拼 SQL）→ 防 SQL 注入
      ↓
L3 事务与连接池          commit / rollback / try-except / 连接复用（pool）
      ↓
L4 ORM（SQLAlchemy 2.x） 模型类 → 表；Session → 事务；自动生成 SQL；Alembic 迁移
```

| 层 | 学完能做什么 | 时间 | 时长 |
|---|---|---|---|
| **L1** | 用 Python 连 MySQL/PG，查出数据并打印/转换 | **10-26 周一** | 4h |
| **L2** | 写安全的增删改查函数（带参数，防注入） | **10-26 周一** | 3h |
| **L3** | 写"转账"式的事务代码，异常自动回滚；理解连接池 | **10-27 周二** | 4h |
| **L4** | 用 SQLAlchemy 定义模型、CRUD、关系映射；Alembic 做迁移 | **阶段 3/4（11-02 起）** | 阶段4 共 15h |

> **顺序很重要**：先学 L1–L3（裸 SQL），再学 L4（ORM）。
> 原因：面试和排障都要求"看得懂 ORM 生成的 SQL"，而且复杂查询很多时候要手写 SQL 绕过 ORM。

---

## 三、每层具体练什么（练习清单）

### L1 · 裸 SQL in Python（10-26，4h）

知识点：
- `pymysql`（MySQL）／ `psycopg`（PostgreSQL）怎么装、怎么连：
  ```python
  import pymysql
  conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                         password="123456", database="practice", charset="utf8mb4")
  ```
- `cursor = conn.cursor()`；`cursor.execute(sql)`；`cursor.fetchone() / fetchall()`
- 结果转成 `list[dict]`（`pymysql.cursors.DictCursor`）
- `with` / `try-finally` 管理连接，**保证 close**
- 常见异常：`pymysql.err.OperationalError`（连不上/密码错）、`ProgrammingError`（SQL 语法错）

练习（4 题）：
1. 连上 `practice` 库，查 12 个员工并打印姓名 + 工资
2. 把查询结果转成 `list[dict]`，再转成 `list[Employee]`（用 D4 学的类）
3. 参数化的单条件查询：输入部门名，返回该部门员工
4. 用 `try/except` 包住连接和查询，出错时打印清楚原因

### L2 · 参数化与安全（10-26，3h）

知识点：
- **错误写法**（SQL 注入）：
  ```python
  cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")   # ❌ name="' OR '1'='1" 就完蛋
  ```
- **正确写法**（参数化，驱动负责转义）：
  ```python
  cursor.execute("SELECT * FROM users WHERE name = %s", (name,))   # ✅
  ```
- `%s` 是**占位符**，不是字符串格式化；`executemany` 批量插入
- 列名/表名不能参数化（只能白名单校验）

练习（4 题）：
1. 把 L1 的查询**全部改成参数化**
2. 演示注入：用拼接写法 + `name = "' OR '1'='1"`，看到返回全部数据 → 再改成参数化，返回空
3. 写 `search_users(keyword)`：模糊查询 `LIKE %s`（注意 `%` 的转义）
4. 写 `insert_many(rows)`：用 `executemany` 一次插 100 条

### L3 · 事务与连接池（10-27，4h）

知识点：
- 关自动提交：`conn.autocommit(False)`（pymysql 默认就关）
- 事务三步：`conn.commit()` / `conn.rollback()`；异常时回滚
- 转账示例（**面试和实战都考**）：
  ```python
  try:
      cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
      cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
      conn.commit()
  except Exception:
      conn.rollback()
      raise
  ```
- 连接池：为什么不能每个请求都新建连接（开销）；SQLAlchemy `Engine` 的 pool 后面会在阶段 4 看到

练习（4 题）：
1. 写 `transfer(from_id, to_id, amount)`：成功 commit，异常 rollback
2. 故意让第二条 UPDATE 失败，验证两条都不生效（看数据库没变）
3. 对比"关掉事务自动提交"和"手动 commit"的区别
4. 说明为什么"每个请求新建连接"在生产环境不可接受

### L4 · SQLAlchemy 2.x（阶段 3/4，11-02 起）

- 定义模型：`class User(Base): __tablename__ = "users"`（D4 的 OOP 在这里派上用场）
- `Session` 管理事务；`select()` 查询；关系（`relationship()`）
- Alembic：把模型变更变成迁移脚本
- **会回看 L1–L3**：打印 SQLAlchemy 生成的 SQL（`echo=True`），确认自己能看懂

---

## 四、时间安排（更新到总排期）

| 日期 | 内容 | 时长 |
|---|---|---|
| 10-21 ~ 10-22 | SQL 考试冲刺（JOIN / 子查询 / 模拟卷） | — |
| 10-23 五 | **考试** | — |
| **10-26 一** | **L1 裸 SQL in Python + L2 参数化与安全** | 7h |
| **10-27 二** | **L3 事务与连接池** + Redis 入门 | 7h |
| 10-28 ~ 10-30 | Redis 五种结构 + 缓存场景 + 基础篇④造 + 阶段1验收收尾 | 剩余 |
| 11-02 起 | 阶段 3 FastAPI + 阶段 4 SQLAlchemy/Alembic（L4） | 45h |

> 具体教材我会在 **10-23 考试后、10-26 之前**写好（`exercises/stage2/python-sql/`），
> 包含：连库脚本模板 + 参数化练习 + 转账事务练习 + 预期结果自检清单。

---

## 五、先有个"形状感"：10 行预览

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root",
                       password="123456", database="practice",
                       charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cur:
        cur.execute("SELECT name, salary FROM employees WHERE dept_id = %s", (1,))
        rows = cur.fetchall()          # [{'name': '张伟', 'salary': ...}, ...]
    for r in rows:
        print(r["name"], r["salary"])
finally:
    conn.close()
```

**看完这段你就能发现**：
- 你学过的 SQL（`SELECT ... WHERE ...`）原样写在字符串里 —— **SQL 没白学**。
- `%s` 占位 + 参数元组 —— 这是防注入的关键（也是考试完要练的重点）。
- `with` / `try-finally` / `close` —— D3 学的文件管理思路，换成数据库连接一样用。
- 结果变成了 `list[dict]` —— 正是 D4 学的容器，后面能直接转成类对象。

---

## 六、一句话回答你的问题

> **会安排，就在下周（10-26）：L1 裸 SQL → L2 参数化防注入 → L3 事务与连接池 → 阶段 4 的 L4 ORM。**
> 你现在手敲 SQL 是打地基，下周开始学"把它接进 Python 程序"，阶段 4 再学"用 ORM 把它工程化"。
