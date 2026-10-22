-- 每个员工的 id、name、部门名（按 id 升序）
SELECT em.id, em.name, dp.name
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
ORDER BY em.id;

-- 研发部所有员工的姓名、工资（按 id 升序）
SELECT em.name, em.salary
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
WHERE dp.name  = "研发部"
ORDER BY em.id ;

-- 每个部门名 + 员工数（只保留有员工的部门，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM employees em
LEFT JOIN departments dp ON dp.id = em.dept_id
GROUP BY dp.name , em.dept_id;

-- 每个部门名 + 平均工资（保留 2 位小数），按平均工资从高到低
SELECT dp.name, ROUND(AVG(em.salary), 2) AS avg_salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY avg_salary DESC ;

-- 工资 > 20000 的员工：emp_name、dept_name、salary（按工资降序）
SELECT em.name AS emp_name, dp.name AS dept_name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE em.salary > 20000
ORDER BY em.salary DESC ;

-- 销售部员工的姓名、工资（按工资升序）
SELECT em.name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "销售部"
GROUP BY em.name, em.salary 
ORDER BY em.salary ;

-- 每个员工的 emp_name + 上级 mgr_name（没上级的也要显示，按 id）
SELECT e.name AS emp_name, m.name AS mgr_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY e.id;

-- 所有部门名 + 员工数（没员工的显示 0，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name;

-- 找出没有员工的部门名
SELECT dp.name
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
WHERE em.dept_id IS NULL
GROUP BY dp.name, em.dept_id;

-- 员工数 > 3 的部门名 + 人数
SELECT dp.name, COUNT(em.dept_id) AS cnt
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name
HAVING COUNT(em.dept_id) > 3;

-- 每个部门名 + 最高工资（没员工的部门也要出现，按最高工资降序）
SELECT dp.name, MAX(em.salary)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY MAX(em.salary) DESC;

-- 研发部和销售部两个部门的员工：emp_name、dept_name（按 id 升序）
SELECT em.name AS emp_name, dp.name AS dept_name
FROM employees em
LEFT JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "研发部" OR dp.name  = "销售部"
ORDER BY em.id;-- 每个员工的 id、name、部门名（按 id 升序）
SELECT em.id, em.name, dp.name
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
ORDER BY em.id;

-- 研发部所有员工的姓名、工资（按 id 升序）
SELECT em.name, em.salary
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
WHERE dp.name  = "研发部"
ORDER BY em.id ;

-- 每个部门名 + 员工数（只保留有员工的部门，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM employees em
LEFT JOIN departments dp ON dp.id = em.dept_id
GROUP BY dp.name , em.dept_id;

-- 每个部门名 + 平均工资（保留 2 位小数），按平均工资从高到低
SELECT dp.name, ROUND(AVG(em.salary), 2) AS avg_salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY avg_salary DESC ;

-- 工资 > 20000 的员工：emp_name、dept_name、salary（按工资降序）
SELECT em.name AS emp_name, dp.name AS dept_name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE em.salary > 20000
GROUP BY em.name ,dp.name, em.salary 
ORDER BY em.salary DESC ;

-- 销售部员工的姓名、工资（按工资升序）
SELECT dp.name, em.name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "销售部"
GROUP BY dp.name, em.name, em.salary 
ORDER BY em.salary ;

-- 每个员工的 emp_name + 上级 mgr_name（没上级的也要显示，按 id）
SELECT em.name AS emp_name, dp.name AS mgr_name
FROM employees em
LEFT JOIN departments dp ON em.dept_id = dp.id
GROUP BY emp_name , mgr_name;

-- 所有部门名 + 员工数（没员工的显示 0，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name, em.dept_id;

-- 找出没有员工的部门名
SELECT dp.name
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
WHERE em.dept_id IS NULL
GROUP BY dp.name, em.dept_id;

-- 员工数 > 3 的部门名 + 人数
SELECT dp.name, COUNT(em.dept_id) AS cnt
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name, em.dept_id
HAVING COUNT(em.dept_id) > 3;

-- 每个部门名 + 最高工资（没员工的部门也要出现，按最高工资降序）
SELECT dp.name, MAX(em.salary)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY MAX(em.salary) DESC;

-- 研发部和销售部两个部门的员工：emp_name、dept_name（按 id 升序）
SELECT em.name AS emp_name, dp.name AS dept_name
FROM employees em
LEFT JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "研发部" OR dp.name  = "销售部"
ORDER BY em.id;

