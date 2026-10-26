# 10 · FastAPI 学习路线（面向公司脚手架）· 2026-10-26 制定

> **学员问题**：现在开始学 FastAPI 了吗？要不要补 Redis？老师让看 [官方中文文档](https://fastapi.tiangolo.com/zh/)，说周五（10-30）培训公司的脚手架。

---

## 一、先回答三个问题

### Q1：现在开始学 FastAPI 吗？→ **是，今天（10-26）开始**

阶段 3 正式启动。原计划 10-26 周先 Redis 再 FastAPI，现调整为 **FastAPI 主线 + Redis 最小集并行**。

### Q2：学 FastAPI 要不要补 Redis？→ **要，但不是"先学完整 Redis"**

| 结论 | 说明 |
|---|---|
| **需要 Redis** | 公司 FastAPI 项目几乎必用：接口缓存、限流、验证码、Session/Token、分布式锁、队列 |
| **不是整门课** | 你 10-23 已速成 5 类结构，缺的是"**在 FastAPI 里怎么用**"：异步客户端、连接池、lifespan、缓存 JSON、TTL、限流 |
| **安排** | **10-27 下午 2h「Redis in FastAPI 最小集」**（够用即可），完整 Redis 放到后面按需补（缓存穿透/击穿/雪崩、集群等） |

### Q3：老师让看的官方文档怎么用？→ **别从首页读，按 Tutorial 章节挑着读**

那个链接（[fastapi.tiangolo.com/zh/#interactive-api-docs-upgrade](https://fastapi.tiangolo.com/zh/#interactive-api-docs-upgrade)）是**首页示例的"交互式文档升级"小节** —— 讲的是"把示例代码从 FastAPI 0.x 旧版升级到新版"，**对学习价值很低**。

正确用法：
1. 首页只看 10 分钟（了解是什么、装什么）
2. 真正学的是 **[教程 - 用户指南](https://fastapi.tiangolo.com/zh/tutorial/)**（菜单"学习 → 教程"）
3. **先跑示例 → 改参数 → 改成自己的需求**，不要通读
4. 每个主题学完，回 `/docs` 里点一遍

---

## 二、5 天路线（10-26 ~ 10-30，含周五脚手架培训）

| 日期 | 内容 | 官方文档对应章节 | 教材/产出 |
|---|---|---|---|
| **10-26 一（今天）** | 第一个 API、路径参数、查询参数、请求体、响应模型、状态码、错误处理、`/docs`、uvicorn | 第一步 / 路径参数 / 查询参数 / 请求体 / 响应模型 / 响应状态码 / 处理错误 | [day01](../exercises/stage3/fastapi/day01/README.md)（7 接口 + 29 项自检） |
| **10-27 二** | 依赖注入 `Depends`、中间件、CORS、全局异常处理、生命周期 `lifespan` + **Redis 最小集（2h）** | 依赖项 / 中间件 / CORS / 生命周期事件 | day02（明天出） |
| **10-28 三** | SQLAlchemy 2.x 接数据库、数据库会话依赖、**APIRouter 多文件分层**、分页与统一响应 | SQL 数据库 / 更大的应用-多个文件 | day03（含 mini 脚手架） |
| **10-29 四** | OAuth2 + JWT 鉴权、`pytest` + `TestClient` 测试、日志、配置 `pydantic-settings` | 安全性 / 测试 / 设置和环境变量 | day04 |
| **10-30 五** | **公司脚手架培训**：听懂 + 提问 + 对照自己写的 mini 脚手架 | — | 本文第四节清单 |

---

## 三、FastAPI Day1 现在就做（预计 3h）

```powershell
cd D:\Program\Python\python-learning\exercises\stage3\fastapi\day01
.\.venv\Scripts\Activate.ps1        # 若还没激活（在仓库根目录激活）
uvicorn main:app --reload           # 启动后打开 http://127.0.0.1:8000/docs
python check_api.py                 # 边写边自检，目标是 29/29
```

> 依赖已装好：fastapi 0.162.0 / uvicorn 0.54.0 / httpx 0.28.1（`requirements-fastapi.txt` 里也写了）。

**今天的目标不是"背语法"，是能独立写出带校验的 CRUD 接口。**

---

## 四、周五（10-30）脚手架培训：要准备的 12 个问题

> 培训时老师讲脚手架，你要能**对上号**，最好能问出水平。提前看懂下面 12 项，培训就是"复习 + 提问"。

| # | 要看懂什么 | 为什么重要 | 自己先做的准备 |
|---|---|---|---|
| 1 | **目录结构**（`app/` 下 routers / models / schemas / services / crud / core） | 决定了你以后加功能往哪放 | 10-28 自己搭一个 mini 版 |
| 2 | **入口**（`main.py` 里 `app = FastAPI()`、`include_router`） | 看代码从这里进 | day01 已写 |
| 3 | **配置**（`settings.py` + 环境变量 `.env`、`pydantic-settings`） | 数据库密码/Redis 地址都在这里 | 10-29 学 |
| 4 | **依赖注入**（`Depends(get_db)` / `Depends(get_current_user)`） | 脚手架的核心套路 | 10-27 学 |
| 5 | **数据库会话**（SQLAlchemy `Session`、`yield` 依赖、`Base`、`engine`） | 每个请求一个 session | 10-28 学 |
| 6 | **Pydantic schema**（`XxxCreate` / `XxxUpdate` / `XxxOut`） | 请求/响应模型分层 | day01 已写 |
| 7 | **路由分层**（`APIRouter(prefix="/users", tags=["用户"])`） | 多文件组织接口 | 10-28 学 |
| 8 | **统一响应/异常**（全局 exception handler、统一 `{code,msg,data}`） | 公司规范一般都有 | 10-27 学 |
| 9 | **鉴权**（OAuth2 + JWT、`get_current_user` 依赖） | 登录态怎么传 | 10-29 学 |
| 10 | **中间件**（日志、耗时、CORS、请求 ID） | 排查问题靠它 | 10-27 学 |
| 11 | **测试**（`pytest` + `TestClient` + 测试数据库覆盖） | 改代码敢不敢改 | 10-29 学 |
| 12 | **启动与部署**（`uvicorn`/`gunicorn`、Dockerfile、`alembic` 迁移） | 上线流程 | 10-30 问老师 |

**培训时值得问的 3 个问题**（显得你真看过）：
1. 脚手架的**数据库会话和 Redis 客户端**是在哪里初始化的？用 `lifespan` 还是全局？
2. 接口的**统一响应格式**是哪个中间件/依赖做的？异常是怎么转成统一格式的？
3. **新建一个业务模块**的标准步骤是什么（router → service → schema → model → 迁移）？

---

## 五、④造 和 Redis 的处理（学员确认）

- **基础篇④造（书签管理器）：暂停**，等 FastAPI 学完再一起练（周六可用时做）。
- **Redis 正式课**：今天不单独开课，10-27 只学"FastAPI 里怎么用"的最小集；完整内容等脚手架项目里真正用到时再补。

---

## 六、本周每日固定动作（不变）

1. **每日 15 分钟闭卷默写**（内容换成 FastAPI：从"只写过一次的接口"里抽一个默写）
2. **每日 5 分钟三段设计**（给一个接口需求写：数据/模块/步骤）
3. 每天结束提交 + 在 `mistakes/` 记当天卡点
