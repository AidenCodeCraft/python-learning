"""FastAPI Day 2 · 依赖注入 / 中间件 / 全局异常 / lifespan（作答文件）

运行：
    cd exercises/stage3/fastapi/day02
    uvicorn main:app --reload
    http://127.0.0.1:8000/docs

自检：
    python check_api.py       # 目标：全 True

说明：Day1 的 CRUD 已经写好了（直接搬过来），你只需要补第 1~8 题的 Day2 部分。
"""

from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

APP_NAME = "商品 API"
APP_VERSION = "2.0.0"

# 应用级状态（真实项目里这里是数据库连接池、Redis 客户端等）
STATE: dict[str, object] = {
    "started": False,        # lifespan 是否已启动
    "db_opened": 0,          # 打开了多少个"数据库会话"
    "db_closed": 0,          # 关闭了多少个
}


# ============================================================
# 第 8 题 · lifespan：应用启动/关闭时执行的代码
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时：STATE["started"] = True；关闭时：STATE["started"] = False。

    ⚠️ yield 之前 = startup，yield 之后 = shutdown。
    真实项目在这里初始化：数据库连接池、Redis 客户端、加载配置。
    """
    # TODO: 启动逻辑
    yield
    # TODO: 关闭逻辑


app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)


# ============================================================
# 第 4 题 · 中间件：给每个响应加 X-Process-Time 响应头
# ============================================================

# TODO: 用 @app.middleware("http") 实现
# async def add_process_time(request: Request, call_next):
#     start = time.perf_counter()
#     response = await call_next(request)
#     response.headers["X-Process-Time"] = f"{(time.perf_counter() - start) * 1000:.2f}"
#     return response


# ============================================================
# 第 5 题 · CORS：允许前端 http://localhost:3000 跨域访问
# ============================================================

# TODO: app.add_middleware(CORSMiddleware, allow_origins=[...], allow_credentials=True,
#                          allow_methods=["*"], allow_headers=["*"])


# ============================================================
# 内存数据（Day1 已实现）
# ============================================================

ITEMS: dict[int, dict] = {
    1: {"id": 1, "name": "Python 入门书", "price": 99.0, "stock": 5, "secret": "内部备注"},
    2: {"id": 2, "name": "机械键盘", "price": 399.0, "stock": 12, "secret": "内部备注"},
}
next_id = 3


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class Item(BaseModel):
    id: int
    name: str
    price: float
    stock: int


# ============================================================
# 第 6 题 · 自定义业务异常 + 全局异常处理器
# ============================================================

class ItemNotFoundError(Exception):
    """业务异常：商品不存在。不要直接 raise HTTPException，交给全局处理器统一格式。"""


# TODO: 用 @app.exception_handler(ItemNotFoundError) 注册处理器
# 要求返回 JSONResponse(status_code=404, content={"code": 40400, "msg": "Item not found", "data": None})


# ============================================================
# 第 1 题 · 分页依赖（类作为依赖）
# ============================================================

class Pagination:
    """分页依赖：skip >= 0，limit 在 1~100。

    ❗用 Query 给默认值 + 校验（不是普通 int 默认值），这样 /items?limit=0 会返回 422。
    """

    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="跳过几条"),
        limit: int = Query(default=10, ge=1, le=100, description="每页几条"),
    ) -> None:
        self.skip = skip
        self.limit = limit


# ============================================================
# 第 2 题 · 配置依赖
# ============================================================

def get_settings() -> dict[str, str]:
    """返回应用配置（真实项目读环境变量 / pydantic-settings）。"""
    # TODO: return {"app_name": APP_NAME, "version": APP_VERSION}
    return {}


# ============================================================
# 第 3 题 · yield 依赖（模拟数据库会话：进入时打开，响应后关闭）
# ============================================================

def get_db():
    """yield 之前打开会话，yield 之后关闭会话。

    要求：
      - 进入：STATE["db_opened"] += 1
      - yield 一个字符串 "session"（真实项目是 Session 对象）
      - finally：STATE["db_closed"] += 1
    """
    # TODO
    yield "session"
    # TODO: finally 里计数


# ============================================================
# 接口
# ============================================================

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/info")
def get_info(settings: dict[str, str] = Depends(get_settings)) -> dict[str, str]:
    """第 2 题：通过 Depends 注入配置，返回 {"app_name": ..., "version": ...}"""
    # TODO: return settings（或组装）
    return {}


@app.get("/db-check")
def db_check(db: str = Depends(get_db)) -> dict[str, object]:
    """第 3 题：返回 {"db": 依赖给的值, "opened": STATE["db_opened"]}"""
    # TODO
    return {}


@app.get("/db-closed")
def db_closed() -> dict[str, object]:
    """第 3 题：返回 {"closed": STATE["db_closed"]}（用来验证 yield 之后的清理真的执行了）"""
    # TODO
    return {}


@app.get("/lifespan-check")
def lifespan_check() -> dict[str, object]:
    """第 8 题：返回 {"started": STATE["started"]}"""
    # TODO
    return {}


@app.get("/items", response_model=list[Item])
def list_items(page: Pagination = Depends()) -> list[dict]:
    """第 1 题：用 Pagination 依赖分页（不再直接写 skip/limit 参数）。"""
    # TODO
    return []


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> dict:
    """第 6 题：不存在时 raise ItemNotFoundError（不是 HTTPException），交给全局处理器。"""
    # TODO
    return {}


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> dict:
    """Day1 已实现，不用改。"""
    global next_id
    new_data = {"id": next_id, **payload.model_dump(), "secret": "内部备注"}
    ITEMS[next_id] = new_data
    next_id += 1
    return new_data


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> dict:
    """Day1 已实现，不用改。"""
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    ITEMS[item_id].update(payload.model_dump(exclude_unset=True))
    return ITEMS[item_id]


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    """Day1 已实现，不用改。"""
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    del ITEMS[item_id]
    return None
