"""
User API - 用户配置管理 API
"""
from flask import Blueprint, request, jsonify
from app.utils.decorators import token_required
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """获取当前用户详细信息"""
    result = UserService.get_profile(current_user['id'])
    if result is None:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    return jsonify({'success': True, 'data': result})


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """更新用户信息"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请提供要更新的信息'}), 400

    result = UserService.update_profile(current_user['id'], data)

    if result['success']:
        return jsonify(result)
    else:
        status_code = 400 if '已存在' in result['message'] else 404
        return jsonify(result), status_code


@user_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """修改密码"""
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': '请提供密码信息'}), 400

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'success': False, 'message': '请提供旧密码和新密码'}), 400

    result = UserService.change_password(current_user['id'], old_password, new_password)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400


@user_bp.route('/avatar', methods=['PUT'])
@token_required
def update_avatar(current_user):
    """更新头像 URL"""
    data = request.get_json()

    if not data or 'avatar_url' not in data:
        return jsonify({'success': False, 'message': '请提供头像 URL'}), 400

    avatar_url = data['avatar_url']

    if not avatar_url:
        return jsonify({'success': False, 'message': '头像 URL 不能为空'}), 400

    result = UserService.update_avatar(current_user['id'], avatar_url)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 404
