# 阶段 1 · 第 4 天（2026-10-17 · 周六 6h）· 函数与容器

> **主题：函数 / 作用域 / 默认参数陷阱 / 类型注解 / list·tuple·dict·set·str / 推导式**
> 为什么是它？**阶段 1 最重的一天**。后面所有代码都是"函数 + 容器"的组合体：
> FastAPI 的接口函数、Pydantic 模型的字段、SQLAlchemy 查询结果、Redis 的 hash —— 全是今天这些东西。
>
> 另外今天要补两门 D5 前置微课：**JSON** 和 **OOP 基础**（见 [micro_json_oop.md](micro_json_oop.md)）。

---

## 今日目标

1. 会用**位置参数 / 关键字参数 / 默认参数**，并说清"多返回值其实是元组"。
2. 能解释**作用域**：函数里为什么"能读全局、一赋值就报 `UnboundLocalError`"。
3. 复述**默认参数陷阱**，并知道它和 D1 的"别名"是同一个原理。
4. 分清 **list / tuple / dict / set** 的特性与使用场景。
5. 写出 **list / dict / set 推导式**，并知道什么时候**不该**用推导式。
6. 会给函数和容器写**类型注解**（含 `X | None`）。

> ⚠️ **今天的核心纪律**：所有预测用 `check()` 打印"对上了吗"。
> D2/D3 各有 3 处"预测写完不核对"，从 D4 起用机器替你核对。

---

## 时间分配（周末 6h）

| 时段 | 分钟 | 做什么 |
|---|---:|---|
| 复习 | 20 | D3 错题本"自测 5 问" + 循环三问 |
| 讲解 + demo | 60 | 读"二、讲解"，把 `demo_reference.py` 每段**先预测再运行** |
| 练习 | 180 | `day04.py` 20 题（档①→②→③） |
| 微课 | 75 | JSON + OOP 基础 → [micro_json_oop.md](micro_json_oop.md) |
| 复盘 | 25 | 对自检清单 + `mistakes/2026-10-17.md` + 提交 |

> 中文乱码先 `chcp 65001`。

---

## 一、间隔复习（来自 D3 错题本）

1. **循环三问**是哪三问？
2. 求 1~n 的和，累加器写在哪？循环变量能不能拿来累加？
3. `count_vowels` 应该遍历什么？为什么遍历元音表是错的？
4. `find_first` 为什么不能 `return 1`？怎么自己发现这种错？
5. 跑完程序后，除了看输出，还要做哪一件事？

<details>
<summary>想完再看答案</summary>

1. 遍历什么（数据源）、攒到哪儿（累加器）、从哪到哪（边界）。
2. 累加器是循环**外面**的 `total = 0`，循环里 `total += i`；循环变量只管走到哪，改它没用。
3. 遍历 **`s`**，用 `in` 拿元音表做判断；遍历元音表的话结果永远和输入无关。
4. 因为返回的是"只对当前测试数据成立"的常量；**换一组数据跑一遍**就能发现。
5. **逐行对着预测读输出**，对不上的当场改 + 记错题本（今天用 `check()` 自动做这件事）。

</details>

---

## 二、讲解 + 示例（60 分钟）

### 要点 1：函数的四种参数

```python
def greet(name: str, greeting: str = "你好") -> str:
    return greeting + ", " + name

greet("Tom")                  # 位置参数
greet(name="Tom")             # 关键字参数
greet("Tom", greeting="Hi")   # 混合（位置参数必须在关键字参数前面）
```

**返回值**：`return a, b` 返回的是一个**元组**，`low, high = min_max(nums)` 是**解包**（D1 的元组解包）。

```python
def min_max(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)

low, high = min_max([3, 1, 9])   # 1 9
```

### 要点 2：默认参数陷阱（D1 学过的"别名"，换了个马甲）

```python
def bad(tag: str, tags: list[str] = []) -> list[str]:   # ← [] 只在定义时造一次
    tags.append(tag)
    return tags
```

`bad("a")` → `['a']`，`bad("b")` → **`['a', 'b']`**（两次调用共享同一个列表）。
原因就是 D1 那句：**可变对象的"改" = 改对象**，而 `tags` 一直指向定义时造的那个列表。

```python
def good(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```

**规则：默认值永远不要用可变对象**（`[]` `{}` `set()`），用 `None` 占位。

### 要点 3：作用域 —— 能读全局，一赋值就变局部

```python
counter = 0

def read_it() -> int:
    return counter          # ✅ 能读全局

def bump_bad() -> None:
    counter = counter + 1   # ❌ UnboundLocalError

def bump_good() -> None:
    global counter          # 声明"我要改全局的"
    counter += 1
```

