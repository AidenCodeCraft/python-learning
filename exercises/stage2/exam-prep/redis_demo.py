"""Redis 5 类数据结构 · 可运行示例（考试速成）

前置：本机 Redis 已起（容器 exam-redis，端口 6380；6379 被 ai-diagnostic 占用，
      详见 00-环境准备.md），已 pip install redis
运行：
    cd exercises/stage2/exam-prep
    python redis_demo.py

设计：每类结构 ① 写数据 ② 读数据 ③ 验证（print 出来），
照着考试要求改 key/值即可。
"""

from __future__ import annotations

import sys

import redis

# Windows PowerShell 默认 GBK：把不能编码的字符替换掉，避免 print 时 UnicodeEncodeError
try:
    sys.stdout.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass

r = redis.Redis(host="127.0.0.1", port=6380, db=0, decode_responses=True)


def demo_string() -> None:
    """String：验证码、计数器、SET NX EX"""
    print("\n=== 1. String ===")
    # ① 读写 + 过期
    r.set("code:13800000000", "123456", ex=300)      # ex=300 秒后自动删除
    print("验证码:", r.get("code:13800000000"), "| 剩余秒数:", r.ttl("code:13800000000"))

    # ② 批量读写
    r.mset({"user:1:name": "张三", "user:2:name": "李四"})
    print("批量:", r.mget("user:1:name", "user:2:name"))

    # ③ 计数（原子操作）
    r.delete("course:1:visits")
    print("访问次数:", r.incr("course:1:visits"), r.incr("course:1:visits"), r.incr("course:1:visits"))

    # ④ 条件写入：只有不存在才写（分布式锁/防重复提交）
    first = r.set("lock:course:1", "1", nx=True, ex=10)
    second = r.set("lock:course:1", "1", nx=True, ex=10)
    print("第一次加锁:", first, "| 第二次加锁:", second, "（None 表示已被占用）")


def demo_hash() -> None:
    """Hash：保存学员资料、字段增减"""
    print("\n=== 2. Hash ===")
    key = "student:100"
    r.delete(key)
    r.hset(key, mapping={"name": "张三", "phone": "13800000000", "hours": 0})
    print("全部字段:", r.hgetall(key))          # dict
    print("单个字段:", r.hget(key, "name"))

    r.hset(key, "phone", "13911111111")          # 改手机号
    print("改手机号后:", r.hget(key, "phone"))

    r.hincrby(key, "hours", 2)                   # 学习时长 +2
    r.hincrby(key, "hours", 3)
    print("学习时长:", r.hget(key, "hours"))

    r.hdel(key, "hours")                         # 删字段
    print("删 hours 后:", r.hgetall(key), "| 存在 name?", r.hexists(key, "name"))


def demo_list() -> None:
    """List：任务队列（先进先出）、只保留最近 N 条"""
    print("\n=== 3. List ===")
    key = "queue:task"
    r.delete(key)
    r.rpush(key, "任务A", "任务B", "任务C")       # 右边进（队尾）
    print("队列:", r.lrange(key, 0, -1), "| 长度:", r.llen(key))
    print("出队（左边出，先进先出）:", r.lpop(key))  # 任务A
    print("剩余:", r.lrange(key, 0, -1))

    # 只保留最近 10 条学习记录
    recent = "recent:study"
    r.delete(recent)
    for i in range(15):
        r.lpush(recent, f"记录{i}")               # 左边进（最新的在左边）
    r.ltrim(recent, 0, 9)                          # 只保留前 10 条（最新的 10 条）
    print("最近记录条数:", r.llen(recent), "| 前 3 条:", r.lrange(recent, 0, 2))


def demo_set() -> None:
    """Set：去重、成员判断、集合运算"""
    print("\n=== 4. Set ===")
    c1, c2 = "course:python:students", "course:mysql:students"
    r.delete(c1, c2)
    r.sadd(c1, "s1", "s2", "s3")
    r.sadd(c2, "s2", "s3", "s4")
    print("Python 课学员:", r.smembers(c1))
    print("MySQL 课学员:", r.smembers(c2), "| 人数:", r.scard(c2))
    print("同时报名两门:", r.sinter(c1, c2))
    print("两门课总人数（去重）:", r.sunion(c1, c2))
    print("只报 Python 没报 MySQL:", r.sdiff(c1, c2))
    print("s1 在 Python 课吗:", r.sismember(c1, "s1"))


def demo_zset() -> None:
    """Sorted Set：排行榜、排名、分数增减"""
    print("\n=== 5. Sorted Set ===")
    key = "rank:score"
    r.delete(key)
    r.zadd(key, {"张三": 85, "李四": 90, "王五": 78})
    print("全部（升序）:", r.zrange(key, 0, -1, withscores=True))
    print("前三名（降序）:", r.zrevrange(key, 0, 2, withscores=True))

    r.zincrby(key, 10, "王五")                     # 王五 +10 → 88
    print("王五加分后:", r.zscore(key, "王五"))

    rank0 = r.zrevrank(key, "张三")                 # 0 开始的名次
    print("张三的排名（0 开始）:", rank0, "→ 界面显示第", rank0 + 1, "名")

    r.zrem(key, "李四")
    print("删李四后:", r.zrevrange(key, 0, -1, withscores=True))


def demo_pipeline() -> None:
    """Pipeline：批量发送命令（减少网络往返）"""
    print("\n=== 6. Pipeline ===")
    pipe = r.pipeline(transaction=True)            # transaction=True = MULTI/EXEC
    pipe.set("pipe:k1", "v1")
    pipe.incr("pipe:cnt")
    pipe.incr("pipe:cnt")
    result = pipe.execute()
    print("管道执行结果:", result, "| cnt =", r.get("pipe:cnt"))


if __name__ == "__main__":
    if not r.ping():
        raise SystemExit("Redis 连不上！先起 Redis（见 00-环境准备.md）")
    print("Redis 连接成功:", r.ping())

    demo_string()
    demo_hash()
    demo_list()
    demo_set()
    demo_zset()
    demo_pipeline()

    # 清理演示数据
    for k in ("code:13800000000", "user:1:name", "user:2:name", "course:1:visits",
              "lock:course:1", "student:100", "queue:task", "recent:study",
              "course:python:students", "course:mysql:students", "rank:score",
              "pipe:k1", "pipe:cnt"):
        r.delete(k)
    print("\n[OK] 全部示例跑通（演示数据已清理）")
