DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT NOT NULL,
  total DECIMAL(10,2) NOT NULL DEFAULT 0,
  status TINYINT NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders (user_id, total, status)
VALUES (1, 99.50, 0),
(2, 200.00, 1),
(1, 15.00, 2);

SELECT status 
FROM orders ord 
WHERE status = 0;

UPDATE orders 
SET status = 1
WHERE status = 0;

SELECT total 
FROM orders ord 
WHERE total < 50;

DELETE FROM orders 
WHERE total < 50;

SELECT em.name, dp.name ,em.salary 
FROM employees em 
JOIN departments dp ON dp.id = em.dept_id
ORDER BY em.salary DESC;

SELECT dp.name , COUNT(em.dept_id)
FROM departments dp 
LEFT JOIN employees em ON em.dept_id = dp.id
GROUP BY dp.name
ORDER BY COUNT(em.dept_id) DESC ;

SELECT em.name , em.salary 
FROM employees em 
WHERE salary > (SELECT AVG(em2.salary) 
FROM employees em2)
ORDER BY em.salary;

SELECT dp.name, ROUND(AVG(em.salary), 2)
FROM departments dp 
LEFT JOIN employees em ON em.dept_id = dp.id
WHERE em.salary > (SELECT AVG(em2.salary)
FROM employees em2)
GROUP BY dp.name;

SELECT em.name , em2.name 
FROM employees em
LEFT JOIN employees em2 ON em.manager_id = em2.id;

SELECT em.name, MAX(em.salary) AS max_salary
FROM employees em
JOIN departments dp ON em.dept_id = dp.id
WHERE dp.name = '研发部'
GROUP BY em.name
ORDER BY max_salary DESC
LIMIT 1;

-- 图书表（books）
-- 字段名	类型	约束	说明
-- id	BIGINT	PK, AUTO_INCREMENT	主键
-- title	VARCHAR(200)	NOT NULL	书名
-- author	VARCHAR(100)	NOT NULL	作者
-- isbn	VARCHAR(20)	NOT NULL, UNIQUE	ISBN，唯一
-- total_copies	INT	NOT NULL, DEFAULT 0, CHECK >= 0	总册数
-- available_copies	INT	NOT NULL, DEFAULT 0, CHECK >= 0	可借册数
CREATE TABLE books (
  id BIGINT PRIMARY KEY AUTO_INCREMENT ,
  title VARCHAR(200) NOT NULL ,
  author VARCHAR(100) NOT NULL,
  isbn VARCHAR(20) NOT NULL UNIQUE,
  total_copies INT NOT NULL DEFAULT 0,
  available_copies INT NOT NULL DEFAULT 0,
  CONSTRAINT chk_total_copies CHECK (total_copies >= 0),
  CONSTRAINT chk_available_copies CHECK (chk_available_copies >= 0),
  CONSTRAINT chk_copies_valid CHECK (available_copies <= total_copies),
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 会员表（members）
-- 字段名	类型	约束	说明
-- id	BIGINT	PK, AUTO_INCREMENT	主键
-- name	VARCHAR(50)	NOT NULL	姓名
-- phone	VARCHAR(20)	NOT NULL, UNIQUE	手机号，唯一
-- created_at	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	注册时间
CREATE TABLE members (
  id BIGINT PRIMARY KEY AUTO_INCREMENT ,
  name VARCHAR(50) NOT NULL ,
  phone VARCHAR(20) NOT NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 借阅记录表（borrow_records）
-- 字段名	类型	约束	说明
-- id	BIGINT	PK, AUTO_INCREMENT	主键
-- book_id	BIGINT	NOT NULL, FK → books.id	哪本书
-- member_id	BIGINT	NOT NULL, FK → members.id	哪个会员
-- borrow_time	DATETIME	NOT NULL, DEFAULT CURRENT_TIMESTAMP	借出时间
-- due_time	DATETIME	NOT NULL	应还时间
-- return_time	DATETIME	NULL	归还时间，未还时为空
-- status	TINYINT	NOT NULL, DEFAULT 0, CHECK IN (0,1,2)	0借出中 / 1已归还 / 2逾期
CREATE TABLE borrow_records (
  id BIGINT PRIMARY KEY AUTO_INCREMENT ,
  book_id BIGINT NOT NULL,
  member_id BIGINT NOT NULL,
  borrow_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_time DATETIME NOT NULL,
  return_time DATETIME DEFAULT NULL,
  status TINYINT NOT NULL DEFAULT 0,
  CONSTRAINT chk_status CHECK (status IN(0, 1, 2)),
  CONSTRAINT fk_borrow_book FOREIGN KEY (book_id) REFERENCES books(id),
  CONSTRAINT fk_borrow_member FOREIGN KEY (member_id) REFERENCES members(id),
  INDEX idx_member_status (member_id, status),
  INDEX idx_book_status (book_id, status)
)ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ① 查某个会员当前还没还的书
SELECT * FROM borrow_records 
WHERE member_id = ? AND return_time IS NULL;
-- 建议索引：在 borrow_records 表上建 联合索引 (member_id, status)，或 (member_id, return_time)。
-- 为什么：member_id 是等值查询，放在联合索引最左列，可以快速定位到该会员的所有借阅记录。

-- ② 查某本书当前被谁借走了
SELECT * FROM borrow_records 
WHERE book_id = ? AND return_time IS NULL;
-- 建议索引：在 borrow_records 表上建 联合索引 (book_id, status)，或 (book_id, return_time)。
-- 为什么：同理，book_id 等值查询放最左列，快速定位这本书的所有借阅记录。