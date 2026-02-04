"""
AI Native 研发平台 - User Model
"""
from datetime import datetime
from app import db


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    gitlab_id = db.Column(db.Integer, unique=True, nullable=True)
    gitlab_username = db.Column(db.String(100))
    gitlab_email = db.Column(db.String(200))
    gitlab_avatar_url = db.Column(db.String(500))
    gitlab_token = db.Column(db.String(500))  # 存储 GitLab access token

    # 邮箱密码登录字段
    username = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(500))

    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)  # 邮箱是否已验证
    last_login_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    repositories = db.relationship('Repository', backref='owner', lazy='dynamic')

    def set_password(self, password):
        """设置密码（自动加密）"""
        from app.utils.password_utils import hash_password
        self.password_hash = hash_password(password)

    def check_password(self, password):
        """验证密码"""
        from app.utils.password_utils import verify_password
        return verify_password(password, self.password_hash)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'gitlab_id': self.gitlab_id,
            'gitlab_username': self.gitlab_username,
            'gitlab_email': self.gitlab_email,
            'gitlab_avatar_url': self.gitlab_avatar_url,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def get_token(self):
        """获取 JWT token"""
        from app.utils.jwt_utils import generate_token
        return generate_token(self.id)

    def __repr__(self):
        return f'<User {self.name or self.username or self.gitlab_username}>'
