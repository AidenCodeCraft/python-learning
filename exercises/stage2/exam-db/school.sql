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

CREATE DATABASE IF NOT EXISTS school
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

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

CREATE TABLE IF NOT EXISTS `courses` (
  `id`    bigint        NOT NULL AUTO_INCREMENT COMMENT '课程ID',
  `name`  varchar(100)  NOT NULL               COMMENT '课程名称',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '课程价格',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='课程表';

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

CREATE TABLE IF NOT EXISTS `accounts` (
  `student_id` bigint        NOT NULL            COMMENT '学员ID',
  `balance`    decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '账户余额',
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_acc_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='账户表';