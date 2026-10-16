# D4 微课 · JSON + OOP 基础（75 分钟）

> **为什么放在今天**：
> - **JSON** 是 dict 的天然搭档（D4 刚学完 dict），也是 D5 待办项目"存盘"要用的东西；
> - **OOP** 是函数/作用域之后最自然的下一步，而阶段 4 的 SQLAlchemy 模型、阶段 3 的 Pydantic 模型都建立在这上面。
>
> 这两节原本在 D5；[03-阶段1节奏修订](../../../notes/03-阶段1节奏修订.md) 前置到 D4，10-18 那天才装得下项目 + 验收。

---

# Part A · JSON（30 分钟）

## A1. 两个核心函数：`dumps` / `loads`

```python
import json

data = {"id": 1, "name": "Tom", "tags": ["a", "b"], "ok": True, "note": None}

text = json.dumps(data)            # Python 对象 → JSON 字符串
back = json.loads(text)            # JSON 字符串 → Python 对象
print(type(text), type(back))      # <class 'str'> <class 'dict'>
```

**记忆**：`s` 结尾的（dumps / loads）操作**字符串**；不带 s 的（dump / load）操作**文件**。

## A2. 类型映射表（背下来）

| Python | JSON |
|---|---|
| `dict` | object `{}` |
| `list` / `tuple` | array `[]` |
| `str` | string |
| `int` / `float` | number |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

## A3. 中文与格式（两个必加参数）

```python
print(json.dumps({"name": "汤姆"}))
# {"name": "\u6c64\u59c6"}        ← 中文被转义了，人看不懂

print(json.dumps({"name": "汤姆"}, ensure_ascii=False))
# {"name": "汤姆"}                 ← 正常

print(json.dumps({"name": "汤姆"}, ensure_ascii=False, indent=2))
# 多行缩进，适合写进文件给人看
```

## A4. 写文件 / 读文件

```python
with open(".tmp/data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(".tmp/data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
```

> **D5 的待办项目就用这一套存盘**：程序退出前 `json.dump`，启动时 `json.load`（文件不存在就当成空列表）。

## A5. 四个常见坑

| 坑 | 现象 |
|---|---|
| 忘了 `ensure_ascii=False` | 中文变成 `\u6c64` |
| `set` 不能序列化 | `TypeError: Object of type set is not JSON serializable` |
| **元组会变 list** | `json.loads(json.dumps((1, 2)))` → `[1, 2]`（回不去了） |
| **key 会被转成字符串** | `json.dumps({1: "a"})` → `'{"1": "a"}'` |

## A6. 练习（3 题）

**练 A1**：写 `to_json(obj: object) -> str`，返回**不转义中文**的 JSON 字符串。
**练 A2**：写 `save_json(path: str, obj: object) -> None` 和 `load_json(path: str) -> object`（`load_json` 在文件不存在时返回 `None`）。
**练 A3（改错 + 说结果）**：下面哪几行会报错？为什么？

```python
json.dumps({"a": {1, 2}})          # ①
json.dumps({"a": (1, 2)})          # ②
json.loads(json.dumps({"a": (1, 2)}))   # ③ 结果是？
json.dumps({(1, 2): "a"})          # ④
```

<details>
<summary>想完再看答案</summary>

- ① 报错：`set` 不能序列化。
- ② 正常，元组被当成 array 输出 `[1, 2]`。
- ③ 结果是 `{'a': [1, 2]}` —— **元组变回不去了**。
- ④ 报错：JSON 的 key 必须是字符串，元组 key 不行（`TypeError: keys must be str...`）。

</details>

---

# Part B · OOP 基础（45 分钟）

## B1. 为什么需要类

你已经会"函数 + 容器"。但当一个东西**既有数据又有操作**时，散着放会很难维护：

```python
todo = {"title": "写代码", "done": False}      # 数据
def finish(todo: dict) -> None:                # 操作
    todo["done"] = True
```

**类 = 把"数据"和"操作数据的函数"打包在一起**。

