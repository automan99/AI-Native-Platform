"""
AI Native 研发平台 - Authentication API
"""
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['GET'])
def get_login_url():
    """获取 GitLab OAuth2 登录 URL"""
    state = request.args.get('state', 'random_state')
    auth_url = AuthService.get_gitlab_authorize_url(state)
    return jsonify({
        'success': True,
        'data': {
            'auth_url': auth_url
        }
    })


@auth_bp.route('/login', methods=['POST'])
def login_with_password():
    """使用用户名/邮箱和密码登录"""
    data = request.get_json()
    login = data.get('login')  # 用户名或邮箱
    password = data.get('password')

    if not login or not password:
        return jsonify({
            'success': False,
            'message': '用户名/邮箱和密码不能为空'
        }), 400

    user, result = AuthService.authenticate_by_password(login, password)

    if user is None:
        return jsonify({
            'success': False,
            'message': result or '登录失败'
        }), 400

    return jsonify({
        'success': True,
        'data': {
            'token': result,
            'user': user.to_dict()
        }
    })


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    import re
    data = request.get_json()
    username = data.get('username', '').strip() if data.get('username') else ''
    email = data.get('email', '').strip().lower() if data.get('email') else ''
    password = data.get('password', '')
    name = data.get('name', '').strip() if data.get('name') else username

    # 验证输入
    if not username or not email or not password:
        return jsonify({
            'success': False,
            'message': '用户名、邮箱和密码不能为空'
        }), 400

    # 验证用户名格式（3-20个字符，字母数字下划线）
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return jsonify({
            'success': False,
            'message': '用户名只能包含字母、数字和下划线，长度3-20个字符'
        }), 400

    # 验证邮箱格式（更宽松的验证，支持新顶级域名）
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({
            'success': False,
            'message': '邮箱格式不正确'
        }), 400

    # 验证密码长度
    if len(password) < 6:
        return jsonify({
            'success': False,
            'message': '密码长度至少为6个字符'
        }), 400

    user, message = AuthService.register_user(username, email, password, name)

    if user is None:
        return jsonify({
            'success': False,
            'message': message
        }), 400

    return jsonify({
        'success': True,
        'message': message,
        'data': user.to_dict()
    }), 201


@auth_bp.route('/callback', methods=['POST'])
def oauth_callback():
    """OAuth2 回调处理"""
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({
            'success': False,
            'message': 'Authorization code is required'
        }), 400

    user, result = AuthService.authenticate_user(code)

    if user is None:
        return jsonify({
            'success': False,
            'message': result or 'Authentication failed'
        }), 400

    return jsonify({
        'success': True,
        'data': {
            'token': result,
            'user': user.to_dict()
        }
    })


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """获取当前登录用户信息"""
    from app.utils.decorators import optional_token

    # 使用 optional_token 装饰器的逻辑
    @optional_token
    def _get_current_user():
        if request.current_user:
            return jsonify({
                'success': True,
                'data': request.current_user.to_dict()
            })
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401

    return _get_current_user()


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """登出（客户端删除 token 即可）"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })
