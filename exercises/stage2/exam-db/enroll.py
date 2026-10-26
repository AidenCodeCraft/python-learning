"""
    必考事务题：
    学员报名课程时，需要扣减账户余额并新增报名记录。余额不足、重复报名或任一步骤失败时，整个操作回滚。

    验收点：
    两次写操作处于同一事务。
    扣款不会导致余额为负。
    重复报名由唯一约束兜底。
    失败后账户余额和报名记录均保持正确。
    SQL 使用参数绑定，异常后释放连接资源。
"""

import pymysql
from pymysql.err import IntegrityError

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "school",
    "charset": "utf8mb4",
    "autocommit": False,
}

def enroll_course(student_id: int, course_id: int) -> dict:
    """ 学员报名课程：插入报名 + 扣减余额，任一步失败整体回滚。 """
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT price FROM courses WHERE id = %s", (course_id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"课程 {course_id} 不存在")
            price = row[0]

            cur.execute(
                "INSERT INTO enrollments (student_id, course_id, status) "
                "VALUES (%s, %s, %s)",
                (student_id, course_id, "pending"),
            )

            cur.execute(
                "UPDATE accounts SET balance = balance - %s "
                "WHERE student_id = %s AND balance >= %s",
                (price, student_id, price),
            )
            if cur.rowcount == 0:
                cur.execute(
                    "SELECT balance FROM accounts WHERE student_id = %s",
                    (student_id,),
                )
                acc = cur.fetchone()
                if acc is None:
                    raise ValueError(f"学员 {student_id} 的账户不存在")
                raise ValueError(f"余额不足：当前 {acc[0]}，需要 {price}")

        conn.commit()
        return {
            "ok": True,
            "student_id": student_id,
            "course_id": course_id,
            "price": str(price),
        }

    except IntegrityError as e:
        conn.rollback()
        if e.args and e.args[0] == 1062:
            raise ValueError(
                f"学员 {student_id} 已报名课程 {course_id}，不能重复报名"
            ) from e
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()