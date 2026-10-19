-- MySQL 练习库初始化（8.0+）
-- 用法（任选一种）：
--   docker compose up -d      （会被 docker-entrypoint 自动执行）
--   mysql -h 127.0.0.1 -P 3306 -u root -p < init.sql
--   或在 DBX 的 SQL 编辑器里整段执行

CREATE DATABASE IF NOT EXISTS practice
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE practice;

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id   INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE employees (
    id         INT PRIMARY KEY,
    name       VARCHAR(50)  NOT NULL,
    dept_id    INT,
    salary     DECIMAL(10, 2) NOT NULL,
    hire_date  DATE NOT NULL,
    manager_id INT,
    CONSTRAINT fk_employee_dept FOREIGN KEY (dept_id) REFERENCES departments (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

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

-- 验证（执行完应该看到 4 + 12 行）
SELECT COUNT(*) AS dept_count FROM departments;
SELECT COUNT(*) AS emp_count FROM employees;