**规则**：函数里只要**给某个名字赋值**，这个名字就变成**局部变量**（不管外面有没有同名的）。
所以 `counter = counter + 1` 会先读右边 → 但右边那个 `counter` 已经被判定为局部、还没赋值 → 报错。

> 实战建议：**别用 `global`**，改成"传进去、返回出来"：
> `counter = bump(counter)`。

### 要点 4：把 list 传进函数，会被"就地改"

```python
def append_item(items: list[int]) -> None:
    items.append(99)        # 就地改 → 调用方的列表也变了

def rebind_item(items: list[int]) -> None:
    items = items + [99]    # 造新列表，重新绑定 → 调用方不受影响
```

又是 D1 的"**改对象 vs 换指向**"。**要改调用方的数据就地改；不想动它就 `items = items + [...]` 或 `items.copy()`。**

### 要点 5：容器四件套对照

| 容器 | 写法 | 有序 | 可变 | 能重复 | 查找 | 典型用途 |
|---|---|---|---|---|---|---|
| `list` | `[1, 2]` | ✅ | ✅ | ✅ | 按**下标** | 顺序数据、队列 |
| `tuple` | `(1, 2)` | ✅ | ❌ | ✅ | 按**下标** | 不变的组合（多返回值、坐标） |
| `dict` | `{"a": 1}` | ✅(3.7+) | ✅ | key 不重复 | 按 **key** | 映射、计数、结构化数据 |
| `set` | `{1, 2}` | ❌ | ✅ | ❌ | 按**值**（O(1)） | 去重、交并差 |

### 要点 6：list 常用方法 + 切片

```python
nums = [3, 1, 4, 1, 5]
nums.sort()            # 就地排序（改自己，返回 None！）
sorted(nums)           # 返回新列表（不改原列表）
nums.append(9)         # 尾部加一个
nums.extend([7, 8])    # 尾部加一批
nums.remove(1)         # 删第一个等于 1 的
nums.pop()             # 弹出最后一个
nums[1:3]              # 切片：下标 1、2
nums[::-1]             # 反转
nums[:2]               # 前两个
```

> ⚠️ `nums.sort()` 返回 **`None`**（就地排），`x = nums.sort()` 会让 `x` 变成 `None`。
> 要新列表用 `sorted(nums)`；要字符串排序/对象排序用 `sorted(items, key=..., reverse=True)`。

### 要点 7：dict 三件套 + 合并

```python
user = {"id": 1, "name": "Tom"}
user.get("age")            # None（不存在不报错）
user.get("age", 0)         # 0（给默认值）← 计数时必用
user.keys() / values() / items()
{**user, "age": 18}        # 合并（后面的键覆盖前面的）
```

**计数模板**（今天 ex13 要用）：

```python
counts: dict[str, int] = {}
for w in text.split():
    counts[w] = counts.get(w, 0) + 1
```

### 要点 8：set 去重与集合运算

```python
set([1, 2, 2, 3])      # {1, 2, 3}
a & b                  # 交集
a | b                  # 并集
a - b                  # 差集
```

**去重 + 排序一行搞定**：`sorted(set(items))`。

### 要点 9：str 常用 + 切片

```python
"  hi  ".strip()             # 'hi'
"a,b,,c".split(",")          # ['a', 'b', '', 'c']
"-".join(["a", "b"])         # 'a-b'
"abc".replace("a", "x")      # 'xbc'
s[1:4] / s[::-1]             # 切片 / 反转
```

### 要点 10：推导式

```python
[n * n for n in range(5)]                 # 列表推导式
[n for n in range(10) if n % 2 == 0]      # 带条件
{n: n * n for n in range(1, 4)}           # 字典推导式
{n % 5 for n in range(10)}                # 集合推导式
```

**什么时候别用**：推导式里塞了嵌套循环 + 多个条件 → 可读性崩了，老老实实写 `for`。

### 要点 11：类型注解（公司规范要求）

```python
def stats(nums: list[int]) -> tuple[int, int, float]: ...
def find(users: dict[str, int], name: str) -> int | None: ...
def add(tag: str, tags: list[str] | None = None) -> list[str]: ...
```

三种最常见的："列表 `list[T]`""字典 `dict[K, V]`""可能没有 `T | None`"。

### 要点 12：`sorted` + `key=lambda`（阶段 0 小任务的重现）

```python
tasks = [{"id": 1, "p": 3}, {"id": 2, "p": 9}]
sorted(tasks, key=lambda t: t["p"], reverse=True)
```

`key=lambda t: t["p"]` 的意思是"**按这一项排序**"；`reverse=True` 是从大到小。

### 示例代码

→ [demo_reference.py](demo_reference.py)（**先预测再运行**）

```powershell
cd D:\Program\Python\python-learning
.\.venv\Scripts\Activate.ps1
chcp 65001
python exercises\stage1\day04\demo_reference.py
```

