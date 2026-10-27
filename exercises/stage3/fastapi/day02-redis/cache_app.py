"""FastAPI + Redis · Cache-Aside 完整示例（可运行）

运行（先起 Redis，见 README）：
    cd exercises/stage3/fastapi/day02-redis
    uvicorn cache_app:app --reload
    http://127.0.0.1:8000/docs

没有 Redis 时（用 fakeredis 模拟，练逻辑足够）：
    $env:USE_FAKE_REDIS="1"; uvicorn cache_app:app --reload
    # 自检也可以用假 Redis：$env:USE_FAKE_REDIS="1"; python check_cache.py
"""

from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import Depends, FastAPI, HTTPException, Request

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CACHE_TTL = 300          # 秒
USE_FAKE = os.getenv("USE_FAKE_REDIS") == "1"

# 模拟数据库
STUDENTS: dict[int, dict] = {
    1: {"id": 1, "name": "张三", "city": "北京", "age": 20},
    2: {"id": 2, "name": "李四", "city": "上海", "age": 22},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """① 启动时建 Redis 连接池（只建一次），关闭时释放。"""
    if USE_FAKE:
        import fakeredis.aioredis
        app.state.redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    else:
        app.state.redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    print(f"[lifespan] Redis 已连接: {USE_FAKE and 'fakeredis' or REDIS_URL}")
    try:
        yield
    finally:
        await app.state.redis.aclose()
        print("[lifespan] Redis 已关闭")


app = FastAPI(title="学生资料 API（带缓存）", lifespan=lifespan)


# ============================================================
# ② 依赖：从 app.state 里取连接池（不是每个请求新建连接）
# ============================================================

def get_redis(request: Request) -> aioredis.Redis:
    return request.app.state.redis


def student_key(student_id: int) -> str:
    return f"student:{student_id}"


# ============================================================
# ③ 读：Cache-Aside（先缓存 → 未命中查库 → 回写缓存）
# ============================================================

@app.get("/students/{student_id}")
async def get_student(
    student_id: int,
    r: aioredis.Redis = Depends(get_redis),
):
    key = student_key(student_id)

    # 1. 先读缓存（Redis 挂掉不应该影响主流程 → try/except 降级）
    try:
        cached = await r.get(key)
    except Exception:
        cached = None

    if cached is not None:
        await r.incr("stats:hit")
        return {"source": "cache", **json.loads(cached)}

    # 2. 未命中 → 查"数据库"
    await r.incr("stats:miss")
    if student_id not in STUDENTS:
        raise HTTPException(status_code=404, detail="Student not found")
    data = STUDENTS[student_id]

    # 3. 回写缓存（中文不转义 + 300 秒过期）
    await r.set(key, json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)
    return {"source": "db", **data}


# ============================================================
# ④ 写：先更新库 → 再删缓存（顺序不能反）
# ============================================================

@app.put("/students/{student_id}")
async def update_student(
    student_id: int,
    payload: dict,
    r: aioredis.Redis = Depends(get_redis),
):
    if student_id not in STUDENTS:
        raise HTTPException(status_code=404, detail="Student not found")

    # 1. 只允许改白名单字段
    allowed = {"name", "city", "age"}
    for k, v in payload.items():
        if k not in allowed:
            raise HTTPException(status_code=400, detail=f"不允许修改字段: {k}")
        STUDENTS[student_id][k] = v

    # 2. 删缓存（让下次读重建）
    await r.delete(student_key(student_id))
    return {"ok": True, "student": STUDENTS[student_id]}


# ============================================================
# ⑤ 限流：INCR + EXPIRE（60 秒内最多 5 次）
# ============================================================

@app.get("/limited")
async def limited(r: aioredis.Redis = Depends(get_redis)):
    key = "ratelimit:demo"
    count = await r.incr(key)          # 单命令原子：不会丢更新
    if count == 1:
        await r.expire(key, 60)        # 第一次设过期，之后不覆盖
    if count > 5:
        raise HTTPException(status_code=429, detail="太频繁了，60 秒后再试")
    return {"count": count, "ttl": await r.ttl(key)}


# ============================================================
# ⑥ 统计（方便自检看命中率）
# ============================================================

@app.get("/stats")
async def stats(r: aioredis.Redis = Depends(get_redis)):
    hit = int(await r.get("stats:hit") or 0)
    miss = int(await r.get("stats:miss") or 0)
    total = hit + miss
    return {
        "hit": hit,
        "miss": miss,
        "hit_rate": round(hit / total, 4) if total else 0.0,
    }


@app.delete("/cache/{student_id}")
async def drop_cache(student_id: int, r: aioredis.Redis = Depends(get_redis)):
    """调试用：手动删缓存。"""
    await r.delete(student_key(student_id))
    return {"deleted": True}