-- Day02
-- 每个员工的 id、name、部门名（按 id 升序）
SELECT em.id, em.name, dp.name
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
ORDER BY em.id;

-- 研发部所有员工的姓名、工资（按 id 升序）
SELECT em.name, em.salary
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
WHERE dp.name  = "研发部"
ORDER BY em.id ;

-- 每个部门名 + 员工数（只保留有员工的部门，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM employees em
LEFT JOIN departments dp ON dp.id = em.dept_id
GROUP BY dp.name , em.dept_id;

-- 每个部门名 + 平均工资（保留 2 位小数），按平均工资从高到低
SELECT dp.name, ROUND(AVG(em.salary), 2) AS avg_salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY avg_salary DESC ;

-- 工资 > 20000 的员工：emp_name、dept_name、salary（按工资降序）
SELECT em.name AS emp_name, dp.name AS dept_name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE em.salary > 20000
GROUP BY em.name ,dp.name, em.salary 
ORDER BY em.salary DESC ;

-- 销售部员工的姓名、工资（按工资升序）
SELECT dp.name, em.name, em.salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "销售部"
GROUP BY dp.name, em.name, em.salary 
ORDER BY em.salary ;

-- 每个员工的 emp_name + 上级 mgr_name（没上级的也要显示，按 id）
SELECT em.name AS emp_name, dp.name AS mgr_name
FROM employees em
LEFT JOIN departments dp ON em.dept_id = dp.id
GROUP BY emp_name , mgr_name;

-- 所有部门名 + 员工数（没员工的显示 0，按 dept_id）
SELECT dp.name, COUNT(em.dept_id)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name, em.dept_id;

-- 找出没有员工的部门名
SELECT dp.name
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
WHERE em.dept_id IS NULL
GROUP BY dp.name, em.dept_id;

-- 员工数 > 3 的部门名 + 人数
SELECT dp.name, COUNT(em.dept_id) AS cnt
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name, em.dept_id
HAVING COUNT(em.dept_id) > 3;

-- 每个部门名 + 最高工资（没员工的部门也要出现，按最高工资降序）
SELECT dp.name, MAX(em.salary)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY MAX(em.salary) DESC;

-- 研发部和销售部两个部门的员工：emp_name、dept_name（按 id 升序）
SELECT em.name AS emp_name, dp.name AS dept_name
FROM employees em
LEFT JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = "研发部" OR dp.name  = "销售部"
ORDER BY em.id;

-- 工资最高的员工姓名 + 工资
SELECT em.name, em.salary
FROM employees em
WHERE salary = (SELECT MAX(em2.salary)
FROM employees em2);

-- 工资高于公司平均工资的员工姓名 + 工资（按工资升序）
SELECT em.name, em.salary
FROM employees em
WHERE salary > (SELECT AVG(em2.salary)
FROM employees em2)
ORDER BY em.salary ;

-- 部门平均工资 > 公司平均工资的部门名 + 平均工资（保留 2 位）
SELECT dp.name, ROUND(AVG(em.salary), 2)
FROM departments dp
JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name 
HAVING AVG(em.salary) > (
SELECT AVG(em2.salary) 
FROM employees em2);

-- 查研发部所有员工（用子查询取 dept_id）
SELECT em.name, em.salary
FROM employees em
WHERE em.dept_id  = (SELECT dp.id
FROM departments dp
WHERE dp.name = "研发部");

-- 工资高于销售部最高工资的员工姓名 + 工资
SELECT em.name, em.salary
FROM employees em
JOIN departments dp ON dp.id = em.dept_id
WHERE em.salary > (SELECT DISTINCT MAX(em2.salary)
FROM employees em2
JOIN departments dp ON em2.dept_id = dp.id
WHERE dp.name = "销售部");

-- 用 NOT IN 或 NOT EXISTS 找没有员工的部门名
SELECT dp.name
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
WHERE NOT EXISTS (SELECT 1
FROM employees em2
WHERE em2.dept_id = dp.id);

-- 每个部门名 + 员工数 + 平均工资（没员工的部门也要出现，按 dept_id）
SELECT dp.name, COUNT(em.name), ROUND(AVG(em.salary), 2)
FROM departments dp
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name;

-- 读代码说结果：说出下面这条查询返回几行、每行是什么
SELECT d.name, COUNT(*) AS cnt
FROM departments d
JOIN employees e ON e.dept_id = d.id
WHERE e.salary > 18000
GROUP BY d.id, d.name
ORDER BY d.id;
-- 返回三行，每行是：研发部	3\n产品部	1\n销售部	2