---

## 三、练习（180 分钟，共 20 题）

> 档① 4 题 → 档② 6 题 → 档③ 10 题，上一档没过不许跳。
> **档① 的预测填进 `check(...)` 的第三个参数**，跑完看"对上了吗"是不是 True。

### 档① 读改（改 `demo_reference.py`，预测填进 `day04.py` 的 `check`）

**1.** `ex01`：把 `add(a, b=10)` 改成 `b=100`，预测 `add(1)` 和 `add(1, 2)`。
**2.** `ex02`：取消 `counter = counter + 1` 的注释，预测抛什么异常。
**3.** `ex03`：把 `items = items + [99]` 改成 `items.append(99)`，预测 `data2`。
**4.** `ex04`：给 `[n * n for n in range(5)]` 加条件 `if n % 2`，预测结果。

### 档② 填空（6 题，改 `day04.py` 里的 TODO）

**5.** `ex05`：改默认值，让 `greet("Tom")` → `你好, Tom`。
**6.** `ex06`：让 `min_max` 真的返回 `(最小值, 最大值)`。
**7.** `ex07`：让 `user.get("age")` 输出 `0`。
**8.** `ex08`：让 `[3, 1, 2, 3, 1]` 输出 `[1, 2, 3]`（去重 + 升序）。
**9.** `ex09`：用切片让 `"abcd"` 输出 `dcba`。
**10.** `ex10`：把 3 行循环改成**一行列表推导式**，结果仍是 `[2, 4, 6]`。

### 档③ 默写（10 题）

| 题 | 函数 | 要求 |
|---|---|---|
| 11 | `repeat(s, times=2)` | `repeat("ab")` → `"abab"`；`repeat("x", 3)` → `"xxx"` |
| 12 | `stats(nums)` | 返回 `(min, max, 平均)`；`stats([1,2,3,4])` → `(1, 4, 2.5)`；空列表 → `(0, 0, 0.0)` |
| 13 | `count_words(text)` | `count_words("a b a")` → `{"a": 2, "b": 1}`（用 `get` 计数） |
| 14 | `unique_sorted(items)` | `[3, 1, 3, 2]` → `[1, 2, 3]` |
| 15 | `merge(a, b)` | `b` 的同名键覆盖 `a` |
| 16 | `top_n(scores, n)` | 按分数**从高到低**取前 n 个**名字**（`items` + `key=lambda` + 切片） |
| 17 | `comprehensions(nums)` | 一次用三个推导式返回 `(偶数平方 list, 值→平方 dict, 取余5 set)` |
| 18 | `get_path(data, path, default)` | 按 `"a.b.c"` 取值，任一层缺失返回 default |
| 19 | **改错题** | 3 个函数各有 1 处错（默认参数 / 假复制 / `return` 位置） |
| 20 | **读代码说结果题** | 6 个预测，填进 `check`（含默认参数陷阱、作用域、推导式、切片、就地修改） |

### 知识点覆盖对照

| 知识点 | 讲解 | 示例 | 编写题 | 读代码说结果 | 改错题 | 变式题 |
|---|---|---|---|---|---|---|
| 函数参数 / 多返回值 | 要点 1 | demo 1 段 | 5, 6, 11, 12 | 20-2 | 19 | 批改时给 |
| 默认参数陷阱 | 要点 2 | demo 2 段 | 19 | 20-1 | **19** | 同上 |
| 作用域 | 要点 3 | demo 3 段 | 2 | 20-2 | — | 同上 |
| 就地改 vs 换指向 | 要点 4 | demo 4 段 | 3 | 20-6 | 19 | 同上 |
| list / tuple | 要点 5, 6 | demo 1, 5 段 | 8, 9, 14 | 20-5 | — | 同上 |
| dict | 要点 7 | demo 6 段 | 7, 13, 15, 16 | 20-4 | — | 同上 |
| set | 要点 8 | demo 7 段 | 8, 14 | — | — | 同上 |
| str | 要点 9 | demo 8 段 | 9, 13 | 20-5 | — | 同上 |
| 推导式 | 要点 10 | demo 9 段 | 4, 10, 17 | 20-3, 20-4 | — | 同上 |
| 类型注解 | 要点 11 | 全文 | 全部 | — | — | 同上 |
| `sorted` + lambda | 要点 12 | — | 16 | — | — | 同上 |
| 嵌套 dict | — | — | 18 | — | — | 同上 |

---

## 四、自检清单（预期输出，已用参考实现核对）

**`demo_reference.py` 的输出**：

