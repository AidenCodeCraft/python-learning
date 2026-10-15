# 练 1（编写）：写 to_int(s: str) -> int | None：能转换就返回整数，转换失败返回 None。 要求：except 写具体类型；不许用裸 except:。
def to_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


# 练 2（读代码说结果）：下面输出什么？（先写下来再跑）
try:
    print(1 / 0)
except TypeError:
    print("A")
except ZeroDivisionError:
    print("B")      # 执行这里
finally:
    print("C")

# 练 3（改错）：下面这段"看起来能跑"，但藏了一个会吞掉 bug 的写法，找出来并改对。
def parse(text: str) -> int:
    try:
        return int(text)
    # except:
    except ValueError:
        return 0