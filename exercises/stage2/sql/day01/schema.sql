-- D1 练习库（SQLite）· 员工与部门
-- 用法：python run_sql.py          （建库并写入种子数据）
--      python run_sql.py "SELECT ...;"
--      python run_sql.py -f answers.sql

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    dept_id    INTEGER,
    salary     REAL NOT NULL,
    hire_date  TEXT NOT NULL,          -- 存成 'YYYY-MM-DD'，字典序 = 时间序
    manager_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES departments (id)
);

INSERT INTO departments (id, name) VALUES
    (1, '研发部'),
    (2, '产品部'),
    (3, '销售部'),
    (4, '人事部'),
    (5, '财务部');   -- 故意留一个"没有员工"的部门，JOIN 练习要用

INSERT INTO employees (id, name, dept_id, salary, hire_date, manager_id) VALUES
    (1,  '张伟', 1, 25000, '2019-03-01', NULL),
    (2,  '李娜', 1, 18000, '2020-07-15', 1),
    (3,  '王强', 1, 32000, '2018-01-10', 1),
    (4,  '刘洋', 2, 22000, '2019-11-20', NULL),
    (5,  '陈静', 2, 16000, '2021-05-06', 4),
    (6,  '杨帆', 3, 15000, '2022-02-14', NULL),
    (7,  '赵敏', 3, 28000, '2017-09-01', 6),
    (8,  '孙磊', 3, 19000, '2020-12-01', 6),
    (9,  '周婷', 4, 12000, '2021-08-23', NULL),
    (10, '吴昊', 4, 14000, '2023-04-10', 9),
    (11, '郑爽', 1, 21000, '2022-06-18', 3),
    (12, '冯磊', 2, 17500, '2023-01-09', 4);
