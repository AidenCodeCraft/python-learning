"""单词计数器 · 构建训练营 Day2 的参考实现（完整可跑）

功能：读取一个文本文件，统计每个单词出现次数，打印出现最多的前 N 个。

用法：
    python word_counter.py sample.txt
    python word_counter.py sample.txt --top 5

设计（对应 Day1 的"三段设计法"）：
    ① 数据：dict[str, int]，例如 {"the": 5, "cat": 3}
    ② 分层：
        read_text()   —— 只负责读文件（不打印）
        count_words() —— 只负责数词（不读文件、不打印）
        top_n()       —— 只负责排序取前 N（不打印）
        main()        —— 只负责串起来 + 打印
    ③ 步骤：读文件 → 切词 → 数词 → 排序 → 取前 N → 打印
"""

from __future__ import annotations

import sys
from pathlib import Path

PUNCTUATION = ".,!?;:\"'()[]{}<>「」"


def read_text(path: Path) -> str:
    """读文件内容；文件不存在时返回空字符串（不抛异常）。"""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def count_words(text: str) -> dict[str, int]:
    """统计每个词出现的次数：统一小写、去掉首尾标点、跳过空串。"""
    counts: dict[str, int] = {}
    for raw in text.split():
        word = raw.strip(PUNCTUATION).lower()
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """按次数从高到低取前 n 个；次数相同时按字母升序。"""
    ordered = sorted(counts.items(), key=lambda kv: (kv[-1], kv[0]))
    return ordered[:n]


def main(argv: list[str]) -> int:
    """命令行入口：统一在这里解析参数、调用上面的函数、负责打印。"""
    if not argv:
        print("用法: python word_counter.py <文件> [--top N]")
        return 1

    path = Path(argv[0])
    top = 10
    if "--top" in argv:
        index = argv.index("--top")
        if index + 1 < len(argv):
            top = int(argv[index + 1])

    text = read_text(path)
    if not text:
        print(f"文件不存在或内容为空: {path}")
        return 1

    counts = count_words(text)
    print(f"不同单词数: {len(counts)}")
    print("-" * 20)
    for word, cnt in top_n(counts, top):
        print(f"{word:<12}{cnt}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
