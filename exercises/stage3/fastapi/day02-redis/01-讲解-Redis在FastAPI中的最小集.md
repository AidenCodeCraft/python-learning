# 01 · Redis 在 FastAPI 里怎么用（最小集 · 2 小时）

> **为什么学**：公司 FastAPI 项目几乎必配 Redis —— 缓存接口结果、限流、验证码、登录态、队列。
> 你在 10-23 已经速成过 Redis 的 5 类数据结构；今天学的是**在 FastAPI 里怎么用它**。
> 可运行代码：[cache_app.py](cache_app.py) ｜ 自检：[check_cache.py](check_cache.py)（14 项，已跑通）

---

## 一、先分清：同步客户端 vs 异步客户端

| | 同步（`redis.Redis`） | **异步（`redis.asyncio.Redis`）** |
|---|---|---|
| 导入 | `import redis` | `import redis.asyncio as aioredis` |
| 调用 | `r.get("k")` | `await r.get("k")` |
| 用在 | 普通脚本、命令行工具 | **FastAPI（异步框架）** |

**FastAPI 里用异步客户端**：否则每个 Redis 操作都会阻塞事件循环（高并发时性能崩）。

```python
import redis.asyncio as aioredis
r = aioredis.from_url("redis://127.0.0.1:6379/0", decode_responses=True)
await r.set("k", "v")
```

> 我们的 `exam-prep` 里那些命令（String/Hash/List/Set/ZSet）**完全一样**，只是前面加 `await`。

---

## 二、连接池：只在启动时建一次（lifespan）

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = aioredis.from_url(REDIS_URL, decode_responses=True)  # 建连接池
    try:
        yield
    finally:
        await app.state.redis.aclose()      # 关闭
```

**为什么**：
- `from_url` 内部维护**连接池**，多个请求复用连接
- 每个请求新建连接 → 慢 + 连接数爆炸
- 关闭时优雅释放

> 这和 Day2 学的 lifespan 是同一个知识点 —— 现在你知道它为什么重要了。

---

## 三、依赖：每个接口怎么拿到 Redis

```python
from fastapi import Depends, Request

def get_redis(request: Request) -> aioredis.Redis:
    return request.app.state.redis

@app.get("/students/{student_id}")
async def get_student(student_id: int, r: aioredis.Redis = Depends(get_redis)):
    ...
```

- `request.app.state` = 整个应用共享的存储（lifespan 里放的东西）
- 用 `Depends` 注入，接口签名干净
- 测试时可以替换成 fakeredis（见自检脚本）

---

## 四、核心场景 1：缓存接口结果（Cache-Aside）

```python
CACHE_TTL = 300

@app.get("/students/{student_id}")
async def get_student(student_id: int, r: aioredis.Redis = Depends(get_redis)):
    key = f"student:{student_id}"

    # ① 先读缓存（Redis 挂了要降级，不能让接口 500）
    try:
        cached = await r.get(key)
    except Exception:
        cached = None
    if cached is not None:
        await r.incr("stats:hit")
        return {"source": "cache", **json.loads(cached)}

    # ② 未命中 → 查数据库
    await r.incr("stats:miss")
    if student_id not in STUDENTS:
        raise HTTPException(status_code=404, detail="Student not found")
    data = STUDENTS[student_id]

    # ③ 回写缓存：JSON 字符串 + 中文不转义 + 300 秒过期
    await r.set(key, json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)
    return {"source": "db", **data}
```

### 三个容易错的细节

| 细节 | 为什么 |
|---|---|
| `json.dumps(data, ensure_ascii=False)` | 不加的话中文变 `\u5f20\u4e09`，虽然能反序列化回来，但缓存里人看不懂、也占空间 |
| `ex=CACHE_TTL` | 不给过期 → 数据永远脏在缓存里 |
| `try/except` 包住缓存读 | **Redis 挂了不能让业务接口挂**（降级为查库） |

---

## 五、核心场景 2：更新时删缓存（不是改缓存）

```python
@app.put("/students/{student_id}")
async def update_student(student_id: int, payload: dict,
                         r: aioredis.Redis = Depends(get_redis)):
    # ① 先更新数据库并"提交"
    STUDENTS[student_id].update(...)

    # ② 再删缓存（让下次读从库重建）
    await r.delete(f"student:{student_id}")
```

**为什么删而不是改**：
- 改缓存要读旧值→改→写回，中间可能被并发请求写脏
- 删了之后下次读会按最新库数据重建 → 简单、不容易错
- 代价：下一次读会"穿透"到库（可以接受）

> 更严格的一致性（延迟双删、版本号）是进阶话题，知道"Cache-Aside = 最终一致"就够了。

---

## 六、核心场景 3：限流 / 计数（INCR 是原子的）

```python
@app.get("/limited")
async def limited(r: aioredis.Redis = Depends(get_redis)):
    key = "ratelimit:demo"
    count = await r.incr(key)      # 单命令原子：不会丢更新
    if count == 1:
        await r.expire(key, 60)    # 只在第一次设过期，别每次都设（否则永不过期）
    if count > 5:
        raise HTTPException(status_code=429, detail="太频繁了，60 秒后再试")
    return {"count": count, "ttl": await r.ttl(key)}
