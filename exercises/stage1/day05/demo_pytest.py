"""pytest 示范：故意一半通过、一半失败

运行（在本目录下）：
    python -m pytest demo_pytest.py -v

看两件事：
    1. FAILED 时 pytest 会打印 "assert 1 + 1 == 3" 这种"期望 vs 实际"
    2. pytest.raises 断言"这里必须抛某种异常"
"""

from __future__ import annotations

from pathlib import Path

import pytest


def test_pass_simple() -> None:
    assert 1 + 1 == 2


def test_pass_sorted() -> None:
    assert sorted([3, 1, 2]) == [1, 2, 3]


def test_fail_assert() -> None:
    """这条会 FAILED —— 看看 pytest 怎么告诉你实际值。"""
    assert 1 + 1 == 3


def test_pass_raises() -> None:
    with pytest.raises(KeyError):
        {"a": 1}["b"]


def test_fail_raises_wrong_type() -> None:
    """这条会 FAILED —— 实际抛的是 ValueError，不是 KeyError。"""
    with pytest.raises(KeyError):
        int("abc")


def test_tmp_path(tmp_path: Path) -> None:
    """tmp_path 是 pytest 自动给的临时目录，测试写文件就用它。"""
    p = tmp_path / "a.txt"
    p.write_text("hi", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "hi"
