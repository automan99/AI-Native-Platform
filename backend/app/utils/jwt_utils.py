"""
AI Native 研发平台 - JWT Utilities
"""
import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_token(user_id, expires_in=None):
    """生成 JWT token"""
    if expires_in is None:
        expires_in = current_app.config.get('JWT_EXPIRATION_HOURS', 24 * 7)  # 默认7天

    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def decode_token(token):
    """解码 JWT token"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_id_from_token(token):
    """从 token 中获取用户 ID"""
    payload = decode_token(token)
    if payload:
        return payload.get('user_id')
    return None
