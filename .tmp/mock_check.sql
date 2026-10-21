-- 临时：核对模拟卷 Part B 的预期结果（SQLite 语法等价版）
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    total      REAL NOT NULL DEFAULT 0,
    status     INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO orders (user_id, total, status) VALUES (1, 99.50, 0), (2, 200.00, 1), (1, 15.00, 2);
SELECT 'B2: 3 行' AS step, COUNT(*) AS cnt FROM orders;
UPDATE orders SET status = 1 WHERE status = 0;
SELECT 'B3: 影响 1 行' AS step, changes() AS affected;
DELETE FROM orders WHERE total < 50;
SELECT 'B4: 影响 1 行' AS step, changes() AS affected;
SELECT 'B4 剩余' AS step, COUNT(*) AS cnt FROM orders;
