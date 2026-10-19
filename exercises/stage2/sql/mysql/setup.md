# MySQL 练习环境搭建（10-20 早上做，约 15 分钟）

> 目标：跑起一个**能随便折腾**的 MySQL 8.0（增删改查练习用），并用 DBX 连上。
> 公司考试是**机考 + MySQL**，所以明天白天第一件事就是把这个环境弄好。
>
> 三条路，按你现场条件选一条：**A 最省事、B 最稳、C 最快但要公司给库**。

---

## 方案 A · Docker（推荐，5 分钟）

> 这台机器上 Docker **已安装但守护进程没启动**（我实测：`docker info` 连不上）。先打开 **Docker Desktop**，等鲸鱼图标变绿。

```powershell
cd D:\Program\Python\python-learning\exercises\stage2\sql\mysql
docker compose up -d
docker compose ps                 # 等 STATUS 变成 healthy（约 20~30 秒）
```

首次启动会自动执行 [init.sql](init.sql) 建好 `practice` 库和两张练习表。

验证：

```powershell
docker compose exec mysql mysql -uroot -p123456 -e "SELECT VERSION(); SHOW DATABASES;"
```

停止 / 重启 / 彻底清理：

```powershell
docker compose stop          # 停（数据保留在 volume 里）
docker compose start         # 再启动
docker compose down          # 停并删容器（数据还在 volume）
docker compose down -v       # 连数据一起删（下次重新初始化）
```

> 如果你要**从公司电脑远程连这台机器的 MySQL**：本机 Docker 已经把 3306 映射出来了，
> 在公司电脑用 `本机IP:3306` 连即可 —— 但**前提是两台机器在同一内网**（或你们有 VPN）。
> 不同内网的话这条路走不通，用方案 B。

---

## 方案 B · 装 MySQL 8.0（公司电脑上，15 分钟）

1. 下载 MySQL Community Server 8.0（或 8.4 LTS）
2. 安装时选 **Developer Default** 或 **Server only**，记住 root 密码
3. 勾选 "MySQL as a Windows Service"，开机自启
4. 手写一个 `init.sql`（本目录那份）在 **MySQL Workbench** 或命令行里执行：

```powershell
mysql -h 127.0.0.1 -P 3306 -u root -p < init.sql
```

> ⚠️ 装完先执行 `SELECT VERSION();` 确认能连上，再看 `SHOW DATABASES;` 有没有 `practice`。

---

## 方案 C · 用公司现成的库（最快，但要申请）

如果公司有测试库/开发库，找 DBA 或同事要：
- host / port / 用户名 / 密码 / 数据库名
- **只读还是可写**（练习 INSERT/UPDATE/DELETE 需要可写权限）
- **千万不要在正式库上练增删改！**

---

## DBX 连接参数（同事推荐的工具）

DBX 是 [dbxio.com](https://dbxio.com/cn) 的轻量数据库客户端（约 20~25MB，支持 MySQL / PostgreSQL / Redis 等 100+ 种数据库）。

新建连接时填：

| 字段 | 值 |
|---|---|
| 类型 | MySQL |
| Host | `127.0.0.1`（本机 Docker/安装）或公司给的地址 |
| Port | `3306` |
| User | `root`（或公司给的账号） |
| Password | Docker 方案是 `123456`；安装方案是你自己设的；公司库用公司给的 |
| Database | `practice` |

连上后打开 SQL 编辑器，粘贴 [init.sql](init.sql) 整个文件执行一次（仅首次）。

**连不上时的排查顺序**：
1. MySQL 服务/容器起了吗？`docker compose ps` 或 `net start | findstr -i mysql`
2. 端口通吗？`Test-NetConnection 127.0.0.1 -Port 3306`
3. 密码对不对（Docker 的是 `123456`）
4. 公司网络限制？换方案 B 本机装

---

## 今天（10-20）白天的用法

```text
① 15 分钟：把 MySQL 跑起来 + DBX 连上 + init.sql 执行完
② 90 分钟：读《数据库基础理论》→ 做 25 题自测
   → exercises/stage2/sql/day01/01-数据库基础理论.md
③ 1.5 小时：SELECT 12 题，在 MySQL 上做一遍（对照同一目录 README 的预期结果）
④ 3 小时：增删改查 12 题（同一个 README 的第 3 部分，考试核心）
```

> 为什么要在 MySQL 上做题：考试是机考 MySQL，**手感要在目标环境里练**。
> 你在 SQLite 写对的语句，MySQL 里可能因为 `DECIMAL` 显示、`DATE` 类型、大小写规则不同而报错。
