"""
AI Native 研发平台 - Flask Application
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """创建 Flask 应用"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 启用 CORS
    CORS(app)

    # 初始化数据库
    db.init_app(app)

    # 注册蓝图
    from app.api.resources import resources_bp
    from app.api.repositories import repositories_bp
    from app.api.stats import stats_bp
    from app.api.auth import auth_bp
    from app.api.mcp import mcp_bp
    from app.api.user import user_bp

    # auth_bp 已有 url_prefix，不需要再添加
    app.register_blueprint(resources_bp, url_prefix='/api')
    app.register_blueprint(repositories_bp, url_prefix='/api')
    app.register_blueprint(stats_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)  # 使用 blueprint 中定义的 url_prefix
    app.register_blueprint(mcp_bp)  # MCP blueprint 已有 url_prefix
    app.register_blueprint(user_bp, url_prefix='/api/user')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    # 创建 Git 仓库存储目录
    git_repos_dir = app.config.get('GIT_REPOS_DIR', './git_repos')
    os.makedirs(git_repos_dir, exist_ok=True)

    # 初始化定时任务
    from app.services.scheduler_service import init_scheduler
    init_scheduler(app)

    return app
