# D5 收尾核销表（2026-10-18 · 周日）· 阶段 1 验收

> **机制**：本表由**教练复核时打勾**。你只需看"未勾项 = 返工清单"。
> **今天是阶段 1 最后一天：下表全绿 = 阶段 1 通过 → 10-19 进入阶段 2。**

## 零、先清 D4 的尾巴（10 分钟）

- [ ] `exercises/stage1/day04/micro_json.py` 的 A3 ③ 注释：`['a', [1, 2]]` → **`{'a': [1, 2]}`**
- [ ] 删掉根目录临时文件：`git rm exercises.py`
- [ ] 把 D4 剩余改动提交（`micro_json.py` / `micro_oop.py` / `variants.py` / `mistakes/2026-10-17.md` / 两张 CHECKLIST）
- [ ] （可选）`ex19_fix_errors` 的返回类型：`-> str` 却返回 `None` → 改成 `-> None` 或真的返回字符串

## 一、pytest

- [ ] `demo_pytest.py` 跑过，知道 FAILED 长什么样（`2 failed, 4 passed`）
- [ ] `test_practice.py` 3 题：`test_pipeline_flow` / `test_raises_keyerror` / `test_file_roundtrip(tmp_path)`
- [ ] 能说清：`assert` 怎么用、`pytest.raises` 干什么、`tmp_path` 是什么

## 二、项目 `todo_cli`

- [ ] `todo.py` 10 个 TODO 全部实现（`to_dict` / `from_dict` / `__str__` / `load` / `save` / `_next_id` / `add` / `list_items` / `done` / `delete`）
- [ ] `cli.py` 的 `main`（TODO 11）实现
- [ ] 三个命令跑通：`add` / `list`（含 `--which`）/ `done` / `delete`
- [ ] 数据真的落盘：删掉 `.tmp/todo.json` 再 `list` 是空的；`add` 之后重启还能看到
- [ ] `done 999` / `delete 999` 不崩，给提示并 return 1
- [ ] `todo.py` + `cli.py` 合计 **100~150 行有效代码**（骨架 86 行，填完约 120~140；不含空行/注释/docstring）
- [ ] 没有裸 `except:`；类型注解完整

## 三、pytest（项目）

- [ ] `python -m pytest -v` → **4 passed**（示范 1 + 自己写 3）
- [ ] 测试用的是 `tmp_path`，**没有往真实 `.tmp/todo.json` 写测试数据**

## 四、async 认知

- [ ] 能回答 3 个问题：解决"算得快"还是"等时别干等"？纯计算会不会变快？FastAPI 为什么常写 `async def`？
- [ ] 能说清 async ≠ 锁（纠正阶段 0 第 7 题的错误模型）

## 五、8 类异常（现场验收）

- [ ] `NameError` / `TypeError` / `IndexError` / `KeyError` / `ValueError` / `IndentationError` / `ImportError` / `AttributeError` —— 看代码能说出哪个
- [ ] 教练随机抽 4 个，**现场改对**（不是背名字）

## 六、口述 6 条（合上所有文件说）

- [ ] 1. 可变/不可变、别名/浅拷贝/deepcopy
- [ ] 2. 默认参数陷阱 + `None` 占位
- [ ] 3. `and`/`or` 返回操作数本身
- [ ] 4. 循环三问
- [ ] 5. 类属性 vs 实例属性
- [ ] 6. async 解决什么问题

## 七、复盘与提交

- [ ] `mistakes/2026-10-18.md`（或直接归档到 D1–D4 的四本错题本里）
- [ ] 项目 README 补上"怎么跑 + 四个命令示例输出"（当作 PR 描述练手）
- [ ] `git add .` + commit（`feat(stage1): todo_cli 项目 + pytest + 阶段 1 验收`）
- [ ] `git push`（网络通了补推全部积压）
- [ ] `git status` 干净

---

## 阶段 1 通过线（教练判定）

| # | 硬指标 |
|---|---|
| 1 | `pytest` **4 passed** |
| 2 | 四个命令真能跑，数据真能持久化 |
| 3 | `todo.py` + `cli.py` 100~150 行 |
| 4 | 8 类异常抽 4 个**现场改对** |
| 5 | 口述 6 条说得出 |
| 6 | Git 提交规范 |

**全绿 → 阶段 1 通过**（10-19 进入阶段 2：SQL + PostgreSQL + Redis）。
任一未过 → 阶段 2 前半天补（止损开关见 [03-阶段1节奏修订](../../../notes/03-阶段1节奏修订.md)）。
