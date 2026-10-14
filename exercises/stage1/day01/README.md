# 阶段 1 · 第 1 天（2026-10-14）· Python 的对象模型

> **主题：名字绑定、可变/不可变、别名与复制**
> 为什么是它？你在阶段 0 第 2 题答成 `a=[1,2,3]`、`b=[1,2,3,4]`（正确是两者都是 `[1,2,3,4]`）。
> 这个洞不补，后面的**默认参数陷阱、浅拷贝、ORM 对象复用、FastAPI 请求体**全是坑。

---

## 今日目标

完成之后你能做到：

1. 说清 `x = 10` 到底发生了什么（**不是**把 10 放进盒子）。
2. 说出哪些类型可变、哪些不可变，并解释为什么。
3. 说清 `b = a` 和 `b = a.copy()` 的区别，以及各自什么时候用。
4. 解释"浅拷贝陷阱"，并知道怎么绕开。
5. 用**同一套原理**解释阶段 0 第 3 题的默认参数陷阱。

---

## 时间分配（工作日 2 小时）

| 时段 | 分钟 | 做什么 |
|---|---:|---|
| 复习 | 0–15 | 做下面"一、间隔复习" |
| 讲解 | 15–40 | 读"二、讲解"，**并把 `demo_reference.py` 亲手跑一遍** |
| 练习 | 40–100 | 做"三、练习"的 10 题（按档位走） |
| 复盘 | 100–120 | 对"四、自检清单" + 写错题本 + Git 提交 |

> 上班时间：只看"二、讲解"和 `demo_reference.py`，练习留到晚上。

---

## 一、间隔复习（15 分钟，先自己说，再看答案）

1. `def f(x, acc=[])` 为什么会出问题？正确写法是什么？
2. `sorted(tasks, key=lambda t: t["priority"], reverse=True)` 每个部分是什么意思？
3. 下面各抛什么异常？
   - `[1, 2][5]`
   - `int("abc")`
   - `{"a": 1}["b"]`
   - `1 + "a"`
   - `10 / 0`
4. Git 从初始化到看到历史，命令顺序是什么？

<details>
<summary>想完再看答案</summary>

1. `[]` 只在**函数定义时**创建一次，所有调用共享同一个列表 → 会累积。改成 `acc=None`，函数内 `if acc is None: acc = []`。
2. `sorted` 返回新列表不改原列表；`key` 指定"按什么排序"；`lambda t: t["priority"]` 是把每个任务映射成它的 priority；`reverse=True` 表示从大到小。
3. `IndexError` / `ValueError` / `KeyError` / `TypeError` / `ZeroDivisionError`。
4. `git init` → `git add .` → `git commit -m "..."` → `git log --oneline`

</details>

---

## 二、讲解 + 示例（25 分钟）

### 要点 1：变量是**名字**，不是盒子

C 里 `int x = 10;` 是"在内存里开一个盒子 x，把 10 放进去"，`x = 20` 是**改盒子里的内容**。

Python 里 `x = 10` 是"**造一个对象 10，然后让名字 x 指向它**"，`x = 20` 是"**让 x 改指向另一个对象 20**"。原来那个 10 一直没变，只是没人指着它了。

```python
x = 10
print(id(x))    # 某个地址 A
x = 20
print(id(x))    # 另一个地址 B —— 证明是"换指向"，不是"改内容"
```

`id()` 返回对象在内存里的身份号。**id 一样 = 同一个对象。**

### 要点 2：不可变对象 vs 可变对象

| 不可变（immutable） | 可变（mutable） |
|---|---|
| `int` `float` `bool` `str` `None` `tuple` `frozenset` | `list` `dict` `set` `bytearray` |

- **不可变**：对象一旦造出来，内容就改不了。你写的"修改"其实是**造了个新对象**。
  ```python
  s = "abc"
  s2 = s
  s = s + "d"     # 造了新字符串 "abcd"，s 指向它；s2 还指着 "abc"
  print(s, s2)    # abcd abc
  ```
- **可变**：可以就地改内容，**对象还是同一个**。
  ```python
  a = [1, 2, 3]
  a.append(4)     # 就地改；id 不变
  ```

> 记住一句话：**不可变的"改"= 换对象；可变的"改"= 改对象。**

### 要点 3：`b = a` 是**别名**，不是复制

```python
a = [1, 2, 3]
b = a            # b 和 a 指向同一个列表
b.append(4)
print(a, b)      # [1, 2, 3, 4] [1, 2, 3, 4]   ← 阶段 0 第 2 题就是这个
print(a is b)    # True
```

**这就是你上次答错的地方**：`b = a` 没有复制任何东西，只是给同一个对象又起了一个名字。

### 要点 4：要"互不影响"，得**复制**

```python
a = [1, 2, 3]
b = a.copy()     # 新列表；等价的还有 list(a) 和 a[:]
b.append(4)
print(a, b)      # [1, 2, 3] [1, 2, 3, 4]
print(a is b)    # False
```

