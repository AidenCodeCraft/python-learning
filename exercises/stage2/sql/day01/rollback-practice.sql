-- 事务回滚 · 10 分钟实验（DBX 里开 **两个标签页**，都连 practice 库）
--
-- 目标：亲眼看到"未提交的修改别人看不到""ROLLBACK 能撤销""COMMIT 之后撤不回来"
--      以及最重要的一条：**DDL（TRUNCATE/DROP/Alter）会隐式提交，回滚不了**
--
-- 用法：按顺序执行，每一步对照注释里的"应该看到什么"。
-- 执行完清理： DROP TABLE rollback_demo;

-- ============================================================
-- 准备（标签页 A 执行一次）
-- ============================================================
DROP TABLE IF EXISTS rollback_demo;

CREATE TABLE rollback_demo (
    id      INT PRIMARY KEY AUTO_INCREMENT,
    name    VARCHAR(20) NOT NULL,
    balance INT NOT NULL DEFAULT 0
);

INSERT INTO rollback_demo (name, balance) VALUES ('张三', 100), ('李四', 200);

-- 此时 A、B 两个标签页都执行这段，应看到：
--   1 | 张三 | 100
--   2 | 李四 | 200


-- ============================================================
-- 实验 1：ROLLBACK（在标签页 A 里按顺序执行）
-- ============================================================
START TRANSACTION;

UPDATE rollback_demo SET balance = balance - 50 WHERE name = '张三';

-- A 里查：看到张三 50（事务内部能看到自己的修改）
SELECT * FROM rollback_demo;

-- 👉 现在切到 **标签页 B** 执行：SELECT * FROM rollback_demo;
--    B 应该还看到 100 —— 未提交的修改别人看不见

-- 切回 A，撤销：
ROLLBACK;

-- A 里再查：张三回到 100 ✅
SELECT * FROM rollback_demo;


-- ============================================================
-- 实验 2：COMMIT
-- ============================================================
START TRANSACTION;

UPDATE rollback_demo SET balance = balance - 50 WHERE name = '张三';

COMMIT;

-- A 和 B 现在都看到张三 50 —— 提交之后就撤不回来了
SELECT * FROM rollback_demo;


-- ============================================================
-- 实验 3：DDL 不能回滚（重点考点）
-- ============================================================
START TRANSACTION;

UPDATE rollback_demo SET balance = 999 WHERE name = '李四';

TRUNCATE TABLE rollback_demo;    -- ⚠️ TRUNCATE 是 DDL，会**隐式提交**上面那条 UPDATE

ROLLBACK;                        -- 已经没用了：表都空了

SELECT * FROM rollback_demo;     -- 0 行（数据没了，UPDATE 也回不去了）

-- 结论：ROLLBACK 只能撤销**未提交的 DML**（INSERT/UPDATE/DELETE）；
--       DDL（TRUNCATE/DROP/ALTER）会隐式提交，**不可回滚**。


-- ============================================================
-- 清理
-- ============================================================
DROP TABLE IF EXISTS rollback_demo;

-- ============================================================
-- 自检小测（做完把答案写在这，交给教练）
-- ============================================================
-- 1. 实验 1 里，标签页 B 在 A 未提交时看到张三的余额是：____
-- 2. ROLLBACK 之后，张三的余额是：____
-- 3. COMMIT 之后，B 看到的余额是：____
-- 4. 实验 3 里 ROLLBACK 为什么救不回来？一句话：____
-- 5. MySQL 默认 autocommit 是多少？它对"回滚"有什么影响：____
