"""
AI Native 研发平台 - Base Syncer
"""
from abc import ABC, abstractmethod
import yaml


class BaseSyncer(ABC):
    """同步器基类"""

    def __init__(self, repository):
        self.repository = repository

    @abstractmethod
    def sync(self):
        """
        执行同步

        Returns:
            dict: {'added': int, 'updated': int, 'removed': int}
        """
        pass

    def parse_metadata(self, content):
        """
        解析元数据文件 (YAML)

        Args:
            content: YAML 文件内容

        Returns:
            dict: 解析后的元数据
        """
        try:
            return yaml.safe_load(content) or {}
        except Exception as e:
            return {}

    def get_install_command(self, resource_type, identifier):
        """生成安装命令"""
        return f"claude {resource_type} install {identifier}"
