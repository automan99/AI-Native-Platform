"""
AI Native 研发平台 - Sync Log Model
"""
from datetime import datetime
from app import db


class SyncLog(db.Model):
    """同步日志模型"""
    __tablename__ = 'sync_logs'

    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer, db.ForeignKey('repositories.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success/failed
    started_at = db.Column(db.DateTime, nullable=False)
    finished_at = db.Column(db.DateTime)
    resources_added = db.Column(db.Integer, default=0)
    resources_updated = db.Column(db.Integer, default=0)
    resources_removed = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'repository_id': self.repository_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'resources_added': self.resources_added,
            'resources_updated': self.resources_updated,
            'resources_removed': self.resources_removed,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<SyncLog {self.repository_id}:{self.status}>'
