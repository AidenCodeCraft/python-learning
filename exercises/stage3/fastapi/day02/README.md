# FastAPI Day 2 · 依赖注入 / 中间件 / 异常 / lifespan（3 小时）

> ✂️ **10-28 减负**：今天**只需做 3 个点** —— **lifespan / Depends 配置依赖 / 自定义异常 + 全局处理器**。
> **中间件、CORS 跳过**（知道"有这么个东西"即可，用到再回来看）。
> 自检目标不是 16/16，而是"3 个点对应的检查项通过"。

> Day1 你写出了 7 个能跑的接口（29/29 ✅）。Day2 学"工程化"：**消除重复代码、统一错误格式、管理资源**。
> 这两套东西是公司脚手架的骨架 —— 周五培训时你会看到它们。

## 阅读顺序

| 步骤 | 文件 | 时间 |
|---|---|---:|
| ① 讲解 | [01-讲解-依赖注入与中间件.md](01-讲解-依赖注入与中间件.md) | 40min |
| ② 练习 | [02-练习.md](02-练习.md)（8 个点） | 100min |
| ③ 自检 | `python check_api.py` → 目标 **16/16** | 10min |
| ④ 官方对照 | 依赖项 / yield 依赖项 / 中间件 / CORS / 处理错误 / 生命周期事件（链接在讲解末尾） | 30min |

## 文件

| 文件 | 用途 |
|---|---|
| [01-讲解-依赖注入与中间件.md](01-讲解-依赖注入与中间件.md) | 先读：为什么需要依赖注入、三种依赖、中间件 vs 依赖、全局异常、lifespan |
| [02-练习.md](02-练习.md) | 8 个点的分步提示 |
| [main.py](main.py) | **作答文件**（Day1 的 CRUD 已搬入，只填 Day2 的 TODO） |
| [check_api.py](check_api.py) | 自检 16 项 |

## 运行

```powershell
cd D:\Program\Python\python-learning\exercises\stage3\fastapi\day02
..\..\..\..\.venv\Scripts\python.exe -m uvicorn main:app --reload
# http://127.0.0.1:8000/docs
..\..\..\..\.venv\Scripts\python.exe check_api.py
```

现在（骨架）**3/16**，全写完 **16/16**。

## 今天要掌握的概念

- [ ] `Depends(f)` 在做什么：**执行接口前先调用 f，把返回值注入参数**
- [ ] 三种依赖写法：普通函数 / 类（`Pagination`）/ `yield`（管资源）
- [ ] `yield` 依赖的 `finally` 在**响应发完后**执行（等价于 Day1 的 try/finally 关连接）
- [ ] 中间件 = 每个请求都过的关卡（改 header、日志、耗时）；**中间件 vs 依赖**的区别
- [ ] CORS 解决什么问题、`allow_origins` 写什么
- [ ] 自定义异常 + `@app.exception_handler` 统一成 `{code, msg, data}`
- [ ] `lifespan`：启动建连接池、关闭释放（`on_event` 已弃用）
