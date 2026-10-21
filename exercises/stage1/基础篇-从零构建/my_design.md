【基础篇 00 · 设计卡】
## 需求 1：单词计数器
### ① 数据
统计结果：dict[str, int]，例如{"the":12, "cat": 5}
### ② 模块
- read_text(path) -> str  只负责读文件内容；文件不存在时返回 ""；不允许打印
- count_words(text) -> dict  只负责切词+去标点+小写+计数；**不读文件、不打印**
- top_n(counts, n) -> list   只负责按次数排序取前 n；**不打印**
- main(argv)                 只负责解析参数、串联上面三步、打印
### ③ 步骤
1. 从 argv 拿文件路径和 --top N（默认 10）
2. read_text 读文本；为空 → 打印提示、返回 1
3. count_words：text.split() 切词 → 每个词 strip 标点 + lower() → 跳过空串 → dict 计数
4. top_n：按 (-次数, 单词) 排序 → 取前 N
5. 打印结果

## 需求 2：学生成绩管理（内存版，不存文件）
### ① 数据
```json
[
  {"name": "张三", "score": 85},
  {"name": "李四", "score": 92}
]
```
用 class，在内存中就是一个存着 Student 对象的列表：[Student("张三", 85), Student("李四", 92)]
### ② 模块
- Student 类：负责定义单个学生的基本结构（包含姓名和分数），不许负责管理其他学生。
- students 列表：负责充当内存数据库，装载所有学生对象，不许直接对外暴露处理逻辑。
- add_student(name, score) 函数：负责接收姓名和分数，实例化学生并追加到列表中，不许负责打印或计算。
- view_students() 函数：负责遍历列表并格式化打印所有学生信息，不许修改数据。
- print_stats() 函数：负责计算并打印平均分和最高分学生，不许修改原列表。
### ③ 步骤
1. 定义 Student 类，包含 __init__ 初始化姓名和分数。
2. 初始化全局空列表 students = []。
3. 定义 add_student(name, score) 函数：students.append(Student(name, score))。
4. 定义 view_students() 函数：遍历 students，打印每个学生的名字和分数。
5. 定义 print_stats() 函数：
6. 判断 if not students: 则打印“无数据”并 return。
7. 计算平均分：avg = sum(s.score for s in students) / len(students)。
8. 找最高分：top_student = max(students, key=lambda s: s.score)。
9. 打印平均分和最高分学生的名字。
10. 执行写死的测试操作：调用 add_student("张三", 85) 和 add_student("李四", 92)。
11. 调用 view_students() 查看所有学生。
12. 调用 print_stats() 打印统计结果。

## 需求 3：简易 ATM（数据要存盘）
### ① 数据
```json
{
  "balance": 1000.0
}
```
在内存中，就是一个普通的字典：data = {"balance": 1000.0}
### ② 模块
- load_balance() 函数：负责从 JSON 文件读取余额并返回（如果文件不存在或格式错误，默认返回 0.0），不许修改余额。
- save_balance(balance) 函数：负责把最新的余额数字覆写进 JSON 文件，不许做业务逻辑判断。
- deposit(amount) 函数：负责接收存款金额，校验正数后，读取余额、加上金额、保存新余额并返回，不许处理取款逻辑。
- withdraw(amount) 函数：负责校验正数和余额是否充足，扣减余额、保存并返回，不许自己直接操作文件（调用读写函数即可）。
- check_balance() 函数：负责读取并打印当前余额，不许修改数据。
### ③ 步骤
1. 定义常量 FILE_PATH = "atm.json"。
2. 定义 load_balance()：尝试 open 文件并用 json.load 读取 balance 值；如果 FileNotFoundError 则返回 0.0。
3. 定义 save_balance(balance)：用 json.dump 将 {"balance": balance} 写入文件。
4. 定义 deposit(amount)：
5. 如果 amount <= 0，抛出异常 ValueError("存款金额必须为正数")。
6. 调用 load_balance() 获取当前余额。
7. 计算新余额并调用 save_balance()。
8. 返回新余额。
9. 定义 withdraw(amount)：
10. 如果 amount <= 0，抛出异常 ValueError("取款金额必须为正数")。
11. 调用 load_balance() 获取当前余额。
12. 如果 amount > 当前余额，抛出异常 ValueError("余额不足")。
13. 计算新余额并调用 save_balance()。
14. 返回新余额。
15. 定义 check_balance()：调用 load_balance() 并 print 出来。
16. 执行硬编码测试：存款 500 → 查余额 → 取款 200 → 查余额 → 尝试取款 1000（触发异常并捕获）。
17. 重启程序（重新运行），直接查余额，验证数据依然存在。