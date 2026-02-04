# 数据库迁移指南

本文档详细说明 AI Native 研发平台 项目的数据库迁移流程和脚本使用方法。

## 目录

- [概述](#概述)
- [迁移脚本说明](#迁移脚本说明)
- [新环境初始化](#新环境初始化)
- [现有环境升级](#现有环境升级)
- [迁移脚本详解](#迁移脚本详解)
- [常见问题](#常见问题)

## 概述

数据库迁移用于在不丢失数据的情况下修改数据库结构。本项目提供多个迁移脚本，用于在不同阶段添加新的数据库字段或表结构。

所有迁移脚本都位于 `backend/` 目录下，文件名格式为 `migrate_*.py`。

## 迁移脚本说明

### 迁移脚本列表

| 脚本名称 | 功能说明 | 适用场景 |
|---------|---------|---------|
| `migrate_repositories_full.py` | 添加 repositories 表的所有必要字段 | 全新安装或需要完整的仓库表结构 |
| `migrate_db.py` | 添加用户认证相关字段 | 需要启用邮箱密码登录功能 |
| `migrate_add_repo_type.py` | 添加仓库类型支持 | 需要支持 GitHub 仓库 |
| `migrate_repositories.py` | 添加 user_id 字段 | 早期版本升级 |

### 迁移脚本特性

所有迁移脚本都包含以下安全特性：

1. **字段存在性检查**：运行前会检查字段是否已存在
2. **幂等性**：可以安全地多次运行同一脚本
3. **错误处理**：失败时不会破坏现有数据
4. **详细日志**：显示每个操作的执行状态

## 新环境初始化

### 前置条件

- MySQL 5.7+ 已安装并运行
- Python 3.8+ 已安装
- 已配置 `.env` 文件

### 初始化步骤

#### 1. 创建数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'aiagent'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ai_agent_hub.* TO 'aiagent'@'localhost';
FLUSH PRIVILEGES;

EXIT;
```

#### 2. 配置环境变量

```bash
# 在项目根目录
cp .env.example .env

# 编辑 .env 文件，设置数据库连接信息
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai-agent-hub?charset=utf8mb4
```

#### 3. 初始化数据库表

```bash
cd backend

# 创建基础表结构
python init_db.py init
```

这将创建以下表：
- `users` - 用户表
- `repositories` - 仓库表
- `resources` - 资源表（Skill/MCP/Hook）
- `mcp_servers` - MCP 服务器表
- `mcp_tools` - MCP 工具表
- `mcp_resources` - MCP 资源表
- `sync_logs` - 同步日志表
- `stats` - 统计表

#### 4. 运行迁移脚本

```bash
# 运行完整仓库表迁移（添加所有必要字段）
python migrate_repositories_full.py

# 运行用户认证迁移（如果需要邮箱登录）
python migrate_db.py

# 运行仓库类型迁移（如果需要支持 GitHub）
python migrate_add_repo_type.py
```

#### 5. 验证初始化

```bash
mysql -u root -p ai_agent_hub

# 查看所有表
SHOW TABLES;

# 查看表结构
DESCRIBE repositories;
DESCRIBE users;

EXIT;
```

#### 6. 启动服务

```bash
# 启动后端服务
python run.py
```

## 现有环境升级

对于已有旧版本数据库的环境，需要谨慎处理升级过程。

### 升级前准备

#### 1. 备份数据库（重要！）

```bash
# 备份整个数据库
mysqldump -u root -p ai_agent_hub > backup_$(date +%Y%m%d_%H%M%S).sql

# 或只备份特定表
mysqldump -u root -p ai_agent_hub repositories users resources > backup_tables_$(date +%Y%m%d).sql
```

#### 2. 检查当前数据库结构

```bash
mysql -u root -p ai_agent_hub

# 查看所有表
SHOW TABLES;

# 查看表结构
DESCRIBE repositories;
DESCRIBE users;

# 记录当前表结构，以便迁移后对比
EXIT;
```

### 升级步骤

#### 1. 停止应用服务

```bash
# 停止后端服务（如果在运行）
# Ctrl+C 或 kill 进程
```

#### 2. 运行迁移脚本

```bash
cd backend

# 根据需要运行迁移脚本
# 脚本会自动检查字段是否已存在，避免重复添加

# 运行完整仓库表迁移
python migrate_repositories_full.py

# 运行用户认证迁移
python migrate_db.py

# 运行仓库类型迁移
python migrate_add_repo_type.py
```

#### 3. 验证迁移结果

```bash
mysql -u root -p ai_agent_hub

# 查看表结构变化
DESCRIBE repositories;
DESCRIBE users;

# 验证数据完整性
SELECT COUNT(*) FROM repositories;
SELECT COUNT(*) FROM users;

EXIT;
```

#### 4. 启动应用服务

```bash
# 启动后端服务
python run.py

# 观察日志，确保没有数据库相关错误
```

### 回滚方案

如果迁移出现问题，可以使用备份恢复：

```bash
# 停止应用服务

# 恢复数据库
mysql -u root -p ai_agent_hub < backup_YYYYMMDD_HHMMSS.sql

# 验证恢复结果
mysql -u root -p ai_agent_hub
SHOW TABLES;
EXIT;

# 重新启动应用服务
```

## 迁移脚本详解

### migrate_repositories_full.py

#### 功能

为 `repositories` 表添加所有必要的字段，包括：

- `user_id` - 用户 ID（外键）
- `description` - 仓库描述
- `branch` - 分支名称
- `path` - 资源路径
- `auth_type` - 认证类型（public/token/ssh）
- `auth_token` - 认证令牌（加密存储）
- `ssh_key` - SSH 密钥（加密存储）
- `sync_mode` - 同步模式（manual/scheduled）
- `sync_interval` - 同步间隔（分钟）
- `sync_enabled` - 是否启用同步
- `enabled` - 是否启用仓库
- `sync_status` - 同步状态（pending/running/success/failed）
- `last_sync_at` - 最后同步时间
- `last_sync_status` - 最后同步状态
- `error_message` - 错误信息
- `webhook_secret` - Webhook 密钥
- `webhook_url` - Webhook URL

#### 使用方法

```bash
cd backend
python migrate_repositories_full.py
```

#### 输出示例

```
Connecting to MySQL: root@localhost:3306/ai-agent-hub
Adding column 'user_id'...
Added column 'user_id' successfully.
Adding column 'description'...
Added column 'description' successfully.
...
Column 'sync_status' already exists.
...

Migration completed successfully!
```

### migrate_db.py

#### 功能

为 `users` 表添加邮箱密码认证相关字段：

- `username` - 用户名（唯一）
- `email` - 邮箱（唯一）
- `password_hash` - 密码哈希
- `name` - 显示名称
- `avatar_url` - 头像 URL
- `is_active` - 是否激活（默认：1）
- `email_verified` - 邮箱是否验证（默认：0）
- `last_login_at` - 最后登录时间

#### 使用方法

```bash
cd backend
python migrate_db.py
```

#### 输出示例

```
Adding username column...
Adding email column...
Adding password_hash column...
Adding name column...
Adding avatar_url column...
Adding is_active column...
Adding email_verified column...
Adding last_login_at column...
Migration completed successfully!

Current users table structure:
  id: int(11)
  gitlab_id: int(11)
  gitlab_token: varchar(255)
  username: varchar(50)
  email: varchar(200)
  password_hash: varchar(255)
  name: varchar(100)
  avatar_url: varchar(500)
  is_active: tinyint(1)
  email_verified: tinyint(1)
  last_login_at: datetime
  created_at: datetime
```

### migrate_add_repo_type.py

#### 功能

为 `repositories` 表添加仓库类型支持：

- `repo_type` - 仓库类型（gitlab/github，默认：gitlab）
- `github_repo_info` - GitHub 仓库信息

#### 使用方法

```bash
cd backend
python migrate_add_repo_type.py
```

#### 输出示例

```
Connecting to MySQL: root@localhost:3306/ai-agent-hub
Adding column 'repo_type'...
Added column 'repo_type' successfully.
Adding column 'github_repo_info'...
Added column 'github_repo_info' successfully.

Migration completed successfully!
```

### migrate_repositories.py

#### 功能

为 `repositories` 表添加 `user_id` 字段，用于关联仓库与用户。

#### 使用方法

```bash
cd backend
python migrate_repositories.py
```

## 常见问题

### Q1: 迁移脚本失败了怎么办？

**A**: 首先检查数据库连接配置是否正确：

```bash
# 检查 .env 文件
cat .env | grep DATABASE_URL

# 测试数据库连接
mysql -u root -p ai_agent_hub
```

如果连接正常但迁移失败，查看错误信息。如果是数据损坏，使用备份恢复：

```bash
mysql -u root -p ai_agent_hub < backup_YYYYMMDD.sql
```

### Q2: 如何查看当前数据库结构？

**A**: 使用以下 MySQL 命令：

```bash
mysql -u root -p ai_agent_hub

# 查看所有表
SHOW TABLES;

# 查看表结构
DESCRIBE table_name;

# 查看创建表的完整 SQL
SHOW CREATE TABLE table_name;

# 查看表的索引
SHOW INDEX FROM table_name;

EXIT;
```

### Q3: 是否需要按顺序运行所有迁移脚本？

**A**:
- **新环境**：建议按以下顺序运行
  1. `init_db.py init`（创建基础表）
  2. `migrate_repositories_full.py`（添加仓库字段）
  3. `migrate_db.py`（添加用户认证字段）
  4. `migrate_add_repo_type.py`（添加仓库类型）

- **现有环境**：可以按需运行，脚本会自动跳过已存在的字段

### Q4: 迁移会影响现有数据吗？

**A**: 迁移脚本只添加新字段，不会删除或修改现有数据。但为了安全起见，运行前务必备份数据库。

### Q5: 如何验证迁移是否成功？

**A**: 检查以下方面：

```bash
# 1. 检查表结构
mysql -u root -p ai_agent_hub
DESCRIBE repositories;
DESCRIBE users;

# 2. 检查数据完整性
SELECT COUNT(*) FROM repositories;
SELECT COUNT(*) FROM users;

# 3. 启动应用，检查日志
python run.py
# 观察是否有数据库相关错误

# 4. 测试应用功能
# 访问 http://localhost:5000/health
# 检查 API 是否正常工作
```

### Q6: 迁移脚本可以重复运行吗？

**A**: 可以。所有迁移脚本都有字段存在性检查，重复运行会跳过已存在的字段，不会出错。

### Q7: 如何回滚迁移？

**A**: 如果迁移出现问题，有两种回滚方式：

**方式 1：手动删除添加的字段**

```bash
mysql -u root -p ai_agent_hub

# 删除特定字段
ALTER TABLE repositories DROP COLUMN new_column_name;

EXIT;
```

**方式 2：使用备份恢复**

```bash
# 停止应用
# 恢复备份
mysql -u root -p ai_agent_hub < backup_YYYYMMDD.sql
```

### Q8: 迁移过程中出现字符编码问题怎么办？

**A**: 确保数据库使用正确的字符集：

```bash
mysql -u root -p ai_agent_hub

# 检查数据库字符集
SHOW VARIABLES LIKE 'character_set_database';
SHOW VARIABLES LIKE 'collation_database';

# 修改数据库字符集
ALTER DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 修改表字符集
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

EXIT;
```

## 最佳实践

1. **备份优先**：运行任何迁移前，务必备份数据库
2. **测试环境先行**：先在测试环境验证迁移脚本
3. **分步执行**：不要一次运行多个迁移，分步执行并验证
4. **记录版本**：记录每次迁移的版本和变更内容
5. **监控日志**：运行迁移时注意查看日志输出
6. **数据验证**：迁移后验证数据的完整性和正确性
7. **文档更新**：及时更新数据库设计文档

## 相关文档

- [项目 README](README.md) - 项目总体说明
- [API 文档](docs/API.md) - API 接口说明（如有）
- [需求文档](需求.md) - 项目需求说明

## 技术支持

如果遇到问题，请查看：
1. 本文档的常见问题部分
2. 项目的 Issue 列表
3. 提交新的 Issue 并附上详细的错误信息
