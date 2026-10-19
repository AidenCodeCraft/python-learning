# 阶段 2 · SQL Day 1（2026-10-20 周二）· 数据库基础 + SELECT + 增删改查

> **这是合并日**：原 day01（SELECT）+ day02（增删改查）+ 数据库理论，合成一天（因 10-19 无法学习）。
> **考纲原文**："增删改查会基本就行" → 今天的内容**完整覆盖考纲**，并且补上职业需要的理论基础。
>
> 📚 理论课 → [01-数据库基础理论.md](01-数据库基础理论.md)（90 分钟）
> 🗺️ 知识全景 → [00-数据库知识地图.md](../00-数据库知识地图.md)
> 🛠️ 环境搭建 → [../mysql/setup.md](../mysql/setup.md)
> 📅 排期依据 → [06-排期重排](../../../../notes/06-排期重排-工作日9h与SQL考试.md)

---

## 一、今天的 9 小时怎么用

| 时段 | 时长 | 做什么 |
|---|---:|---|
| 早上 | 15min | **搭 MySQL + DBX 连上 + 执行 `init.sql`**（见 [setup.md](../mysql/setup.md)） |
| 上午 | 90min | 读 [01-数据库基础理论.md](01-数据库基础理论.md) → 做 25 题自测（错 ≤5 题算过关） |
| 上午剩余 | 1.5h | **第 2 部分：SELECT 12 题**（先在 MySQL 上重做；本地的 `run_sql.py` 可当速查工具） |
| 下午 | 3h | **第 3 部分：增删改查 12 题**（考试核心，全部在 DBX 里做） |
| 晚上 | 40~60min | 基础篇训练 00 方法课：[三段设计法](../../../stage1/基础篇-从零构建/00-方法-三段设计法.md)（**不写代码**） |
| 晚上剩余 | 30min | 错题本 `mistakes/2026-10-20.md` + 提交 |

> ⚠️ 中文乱码先在终端执行 `chcp 65001`。

---

## 二、今日目标（合并后共 11 条）

**理论层（上午）**
1. 说清数据库 vs Excel 的区别（并发/约束/查询/恢复）
2. 说清主键 / 候选键 / 外键，以及"为什么互联网公司常不用物理外键"
3. 说出 **SQL 五大分类**（DDL/DML/DQL/DCL/TCL）各含哪些语句
4. 会选数据类型：金额 `DECIMAL`、id `BIGINT`、字符集 `utf8mb4`
5. 能说出三范式各消除什么依赖，以及什么时候反范式

**操作层（上午 + 下午）**
6. 写 `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT` 五件套
7. 用 `COUNT / SUM / AVG / MIN / MAX` 做统计，用 `GROUP BY` 分组
8. 记住三条易错：`NULL` 用 `IS NULL`、聚合用 `HAVING` 过滤、字符串用单引号
9. 会 `CREATE TABLE` 建表（类型 + 主键 + 非空 + 自增）
10. 会 `INSERT` / `UPDATE` / `DELETE`，并养成"先 SELECT 确认再改"的习惯
11. 能说清事务的 `START TRANSACTION` / `COMMIT` / `ROLLBACK`

---

## 三、第 1 部分：练习环境（15 分钟）

### 路线 A：MySQL（**考试同款，必须做**）

按 [../mysql/setup.md](../mysql/setup.md) 起一个 MySQL 8.0（Docker / 安装包 / 公司现成库，三选一），
用 **DBX** 连上，执行 [../mysql/init.sql](../mysql/init.sql) 建好 `practice` 库。

### 路线 B：本地 SQLite 速查（可选，0 分钟）

