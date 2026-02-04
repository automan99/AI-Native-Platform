"""
AI Native 研发平台 - Repository Model
"""
from datetime import datetime
from app import db


class Repository(db.Model):
    """Git 仓库模型（支持 GitLab 和 GitHub）"""
    __tablename__ = 'repositories'

    # 基础字段
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    repo_type = db.Column(db.String(20), default='gitlab')  # gitlab/github
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False, unique=True)

    # Git 配置
    branch = db.Column(db.String(100), default='main')
    path = db.Column(db.String(500))  # 仓库内的代码路径

    # 认证配置
    auth_type = db.Column(db.String(20), default='public')  # public/token/ssh
    auth_token = db.Column(db.String(500))  # 加密存储
    ssh_key = db.Column(db.Text)  # 加密存储

    # GitLab 配置
    gitlab_project_id = db.Column(db.Integer)

    # GitHub 配置
    github_repo_info = db.Column(db.String(200))  # owner/repo 格式

    # 同步配置
    sync_mode = db.Column(db.String(20), default='manual')  # manual/scheduled/webhook
    sync_interval = db.Column(db.Integer, default=60)  # 定时同步间隔（分钟）
    sync_enabled = db.Column(db.Boolean, default=True)
    enabled = db.Column(db.Boolean, default=True)  # 整体启用状态

    # 同步状态
    sync_status = db.Column(db.String(20), default='pending')  # pending/syncing/success/failed
    last_sync_at = db.Column(db.DateTime)
    last_sync_status = db.Column(db.String(20))
    error_message = db.Column(db.Text)

    # Webhook 配置
    webhook_secret = db.Column(db.String(500))  # 加密存储
    webhook_url = db.Column(db.String(500))  # Webhook 回调地址

    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    resources = db.relationship('Resource', backref='repository', lazy='dynamic', cascade='all, delete-orphan')
    sync_logs = db.relationship('SyncLog', backref='repository', lazy='dynamic', order_by='desc(SyncLog.created_at)')

    def to_dict(self, include_sensitive=False):
        """
        转换为字典

        Args:
            include_sensitive: 是否包含敏感信息（token、ssh_key等）
        """
        from app.utils.crypto import CryptoUtil

        data = {
            'id': self.id,
            'user_id': self.user_id,
            'repo_type': self.repo_type,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'branch': self.branch,
            'path': self.path,
            'auth_type': self.auth_type,
            'gitlab_project_id': self.gitlab_project_id,
            'sync_mode': self.sync_mode,
            'sync_interval': self.sync_interval,
            'sync_enabled': self.sync_enabled,
            'enabled': self.enabled,
            'sync_status': self.sync_status,
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None,
            'last_sync_status': self.last_sync_status,
            'error_message': self.error_message,
            'webhook_url': self.webhook_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'resource_count': self.resources.count()
        }

        # 敏感信息处理
        if include_sensitive:
            # 包含完整的敏感信息（仅用于编辑时回显）
            data['auth_token'] = self.auth_token
            data['ssh_key'] = self.ssh_key
            data['webhook_secret'] = self.webhook_secret
        else:
            # 遮罩敏感信息
            if self.auth_token:
                data['has_auth_token'] = True
            if self.ssh_key:
                data['has_ssh_key'] = True
            if self.webhook_secret:
                data['has_webhook_secret'] = True

        return data

    def __repr__(self):
        return f'<Repository {self.name}>'
