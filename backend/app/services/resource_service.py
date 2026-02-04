"""
AI Native 研发平台 - Resource Service
"""
from sqlalchemy import or_
from app import db
from app.models.resource import Resource
from app.models.stat import Stat


class ResourceService:
    """资源服务"""

    @staticmethod
    def get_list(resource_type=None, keyword=None, page=1, page_size=20):
        """
        获取资源列表

        Args:
            resource_type: 资源类型 (skill/mcp/hook)
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量

        Returns:
            (资源列表, 总数)
        """
        query = Resource.query.filter_by(is_active=True)

        # 按类型筛选
        if resource_type:
            query = query.filter_by(type=resource_type)

        # 按关键词搜索
        if keyword:
            search_pattern = f'%{keyword}%'
            query = query.filter(
                or_(
                    Resource.name.like(search_pattern),
                    Resource.description.like(search_pattern),
                    Resource.identifier.like(search_pattern)
                )
            )

        # 排序：最新更新的在前
        query = query.order_by(Resource.updated_at.desc())

        # 分页
        total = query.count()
        resources = query.offset((page - 1) * page_size).limit(page_size).all()

        return resources, total

    @staticmethod
    def get_by_id(resource_id):
        """根据 ID 获取资源"""
        return Resource.query.get(resource_id)

    @staticmethod
    def record_view(resource_id, user_ip=None, user_agent=None):
        """记录浏览行为"""
        resource = Resource.query.get(resource_id)
        if resource:
            resource.view_count += 1
            stat = Stat(
                resource_id=resource_id,
                action_type='view',
                user_ip=user_ip,
                user_agent=user_agent
            )
            db.session.add(stat)
            db.session.commit()
        return resource

    @staticmethod
    def record_install(resource_id, user_ip=None, user_agent=None):
        """记录安装行为"""
        resource = Resource.query.get(resource_id)
        if resource:
            resource.install_count += 1
            stat = Stat(
                resource_id=resource_id,
                action_type='install',
                user_ip=user_ip,
                user_agent=user_agent
            )
            db.session.add(stat)
            db.session.commit()
        return resource

    @staticmethod
    def get_top_resources(limit=10, resource_type=None):
        """获取热门资源"""
        query = Resource.query.filter_by(is_active=True)

        if resource_type:
            query = query.filter_by(type=resource_type)

        return query.order_by(Resource.install_count.desc()).limit(limit).all()

    @staticmethod
    def get_latest_resources(limit=10, resource_type=None):
        """获取最新资源"""
        query = Resource.query.filter_by(is_active=True)

        if resource_type:
            query = query.filter_by(type=resource_type)

        return query.order_by(Resource.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_stats_overview():
        """获取统计首页"""
        from app.models.repository import Repository

        total_skills = Resource.query.filter_by(type='skill', is_active=True).count()
        total_mcps = Resource.query.filter_by(type='mcp', is_active=True).count()
        total_hooks = Resource.query.filter_by(type='hook', is_active=True).count()
        total_installs = db.session.query(db.func.sum(Resource.install_count)).scalar() or 0
        total_views = db.session.query(db.func.sum(Resource.view_count)).scalar() or 0
        total_repos = Repository.query.count()

        return {
            'total_skills': total_skills,
            'total_mcps': total_mcps,
            'total_hooks': total_hooks,
            'total_resources': total_skills + total_mcps + total_hooks,
            'total_installs': total_installs,
            'total_views': total_views,
            'total_repos': total_repos
        }
