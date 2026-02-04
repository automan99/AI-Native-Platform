"""
AI Native 研发平台 - Stat Model
"""
from datetime import datetime
from app import db


class Stat(db.Model):
    """统计记录模型"""
    __tablename__ = 'stats'

    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    action_type = db.Column(db.String(20), nullable=False)  # view/install
    user_ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 索引
    __table_args__ = (
        db.Index('idx_resource_action', 'resource_id', 'action_type'),
        db.Index('idx_created_at', 'created_at'),
    )

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'action_type': self.action_type,
            'user_ip': self.user_ip,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Stat {self.resource_id}:{self.action_type}>'