不想开 DBX 时，可以用本目录的 SQLite 工具快速验证语法：

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
cd exercises\stage2\sql\day01
python run_sql.py                                  # 建库（只需一次）
python run_sql.py "SELECT * FROM employees LIMIT 5;"
```

> ⚠️ 但**考试是机考 MySQL**，最终答案必须在 MySQL 里跑对过。SQLite 只用来"随手验证语法"。

### 练习库结构（两张表）

| departments（部门） | 说明 |
|---|---|
| `id` | 主键 |
| `name` | 部门名 |

| employees（员工） | 说明 |
|---|---|
| `id` | 主键 |
| `name` | 姓名 |
| `dept_id` | 外键 → departments.id |
| `salary` | 工资（DECIMAL） |
| `hire_date` | 入职日期（DATE） |
| `manager_id` | 上级的 id（可为 NULL） |

**记住这个关系**：`employees.dept_id` 指向 `departments.id` —— 明天学 `JOIN` 就靠它把两张表连起来。

---

## 四、第 2 部分：SELECT 基础 + 12 题（1.5h）

### 4.1 一条 SELECT 的完整骨架

```sql
SELECT   要哪些列
FROM     哪张表
WHERE    按什么条件过滤（逐行判断真假）
ORDER BY 按什么排序（ASC 升序 / DESC 降序）
LIMIT    只要前几条
```

**书写顺序**是上面这样，但**执行顺序不一样**（考试爱考）：

```text
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

→ `WHERE` 在 `SELECT` **之前**执行，所以 `WHERE` 里**不能**用 `SELECT` 起的别名，也不能用聚合函数。

### 4.2 WHERE：比较 / 逻辑 / 模糊 / 区间 / 枚举

```sql
WHERE salary > 20000
WHERE salary >= 15000 AND salary <= 20000
WHERE name LIKE '张%'                  -- % 任意多个字符；_ 一个字符
WHERE salary BETWEEN 15000 AND 20000   -- 含端点
WHERE dept_id IN (1, 3)
WHERE manager_id IS NULL               -- ⚠️ 不能写 = NULL
```

`NULL` 不等于任何值（连 `NULL = NULL` 都不成立），必须用 `IS NULL` / `IS NOT NULL`。

### 4.3 ORDER BY + LIMIT

```sql
ORDER BY salary DESC            -- 从高到低
ORDER BY salary DESC, name ASC  -- 先按工资降序，工资相同再按姓名升序
LIMIT 3                         -- 前 3 条（取 Top N）
```

### 4.4 聚合函数（多行变一行）

| 函数 | 作用 |
|---|---|
| `COUNT(*)` | 数行数 |
| `COUNT(列名)` | 数这一列**非 NULL** 的个数 |
| `SUM(列)` / `AVG(列)` | 求和 / 平均 |
| `MIN(列)` / `MAX(列)` | 最小 / 最大 |

```sql
SELECT COUNT(*), AVG(salary) FROM employees;   -- 12 | 19958.3333...
```

`ROUND(x, 2)` 保留 2 位小数。

### 4.5 GROUP BY + HAVING

```sql
SELECT dept_id, COUNT(*) AS cnt
FROM employees
GROUP BY dept_id;
```

**规则**：`GROUP BY` 之后 `SELECT` 里只能出现两种东西 —— ① 分组列 ② 聚合函数。
（写别的列在 MySQL 里可能"容忍"，在 PostgreSQL / 考场标准答案里就是**错**。）

`HAVING` 是"分组之后"的过滤（`WHERE` 是分组之前）：

```sql
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 15000;
```

### 4.6 起别名 `AS` 与三条格式注意

```sql
SELECT name AS 姓名, salary AS 工资 FROM employees;
```

1. 字符串用**单引号**：`'张%'`；2. 语句以**分号**结尾；3. 关键字大小写不敏感，但习惯大写关键字。

### 4.7 SELECT 练习（12 题）

> 在 DBX 里新建一个 SQL 标签，每题写一条，**单条执行**，对照 4.8 的自检清单。
> **不给答案，只给预期结果**，自己判对错。

