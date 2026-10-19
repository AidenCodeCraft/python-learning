import pytest

from pathlib import Path

def test_pipeline_flow() -> None:
    store = Todo()
    store.add("a")
    store.add("b")
    store.done(1)

    assert store.taske[0].done is True
    assert store.taske[1].done is False

def test_raises_keyerror() -> None:
    with pytest.raises(KeyError):
        {"a": 1}["b"]

def test_file_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "a.txt"
    p.write_text("hi", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "hi"
