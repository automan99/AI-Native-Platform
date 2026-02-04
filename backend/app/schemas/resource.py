"""
AI Native 研发平台 - Resource Schemas
"""
from marshmallow import Schema, fields, validate, validate as v


class ResourceSchema(Schema):
    """单个资源详情 Schema"""
    id = fields.Int()
    repository_id = fields.Int()
    type = fields.Str()
    name = fields.Str()
    identifier = fields.Str()
    description = fields.Str()
    version = fields.Str()
    author = fields.Str()
    readme_content = fields.Str()
    install_command = fields.Str()
    path = fields.Str()
    metadata = fields.Dict()
    view_count = fields.Int()
    install_count = fields.Int()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class ResourceListSchema(Schema):
    """资源列表 Schema"""
    id = fields.Int()
    type = fields.Str()
    name = fields.Str()
    identifier = fields.Str()
    description = fields.Str()
    version = fields.Str()
    author = fields.Str()
    view_count = fields.Int()
    install_count = fields.Int()
    updated_at = fields.DateTime()


class ResourceQuerySchema(Schema):
    """资源查询参数 Schema"""
    type = fields.Str(validate=v.OneOf(['skill', 'mcp', 'hook', '']))
    keyword = fields.Str()
    page = fields.Int(missing=1, validate=v.Range(min=1))
    page_size = fields.Int(missing=20, validate=v.Range(min=1, max=100))
