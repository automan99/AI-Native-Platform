"""
AI Native 研发平台 - Repository Schemas
"""
from marshmallow import Schema, fields, validate as v


class RepositorySchema(Schema):
    """仓库 Schema"""
    id = fields.Int()
    name = fields.Str()
    url = fields.Str()
    gitlab_project_id = fields.Int()
    sync_enabled = fields.Bool()
    sync_status = fields.Str()
    last_sync_at = fields.DateTime(allow_none=True)
    last_sync_status = fields.Str(allow_none=True)
    error_message = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    resource_count = fields.Int()


class RepositoryCreateSchema(Schema):
    """创建仓库 Schema"""
    url = fields.Str(required=True, validate=v.URL())
    name = fields.Str(required=True)


class SyncResultSchema(Schema):
    """同步结果 Schema"""
    status = fields.Str()
    message = fields.Str()
    resources_added = fields.Int()
    resources_updated = fields.Int()
    resources_removed = fields.Int()
