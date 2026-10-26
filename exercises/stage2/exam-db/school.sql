-- 1.String 与 Hash： 保存学员资料时，各适合什么场景？
-- 答：如果学员资料数据是整块一起读写就用String；如果学员资料数据需要单独进行读写增删某个字段，那么就用Hash。

-- 2.List 与 Set： 哪个允许重复？哪个保留顺序？
-- 答：List允许重复、按插入顺序保留；Set不允许重复、没用顺序。

-- 3.Set 与 Sorted Set： 成绩排行榜为什么适合使用有序集合？
-- 答：Sorted Set适合成绩排行榜，因为每个成员都带一个分数，并按照分数自动排序；Set为无序的。

-- 4.排行榜： Redis 返回的排名从几开始？如何转换为界面显示的名次？
-- 答：zrevrank排名从0开始；界面显示名次需要+1。

-- 5.Pipeline 与事务： 批量发送命令与事务执行有什么区别？
-- 答：Pipeline是网络的优化，他会把多条指令打包一起发送，在指令执行时会被其他指令插入；事务是服务端，他在执行队列中指令时不会被其他指令打断。

-- 6.原子性： Python 中先 GET 再 SET 实现计数，会有什么并发问题？
-- 答：先 GET 再 SET 的计数会引发丢失更新的问题，GET 和 SET 本身是有原子性的但是两条命令之间没有。

CREATE DATABASE IF NOT EXISTS school;

