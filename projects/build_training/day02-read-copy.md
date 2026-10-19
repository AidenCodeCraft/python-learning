# Day 2（10-21 三 晚）· 读 + 抄：把一份完整程序"吃透"

> **今晚任务**：读一份 65 行的完整程序 → 逐行注释 → 关掉参考手抄一遍 → 跑通。
> 时间：50~60 分钟。做完发我两份东西：**带注释的版本** + **手抄版能否跑通**。

参考实现 → [reference/word_counter.py](reference/word_counter.py)
示例数据 → [reference/sample.txt](reference/sample.txt)

---

## 第一步：跑起来（5 分钟）

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
cd projects\build_training\reference
python word_counter.py sample.txt --top 5
```

**预期输出（已实测）**：

```text
不同单词数: 22
--------------------
the         12
cat         5
dog         4
and         3
sea         3
```

再跑两个边界情况：

```powershell
python word_counter.py                # 预期：打印用法，返回码 1
python word_counter.py nope.txt       # 预期：文件不存在或内容为空，返回码 1
```

---

## 第二步：逐行注释（20 分钟）

把 `word_counter.py` 复制成 `my_word_counter_annotated.py`，然后**每一行代码上方**加一行注释，写清楚：

- 这行在干嘛
- 数据从哪来、到哪去
- **为什么这么写**（尤其是这几处，必须注释到位）：

| 位置 | 你要说清的问题 |
|---|---|
| `counts.get(word, 0) + 1` | 为什么不用 `counts[word] += 1`？（提示：第一次出现的词） |
| `raw.strip(PUNCTUATION).lower()` | 为什么先 strip 再 lower？顺序反过来行不行？ |
| `sorted(..., key=lambda kv: (-kv[1], kv[0]))` | `-kv[1]` 和 `kv[0]` 分别控制什么？为什么用元组？ |
| `if not word: continue` | 什么情况下 `word` 会是空串？ |
| `if not path.exists(): return ""` | 为什么不直接 `raise`？（对比 Day1 需求 3 的设计） |
| `main(argv)` 里统一解析参数 | 为什么不在各函数里读 `sys.argv`？ |

---

## 第三步：关掉参考，手抄一遍（20 分钟）

新建 `projects/build_training/my_word_counter.py`，**从零把整个程序敲一遍**：

- 允许**看**参考（卡住时瞄一眼）
- **禁止复制粘贴、禁止直接 copy 文件**
- 抄完必须能跑出和第一步**一模一样**的输出

> 为什么必须手抄：你现在的瓶颈不是"理解"，是"手和脑子没有建立这个程序的肌肉记忆"。
> 抄一遍的价值 ≈ 读三遍。

---

## 第四步：回答 5 个理解题（10 分钟，写在文件末尾注释里）

1. 这个程序分成了 4 个函数，**为什么 `read_text` 不直接打印，非要 `main` 来打印？**
2. 如果文本文件有 10 万行，`read_text` 一次全读进内存会有什么问题？可以怎么改？（提示：D3 学的逐行读）
3. 为什么 `main` 返回 0 / 1？返回给谁看？
4. 如果我想加功能"只统计长度 ≥ 3 的词"，**最应该改哪个函数**？为什么不是 `main`？
5. `if __name__ == "__main__":` 这一行，如果删掉会怎样？

---

## 提交格式

```text
【构建训练 Day2 · 读+抄】
1. 第一步跑通的输出（贴 5 行）
2. my_word_counter_annotated.py 的路径（或贴出来）
3. my_word_counter.py 跑通的输出
4. 5 个理解题的答案
5. 卡住的地方 / 我的思路
```

## 自检

- [ ] 三步输出都和"预期输出"一致
- [ ] 注释覆盖了 6 个关键位置
- [ ] 手抄版**没有复制粘贴**（我能看出来：变量名、注释风格会不一样）
- [ ] 5 个理解题都写了，哪怕答错
