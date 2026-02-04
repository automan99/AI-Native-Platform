# AI Native 研发平台 - 文档索引

本文档提供了 AI Native 研发平台 项目的所有文档索引和快速导航。

## 文档列表

### 核心文档

| 文档名称 | 文件路径 | 说明 | 适用对象 |
|---------|---------|------|---------|
| 项目说明 | [README.md](README.md) | 项目概述、功能特性、技术栈、安装步骤 | 所有人 |
| 快速开始 | [QUICKSTART.md](QUICKSTART.md) | 5-10 分钟快速搭建开发环境 | 新用户 |
| 数据库迁移指南 | [DATABASE_MIGRATION.md](DATABASE_MIGRATION.md) | 数据库迁移脚本使用和最佳实践 | 开发者、运维 |
| 需求文档 | [需求.md](需求.md) | 项目需求说明 | 产品经理、开发者 |

## 文档使用指南

### 新用户入门

1. **第一步**: 阅读 [README.md](README.md) 了解项目概况
2. **第二步**: 按照 [QUICKSTART.md](QUICKSTART.md) 快速搭建环境
3. **第三步**: 参考 [需求.md](需求.md) 了解业务逻辑

### 开发者指南

1. **环境搭建**: [QUICKSTART.md](QUICKSTART.md) - 手动快速启动部分
2. **数据库操作**: [DATABASE_MIGRATION.md](DATABASE_MIGRATION.md) - 迁移脚本详解
3. **API 开发**: [README.md](README.md) - API 接口部分
4. **代码结构**: [README.md](README.md) - 目录结构部分

### 运维部署

1. **生产部署**: [README.md](README.md) - 配置说明部分
2. **数据库升级**: [DATABASE_MIGRATION.md](DATABASE_MIGRATION.md) - 现有环境升级流程
3. **备份恢复**: [DATABASE_MIGRATION.md](DATABASE_MIGRATION.md) - 常见问题部分

## 快速导航

### 安装相关

- [环境要求](README.md#环境要求)
- [后端安装](README.md#后端安装)
- [前端安装](README.md#前端安装)
- [一键启动](QUICKSTART.md#一键启动脚本)

### 配置相关

- [环境变量配置](README.md#配置环境变量)
- [后端配置说明](README.md#配置说明)
- [数据库配置](DATABASE_MIGRATION.md#前置条件)

### 数据库相关

- [数据库初始化](README.md#初始化数据库)
- [数据库迁移](DATABASE_MIGRATION.md#迁移脚本说明)
- [迁移脚本列表](DATABASE_MIGRATION.md#迁移脚本列表)
- [常见问题](DATABASE_MIGRATION.md#常见问题)

### API 相关

- [资源接口](README.md#资源接口)
- [仓库接口](README.md#仓库接口)
- [统计接口](README.md#统计接口)
- [认证接口](README.md#认证接口)

### 开发相关

- [目录结构](README.md#目录结构)
- [技术栈](README.md#技术栈)
- [开发计划](README.md#开发计划)
- [仓库规范](README.md#仓库规范)

## 文档贡献

如果您发现文档有错误或需要补充，欢迎：

1. 直接修改文档并提交 PR
2. 提交 Issue 说明需要改进的地方
3. 提供使用案例和最佳实践

## 文档更新记录

### 2026-02-04

- 更新 README.md，补充完整的项目说明
- 新增 DATABASE_MIGRATION.md - 数据库迁移详细指南
- 新增 QUICKSTART.md - 快速开始指南
- 新增 DOCS.md - 文档索引
- 优化文档结构和内容组织

## 常用命令速查

### 数据库操作

```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 备份数据库
mysqldump -u root -p ai_agent_hub > backup.sql

# 恢复数据库
mysql -u root -p ai_agent_hub < backup.sql

# 查看表结构
DESCRIBE table_name;
```

### 后端操作

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py init

# 运行迁移
python migrate_repositories_full.py

# 启动服务
python run.py
```

### 前端操作

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 获取帮助

- 查看 [常见问题](QUICKSTART.md#常见问题)
- 查看 [数据库迁移常见问题](DATABASE_MIGRATION.md#常见问题)
- 提交 [GitHub Issue](https://github.com/your-repo/issues)

## 许可证

MIT License

---

最后更新: 2026-02-04
