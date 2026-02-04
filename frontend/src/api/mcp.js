import api from './index'

export const mcpApi = {
  // 获取 MCP Server 列表
  getServers(params) {
    return api.get('/mcp/servers', { params })
  },

  // 获取 MCP Server 详情
  getServer(id, includeSensitive = false) {
    return api.get(`/mcp/servers/${id}`, {
      params: { include_sensitive: includeSensitive }
    })
  },

  // 创建 MCP Server
  create(data) {
    return api.post('/mcp/servers', data)
  },

  // 更新 MCP Server
  update(id, data) {
    return api.put(`/mcp/servers/${id}`, data)
  },

  // 删除 MCP Server
  delete(id) {
    return api.delete(`/mcp/servers/${id}`)
  },

  // 切换 Server 启用状态
  toggle(id) {
    return api.post(`/mcp/servers/${id}/toggle`)
  },

  // 同步 Server
  sync(id) {
    return api.post(`/mcp/servers/${id}/sync`)
  },

  // 获取所有 Tools
  getTools(serverId) {
    return api.get('/mcp/tools', {
      params: serverId ? { server_id: serverId } : {}
    })
  },

  // 获取分组后的 Tools
  getToolsGrouped() {
    return api.get('/mcp/tools/grouped')
  },

  // 调用 Tool
  callTool(serverId, toolName, args) {
    return api.post('/mcp/tools/call', {
      server_id: serverId,
      tool_name: toolName,
      arguments: args
    })
  },

  // 获取 Resources
  getResources(serverId) {
    return api.get('/mcp/resources', {
      params: serverId ? { server_id: serverId } : {}
    })
  }
}
