"""
AI Native 研发平台 - Authentication Service
"""
import requests
from datetime import datetime
from app import db
from app.models.user import User
from app.utils.jwt_utils import generate_token


class AuthService:
    """认证服务"""

    @staticmethod
    def get_gitlab_authorize_url(state=None):
        """获取 GitLab OAuth2 授权 URL"""
        from flask import current_app
        config = current_app.config

        url = f"{config['GITLAB_URL']}/oauth/authorize"
        params = {
            'client_id': config['GITLAB_CLIENT_ID'],
            'redirect_uri': config['GITLAB_REDIRECT_URI'],
            'response_type': 'code',
            'scope': 'read_user profile email',
            'state': state or 'random_state'
        }
        return f"{url}?{requests.compat.urlencode(params)}"

    @staticmethod
    def exchange_code_for_token(code):
        """用授权码换取 access token"""
        from flask import current_app
        config = current_app.config

        url = f"{config['GITLAB_URL']}/oauth/token"
        data = {
            'client_id': config['GITLAB_CLIENT_ID'],
            'client_secret': config['GITLAB_CLIENT_SECRET'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': config['GITLAB_REDIRECT_URI']
        }

        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Token exchange error: {e}")
            return None

    @staticmethod
    def get_gitlab_user_info(access_token):
        """获取 GitLab 用户信息"""
        from flask import current_app
        config = current_app.config

        url = f"{config['GITLAB_URL']}/api/v4/user"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Get user info error: {e}")
            return None

    @staticmethod
    def authenticate_user(code):
        """通过 OAuth2 code 认证用户"""
        # 1. 换取 access token
        token_data = AuthService.exchange_code_for_token(code)
        if not token_data or 'access_token' not in token_data:
            return None, 'Failed to exchange code for token'

        access_token = token_data['access_token']

        # 2. 获取用户信息
        user_info = AuthService.get_gitlab_user_info(access_token)
        if not user_info:
            return None, 'Failed to get user information'

        # 3. 查找或创建用户
        gitlab_id = user_info.get('id')
        user = User.query.filter_by(gitlab_id=gitlab_id).first()

        if user:
            # 更新现有用户信息
            user.gitlab_username = user_info.get('username')
            user.gitlab_email = user_info.get('email')
            user.gitlab_avatar_url = user_info.get('avatar_url')
            user.gitlab_token = access_token
            if not user.name:
                user.name = user_info.get('name')
            if not user.avatar_url:
                user.avatar_url = user_info.get('avatar_url')
            user.last_login_at = datetime.utcnow()
        else:
            # 创建新用户
            user = User(
                gitlab_id=gitlab_id,
                gitlab_username=user_info.get('username'),
                gitlab_email=user_info.get('email'),
                gitlab_avatar_url=user_info.get('avatar_url'),
                gitlab_token=access_token,
                name=user_info.get('name'),
                avatar_url=user_info.get('avatar_url'),
                last_login_at=datetime.utcnow()
            )
            db.session.add(user)

        db.session.commit()

        # 4. 生成 JWT token
        jwt_token = generate_token(user.id)

        return user, jwt_token

    @staticmethod
    def register_user(username, email, password, name=None):
        """用户注册"""
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return None, '用户名已存在'

        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return None, '邮箱已被注册'

        # 创建新用户
        user = User(
            username=username,
            email=email,
            name=name or username,
            is_active=True,
            email_verified=False  # 默认未验证，可以后续添加邮件验证功能
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user, '注册成功'

    @staticmethod
    def authenticate_by_password(login, password):
        """通过用户名或邮箱和密码认证"""
        # 尝试用用户名登录
        user = User.query.filter_by(username=login).first()

        # 如果用户名不存在，尝试用邮箱登录
        if not user:
            user = User.query.filter_by(email=login).first()

        if not user:
            return None, '用户名或邮箱不存在'

        if not user.password_hash:
            return None, '该账号使用 GitLab 登录'

        if not user.check_password(password):
            return None, '密码错误'

        if not user.is_active:
            return None, '账号已被禁用'

        # 更新最后登录时间
        user.last_login_at = datetime.utcnow()
        db.session.commit()

        # 生成 JWT token
        jwt_token = generate_token(user.id)

        return user, jwt_token

    @staticmethod
    def get_current_user(user_id):
        """根据用户 ID 获取当前用户"""
        return User.query.get(user_id)
