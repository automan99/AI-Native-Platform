"""
AI Native 研发平台 - Stats API
"""
from flask import Blueprint, request, jsonify
from app.services.stats_service import StatsService

stats_bp = Blueprint('stats', __name__)


@stats_bp.route('/stats/overview', methods=['GET'])
def get_overview():
    """获取平台首页统计"""
    stats = StatsService.get_overview()

    return jsonify({
        'success': True,
        'data': stats
    })


@stats_bp.route('/stats/top', methods=['GET'])
def get_top_resources():
    """获取热门资源排行"""
    resource_type = request.args.get('type')
    limit = int(request.args.get('limit', 10))
    order_by = request.args.get('order_by', 'install_count')

    resources = StatsService.get_top_resources(
        limit=limit,
        resource_type=resource_type,
        order_by=order_by
    )

    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in resources]
    })


@stats_bp.route('/stats/latest', methods=['GET'])
def get_latest_resources():
    """获取最新资源"""
    resource_type = request.args.get('type')
    limit = int(request.args.get('limit', 10))

    resources = StatsService.get_latest_resources(
        limit=limit,
        resource_type=resource_type
    )

    return jsonify({
        'success': True,
        'data': [r.to_dict() for r in resources]
    })
