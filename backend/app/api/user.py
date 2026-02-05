"""
User API - 用户配置管理 API
"""
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.utils.decorators import token_required
from app.services.user_service import UserService

user_bp = Blueprint('user', __name__)

# 允许的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@user_bp.route('/avatar/upload', methods=['POST'])
@token_required
def upload_avatar(current_user):
    """上传头像文件"""
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '请选择文件'}), 400

    file = request.files['file']

    # 检查文件名
    if file.filename == '':
        return jsonify({'success': False, 'message': '请选择文件'}), 400

    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '只支持 PNG、JPG、JPEG、GIF、WEBP 格式的图片'}), 400

    # 检查文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': '文件大小不能超过 5MB'}), 400

    # 生成唯一文件名
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

    # 确保上传目录存在
    upload_dir = os.path.join(current_app.root_path, '..', 'uploads', 'avatars')
    os.makedirs(upload_dir, exist_ok=True)

    # 保存文件
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)

    # 生成访问 URL
    avatar_url = f"/uploads/avatars/{unique_filename}"

    # 更新用户头像
    result = UserService.update_avatar(current_user['id'], avatar_url)

    if result['success']:
        return jsonify(result)
    else:
        # 如果更新失败，删除已上传的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify(result), 404
