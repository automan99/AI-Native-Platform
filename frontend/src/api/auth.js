/**
 * Authentication API
 */
import api from './index'

export const authApi = {
  // 获取 GitLab OAuth2 登录 URL
  getLoginUrl() {
    return api.get('/auth/login')
  },

  // 邮箱密码登录
  loginWithPassword(login, password) {
    return api.post('/auth/login', { login, password })
  },

  // 用户注册
  register(data) {
    return api.post('/auth/register', data)
  },

  // OAuth 回调
  callback(code) {
    return api.post('/auth/callback', { code })
  },

  // 获取当前用户信息
  getCurrentUser() {
    return api.get('/auth/me')
  },

  // 登出
  logout() {
    return api.post('/auth/logout')
  }
}
