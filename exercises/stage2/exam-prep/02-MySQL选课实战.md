# 02 · MySQL 选课场景实战（90 分钟，按考点刷）

> **考点原文**：用统一的"学员选课"场景，四张表：`students` / `courses` / `enrollments` / `accounts`。
> 建库：[schema.sql](schema.sql)（9 学员 / 4 课程 / 14 报名 / 8 账户）
> **做法**：每题直接在 DBX 里写，写完对照"参考写法"。今天不追求全做完，**追求把每类题型的模板记住**。

---

## 一、四张表的关系（先看懂再写 SQL）

```text
students(学员) 1 ─── N enrollments(报名) N ─── 1 courses(课程)
    │
    └── 1 accounts(账户，一人一个，余额)

唯一约束：students.phone 唯一；enrollments (student_id, course_id) 联合唯一
NULL 规则：enrollments.score 为 NULL 表示"未出成绩"
金额：courses.price / accounts.balance 都是 DECIMAL(10,2)
逻辑删除：students.is_deleted = 1 表示已删（查询要排除）
```

---

## 二、增 · INSERT（考点 6 种）

### 1. 单条插入

```sql
INSERT INTO students (name, age, phone, city) VALUES ('郑十一', 22, '13800000009', '杭州');
```

### 2. 批量插入

```sql
INSERT INTO students (name, age, phone, city) VALUES
    ('甲', 20, '13800000010', '北京'),
    ('乙', 21, '13800000011', '上海'),
    ('丙', 22, '13800000012', '广州');
```

### 3. 默认值 + 自增主键（插入后拿生成的主键）

```sql
INSERT INTO courses (name, price) VALUES ('Docker实战', 299.00);
SELECT LAST_INSERT_ID();          -- 拿到刚生成的主键 id
```

Python 里：`cur.lastrowid`（插入后立即读）。

### 4. 唯一约束 + 捕获错误回滚

```sql
-- 重复手机号会报错：Duplicate entry '13800000001' for key 'students.phone'
INSERT INTO students (name, age, phone, city) VALUES ('重复的人', 20, '13800000001', '北京');
```

Python 写法（**考点必考**）：

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="123456",
                       database="school", charset="utf8mb4", autocommit=False)
try:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO students (name, age, phone, city) VALUES (%s, %s, %s, %s)",
            ("重复的人", 20, "13800000001", "北京"),
        )
    conn.commit()
except pymysql.err.IntegrityError as e:
    conn.rollback()
    print("唯一约束冲突，已回滚：", e)
finally:
    conn.close()
```

### 5. 插入查询结果（INSERT ... SELECT）

```sql
-- 先建归档表
CREATE TABLE students_archive LIKE students;

