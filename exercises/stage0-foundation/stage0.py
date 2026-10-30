# A1. list / tuple / dict / set 各写一句话区别，并各写一句创建代码。
# list 列表，按写入的顺序存，可以用下标取值，可以重复，list_a1: list[int] = [1,2,3]
# tuple 元组，tuple_a1: tuple[int] = ([1],[2])
# dict 字典，键值对，dict_a1: dict[int] = {1:"1",2:"2"}
# set 集合，自动去重，set_a1: set[str] = {'1','2','a'}

# A2 下面代码输出什么？为什么？
# def f(x=[]):
#     x.append(1)
#     return x
# print(f())
# print(f())
# 输出：[1] [1, 1]。因为f()未传递值所以为空，但是.append之后就是在原本的基础上追加，x初始化在参数列表中。

# A3. a = {"name": "张三", "tags": ["a", "b"]}；b = a.copy()；b["tags"].append("c")； 问：a["tags"] 现在是什么？为什么？
# a["tags"]现在的结果就是["a", "b", "c"]因为是浅拷贝，而非深拷贝，浅拷贝只拷贝外围成员，内部的对象不会被拷贝，修改内部对象会把a的也修改，因为他们是共享的同一个"tags"。

# A4. 下面两段分别输出什么？为什么？
# a = 256; b = 256; print(a is b)
# a = 1000; b = 1000; print(a is b)
# 两端都输出Turn，因为a和b都是相等的

# A5. 用一行代码把字符串 " 张三,20 " 拆成 "张三" 和整数 20。
# str = " 张三,20 "
# print(str.strip().split(","))

# A6. 写程序：找出 1~100 里第一个能被 7 整除的数，找到就停止循环。
# for i in range(1, 100):
#     if i % 7 == 0:
#         break

# A7. 写两个函数：total(*nums) 返回所有数字之和；show(**kwargs) 打印所有键值对。
# def total(number: list[int]) -> int:
#     sum = 0
#     for i in number:
#         sum += i
#     return sum
# def show(number: dict) -> None:
#     print(**number)

# A8. 为什么函数内部给全局变量赋值要写 global？写个例子说明不加会怎样。
# 如果不加global的话这个全局变量就会变为函数的局部变量。
# SU = 5
# def add_sum() -> int:
#     print(SU)
#     SU += 1
#     print(SU)
#     return 0
# add_sum()
# 不加会报错


# A9. try / except / else / finally 分别在什么时机执行？写一个"除零就重试"的小函数（重试 3 次）。
# try在最开始执行，如果try中报错就执行except，try和except都执行完成之后执行finally，如果没有报错就执行else。
# def div(a: float, b: float) -> float:
#     for i in range(2):
#         try:
#             return a / b
#         except ZeroDivisionError:
#             raise ValueError("除数不能为0")
#     return 0.0


# A10. 写一个类 Student：
# __init__(self, name, score)
# 方法 is_pass()：分数 >= 60 返回 True
# __str__ 返回 "张三: 85"
# class Student:
#     def __int__(self, name, score):
#         self.name = name
#         self.score = score

#     def is_pass(self):
#         return self.score >= 60

#     def __str__(self) -> str:
#         return "张三：85"


# A11. 写函数 load_config(path)：读 JSON 文件返回 dict；文件不存在返回 {}；再写 save_config(path, data)，中文不转义。
# def load_config(path):
#     try:
#         with open(path, "r", encoding="utf-8"):
#             import json

#             return json.load(path)
#     except FileNotFoundError:
#         return {}

# def save_config(path, data)
#     import json
#     try:
#         with open(path, "w", encoding="utf-8"):
#             json.dumps(data)
#     except FileNotFoundError:
#         return {}


# A12. if __name__ == "__main__": 有什么用？为什么要用虚拟环境（venv）？
# if __name__ == "__main__"表示当前文件是被直接执行，而非导入，是程序的主入口。
# 虚拟环境是为了每个项目都存在自己的一套python环境,防止污染,混淆.


