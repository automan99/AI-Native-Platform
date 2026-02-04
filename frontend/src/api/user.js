/**
 * User API Client
 */
import api from './index'

export const userApi = {
  // 获取当前用户详细信息
  getProfile() {
    return api.get('/user/profile')
  },

  // 更新用户信息
  updateProfile(data) {
    return api.put('/user/profile', data)
  },

  // 修改密码
  changePassword(oldPassword, newPassword) {
    return api.post('/user/change-password', {
      old_password: oldPassword,
      new_password: newPassword
    })
  },

  // 更新头像 URL
  updateAvatar(avatarUrl) {
    return api.put('/user/avatar', { avatar_url: avatarUrl })
  }
}
