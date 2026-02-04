# AI Native 研发平台

AI Native 研发平台 - 统一管理 Skill、MCP、Hook 三类 AI Agent 资源。

## 项目简介

AI Native 研发平台 是一个 AI Native 研发平台，用于管理和发现 AI Agent 相关资源（Skill、MCP、Hook）的统一平台。平台通过对接 GitLab/GitHub 仓库自动发现和同步资源，支持用户认证、仓库管理、资源浏览、统计分析等功能，为开发者提供便捷的查询、查看和安装服务。

## 功能特性

### 前端功能
- **资源管理**: 支持 Skill、MCP、Hook 三类资源的查询和浏览
- **资源详情**: 展示资源的完整信息、README 文档、安装命令
- **统计分析**: 实时显示资源使用量和安装量统计
- **仓库管理**: 添加、删除 GitLab/GitHub 仓库，手动/自动同步资源
- **用户认证**: 支持 GitLab OAuth2 和邮箱密码登录

### 后端功能
- **GitLab/GitHub 集成**: 自动从 GitLab/GitHub 仓库发现和同步资源
- **定时同步**: 支持定时自动同步和手动同步
- **RESTful API**: 完整的 REST API 接口
- **统计服务**: 记录资源浏览和安装行为
- **用户系统**: 支持用户注册、登录、权限管理

## 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 后端框架 | Python 3.8+ + Flask 3.0 | RESTful API 框架 |
| 前端框架 | Vue.js 3 + Vite | 现代化前端框架 |
| 数据库 | MySQL 5.7+ | 关系型数据库 |
| ORM | SQLAlchemy | Python ORM 框架 |
| 任务调度 | APScheduler | Python 定时任务库 |
| 版本控制 | GitLab API / GitHub API | 仓库集成 |
| 认证授权 | JWT + OAuth2 | 用户认证 |
| HTTP 客户端 | Axios | 前端 HTTP 请求 |

## 目录结构

```
ai-agent-hub/
├── backend/                      # 后端代码
│   ├── app/
│   │   ├── models/              # 数据库模型
│   │   │   ├── user.py         # 用户模型
│   │   │   ├── repository.py   # 仓库模型
│   │   │   ├── resource.py     # 资源模型
│   │   │   ├── mcp_server.py   # MCP 服务器模型
│   │   │   ├── sync_log.py     # 同步日志模型
│   │   │   └── stat.py         # 统计模型
│   │   ├── schemas/             # API 数据模式
│   │   │   ├── resource.py     # 资源模式
│   │   │   └── repository.py   # 仓库模式
│   │   ├── services/            # 业务逻辑
│   │   │   ├── auth_service.py # 认证服务
│   │   │   ├── repository_service.py # 仓库服务
│   │   │   ├── resource_service.py   # 资源服务
│   │   │   ├── mcp_service.py        # MCP 服务
│   │   │   ├── stats_service.py      # 统计服务
│   │   │   ├── sync_service.py       # 同步服务
│   │   │   └── scheduler_service.py  # 定时任务服务
│   │   ├── api/                 # API 路由
│   │   │   ├── auth.py         # 认证接口
│   │   │   ├── repositories.py # 仓库接口
│   │   │   ├── resources.py    # 资源接口
│   │   │   ├── mcp.py          # MCP 接口
│   │   │   └── stats.py        # 统计接口
│   │   ├── sync/                # 同步器
│   │   │   ├── base_syncer.py  # 基础同步器
│   │   │   └── gitlab_syncer.py # GitLab 同步器
│   │   ├── utils/               # 工具函数
│   │   │   ├── jwt_utils.py    # JWT 工具
│   │   │   ├── password_utils.py # 密码工具
│   │   │   ├── crypto.py       # 加密工具
│   │   │   ├── gitlab_client.py # GitLab 客户端
│   │   │   └── github_client.py # GitHub 客户端
│   │   ├── config.py            # 配置文件
│   │   └── __init__.py          # 应用初始化
│   ├── requirements.txt          # Python 依赖
│   ├── init_db.py               # 数据库初始化脚本
│   ├── migrate_*.py             # 数据库迁移脚本
│   ├── run.py                   # 启动文件
│   └── venv/                    # 虚拟环境（可选）
├── frontend/                     # 前端代码
│   ├── src/
│   │   ├── api/                 # API 调用
│   │   ├── views/               # 页面组件
│   │   ├── router/              # 路由配置
│   │   ├── App.vue              # 根组件
│   │   └── main.js              # 入口文件
│   ├── package.json             # Node 依赖
│   ├── vite.config.js           # Vite 配置
│   └── node_modules/            # Node 依赖
├── docs/                        # 文档
│   └── 需求.md                  # 需求文档
├── .env.example                 # 环境变量模板
└── README.md                    # 项目说明
```

## 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本
- **MySQL**: 5.7 或更高版本
- **Git**: 用于克隆仓库

### 后端安装

#### 1. 创建虚拟环境（推荐）

使用虚拟环境可以避免依赖冲突：

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置数据库