# B1. GET / POST / PUT / DELETE 各是什么语义？哪些是"幂等"的？
# GET:获取(查)数据 POST:新增(增)数据 PUT:修改(改)数据 DELETE:删除(删)数据,幂等不知道

# B2. 各用一句话说：200 / 201 / 204 / 400 / 401 / 403 / 404 / 422 / 500。
# 只记得200是成功ok的意思

# B3. 请求 GET /items/5?limit=10，带 header Authorization: Bearer xxx 和 body {"a": 1}。 在 FastAPI 里，5、limit、Authorization、body 分别对应函数里的什么写法？
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# app = FastAPI()
# class Item(BaseModel):
#     items_id: int = Field(gt=0, le=100)
#     limit: int = Field(100, gt=0, le=100)
# @app.get("/items/{items_id}")
# def items(items_id, limit):
#     return items_id, limit
# 在 FastAPI里5就相当于@app.get("/items/{items_id}")中的items_id,limit就相当于items函数中的limit参数.body就相当于class Item(BaseModel):中的内容.Authorization不清楚.

# B4. json.dumps({"name": "张三"}, ensure_ascii=False) 和 json.dumps({"name": "张三"}) 输出有什么不同？
# 前者在json中输出的是正常的字符,能看懂的.后者输出都是乱码的.

# B5. 什么是"阻塞"？为什么 FastAPI 里推荐 async def + 异步客户端（如 redis.asyncio、aiomysql）？
# 阻塞就是一个函数中把主线程占用一直不释放,卡住在里面了. 异步就是程序执行在此处后需要专门等待他执行完成,主线程可以继续往下执行.

# B6. 浏览器报 CORS 错误是什么原因？服务端怎么解决？
# 不知道

# C1. 写出 SELECT 各子句的逻辑执行顺序（FROM / WHERE / GROUP BY / HAVING / SELECT / ORDER BY / LIMIT）。
# SELECT FROM WHERE HAVING GROUP BY ORDER BY LIMIT

# C2. 有联合索引 (status, score)，查询 WHERE score > 60 能用上这个索引吗？为什么？改成什么条件能用上？
# 不清楚,记不全了.

# C3. 事务 ACID 四个特性分别是什么？各靠 MySQL 的什么机制实现？
# A 原子性,其他的忘记了.

# C4. departments LEFT JOIN employees 后，COUNT(*) 和 COUNT(employees.id) 对"没有员工的部门"结果各是多少？为什么？
# COUNT(*)会把null也算+1,如果只是COUNT(employees.id)就null算作0

# D1. 路径参数、查询参数、请求体，在函数里怎么区分？（写判断规律）
# 路径参数就是@app.get("/items/{items_id}"),查询参数def items(itesm_id,limit)中的limit就是查询参数.用http://就是请求体. 如:http://223.244.82.69/items/5?limit=10

# D2. Field(gt=0)、Field(ge=0)、Field(min_length=1)、Field(le=100) 分别校验什么？
# gt大于,ge大于等于,min_length最小长度,le大于等于

# D3. response_model 干什么用？为什么它能把 secret 字段过滤掉？
# response_model过滤敏感数据的,防止把secret给到json中用户看到.

# D4. Depends 干什么？它和"装饰器"的区别是什么？
# Depends在函数参数列表中使用,会先执行Depends中的函数.和"装饰器"的区别不清楚.

# D5. lifespan 干什么用？为什么数据库连接池 / Redis 客户端要放在里面初始化？
# 不知道

# E1. 写出完整命令序列：从 master 拉一个新分支 → 改代码 → 提交 → 推送 → 准备开 PR。
# 不知道

# E2. 用 pytest 写一个测试：验证 add(1, 2) == 3。
# 不知道

# E3. 为什么数据库密码不能写死在代码里？应该放在哪、代码怎么读？
# 写在密码中会暴露