-- 把北京且年龄 >= 20 的学员归档（跳过 id 和 created_at 的默认值问题）
INSERT INTO students_archive (id, name, age, phone, city, is_deleted)
SELECT id, name, age, phone, city, is_deleted
FROM students
WHERE city = '北京' AND age >= 20;
```

### 6. 冲突处理（upsert）

```sql
-- 已存在就更新，不存在就插入（MySQL 特有）
INSERT INTO enrollments (student_id, course_id, score, status)
VALUES (2, 3, 75, 1)
ON DUPLICATE KEY UPDATE score = VALUES(score), status = VALUES(status);
```

---

## 三、查 · SELECT（考点 13 层，重点在后 6 层）

| # | 任务 | 参考写法 |
|---|---|---|
| 1 | 查学员姓名和城市 | `SELECT name, city FROM students;` |
| 2 | 列出不重复城市 | `SELECT DISTINCT city FROM students;` |
| 3 | 查北京且年龄 >= 20 的学员 | `WHERE city='北京' AND age>=20` |
| 4 | 年龄区间 + 指定城市 | `WHERE age BETWEEN 19 AND 22 AND city IN ('北京','上海')` |
| 5 | 姓"张"的学员 | `WHERE name LIKE '张%'` |
| 6 | 未出成绩的报名 | `WHERE score IS NULL` |
| 7 | 按报名时间倒序分页，时间相同按主键排序 | `ORDER BY created_at DESC, id DESC LIMIT 0, 5` |
| 8 | 统计每门课报名数、平均分、最高分 | `SELECT course_id, COUNT(*), ROUND(AVG(score),2), MAX(score) FROM enrollments GROUP BY course_id` |
| 9 | 报名人数 > 2 的课程 | `GROUP BY course_id HAVING COUNT(*) > 2` |
| 10 | 内连接：学员姓名 + 课程名 + 成绩 | `FROM students s JOIN enrollments e ON e.student_id=s.id JOIN courses c ON c.id=e.course_id` |
| 11 | 外连接：所有学员（含未报名） | `FROM students s LEFT JOIN enrollments e ON ...` |
| 12 | 高于**该课程平均分**的学员 | 子查询（见下） |
| 13 | 从未报名课程的学员 | `WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id)` |
| 14 | 成绩转优秀/及格/不及格 | `CASE WHEN score >= 85 THEN '优秀' WHEN score >= 60 THEN '及格' ELSE '不及格' END` |

**12 的参考写法**：

```sql
SELECT s.name, c.name AS course_name, e.score
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses c  ON c.id = e.course_id
WHERE e.score > (
    SELECT AVG(e2.score) FROM enrollments e2 WHERE e2.course_id = e.course_id
);
```

**13 的参考写法**：

```sql
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id);
```

**加分（CTE / 窗口函数，时间不够跳过）**：

```sql
-- 每门课成绩前三名（窗口函数）
SELECT course_id, student_id, score, rn FROM (
    SELECT course_id, student_id, score,
           ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY score DESC) AS rn
    FROM enrollments WHERE score IS NOT NULL
) t WHERE rn <= 3;

-- CTE
WITH course_avg AS (
    SELECT course_id, AVG(score) AS avg_score
    FROM enrollments WHERE score IS NOT NULL GROUP BY course_id
)
SELECT c.name, ROUND(ca.avg_score, 2) AS avg_score
FROM course_avg ca JOIN courses c ON c.id = ca.course_id;
```

---

## 四、改 · UPDATE（考点 6 种，重点：WHERE + 事务 + 判断影响行数）

```sql
-- 1. 单字段：改手机号
UPDATE students SET phone = '13900000001' WHERE id = 1;

-- 2. 多字段：同时改城市和年龄
UPDATE students SET city = '杭州', age = 21 WHERE id = 1;

-- 3. 条件批量：指定课程的待审核 → 已通过
UPDATE enrollments SET status = 1 WHERE course_id = 1 AND status = 0;

-- 4. 表达式：课程价格 +10%
UPDATE courses SET price = price * 1.1 WHERE id = 1;

-- 5. 条件扣减（余额足够才扣，并检查影响行数）
UPDATE accounts SET balance = balance - 299
WHERE student_id = 1 AND balance >= 299;
-- 然后看 ROW_COUNT()（Python 里 cur.rowcount）是否为 1 → 1 表示扣成功

-- 6. 多表关联更新（进阶）
UPDATE enrollments e
JOIN courses c ON c.id = e.course_id
SET e.status = 1
WHERE c.name = 'Python入门' AND e.status = 0;
```

**Python 判断影响行数（考点明确要求）**：

```python
with conn.cursor() as cur:
    cur.execute("UPDATE accounts SET balance = balance - %s WHERE student_id = %s AND balance >= %s",
                (299, 1, 299))
    if cur.rowcount == 0:
        conn.rollback()
        print("余额不足或用户不存在")
    else:
        conn.commit()
```

---

## 五、删 · DELETE（考点 6 种）

```sql
-- 1. 单条删除
DELETE FROM enrollments WHERE id = 13;

-- 2. 条件批量：删除 2026-01-01 前已取消的报名
DELETE FROM enrollments WHERE status = 2 AND created_at < '2026-01-01';

