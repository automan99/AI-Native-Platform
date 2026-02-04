import api from './index'

export const statsApi = {
  // 获取首页统计
  getOverview() {
    return api.get('/stats/overview')
  },

  // 获取热门资源
  getTop(params) {
    return api.get('/stats/top', { params })
  },

  // 获取最新资源
  getLatest(params) {
    return api.get('/stats/latest', { params })
  }
}
