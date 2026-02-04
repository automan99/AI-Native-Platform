import api from './index'

export const resourceApi = {
  // 获取资源列表
  getList(params) {
    return api.get('/resources', { params })
  },

  // 获取资源详情
  getDetail(id) {
    return api.get(`/resources/${id}`)
  },

  // 记录安装
  recordInstall(id) {
    return api.post(`/resources/${id}/install`)
  },

  // 获取热门资源
  getTop(params) {
    return api.get('/resources/top', { params })
  },

  // 获取最新资源
  getLatest(params) {
    return api.get('/resources/latest', { params })
  }
}