-- 学员表
CREATE TABLE IF NOT EXISTS `students` (
  `id`         bigint      NOT NULL AUTO_INCREMENT COMMENT '学员ID',
  `name`       varchar(50) NOT NULL                COMMENT '姓名',
  `age`        int         DEFAULT NULL            COMMENT '年龄',
  `phone`      varchar(20) NOT NULL                COMMENT '手机号（唯一）',
  `city`       varchar(50) DEFAULT NULL            COMMENT '城市',
  `created_at` datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_students_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学员表';

-- 课程表
CREATE TABLE IF NOT EXISTS `courses` (
  `id`    bigint        NOT NULL AUTO_INCREMENT COMMENT '课程ID',
  `name`  varchar(100)  NOT NULL               COMMENT '课程名称',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '课程价格',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课程表';

-- 报名表
CREATE TABLE IF NOT EXISTS `enrollments` (
  `id`         bigint   NOT NULL AUTO_INCREMENT COMMENT '报名ID',
  `student_id` bigint   NOT NULL               COMMENT '学员ID',
  `course_id`  bigint   NOT NULL               COMMENT '课程ID',
  `score`      int      DEFAULT NULL           COMMENT '成绩（NULL 表示未出成绩）',
  `status`     tinyint  NOT NULL DEFAULT '0'   COMMENT '状态：0-待支付 1-已支付 2-已取消',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_student_course` (`student_id`,`course_id`),
  KEY `fk_en_course` (`course_id`),
  CONSTRAINT `fk_en_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  CONSTRAINT `fk_en_course` FOREIGN KEY (`course_id`)  REFERENCES `courses` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='报名表';

-- 账户表
CREATE TABLE IF NOT EXISTS `accounts` (
  `student_id` bigint        NOT NULL            COMMENT '学员ID',
  `balance`    decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '账户余额',
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_acc_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账户表';

-- 1.增：INSERT
-- 单条插入	新增一名学员
INSERT INTO students (name, age, phone, city) 
VALUES ('张三', 20, '18500000001', '北京');

-- 批量插入	新增 10 名学员
INSERT INTO students (name, age, phone, city)
VALUES ('李四', 22, '18500000002', '上海'),
    ('王五', 19, '18500000003', '北京'),
    ('赵六', 25, '18500000004', '广州');

-- 默认值与自增主键	新增课程并获取生成的主键
INSERT INTO courses (name, price)
VALUES ('Python', 599.00);
SELECT LAST_INSERT_ID();

-- 唯一约束	重复插入手机号，捕获错误并回滚
SET autocommit = 0;
START TRANSACTION;
INSERT INTO students (name, age, phone, city)
VALUES ("李白", 18, "18500000007", "合肥");
INSERT INTO students (name, age, phone, city)
VALUES ('杜甫', 20, '18500000007', '合肥');
ROLLBACK;
SELECT * FROM `students` WHERE `phone` = '18500000007';
COMMIT; 

-- 插入查询结果	把符合条件的学员写入教师提供的归档表
CREATE TABLE students_archive LIKE students;
INSERT INTO students_archive (id, name, age, phone, city, created_at)
SELECT s.id, s.name, s.age, s.phone, s.city, s.created_at
FROM students s
WHERE s.city = '北京' AND s.age >= 20
  AND NOT EXISTS (
    SELECT 1 FROM students_archive a WHERE a.phone = s.phone
  );

-- 冲突处理	对已存在的数据按指定规则更新，可作为进阶题
INSERT INTO students (name, age, phone, city)
VALUES ('李清照', 20, '18500000008', '陕西') AS new
ON DUPLICATE KEY UPDATE
 name = new.name,
 age  = new.age,
 city = new.city;

-- 2.查：SELECT
-- 基础查询	查询学员姓名和城市，列出不重复城市
SELECT name, city 
FROM students ;

SELECT DISTINCT city 
FROM students;

-- 条件查询	查询指定城市且年龄满足条件的学员
SELECT id, name, age, city 
FROM students
WHERE city = "北京" AND age >= 20;

-- 范围与集合	查询年龄区间内、来自指定城市的学员
SELECT id, name, age, city 
FROM students
WHERE age  BETWEEN 18 AND 25 AND city IN ('北京', '上海', '广州');

-- 模糊查询	查询姓“张”的学员
SELECT id, name, age, city 
FROM students
WHERE name LIKE '张%';

-- 空值判断	查询尚未出成绩的报名记录
SELECT id, student_id, course_id, score, status, created_at
FROM enrollments
WHERE score IS NULL ;

-- 排序与分页	按报名时间倒序分页，同时间按主键排序
SELECT id, student_id, course_id, score, status, created_at
FROM enrollments
ORDER BY created_at DESC , id  DESC 
LIMIT 10 OFFSET 0;

-- 聚合	统计课程报名数、平均分和最高分
SELECT course_id , COUNT(*), ROUND(AVG(score), 2) AS avg, MAX(score) AS max
FROM enrollments
GROUP BY course_id ;

-- 分组过滤	查询报名人数超过 5 人的课程
SELECT course_id , COUNT(*) AS '报名人数'
FROM enrollments
GROUP BY course_id 
HAVING COUNT(*) > 5;

-- 内连接	查询学员姓名、课程名称和成绩
SELECT s.name , c.name, e.score
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses  c ON c.id = e.course_id;

-- 外连接	查询所有学员，包括未报名学员
SELECT s.name, c.name AS 课程名称, e.score
FROM students s
LEFT JOIN enrollments e ON e.student_id = s.id
LEFT JOIN courses     c ON c.id = e.course_id;

-- 子查询	查询成绩高于该课程平均分的学员
SELECT e.student_id, e.course_id, e.score
FROM enrollments e
WHERE e.score > (
  SELECT AVG(e2.score)
  FROM enrollments e2
  WHERE e2.course_id = e.course_id
);

-- 无匹配记录	查询从未报名课程的学员
SELECT s.id, s.name
FROM students s
WHERE NOT EXISTS (
  SELECT 1 FROM enrollments e WHERE e.student_id = s.id
);

-- 条件表达式	将成绩转换为优秀、及格、不及格
SELECT id, student_id, course_id, score,
  CASE
    WHEN score IS NULL THEN '未出成绩'
    WHEN score >= 85   THEN '优秀'
    WHEN score >= 60   THEN '及格'
    ELSE '不及格'
  END AS 成绩等级
FROM enrollments;

-- 3. 改：UPDATE
-- 单字段更新	根据学员编号修改手机号
UPDATE students 
SET phone = '18500000091'
WHERE id = 1;

-- 多字段更新	同时修改学员城市和年龄
UPDATE students 
SET age = 21, city = '杭州'
WHERE id = 2;

-- 条件批量更新	将指定课程的待审核报名改为已通过
UPDATE enrollments 
SET status = 1
WHERE course_id =1 AND status = 0;

-- 表达式更新	给指定课程价格统一增加 10%
UPDATE courses 
SET price = ROUND(price * 1.10, 2)
WHERE id = 1;

-- 条件扣减	仅当余额足够时扣除课程费用，并检查受影响行数
UPDATE accounts a
JOIN courses cr ON cr.id = 1
SET a.balance = a.balance - cr.price 
WHERE a.student_id = 1
  AND a.balance >= cr.price ;

-- 多表关联更新	根据课程或学员条件批量修改报名状态，作为进阶题
UPDATE enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses  c ON c.id = e.course_id
SET e.status = 1
WHERE s.city = '北京'
  AND c.price < 300
  AND e.status = 0;

-- 4. 删：DELETE
-- 单条删除	删除指定报名记录
DELETE FROM enrollments 
WHERE id = 1;

-- 条件批量删除	删除指定日期以前已取消的报名
DELETE FROM enrollments
WHERE status = 2 AND created_at < '2025-01-01';

-- 多条件删除	删除指定课程中状态为取消的记录
DELETE FROM enrollments
WHERE course_id = 1
  AND status = 2;

-- 关联数据处理	删除学员及其报名记录，按题目规定的事务或外键策略执行
SET autocommit = 0;
START TRANSACTION;
DELETE FROM enrollments WHERE student_id = 1;
DELETE FROM accounts    WHERE student_id = 1;
DELETE FROM students    WHERE id = 1;
SELECT ROW_COUNT();
COMMIT;

-- 逻辑删除	使用状态字段标记删除，查询时排除
UPDATE enrollments SET status = 3 WHERE id = 1;
SELECT id, student_id, course_id, score, status, created_at
FROM enrollments en 
WHERE status <> 3;

-- 概念辨析	说明 DELETE、TRUNCATE、DROP 的区别
-- DELETE：删除表格中指定某项数据内容
-- TRUNCATE：清空表格中的所有数据，保留表结构
-- DROP：删除表，包括表结构