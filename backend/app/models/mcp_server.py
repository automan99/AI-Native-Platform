"""
MCP Server Model
"""
from datetime import datetime
from app import db


class MCPServer(db.Model):
    """MCP Server 模型"""
    __tablename__ = 'mcp_servers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # 传输类型: stdio, http
    transport_type = db.Column(db.String(20), nullable=False, default='stdio')

    # stdio 配置
    command = db.Column(db.String(500))
    arguments = db.Column(db.JSON)  # 命令参数列表
    env = db.Column(db.JSON)  # 环境变量

    # http 配置
    url = db.Column(db.String(500))

    # 通用配置
    timeout = db.Column(db.Integer, default=30)
    enabled = db.Column(db.Boolean, default=True)

    # 统计信息
    total_tools = db.Column(db.Integer, default=0)
    total_resources = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='mcp_servers')

    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'transport_type': self.transport_type,
            'timeout': self.timeout,
            'enabled': self.enabled,
            'total_tools': self.total_tools,
            'total_resources': self.total_resources,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'contributor': self.user.to_dict() if self.user else None
        }

        if include_sensitive:
            if self.transport_type == 'stdio':
                data.update({
                    'command': self.command,
                    'arguments': self.arguments,
                    'env': self.env
                })
            elif self.transport_type == 'http':
                data.update({
                    'url': self.url
                })

        return data


class MCPTool(db.Model):
    """MCP Tool 模型"""
    __tablename__ = 'mcp_tools'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('mcp_servers.id'), nullable=False)

    # Tool 基本信息
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Tool Schema (JSON Schema 格式)
    input_schema = db.Column(db.JSON)

    # 统计信息
    call_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    server = db.relationship('MCPServer', backref='tools')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'server_id': self.server_id,
            'name': self.name,
            'description': self.description,
            'input_schema': self.input_schema,
            'call_count': self.call_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class MCPResource(db.Model):
    """MCP Resource 模型"""
    __tablename__ = 'mcp_resources'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey('mcp_servers.id'), nullable=False)

    # Resource 基本信息
    uri = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    mime_type = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    server = db.relationship('MCPServer', backref='resources')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'server_id': self.server_id,
            'uri': self.uri,
            'name': self.name,
            'description': self.description,
            'mime_type': self.mime_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
