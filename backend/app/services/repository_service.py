"""
AI Native 研发平台 - Repository Service
"""
from app import db
from app.models.repository import Repository
from app.utils.crypto import CryptoUtil


class RepositoryService:
    """仓库服务"""

    @staticmethod
    def get_list(page=1, page_size=20):
        """获取所有仓库列表"""
        query = Repository.query.order_by(Repository.created_at.desc())
        total = query.count()
        repositories = query.offset((page - 1) * page_size).limit(page_size).all()
        return repositories, total

    @staticmethod
    def get_list_by_user(user_id, page=1, page_size=20):
        """获取用户的仓库列表"""
        query = Repository.query.filter_by(user_id=user_id).order_by(Repository.created_at.desc())
        total = query.count()
        repositories = query.offset((page - 1) * page_size).limit(page_size).all()
        return repositories, total

    @staticmethod
    def get_by_id(repo_id):
        """根据 ID 获取仓库"""
        return Repository.query.get(repo_id)

    @staticmethod
    def get_by_url(url):
        """根据 URL 获取仓库"""
        return Repository.query.filter_by(url=url).first()

    @staticmethod
    def get_by_url_and_user(url, user_id):
        """根据 URL 和用户 ID 获取仓库"""
        return Repository.query.filter_by(url=url, user_id=user_id).first()

    @staticmethod
    def get_scheduled_repositories():
        """获取需要定时同步的仓库"""
        return Repository.query.filter_by(
            sync_mode='scheduled',
            sync_enabled=True,
            enabled=True
        ).all()

    @staticmethod
    def create(user_id, name, url, gitlab_project_id=None, repo_type='gitlab', github_repo_info=None, **kwargs):
        """
        创建仓库

        Args:
            user_id: 用户ID
            name: 仓库名称
            url: 仓库地址
            gitlab_project_id: GitLab项目ID
            repo_type: 仓库类型 (gitlab/github)
            github_repo_info: GitHub仓库信息 (owner/repo)
            **kwargs: 其他可选字段 (description, branch, path, auth_type, auth_token, ssh_key,
                        sync_mode, sync_interval, enabled, webhook_secret, webhook_url)
        """
        repo = Repository(
            user_id=user_id,
            repo_type=repo_type,
            name=name,
            url=url,
            gitlab_project_id=gitlab_project_id,
            description=kwargs.get('description'),
            branch=kwargs.get('branch', 'main'),
            path=kwargs.get('path'),
            auth_type=kwargs.get('auth_type', 'public'),
            auth_token=CryptoUtil.encrypt(kwargs['auth_token']) if kwargs.get('auth_token') else None,
            ssh_key=CryptoUtil.encrypt(kwargs['ssh_key']) if kwargs.get('ssh_key') else None,
            sync_mode=kwargs.get('sync_mode', 'manual'),
            sync_interval=kwargs.get('sync_interval', 60),
            sync_enabled=kwargs.get('sync_enabled', True),
            enabled=kwargs.get('enabled', True),
            webhook_secret=CryptoUtil.encrypt(kwargs['webhook_secret']) if kwargs.get('webhook_secret') else None,
            webhook_url=kwargs.get('webhook_url')
        )
        db.session.add(repo)
        db.session.commit()
        return repo

    @staticmethod
    def update(repo_id, **kwargs):
        """
        更新仓库信息

        Args:
            repo_id: 仓库ID
            **kwargs: 要更新的字段
        """
        repo = Repository.query.get(repo_id)
        if not repo:
            return None

        # 可更新字段列表
        updatable_fields = [
            'name', 'description', 'url', 'branch', 'path',
            'auth_type', 'sync_mode', 'sync_interval',
            'sync_enabled', 'enabled', 'webhook_url'
        ]

        # 更新普通字段
        for field in updatable_fields:
            if field in kwargs and kwargs[field] is not None:
                setattr(repo, field, kwargs[field])

        # 处理敏感字段（加密存储）
        if 'auth_token' in kwargs:
            if kwargs['auth_token']:
                repo.auth_token = CryptoUtil.encrypt(kwargs['auth_token'])
            elif kwargs.get('auth_token') == '':
                repo.auth_token = None

        if 'ssh_key' in kwargs:
            if kwargs['ssh_key']:
                repo.ssh_key = CryptoUtil.encrypt(kwargs['ssh_key'])
            elif kwargs.get('ssh_key') == '':
                repo.ssh_key = None

        if 'webhook_secret' in kwargs:
            if kwargs['webhook_secret']:
                repo.webhook_secret = CryptoUtil.encrypt(kwargs['webhook_secret'])
            elif kwargs.get('webhook_secret') == '':
                repo.webhook_secret = None

        db.session.commit()
        return repo

    @staticmethod
    def get_decrypted_secrets(repo_id):
        """
        获取解密后的敏感信息

        Args:
            repo_id: 仓库ID

        Returns:
            dict: 包含解密后的敏感信息
        """
        repo = Repository.query.get(repo_id)
        if not repo:
            return None

        return {
            'auth_token': CryptoUtil.decrypt(repo.auth_token) if repo.auth_token else None,
            'ssh_key': CryptoUtil.decrypt(repo.ssh_key) if repo.ssh_key else None,
            'webhook_secret': CryptoUtil.decrypt(repo.webhook_secret) if repo.webhook_secret else None
        }

    @staticmethod
    def delete(repo_id):
        """删除仓库"""
        repo = Repository.query.get(repo_id)
        if repo:
            db.session.delete(repo)
            db.session.commit()
        return repo

    @staticmethod
    def update_sync_status(repo_id, status, error_message=None):
        """更新同步状态"""
        repo = Repository.query.get(repo_id)
        if repo:
            repo.sync_status = status
            if error_message:
                repo.error_message = error_message
            db.session.commit()
        return repo

    @staticmethod
    def toggle_enabled(repo_id):
        """切换仓库启用状态"""
        repo = Repository.query.get(repo_id)
        if repo:
            repo.enabled = not repo.enabled
            db.session.commit()
        return repo
