"""
AI Native 研发平台 - Configuration
"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """基础配置"""

    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'mysql+pymysql://root:password@localhost:3306/ai-agent-hub?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # GitLab 配置
    GITLAB_URL = os.environ.get('GITLAB_URL') or 'https://gitlab.com'
    GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN') or ''

    # GitLab OAuth2 配置
    GITLAB_CLIENT_ID = os.environ.get('GITLAB_CLIENT_ID') or ''
    GITLAB_CLIENT_SECRET = os.environ.get('GITLAB_CLIENT_SECRET') or ''
    GITLAB_REDIRECT_URI = os.environ.get('GITLAB_REDIRECT_URI') or 'http://localhost:5173/auth/callback'

    # JWT 配置
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS') or '168')  # 默认7天

    # 同步配置
    SYNC_INTERVAL_MINUTES = int(os.environ.get('SYNC_INTERVAL_MINUTES') or '60')

    # Git 仓库存储目录
    GIT_REPOS_DIR = os.environ.get('GIT_REPOS_DIR') or './git_repos'

    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