创建 MySQL 数据库：

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选）
CREATE USER 'aiagent'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ai_agent_hub.* TO 'aiagent'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. 配置环境变量

复制环境变量模板并根据需要修改：

```bash
# 在项目根目录
cp .env.example .env

# 编辑 .env 文件，修改数据库连接信息等
```

环境变量说明：

- `SECRET_KEY`: Flask 密钥，生产环境必须修改
- `DATABASE_URL`: 数据库连接字符串
- `GITLAB_URL`: GitLab 服务器地址
- `GITLAB_TOKEN`: GitLab 访问令牌
- `GITLAB_CLIENT_ID`: GitLab OAuth2 客户端 ID（可选）
- `GITLAB_CLIENT_SECRET`: GitLab OAuth2 客户端密钥（可选）
- `JWT_EXPIRATION_HOURS`: JWT 过期时间（小时）
- `SYNC_INTERVAL_MINUTES`: 定时同步间隔（分钟）

#### 4. 初始化数据库

使用初始化脚本创建数据库表：

```bash
# 在 backend 目录下
python init_db.py init
```

其他数据库操作命令：

```bash
# 重置数据库（删除所有表并重新创建）
python init_db.py reset

# 删除所有表
python init_db.py drop
```

#### 5. 运行数据库迁移（可选）

如果需要添加新的数据库字段或表结构变更，运行迁移脚本：

```bash
# 添加仓库相关字段
python migrate_repositories_full.py

# 添加用户认证字段
python migrate_db.py

# 添加仓库类型字段
python migrate_add_repo_type.py
```

