# FastAPI × Redis · 最小集（2 小时）

> ⏸️ **10-28 起暂停 / 降级为"了解即可"**。上岗前你只需要 **3 件事**：
> ① 用**同步** redis-py 跑通 `set / get / hset / hgetall / incr`（5 行）
> ② 看懂"缓存三步"：读缓存 → 未命中查库 → 写回 + TTL
> ③ 在 FastAPI 里**调用现成封装**（抄脚手架的 get_cache / set_cache）
>
> **异步客户端 / lifespan 连接池 / 限流 → 11-09 之后再学。**
> 减负说明见 [notes/13 第五节](../../../notes/13-现实评估与减负版计划.md)。

> **目标**：能在 FastAPI 里用 Redis 做**接口缓存 / 更新后删缓存 / 限流**，并知道连接池放在哪。
> 讲解：[01-讲解-Redis在FastAPI中的最小集.md](01-讲解-Redis在FastAPI中的最小集.md)
> 代码：[cache_app.py](cache_app.py)（完整可运行）｜ 自检：[check_cache.py](check_cache.py)（**14/14 已验证**）

## 为什么是"最小集"，不是"完整 Redis 课"

| 已学（10-23 速成） | 今天补 |
|---|---|
| 5 类数据结构 + 命令 | **异步客户端** `redis.asyncio` + `await` |
| Cache-Aside 理论 | 在 FastAPI 里落地：lifespan 连接池 + `Depends` 注入 + JSON + TTL |
| `INCR` 原子计数 | 限流实现（`INCR` + `EXPIRE`） |
| — | 缓存降级（Redis 挂了接口不能挂）、key 命名约定 |

> 完整 Redis（穿透/击穿/雪崩、分布式锁、集群、持久化）等你真正在项目里遇到再补，现在学多了记不住。

## 跑起来

### 有真 Redis

```powershell
docker run -d --name exam-redis -p 6379:6379 redis:7
docker exec -it exam-redis redis-cli ping

cd D:\Program\Python\python-learning\exercises\stage3\fastapi\day02-redis
..\..\..\..\.venv\Scripts\python.exe -m uvicorn cache_app:app --reload
# /docs 里调：GET /students/1 两次、PUT 后 GET、GET /limited 六次
```

### 没有 Redis（fakeredis 兜底）

```powershell
$env:USE_FAKE_REDIS="1"
..\..\..\..\.venv\Scripts\python.exe check_cache.py     # 14 项自检
```

## 自检覆盖

首次查库 → 二次命中缓存 → 命中率统计 → 更新后删缓存（下次又查库）→ 白名单字段拦截 → 404 → 限流 5 次后 429 → 手动删缓存后重建。

## 验收标准

- [ ] `check_cache.py` **14/14**（有/无 Redis 都行）
- [ ] 能说清：为什么用 `redis.asyncio` 而不是同步客户端
- [ ] 能说清：为什么连接池放 `lifespan` 里，而不是每个请求 `from_url`
- [ ] 能说清：为什么更新时"删缓存"而不是"改缓存"
- [ ] 能说清：`ensure_ascii=False` 解决什么
- [ ] 能默写限流那 5 行（INCR + 首次 EXPIRE + 判断）
- [ ] 能说清：Redis 挂了接口为什么不挂（降级）