## B2. 最小可用的类

```python
class Todo:
    def __init__(self, title: str) -> None:
        self.title = title          # 实例属性
        self.done = False

    def finish(self) -> None:
        self.done = True

    def __str__(self) -> str:       # print(obj) 时显示什么
        return f"[{'x' if self.done else ' '}] {self.title}"
```

```python
t = Todo("写代码")       # 调用 __init__，self 就是 t
t.finish()
print(t)                 # [x] 写代码
```

**三条必须记住的**：

1. `__init__` 是"造对象时自动跑"的函数（不是构造函数，别纠结名字）。
2. **`self` 就是"这个对象自己"**，第一个参数必须写 `self`（调用时不用传）。
3. `self.title = title` 才是"存到对象身上"；只写 `title = title` 就丢了。

## B3. 实例属性 vs 类属性（⚠️ 阶段 0 第 6 题的坑）

```python
class Counter:
    count = 0                  # 类属性：所有实例共享

    def bump(self) -> None:
        self.count += 1        # ← 看起来在改类属性，其实创建了"实例属性"！

a, b = Counter(), Counter()
a.bump()
a.bump()
b.bump()
print(a.count, b.count, Counter.count)     # 2 1 0
```

**为什么**：`self.count += 1` 等价于 `self.count = self.count + 1` —— 右边**读**到了类属性 0，然后**赋值**给了 `a` 自己的一份。
→ 这就是 D1 的"**换指向 vs 改对象**"在类里的又一次现身。

**要所有实例共享一个计数器，得写 `Counter.count += 1`**（或者干脆用一个模块级变量）。

## B4. 方法、属性、`__str__`

```python
class Todo:
    ...
    def to_dict(self) -> dict[str, object]:     # 类 → dict（准备存 JSON）
        return {"title": self.title, "done": self.done}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Todo":   # dict → 类
        t = cls(str(data["title"]))
        t.done = bool(data["done"])
        return t
```

这两个方法（`to_dict` / `from_dict`）是**阶段 3、4 的核心套路**：Pydantic 模型、SQLAlchemy 模型都在干这件事 —— "对象 ↔ 数据"。今天先手写一遍，后面就懂了。

## B5. 练习（3 题）

**练 B1**：写 `class Todo`：`__init__(title)` 存 `title` 和 `done=False`；`finish()` 把 `done` 设为 True；`__str__` 返回 `[x] 标题` 或 `[ ] 标题`。

**练 B2**：给 `Todo` 加 `to_dict()` 和 `from_dict(data)`，并验证：
```python
t = Todo("写代码")
t.finish()
t2 = Todo.from_dict(t.to_dict())
print(t2)          # 应该和 t 一样
```

**练 B3（读代码说结果）**：

```python
class Bag:
    items = []

    def add(self, x: int) -> None:
        self.items.append(x)

b1, b2 = Bag(), Bag()
b1.add(1)
b2.add(2)
print(Bag.items, b1.items, b2.items)
```

<details>
<summary>想完再看答案</summary>

打印 **`[1, 2] [1, 2] [1, 2]`**。

原因：`items = []` 是**类属性**，`b1.items.append(x)` 里 `b1.items` 先**读到**那个类属性列表，然后 `.append` **就地改**它（D1 的"改对象"），**没有赋值给 self**，所以没有创建实例属性 → 两个实例看到的是同一个列表。

对比 B3 的 `self.count += 1`：那里有**赋值**，所以创建了实例属性。**差一个"赋值"，行为完全不同。**

正确写法：在 `__init__` 里 `self.items: list[int] = []`（每个实例一份）。

</details>

---

## 写完后

- JSON 练习 → `exercises/stage1/day04/micro_json.py`
- OOP 练习 → `exercises/stage1/day04/micro_oop.py`
- 测试文件写到 `.tmp/` 下（已被 gitignore 忽略）
- 记得在提交信息里带上 `+ JSON/OOP 微课`
