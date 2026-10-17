# 阶段 1 · 第 5 天（2026-10-18 · 周日 6h）· 工程化收尾 + 阶段 1 验收

> **主题：`pytest` ×3 + async 认知 + `todo_cli` 项目 + 阶段 1 验收**
> 今天是阶段 1 最后一天。**验收不通过 → 阶段 2 顺延**（见 [03-阶段1节奏修订](../../../notes/03-阶段1节奏修订.md) 的止损开关）。
>
> 今天的核心不是"学新语法"，而是把 D1–D4 学的东西**组装成一个能跑、能测、能提交的产物**。

---

## 今日时间表（6h）

| 时段 | 分钟 | 做什么 |
|---|---:|---|
| 收尾 | 10 | **清 D4 的尾巴**（见 [CHECKLIST.md](CHECKLIST.md) 第六节第一条） |
| pytest 讲解 | 30 | 读第一节 + 跑 `demo_pytest.py` |
| pytest 实战 | 50 | 给 `projects/stage1/todo_cli/test_todo.py` 写 3 个测试 |
| 项目主体 | 130 | 填 `todo.py` + `cli.py` 的 11 个 TODO，做到能 `add / list / done / delete` |
| async 认知 | 20 | 只讲不写代码（第二节） |
| 验收 | 60 | 8 类异常现场修正 + 口述 + 跑测试 + 提交 |
| 复盘 | 30 | 错题本 + CHECKLIST + README 收尾 |

> 中文乱码先 `chcp 65001`。

---

## 一、pytest：把"我会检查"变成"机器每次替我检查"

### 1. 为什么需要它（你已经吃过亏）

D2、D3、D4 你各有 2~3 处"**写完没运行 / 运行了没核对**"，D4 的微课甚至一跑就崩（`KeyError: 'tile'`）。
而 D4 的 20 题因为有 `check()` 自动跑，**全对**。

`pytest` 就是那个 `check()` 的正式版：**一次写好，以后每次改代码都能一键重跑全部检查。**

### 2. 最小用法（三句话）

```python
# test_demo.py
def test_add() -> None:
    assert 1 + 1 == 2          # 断言：不成立就 FAIL

def test_raises() -> None:
    import pytest
    with pytest.raises(ValueError):     # 断言"这里必须抛 ValueError"
        int("abc")
```

运行（在 `exercises/stage1/day05/` 目录下）：

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
cd exercises\stage1\day05
python -m pytest -v
```

**规则**：文件名 `test_*.py`、函数名 `test_*`、用普通 `assert`。

### 3. 两个必会的小工具

**`pytest.raises`** —— 断言"这里应该抛异常"：

```python
with pytest.raises(KeyError):
    {"a": 1}["b"]
