"""
User Service - 用户配置管理服务
"""
from datetime import datetime
from app import db
from app.models.user import User
from app.utils.password_utils import verify_password, hash_password


class UserService:
    """用户服务类"""

    @staticmethod
    def get_profile(user_id):
        """获取用户详细信息"""
        user = User.query.get(user_id)
        if not user:
            return None
        return user.to_dict()

    @staticmethod
    def update_profile(user_id, data):
        """
        更新用户信息
        data: dict 包含 username, name, email 等字段
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'message': '用户不存在'}

        errors = []
        update_data = {}

        # 验证并更新 username
        if 'username' in data and data['username']:
            username = data['username']
            if username != user.username:
                existing = User.query.filter_by(username=username).first()
                if existing:
                    errors.append('用户名已存在')
                else:
                    update_data['username'] = username

        # 验证并更新 name
        if 'name' in data:
            update_data['name'] = data['name']

        # 验证并更新 email
        if 'email' in data and data['email']:
            email = data['email']
            if email != user.email:
                existing = User.query.filter_by(email=email).first()
                if existing:
                    errors.append('邮箱已被使用')
                else:
                    update_data['email'] = email

        if errors:
            return {'success': False, 'message': ', '.join(errors)}

        # 更新数据
        for key, value in update_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            'success': True,
            'message': '个人信息更新成功',
            'data': user.to_dict()
        }

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        修改密码
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'message': '用户不存在'}

        # 检查用户是否有密码（OAuth用户可能没有密码）
        if not user.password_hash:
            return {'success': False, 'message': '该账户使用第三方登录，无法修改密码'}

        # 验证旧密码
        if not verify_password(old_password, user.password_hash):
            return {'success': False, 'message': '当前密码错误'}

        # 验证新密码长度
        if len(new_password) < 6:
            return {'success': False, 'message': '新密码长度不能少于6位'}

        # 更新密码
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        return {'success': True, 'message': '密码修改成功'}

    @staticmethod
    def update_avatar(user_id, avatar_url):
        """
        更新头像 URL
        """
        user = User.query.get(user_id)
        if not user:
            return {'success': False, 'message': '用户不存在'}

        user.avatar_url = avatar_url
        user.updated_at = datetime.utcnow()
        db.session.commit()

        return {
            'success': True,
            'message': '头像更新成功',
            'data': user.to_dict()
        }
