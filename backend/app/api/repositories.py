"""
AI Native 研发平台 - Repositories API
"""
from flask import Blueprint, request, jsonify
from app.services.repository_service import RepositoryService
from app.services.sync_service import SyncService
from app.utils.gitlab_client import GitLabClient
from app.utils.github_client import GitHubClient
from app.utils.decorators import token_required

repositories_bp = Blueprint('repositories', __name__)


def detect_repo_type(url):
    """检测仓库类型"""
    url = url.lower()
    if 'github.com' in url:
        return 'github'
    elif 'gitlab.com' in url or 'gitlab' in url:
        return 'gitlab'
    else:
        # 默认使用 gitlab
        return 'gitlab'


@repositories_bp.route('/repositories', methods=['GET'])
@token_required
def get_repositories():
    """获取当前用户的仓库列表"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    repositories, total = RepositoryService.get_list_by_user(
        user_id=request.current_user.id,
        page=page,
        page_size=page_size
    )

    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in repositories],
        'total': total,
        'page': page,
        'page_size': page_size
    })


@repositories_bp.route('/repositories/<int:repo_id>', methods=['GET'])
@token_required
def get_repository(repo_id):
    """获取仓库详情"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权访问该仓库'
        }), 403

    # 如果请求包含敏感信息，则返回完整数据（用于编辑）
    include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'

    return jsonify({
        'success': True,
        'data': repository.to_dict(include_sensitive=include_sensitive)
    })


@repositories_bp.route('/repositories', methods=['POST'])
@token_required
def create_repository():
    """添加仓库"""
    data = request.get_json()

    url = data.get('url')
    name = data.get('name')

    if not url or not name:
        return jsonify({
            'success': False,
            'message': 'URL 和名称不能为空'
        }), 400

    # 验证认证方式和对应字段
    auth_type = data.get('auth_type', 'public')
    if auth_type == 'token' and not data.get('auth_token'):
        return jsonify({
            'success': False,
            'message': 'Token认证方式需要提供访问令牌'
        }), 400
    if auth_type == 'ssh' and not data.get('ssh_key'):
        return jsonify({
            'success': False,
            'message': 'SSH认证方式需要提供SSH密钥'
        }), 400

    # 验证同步方式和对应字段
    sync_mode = data.get('sync_mode', 'manual')
    if sync_mode == 'scheduled':
        sync_interval = data.get('sync_interval', 60)
        if sync_interval < 1:
            return jsonify({
                'success': False,
                'message': '同步间隔必须大于0分钟'
            }), 400
    if sync_mode == 'webhook' and not data.get('webhook_secret'):
        return jsonify({
            'success': False,
            'message': 'Webhook同步方式需要提供Webhook密钥'
        }), 400

    # 检查是否已存在（仅检查当前用户的仓库）
    existing = RepositoryService.get_by_url_and_user(url, request.current_user.id)
    if existing:
        return jsonify({
            'success': False,
            'message': '仓库已存在'
        }), 400

    try:
        # 检测仓库类型
        repo_type = detect_repo_type(url)

        # 根据类型获取项目 ID
        if repo_type == 'github':
            client = GitHubClient(data.get('auth_token'))
            repo_info = client.extract_repo_info(url)
            gitlab_project_id = None
            github_repo_info = f"{repo_info['owner']}/{repo_info['repo']}"
        else:
            client = GitLabClient()
            gitlab_project_id = client.extract_project_id(url)
            github_repo_info = None

        # 创建仓库（关联当前用户）
        repository = RepositoryService.create(
            user_id=request.current_user.id,
            repo_type=repo_type,
            name=name,
            url=url,
            gitlab_project_id=gitlab_project_id,
            github_repo_info=github_repo_info,
            description=data.get('description'),
            branch=data.get('branch', 'main'),
            path=data.get('path'),
            auth_type=auth_type,
            auth_token=data.get('auth_token'),
            ssh_key=data.get('ssh_key'),
            sync_mode=sync_mode,
            sync_interval=data.get('sync_interval', 60),
            enabled=data.get('enabled', True),
            sync_enabled=data.get('sync_enabled', True),
            webhook_secret=data.get('webhook_secret'),
            webhook_url=data.get('webhook_url')
        )

        return jsonify({
            'success': True,
            'message': '仓库添加成功',
            'data': repository.to_dict()
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'添加失败: {str(e)}'
        }), 500


