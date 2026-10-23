# 01 · Redis 速成（90 分钟 · 只学考点要的）

> **为什么必须学**：考点里 Redis 占一整部分（5 类结构 + Python 操作 + 6 道理解题）。
> **目标**：能对着考点表格，用 Python 写出每个操作的代码并验证结果。
> 配套可运行代码 → [redis_demo.py](redis_demo.py)（每类结构跑一遍，改参数再跑）

---

## 一、Redis 是什么（一句话）

**内存里的 Key-Value 数据库**，读写极快（微秒级），常用来做**缓存、计数器、排行榜、队列、会话**。
它没有表、没有 SQL，用**命令**操作，key 是字符串，value 有 5 种常用结构。

```python
import redis
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
r.ping()   # True 就代表连上了
```

> `decode_responses=True` 很重要：不加的话 `get` 返回 `b'123'`（bytes），加了返回 `'123'`（str）。

---

## 二、5 类结构速查（考试只用这张表）

### 1. String 字符串

| 操作 | Redis 命令 | Python（redis-py） |
|---|---|---|
| 写 | `SET k v` | `r.set("k", "v")` |
| 带过期写 | `SET k v EX 300` | `r.set("k", "v", ex=300)` |
| 读 | `GET k` | `r.get("k")` |
| 批量写/读 | `MSET` / `MGET` | `r.mset({"a":"1","b":"2"})` / `r.mget("a","b")` |
| 自增/自减 | `INCR` / `DECR` | `r.incr("cnt")` / `r.decr("cnt")` |
| **不存在才写** | `SET k v NX EX 10` | `r.set("k", "v", nx=True, ex=10)` |
| 过期/剩余时间 | `EXPIRE` / `TTL` | `r.expire("k", 60)` / `r.ttl("k")` |

**考试对应题**：保存验证码并设置有效期 → `r.set(key, code, ex=300)`；统计课程访问次数 → `r.incr(key)`。

### 2. Hash 哈希（一个 key 存多个字段，像一行记录）

| 操作 | Redis 命令 | Python |
|---|---|---|
| 批量写字段 | `HSET k f1 v1 f2 v2` | `r.hset("k", mapping={"name":"张三","phone":"138"})` |
| 读一个字段 | `HGET k f` | `r.hget("k", "name")` |
| 读全部 | `HGETALL k` | `r.hgetall("k")` → **dict** |
| 删字段 | `HDEL k f` | `r.hdel("k", "phone")` |
| 字段是否存在 | `HEXISTS k f` | `r.hexists("k", "name")` |
| 字段加数字 | `HINCRBY k f 2` | `r.hincrby("k", "hours", 2)` |

**考试对应题**：保存学员资料、改手机号、加学习时长、删字段 —— 全用 Hash。

### 3. List 列表（有序、可重复）

| 操作 | Redis 命令 | Python |
|---|---|---|
| 左/右进 | `LPUSH` / `RPUSH` | `r.lpush("q", "a")` / `r.rpush("q", "b")` |
| 左/右出 | `LPOP` / `RPOP` | `r.lpop("q")` / `r.rpop("q")` |
| 范围读 | `LRANGE q 0 -1` | `r.lrange("q", 0, -1)` |
| 长度 | `LLEN q` | `r.llen("q")` |
| 改某个位置 | `LSET q 0 x` | `r.lset("q", 0, "x")` |
| 删元素 | `LREM q 1 val` | `r.lrem("q", 1, "val")` |
| **只保留区间** | `LTRIM q 0 9` | `r.ltrim("q", 0, 9)` |

**考试对应题**：先进先出任务队列（`RPUSH` 进 + `LPOP` 出）；只保留最近 10 条记录（`LTRIM 0 9`）。

> 注意 `lpush` 多个值时：`lpush("q","a","b")` 结果是 `["b","a"]`（每个都插到最左边）。

### 4. Set 集合（无序、**自动去重**）

| 操作 | Redis 命令 | Python |
|---|---|---|
| 加成员 | `SADD k a b` | `r.sadd("k", "a", "b")` |
| 全部成员 | `SMEMBERS k` | `r.smembers("k")` |
| 是否成员 | `SISMEMBER k a` | `r.sismember("k", "a")` |
| 删成员 | `SREM k a` | `r.srem("k", "a")` |
| 人数 | `SCARD k` | `r.scard("k")` |
| 交集/并集/差集 | `SINTER` `SUNION` `SDIFF` | `r.sinter("a","b")` / `r.sunion(...)` / `r.sdiff(...)` |