-- 3. 多条件
DELETE FROM enrollments WHERE course_id = 3 AND status = 2;

-- 4. 关联数据处理（先删子表再删主表，或按外键策略）
DELETE FROM enrollments WHERE student_id = 99;
DELETE FROM accounts WHERE student_id = 99;
DELETE FROM students WHERE id = 99;

-- 5. 逻辑删除（推荐：用状态字段标记，查询时排除）
UPDATE students SET is_deleted = 1 WHERE id = 1;
SELECT * FROM students WHERE is_deleted = 0;     -- 所有查询都要带这个条件

-- 6. 概念辨析：DELETE / TRUNCATE / DROP
-- DELETE：删行，可 WHERE，可回滚（DML）
-- TRUNCATE：清空整表（含自增重置），不能 WHERE，不可回滚（DDL）
-- DROP：连表结构一起删
```

---

## 六、事务 · 报名扣款（**考点说必考一道**）

> **题目**：学员报名课程时，需要扣减账户余额并新增报名记录。
> 余额不足、重复报名或任一步骤失败时，整个操作回滚。

### 参考实现（Python + pymysql）

```python
import pymysql

def enroll(student_id: int, course_id: int) -> bool:
    """报名成功返回 True，失败回滚返回 False。"""
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456",
                           database="school", charset="utf8mb4", autocommit=False)
    try:
        with conn.cursor() as cur:
            # 1. 查课程价格（不存在 → 退出）
            cur.execute("SELECT price FROM courses WHERE id = %s", (course_id,))
            row = cur.fetchone()
            if row is None:
                conn.rollback()
                return False
            price = row[0]

            # 2. 扣余额：带 balance >= price 条件，防止扣成负数
            cur.execute(
                "UPDATE accounts SET balance = balance - %s "
                "WHERE student_id = %s AND balance >= %s",
                (price, student_id, price),
            )
            if cur.rowcount == 0:
                conn.rollback()          # 余额不足
                return False

            # 3. 插报名记录（唯一约束兜底：重复报名会抛 IntegrityError）
            cur.execute(
                "INSERT INTO enrollments (student_id, course_id, status) VALUES (%s, %s, 1)",
                (student_id, course_id),
            )
        conn.commit()
        return True
    except pymysql.err.IntegrityError:
        conn.rollback()                  # 重复报名
        return False
    except Exception:
        conn.rollback()                  # 任何其他错误
        raise
    finally:
        conn.close()                     # 一定释放连接
```

**验收点（对照考点）**：
- [x] 两次写操作在**同一个事务**（同一个 conn，最后统一 commit）
- [x] 扣款带 `balance >= price`，**余额不会为负**
- [x] 重复报名由**唯一约束**兜底（IntegrityError → rollback）
- [x] 失败后余额和报名记录都保持原样
- [x] SQL **参数化**（`%s`），异常后**关闭连接**

---

## 七、90 分钟怎么刷（别全做，按题型刷）

| 分钟 | 做什么 |
|---:|---|
| 0–15 | 建库 + 跑 `schema.sql`，用 SQL 验证 4 张表数据 |
| 15–40 | **查询 14 个层次**里挑 8 个写（重点：聚合/分组过滤/内连接/子查询/CASE） |
| 40–55 | **增** 6 种里挑 4 个（单条、批量、唯一约束、upsert） |
| 55–70 | **改** 4 个（单字段、多字段、表达式、条件扣减 + 看 rowcount） |
| 70–85 | **事务报名扣款**：手写一遍 Python 代码（关掉参考） |
| 85–90 | 看一遍本节，把模板记下来 |

## 自检

- [ ] 能不看资料写出"学员+课程+成绩"的三表 JOIN
- [ ] 能写"高于课程平均分"的相关子查询
- [ ] 能写"从未报名"的 NOT EXISTS
- [ ] 能写 CASE WHEN 转换成绩
- [ ] 能写条件扣减 + 判断 `rowcount`
- [ ] 能默写报名扣款事务（含 IntegrityError 回滚 + finally 关闭）