@repositories_bp.route('/repositories/<int:repo_id>', methods=['PUT'])
@token_required
def update_repository(repo_id):
    """更新仓库信息"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权修改该仓库'
        }), 403

    data = request.get_json()

    # 验证认证方式和对应字段
    auth_type = data.get('auth_type', repository.auth_type)
    if auth_type == 'token' and not data.get('auth_token') and not repository.auth_token:
        return jsonify({
            'success': False,
            'message': 'Token认证方式需要提供访问令牌'
        }), 400
    if auth_type == 'ssh' and not data.get('ssh_key') and not repository.ssh_key:
        return jsonify({
            'success': False,
            'message': 'SSH认证方式需要提供SSH密钥'
        }), 400

    # 验证同步方式和对应字段
    sync_mode = data.get('sync_mode', repository.sync_mode)
    if sync_mode == 'scheduled':
        sync_interval = data.get('sync_interval', repository.sync_interval)
        if sync_interval < 1:
            return jsonify({
                'success': False,
                'message': '同步间隔必须大于0分钟'
            }), 400
    if sync_mode == 'webhook':
        if not data.get('webhook_secret') and not repository.webhook_secret:
            return jsonify({
                'success': False,
                'message': 'Webhook同步方式需要提供Webhook密钥'
            }), 400

    try:
        repository = RepositoryService.update(repo_id, **data)
        return jsonify({
            'success': True,
            'message': '仓库更新成功',
            'data': repository.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新失败: {str(e)}'
        }), 500


@repositories_bp.route('/repositories/<int:repo_id>/toggle', methods=['POST'])
@token_required
def toggle_repository(repo_id):
    """切换仓库启用状态"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权修改该仓库'
        }), 403

    repository = RepositoryService.toggle_enabled(repo_id)

    return jsonify({
        'success': True,
        'message': f'仓库已{"启用" if repository.enabled else "禁用"}',
        'data': repository.to_dict()
    })


@repositories_bp.route('/repositories/<int:repo_id>', methods=['DELETE'])
@token_required
def delete_repository(repo_id):
    """删除仓库"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权删除该仓库'
        }), 403

    RepositoryService.delete(repo_id)

    return jsonify({
        'success': True,
        'message': '仓库删除成功'
    })


@repositories_bp.route('/repositories/<int:repo_id>/sync', methods=['POST'])
@token_required
def sync_repository(repo_id):
    """手动触发仓库同步"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权同步该仓库'
        }), 403

    success, message, result = SyncService.sync_repository(repo_id)

    if not success:
        return jsonify({
            'success': False,
            'message': message
        }), 400

    return jsonify({
        'success': True,
        'message': message,
        'data': result
    })


@repositories_bp.route('/repositories/<int:repo_id>/status', methods=['GET'])
@token_required
def get_repository_status(repo_id):
    """获取仓库同步状态"""
    repository = RepositoryService.get_by_id(repo_id)

    if not repository:
        return jsonify({
            'success': False,
            'message': '仓库不存在'
        }), 404

    # 检查权限
    if repository.user_id != request.current_user.id:
        return jsonify({
            'success': False,
            'message': '无权访问该仓库'
        }), 403

    status = SyncService.get_sync_status(repo_id)

    if not status:
        return jsonify({
            'success': False,
            'message': '获取状态失败'
        }), 404

    return jsonify({
        'success': True,
        'data': status
    })