**考试对应题**：统计课程报名人数（`SCARD`）；查询同时报名两门课的学员（`SINTER`）。

### 5. Sorted Set 有序集合（排行榜专用）

| 操作 | Redis 命令 | Python |
|---|---|---|
| 加成员+分数 | `ZADD k 85 张三` | `r.zadd("k", {"张三": 85})` |
| 查分数 | `ZSCORE k 张三` | `r.zscore("k", "张三")` |
| 加分 | `ZINCRBY k 5 张三` | `r.zincrby("k", 5, "张三")` |
| 按分数升序 | `ZRANGE k 0 -1 WITHSCORES` | `r.zrange("k", 0, -1, withscores=True)` |
| **降序（取前 N）** | `ZREVRANGE k 0 2 WITHSCORES` | `r.zrevrange("k", 0, 2, withscores=True)` |
| **排名** | `ZREVRANK k 张三` | `r.zrevrank("k", "张三")` → **从 0 开始** |
| 删 | `ZREM k 张三` | `r.zrem("k", "张三")` |

**考试对应题**：成绩排行榜、查前三名（`zrevrange 0 2`）、查指定学员排名（`zrevrank` → **+1 才是名次**）。

### 6. Pipeline（考点理解题会问）

```python
pipe = r.pipeline(transaction=True)   # True = MULTI/EXEC 事务
pipe.set("k1", "v1")
pipe.incr("cnt")
result = pipe.execute()               # 一次性发出去，返回结果列表
```

---

## 三、6 道理解题（考点原文，先自己答再看）

### 1. String 与 Hash：保存学员资料时，各适合什么场景？

> **答**：整条数据是一个整体、只读写整块 → String（存 JSON 字符串）；
> 需要**单独读写/增减某个字段**（改手机号、加学习时长）→ Hash，不必读出整条再写回。

### 2. List 与 Set：哪个允许重复？哪个保留顺序？

> **答**：List 允许重复、**保留顺序**（按插入位置）；Set **不允许重复**、无序。

### 3. Set 与 Sorted Set：成绩排行榜为什么适合有序集合？

> **答**：Sorted Set 每个成员带一个**分数**，内部按分数排好序，取前 N / 查排名都是 O(logN)；
> 普通 Set 无序，查排名要全取出再排序。

### 4. 排行榜：Redis 返回的排名从几开始？如何转换为界面显示的名次？

> **答**：`zrevrank` 返回从 **0** 开始，**+1** 就是界面名次（第 1 名）。

### 5. Pipeline 与事务：批量发送命令与事务执行有什么区别？

> **答**：Pipeline 是**减少网络往返**（一次发多条，性能优化），不保证原子性；
> Redis 事务（`MULTI/EXEC`）保证**命令按顺序执行、中间不被插队**（但它没有回滚，某条失败其他仍执行）。
> `pipeline(transaction=True)` 两者兼有。

### 6. 原子性：Python 中先 GET 再 SET 实现计数，会有什么并发问题？

> **答**：两个客户端可能同时 GET 到 9，都 SET 成 10，结果少加一次（丢失更新）。
> 用法：直接用 Redis 的 **`INCR`**（单命令原子），或事务/Lua 脚本。

---

## 四、90 分钟怎么练（照做）

| 分钟 | 做什么 |
|---:|---|
| 0–10 | 起 Redis + 跑通 `redis_demo.py`（看到"全部示例跑通"） |
| 10–30 | 读第二节 5 类结构表，边读边在 demo 里改参数重跑 |
| 30–60 | 照着考点表格，**不看 demo** 自己写一遍 5 类结构的常用操作（每类 3~4 条） |
| 60–80 | 答第三节 6 道理解题（口述） |
| 80–90 | 看 [速查卡](速查卡.md) 的 Redis 部分，抄一遍命令 |

## 五、自检（能全做到就算过关）

- [ ] 能连 Redis（`ping()` → True）
- [ ] String：写带过期验证码、`incr` 计数、`set nx` 条件写
- [ ] Hash：批量写、读单个、读全部、改字段、字段计数
- [ ] List：队列进出、`ltrim` 只保留 N 条
- [ ] Set：去重、`sismember`、交集
- [ ] ZSet：`zadd`、`zincrby`、`zrevrange` 取前三、`zrevrank` 排名
- [ ] 6 道理解题能口述（尤其第 4、6 题）