```

> 这就是考试理解题"先 GET 再 SET 会丢更新"的答案：用 `INCR` 一次搞定。
> 再往上就是 `zset` 滑动窗口限流、Redis 分布式锁（后面用到再说）。

---

## 七、key 命名与序列化约定（公司规范一般这么定）

| 约定 | 例子 |
|---|---|
| `业务:对象:id` | `student:1`、`order:20261027001` |
| 缓存统一前缀，方便批量清理 | `cache:student:1` |
| 值统一存 JSON 字符串 | `{"id":1,"name":"张三"}` |
| 一定要有 TTL（除少数持久计数字） | `ex=300` |
| 统计类 key 分开 | `stats:hit`、`stats:miss` |

---

## 八、跑起来（两种模式）

### 模式 A：真 Redis（推荐，顺便验证 10-23 学的命令）

```powershell
# 1. 启动 Docker Desktop，然后：
docker run -d --name exam-redis -p 6379:6379 redis:7
docker exec -it exam-redis redis-cli ping        # PONG

# 2. 启动服务
cd D:\Program\Python\python-learning\exercises\stage3\fastapi\day02-redis
..\..\..\..\.venv\Scripts\python.exe -m uvicorn cache_app:app --reload

# 3. 浏览器调：
#    GET  /students/1   两次 → 第一次 source=db，第二次 source=cache
#    PUT  /students/1   {"city":"杭州"} → 再 GET 又变 source=db
#    GET  /stats        看命中率
#    GET  /limited      连点 6 次 → 第 6 次 429
```

也可以用 `redis-cli` 直接看：
```powershell
docker exec -it exam-redis redis-cli KEYS "student:*"
docker exec -it exam-redis redis-cli TTL student:1
```

### 模式 B：没有 Redis（fakeredis 模拟）

```powershell
$env:USE_FAKE_REDIS="1"
..\..\..\..\.venv\Scripts\python.exe -m uvicorn cache_app:app --reload
# 或直接跑自检
..\..\..\..\.venv\Scripts\python.exe check_cache.py
```

> `fakeredis` 在内存里模拟 Redis，命令行为一样，适合练逻辑。**但考试/工作要连真 Redis。**

---

## 九、自检（14 项 · 我跑过 14/14）

```powershell
cd exercises\stage3\fastapi\day02-redis
$env:USE_FAKE_REDIS="1"; python check_cache.py
```

覆盖：首次查库 → 二次命中 → 命中率统计 → 更新后删缓存 → 白名单字段 → 404 → 限流 5 次后 429 → 手动删缓存后重建。

---

## 十、小练习（自己加，30 分钟）

1. **给列表接口加缓存**：新增 `GET /students`，缓存整个列表 `students:all`，TTL 60 秒。
2. **加一个版本号**：每次更新学生后 `INCR "students:version"`，`/stats` 返回版本号。
3. **限流改成"每 60 秒 10 次"**，并让 key 按路径区分（`ratelimit:{path}`），这样不同接口互不影响。
4. **（进阶）验证码接口**：`POST /sms-code` 生成 6 位数字，`r.set(f"sms:{phone}", code, ex=300)`；`POST /verify` 校验，通过后删 key。

---

## 十一、和已学内容的连接

| 已学 | 在这里用在哪 |
|---|---|
| Redis 5 类结构（10-23 速成） | String 做缓存/计数；ZSet 做排行榜；Set 做去重 |
| Day2 依赖注入 | `Depends(get_redis)` 拿客户端 |
| Day2 lifespan | 启动时建连接池、关闭时释放 |
| Cache-Aside（考试综合题） | 今天这套代码就是那道题的工程版 |
| SQL 参数化/事务 | 缓存后面的"数据库"部分，真实项目换成 SQLAlchemy Session |

---

## 十二、常见报错

| 报错 | 原因 | 解决 |
|---|---|---|
| `redis.exceptions.ConnectionError` | Redis 没起 / 端口不对 | `docker ps`、`ping` |
| `TypeError: object dict can't be used in 'await' expression` | 用了同步客户端还 `await` | 用 `redis.asyncio` |
| `coroutine was never awaited` | 忘了 `await` | 每个命令都 `await` |
| 返回 `b'...'` | 没设 `decode_responses=True` | `from_url(..., decode_responses=True)` |
| 缓存永远不失效 | `expire` 在每个请求都重置 | 只在 `count == 1` 时设 |
| 中文变 `\u5f20` | `ensure_ascii=True`（默认） | `json.dumps(..., ensure_ascii=False)` |
| Redis 挂了接口全 500 | 没做降级 | 缓存读写包 `try/except` |