详细迁移说明请参考 [数据库迁移指南](#数据库迁移指南)。

#### 6. 启动后端服务

```bash
# 在 backend 目录下
python run.py
```

后端服务将运行在 `http://localhost:5000`

### 前端安装

#### 1. 安装依赖

```bash
# 进入前端目录
cd frontend

# 安装 npm 依赖
npm install
```

#### 2. 启动开发服务器

```bash
npm run dev
```

前端服务将运行在 `http://localhost:5173`

#### 3. 构建生产版本

```bash
npm run build
```

构建产物将输出到 `frontend/dist` 目录。

## API 接口

### 资源接口
- `GET /api/resources` - 获取资源列表
- `GET /api/resources/<id>` - 获取资源详情
- `POST /api/resources/<id>/install` - 记录安装行为
- `GET /api/resources/top` - 获取热门资源
- `GET /api/resources/latest` - 获取最新资源

### 仓库接口
- `GET /api/repositories` - 获取仓库列表
- `POST /api/repositories` - 添加仓库
- `DELETE /api/repositories/<id>` - 删除仓库
- `POST /api/repositories/<id>/sync` - 同步仓库
- `GET /api/repositories/<id>/status` - 获取同步状态

### 统计接口
- `GET /api/stats/overview` - 获取平台首页统计
- `GET /api/stats/top` - 获取热门资源排行
- `GET /api/stats/latest` - 获取最新资源

## 仓库规范

为了让平台能正确发现资源，仓库需要遵循以下目录结构：

```
gitlab-repo/ 或 github-repo/
├── skills/              # Skill 定义目录
│   ├── skill-1/
│   │   ├── skill.yaml   # Skill 元数据
│   │   ├── README.md
│   │   └── ...
│   └── skill-2/
├── mcp/                 # MCP Server 定义目录
│   ├── mcp-1/
│   │   ├── mcp.yaml     # MCP 元数据
│   │   ├── README.md
│   │   └── ...
│   └── mcp-2/
└── hooks/               # Hook 定义目录
    ├── hook-1/
    │   ├── hook.yaml    # Hook 元数据
    │   ├── README.md
    │   └── ...
    └── hook-2/
```

### 元数据文件格式 (YAML)

```yaml
# skill.yaml / mcp.yaml / hook.yaml
name: "示例资源名称"
identifier: "example-resource"
version: "1.0.0"
description: "资源描述信息"
author: "作者名"
tags:
  - "tag1"
  - "tag2"
```

## 数据库迁移指南

### 迁移脚本说明

项目包含多个数据库迁移脚本，用于在不同阶段添加新的数据库字段或表结构。所有迁移脚本都位于 `backend/` 目录下。

### 可用的迁移脚本

#### 1. migrate_repositories_full.py - 仓库表完整迁移

添加 repositories 表的所有必要字段，包括：
- 用户关联 (user_id)
- 仓库描述 (description)
- 分支信息 (branch)
- 路径配置 (path)
- 认证配置 (auth_type, auth_token, ssh_key)
- 同步配置 (sync_mode, sync_interval, sync_enabled, enabled)
- 同步状态 (sync_status, last_sync_at, last_sync_status, error_message)
- Webhook 配置 (webhook_secret, webhook_url)

**使用场景**：全新安装或需要完整的仓库表结构

**运行方法**：
```bash
cd backend
python migrate_repositories_full.py
```

#### 2. migrate_db.py - 用户认证字段迁移

为 users 表添加邮箱密码认证相关字段：
- username - 用户名
- email - 邮箱
- password_hash - 密码哈希
- name - 显示名称
- avatar_url - 头像 URL
- is_active - 是否激活
- email_verified - 邮箱是否验证
- last_login_at - 最后登录时间

**使用场景**：需要启用邮箱密码登录功能

**运行方法**：
```bash
cd backend
python migrate_db.py
```

#### 3. migrate_add_repo_type.py - 仓库类型迁移

添加仓库类型支持：
- repo_type - 仓库类型（gitlab/github）
- github_repo_info - GitHub 仓库信息

**使用场景**：需要支持 GitHub 仓库

**运行方法**：
```bash
cd backend
python migrate_add_repo_type.py
```

#### 4. migrate_repositories.py - 用户 ID 迁移

为 repositories 表添加 user_id 字段，用于关联仓库与用户。

**使用场景**：早期版本升级，需要添加用户关联

**运行方法**：
```bash
cd backend
python migrate_repositories.py
```

### 新环境初始化流程

对于全新安装的项目，建议按以下顺序执行：

```bash
# 1. 创建数据库
mysql -u root -p
CREATE DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库连接信息

# 3. 初始化数据库表
cd backend
python init_db.py init

# 4. 运行完整迁移（添加所有必要字段）
python migrate_repositories_full.py

# 5. 运行用户认证迁移（如果需要邮箱登录）
python migrate_db.py

# 6. 运行仓库类型迁移（如果需要支持 GitHub）
python migrate_add_repo_type.py

# 7. 启动服务
python run.py
```

### 现有环境升级流程

如果已有旧版本数据库，需要谨慎处理：

```bash
# 1. 备份数据库（重要！）
mysqldump -u root -p ai_agent_hub > backup_$(date +%Y%m%d).sql

# 2. 根据需要运行迁移脚本
# 迁移脚本会自动检查字段是否已存在，避免重复添加
python migrate_repositories_full.py
python migrate_db.py
python migrate_add_repo_type.py

# 3. 验证迁移结果
mysql -u root -p ai_agent_hub
DESCRIBE repositories;
DESCRIBE users;
```

### 迁移脚本特性

所有迁移脚本都包含以下安全特性：

1. **字段存在性检查**：运行前会检查字段是否已存在
2. **幂等性**：可以安全地多次运行同一脚本
3. **错误处理**：失败时不会破坏现有数据
4. **详细日志**：显示每个操作的执行状态

### 常见问题

**Q: 迁移脚本失败了怎么办？**

A: 检查数据库连接配置，确保 DATABASE_URL 正确。如果数据已损坏，使用备份恢复：

```bash
mysql -u root -p ai_agent_hub < backup_YYYYMMDD.sql
```

**Q: 如何查看当前数据库结构？**

A: 使用 MySQL 命令查看表结构：

```bash
mysql -u root -p ai_agent_hub
DESCRIBE table_name;
SHOW CREATE TABLE table_name;
```

**Q: 是否需要按顺序运行所有迁移脚本？**

A: 新环境建议按顺序运行。现有环境可以按需运行，脚本会自动跳过已存在的字段。

## 配置说明

### 后端配置 (backend/app/config.py)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| SECRET_KEY | Flask 密钥 | dev-secret-key |
| DATABASE_URL | 数据库连接字符串 | MySQL 本地连接 |
| GITLAB_URL | GitLab 服务器地址 | https://gitlab.com |
| GITLAB_TOKEN | GitLab 访问令牌 | - |
| GITLAB_CLIENT_ID | GitLab OAuth2 客户端 ID | - |
| GITLAB_CLIENT_SECRET | GitLab OAuth2 客户端密钥 | - |
| JWT_EXPIRATION_HOURS | JWT 过期时间（小时） | 168 (7天) |
| SYNC_INTERVAL_MINUTES | 定时同步间隔(分钟) | 60 |
| GIT_REPOS_DIR | Git 仓库存储目录 | ./git_repos |

### 定时同步

平台默认每 60 分钟自动同步所有启用的仓库。可在 `config.py` 中修改 `SYNC_INTERVAL_MINUTES` 配置，或通过环境变量 `SYNC_INTERVAL_MINUTES` 设置。

## 开发计划

### 已完成功能

- [x] 数据库设计与创建
- [x] 后端基础框架搭建
- [x] GitLab/GitHub 同步服务开发
- [x] 后端 API 开发
- [x] 前端页面开发
- [x] 定时任务配置
- [x] 用户认证系统（OAuth2 + 邮箱密码）
- [x] 仓库管理功能
- [x] 资源管理功能
- [x] 统计分析功能
- [x] MCP 服务器管理
- [x] 数据库迁移脚本

### 计划中功能

- [ ] 单元测试和集成测试
- [ ] API 文档生成（Swagger/OpenAPI）
- [ ] Docker 部署支持
- [ ] CI/CD 流程配置
- [ ] 性能优化
- [ ] 日志系统完善
- [ ] 监控和告警
- [ ] 国际化支持

## 相关文档

- [数据库迁移指南](DATABASE_MIGRATION.md) - 详细的数据库迁移说明和最佳实践
- [需求文档](需求.md) - 项目需求说明

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提 Issue。
