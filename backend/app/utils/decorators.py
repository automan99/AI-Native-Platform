"""
AI Native 研发平台 - Authentication Decorators
"""
from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import get_user_id_from_token
from app.models.user import User


def token_required(f):
    """Token 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        # 从 header 获取 token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401

        # 验证 token
        user_id = get_user_id_from_token(token)
        if not user_id:
            return jsonify({'success': False, 'message': 'Token is invalid or expired'}), 401

        # 获取用户
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({'success': False, 'message': 'User not found or inactive'}), 401

        # 将用户信息添加到 request 对象
        request.current_user = user

        # 不传递参数，被装饰的函数通过 request.current_user 访问用户信息
        return f(*args, **kwargs)

    return decorated_function


def optional_token(f):
    """可选 Token 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                pass

        request.current_user = None

        if token:
            user_id = get_user_id_from_token(token)
            if user_id:
                user = User.query.get(user_id)
                if user and user.is_active:
                    request.current_user = user

        return f(*args, **kwargs)

    return decorated_function
