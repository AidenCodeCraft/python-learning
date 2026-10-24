# 03 · 综合题：Redis + MySQL 缓存查询（50 分钟）

> **考点原文**（综合题，很可能原样出）：
> 1. MySQL 保存学员资料
> 2. 查询时先读 Redis，未命中再查询 MySQL
> 3. 将查到的资料写入 Redis，有效期 300 秒
> 4. 修改资料时，先更新并提交 MySQL，再删除对应缓存
> 5. 不存在的学员返回明确结果
> 6. 正确处理 JSON、中文、数据库异常
>
> **这就是"Cache-Aside（旁路缓存）"模式**，后端最常用的缓存写法。
>
> 本机 Redis 端口是 **6380**（6379 被 `ai-diagnostic-redis` 占用）；考试现场按现场配置改 host/port。

---

## 一、模式图（背下来）

```text
读：  查 Redis ──命中──► 直接返回
        │未命中
        ▼
     查 MySQL ──有──► 写回 Redis（TTL 300s）→ 返回
        │没有
        ▼
      返回 None（明确告诉调用方"不存在"）

写：  先 UPDATE MySQL 并 commit
        ▼
      再 DELETE 对应缓存（不是更新缓存！）
```

**为什么"删缓存"而不是"更新缓存"**：更新缓存可能和并发读交错，写出旧值；删除后下次读会从库重建，逻辑更简单、更不容易错。

---

## 二、完整参考实现（考试直接照这个改）

```python
import json

import pymysql
import redis

# ---------- 连接（考试时改成你的配置）----------
REDIS = redis.Redis(host="127.0.0.1", port=6380, db=0, decode_responses=True)
CACHE_TTL = 300          # 秒
DB_CONF = dict(host="127.0.0.1", port=3306, user="root", password="123456",
               database="school", charset="utf8mb4",
               cursorclass=pymysql.cursors.DictCursor)


def _connect() -> pymysql.connections.Connection:
    return pymysql.connect(**DB_CONF)


def cache_key(student_id: int) -> str:
    return f"student:{student_id}"


# ---------- 读：先缓存，后数据库 ----------
def get_student(student_id: int) -> dict | None:
    """查到返回 dict；不存在返回 None；数据库/Redis 异常向上抛。"""
    key = cache_key(student_id)

    # 1. 先读缓存
    try:
        cached = REDIS.get(key)
        if cached is not None:
            return json.loads(cached)          # 命中：JSON 反序列化
    except redis.RedisError:
        pass                                    # 缓存挂了不影响主流程（降级查库）

    # 2. 未命中 → 查 MySQL
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, age, phone, city FROM students "
                "WHERE id = %s AND is_deleted = 0",
                (student_id,),
            )
            row = cur.fetchone()
    finally:
        conn.close()                            # 一定释放连接

    if row is None:
        return None                             # 明确返回"不存在"

    # 3. 写回缓存（中文不转义 + 300 秒过期）
    try:
        REDIS.set(key, json.dumps(row, ensure_ascii=False), ex=CACHE_TTL)
    except redis.RedisError:
        pass
    return row


# ---------- 写：先更新库，再删缓存 ----------
ALLOWED_FIELDS = {"name", "age", "phone", "city"}


def update_student(student_id: int, **fields: object) -> bool:
    """更新成功 True；学员不存在 False。字段名走白名单，值走参数化。"""
    sets, values = [], []
    for name, value in fields.items():
        if name not in ALLOWED_FIELDS:
            raise ValueError(f"不允许更新的字段: {name}")     # 列名不能参数化 → 白名单
        sets.append(f"{name} = %s")                            # 只拼列名（白名单内）
        values.append(value)

    if not sets:
        return False

    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE students SET {', '.join(sets)} WHERE id = %s AND is_deleted = 0",
                (*values, student_id),
            )
            affected = cur.rowcount
        conn.commit()                                          # 先提交库
    except pymysql.err.MySQLError:
        conn.rollback()                                         # 失败回滚
        raise
    finally:
        conn.close()

    if affected == 0:
        return False                                            # 学员不存在（没更新任何行）

    # 再删缓存（提交成功之后！）
    try:
        REDIS.delete(cache_key(student_id))
    except redis.RedisError:
        pass
    return True
```

