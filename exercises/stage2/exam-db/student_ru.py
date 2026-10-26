"""
    题目：实现学员资料查询与更新。

    要求：
    MySQL 保存学员资料。
    查询时先读 Redis，未命中再查询 MySQL。
    将查到的资料写入 Redis，有效期为 300 秒。
    修改资料时，先更新并提交 MySQL，再删除对应缓存。
    不存在的学员返回明确结果。
    正确处理 JSON、中文、数据库异常。
"""

import json
import pymysql
import redis
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "school",
    "charset": "utf8mb4",
    "autocommit": False,
}

REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": "123456",
    "decode_responses": True,
}

CACHE_TTL = 300
ALLOWED_UPDATE_FIELDS = {"name", "age", "phone", "city"}

r = redis.Redis(**REDIS_CONFIG)


def _key(student_id: int) -> str:
    return f"student:{student_id}"


def _to_json_row(row: dict) -> dict:
    """JSON 可序列化 dict"""
    out = {}
    for k, v in row.items():
        out[k] = v.isoformat(sep=" ") if isinstance(v, datetime) else v
    return out


def get_student(student_id: int) -> dict | None:
    """
    先读 Redis；未命中查 MySQL 
    """
    key = _key(student_id)

    # 读缓存
    try:
        cached = r.get(key)
        if cached is not None:
            return json.loads(cached)
    except redis.RedisError as e:
        print(f"[warn] Redis 读取失败，降级查库: {e}")

    # 未命中查 MySQL
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(
                "SELECT id, name, age, phone, city, created_at "
                "FROM students WHERE id = %s",
                (student_id,),
            )
            row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    # 回填缓存
    data = _to_json_row(row)
    try:
        r.set(key, json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)
    except redis.RedisError as e:
        print(f"[warn] Redis 回填失败，忽略: {e}")

    return data


def update_student(student_id: int, updates: dict) -> bool:
    """
    先更新 MySQL 并提交，再删除缓存。
    """
    if not updates:
        raise ValueError("updates 不能为空")
    invalid = set(updates) - ALLOWED_UPDATE_FIELDS
    if invalid:
        raise ValueError(f"不允许更新字段: {invalid}")

    # 更新 MySQL
    set_clause = ", ".join(f"`{k}` = %s" for k in updates)
    values = list(updates.values()) + [student_id]

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE students SET {set_clause} WHERE id = %s",
                values,
            )
            affected = cur.rowcount
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    # 提交成功后再删缓存
    try:
        r.delete(_key(student_id))
    except redis.RedisError as e:
        print(f"Redis 删除失败，等待 TTL 自然过期: {e}")

    return affected > 0