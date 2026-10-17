"""待办清单 · 命令行入口

用法（在 projects/stage1/todo_cli/ 目录下运行）：
    python cli.py add "写代码" --priority 1
    python cli.py list
    python cli.py list --which done
    python cli.py done 1
    python cli.py delete 1
"""

from __future__ import annotations

import sys

from todo import TodoStore

USAGE = """用法:
  python cli.py add <标题> [--priority 1|2|3]
  python cli.py list [--which all|todo|done]
  python cli.py done <id>
  python cli.py delete <id>"""


def main(argv: list[str]) -> int:
    """TODO 11：解析 argv 并分发到 TodoStore。

    argv 是 sys.argv[1:]（不含脚本名）。要求：
      - 没有子命令 / 未知子命令 → 打印 USAGE，return 1
      - add 成功 → 打印 `已添加 #<id> <标题>`
      - list → 每条打印一行（直接用 str(todo)）；空列表打印 `（没有待办）`
      - done / delete 成功 → 打印成功信息；id 不存在 → 打印提示并 return 1
      - 所有命令结束时 return 0

    提示：可以用 argparse（见 projects/stage1/todo_cli/README.md 提示 3），
          也可以手动判断 argv[0]。别在这里读写 JSON —— 那是 TodoStore 的活。
    """
    raise NotImplementedError("TODO 11: 实现 main")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
