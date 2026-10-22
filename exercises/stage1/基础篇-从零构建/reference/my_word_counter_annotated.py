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

# 创建一个读文件的函数read_text，需要传递文件地址，函数返回str格式
def read_text(path: Path) -> str:
    """读文件内容；文件不存在时返回空字符串（不抛异常）。"""
    # 判断path这个路径是否存在。
    if not path.exists():
        # 不存在时返回空字符串
        # 因为 main 已经做好了兜底。
        return ""
    # 以文本模式打开这个路径的文件，按照UTF-8的格式读取它，然后关闭文件。返回读取的文件内容给到调用方。
    return path.read_text(encoding="utf-8")

# 创建一个统计单词的函数，传递文本参数到text，返回的参数是dict字典，如：{"the":12,"or":9}
def count_words(text: str) -> dict[str, int]:
    """统计每个词出现的次数：统一小写、去掉首尾标点、跳过空串。"""
    # 先声明一个空的接收每个单词出现的次数的dict
    counts: dict[str, int] = {}
    # 循环读取文本中的每个单词，.split()就是把文本中的字符转换为数组的形式
    for raw in text.split():
        # 把读取到的字符使用.strip()去除掉首尾空格，并去除掉PUNCTUATION中的字符，然后把字符转换为小写
        # 先 strip 再 lower 是更标准的写法，顺序可以反过来。
        word = raw.strip(PUNCTUATION).lower()
        # 判断word是否为None
        # 如果把 if not word: continue 删掉，当你遇到 '...' 时，程序会执行：counts[''] = counts.get('', 0) + 1
        if not word:
            # 跳过当前循环
            continue
        # 先把word拿到的字符在counts中匹配，如果有就把对应的键的value + 1，如果没有就默认0。得到的结果赋值给counts的对应键
        # counts[word] += 1 会报错第一次出现的键根本就没有这个值。回报KeyError
        counts[word] = counts.get(word, 0) + 1
    # 返回counts
    return counts

# 创建一个取前n个的函数，传递counts和n，返回list的元组数据
def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """按次数从高到低取前 n 个；次数相同时按字母升序。"""
    # sorted对任何可迭代对象进行排序，默认从小到大，因为dict不能直接排序，需要转换为视图对象.items()，
    # 对这个字典里的所有键值对进行排序，先按次数的负数从小到大排（也就是次数从大到小），如果次数一样，就按字母从小到大排。
    # -kv[1]控制第一优先级：次数降序， kv[0]控制第二优先级：字母升序，当 key 返回一个元组时，Python 会执行“字典序比较”：
    ordered = sorted(counts.items(), key=lambda kv: (kv[-1], kv[0]))
    # 返回切片前n个
    return ordered[:n]

# 创建一个main的主函数，argv: list[str] 接收一个字符串列表作为参数，返回一个整数
# 不在各函数里读 sys.argv 核心业务逻辑，尽量写成纯粹的“输入 → 输出”
def main(argv: list[str]) -> int:
    """命令行入口：统一在这里解析参数、调用上面的函数、负责打印。"""
    # 判断用户是否传入了参数
    if not argv:
        # 控制台打印用法
        print("用法: python word_counter.py <文件> [--top N]")
        # 返回1
        return 1

    # argv[0] 就是用户输入的第一个参数传递给path
    path = Path(argv[0])
    # top的默认值10
    top = 10
    # 判断argv中是否存在--top这个参数
    if "--top" in argv:
        # 找到argv中--top的位置
        index = argv.index("--top")
        # 保 "--top" 后面确实跟着一个数字，防止用户只敲了 --top 没敲数字导致报错。
        if index + 1 < len(argv):
            # 把紧跟在 "--top" 后面的那个字符串（比如 "5"）转成整数 5，赋值给 top。
            top = int(argv[index + 1])

    # 把地址发送到读文件函数中，并text接收结果
    text = read_text(path)
    # 判断text是否为None
    if not text:
        # 控制台打印
        print(f"文件不存在或内容为空: {path}")
        # 返回结果1
        return 1

    # 把text接收到的结果给到count_words统计单词的次数
    counts = count_words(text)
    # 控制台打印counts的项目数量
    print(f"不同单词数: {len(counts)}")
    # 控制台打印 - 20次
    print("-" * 20)
    # 循环取top_n中的字典结果word为键，cnt为值。top_n就是把counts和top传递过去排序
    for word, cnt in top_n(counts, top):
        # 控制台打印word键 空格12个，cnt值
        print(f"{word:<12}{cnt}")

    # 返回0
    return 0

# python的标准入口
if __name__ == "__main__":
    # sys.argv 包含了运行时的所有参数，argv[1:]切片截取第一个参数及以后的
    sys.exit(main(sys.argv[1:]))

# 这个程序分成了 4 个函数，为什么 read_text 不直接打印，非要 main 来打印？
# 一个函数只做一件事儿

# 如果文本文件有 10 万行，read_text 一次全读进内存会有什么问题？可以怎么改？（提示：D3 学的逐行读）
# 内存会不够用，采用逐行遍历的方式读取文件中的内容

# 为什么 main 返回 0 / 1？返回给谁看？
# 返回给sys.exit，表示程序是否正常退出

# 如果我想加功能"只统计长度 ≥ 3 的词"，最应该改哪个函数？为什么不是 main？
# 改count_words函数，main函数只做基本的传参和打印。

# if __name__ == "__main__": 这一行，如果删掉会怎样？
# 防止被其他文件导入（import）时自动执行