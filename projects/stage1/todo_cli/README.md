# 项目：todo_cli（阶段 1 验收产物）

> 目标：把 D1–D4 学的东西（函数、容器、类、文件、JSON、异常、类型注解）**组装成一个能跑的小工具**。
> 规模目标：`todo.py` + `cli.py` 合计 **100~150 行有效代码**（不含空行、注释和 docstring）。

---

## 一、功能需求

| 命令 | 行为 |
|---|---|
| `add <标题> [--priority 1|2|3]` | 新增一条待办，id 自动从 1 自增 |
| `list [--which all\|todo\|done]` | 列出待办（默认全部） |
| `done <id>` | 把某条标记为完成 |
| `delete <id>` | 删除某条 |

**数据持久化**：每次修改都要写回 JSON 文件（默认 `.tmp/todo.json`）。

---

## 二、数据格式（JSON）

```json
[
  {"id": 1, "title": "写代码", "done": false, "priority": 2},
  {"id": 2, "title": "自测", "done": true, "priority": 1}
]
```

---

## 三、文件职责（这就是"模块拆分"）

| 文件 | 职责 | 不许做什么 |
|---|---|---|
| `todo.py` | `Todo` 类 + `TodoStore` 类：数据、校验、读写 JSON | **不许 print、不许碰 sys.argv** |
| `cli.py` | 解析命令行参数、调用 `TodoStore`、打印结果 | 不许直接读写 JSON 文件 |
| `test_todo.py` | pytest 测试 | 不许依赖真实用户输入 |

> 分层的判断标准只有一句：**`todo.py` 被 import 时，不应该产生任何副作用**（不打印、不跑命令）。

---

## 四、怎么跑

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
cd projects\stage1\todo_cli

python cli.py add "写代码" --priority 1
python cli.py add "自测"
python cli.py list
python cli.py done 1
python cli.py list --which done
python cli.py delete 2

python -m pytest -v
```

---

## 五、验收标准

- [ ] 四个命令都能用，且**数据真的存进了 `.tmp/todo.json`**（关掉再开还在）
- [ ] `list --which todo` / `list --which done` 过滤正确
- [ ] `done 999` / `delete 999`（不存在的 id）**给出提示并返回非 0**，不崩
- [ ] `python -m pytest -v` → **4 passed**（1 个示范 + 你写的 3 个）
- [ ] `todo.py` + `cli.py` 合计 **100~150 行有效代码**（现骨架是 86 行，填完大约 120~140）
- [ ] 类型注解完整、没有裸 `except`
- [ ] `git commit -m "feat(stage1): todo_cli 项目（阶段 1 验收）"`

---

## 六、实现提示（卡住了再看）

<details>
<summary>提示 1：JSON 读写要保证目录存在</summary>

`.tmp/` 可能不存在 → `save()` 里先 `self.path.parent.mkdir(parents=True, exist_ok=True)`。
</details>

<details>
<summary>提示 2：`load()` 的正确骨架</summary>

```python
def load(self) -> None:
    if not self.path.exists():
        return                       # 文件不存在 → 保持空列表，不报错
    with open(self.path, encoding="utf-8") as f:
        raw = json.load(f)           # 读出来是 list[dict]
    self.todos = [Todo.from_dict(d) for d in raw]
```
</details>

<details>
<summary>提示 3：`--priority` 这种可选参数怎么解析</summary>

用标准库 `argparse` 最省事，也可以用 `sys.argv` 手动判断。**推荐 argparse**：
```python
import argparse
parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="cmd", required=True)
p_add = sub.add_parser("add")
p_add.add_argument("title")
p_add.add_argument("--priority", type=int, default=2, choices=[1, 2, 3])
```
</details>

<details>
<summary>提示 4：`_next_id` 一行写法</summary>

`return max((t.id for t in self.todos), default=0) + 1`
</details>
