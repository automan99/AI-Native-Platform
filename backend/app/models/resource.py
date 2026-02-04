"""
AI Native 研发平台 - Resource Model
"""
from datetime import datetime
from app import db


class Resource(db.Model):
    """资源模型 (Skill/MCP/Hook)"""
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer, db.ForeignKey('repositories.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # skill/mcp/hook
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    version = db.Column(db.String(50))
    author = db.Column(db.String(100))
    readme_content = db.Column(db.Text)
    install_command = db.Column(db.Text)
    path = db.Column(db.String(500))
    extra_data = db.Column(db.JSON)  # 额外的元数据
    view_count = db.Column(db.Integer, default=0)
    install_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 唯一约束
    __table_args__ = (
        db.UniqueConstraint('repository_id', 'identifier', name='uq_repository_identifier'),
        db.Index('idx_type', 'type'),
        db.Index('idx_name', 'name'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'repository_id': self.repository_id,
            'type': self.type,
            'name': self.name,
            'identifier': self.identifier,
            'description': self.description,
            'version': self.version,
            'author': self.author,
            'readme_content': self.readme_content,
            'install_command': self.install_command,
            'path': self.path,
            'extra_data': self.extra_data or {},
            'view_count': self.view_count,
            'install_count': self.install_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Resource {self.type}:{self.name}>'