| 写法 | 结果 |
|---|---|
| `b = a` | 别名，同一个对象 |
| `b = a.copy()` / `list(a)` / `a[:]` | 浅拷贝，新的最外层对象 |
| `b = copy.deepcopy(a)` | 深拷贝，连里面的东西也复制 |

### 要点 5：浅拷贝陷阱（**今天最重要的一点**）

`.copy()` 只复制**最外面一层**，里面装的对象还是共享的：

```python
outer = [[1, 2], [3]]
shallow = outer.copy()
shallow[0].append(99)
print(outer)                        # [[1, 2, 99], [3]]   ← 原列表也变了！
print(outer[0] is shallow[0])       # True                  ← 里面的列表是同一个
```

要彻底独立，用 `copy.deepcopy()`：

```python
import copy
outer = [[1, 2], [3]]
deep = copy.deepcopy(outer)
deep[0].append(99)
print(outer)      # [[1, 2], [3]]   干净
```

### 要点 6：`tuple` 的"不可变"到底指什么

元组不可变 = **元组里存的那几个"指向"不能换**。但指向的**对象本身**该可变还是可变：

```python
t = (1, 2, [3])
t[2].append(4)    # 合法！改的是那个列表，不是元组
print(t)          # (1, 2, [3, 4])
t[1] = 9          # TypeError: 'tuple' object does not support item assignment
```

### 要点 7：`==` 比内容，`is` 比身份

```python
u = [1, 2]
v = [1, 2]
print(u == v)     # True   内容相同
print(u is v)     # False  但不是同一个对象
```

### 要点 8：回头看默认参数陷阱 —— 它其实是同一个问题

```python
def add_task_bad(title, tasks=[]):     # 这个 [] 只在定义时造了 1 个
    tasks.append(title)
    return tasks

add_task_bad("a")   # ['a']
add_task_bad("b")   # ['a', 'b']   ← 因为两次调用共享同一个列表（别名！）
```

再看这个对比：

```python
r = [1, 2, 3]
t = r.copy()        # 新列表 → 改 t 不影响 r
t = r               # 别名   → 改 t 就是改 r
```

`tasks=[]` 就是"别名"，`tasks=None` + 函数内新建就是"复制"。**同一个原理。**

### 示例代码

→ 运行 [demo_reference.py](demo_reference.py)

```powershell
cd G:\python-learning
.\.venv\Scripts\Activate.ps1
python exercises\stage1\day01\demo_reference.py
```

**先每段预测输出，再运行。**

---

## 三、练习（60 分钟，共 10 题）

> **规则（新）**：
> - **档① 读改** → **档② 填空** → **档③ 默写**。上一档没过，不许做下一档。
> - 不会的直接写"不会 + 你的思路"，**不要空着**，也**不要先去搜答案**。
> - 答案不给，但下面"四、自检清单"有**预期输出**，你可以自己判对错。

### 档① 读改（先改 `demo_reference.py`，观察输出怎么变）

**1.** 把第 4 段（别名）里的 `q.append(4)` 改成 `q = q + [4]`。
预测并运行：`p` 和 `q` 各是什么？`p is q` 是什么？**为什么和原来不同？**

**2.** 把第 5 段（复制）里的 `t = r.copy()` 改成 `t = r`。
预测并运行：`r` 最后是什么？

**3.** 把第 6 段（浅拷贝）里的 `shallow = outer.copy()` 改成
`shallow = copy.deepcopy(outer)`（文件顶部加 `import copy`）。
预测并运行：`outer` 最后是什么？和原来差在哪？

### 档② 填空（把 `______` 补上，让程序达到注释里的预期）

**4.**
```python
import copy
a = [[1, 2], [3]]
b = ______            # 只填一行
b[0].append(99)
print(a)              # 期望: [[1, 2], [3]]
```

**5.**
```python
def collect(item, box=None):
    if ______:        # 只填一个条件
        box = []
    box.append(item)
    return box

print(collect("a"))   # 期望: ['a']
print(collect("b"))   # 期望: ['b']
```

**6.**
```python
m = [5]
n = ______            # 只填一行
n.append(6)
print(m, n)           # 期望: [5] [5, 6]
```

### 档③ 默写（关掉所有参考资料）

**7.** 交换 `a` 和 `b` 的值，**不借助第三个变量**。
先写你自己的版本（你 C/Java 的直觉是什么？），再想 Python 有没有更短的写法，两种都写上。

**8.** 写代码验证下面两个结论，并各用一句话解释：
- `bool` 是 `int` 的子类（提示：`isinstance`）
- `True + True` 的结果是什么，为什么

**9.** 给定：
```python
tasks = [
    {"id": 1, "status": "todo"},
    {"id": 2, "status": "done"},
]
```
- 打印 `tasks[0] == {"id": 1, "status": "todo"}` 和 `tasks[0] is tasks[0]`，解释这两个结果。
- 执行 `snapshot = tasks.copy()`，再 `snapshot[0]["status"] = "done"`，打印 `tasks`。
  **为什么原列表也变了？**
