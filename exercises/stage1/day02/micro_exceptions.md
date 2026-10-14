# D2 微课 · 异常处理入门（30 分钟）

> **为什么放在今天**：D2 的运算符天生会抛异常 —— `10 / 0`、`int("abc")`、`1 + "a"`。
> 今天只学"**认脸 + 会捕获**"，不学自定义异常类（阶段 3 处理 FastAPI 错误响应时再深入）。
>
> 原计划里这一节属于 D5；[03-阶段1节奏修订](../../../notes/03-阶段1节奏修订.md) 把它前置到 D2，D5 才装得下。

---

## 1. 先认脸：你迟早会见到的 8 类异常

| 代码 | 抛出的异常 | 一句话原因 |
|---|---|---|
| `10 / 0` | `ZeroDivisionError` | 除数不能为 0 |
| `int("abc")` | `ValueError` | 类型对但内容不合法 |
| `1 + "a"` | `TypeError` | 两种类型不能相加 |
| `{"a": 1}["b"]` | `KeyError` | 字典里没这个 key |
| `[1, 2][5]` | `IndexError` | 下标越界 |
| `undefined_name` | `NameError` | 名字没定义过 |
| `import notexist` | `ModuleNotFoundError`（`ImportError` 的子类） | 模块找不到 |
| `"abc".push("d")` | `AttributeError` | 这个对象没有这个方法 |

> 这 8 类就是阶段 1 验收里要求你**现场修正**的那 8 个，今天的任务是"看代码说出抛哪个"，D5 验收时会让你现场改。

---

## 2. `try / except`：只捕获你预期的那个异常

```python
user_input = "abc"

try:
    n = int(user_input)
except ValueError:
    n = 0          # 转换失败 → 给个兜底值

print(n)           # 0
```

**三条纪律：**

1. `except` 一定要写**具体类型**，不要写裸 `except:`。
   裸 `except:` 会把 `KeyboardInterrupt`、你代码里的 `TypeError` bug 全吞掉 —— 到时候"程序不报错但结果不对"，最难查。
2. **只包住可能出错的那一两行**，不要把整个函数塞进 `try`。
3. 捕获之后要**有意义的处理**，不要只写 `pass`。

---

## 3. 多分支 + `else` + `finally`

```python
try:
    result = 10 / int(divisor)
except ZeroDivisionError:
    print("除数不能为 0")
except ValueError:
    print("输入的不是数字")
else:
    print("成功，结果是", result)   # 没抛异常才执行
finally:
    print("无论成功失败都执行")      # 收尾（关文件、释放连接）
```

执行顺序记法：**`try` → 出错就跳到匹配的 `except` → 没错就走 `else` → 无论如何都走 `finally`**。

---

## 4. 主动抛异常：`raise`

```python
def set_age(age: int) -> None:
    if age < 0:
        raise ValueError(f"年龄不能为负: {age}")
```

用途：你的函数发现"参数不合法"时，**别默默返回 None**，直接抛出去让调用方知道。

---

## 5. 30 分钟练习（3 题）

**练 1（编写）**：写 `to_int(s: str) -> int | None`：能转换就返回整数，转换失败返回 `None`。
要求：`except` 写具体类型；**不许**用裸 `except:`。

**练 2（读代码说结果）**：下面输出什么？（先写下来再跑）

```python
try:
    print(1 / 0)
except TypeError:
    print("A")
except ZeroDivisionError:
    print("B")
finally:
    print("C")
```

**练 3（改错）**：下面这段"看起来能跑"，但藏了一个会吞掉 bug 的写法，找出来并改对。

```python
def parse(text: str) -> int:
    try:
        return int(text)
    except:
        return 0
```

<details>
<summary>想完再看答案</summary>

- 练 2：打印 **`B`** 然后 **`C`**（`1/0` 抛 `ZeroDivisionError`，不匹配 `TypeError`，跳到第二个 `except`；`finally` 一定执行）。
- 练 3：裸 `except:` 会连 `KeyboardInterrupt`、`MemoryError` 和自己的 `TypeError` 一起吞掉。
  改成 `except ValueError:`（`int()` 转换失败只抛 `ValueError`）。

</details>

---

## 6. 写完后

把这三题的代码/答案放进 `day02.py` 末尾，或单独存 `micro_exceptions.py`，然后一起提交。
