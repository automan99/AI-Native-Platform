import api from './index'

export const repositoryApi = {
  // 获取仓库列表
  getList(params) {
    return api.get('/repositories', { params })
  },

  // 获取仓库详情
  getDetail(id, includeSensitive = false) {
    return api.get(`/repositories/${id}`, {
      params: { include_sensitive: includeSensitive }
    })
  },

  // 添加仓库
  create(data) {
    return api.post('/repositories', data)
  },

  // 更新仓库
  update(id, data) {
    return api.put(`/repositories/${id}`, data)
  },

  // 删除仓库
  delete(id) {
    return api.delete(`/repositories/${id}`)
  },

  // 切换启用状态
  toggle(id) {
    return api.post(`/repositories/${id}/toggle`)
  },

  // 同步仓库
  sync(id) {
    return api.post(`/repositories/${id}/sync`)
  },

  // 获取同步状态
  getStatus(id) {
    return api.get(`/repositories/${id}/status`)
  }
}
