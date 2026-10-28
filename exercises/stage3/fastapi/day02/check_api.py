"""FastAPI Day 2 · 自检脚本

用法：
    cd exercises/stage3/fastapi/day02
    python check_api.py

注意：这里用 `with TestClient(app) as client:` —— 这样才会触发 lifespan（startup/shutdown）。
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

results: list[bool] = []


def check(label: str, actual: object, expect: object) -> None:
    ok = actual == expect
    results.append(ok)
    print(f"{label:<28} 实际={actual!r:<44} 预期={expect!r:<44} 对上了吗: {ok}")


def body(r) -> object:
    try:
        return r.json()
    except Exception:
        return {}


def main() -> None:
    with TestClient(app, raise_server_exceptions=False) as client:
        # 第 8 题 · lifespan
        r = client.get("/lifespan-check")
        check("lifespan 已启动", body(r), {"started": True})

        # 第 2 题 · 配置依赖
        r = client.get("/info")
        check("GET /info", body(r), {"app_name": "商品 API", "version": "2.0.0"})

        # 第 1 题 · 分页依赖
        r = client.get("/items")
        check(
            "GET /items 默认分页条数",
            len(body(r)) if isinstance(body(r), list) else -1,
            2,
        )
        r = client.get("/items?skip=1&limit=1")
        data = body(r)
        check("GET /items 分页条数", len(data) if isinstance(data, list) else -1, 1)
        check(
            "GET /items 分页 id",
            data[0].get("id") if isinstance(data, list) and data else None,
            2,
        )
        check(
            "GET /items?limit=0 状态码", client.get("/items?limit=0").status_code, 422
        )
        check(
            "GET /items?limit=999 状态码",
            client.get("/items?limit=999").status_code,
            422,
        )

        # 第 3 题 · yield 依赖
        r = client.get("/db-check")
        check("GET /db-check", body(r), {"db": "session", "opened": 1})
        r = client.get("/db-closed")
        check("GET /db-closed", body(r), {"closed": 1})

        # 第 4 题 · 中间件加响应头
        r = client.get("/")
        header = r.headers.get("x-process-time")
        check("X-Process-Time 存在", header is not None, True)
        try:
            ok_float = float(header) >= 0
        except (TypeError, ValueError):
            ok_float = False
        check("X-Process-Time 是数字", ok_float, True)

        # 第 5 题 · CORS
        r = client.get("/items", headers={"Origin": "http://localhost:3000"})
        check(
            "CORS 允许的源",
            r.headers.get("access-control-allow-origin"),
            "http://localhost:3000",
        )
        r = client.get("/items", headers={"Origin": "http://evil.com"})
        check("CORS 未允许的源无头", r.headers.get("access-control-allow-origin"), None)

        # 第 6/7 题 · 自定义异常 + 全局处理器
        r = client.get("/items/999")
        check("GET /items/999 状态码", r.status_code, 404)
        check(
            "GET /items/999 统一格式",
            body(r),
            {"code": 40400, "msg": "Item not found", "data": None},
        )
        r = client.get("/items/1")
        check(
            "GET /items/1 正常",
            body(r),
            {"id": 1, "name": "Python 入门书", "price": 99.0, "stock": 5},
        )

    # 汇总
    ok = sum(results)
    total = len(results)
    print(f"\n{'=' * 60}\n通过 {ok}/{total}")
    if ok == total:
        print("🎉 全对！Day2 过关")
    else:
        print("还没全对 —— 从上往下找第一个 False，去改 main.py")


if __name__ == "__main__":
    main()
