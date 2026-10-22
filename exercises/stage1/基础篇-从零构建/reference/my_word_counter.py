from pathlib import Path
import sys

PUNCTUATION = ".,!?;:\"'()[]{}<>「」"

def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def count_words(text: str, min_lenth: int = 1) -> tuple[dict[str, int], int]:
    counts: dict[str, int] = {}
    total = len(text.split())
    for raw in text.split():
        word = raw.strip(PUNCTUATION).lower()
        if not word or len(word) < min_lenth:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts, total

def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
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
            try:
                top = int(argv[index + 1])
            except ValueError:
                print("--top 后面的参数必须是整数")

    text = read_text(path)
    if not text:
        print(f"文件不存在或内容为空: {path}")
        return 1

    min_length = 1
    if "--min-length" in argv:
        index = argv.index("--min-length")
        if index + 1 < len(argv):
            try:
                min_length = int(argv[index + 1])
            except ValueError:
                print("--min-length 后面的参数必须是整数")
    counts, total = count_words(text, min_length)
    # 其实我一开始想着是在main中直接加上len(text.split())这种最简单，也最直接，如果只是临时解决可以这样。
    # 但是因为count_words本身就是统计文件中字符串的个数，再完善其功能让能返回一共多少个单词，刚好合适。
    print(f"原文共 {total} 个词，不同单词数: {len(counts)}")

    print("-" * 20)
    for word, cnt in top_n(counts, top):
        print(f"{word:<12}{cnt}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))