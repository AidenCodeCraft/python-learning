-- 数据库考试 · 学员选课练习库（MySQL 8.0）
-- 用法：DBX 里整段执行，或 docker exec -i exam-mysql mysql -uroot -p123456 < schema.sql

CREATE DATABASE IF NOT EXISTS school
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE school;

-- 先删有外键的表
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;

-- 1. 学员
CREATE TABLE students (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,
    name       VARCHAR(50)  NOT NULL,
    age        INT,
    phone      VARCHAR(20)  NOT NULL UNIQUE,          -- 手机号唯一
    city       VARCHAR(50),
    is_deleted TINYINT NOT NULL DEFAULT 0,            -- 逻辑删除标记
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 2. 课程
CREATE TABLE courses (
    id    BIGINT PRIMARY KEY AUTO_INCREMENT,
    name  VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0           -- 金额用 DECIMAL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 3. 报名（同一学员不能重复报名同一课程；未出成绩用 NULL）
CREATE TABLE enrollments (
    id         BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL,
    course_id  BIGINT NOT NULL,
    score      INT NULL,
    status     TINYINT NOT NULL DEFAULT 0,            -- 0待审核 1已通过 2已取消
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_student_course UNIQUE (student_id, course_id),
    CONSTRAINT fk_en_student FOREIGN KEY (student_id) REFERENCES students (id),
    CONSTRAINT fk_en_course  FOREIGN KEY (course_id)  REFERENCES courses (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- 4. 账户
CREATE TABLE accounts (
    student_id BIGINT PRIMARY KEY,
    balance    DECIMAL(10, 2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_acc_student FOREIGN KEY (student_id) REFERENCES students (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ==================== 种子数据 ====================

INSERT INTO students (name, age, phone, city) VALUES
    ('张三', 20, '13800000001', '北京'),
    ('李四', 22, '13800000002', '上海'),
    ('王五', 19, '13800000003', '北京'),
    ('赵六', 25, '13800000004', '广州'),
    ('钱七', 21, '13800000005', '上海'),
    ('孙八', 23, '13800000006', '深圳'),
    ('周九', 20, '13800000007', '北京'),
    ('吴十', 24, '13800000008', '广州'),
    ('郑十一', 26, '13800000009', '杭州');   -- 故意不报名任何课程，用于"从未报名"题

INSERT INTO courses (name, price) VALUES
    ('Python入门', 299.00),
    ('MySQL实战', 399.00),
    ('Redis进阶', 199.00),
    ('FastAPI开发', 499.00);

INSERT INTO enrollments (student_id, course_id, score, status) VALUES
    (1, 1, 85,   1),
    (1, 2, 90,   1),
    (2, 1, 78,   1),
    (2, 3, NULL, 0),      -- 未出成绩
    (3, 1, 92,   1),
    (3, 4, NULL, 0),      -- 未出成绩
    (4, 2, 66,   1),
    (5, 1, 58,   1),
    (5, 2, NULL, 2),      -- 已取消
    (6, 3, 88,   1),
    (7, 1, 95,   1),
    (7, 2, NULL, 0),      -- 未出成绩
    (8, 4, 72,   1),
    (8, 1, NULL, 0);      -- 待审核（用于"多表关联更新"题）

INSERT INTO accounts (student_id, balance) VALUES
    (1, 1000.00),
    (2, 500.00),
    (3, 0.00),
    (4, 2000.00),
    (5, 800.00),
    (6, 300.00),
    (7, 1500.00),
    (8, 100.00);

-- 验证：应输出 students 9 / courses 4 / enrollments 14 / accounts 8
SELECT 'students' AS t, COUNT(*) AS cnt FROM students
UNION ALL SELECT 'courses', COUNT(*) FROM courses
UNION ALL SELECT 'enrollments', COUNT(*) FROM enrollments
UNION ALL SELECT 'accounts', COUNT(*) FROM accounts;
