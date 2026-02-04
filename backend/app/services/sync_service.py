"""
AI Native 研发平台 - Sync Service
同步服务，通过 GitHub/GitLab API 直接获取数据，无需克隆到本地
"""
import re
import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional
from flask import current_app
from app import db
from app.models.repository import Repository
from app.models.resource import Resource
from app.models.sync_log import SyncLog
from app.utils.gitlab_client import GitLabClient
from app.utils.github_client import GitHubClient
from app.utils.crypto import CryptoUtil


class SyncService:
    """同步服务"""

    @staticmethod
    def sync_repository(repo_id):
        """
        同步指定仓库

        Returns:
            (success, message, sync_result)
        """
        repo = Repository.query.get(repo_id)
        if not repo:
            return False, "仓库不存在", None

        # 更新同步状态
        repo.sync_status = 'syncing'
        db.session.commit()

        # 创建同步日志
        sync_log = SyncLog(
            repository_id=repo_id,
            status='syncing',
            started_at=datetime.utcnow()
        )
        db.session.add(sync_log)
        db.session.commit()

        try:
            # 根据仓库类型选择客户端
            if repo.repo_type == 'github':
                result = ApiSyncService.sync_github_repository(repo)
            else:
                result = ApiSyncService.sync_gitlab_repository(repo)

            if result.get('success'):
                # 更新同步日志
                sync_log.status = 'success'
                sync_log.finished_at = datetime.utcnow()
                sync_log.resources_added = result.get('added', 0)
                sync_log.resources_updated = result.get('updated', 0)
                sync_log.resources_removed = result.get('removed', 0)

                # 更新仓库状态
                repo.sync_status = 'success'
                repo.last_sync_at = datetime.utcnow()
                repo.last_sync_status = 'success'
                repo.error_message = None
                repo.resource_count = Resource.query.filter_by(repository_id=repo_id, is_active=True).count()

                db.session.commit()

                return True, "同步成功", result
            else:
                raise Exception(result.get('message', '同步失败'))

        except Exception as e:
            # 同步失败
            sync_log.status = 'failed'
            sync_log.finished_at = datetime.utcnow()
            sync_log.error_message = str(e)

            repo.sync_status = 'failed'
            repo.last_sync_status = 'failed'
            repo.error_message = str(e)

            db.session.commit()

            return False, f"同步失败: {str(e)}", None

    @staticmethod
    def sync_all():
        """同步所有启用的仓库"""
        repos = Repository.query.filter_by(sync_enabled=True, enabled=True).all()
        results = []

        for repo in repos:
            success, message, result = SyncService.sync_repository(repo.id)
            results.append({
                'repo_id': repo.id,
                'repo_name': repo.name,
                'success': success,
                'message': message
            })

        return results

    @staticmethod
    def get_sync_status(repo_id):
        """获取同步状态"""
        repo = Repository.query.get(repo_id)
        if not repo:
            return None

        # 获取最新的同步日志
        latest_log = SyncLog.query.filter_by(repository_id=repo_id).order_by(
            SyncLog.created_at.desc()
        ).first()

        return {
            'sync_status': repo.sync_status,
            'last_sync_at': repo.last_sync_at.isoformat() if repo.last_sync_at else None,
            'last_sync_status': repo.last_sync_status,
            'error_message': repo.error_message,
            'latest_log': latest_log.to_dict() if latest_log else None
        }


