# Python 中使用 SQL · 路线与计划（2026-10-22 提前启动）

> **触发**：考试不正规（可上网查）→ 不再为考试刷题，**把"Python 中使用 SQL"提前到今天（10-22）**。
> 这是阶段 2 的核心工程能力，也是阶段 3/4（FastAPI + SQLAlchemy）的地基。
>
> 排期依据 → [06-排期重排](../../../notes/06-排期重排-工作日9h与SQL考试.md) ·
> 四层路线 → [07-Python中使用SQL-路线图](../../../notes/07-Python中使用SQL-路线图.md)

---

## 一、三天路线（全部可运行、用真实练习库）

| Day | 日期 | 内容 | 教材 | 产出 |
|---|---|---|---|---|
| **Day 1** | **10-22 今天** | **DB-API 基础**：连接→游标→执行→取结果→关闭；`fetchone/fetchall`；结果转 dict / 转对象；`try/finally` 关连接 | [day01-dbapi.md](day01-dbapi.md) | [day01.py](day01.py) 8 题 |
| **Day 2** | **10-22 今天** | **参数化与 SQL 注入**：拼接 vs 占位符；亲手演示注入 `' OR '1'='1`；`executemany`；LIKE 参数；列名白名单 | [day02-parameterized.md](day02-parameterized.md) | [day02.py](day02.py) 8 题 |
| **Day 3** | **10-23 明天（考后）** | **事务与连接管理 + pymysql 实战**：commit/rollback/异常；连接池概念；装 `pymysql` 连公司 MySQL 跑同一批查询 | Day3 教材（明天出） | 用 pymysql 重写 Day1/2 的查询 |

> 数据库安排：Day1/2 用 **sqlite3**（Python 自带，0 安装）把"代码里用 SQL"练熟；
> Day3 切 **pymysql + MySQL**（同一套 DB-API，只换连接参数和占位符 `?` → `%s`）。

---

## 二、新排期（考试不再占时间）

| 日期 | 内容 |
|---|---|
| **10-22 四（今天下午+晚上）** | Python+SQL Day1 + Day2（约 5h）+ 模拟卷 Part C 收尾（20min） |
| **10-23 五（考试 + 下午）** | 上午考试 → 下午 Python+SQL **Day3（事务 + pymysql 连 MySQL）** |
| 10-24 / 10-25 | 周末不可用 |
| **10-26 一 ~ 10-30 五** | ① Redis 五种结构 + 缓存场景（8h）② SQL 工程层：索引/EXPLAIN/事务隔离/表设计（10h）③ 基础篇④造（书签管理器）+ **阶段 1 正式验收**（10h）④ pymysql 综合小项目（把 todo_cli 改成数据库版，8h）⑤ 缓冲（9h） |
| **11-02 一 ~ 11-06 五** | 阶段 3 FastAPI（20h）+ 阶段 4 SQLAlchemy/Alembic/分层/JWT/Docker（15h）+ 阶段 5 需求模拟（8h）+ 缓冲 |
| **11-09 一** | 开始承接公司简单需求 |

---

## 三、今天从哪开始

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
cd exercises\stage2\python-sql
python day01.py        # 一开始全是 False（骨架），逐题填
```

**步骤**：
1. 读 [day01-dbapi.md](day01-dbapi.md) 第一节（DB-API 五步 + 对照表），约 20 分钟
2. 做 day01.py 的 8 题（约 1.5h）→ 全部"对上了吗: True"
3. 读 [day02-parameterized.md](day02-parameterized.md)，做 day02.py 的 8 题（约 1.5h）
4. 每做完一天，把输出发我

---

## 四、三个"必须亲手做"的实验（都是重点）

1. **注入演示**（Day2 ex02/ex03）：同一串 `' OR '1'='1`，拼接版返回 **12 行**，参数化版返回 **0 行** —— 亲眼看到才记得住。
2. **连接关闭**（Day1 ex08）：故意执行错误 SQL，`finally` 里关连接。
3. **回滚实验**（Day2 ex08）：插入 3 条 → rollback → 查出来是 0 条。

---

## 五、验收标准（三天全过）

- [ ] DB-API 五步能默写
- [ ] 能说清 `?`（sqlite3）与 `%s`（pymysql）的区别
- [ ] 所有 SQL 都是**参数化**的（代码里搜不到 `f"...{变量}..."` 拼 SQL）
- [ ] 能用 `row_factory` / `DictCursor` 把结果转 dict，再转对象
- [ ] 能写 `executemany` 批量插入
- [ ] 能写"转账式"事务：异常 → rollback；成功 → commit
- [ ] 能用 pymysql 连 MySQL 跑通 Day1 的 8 个查询