| # | 题目 | 提示 |
|---|---|---|
| 1 | 查所有员工的所有字段（按 id 升序） | `SELECT *` |
| 2 | 只查 `name` 和 `salary`（按 id 升序） | 列清单 |
| 3 | 查**研发部**（`dept_id = 1`）所有员工的姓名、工资（按 id 升序） | `WHERE ... AND` |
| 4 | 查工资 **> 20000** 的员工姓名、工资（按工资从高到低） | `ORDER BY ... DESC` |
| 5 | 查工资在 **15000 ~ 20000 之间**（含端点）的姓名、工资（按工资升序） | `BETWEEN` |
| 6 | 查工资最高的**前 3 名**（姓名、工资，从高到低） | `ORDER BY + LIMIT` |
| 7 | 公司总人数（一个数） | `COUNT(*)` |
| 8 | 平均工资（保留 2 位小数，别名 `avg_salary`） | `AVG + ROUND` |
| 9 | 最高工资和最低工资（两个列：`max_salary`、`min_salary`） | `MAX / MIN` |
| 10 | 每个部门的员工数（列：`dept_id`、`cnt`，按 dept_id 升序） | `GROUP BY` |
| 11 | 每个部门的平均工资，从高到低（列：`dept_id`、`avg_salary`，保留 2 位小数） | `GROUP BY + ORDER BY 聚合结果` |
| 12 | 名字里带"张"的员工姓名 | `LIKE '张%'` |

### 4.8 SELECT 自检清单（预期结果 · 已用参考实现核对）

> MySQL 里 `DECIMAL` 会显示 `25000.00`；SQLite 显示 `25000.0`。**看数值本身对就行。**

| # | 预期 | 行数 |
|---|---|---|
| 1 | 12 行，6 列（`id, name, dept_id, salary, hire_date, manager_id`） | 12 |
| 2 | 12 行（name, salary） | 12 |
| 3 | 张伟 25000、李娜 18000、王强 32000、郑爽 21000 | 4 |
| 4 | 王强 32000、赵敏 28000、张伟 25000、刘洋 22000、郑爽 21000 | 5 |
| 5 | 杨帆 15000、陈静 16000、冯磊 17500、李娜 18000、孙磊 19000 | 5 |
| 6 | 王强 32000、赵敏 28000、张伟 25000 | 3 |
| 7 | `12` | 1 |
| 8 | `19958.33` | 1 |
| 9 | `32000` / `12000` | 1 |
| 10 | `1→4`、`2→3`、`3→3`、`4→2` | 4 |
| 11 | `1→24000.00`、`3→20666.67`、`2→18500.00`、`4→13000.00` | 4 |
| 12 | 张伟 | 1 |

**对不上的题号记下来，写进错题本。**

---

## 五、第 3 部分：增删改查 12 题（3h，考试核心）

> 这部分**必须在 MySQL 里做**（不是 SQLite）—— 机考就是 MySQL。
> 12 题**按顺序**做：前面建表/插入的结果，后面会用到。

### 5.1 `CREATE TABLE`：常用类型与约束

```sql
CREATE TABLE students (
    id         INT PRIMARY KEY AUTO_INCREMENT,   -- 自增整数主键
    name       VARCHAR(50) NOT NULL,             -- 变长字符串，必须给长度
    score      INT NOT NULL DEFAULT 0,           -- 整数，默认 0
    class_name VARCHAR(20)
);
```

| 类型 | 用途 | 说明 |
|---|---|---|
| `INT` | 整数 | 自增主键用 `INT PRIMARY KEY AUTO_INCREMENT` |
| `VARCHAR(n)` | 短字符串 | **必须写长度** |
| `TEXT` | 长文本 | 不用写长度 |
| `DECIMAL(10,2)` | 金额/精确小数 | 10 位数字，其中 2 位小数 |
| `DATE` / `DATETIME` | 日期 / 日期时间 | `'2026-10-20'` / `'2026-10-20 13:30:00'` |

约束：`PRIMARY KEY`、`NOT NULL`、`DEFAULT`、`UNIQUE`、`FOREIGN KEY`。

### 5.2 `INSERT`：增

```sql
-- 单行（推荐写列名，别依赖列顺序）
INSERT INTO students (name, score, class_name) VALUES ('张三', 85, '一班');

-- 多行（一条语句插多行，比写多条快）
INSERT INTO students (name, score, class_name) VALUES
    ('李四', 92, '一班'),
    ('王五', 48, '二班');
```

`id` 是自增的，**不用也不该手动插入**。

### 5.3 `UPDATE`：改 —— **必须带 WHERE！**

```sql
-- ⚠️ 危险写法：整张表所有人的分数都变成 90
UPDATE students SET score = 90;

-- 正确写法：只改一个人
UPDATE students SET score = 90 WHERE name = '张三';
```

