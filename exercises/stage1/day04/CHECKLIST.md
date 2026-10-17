# D4 收尾核销表（2026-10-17 · 周六）· 教练复核版

> **机制**：本表由**教练复核时打勾**。你只需看"未勾项 = 返工清单"。
> **复核时间：2026-10-17 13:20（第二次复核，教练实测）**。

## 一、当天学习产出

- [x] 档① 4 题 —— `check` 四处全 True ✅
- [x] 档② 6 题 —— 全部正确 ✅
- [x] 档③ 10 题 —— ex11–ex18 全对、ex20 六个预测全 True；**ex19 三个函数逻辑对、自测 print 也补上了** ✅（剩一个小瑕疵见返工表 5）
- [ ] 微课 6 题 —— **B2 已跑通** ✅、**A1 已修** ✅、A3④ 已修 ✅；**A2 仍坏、A3③ 仍错**（4.5 / 6）
- [x] "四、自检清单"逐题对过 ✅

## 二、文件回填

- [x] `demo_reference.py` 四处改动完成并跑过 ✅
- [x] `day04.py` 每个 `check(...)` 都填了预测值（全 True）✅
- [x] 类型注解完整 ✅

## 三、复盘

- [x] `mistakes/2026-10-17.md` 已写（教练代笔）
- [ ] 合上错题本，把"自测 5 问"用嘴答一遍 ← 教练无法代验
- [ ] README"今日验收标准"8 条 —— 微课那条还差 2 处

## 四、环境与提交

- [ ] `git add` / `commit`（工作区还有 9 个文件）
- [ ] `git push`（本地比 origin 超前 2 个提交）
- [ ] `git status` 干净

## 五、交给教练

- [x] 提交检查

---

## 六、返工清单（只剩 4 项，约 5 分钟）

| # | 项 | 怎么改 |
|---|---|---|
| 1 | 微课 **A2 · `load_json` 仍返回 None** | 你现在是：`try: with open(...) as f: loaded = json.load(f); if not load_json: return None` —— ①`if not load_json` 判断的是**函数对象**（恒为真），②**没有 `return loaded`**。<br>正解：`try: with open(...) as f: return json.load(f)` + `except FileNotFoundError: return None` |
| 2 | 微课 **A3 · ③ 仍错** | 正确答案是 **`{'a': [1, 2]}`**（外层还是 dict，只有元组变 list），不是 `['a', [1, 2]]` |
| 3 | 根目录 `exercises.py` | 删掉：`git rm exercises.py` |
| 4 | 提交 | 拆两条：`fix(stage1): day04 微课 A2/A3 修正` / `chore: 清理临时文件` |

### 为什么 A2 又漏了？—— 同一个病

`micro_json.py` 直接运行**没有任何输出** —— 说明 A1/A2 从来没被**调用**过。
你修了 `try/except` 却没加 `return loaded`，就是因为没有一行代码去用这个函数。

**把文件末尾加上这 3 行，以后它自己会告诉你对不对**：

```python
if __name__ == "__main__":
    print("A1:", to_json({"name": "汤姆"}))
    save_json(".tmp/chk.json", {"a": 1})
    print("A2:", load_json(".tmp/chk.json"), load_json(".tmp/nope.json"))
    # 期望： A1: {"name": "汤姆"}     A2: {'a': 1} None
```

> 小瑕疵（不算错）：`ex19_fix_errors() -> str` 现在靠 `print` 自测，但**返回的还是 `None`**。要么改成 `-> None`，要么把 "3/3 通过" 当字符串返回。

## 关账标准

上表 1–4 完成 → 教练复核 → **D4 通过，D5（周日 6h：pytest + async 认知 + `todo_cli` 项目 + 阶段 1 验收）开始**。
