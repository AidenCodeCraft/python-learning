# 练 B1：写 class Todo：__init__(title) 存 title 和 done=False；finish() 把 done 设为 True；__str__ 返回 [x] 标题 或 [ ] 标题。
class Todo:
    def __init__(self, title: str) -> None:
        self.title = title
        self.done = False

    def finish(self) -> None:
        self.done = True

    def __str__(self) -> str:
        return f"[{'x' if self.done else ''}] {self.title}"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "done": self.done
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Todo":
        t = cls(str(data["title"]))
        t.done = bool(data["done"])
        return t

# 练 B2：给 Todo 加 to_dict() 和 from_dict(data)，并验证：
t = Todo("写代码")
t.finish()
t2 = Todo.from_dict(t.to_dict())
print(t2)          # 应该和 t 一样

# 练 B3（读代码说结果）：
class Bag:
    items = []

    def add(self, x: int) -> None:
        self.items.append(x)
b1, b2 = Bag(), Bag()
b1.add(1)
b2.add(2)
print(Bag.items, b1.items, b2.items)    # [1, 2] [1, 2] [1, 2]