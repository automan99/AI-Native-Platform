"""
AI Native 研发平台 - Stats Service
"""
from sqlalchemy import func
from app import db
from app.models.resource import Resource
from app.models.stat import Stat
from app.models.repository import Repository


class StatsService:
    """统计服务"""

    @staticmethod
    def get_overview():
        """获取平台首页统计"""
        total_skills = Resource.query.filter_by(type='skill', is_active=True).count()
        total_mcps = Resource.query.filter_by(type='mcp', is_active=True).count()
        total_hooks = Resource.query.filter_by(type='hook', is_active=True).count()
        total_installs = db.session.query(func.sum(Resource.install_count)).scalar() or 0
        total_views = db.session.query(func.sum(Resource.view_count)).scalar() or 0
        total_repos = Repository.query.count()

        return {
            'total_skills': total_skills,
            'total_mcps': total_mcps,
            'total_hooks': total_hooks,
            'total_resources': total_skills + total_mcps + total_hooks,
            'total_installs': int(total_installs),
            'total_views': int(total_views),
            'total_repos': total_repos
        }

    @staticmethod
    def get_top_resources(limit=10, resource_type=None, order_by='install_count'):
        """获取热门资源排行"""
        query = Resource.query.filter_by(is_active=True)

        if resource_type:
            query = query.filter_by(type=resource_type)

        order_field = getattr(Resource, order_by, Resource.install_count)
        return query.order_by(order_field.desc()).limit(limit).all()

    @staticmethod
    def get_latest_resources(limit=10, resource_type=None):
        """获取最新资源"""
        query = Resource.query.filter_by(is_active=True)

        if resource_type:
            query = query.filter_by(type=resource_type)

        return query.order_by(Resource.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_resource_stats(resource_id):
        """获取单个资源的统计信息"""
        resource = Resource.query.get(resource_id)
        if not resource:
            return None

        # 获取最近7天的统计
        from datetime import datetime, timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        recent_views = Stat.query.filter(
            Stat.resource_id == resource_id,
            Stat.action_type == 'view',
            Stat.created_at >= seven_days_ago
        ).count()

        recent_installs = Stat.query.filter(
            Stat.resource_id == resource_id,
            Stat.action_type == 'install',
            Stat.created_at >= seven_days_ago
        ).count()

        return {
            'total_views': resource.view_count,
            'total_installs': resource.install_count,
            'recent_views': recent_views,
            'recent_installs': recent_installs
        }
