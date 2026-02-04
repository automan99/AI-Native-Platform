"""
MCP Service - MCP Server 管理
"""
import subprocess
import json
import asyncio
import sys
import shutil
import os
from typing import Dict, List, Any, Optional
from app import db
from app.models.mcp_server import MCPServer, MCPTool, MCPResource


def _find_command(command: str) -> str:
    """查找命令，在 Windows 上自动添加 .cmd 或 .exe 后缀"""
    # 如果是完整路径，直接返回
    if '\\' in command or '/' in command:
        return command

    # 在 Windows 上尝试查找命令
    if sys.platform == 'win32':
        # 首先尝试直接使用 shutil.which
        full_path = shutil.which(command)
        if full_path:
            return full_path

        # 尝试常见的 Windows 可执行文件后缀
        for ext in ['.cmd', '.exe', '.bat']:
            if shutil.which(command + ext):
                return command + ext

    return command


class MCPService:
    """MCP Server 管理服务"""

    @staticmethod
    def get_servers(enabled_only: bool = False) -> List[Dict]:
        """获取 MCP Server 列表"""
        query = MCPServer.query
        if enabled_only:
            query = query.filter_by(enabled=True)
        servers = query.order_by(MCPServer.created_at.desc()).all()
        return [server.to_dict(include_sensitive=False) for server in servers]

    @staticmethod
    def get_server_by_id(server_id: int, include_sensitive: bool = False) -> Optional[Dict]:
        """获取 MCP Server 详情"""
        server = MCPServer.query.get(server_id)
        if not server:
            return None
        return server.to_dict(include_sensitive=include_sensitive)

    @staticmethod
    def create_server(data: Dict) -> Dict:
        """创建 MCP Server"""
        server = MCPServer(
            name=data.get('name'),
            description=data.get('description'),
            transport_type=data.get('transport_type', 'stdio'),
            command=data.get('command'),
            arguments=data.get('arguments'),
            env=data.get('env'),
            url=data.get('url'),
            timeout=data.get('timeout', 30),
            enabled=data.get('enabled', True),
            user_id=data.get('user_id')
        )

        db.session.add(server)
        db.session.commit()
        db.session.refresh(server)

        # 如果启用了 server，立即同步 tools
        if server.enabled:
            MCPService.sync_server_tools(server.id)

        return server.to_dict(include_sensitive=True)

    @staticmethod
    def update_server(server_id: int, data: Dict) -> Optional[Dict]:
        """更新 MCP Server"""
        server = MCPServer.query.get(server_id)
        if not server:
            return None

        if 'name' in data:
            server.name = data['name']
        if 'description' in data:
            server.description = data['description']
        if 'timeout' in data:
            server.timeout = data['timeout']
        if 'enabled' in data:
            server.enabled = data['enabled']
        if 'transport_type' in data:
            server.transport_type = data['transport_type']
        if 'command' in data:
            server.command = data['command']
        if 'arguments' in data:
            server.arguments = data['arguments']
        if 'env' in data:
            server.env = data['env']
        if 'url' in data:
            server.url = data['url']

        db.session.commit()
        db.session.refresh(server)

        # 如果启用了 server，重新同步 tools
        if server.enabled:
            MCPService.sync_server_tools(server.id)

        return server.to_dict(include_sensitive=True)

    @staticmethod
    def delete_server(server_id: int) -> bool:
        """删除 MCP Server"""
        server = MCPServer.query.get(server_id)
        if not server:
            return False

        # 删除关联的 tools 和 resources
        MCPTool.query.filter_by(server_id=server_id).delete()
        MCPResource.query.filter_by(server_id=server_id).delete()

        db.session.delete(server)
        db.session.commit()
        return True

    @staticmethod
    def toggle_server(server_id: int) -> Optional[Dict]:
        """切换 Server 启用状态"""
        server = MCPServer.query.get(server_id)
        if not server:
            return None

        server.enabled = not server.enabled
        db.session.commit()

        if server.enabled:
            # 启用时同步 tools
            MCPService.sync_server_tools(server.id)

        return server.to_dict()

    @staticmethod
    def sync_server_tools(server_id: int) -> Dict:
        """同步 MCP Server 的 tools 和 resources"""
        server = MCPServer.query.get(server_id)
        if not server:
            return {'success': False, 'message': 'Server not found'}

        if not server.enabled:
            return {'success': False, 'message': 'Server is disabled'}

        try:
            if server.transport_type == 'stdio':
                result = MCPService._sync_stdio_server(server)
            elif server.transport_type == 'http':
                result = MCPService._sync_http_server(server)
            else:
                return {'success': False, 'message': f'Unknown transport type: {server.transport_type}'}

            if result['success']:
                # 更新统计信息
                server.total_tools = result.get('tool_count', 0)
                server.total_resources = result.get('resource_count', 0)
                db.session.commit()

            return result

        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def _sync_stdio_server(server: MCPServer) -> Dict:
        """同步 stdio 类型的 MCP Server"""
        try:
            # 构建命令，自动查找命令路径
            command = _find_command(server.command)
            cmd = [command] + (server.arguments or [])

            # 准备环境变量（继承系统环境变量）
            env = os.environ.copy()
            if server.env:
                env.update(server.env)

            # 执行 MCP list 命令
            process = subprocess.Popen(
                cmd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # 发送 list_tools 请求
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }

            stdout, stderr = process.communicate(
                input=json.dumps(request) + "\n",
                timeout=server.timeout
            )

            if process.returncode != 0:
                return {'success': False, 'message': f'Process failed: {stderr}'}

            # 解析响应
            response = json.loads(stdout)

            if 'error' in response:
                return {'success': False, 'message': response['error'].get('message', 'Unknown error')}

            # 删除旧的 tools
            MCPTool.query.filter_by(server_id=server.id).delete()

            # 保存新的 tools
            tools = response.get('result', {}).get('tools', [])
            for tool in tools:
                mcp_tool = MCPTool(
                    server_id=server.id,
                    name=tool.get('name'),
                    description=tool.get('description'),
                    input_schema=tool.get('inputSchema')
                )
                db.session.add(mcp_tool)

            db.session.commit()

            # 尝试同步 resources
            request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "resources/list"
            }

            process = subprocess.Popen(
                cmd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            stdout, stderr = process.communicate(
                input=json.dumps(request) + "\n",
                timeout=server.timeout
            )

            # 删除旧的 resources
            MCPResource.query.filter_by(server_id=server.id).delete()

            if process.returncode == 0:
                response = json.loads(stdout)
                if 'result' in response:
                    resources = response['result'].get('resources', [])
                    for resource in resources:
                        mcp_resource = MCPResource(
                            server_id=server.id,
                            uri=resource.get('uri'),
                            name=resource.get('name'),
                            description=resource.get('description'),
                            mime_type=resource.get('mimeType')
                        )
                        db.session.add(mcp_resource)

            db.session.commit()

            return {
                'success': True,
                'tool_count': len(tools),
                'resource_count': MCPResource.query.filter_by(server_id=server.id).count()
            }

        except subprocess.TimeoutExpired:
            return {'success': False, 'message': 'Process timeout'}
        except json.JSONDecodeError as e:
            return {'success': False, 'message': f'Invalid JSON response: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'Sync failed: {str(e)}'}

    @staticmethod
    def _sync_http_server(server: MCPServer) -> Dict:
        """同步 HTTP 类型的 MCP Server"""
        # HTTP 类型的同步需要通过 HTTP 请求
        # 这里简化处理，返回占位信息
        # 实际实现需要使用 requests 或 httpx 库

        # TODO: 实现 HTTP MCP Server 的同步
        return {
            'success': True,
            'tool_count': 0,
            'resource_count': 0,
            'message': 'HTTP sync not yet implemented'
        }

    @staticmethod
    def get_tools(server_id: Optional[int] = None) -> List[Dict]:
        """获取 MCP Tools 列表"""
        query = MCPTool.query
        if server_id:
            query = query.filter_by(server_id=server_id)

        tools = query.join(MCPServer).filter(MCPServer.enabled == True).all()
        return [tool.to_dict() for tool in tools]

    @staticmethod
    def get_all_tools_grouped() -> Dict[str, List[Dict]]:
        """获取所有 Tools，按 Server 分组"""
        servers = MCPServer.query.filter_by(enabled=True).all()

        result = {}
        for server in servers:
            tools = MCPTool.query.filter_by(server_id=server.id).all()
            result[str(server.id)] = {
                'server_name': server.name,
                'tools': [tool.to_dict() for tool in tools]
            }

        return result

    @staticmethod
    def get_resources(server_id: Optional[int] = None) -> List[Dict]:
        """获取 MCP Resources 列表"""
        query = MCPResource.query
        if server_id:
            query = query.filter_by(server_id=server_id)

        resources = query.join(MCPServer).filter(MCPServer.enabled == True).all()
        return [resource.to_dict() for resource in resources]

    @staticmethod
    def call_tool(server_id: int, tool_name: str, arguments: Dict) -> Dict:
        """调用 MCP Tool"""
        server = MCPServer.query.get(server_id)
        if not server or not server.enabled:
            return {'success': False, 'message': 'Server not found or disabled'}

        try:
            if server.transport_type == 'stdio':
                result = MCPService._call_stdio_tool(server, tool_name, arguments)
            else:
                result = {'success': False, 'message': 'HTTP tool call not yet implemented'}

            if result['success']:
                # 更新调用计数
                tool = MCPTool.query.filter_by(server_id=server_id, name=tool_name).first()
                if tool:
                    tool.call_count += 1
                    db.session.commit()

            return result

        except Exception as e:
            return {'success': False, 'message': str(e)}

    @staticmethod
    def _call_stdio_tool(server: MCPServer, tool_name: str, arguments: Dict) -> Dict:
        """调用 stdio 类型的 tool"""
        try:
            command = _find_command(server.command)
            cmd = [command] + (server.arguments or [])

            env = {}
            if server.env:
                env.update(server.env)

            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments or {}
                }
            }

            process = subprocess.Popen(
                cmd,
                env=env,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            stdout, stderr = process.communicate(
                input=json.dumps(request) + "\n",
                timeout=server.timeout
            )

            if process.returncode != 0:
                return {'success': False, 'message': f'Process failed: {stderr}'}

            response = json.loads(stdout)

            if 'error' in response:
                return {'success': False, 'message': response['error'].get('message', 'Unknown error')}

            return {
                'success': True,
                'result': response.get('result')
            }

        except subprocess.TimeoutExpired:
            return {'success': False, 'message': 'Process timeout'}
        except json.JSONDecodeError as e:
            return {'success': False, 'message': f'Invalid JSON response: {str(e)}'}
        except Exception as e:
            return {'success': False, 'message': f'Tool call failed: {str(e)}'}
