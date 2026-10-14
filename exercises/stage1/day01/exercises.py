def add_task_bad(title, tasks=None):     # 这个 [] 只在定义时造了 1 个
    if tasks is None:
        tasks = []
    tasks.append(title)
    return tasks

print(add_task_bad("a"))   # ['a']
print(add_task_bad("b"))   # ['a', 'b']   ← 因为两次调用共享同一个列表（别名！）