**安全三步法（真实工作也这么干）**：

```sql
SELECT * FROM students WHERE class_name = '二班';                    -- ① 先看会改到谁
UPDATE students SET score = score + 5 WHERE class_name = '二班';     -- ② 再改
SELECT * FROM students WHERE class_name = '二班';                    -- ③ 确认结果
```

### 5.4 `DELETE`：删 —— **必须带 WHERE！**

```sql
DELETE FROM students WHERE name = '王五';
```

三个"删"的区别（**考试常考**）：

| 语句 | 删什么 | 能带 WHERE | 能回滚 |
|---|---|---|---|
| `DELETE FROM t WHERE ...` | 删符合条件的**行** | ✅ | ✅（事务里） |
| `TRUNCATE TABLE t` | 清空整张表（表还在） | ❌ | ❌ |
| `DROP TABLE t` | 连**表结构一起删** | ❌ | ❌ |

### 5.5 `ALTER TABLE`：改表结构

```sql
ALTER TABLE students ADD COLUMN email VARCHAR(100);
ALTER TABLE students MODIFY COLUMN email VARCHAR(200);
ALTER TABLE students DROP COLUMN email;
```

### 5.6 事务

**一句话**：事务 = "一组要么全成功、要么全不算数的操作"（典型场景：转账 A 扣钱 + B 加钱）。

```sql
START TRANSACTION;
UPDATE students SET score = score + 2 WHERE class_name = '一班';
ROLLBACK;          -- 撤销，等于什么都没发生
-- 或
COMMIT;            -- 确认，永久生效
```

### 5.7 MySQL 必备小命令

```sql
SELECT VERSION();
SHOW DATABASES;
USE practice;
SHOW TABLES;
DESCRIBE students;
```

### 5.8 增删改查练习（12 题，按顺序）

> 在 DBX 里新建一个 SQL 编辑器标签，每题写进去、**按顺序单条执行**。
> 做完对照 5.9 的自检清单。**不许一次全选执行。**

| # | 题目 | 提示 |
|---|---|---|
| 1 | 建表 `students`：`id` 自增主键、`name` 不许空、`score` 整数默认 0、`class_name` 变长 20 | `CREATE TABLE` |
| 2 | 插入一行：张三，85 分，一班 | `INSERT INTO ... VALUES` |
| 3 | 一条语句插入三行：李四 92 一班、王五 **48** 二班、赵六 76 二班 | 多行 VALUES |
| 4 | 查出所有学生（按 id 升序） | `SELECT *` |
| 5 | 把张三的分数改成 90 | `UPDATE ... WHERE` |
| 6 | 给**二班所有人**加 5 分 | `SET score = score + 5` |
| 7 | 把**低于 60 分**的人改成 60 | `UPDATE ... WHERE score < 60` |
| 8 | 删除王五 | `DELETE ... WHERE` |
| 9 | 删除三班的所有学生（注意：三班可能不存在） | 看影响几行 |
| 10 | 统计：总人数、平均分（保留 2 位小数） | `COUNT(*)`、`ROUND(AVG(score),2)` |
| 11 | 给表加一列 `email VARCHAR(100)` | `ALTER TABLE ... ADD COLUMN` |
| 12 | 事务练习：`START TRANSACTION` → 一班所有人 +2 → `ROLLBACK` → 查分数；再 `START TRANSACTION` → +2 → `COMMIT` → 查分数 | 两次结果不同 |

### 5.9 增删改查自检清单（预期结果 · 已逐条核对）

| # | 预期 |
|---|---|
| 1 | 表创建成功，`DESCRIBE students;` 能看到 4 个字段 |
| 2 | 影响 1 行，张三的 `id = 1` |
| 3 | 影响 3 行，id 依次是 2、3、4 |
| 4 | **4 行**（张三 85 一班 / 李四 92 一班 / 王五 48 二班 / 赵六 76 二班） |
| 5 | 影响 **1** 行，张三变 90 |
| 6 | 影响 **2** 行，二班变成 王五 53、赵六 81 |
| 7 | 影响 **1** 行（王五 53 → 60）；**如果显示 0 行，说明你第 6 题没做对** |
| 8 | 影响 **1** 行；剩 3 人 |
| 9 | 影响 **0** 行（没有三班）—— **0 行不是错，是正确结果** |
| 10 | `3` 人，平均 `87.67`（(90+92+81)/3 = 87.666…） |
| 11 | 成功，`DESCRIBE students;` 多出 `email` 列 |
| 12 | **ROLLBACK 后**：一班还是 张三 90 / 李四 92；**COMMIT 后**：张三 92 / 李四 94 |