---

## 三、考点 6 条要求逐条对应（验收自查）

| 考点要求 | 代码里在哪 | 说明 |
|---|---|---|
| 1. MySQL 存资料 | `_connect` + `SELECT ... FROM students` | 用 `school` 库 |
| 2. 先 Redis 未命中再 MySQL | `get_student` ①②③ | 命中直接 return |
| 3. 写回 Redis + 300 秒 | `REDIS.set(key, json, ex=CACHE_TTL)` | `ex=300` |
| 4. 修改：先更新提交 MySQL，再删缓存 | `update_student`：`conn.commit()` 之后 `REDIS.delete` | **顺序不能反** |
| 5. 不存在返回明确结果 | `return None`（查询）/ `return False`（更新） | 不要抛异常 |
| 6. JSON / 中文 / 异常 | `json.dumps(ensure_ascii=False)`；`charset="utf8mb4"`；`except pymysql.err.MySQLError` / `redis.RedisError` | 缓存异常可降级，数据库异常要回滚 |

---

## 四、验证脚本（跑一遍，考场上心里有底）

```python
if __name__ == "__main__":
    sid = 1
    REDIS.delete(cache_key(sid))
    print("第一次查询（未命中，查库）:", get_student(sid))
    print("缓存里现在有:", REDIS.get(cache_key(sid)) is not None)
    print("第二次查询（命中，读缓存）:", get_student(sid))

    print("改手机号:", update_student(sid, phone="13911112222"))
    print("缓存被删了吗:", REDIS.get(cache_key(sid)) is None)
    print("再查（重建缓存）:", get_student(sid))

    print("查不存在的人:", get_student(9999))          # None
    print("改不存在的人:", update_student(9999, city="火星"))  # False
```

**预期输出**：
```text
第一次查询（未命中，查库）: {'id': 1, 'name': '张三', ...}
缓存里现在有: True
第二次查询（命中，读缓存）: {...}
改手机号: True
缓存被删了吗: True
再查（重建缓存）: {... 'phone': '13911112222' ...}
查不存在的人: None
改不存在的人: False
```

---

## 五、进阶追问（考点原文提了一句"不要当作强一致性"）

> "**并发情况下的缓存一致性问题**" —— 面试/进阶会问。

答法：
1. 先更库再删缓存，仍可能短时间不一致：**读请求在"删缓存之前"拿到旧值，在"删缓存之后"写回缓存** → 缓存里留旧值，直到 300s 过期。
2. 缓解手段：
   - **缩短 TTL**（如 60s）
   - **延迟双删**：更新库 → 删缓存 → 等几百毫秒 → 再删一次
   - 更新时用**版本号/时间戳**，读时比对
   - 对强一致要求高的数据，**直接读库**不缓存
3. 一句话总结：**Cache-Aside 是"最终一致"，不是强一致。**

---

## 六、50 分钟怎么练

| 分钟 | 做什么 |
|---:|---|
| 0–15 | 读第二节代码，逐行注释（尤其是顺序和异常处理） |
| 15–35 | **关掉资料**，自己把 `get_student` 和 `update_student` 敲一遍 |
| 35–45 | 跑第四节验证脚本，输出对得上 |
| 45–50 | 口述 6 条验收 + 进阶追问的答法 |

## 自检

- [ ] 能默写"读：缓存→库→写回"三段
- [ ] 能默写"写：commit 之后 delete 缓存"
- [ ] 知道为什么删缓存而不是更新缓存
- [ ] 能说出 `ensure_ascii=False` 和 `charset="utf8mb4"` 各解决什么问题
- [ ] 能说出缓存异常时"降级查库"、数据库异常时"回滚 + 抛"