- 写出**一种**让 `snapshot` 真正独立的改法。

**10.（综合题，今天最重的一题）**
1. 定义 `a = [1, 2, 3]`。
2. 用**三种**不同方式生成"内容相同、互不影响"的 `b`（提示：`.copy()`、`list(...)`、切片）。
3. 每种方式都用 `print(b is a)` 验证结果是 `False`。
4. 对 `b` 执行 `b.append(4)`，确认 `a` 没变。
5. 现在改成 `b = a`（别名），再 `b.append(4)`，确认 `a` 变了。
6. 用**一句话**写进错题本：什么时候该用 `=`，什么时候该用 `.copy()`。

---

## 四、自检清单（预期输出，对完再提交）

> 先自己判，把**对不上的题号**记下来。不给我代码我也能帮你。

**`demo_reference.py` 原样的输出**（你的 `id` 数字会不同，只要"变没变"对得上就行）：

```text
1-a: 140720554034376      ← 一串数字
1-b: 140720554034696      ← 和 1-a 不同的数字
2-a: abcd abc
2-b: 6 5
3-a: 2427331633152        ← 一串数字
3-b: 2427331633152        ← 和 3-a 完全相同
3-c: [1, 2, 3, 4]
4-a: [1, 2, 3, 4] [1, 2, 3, 4]
4-b: True
5-a: [1, 2, 3] [1, 2, 3, 4]
5-b: False
6-a: [[1, 2, 99], [3]]
6-b: True
7-a: (1, 2, [3, 4])
8-a: True False
9-a: ['a']
9-b: ['a', 'b']
9-c: ['a']
9-d: ['b']
10-a: True
10-b: <class 'bool'> <class 'int'> <class 'float'> <class 'str'> <class 'NoneType'>
```

**练习的预期结果**：

| 题 | 预期 | 关键点 |
|---|---|---|
| 1 | `p` = `[1, 2, 3]`，`q` = `[1, 2, 3, 4]`，`p is q` = `False` | `q + [4]` **造新列表**，不是就地改 |
| 2 | `r` = `[1, 2, 3, 4]` | `t = r` 是别名 |
| 3 | `outer` = `[[1, 2], [3]]` | `deepcopy` 连内层也复制 |
| 4 | `b = copy.deepcopy(a)` | 浅拷贝不够，因为 `a` 是嵌套的 |
| 5 | `if box is None:` | 判断"没传"而不是"空列表" |
| 6 | `n = m.copy()` | `list(m)`、`m[:]` 也对 |
| 7 | `a, b = b, a` | 右侧先算成一个元组，再一起解包；不需要临时变量 |
| 8 | `isinstance(True, int)` → `True`；`True + True` → `2` | Python 里 `bool` 继承自 `int`，`True == 1` |
| 9 | `True` / `True`；`tasks` 变成 `[{'id': 1, 'status': 'done'}, {'id': 2, 'status': 'done'}]`；改法 = `copy.deepcopy(tasks)` | `.copy()` 是浅拷贝，内层字典还是同一个 |
| 10 | 三种方式 `is` 都是 `False`；第 5 步 `a` 变成 `[1, 2, 3, 4]` | 一句话：**要共享改动用 `=`，要互不影响用 `.copy()`** |

---

## 五、复盘（20 分钟）

新建 `mistakes/2026-10-14.md`，按这个格式写：

```markdown
# 错题本 2026-10-14

## 错题 1
- 现象：我写的是 …，实际输出是 …
- 错因：（一句话，说到概念层。不要写"粗心"）
- 正确写法：
    ```python
    ...
    ```
- 变式：如果数据换成 …，结果会怎样？

## 错题 2
...

## 今天最不稳的一个点
（一句话）

## 明天开始前要复习的
（一句话）
```

然后在仓库根目录提交：

```powershell
cd G:\python-learning
git add .
git commit -m "feat(stage1): day01 对象模型练习与错题"
git log --oneline
```

---

## 六、提交格式

做完发我：

```text
【阶段1 D1 提交】
1. 档① 三题的结果与解释
2. 档② 三题你填的内容
3. 档③ 第 7 题（两种写法）
4. 档③ 第 8 题
5. 档③ 第 9 题（三问）
6. 档③ 第 10 题（六步）
7. self-check 对不上的题号
8. git log --oneline
9. 卡住点 / 我的思路
```

我会按固定格式反馈：**结论 / 正确点 / 具体问题 / 错因分析 / 最小修改建议 / 2~3 道变式题 / 需要复习的旧知识点 / 下一步任务**。

---

## 今日验收标准

- [ ] 能不看资料说清：`b = a` 和 `b = a.copy()` 的区别
- [ ] 能说出至少 4 个不可变类型、3 个可变类型
- [ ] 能解释浅拷贝为什么会"影响到原数据"
- [ ] 能用同一套原理讲通默认参数陷阱
- [ ] `demo_reference.py` 跑通，且每段输出都能提前预测对
