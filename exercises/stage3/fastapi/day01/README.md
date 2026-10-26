# FastAPI Day 1 · 从零到第一个可用的商品 API（2026-10-26）

> **上一版写得像速查，这一版拆成了"讲解 + 练习"两份，从头讲。**
> 目标：约 3 小时，能独立写出带校验的 CRUD 接口，并看懂 `/docs`。

---

## 阅读顺序（重要）

| 步骤 | 文件 | 时间 | 做什么 |
|---|---|---:|---|
| **① 讲解** | **[01-讲解-零基础看懂.md](01-讲解-零基础看懂.md)** | 40min | 建立画面：请求→函数→JSON；逐行拆解最小例子；三种参数来源；Pydantic；状态码；常见报错 |
| **② 练习** | **[02-练习-7个接口.md](02-练习-7个接口.md)** | 120min | 7 个接口，每题都有"在练什么 / 从哪开始 / 预期结果 / 常见错误" |
| ③ 对照官方文档 | [01 讲解第 13 节](01-讲解-零基础看懂.md#13-官方文档怎么配合看别通读) | 30min | 只看 6 个小节（第一步 / 路径参数 / 查询参数 / 请求体 / 响应模型 / 处理错误） |
| ④ 自检 | `python check_api.py` | 10min | 目标 **29/29** |

---

## 文件清单

| 文件 | 用途 |
|---|---|
| [01-讲解-零基础看懂.md](01-讲解-零基础看懂.md) | **先读这个**：概念 + 逐行拆解 + 术语表 + 官方文档对照 |
| [02-练习-7个接口.md](02-练习-7个接口.md) | 7 题的分步讲解（做题时看） |
| [main.py](main.py) | **作答文件**（7 个接口的骨架，你填 TOD O） |
| [check_api.py](check_api.py) | 自检脚本（29 项检查，自动判分） |
| [../requirements-fastapi.txt](../requirements-fastapi.txt) | 依赖清单（换机器时 `pip install -r`） |

---

## 运行（今天第一步）

```powershell
cd D:\Program\Python\python-learning\exercises\stage3\fastapi\day01

# 启动（方式 A：venv 已激活）
uvicorn main:app --reload
# 启动（方式 B：没激活，最保险）
D:\Program\Python\python-learning\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

成功会看到：
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

然后浏览器打开：
- **http://127.0.0.1:8000/docs** —— Swagger UI，能点 `Try it out` 手动调接口
- http://127.0.0.1:8000/health —— 你写的健康检查

> ⚠️ 现在接口还是骨架（返回 `{}`），`/docs` 能打开但结果不对 —— 这就是你要填的。

---

## 自检

```powershell
python check_api.py          # 或 .venv\Scripts\python.exe check_api.py
```

- 每行打印 `对上了吗: True/False`
- 最后 `通过 X/29`
- 现在（骨架）应该是 **9/29**；全写完是 **29/29**

---

## 今天要掌握的概念（自查）

- [ ] 一次 HTTP 请求的三件事：方法（GET/POST/PUT/DELETE）+ 路径 +（可选）请求体
- [ ] 类型注解在 FastAPI 里 = 自动校验 + 自动文档（不是装饰）
- [ ] 参数三种来源：路径参数 / 查询参数（有默认值）/ 请求体（Pydantic 模型）
- [ ] `Pydantic` + `Field` 写校验规则；不满足 → 422
- [ ] `response_model` = 响应白名单（过滤 secret）
- [ ] `raise HTTPException(404, detail=...)` vs `return {"error": ...}` 的区别
- [ ] uvicorn 命令里 `main:app` 是什么意思
- [ ] `/docs` 是怎么自动生成的（OpenAPI）

---

## 验收标准

- [ ] `check_api.py` **29/29**
- [ ] `uvicorn main:app --reload` 能启动，`/docs` 里能看到 7 个接口
- [ ] 能在 `/docs` 里用 `Try it out` 成功调一次 POST
- [ ] 上面 8 个概念能口述
- [ ] 提交（见 02 文件末尾的提交模板）

---

## 和官方文档的关系

老师给的 [中文文档首页](https://fastapi.tiangolo.com/zh/) 用来"查"，我们的教材用来"学"：

- **主线**：本目录 01 → 02（顺序、例子、练习、报错都属于同一套代码）
- **参考**：官方 6 个小节（链接见 01 第 13 节），读法：**先跑它的示例 → 改参数 → 回来看我们的练习**
- ❌ 不要从"首页的示例升级/交互式文档"、`async/await`、`高级用户指南` 开始看
