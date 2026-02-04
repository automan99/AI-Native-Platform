"""
AI Native 研发平台 - GitLab Syncer
"""
from datetime import datetime
from app import db
from app.models.resource import Resource
from app.sync.base_syncer import BaseSyncer
from app.utils.gitlab_client import GitLabClient


class GitLabSyncer(BaseSyncer):
    """GitLab 仓库同步器"""

    # 资源目录映射
    RESOURCE_DIRS = {
        'skill': 'skills',
        'mcp': 'mcp',
        'hook': 'hooks'
    }

    # 元数据文件名
    METADATA_FILES = {
        'skill': 'skill.yaml',
        'mcp': 'mcp.yaml',
        'hook': 'hook.yaml'
    }

    def sync(self):
        """
        同步仓库中的所有资源

        Returns:
            dict: {'added': int, 'updated': int, 'removed': int}
        """
        client = GitLabClient()
        result = {'added': 0, 'updated': 0, 'removed': 0}

        # 获取仓库中所有现有资源
        existing_resources = {
            r.identifier: r
            for r in Resource.query.filter_by(
                repository_id=self.repository.id,
                is_active=True
            ).all()
        }

        # 发现的所有资源
        found_resources = set()

        # 遍历每种资源类型
        for resource_type, dir_name in self.RESOURCE_DIRS.items():
            try:
                # 扫描目录
                items = client.list_directory(
                    self.repository.gitlab_project_id,
                    dir_name
                )

                for item in items or []:
                    if item.get('type') == 'tree':
                        # 这是一个子目录，可能是资源目录
                        resource_path = f"{dir_name}/{item['path']}"
                        identifier = f"{self.repository.name}/{item['path']}"

                        # 尝试解析资源
                        resource_data = self._parse_resource(
                            client, resource_type, resource_path, identifier
                        )

                        if resource_data:
                            found_resources.add(identifier)

                            # 检查是否需要新增或更新
                            if identifier in existing_resources:
                                # 检查是否需要更新
                                existing = existing_resources[identifier]
                                if self._need_update(existing, resource_data):
                                    self._update_resource(existing, resource_data)
                                    result['updated'] += 1
                            else:
                                # 新增资源
                                self._create_resource(resource_data)
                                result['added'] += 1

            except Exception as e:
                # 记录错误但继续处理其他类型
                print(f"Error syncing {resource_type}: {str(e)}")

        # 标记不再存在的资源为无效
        for identifier, resource in existing_resources.items():
            if identifier not in found_resources:
                resource.is_active = False
                result['removed'] += 1

        db.session.commit()
        return result

    def _parse_resource(self, client, resource_type, resource_path, identifier):
        """解析单个资源"""
        metadata_file = self.METADATA_FILES[resource_type]
        metadata_path = f"{resource_path}/{metadata_file}"

        try:
            # 读取元数据文件
            metadata_content = client.get_file(
                self.repository.gitlab_project_id,
                metadata_path
            )

            if not metadata_content:
                return None

            metadata = self.parse_metadata(metadata_content)
            if not metadata:
                return None

            # 尝试读取 README
            readme_content = ''
            try:
                readme_path = f"{resource_path}/README.md"
                readme_content = client.get_file(
                    self.repository.gitlab_project_id,
                    readme_path
                ) or ''
            except:
                pass

            return {
                'type': resource_type,
                'identifier': identifier,
                'name': metadata.get('name', identifier.split('/')[-1]),
                'description': metadata.get('description', ''),
                'version': metadata.get('version', '1.0.0'),
                'author': metadata.get('author', ''),
                'metadata': metadata,
                'readme_content': readme_content,
                'path': resource_path,
                'install_command': self.get_install_command(resource_type, identifier)
            }

        except Exception as e:
            print(f"Error parsing resource {resource_path}: {str(e)}")
            return None

    def _need_update(self, existing, new_data):
        """检查资源是否需要更新"""
        return (
            existing.name != new_data['name'] or
            existing.description != new_data['description'] or
            existing.version != new_data['version'] or
            existing.author != new_data['author']
        )

    def _update_resource(self, resource, data):
        """更新资源"""
        resource.name = data['name']
        resource.description = data['description']
        resource.version = data['version']
        resource.author = data['author']
        resource.extra_data = data['metadata']
        resource.readme_content = data['readme_content']
        resource.updated_at = datetime.utcnow()

    def _create_resource(self, data):
        """创建资源"""
        resource = Resource(
            repository_id=self.repository.id,
            type=data['type'],
            identifier=data['identifier'],
            name=data['name'],
            description=data['description'],
            version=data['version'],
            author=data['author'],
            readme_content=data['readme_content'],
            install_command=data['install_command'],
            path=data['path'],
            extra_data=data['metadata'],
            is_active=True
        )
        db.session.add(resource)
