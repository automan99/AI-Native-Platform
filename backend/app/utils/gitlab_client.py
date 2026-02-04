"""
AI Native 研发平台 - GitLab API Client
"""
import requests
from urllib.parse import urljoin
from app.config import Config


class GitLabClient:
    """GitLab API 客户端"""

    def __init__(self):
        self.base_url = Config.GITLAB_URL
        self.token = Config.GITLAB_TOKEN
        self.api_base = urljoin(self.base_url, '/api/v4/')

    def _request(self, method, endpoint, **kwargs):
        """发送请求"""
        headers = kwargs.pop('headers', {})
        if self.token:
            headers['PRIVATE-TOKEN'] = self.token

        url = urljoin(self.api_base, endpoint)
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, **kwargs):
        """GET 请求"""
        return self._request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        """POST 请求"""
        return self._request('POST', endpoint, **kwargs)

    def get_project(self, project_id):
        """获取项目信息"""
        return self.get(f'/projects/{project_id}')

    def get_project_by_url(self, project_url):
        """根据 URL 获取项目"""
        # 从 URL 中提取项目路径
        # 例如: https://gitlab.com/group/project
        path = project_url.replace(self.base_url, '').strip('/')
        encoded_path = requests.utils.quote(path, safe='')
        return self.get(f'/projects/{encoded_path}')

    def list_directory(self, project_id, path='', ref='main'):
        """
        列出目录内容

        Args:
            project_id: 项目 ID
            path: 目录路径 (空字符串表示根目录)
            ref: 分支名 (默认 main)

        Returns:
            list: 文件/目录列表
        """
        try:
            params = {'ref': ref, 'per_page': 100}
            if path:
                params['path'] = path
            return self.get(
                f'/projects/{project_id}/repository/tree',
                params=params
            )
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return []
            raise

    def get_file_content(self, project_id, file_path, ref='main'):
        """
        获取文件内容

        Args:
            project_id: 项目 ID
            file_path: 文件路径
            ref: 分支名 (默认 main)

        Returns:
            str: 文件内容，如果文件不存在返回 None
        """
        try:
            encoded_path = requests.utils.quote(file_path, safe='')
            result = self.get(
                f'/projects/{project_id}/repository/files/{encoded_path}/raw',
                params={'ref': ref}
            )
            return result
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def extract_project_id(self, repo_url):
        """
        从仓库 URL 提取项目 ID

        Args:
            repo_url: GitLab 仓库 URL

        Returns:
            int: 项目 ID
        """
        try:
            project = self.get_project_by_url(repo_url)
            return project.get('id')
        except Exception as e:
            raise ValueError(f"无法获取项目信息: {str(e)}")
