"""D4 示例：函数与容器（读改素材）

用法：
    1. 每段**先在纸上预测输出**，再运行。
    2. 运行：python demo_reference.py
    3. 对不上的地方，回 README 第二节找原因。

注意：本文件**故意不写答案**（注释里没有输出）。预期输出在 README 第四节"自检清单"。
"""

from __future__ import annotations

# ============================================================
# 1. 函数基础：参数、返回值、多返回值
# ============================================================
def add(a: int, b: int = 10) -> int:
    return a + b


print("1-a:", add(1), add(1, 2), add(b=5, a=1))


def min_max(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)


low, high = min_max([3, 1, 9])
print("1-b:", low, high, min_max([3, 1, 9]))


# ============================================================
# 2. 默认参数陷阱（D1 学过原理：默认值只在定义时创建一次）
# ============================================================
def bad_add(title: str, tasks: list[str] = []) -> list[str]:
    tasks.append(title)
    return tasks


print("2-a:", bad_add("a"))
print("2-b:", bad_add("b"))


def good_add(title: str, tasks: list[str] | None = None) -> list[str]:
    if tasks is None:
        tasks = []
    tasks.append(title)
    return tasks


print("2-c:", good_add("a"))
print("2-d:", good_add("b"))


# ============================================================
# 3. 作用域：函数里能读全局，但"赋值"会让它变成局部
# ============================================================
counter = 0


def read_counter() -> int:
    return counter


print("3-a:", read_counter())


def bump_bad() -> None:
    counter = counter + 1       # 取消注释会报 UnboundLocalError
    print(counter)


def bump_good() -> None:
    global counter              # 少用，但要知道它的存在
    counter += 1


print("3-b:", "bump_bad 默认是注释掉的，见 README 说明")


# ============================================================
# 4. 可变 / 不可变参数：传进去的列表会被就地改
# ============================================================
def append_item(items: list[int]) -> None:
    items.append(99)


data = [1, 2]
append_item(data)
print("4-a:", data)


def rebind_item(items: list[int]) -> None:
    items = items + [99]        # 造新列表，不动原来的


data2 = [1, 2]
rebind_item(data2)
print("4-b:", data2)


# ============================================================
# 5. list：常用方法 + 切片
# ============================================================
nums = [3, 1, 4, 1, 5]
print("5-a:", sorted(nums), nums)
nums.sort()
print("5-b:", nums)
print("5-c:", nums[1:3], nums[::-1], nums[:2])


# ============================================================
# 6. dict：get / keys / values / items / 合并
# ============================================================
user = {"id": 1, "name": "Tom"}
print("6-a:", user.get("age"), user.get("age", 0))
print("6-b:", list(user.keys()), list(user.values()))
print("6-c:", {**user, "age": 18})
print("6-d:", "id" in user, 1 in user)


# ============================================================
# 7. set：去重与集合运算
# ============================================================
print("7-a:", set([1, 2, 2, 3]))
a, b = {1, 2, 3}, {2, 3, 4}
print("7-b:", a & b, a | b, a - b)


# ============================================================
# 8. str：split / join / strip / replace / 切片
# ============================================================
text = "  hello world  "
print("8-a:", repr(text.strip()))
print("8-b:", text.strip().split(" "))
print("8-c:", "-".join(["a", "b", "c"]))
print("8-d:", "a,b,,c".split(","))


# ============================================================
# 9. 推导式：一行造出 list / dict / set
# ============================================================
print("9-a:", [n * n for n in range(5)])
print("9-b:", [n for n in range(10) if n % 2 == 0])
print("9-c:", {n: n * n for n in range(1, 4)})
print("9-d:", {n % 3 for n in range(10)})


# ============================================================
# 10. 类型注解：给"可能没有"的值用 | None
# ============================================================
def find_user(users: dict[str, int], name: str) -> int | None:
    return users.get(name)


print("10-a:", find_user({"Tom": 1}, "Tom"), find_user({"Tom": 1}, "Ann"))
