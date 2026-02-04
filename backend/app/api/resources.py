"""
AI Native 研发平台 - Resources API
"""
from flask import Blueprint, request, jsonify
from app.services.resource_service import ResourceService
from app.services.stats_service import StatsService

resources_bp = Blueprint('resources', __name__)


@resources_bp.route('/resources', methods=['GET'])
def get_resources():
    """获取资源列表"""
    # 获取查询参数
    resource_type = request.args.get('type')
    keyword = request.args.get('keyword')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    # 限制每页最大数量
    page_size = min(page_size, 100)

    resources, total = ResourceService.get_list(
        resource_type=resource_type,
        keyword=keyword,
        page=page,
        page_size=page_size
    )

    # 构建返回数据，添加仓库信息
    data = []
    for r in resources:
        item = r.to_dict()
        if r.repository:
            item['repository_name'] = r.repository.name
            item['repository_url'] = r.repository.url
            # 获取添加该仓库的用户（平台用户）
            if r.repository.owner:
                owner = r.repository.owner
                item['repository_owner'] = owner.name or owner.username or owner.gitlab_username or '未知用户'
        data.append(item)

    return jsonify({
        'success': True,
        'data': data,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@resources_bp.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource_detail(resource_id):
    """获取资源详情"""
    resource = ResourceService.get_by_id(resource_id)

    if not resource or not resource.is_active:
        return jsonify({
            'success': False,
            'message': '资源不存在'
        }), 404

    # 记录浏览
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    ResourceService.record_view(resource_id, user_ip, user_agent)

    # 获取统计信息
    stats = StatsService.get_resource_stats(resource_id)

    result = resource.to_dict()
    result['stats'] = stats

    # 添加仓库信息
    if resource.repository:
        result['repository_name'] = resource.repository.name
        result['repository_url'] = resource.repository.url
        # 获取添加该仓库的用户（平台用户）
        if resource.repository.owner:
            owner = resource.repository.owner
            result['repository_owner'] = owner.name or owner.username or owner.gitlab_username or '未知用户'

    return jsonify({
        'success': True,
        'data': result
    })


@resources_bp.route('/resources/<int:resource_id>/install', methods=['POST'])
def record_install(resource_id):
    """记录安装行为"""
    resource = ResourceService.record_install(
        resource_id,
        user_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )

    if not resource:
        return jsonify({
            'success': False,
            'message': '资源不存在'
        }), 404

    return jsonify({
        'success': True,
        'message': '安装记录成功'
    })


@resources_bp.route('/resources/top', methods=['GET'])
def get_top_resources():
    """获取热门资源"""
    resource_type = request.args.get('type')
    limit = int(request.args.get('limit', 10))

    resources = ResourceService.get_top_resources(
        limit=limit,
        resource_type=resource_type
    )

    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in resources]
    })


@resources_bp.route('/resources/latest', methods=['GET'])
def get_latest_resources():
    """获取最新资源"""
    resource_type = request.args.get('type')
    limit = int(request.args.get('limit', 10))

    resources = ResourceService.get_latest_resources(
        limit=limit,
        resource_type=resource_type
    )

    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in resources]
    })
