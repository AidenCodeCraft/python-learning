from pathlib import Path
import sys

PUNCTUATION = ".,!?;:\"'()[]{}<>「」"

def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for raw in text.split():
        word = raw.strip(PUNCTUATION).lower()
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts

def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    ordered = sorted(counts.items(), key=lambda kv: (kv[-1], kv[0]))
    return ordered

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
    sys.exit()