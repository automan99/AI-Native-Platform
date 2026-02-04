/**
 * Authentication Store
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { userApi } from '@/api/user'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userInfo = computed(() => user.value)

  // Actions
  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  function setUser(newUser) {
    user.value = newUser
    if (newUser) {
      localStorage.setItem('user', JSON.stringify(newUser))
    } else {
      localStorage.removeItem('user')
    }
  }

  // GitLab OAuth2 登录
  async function loginWithGitLab() {
    try {
      const res = await authApi.getLoginUrl()
      if (res.success) {
        window.location.href = res.data.auth_url
      }
    } catch (e) {
      console.error('GitLab login error:', e)
      throw e
    }
  }

  // 邮箱密码登录
  async function loginWithPassword(login, password) {
    try {
      const res = await authApi.loginWithPassword(login, password)
      if (res.success) {
        setToken(res.data.token)
        setUser(res.data.user)
        return { success: true }
      }
      return { success: false, message: res.message }
    } catch (e) {
      console.error('Password login error:', e)
      return { success: false, message: '登录失败，请稍后重试' }
    }
  }

  // 用户注册
  async function register(data) {
    try {
      const res = await authApi.register(data)
      if (res.success) {
        return { success: true, message: res.message }
      }
      return { success: false, message: res.message }
    } catch (e) {
      console.error('Register error:', e)
      return { success: false, message: '注册失败，请稍后重试' }
    }
  }

  // OAuth 回调处理
  async function handleCallback(code) {
    try {
      const res = await authApi.callback(code)
      if (res.success) {
        setToken(res.data.token)
        setUser(res.data.user)
        return true
      }
      return false
    } catch (e) {
      console.error('Callback error:', e)
      throw e
    }
  }

  // 获取当前用户信息
  async function fetchCurrentUser() {
    if (!token.value) return null

    try {
      const res = await authApi.getCurrentUser()
      if (res.success) {
        setUser(res.data)
        return res.data
      }
    } catch (e) {
      console.error('Fetch current user error:', e)
      logout()
    }
    return null
  }

  // 登出
  function logout() {
    setToken(null)
    setUser(null)
  }

  // 更新个人信息
  async function updateProfile(data) {
    if (!token.value) return { success: false, message: '未登录' }

    try {
      const res = await userApi.updateProfile(data)
      if (res.success) {
        // 更新本地用户信息
        await fetchCurrentUser()
        return { success: true, message: res.message }
      }
      return { success: false, message: res.message }
    } catch (e) {
      console.error('Update profile error:', e)
      return { success: false, message: '更新个人信息失败' }
    }
  }

  // 修改密码
  async function changePassword(oldPassword, newPassword) {
    if (!token.value) return { success: false, message: '未登录' }

    try {
      const res = await userApi.changePassword(oldPassword, newPassword)
      return res
    } catch (e) {
      console.error('Change password error:', e)
      return { success: false, message: '修改密码失败' }
    }
  }

  // 更新头像
  async function updateAvatar(avatarUrl) {
    if (!token.value) return { success: false, message: '未登录' }

    try {
      const res = await userApi.updateAvatar(avatarUrl)
      if (res.success) {
        await fetchCurrentUser()
        return { success: true, message: res.message }
      }
      return { success: false, message: res.message }
    } catch (e) {
      console.error('Update avatar error:', e)
      return { success: false, message: '更新头像失败' }
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    userInfo,
    setToken,
    setUser,
    loginWithGitLab,
    loginWithPassword,
    register,
    handleCallback,
    fetchCurrentUser,
    logout,
    updateProfile,
    changePassword,
    updateAvatar
  }
})
