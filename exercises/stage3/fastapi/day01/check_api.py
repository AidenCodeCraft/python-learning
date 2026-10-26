"""FastAPI Day 1 · 自检脚本（不用手动点 Swagger，直接对答案）

用法：
    cd exercises/stage3/fastapi/day01
    python check_api.py

原理：fastapi.testclient.TestClient 可以**不启动服务器**直接调你的接口。
每一行打印"对上了吗"，False 就回去改 main.py。
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app, ITEMS

client = TestClient(app, raise_server_exceptions=False)


def check(label: str, actual: object, expect: object) -> bool:
    ok = actual == expect
    print(f"{label:<26} 实际={actual!r:<44} 预期={expect!r:<44} 对上了吗: {ok}")
    return ok


def body(r) -> object:
    """安全解析响应体：500/空 body 时返回 {}，不让脚本崩。"""
    try:
        return r.json()
    except Exception:
        return {}


def first_of(r) -> dict:
    data = body(r)
    return data[0] if isinstance(data, list) and data else {}


def count_of(r) -> int:
    data = body(r)
    return len(data) if isinstance(data, list) else -1


def main() -> None:
    results: list[bool] = []

    # 1. GET /
    r = client.get("/")
    results.append(check("GET / 状态码", r.status_code, 200))
    results.append(check("GET / body", body(r), {"message": "Hello FastAPI"}))

    # 2. GET /health
    r = client.get("/health")
    results.append(check("GET /health 状态码", r.status_code, 200))
    results.append(check("GET /health body", body(r), {"status": "ok"}))

    # 3. GET /items（response_model 过滤 secret）
    r = client.get("/items")
    results.append(check("GET /items 状态码", r.status_code, 200))
    results.append(check("GET /items 条数", count_of(r), 2))
    results.append(check("GET /items 第一条", first_of(r),
                         {"id": 1, "name": "Python 入门书", "price": 99.0, "stock": 5}))
    results.append(check("GET /items 不含 secret", "secret" in first_of(r), False))

    # 分页
    r = client.get("/items?skip=1&limit=1")
    results.append(check("GET /items 分页条数", count_of(r), 1))
    results.append(check("GET /items 分页 id", first_of(r).get("id"), 2))

    # 4. GET /items/{item_id}
    r = client.get("/items/1")
    results.append(check("GET /items/1 状态码", r.status_code, 200))
    results.append(check("GET /items/1 body", body(r),
                         {"id": 1, "name": "Python 入门书", "price": 99.0, "stock": 5}))
    results.append(check("GET /items/1 不含 secret", "secret" in body(r), False))

    r = client.get("/items/999")
    results.append(check("GET /items/999 状态码", r.status_code, 404))
    results.append(check("GET /items/999 detail", body(r).get("detail") if isinstance(body(r), dict) else None,
                         "Item not found"))

    # 路径参数类型校验：传字符串 → 422
    r = client.get("/items/abc")
    results.append(check("GET /items/abc 状态码", r.status_code, 422))

    # 5. POST /items
    r = client.post("/items", json={"name": "鼠标", "price": 59.9})
    results.append(check("POST /items 状态码", r.status_code, 201))
    results.append(check("POST /items 新 id", body(r).get("id") if isinstance(body(r), dict) else None, 3))
    results.append(check("POST /items 默认 stock", body(r).get("stock") if isinstance(body(r), dict) else None, 0))
    results.append(check("POST /items name", body(r).get("name") if isinstance(body(r), dict) else None, "鼠标"))

    # 请求体校验：price <= 0 → 422
    r = client.post("/items", json={"name": "坏数据", "price": -1})
    results.append(check("POST price=-1 状态码", r.status_code, 422))
    r = client.post("/items", json={"name": "", "price": 10})
    results.append(check("POST name 空串 状态码", r.status_code, 422))

    # 6. PUT /items/{item_id}
    r = client.put("/items/1", json={"price": 88.0})
    results.append(check("PUT /items/1 状态码", r.status_code, 200))
    results.append(check("PUT /items/1 只改 price", body(r).get("price") if isinstance(body(r), dict) else None, 88.0))
    results.append(check("PUT /items/1 name 不变", body(r).get("name") if isinstance(body(r), dict) else None,
                         "Python 入门书"))

    r = client.put("/items/999", json={"price": 1.0})
    results.append(check("PUT /items/999 状态码", r.status_code, 404))

    # 7. DELETE /items/{item_id}
    r = client.delete("/items/2")
    results.append(check("DELETE /items/2 状态码", r.status_code, 204))
    results.append(check("DELETE 后 GET 状态码", client.get("/items/2").status_code, 404))
    r = client.delete("/items/999")
    results.append(check("DELETE /items/999 状态码", r.status_code, 404))

    # 汇总
    ok = sum(results)
    total = len(results)
    print(f"\n{'=' * 60}\n通过 {ok}/{total}")
    if ok != total:
        print("还没全对 —— 从上往下找第一个 False 去改 main.py")
    else:
        print("🎉 全对！Day1 过关，再去 /docs 手动点一遍试试")
    print(f"(提示：内存数据会被改动，重新运行脚本即复位；当前 ITEMS 数量 {len(ITEMS)})")


if __name__ == "__main__":
    main()