```text
1-a: 11 3 6          1-b: 1 9 (1, 9)
2-a: ['a']           2-b: ['a', 'b']        2-c: ['a']      2-d: ['b']
3-a: 0               3-b: （提示行）
4-a: [1, 2, 99]      4-b: [1, 2]
5-a: [1, 1, 3, 4, 5] [3, 1, 4, 1, 5]        5-b: [1, 1, 3, 4, 5]
5-c: [1, 3] [5, 4, 3, 1, 1] [1, 1]
6-a: None 0          6-b: ['id', 'name'] [1, 'Tom']
6-c: {'id': 1, 'name': 'Tom', 'age': 18}     6-d: True False
7-a: {1, 2, 3}       7-b: {2, 3} {1, 2, 3, 4} {1}
8-a: 'hello world'   8-b: ['hello', 'world']  8-c: a-b-c    8-d: ['a', 'b', '', 'c']
9-a: [0, 1, 4, 9, 16]  9-b: [0, 2, 4, 6, 8]    9-c: {1: 1, 2: 4, 3: 9}   9-d: {0, 1, 2}
10-a: 1 None
```

**20 题的预期结果**：

| 题 | 预期 | 关键点 |
|---|---|---|
| 1 | `add(1)` = **101**、`add(1, 2)` = **3** | 默认值只在"没传"时生效 |
| 2 | `UnboundLocalError` | 函数里赋值 → 名字变局部 |
| 3 | `data2` = **`[1, 2, 99]`** | `append` 就地改，会影响调用方 |
| 4 | **`[1, 9]`** | `x % 2` 为真的是 1、3 → 1、9 |
| 5 | `你好, Tom` | — |
| 6 | `1 9` | 多返回值 = 元组 |
| 7 | `0` | `get` 的第二个参数是默认值 |
| 8 | `[1, 2, 3]` | `sorted(set(nums))` |
| 9 | `dcba` | `s[::-1]` |
| 10 | `[2, 4, 6]` | `[n for n in range(1, 7) if n % 2 == 0]` |
| 11 | `abab xxx` | `s * times` |
| 12 | `(1, 4, 2.5) (0, 0, 0.0)` | 空列表要先判 |
| 13 | `{'a': 2, 'b': 1}` | `counts.get(w, 0) + 1` |
| 14 | `[1, 2, 3]` | 去重 + 升序 |
| 15 | `{'x': 9, 'y': 2}` | `{**a, **b}` |
| 16 | `['Bob', 'Tom']` | `sorted(items, key=lambda kv: kv[1], reverse=True)` |
| 17 | `([4, 16], {1: 1, 2: 4, 3: 9, 4: 16}, {1, 2, 3, 4})` | 三个推导式 |
| 18 | `1 None 缺失` | `path.split(".")` + `isinstance(cur, dict)` |
| 19 | 见函数 docstring（`add_tag` 不累积 / `copy_tags` 真复制 / `first_even([1,3])` → `-1`） | 3 处错各 1 个概念 |
| 20 | `[[1, 2], [1, 2]]` / `10` / `[2, 6]` / `{'bb': 2, 'ccc': 3}` / `('ell', 'olleh')` / `([1, 0], [1, 0])` | 20-1 和 20-6 是同一个陷阱的两种面孔（共享对象） |

---

## 五、复盘

1. 新建 `mistakes/2026-10-17.md`（现象 → 概念层错因 → 正确写法 → 变式）。
2. 微课 75 分钟 → [micro_json_oop.md](micro_json_oop.md)（JSON + OOP 基础）。
3. [CHECKLIST.md](CHECKLIST.md)：**清单由教练打勾**，你只需看"未勾项"。
4. 提交：

```powershell
git add .
git commit -m "feat(stage1): day04 函数与容器 20 题 + JSON/OOP 微课"
```

---

## 六、提交格式

```text
【阶段1 D4 提交】
1. 档① 四题：check 输出里"对上了吗"全 True 吗？哪几处是 False？
2. 档② 六题：你改成了什么（改前 → 改后）
3. 档③ 第 11~18 题的代码
4. 第 19 题：3 处错分别是什么 + 正确版本
5. 第 20 题：6 个预测
6. self-check 对不上的题号
7. 微课：JSON 3 题 + OOP 3 题
8. git log --oneline
9. 卡住点 / 我的思路
```

---

## 今日验收标准

- [ ] 说清位置/关键字/默认参数，知道多返回值是元组
- [ ] 能解释 `UnboundLocalError` 是怎么来的
- [ ] 默认参数陷阱能当场复现并改正
- [ ] 分清 list/tuple/dict/set，会 `sorted(set(x))`、`get` 计数、`{**a, **b}`
- [ ] 会写 list/dict/set 推导式
- [ ] 20 题的 `check` 输出里"对上了吗"**全 True**
- [ ] 微课 6 题完成
- [ ] Git 已提交
