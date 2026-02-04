"""
MCP Server API
"""
from flask import Blueprint, request, jsonify
from functools import wraps
from app import db
from app.services.mcp_service import MCPService

mcp_bp = Blueprint('mcp', __name__, url_prefix='/api/mcp')


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 这里简化处理，实际应该从 token 获取用户信息
        # TODO: 实现完整的 JWT 验证
        return f(*args, **kwargs)
    return decorated_function


@mcp_bp.route('/servers', methods=['GET'])
def get_servers():
    """获取 MCP Server 列表"""
    enabled_only = request.args.get('enabled_only', 'false').lower() == 'true'
    servers = MCPService.get_servers(enabled_only=enabled_only)
    return jsonify({
        'success': True,
        'data': servers
    })


@mcp_bp.route('/servers/<int:server_id>', methods=['GET'])
def get_server(server_id):
    """获取 MCP Server 详情"""
    include_sensitive = request.args.get('include_sensitive', 'false').lower() == 'true'
    server = MCPService.get_server_by_id(server_id, include_sensitive=include_sensitive)
    if not server:
        return jsonify({
            'success': False,
            'message': 'Server not found'
        }), 404
    return jsonify({
        'success': True,
        'data': server
    })


@mcp_bp.route('/servers', methods=['POST'])
@login_required
def create_server():
    """创建 MCP Server"""
    data = request.get_json()

    # 验证必填字段
    required_fields = ['name', 'transport_type']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400

    # 验证传输类型配置
    if data['transport_type'] == 'stdio' and not data.get('command'):
        return jsonify({
            'success': False,
            'message': 'stdio type requires command'
        }), 400

    if data['transport_type'] == 'http' and not data.get('url'):
        return jsonify({
            'success': False,
            'message': 'http type requires url'
        }), 400

    server = MCPService.create_server(data)
    return jsonify({
        'success': True,
        'data': server,
        'message': 'Server created successfully'
    })


@mcp_bp.route('/servers/<int:server_id>', methods=['PUT'])
@login_required
def update_server(server_id):
    """更新 MCP Server"""
    data = request.get_json()
    server = MCPService.update_server(server_id, data)
    if not server:
        return jsonify({
            'success': False,
            'message': 'Server not found'
        }), 404
    return jsonify({
        'success': True,
        'data': server,
        'message': 'Server updated successfully'
    })


@mcp_bp.route('/servers/<int:server_id>', methods=['DELETE'])
@login_required
def delete_server(server_id):
    """删除 MCP Server"""
    if not MCPService.delete_server(server_id):
        return jsonify({
            'success': False,
            'message': 'Server not found'
        }), 404
    return jsonify({
        'success': True,
        'message': 'Server deleted successfully'
    })


@mcp_bp.route('/servers/<int:server_id>/toggle', methods=['POST'])
@login_required
def toggle_server(server_id):
    """切换 Server 启用状态"""
    server = MCPService.toggle_server(server_id)
    if not server:
        return jsonify({
            'success': False,
            'message': 'Server not found'
        }), 404
    return jsonify({
        'success': True,
        'data': server,
        'message': 'Server status updated'
    })


@mcp_bp.route('/servers/<int:server_id>/sync', methods=['POST'])
@login_required
def sync_server(server_id):
    """同步 MCP Server 的 tools 和 resources"""
    result = MCPService.sync_server_tools(server_id)
    if result['success']:
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Server synced successfully'
        })
    return jsonify({
        'success': False,
        'message': result.get('message', 'Sync failed')
    }), 500


@mcp_bp.route('/tools', methods=['GET'])
def get_tools():
    """获取所有 MCP Tools"""
    server_id = request.args.get('server_id', type=int)
    tools = MCPService.get_tools(server_id)
    return jsonify({
        'success': True,
        'data': tools
    })


@mcp_bp.route('/tools/grouped', methods=['GET'])
def get_tools_grouped():
    """获取分组后的 MCP Tools"""
    tools = MCPService.get_all_tools_grouped()
    return jsonify({
        'success': True,
        'data': tools
    })


@mcp_bp.route('/tools/call', methods=['POST'])
@login_required
def call_tool():
    """调用 MCP Tool"""
    data = request.get_json()

    required_fields = ['server_id', 'tool_name']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400

    result = MCPService.call_tool(
        data['server_id'],
        data['tool_name'],
        data.get('arguments', {})
    )

    if result['success']:
        return jsonify({
            'success': True,
            'data': result
        })
    return jsonify({
        'success': False,
        'message': result.get('message', 'Tool call failed')
    }), 500


@mcp_bp.route('/resources', methods=['GET'])
def get_resources():
    """获取所有 MCP Resources"""
    server_id = request.args.get('server_id', type=int)
    resources = MCPService.get_resources(server_id)
    return jsonify({
        'success': True,
        'data': resources
    })
