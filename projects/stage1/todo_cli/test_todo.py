"""阶段 1 验收：3 个 pytest 测试（自己写）+ 1 个示范

运行：
    cd projects/stage1/todo_cli
    python -m pytest -v

目标：4 passed（1 个示范 + 你写的 3 个）
"""

from __future__ import annotations

from pathlib import Path

import pytest

from todo import Todo, TodoStore


def test_load_missing_file_is_empty(tmp_path: Path) -> None:
    """【示范，已写好】文件不存在时不许崩，todos 是空列表。

    注意：它现在会 FAILED —— 因为 `TodoStore.load()` 还是 TODO 4。
    完成 TODO 4 之后，这条会自动变绿；你写的另外 3 条也一样。
    """
    store = TodoStore(tmp_path / "nope.json")
    assert store.todos == []


def test_add_and_list(tmp_path: Path) -> None:
    """TODO 12：add 两条后，todos 里应有 2 条，id 分别是 1、2。

    要求：
      - 用 TodoStore(tmp_path / "t.json")（不要用真实数据文件！）
      - add("a") 和 add("b")
      - 断言 len(store.todos) == 2
      - 断言 [t.id for t in store.todos] == [1, 2]
      - 断言 [t.title for t in store.todos] == ["a", "b"]
    """
    raise NotImplementedError("TODO 12: 写这个测试")


def test_done_marks_only_target(tmp_path: Path) -> None:
    """TODO 13：done(1) 之后，第 1 条是 True、第 2 条仍是 False。"""
    raise NotImplementedError("TODO 13: 写这个测试")


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    """TODO 14：持久化真的生效。

    要求：
      - store1 在 tmp_path 里 add 两条
      - 新建 store2 = TodoStore(同一个路径)
      - 断言 store2.todos 的内容和 store1 一致（id / title / done / priority）
    """
    raise NotImplementedError("TODO 14: 写这个测试")
