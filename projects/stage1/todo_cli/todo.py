"""待办清单 · 核心逻辑（阶段 1 验收项目）

数据文件：JSON 数组，每条形如
    {"id": 1, "title": "写代码", "done": false, "priority": 2}

分层：
    todo.py       数据与逻辑（Todo + TodoStore）—— 不 print、不碰 sys.argv
    cli.py        命令行入口 —— 只解析参数、调 store、打印
    test_todo.py  pytest 测试

运行测试：
    cd projects/stage1/todo_cli
    python -m pytest -v
"""

from __future__ import annotations

import json
from pathlib import Path

DEFAULT_PATH = Path(".tmp/todo.json")


class Todo:
    """一条待办。"""

    def __init__(self, title: str, priority: int = 2, done: bool = False, todo_id: int = 0) -> None:
        self.id = todo_id
        self.title = title
        self.priority = priority
        self.done = done

    def to_dict(self) -> dict[str, object]:
        """TODO 1：转成能写进 JSON 的 dict（键名与文件格式一致：id / title / done / priority）。"""
        raise NotImplementedError("TODO 1: 实现 Todo.to_dict")

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Todo":
        """TODO 2：从 JSON 读出来的 dict 造一个 Todo。

        注意：JSON 读回来 id 是 int、done 是 bool，但类型是 object，
        请用 int(...) / bool(...) 转一下（类型注解要求）。
        """
        raise NotImplementedError("TODO 2: 实现 Todo.from_dict")

    def __str__(self) -> str:
        """TODO 3：格式形如 `[x] (P1) 写代码`；未完成时是 `[ ]`。"""
        raise NotImplementedError("TODO 3: 实现 Todo.__str__")


class TodoStore:
    """待办集合：负责增删改查 + 读写 JSON。"""

    def __init__(self, path: Path = DEFAULT_PATH) -> None:
        self.path = path
        self.todos: list[Todo] = []
        self.load()

    # ---------- 读写 ----------

    def load(self) -> None:
        """TODO 4：文件不存在 → todos 保持空列表（不许崩）；存在 → 读出来转成 Todo。"""
        raise NotImplementedError("TODO 4: 实现 TodoStore.load")

    def save(self) -> None:
        """TODO 5：把 todos 写成 JSON（ensure_ascii=False, indent=2）。

        提示：父目录可能不存在，先 self.path.parent.mkdir(parents=True, exist_ok=True)。
        """
        raise NotImplementedError("TODO 5: 实现 TodoStore.save")

    # ---------- 业务 ----------

    def _next_id(self) -> int:
        """TODO 6：返回下一个可用 id（空列表时 1，否则最大 id + 1）。"""
        raise NotImplementedError("TODO 6: 实现 TodoStore._next_id")

    def add(self, title: str, priority: int = 2) -> Todo:
        """TODO 7：造 Todo → 分配 id → 追加到 todos → save() → 返回它。"""
        raise NotImplementedError("TODO 7: 实现 TodoStore.add")

    def list_items(self, which: str = "all") -> list[Todo]:
        """TODO 8：which 取 "all" / "todo" / "done"，返回对应子集。

        which 不是这三个值之一时，抛 ValueError。
        """
        raise NotImplementedError("TODO 8: 实现 TodoStore.list_items")

    def done(self, todo_id: int) -> bool:
        """TODO 9：把指定 id 标为完成并 save()；找不到返回 False。"""
        raise NotImplementedError("TODO 9: 实现 TodoStore.done")

    def delete(self, todo_id: int) -> bool:
        """TODO 10：删除指定 id 并 save()；找不到返回 False。"""
        raise NotImplementedError("TODO 10: 实现 TodoStore.delete")
