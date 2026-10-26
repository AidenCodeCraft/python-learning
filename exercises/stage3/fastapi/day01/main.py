"""FastAPI Day 1 · 商品 API（作答文件）

运行（开发模式，改代码自动重启）：
    cd exercises/stage3/fastapi/day01
    uvicorn main:app --reload

打开交互式文档：
    http://127.0.0.1:8000/docs        # Swagger UI（可以点 Try it out 直接调接口）
    http://127.0.0.1:8000/redoc       # ReDoc

自检（不用手动点，直接对答案）：
    python check_api.py

规则：每个函数只做它自己的事；SQL/参数校验交给框架（Pydantic）和依赖。
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="商品 API", version="1.0.0")

# ============================================================
# 内存"数据库"（今天不连真库，Day3 再换成 SQLAlchemy）
# ============================================================
ITEMS: dict[int, dict] = {
    1: {"id": 1, "name": "Python 入门书", "price": 99.0, "stock": 5, "secret": "内部备注"},
    2: {"id": 2, "name": "机械键盘", "price": 399.0, "stock": 12, "secret": "内部备注"},
}
next_id = 3


# ============================================================
# Pydantic 模型（请求体校验 + 响应过滤）
# ============================================================

class ItemCreate(BaseModel):
    """创建商品时的请求体：只允许这三样。"""
    name: str = Field(min_length=1, max_length=50, description="商品名")
    price: float = Field(gt=0, description="单价，必须 > 0")
    stock: int = Field(default=0, ge=0, description="库存，>= 0")


class ItemUpdate(BaseModel):
    """更新商品：所有字段可选（只传要改的）。"""
    name: str | None = Field(default=None, min_length=1, max_length=50)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class Item(BaseModel):
    """响应模型：只暴露这 4 个字段（secret 会被过滤掉）。"""
    id: int
    name: str
    price: float
    stock: int


# ============================================================
# 第 1 题 · 最简单的接口
# ============================================================

@app.get("/")
def read_root() -> dict[str, str]:
    """GET / 返回 {"message": "Hello FastAPI"}"""
    # TODO
    return {}


# ============================================================
# 第 2 题 · 健康检查（公司脚手架必有的 /health）
# ============================================================

@app.get("/health")
def health() -> dict[str, str]:
    """GET /health 返回 {"status": "ok"}"""
    # TODO
    return {}


# ============================================================
# 第 3 题 · 列表 + 查询参数（分页）
# ============================================================

@app.get("/items", response_model=list[Item])
def list_items(skip: int = 0, limit: int = 10) -> list[dict]:
    """GET /items?skip=0&limit=10
    - 返回 ITEMS 的列表，按 id 升序
    - 用 skip / limit 分页（切片）
    - ⚠️ 注意 response_model 会把 secret 过滤掉
    """
    # TODO
    return []


# ============================================================
# 第 4 题 · 路径参数 + 404
# ============================================================

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> dict:
    """GET /items/{item_id}
    - item_id 是 **int**（路径参数，框架自动转换 + 校验）
    - 不存在 → raise HTTPException(status_code=404, detail="Item not found")
    """
    # TODO
    return {}


# ============================================================
# 第 5 题 · POST + 请求体 + 状态码 201
# ============================================================

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> dict:
    """POST /items
    - 请求体 ItemCreate（name/price/stock）
    - 用 next_id 分配新 id，写进 ITEMS，返回新商品
    - 状态码必须是 201（decoration 里的 status_code 已经写了，不用你再改）
    """
    # TODO
    return {}


# ============================================================
# 第 6 题 · PUT 局部更新（只改传了的字段）
# ============================================================

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemUpdate) -> dict:
    """PUT /items/{item_id}
    - 不存在 → 404 "Item not found"
    - 只更新 payload 里**不是 None** 的字段（用 model_dump(exclude_unset=True) 或判断 None）
    - 返回更新后的商品
    """
    # TODO
    return {}


# ============================================================
# 第 7 题 · DELETE + 204
# ============================================================

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    """DELETE /items/{item_id}
    - 不存在 → 404 "Item not found"
    - 存在 → 删除，返回 None（204 不能有 body）
    """
    # TODO
    return None
