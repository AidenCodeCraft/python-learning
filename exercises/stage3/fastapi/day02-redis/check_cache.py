"""FastAPI + Redis 自检脚本

用法：
    # 有真 Redis：
    cd exercises/stage3/fastapi/day02-redis
    python check_cache.py

    # 没有 Redis（用 fakeredis 模拟，逻辑一样）：
    $env:USE_FAKE_REDIS="1"; python check_cache.py
"""

from __future__ import annotations

import os
import sys

os.environ.setdefault("USE_FAKE_REDIS", "1")  # 默认用假 Redis，保证本机没 Redis 也能跑

from fastapi.testclient import TestClient  # noqa: E402

from cache_app import app  # noqa: E402

results: list[bool] = []


def check(label: str, actual: object, expect: object) -> None:
    ok = actual == expect
    results.append(ok)
    print(f"{label:<30} 实际={actual!r:<40} 预期={expect!r:<40} 对上了吗: {ok}")


def body(r):
    try:
        return r.json()
    except Exception:
        return {}


def main() -> None:
    with TestClient(app) as client:
        # ① 第一次：未命中 → 查库
        r = client.get("/students/1")
        check("第一次读取来源", body(r).get("source"), "db")
        check("返回中文正确", body(r).get("name"), "张三")

        # ② 第二次：命中缓存
        r = client.get("/students/1")
        check("第二次读取来源", body(r).get("source"), "cache")

        # ③ 统计
        r = client.get("/stats")
        check("stats hit", body(r).get("hit"), 1)
        check("stats miss", body(r).get("miss"), 1)

        # ④ 更新后删缓存 → 下次读又是查库
        r = client.put("/students/1", json={"city": "杭州"})
        check("更新成功", body(r).get("ok"), True)
        r = client.get("/students/1")
        check("更新后来源", body(r).get("source"), "db")
        check("更新后城市", body(r).get("city"), "杭州")

        # ⑤ 不允许改的字段
        r = client.put("/students/1", json={"id": 999})
        check("禁止改字段状态码", r.status_code, 400)

        # ⑥ 不存在的学生
        r = client.get("/students/999")
        check("不存在学生状态码", r.status_code, 404)

        # ⑦ 限流：5 次内成功，第 6 次 429
        codes = [client.get("/limited").status_code for _ in range(6)]
        check("限流前 5 次", codes[:5], [200, 200, 200, 200, 200])
        check("第 6 次被限流", codes[5], 429)

        # ⑧ 缓存 TTL
        client.get("/students/2")  # 先把 2 写进缓存
        r = client.delete("/cache/2")
        check("手动删缓存", body(r).get("deleted"), True)
        r = client.get("/students/2")
        check("删缓存后来源", body(r).get("source"), "db")

    ok = sum(results)
    total = len(results)
    print(f"\n{'=' * 60}\n通过 {ok}/{total}")
    print(
        "模式:",
        "fakeredis（模拟）" if os.getenv("USE_FAKE_REDIS") == "1" else "真实 Redis",
    )
    if ok != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