```

**`tmp_path`** —— pytest 自动给你的**临时目录**（测试写文件用它，不污染项目）：

```python
def test_write(tmp_path) -> None:
    p = tmp_path / "a.txt"        # 一个不存在的临时文件路径
    p.write_text("hi", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "hi"
```

### 4. 运行结果怎么看

```text
test_xxx.py::test_add PASSED        ← 过了
test_xxx.py::test_bad FAILED        ← 断言不成立（下面会打印 "assert 1 == 2" 这种）
ERROR                                ← 代码本身崩了（import 错、语法错）
```

**先看最后一行汇总**：`1 failed, 3 passed in 0.12s`。

### 5. 练习（3 题，写在 `exercises/stage1/day05/test_practice.py`）

1. 写 `test_pipeline_flow()`：`store.add("a")` → `store.add("b")` → `store.done(1)`，断言第 1 条 `done` 为 `True`、第 2 条为 `False`。
2. 写 `test_raises_keyerror()`：用 `pytest.raises` 断言 `{"a": 1}["b"]` 抛 `KeyError`。
3. 写 `test_file_roundtrip(tmp_path)`：往 `tmp_path` 写一个 JSON，再读回来，断言内容一致。

### 示例文件

→ [demo_pytest.py](demo_pytest.py)（一个**故意有一半失败**的示范，跑一遍看 FAILED 长什么样）

---

## 二、async / await 认知课（20 分钟，**不写代码**）

> 原计划把它当知识点；修订版降级为"认知课"——**你现在只需要能说清它是什么**，正式动手放在阶段 3（FastAPI 天然是 async）。

### 一句话

**`async` 是"遇到等待就让路"的写法。** 它解决的不是"算得快"，而是"**等 I/O 的时候别干等着**"。

### 类比

- **同步（普通函数）**：你去餐厅点餐，站在窗口等厨师做好，期间什么都不干。
- **异步（async 函数）**：你点完餐拿个号，回座位看手机；餐好了叫你。**等的时间被你拿去干别的了。**

### 两个关键词

```python
async def fetch(url: str) -> str:      # async def 定义"协程"
    ...

await fetch("http://...")              # await = "这里要等，先让出去"
```

### 什么时候有用 / 没用

| 有用 | 没用 |
|---|---|
| 网络请求、数据库查询、读文件（**等 I/O**） | 纯计算（`1+1`、循环求和）—— 再 async 也不会变快 |

### 你现在只需要能回答 3 个问题

1. `async` 解决的是"算得快"还是"等的时候别干等"？→ **后者**。
2. 纯计算的函数用 async 会变快吗？→ **不会**。
3. FastAPI 的接口函数为什么常写成 `async def`？→ 因为里面多半要**等数据库/等网络**。

> ❌ 你阶段 0 第 7 题答的是"类似 C 的锁、有竞争的时候用" —— 那是**错误心智模型**。锁是"防止同时改共享数据"；async 是"等待时让出执行权"。两者不是一回事。

---

## 三、8 类异常：现场验收用

阶段 1 验收要求你**现场说异常类型 + 现场改对**。先自测：

| 代码 | 抛什么异常？ |
|---|---|
| `undefined_name` | ? |
| `1 + "a"` | ? |
| `[1, 2][5]` | ? |
| `{"a": 1}["b"]` | ? |
| `int("abc")` | ? |
| `if True` 下一行缩进不一致 | ? |
| `import not_exist_module` | ? |
| `"abc".push("d")` | ? |

<details>
<summary>对答案</summary>

`NameError` / `TypeError` / `IndexError` / `KeyError` / `ValueError` / `IndentationError` / `ModuleNotFoundError`（`ImportError` 的子类）/ `AttributeError`

</details>

> 验收时我会**随机抽 4 个**给你现改，不是背名字就行 —— 要能说出"为什么"。

---

## 四、项目：`todo_cli`（阶段 1 的验收产物）

→ [projects/stage1/todo_cli/README.md](../../../projects/stage1/todo_cli/README.md)

| 文件 | 你要做什么 |
|---|---|
| `todo.py` | 填 10 个 TODO（`Todo` 类 + `TodoStore` 类） |
| `cli.py` | 填 1 个 TODO（命令行分发） |
| `test_todo.py` | 写 3 个 pytest（有 1 个示范已写好） |

**目标**：`python cli.py add "写代码"` / `list` / `done 1` / `delete 1` 全部能用，数据存 JSON，测试全绿。

---

## 五、阶段 1 验收清单（我明天逐条查）

| # | 验收项 | 怎么验 |
|---|---|---|
| 1 | 100~150 行可运行脚本 | `todo.py` + `cli.py` 行数；四个命令真跑一遍 |
| 2 | 3 个 pytest 全绿 | `python -m pytest -v` |
| 3 | 8 类异常现场修正 | 我抽 4 个现场改 |
| 4 | 能用函数 + 模块拆分 | 说清 `todo.py` / `cli.py` 的职责边界 |
| 5 | Git 提交（`feat:` 规范） | `git log --oneline` |
| 6 | 口述 6 条 | 见下 |

### 口述 6 条（合上所有文件说）

1. 可变 / 不可变；别名 / 浅拷贝 / `deepcopy`
2. 默认参数陷阱；`None` 占位的原因
3. `and` / `or` 返回操作数本身
4. 循环三问（数据源 / 累加器 / 边界）
5. 类属性 vs 实例属性
6. `async` 解决什么问题

---

## 六、提交格式

```text
【阶段1 D5 提交 + 阶段验收】
1. pytest 练习 3 题 + 项目 3 个测试的 pytest -v 输出
2. todo.py / cli.py 的最终代码（贴出来）+ 行数（wc / (Get-Content).Count）
3. 四个命令的实际输出（add / list / done / delete）
4. 8 类异常：我的答案 + 我改对的那 4 个
5. 口述 6 条（每条约一句话）
6. self-check / 报错截图
7. git log --oneline
8. 卡住点
```

---

## 七、如果我做了什么不符合预期，你会怎么判？

- 测试没跑绿 → **D5 不通过**，阶段 2 顺延半天（用止损开关）
- 项目跑不起来 / 数据存不住 → 不通过
- 8 类异常现场说不出 → 补 30 分钟再验
- **验收通过 → 10-19 起按计划进入阶段 2（数据库与 Redis）**