> 最终状态（12 题全做完）：**张三 92、李四 94、赵六 81**，加一列 email，共 3 人。

### 5.10 写不出来时的 5 级提示（两部分通用）

1. **思路**：这题是"改结构"（DDL）还是"改数据"（DML）还是"查"（DQL）？
2. **伪代码**：`UPDATE 表 SET 列 = 值 WHERE 条件;`
3. **关键 API**：自增 `AUTO_INCREMENT`；加分 `SET score = score + 5`；区间 `BETWEEN a AND b`；Top N `ORDER BY + LIMIT`
4. **局部代码**：先写 `WHERE` 那条 `SELECT` 确认选中数据对了，再改成 `UPDATE` / `DELETE`
5. **完整答案**：连续两次卡住且你主动要，我再给

---

## 六、复盘 + 提交（30 分钟）

1. 新建 `mistakes/2026-10-20.md`（照 D1–D4 格式：现象 → **概念层**错因 → 正确写法 → 变式）。
2. 把作答写进两个模板文件：
   - SELECT 12 题 → [answers.sql](answers.sql)（可用 `python run_sql.py -f answers.sql` 一次跑完）
   - 增删改查 12 题 → [answers_crud.sql](answers_crud.sql)（在 DBX / MySQL 里按顺序执行）
3. 发我：

```text
【阶段2 SQL Day1 提交（合并日）】
1. 理论自测 25 题：错了几题？错的是哪几个知识点？
2. SELECT 12 题：自检清单对不上的题号
3. 增删改查 12 题：自检清单对不上的题号（重点 6/7/9/12）
4. 三个易错点记住了没：UPDATE/DELETE 必须带 WHERE、0 行也可能正确、事务回滚
5. 构建训练 Day1 的三张设计卡
6. git log --oneline
```

```powershell
git add exercises/stage2 exercises/stage1 notes
git commit -m "feat(stage2): SQL Day1 理论+SELECT+增删改查（合并日）+ 构建训练营"
```

---

## 七、今日验收标准

**理论**
- [ ] 主键 / 候选键 / 外键的区别说得清
- [ ] SQL 五大分类 + 每类 2 个语句
- [ ] 金额为什么用 `DECIMAL`、id 为什么用 `BIGINT`、字符集为什么用 `utf8mb4`
- [ ] 三范式各消除什么依赖
- [ ] 理论自测 25 题 **错 ≤5 题**

**操作**
- [ ] SELECT 12 题：**至少 10 题**对上
- [ ] 增删改查 12 题：**至少 11 题**对上
- [ ] 能说出 SQL 执行顺序（`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`）
- [ ] 能说出 `DELETE` / `TRUNCATE` / `DROP` 的区别
- [ ] 能解释第 9 题为什么影响 0 行是正确的
- [ ] 能说清 `ROLLBACK` 和 `COMMIT` 的区别

**构建训练**
- [ ] 三张设计卡写完（只有设计，没有代码）

---

## 八、明天（10-21 周三）：JOIN + 子查询

| 时段 | 内容 |
|---|---|
| 上午 | `JOIN`（INNER / LEFT）讲解 + 25 题 |
| 下午 | 子查询 + `GROUP BY` 综合 + 25 题 |
| 晚上 | 基础篇 ①读 + ②抄：读 [word_counter.py](../../../stage1/基础篇-从零构建/reference/word_counter.py) → 逐行注释 → 手抄跑通 |

> **本周不碰**：索引原理、EXPLAIN、事务隔离级别、存储引擎 —— 那是 10-26 周的内容（见 [00-数据库知识地图](../00-数据库知识地图.md)）。
