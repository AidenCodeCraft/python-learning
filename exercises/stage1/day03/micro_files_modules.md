# D3 微课 · 文件读写 + 模块与包（45 分钟）

> **为什么放在今天**：循环 + 文件是天生一对（**逐行读文件**）。
> 原计划里这一节属于 D5；[03-阶段1节奏修订](../../../notes/03-阶段1节奏修订.md) 把它前置到 D3，10-18 那天才装得下项目 + 验收。
>
> 本课只学"够用"：读写文本文件 + 会拆模块。JSON、异常体系、pytest 分别放在 D4 / D5。

---

## 1. 打开文件的唯一正确姿势

```python
with open(".tmp/data.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

三件事必须同时做到：

| 要素 | 为什么 |
|---|---|
| `with` | 出了代码块**自动关闭文件**，哪怕中间抛异常 |
| `encoding="utf-8"` | Windows 默认用 GBK 读文件，中文会乱码或直接 `UnicodeDecodeError` |
| 模式字符串 | `"r"` 读 / `"w"` 写（**会清空原文件**）/ `"a"` 追加 |

> 测试文件请写到 `.tmp/` 目录下（已在 `.gitignore` 里，不会被提交）。

---

## 2. 三种读法，先会用第三种

```python
# ① 一次全读成字符串（文件小的时候用）
with open(".tmp/a.txt", encoding="utf-8") as f:
    text = f.read()

# ② 读成列表，每行末尾带 "\n"
with open(".tmp/a.txt", encoding="utf-8") as f:
    lines = f.readlines()

# ③ 逐行遍历（推荐：省内存，能处理大文件）
with open(".tmp/a.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())      # strip() 去掉行尾的 \n 和空格
```

**记住**：`readlines()` 和 `for line in f` 拿到的行**都带 `\n`**，处理前先 `strip()`。

---

## 3. 写文件

```python
with open(".tmp/out.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
```

两个坑：

1. **`write()` 不会自动换行** —— 要自己写 `\n`。
2. **`"w"` 模式会清空已有内容** —— 想追加用 `"a"`。

---

## 4. 路径：相对路径是相对"当前工作目录"

```python
import os
from pathlib import Path

print(os.getcwd())                  # 当前工作目录（你敲 python 命令的地方）
print(Path(__file__).parent)        # 当前脚本所在目录
```

**踩坑场景**：在项目根目录敲 `python exercises/stage1/day03/demo.py`，脚本里的 `".tmp/a.txt"` 指的是**项目根下的 `.tmp/`**，不是脚本旁边的。
→ 要拿"脚本旁边的文件"，用 `Path(__file__).parent / "a.txt"`。

---

## 5. 会遇到的异常

| 场景 | 异常 |
|---|---|
| 读一个不存在的文件 | `FileNotFoundError` |
| 编码写错了（比如没写 utf-8 读中文） | `UnicodeDecodeError` |
| 文件被别的程序占用 | `PermissionError` |

```python
try:
    with open(".tmp/maybe.txt", encoding="utf-8") as f:
        text = f.read()
except FileNotFoundError:
    text = ""          # 兜底
```

---

## 6. 模块：把自己的代码拆成文件

**`math` 这种是标准库模块**，用法：

```python
import math                     # 用的时候写 math.sqrt(9)
import math as m                # 别名
from math import sqrt           # 直接 sqrt(9)
```

**自己写模块**：新建 `file_utils.py`，然后在别的文件里 `import file_utils`，用 `file_utils.count_lines(...)`。
**注意**：`import` 找的是**当前目录**和 `sys.path` 里的路径 —— 所以两个文件要放同一目录，或在项目根目录运行。

**包**：一个**目录** + 里面一个 `__init__.py` 就是包，例如 `utils/` + `utils/file_utils.py` → `from utils.file_utils import count_lines`。

### `if __name__ == "__main__":` 到底干嘛的

```python
# file_utils.py
def count_lines(path: str) -> int:
    ...


if __name__ == "__main__":
    # 只有"直接运行这个文件"时才执行；被 import 时不执行
    print(count_lines(".tmp/a.txt"))
```

没有这个保护，别人 `import file_utils` 时会**顺手把你的测试代码跑一遍** —— 这是新手最常见的坑之一。

---

## 7. 45 分钟练习（4 题）

**练 1（编写）**：写 `count_lines(path: str) -> int`
- 用 `with open(path, encoding="utf-8")` + `for line in f` 数行数
- 文件不存在 → 返回 `0`（用 `try/except FileNotFoundError`）

**练 2（编写）**：写 `write_and_read(path: str, lines: list[str]) -> list[str]`
- 把 `lines` 逐行写进文件（**自己加 `\n`**）
- 再读回来，返回**去掉 `\n`** 的列表
- 验证：`write_and_read(".tmp/t.txt", ["a", "b"]) == ["a", "b"]`

**练 3（改错）**：下面这段有 **2 个隐患**，找出来并改对（提示：一个跟"关文件"有关，一个跟"中文"有关）

```python
def read_all(path: str) -> str:
    f = open(path, "r")
    text = f.read()
    f.close()
    return text
```

**练 4（模块）**：
1. 新建 `file_utils.py`，把练 1 的 `count_lines` 放进去；
2. 给 `file_utils.py` 加上 `if __name__ == "__main__":` 自测块；
3. 新建 `use_utils.py`，`import file_utils` 并调用它；
4. 分别运行两个文件，观察自测块**只在直接运行时**才打印。

<details>
<summary>想完再看答案（练 3）</summary>

1. **没用 `with`**：如果 `read()` 抛异常，`f.close()` 永远执行不到 → 文件句柄泄漏。改成 `with open(...) as f:`。
2. **没写 `encoding="utf-8"`**：Windows 上默认按 GBK 解码，读中文文件会乱码或抛 `UnicodeDecodeError`。

```python
def read_all(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```

</details>

---

## 8. 写完后

把这 4 题写进 `exercises/stage1/day03/micro_files_modules.py`（练 1/2/3 放在这里），`file_utils.py` / `use_utils.py` 放在同目录。
别忘了在 [CHECKLIST.md](CHECKLIST.md) 里给微课打勾。
