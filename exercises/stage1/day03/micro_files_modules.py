# 练 1（编写）：写 count_lines(path: str) -> int
# 用 with open(path, encoding="utf-8") + for line in f 数行数
# 文件不存在 → 返回 0（用 try/except FileNotFoundError）

def count_lines(path: str) -> int:
    count = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                count += 1
    except FileNotFoundError:
        return 0
    return count

# 练 2（编写）：写 write_and_read(path: str, lines: list[str]) -> list[str]
# 把 lines 逐行写进文件（自己加 \n）
# 再读回来，返回去掉 \n 的列表
# 验证：write_and_read(".tmp/t.txt", ["a", "b"]) == ["a", "b"]

def write_and_read(path: str, lines: list[str]) -> list[str]:
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

print(write_and_read(".tmp/t.txt", ["a", "b"]))

# 练 3（改错）：下面这段有 2 个隐患，找出来并改对（提示：一个跟"关文件"有关，一个跟"中文"有关）
def read_all(path: str) -> str:
    # f = open(path, "r", encoding="utf-8")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # f.close()
    return text

# 练 4（模块）：
# 新建 file_utils.py，把练 1 的 count_lines 放进去；
# 给 file_utils.py 加上 if __name__ == "__main__": 自测块；
# 新建 use_utils.py，import file_utils 并调用它；
# 分别运行两个文件，观察自测块只在直接运行时才打印。