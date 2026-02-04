# AI Native 研发平台 - 快速开始指南

本指南帮助您在 5-10 分钟内快速搭建 AI Native 研发平台 开发环境。

## 前置条件检查

在开始之前，请确保您的系统已安装以下软件：

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 检查 Node.js 版本（需要 16+）
node --version

# 检查 MySQL 版本（需要 5.7+）
mysql --version

# 检查 Git
git --version
```

如果未安装，请先安装相应软件：

- **Python**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Node.js**: [https://nodejs.org/](https://nodejs.org/)
- **MySQL**: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
- **Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)

## 一键启动脚本

### Windows 用户

创建文件 `start.bat`：

```batch
@echo off
echo ========================================
echo AI Native 研发平台 - 快速启动
echo ========================================

echo.
echo [1/4] 创建并配置数据库...
mysql -u root -p < create_database.sql
if errorlevel 1 (
    echo 数据库创建失败，请检查 MySQL 密码
    pause
    exit /b 1
)

echo.
echo [2/4] 配置环境变量...
if not exist .env (
    copy .env.example .env
    echo 请编辑 .env 文件，配置数据库连接信息
    pause
)

echo.
echo [3/4] 初始化后端...
cd backend
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
python init_db.py init
python migrate_repositories_full.py
python migrate_db.py
python migrate_add_repo_type.py

echo.
echo [4/4] 启动服务...
start cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python run.py"
timeout /t 3 /nobreak > nul
start cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo 服务启动完成！
echo 后端: http://localhost:5000
echo 前端: http://localhost:5173
echo ========================================
pause
```

### Linux/Mac 用户

创建文件 `start.sh`：

```bash
#!/bin/bash

echo "========================================"
echo "AI Native 研发平台 - 快速启动"
echo "========================================"

echo ""
echo "[1/4] 创建并配置数据库..."
mysql -u root -p < create_database.sql
if [ $? -ne 0 ]; then
    echo "数据库创建失败，请检查 MySQL 密码"
    exit 1
fi

echo ""
echo "[2/4] 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件，配置数据库连接信息"
    read -p "按 Enter 继续..."
fi

echo ""
echo "[3/4] 初始化后端..."
cd backend
if [ ! -d venv ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python init_db.py init
python migrate_repositories_full.py
python migrate_db.py
python migrate_add_repo_type.py

echo ""
echo "[4/4] 启动服务..."
cd ..
gnome-terminal -- bash -c "cd backend && source venv/bin/activate && python run.py; exec bash"
sleep 3
gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash"

echo ""
echo "========================================"
echo "服务启动完成！"
echo "后端: http://localhost:5000"
echo "前端: http://localhost:5173"
echo "========================================"
```

创建数据库初始化脚本 `create_database.sql`：

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 显示成功消息
SELECT 'Database created successfully!' AS Message;
```

## 手动快速启动

如果您更喜欢手动操作，请按照以下步骤：

### 步骤 1: 创建数据库（1 分钟）

```bash
# 登录 MySQL
mysql -u root -p

# 执行以下 SQL 命令
CREATE DATABASE ai_agent_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 步骤 2: 配置环境变量（1 分钟）

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，修改数据库连接信息
# Windows: notepad .env
# Linux/Mac: nano .env
```

修改以下配置：

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/ai-agent-hub?charset=utf8mb4
SECRET_KEY=your-secret-key-here
```

### 步骤 3: 初始化后端（3-5 分钟）

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

# 初始化数据库
python init_db.py init

# 运行迁移脚本
python migrate_repositories_full.py
python migrate_db.py
python migrate_add_repo_type.py

# 启动后端服务
python run.py
```

### 步骤 4: 启动前端（1-2 分钟）

打开新的终端窗口：

```bash
# 进入前端目录
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

## 验证安装

### 检查后端服务

```bash
# 访问健康检查接口
curl http://localhost:5000/health

# 预期输出
# {"status":"ok"}
```

### 检查前端服务

在浏览器中访问：
- 前端界面: http://localhost:5173
- 后端 API: http://localhost:5000

## 常见问题

### Q1: MySQL 连接失败

**错误**: `Can't connect to MySQL server on 'localhost'`

**解决**:
1. 检查 MySQL 服务是否启动
   ```bash
   # Windows
   net start MySQL

   # Linux/Mac
   sudo service mysql start
   # 或
   sudo systemctl start mysql
   ```

2. 检查 MySQL 密码是否正确
3. 确认数据库已创建

### Q2: Python 依赖安装失败

**错误**: `pip install` 失败

**解决**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 前端端口被占用

**错误**: `Port 5173 is already in use`

**解决**:
```bash
# 查找占用端口的进程
# Windows
netstat -ano | findstr :5173

# Linux/Mac
lsof -i :5173

# 杀死进程或修改端口
# 修改 frontend/vite.config.js 中的 server.port
```

### Q4: 数据库迁移失败

**错误**: 迁移脚本执行失败

**解决**:
1. 检查 .env 文件中的数据库连接配置
2. 确认数据库已创建
3. 查看详细的错误信息，参考 [数据库迁移指南](DATABASE_MIGRATION.md)

### Q5: 虚拟环境激活失败

**错误**: `venv\Scripts\activate` 失败

**解决**:
```bash
# Windows PowerShell 可能需要修改执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 或使用 Command Prompt (cmd) 而不是 PowerShell
```

## 下一步

安装完成后，您可以：

1. **添加仓库**: 通过前端界面添加 GitLab 或 GitHub 仓库
2. **同步资源**: 手动或自动同步仓库中的资源
3. **浏览资源**: 查看 Skill、MCP、Hook 等资源
4. **查看统计**: 查看资源使用统计

## 开发模式提示

### 后端开发

```bash
# 自动重启服务（需要安装 flask）
pip install Flask==3.0.0

# 开启调试模式
# 在 run.py 中设置 debug=True
app.run(host='0.0.0.0', port=5000, debug=True)
```

### 前端开发

```bash
# 热重载已默认启用
# 修改代码后自动刷新浏览器

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 获取帮助

如果遇到问题：

1. 查看 [数据库迁移指南](DATABASE_MIGRATION.md)
2. 查看 [README.md](README.md) 完整文档
3. 检查日志文件
4. 提交 Issue 并附上错误信息

## 停止服务

```bash
# 停止后端: Ctrl+C 或关闭终端
# 停止前端: Ctrl+C 或关闭终端

# 停止虚拟环境
deactivate
```

## 生产环境部署

对于生产环境部署，请参考：

- 使用 Docker 部署
- 配置 Nginx 反向代理
- 使用 Gunicorn/uWSGI 运行后端
- 配置 HTTPS
- 设置环境变量
- 配置日志和监控

（生产部署文档正在完善中）

祝您使用愉快！
