-- D1 SQL 练习作答文件
-- 用法：python run_sql.py -f answers.sql
--
-- 规则：
--   1. 每题写一条语句，**以分号结尾**（别在字符串里写分号）
--   2. 先写，再跑；跑完对照 README 第四节的"自检清单"
--   3. 写不出来就在注释里写"我的思路"，别留空

-- 1. 查所有员工的所有字段（按 id 升序）
-- TODO
SELECT *
FROM employees em 
ORDER BY id;
-- 2. 只查 name 和 salary 两列（按 id 升序）
-- TODO
SELECT em.name, em.salary
FROM employees em 
ORDER BY id;
-- 3. 查研发部（dept_id = 1）所有员工的姓名、工资（按 id 升序）
-- TODO
SELECT em.name, em.salary
FROM employees em
WHERE em.dept_id =1
ORDER BY id;
-- 4. 查工资大于 20000 的员工姓名、工资（按工资从高到低）
-- TODO
SELECT em.name, em.salary
FROM employees em
WHERE em.salary > 20000
ORDER BY em.salary DESC;
-- 5. 查工资在 15000 ~ 20000 之间（含端点）的员工姓名、工资（按工资升序）
-- TODO
SELECT em.name, em.salary
FROM employees em
-- WHERE em.salary >= 15000 AND em.salary <= 20000 
WHERE em.salary BETWEEN 15000 AND 20000
ORDER BY em.salary;
-- 6. 查工资最高的前 3 名（姓名、工资，从高到低）
-- TODO
SELECT em.name, em.salary
FROM employees em
ORDER BY em.salary DESC
LIMIT 3;
-- 7. 公司总人数
-- TODO
SELECT COUNT(em.id)
FROM employees em;
-- 8. 平均工资（四舍五入到 2 位小数）
-- TODO
SELECT ROUND(AVG(em.salary), 2) AS avg_salary
FROM employees em;
-- 9. 最高工资和最低工资（两个列：max_salary、min_salary）
-- TODO
SELECT MAX(em.salary) AS max_salary, MIN(em.salary) AS min_salary
FROM employees em;
-- 10. 每个部门的员工数（列：dept_id、cnt，按 dept_id 升序）
-- TODO
SELECT em.dept_id, COUNT(*)
FROM employees em
GROUP BY dept_id
ORDER BY dept_id ASC;
-- 11. 每个部门的平均工资，从高到低（列：dept_id、avg_salary，保留 2 位小数）
-- TODO
SELECT em.dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees em
GROUP BY dept_id
ORDER BY avg_salary DESC;
-- 12. 名字里带"张"的员工姓名
-- TODO
SELECT em.name
FROM employees em
WHERE name LIKE '张%';