class ApiSyncService:
    """基于 API 的同步服务"""

    @staticmethod
    def sync_github_repository(repository: Repository) -> Dict:
        """
        同步 GitHub 仓库

        Args:
            repository: 仓库对象

        Returns:
            Dict: 同步结果
        """
        try:
            # 获取 token
            token = None
            if repository.auth_token:
                try:
                    token = CryptoUtil.decrypt(repository.auth_token)
                except Exception as e:
                    current_app.logger.error(f'Failed to decrypt token: {e}')

            client = GitHubClient(token)

            # 提取仓库信息
            repo_info = client.extract_repo_info(repository.url)
            owner = repo_info['owner']
            repo_name = repo_info['repo']

            # 获取默认分支
            branch = repository.branch or client.get_default_branch(owner, repo_name)

            # 解析资源
            resources = []

            # 扫描 skills/
            skills = ApiSyncService._parse_github_skills(
                client, owner, repo_name, repository, branch
            )
            resources.extend(skills)

            # 同步到数据库
            stats = ApiSyncService._sync_resources_to_db(repository, resources)

            return {
                'success': True,
                'added': stats['added'],
                'updated': stats['updated'],
                'removed': stats['removed']
            }

        except Exception as e:
            current_app.logger.error(f'GitHub sync failed: {e}')
            return {
                'success': False,
                'message': str(e)
            }

    @staticmethod
    def sync_gitlab_repository(repository: Repository) -> Dict:
        """
        同步 GitLab 仓库

        Args:
            repository: 仓库对象

        Returns:
            Dict: 同步结果
        """
        try:
            # 获取 token
            token = None
            if repository.auth_token:
                try:
                    token = CryptoUtil.decrypt(repository.auth_token)
                except Exception as e:
                    current_app.logger.error(f'Failed to decrypt token: {e}')

            client = GitLabClient(token) if token else GitLabClient()

            project_id = repository.gitlab_project_id
            branch = repository.branch or 'main'

            # 解析资源
            resources = []

            # 扫描 skills/
            skills = ApiSyncService._parse_gitlab_skills(
                client, project_id, repository, branch
            )
            resources.extend(skills)

            # 同步到数据库
            stats = ApiSyncService._sync_resources_to_db(repository, resources)

            return {
                'success': True,
                'added': stats['added'],
                'updated': stats['updated'],
                'removed': stats['removed']
            }

        except Exception as e:
            current_app.logger.error(f'GitLab sync failed: {e}')
            return {
                'success': False,
                'message': str(e)
            }

    @staticmethod
    def _parse_github_skills(client: GitHubClient, owner: str, repo: str,
                            repository: Repository, branch: str) -> List[Dict]:
        """解析 GitHub Skills"""
        resources = []

        try:
            # 列出 skills 目录
            items = client.list_directory(owner, repo, 'skills', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'dir':
                    continue

                skill_name = item.get('name')
                if skill_name.startswith('.'):
                    continue

                # 解析单个 Skill
                skill = ApiSyncService._parse_github_skill(
                    client, owner, repo, skill_name, repository, branch
                )
                if skill:
                    resources.append(skill)

        except Exception as e:
            current_app.logger.error(f'解析 GitHub Skills 失败: {e}')

        return resources

    @staticmethod
    def _parse_github_skill(client: GitHubClient, owner: str, repo: str,
                          skill_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitHub Skill"""
        try:
            skill_path = f'skills/{skill_name}'

            # 默认技能信息
            skill_info = {
                'repository_id': repository.id,
                'type': 'skill',
                'name': skill_name,
                'identifier': f"{repository.id}-{skill_name.lower().replace('-', '_')}",
                'description': f'{skill_name} skill',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude skill install {skill_name}",
                'path': skill_path,
                'metadata': {}
            }

            # 查找 SKILL.md（Claude Code 标准）
            skill_md_content = client.get_file_content(owner, repo, f'{skill_path}/SKILL.md', branch)
            if skill_md_content:
                # 提取 YAML front matter
                front_matter = ApiSyncService._extract_front_matter(skill_md_content)
                if front_matter:
                    if front_matter.get('name'):
                        skill_info['name'] = front_matter['name']
                    if front_matter.get('description'):
                        skill_info['description'] = front_matter['description']
                    if front_matter.get('version'):
                        skill_info['version'] = front_matter['version']
                    if front_matter.get('author'):
                        skill_info['author'] = front_matter['author']
                    # 存储参数定义
                    if front_matter.get('parameters'):
                        skill_info['metadata']['parameters'] = front_matter['parameters']

                skill_info['readme_content'] = skill_md_content
            else:
                # 查找 README.md
                readme_content = client.get_file_content(owner, repo, f'{skill_path}/README.md', branch)
                if readme_content:
                    skill_info['readme_content'] = readme_content
                else:
                    # 尝试查找脚本文件
                    for script_file in ['skill.py', 'index.py', 'main.py', 'skill.js', 'index.js', 'main.js']:
                        script_content = client.get_file_content(owner, repo, f'{skill_path}/{script_file}', branch)
                        if script_content:
                            skill_info['readme_content'] = script_content
                            break

            return skill_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitHub Skill 失败 {skill_name}: {e}')
            return None

    @staticmethod
    def _parse_github_mcp_servers(client: GitHubClient, owner: str, repo: str,
                                  repository: Repository, branch: str) -> List[Dict]:
        """解析 GitHub MCP Servers"""
        resources = []

        try:
            items = client.list_directory(owner, repo, 'mcp', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'dir':
                    continue

                mcp_name = item.get('name')
                if mcp_name.startswith('.'):
                    continue

                mcp = ApiSyncService._parse_github_mcp(
                    client, owner, repo, mcp_name, repository, branch
                )
                if mcp:
                    resources.append(mcp)

        except Exception as e:
            current_app.logger.error(f'解析 GitHub MCP 失败: {e}')

        return resources

    @staticmethod
    def _parse_github_mcp(client: GitHubClient, owner: str, repo: str,
                         mcp_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitHub MCP Server"""
        try:
            mcp_path = f'mcp/{mcp_name}'

            mcp_info = {
                'repository_id': repository.id,
                'type': 'mcp',
                'name': mcp_name,
                'identifier': f"{repository.id}-{mcp_name.lower().replace('-', '_')}",
                'description': f'{mcp_name} MCP Server',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude mcp install {mcp_name}",
                'path': mcp_path,
                'metadata': {}
            }

            # 查找 MCP.md 或 README.md
            for md_file in ['MCP.md', 'mcp.md', 'README.md']:
                content = client.get_file_content(owner, repo, f'{mcp_path}/{md_file}', branch)
                if content:
                    mcp_info['readme_content'] = content

                    # 提取元数据
                    front_matter = ApiSyncService._extract_front_matter(content)
                    if front_matter:
                        if front_matter.get('name'):
                            mcp_info['name'] = front_matter['name']
                        if front_matter.get('description'):
                            mcp_info['description'] = front_matter['description']
                        if front_matter.get('version'):
                            mcp_info['version'] = front_matter['version']
                    break

            return mcp_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitHub MCP 失败 {mcp_name}: {e}')
            return None

    @staticmethod
    def _parse_github_hooks(client: GitHubClient, owner: str, repo: str,
                          repository: Repository, branch: str) -> List[Dict]:
        """解析 GitHub Hooks"""
        resources = []

        try:
            items = client.list_directory(owner, repo, 'hooks', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'dir':
                    continue

                hook_name = item.get('name')
                if hook_name.startswith('.'):
                    continue

                hook = ApiSyncService._parse_github_hook(
                    client, owner, repo, hook_name, repository, branch
                )
                if hook:
                    resources.append(hook)

        except Exception as e:
            current_app.logger.error(f'解析 GitHub Hooks 失败: {e}')

        return resources

    @staticmethod
    def _parse_github_hook(client: GitHubClient, owner: str, repo: str,
                          hook_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitHub Hook"""
        try:
            hook_path = f'hooks/{hook_name}'

            hook_info = {
                'repository_id': repository.id,
                'type': 'hook',
                'name': hook_name,
                'identifier': f"{repository.id}-{hook_name.lower().replace('-', '_')}",
                'description': f'{hook_name} hook',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude hook install {hook_name}",
                'path': hook_path,
                'metadata': {}
            }

            # 查找 HOOK.md 或 README.md
            for md_file in ['HOOK.md', 'hook.md', 'README.md']:
                content = client.get_file_content(owner, repo, f'{hook_path}/{md_file}', branch)
                if content:
                    hook_info['readme_content'] = content

                    # 提取元数据
                    front_matter = ApiSyncService._extract_front_matter(content)
                    if front_matter:
                        if front_matter.get('name'):
                            hook_info['name'] = front_matter['name']
                        if front_matter.get('description'):
                            hook_info['description'] = front_matter['description']
                        if front_matter.get('version'):
                            hook_info['version'] = front_matter['version']
                    break

            return hook_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitHub Hook 失败 {hook_name}: {e}')
            return None

    @staticmethod
    def _parse_gitlab_skills(client: GitLabClient, project_id: int,
                            repository: Repository, branch: str) -> List[Dict]:
        """解析 GitLab Skills"""
        resources = []

        try:
            # 列出 skills 目录
            items = client.list_directory(project_id, 'skills', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'tree':
                    continue

                skill_name = item.get('path')
                if skill_name.startswith('.'):
                    continue

                # 解析单个 Skill
                skill = ApiSyncService._parse_gitlab_skill(
                    client, project_id, skill_name, repository, branch
                )
                if skill:
                    resources.append(skill)

        except Exception as e:
            current_app.logger.error(f'解析 GitLab Skills 失败: {e}')

        return resources

    @staticmethod
    def _parse_gitlab_skill(client: GitLabClient, project_id: int,
                          skill_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitLab Skill"""
        try:
            skill_path = f'skills/{skill_name}'

            # 默认技能信息
            skill_info = {
                'repository_id': repository.id,
                'type': 'skill',
                'name': skill_name,
                'identifier': f"{repository.id}-{skill_name.lower().replace('-', '_')}",
                'description': f'{skill_name} skill',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude skill install {skill_name}",
                'path': skill_path,
                'metadata': {}
            }

            # 查找 SKILL.md
            skill_md_content = client.get_file_content(project_id, f'{skill_path}/SKILL.md', branch)
            if skill_md_content:
                front_matter = ApiSyncService._extract_front_matter(skill_md_content)
                if front_matter:
                    if front_matter.get('name'):
                        skill_info['name'] = front_matter['name']
                    if front_matter.get('description'):
                        skill_info['description'] = front_matter['description']
                    if front_matter.get('version'):
                        skill_info['version'] = front_matter['version']
                    if front_matter.get('author'):
                        skill_info['author'] = front_matter['author']
                    if front_matter.get('parameters'):
                        skill_info['metadata']['parameters'] = front_matter['parameters']

                skill_info['readme_content'] = skill_md_content
            else:
                # 查找 README.md
                readme_content = client.get_file_content(project_id, f'{skill_path}/README.md', branch)
                if readme_content:
                    skill_info['readme_content'] = readme_content

            return skill_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitLab Skill 失败 {skill_name}: {e}')
            return None

    @staticmethod
    def _parse_gitlab_mcp_servers(client: GitLabClient, project_id: int,
                                  repository: Repository, branch: str) -> List[Dict]:
        """解析 GitLab MCP Servers"""
        resources = []

        try:
            items = client.list_directory(project_id, 'mcp', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'tree':
                    continue

                mcp_name = item.get('path')
                if mcp_name.startswith('.'):
                    continue

                mcp = ApiSyncService._parse_gitlab_mcp(
                    client, project_id, mcp_name, repository, branch
                )
                if mcp:
                    resources.append(mcp)

        except Exception as e:
            current_app.logger.error(f'解析 GitLab MCP 失败: {e}')

        return resources

    @staticmethod
    def _parse_gitlab_mcp(client: GitLabClient, project_id: int,
                         mcp_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitLab MCP Server"""
        try:
            mcp_path = f'mcp/{mcp_name}'

            mcp_info = {
                'repository_id': repository.id,
                'type': 'mcp',
                'name': mcp_name,
                'identifier': f"{repository.id}-{mcp_name.lower().replace('-', '_')}",
                'description': f'{mcp_name} MCP Server',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude mcp install {mcp_name}",
                'path': mcp_path,
                'metadata': {}
            }

            # 查找 MCP.md 或 README.md
            for md_file in ['MCP.md', 'mcp.md', 'README.md']:
                content = client.get_file_content(project_id, f'{mcp_path}/{md_file}', branch)
                if content:
                    mcp_info['readme_content'] = content

                    front_matter = ApiSyncService._extract_front_matter(content)
                    if front_matter:
                        if front_matter.get('name'):
                            mcp_info['name'] = front_matter['name']
                        if front_matter.get('description'):
                            mcp_info['description'] = front_matter['description']
                        if front_matter.get('version'):
                            mcp_info['version'] = front_matter['version']
                    break

            return mcp_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitLab MCP 失败 {mcp_name}: {e}')
            return None

    @staticmethod
    def _parse_gitlab_hooks(client: GitLabClient, project_id: int,
                          repository: Repository, branch: str) -> List[Dict]:
        """解析 GitLab Hooks"""
        resources = []

        try:
            items = client.list_directory(project_id, 'hooks', branch)
            if not items:
                return resources

            for item in items:
                if item.get('type') != 'tree':
                    continue

                hook_name = item.get('path')
                if hook_name.startswith('.'):
                    continue

                hook = ApiSyncService._parse_gitlab_hook(
                    client, project_id, hook_name, repository, branch
                )
                if hook:
                    resources.append(hook)

        except Exception as e:
            current_app.logger.error(f'解析 GitLab Hooks 失败: {e}')

        return resources

    @staticmethod
    def _parse_gitlab_hook(client: GitLabClient, project_id: int,
                          hook_name: str, repository: Repository, branch: str) -> Optional[Dict]:
        """解析单个 GitLab Hook"""
        try:
            hook_path = f'hooks/{hook_name}'

            hook_info = {
                'repository_id': repository.id,
                'type': 'hook',
                'name': hook_name,
                'identifier': f"{repository.id}-{hook_name.lower().replace('-', '_')}",
                'description': f'{hook_name} hook',
                'version': '1.0.0',
                'author': '',
                'readme_content': '',
                'install_command': f"claude hook install {hook_name}",
                'path': hook_path,
                'metadata': {}
            }

            # 查找 HOOK.md 或 README.md
            for md_file in ['HOOK.md', 'hook.md', 'README.md']:
                content = client.get_file_content(project_id, f'{hook_path}/{md_file}', branch)
                if content:
                    hook_info['readme_content'] = content

                    front_matter = ApiSyncService._extract_front_matter(content)
                    if front_matter:
                        if front_matter.get('name'):
                            hook_info['name'] = front_matter['name']
                        if front_matter.get('description'):
                            hook_info['description'] = front_matter['description']
                        if front_matter.get('version'):
                            hook_info['version'] = front_matter['version']
                    break

            return hook_info

        except Exception as e:
            current_app.logger.warning(f'解析 GitLab Hook 失败 {hook_name}: {e}')
            return None

    @staticmethod
    def _extract_front_matter(content: str) -> Optional[Dict]:
        """提取 YAML front matter"""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except:
                pass
        return None

    @staticmethod
    def _sync_resources_to_db(repository: Repository, resources: List[Dict]) -> Dict:
        """
        同步资源到数据库

        Args:
            repository: 仓库对象
            resources: 资源列表

        Returns:
            Dict: 统计信息
        """
        stats = {'added': 0, 'updated': 0, 'removed': 0}

        # 获取当前数据库中的资源
        existing_resources = {
            resource.path: resource
            for resource in Resource.query.filter_by(repository_id=repository.id).all()
        }

        # 当前同步的资源路径集合
        current_paths = {resource['path'] for resource in resources}

        # 更新或添加资源
        for resource_data in resources:
            existing_resource = existing_resources.get(resource_data['path'])

            if existing_resource:
                # 检查是否需要更新
                if (existing_resource.name != resource_data['name'] or
                    existing_resource.description != resource_data['description'] or
                    existing_resource.version != resource_data['version'] or
                    existing_resource.readme_content != resource_data['readme_content']):
                    existing_resource.name = resource_data['name']
                    existing_resource.identifier = resource_data['identifier']
                    existing_resource.description = resource_data['description']
                    existing_resource.version = resource_data['version']
                    existing_resource.author = resource_data['author']
                    existing_resource.readme_content = resource_data['readme_content']
                    existing_resource.install_command = resource_data['install_command']
                    existing_resource.extra_data = resource_data['metadata'] if resource_data['metadata'] else None
                    existing_resource.is_active = True
                    existing_resource.updated_at = datetime.utcnow()
                    stats['updated'] += 1
                else:
                    # 激活之前不活跃的资源
                    if not existing_resource.is_active:
                        existing_resource.is_active = True
                        stats['updated'] += 1
            else:
                # 添加新资源
                new_resource = Resource(
                    repository_id=resource_data['repository_id'],
                    type=resource_data['type'],
                    name=resource_data['name'],
                    identifier=resource_data['identifier'],
                    description=resource_data['description'],
                    version=resource_data['version'],
                    author=resource_data['author'],
                    readme_content=resource_data['readme_content'],
                    install_command=resource_data['install_command'],
                    path=resource_data['path'],
                    extra_data=resource_data['metadata'] if resource_data['metadata'] else None,
                    is_active=True
                )
                db.session.add(new_resource)
                stats['added'] += 1

        # 标记不再存在的资源为不活跃
        for path, resource in existing_resources.items():
            if path not in current_paths and resource.is_active:
                resource.is_active = False
                stats['removed'] += 1

        db.session.commit()
        return stats
