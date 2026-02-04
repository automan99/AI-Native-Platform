"""
AI Native 研发平台 - GitHub API Client
"""
import requests
import base64
from app.config import Config


class GitHubClient:
    """GitHub API 客户端"""

    def __init__(self, token=None):
        self.base_url = 'https://api.github.com'
        self.token = token

    def _request(self, method, endpoint, **kwargs):
        """发送请求"""
        headers = kwargs.pop('headers', {})
        headers['Accept'] = 'application/vnd.github.v3+json'
        if self.token:
            headers['Authorization'] = f'token {self.token}'

        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, **kwargs):
        """GET 请求"""
        return self._request('GET', endpoint, **kwargs)

    def get_repo_by_url(self, repo_url):
        """
        根据 URL 获取仓库信息

        Args:
            repo_url: GitHub 仓库 URL
            例如: https://github.com/owner/repo

        Returns:
            dict: 仓库信息
        """
        # 从 URL 中提取 owner/repo
        from urllib.parse import urlparse
        parsed = urlparse(repo_url)
        path = parsed.path.strip('/')
        if not path or path.count('/') != 1:
            raise ValueError(f"无效的 GitHub 仓库 URL: {repo_url}")

        return self.get(f'/repos/{path}')

    def list_directory(self, owner, repo, path='', ref='main'):
        """
        列出目录内容

        Args:
            owner: 仓库所有者
            repo: 仓库名称
            path: 目录路径 (空字符串表示根目录)
            ref: 分支名 (默认 main)

        Returns:
            list: 文件/目录列表
        """
        try:
            endpoint = f'/repos/{owner}/{repo}/contents/{path}'
            if path:
                endpoint = f'/repos/{owner}/{repo}/contents/{path}'
            else:
                endpoint = f'/repos/{owner}/{repo}/contents'

            result = self.get(endpoint, params={'ref': ref})

            # GitHub API 返回数组或单个对象
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and result.get('type') == 'file':
                return [result]
            return []
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return []
            raise

    def get_file_content(self, owner, repo, file_path, ref='main'):
        """
        获取文件内容

        Args:
            owner: 仓库所有者
            repo: 仓库名称
            file_path: 文件路径
            ref: 分支名 (默认 main)

        Returns:
            str: 文件内容，如果文件不存在返回 None
        """
        try:
            result = self.get(
                f'/repos/{owner}/{repo}/contents/{file_path}',
                params={'ref': ref}
            )
            # GitHub API 返回 base64 编码的内容
            if result.get('encoding') == 'base64':
                return base64.b64decode(result['content']).decode('utf-8')
            elif result.get('content'):
                return result['content']
            return None
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise

    def extract_repo_info(self, repo_url):
        """
        从仓库 URL 提取仓库信息

        Args:
            repo_url: GitHub 仓库 URL

        Returns:
            dict: 包含 owner 和 repo 的字典
        """
        from urllib.parse import urlparse
        parsed = urlparse(repo_url)
        path = parsed.path.strip('/')
        # 移除 .git 后缀
        if path.endswith('.git'):
            path = path[:-4]
        parts = path.split('/')
        if len(parts) != 2:
            raise ValueError(f"无效的 GitHub 仓库 URL: {repo_url}")

        return {'owner': parts[0], 'repo': parts[1]}

    def get_default_branch(self, owner, repo):
        """获取仓库默认分支"""
        try:
            repo_info = self.get(f'/repos/{owner}/{repo}')
            return repo_info.get('default_branch', 'main')
        except:
            return 'main'

