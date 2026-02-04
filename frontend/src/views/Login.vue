<template>
  <div class="auth-page">
    <!-- Background Layer -->
    <div class="background-layer">
      <div class="sky-gradient"></div>
      <div class="stars"></div>
      <div class="aurora"></div>
      <div class="moon"></div>
      <div class="mountains"></div>
      <div class="foliage"></div>
    </div>

    <!-- Auth Form Container -->
    <div class="auth-container">
      <!-- Login Mode -->
      <div v-if="isLoginMode" class="login-mode">
        <!-- Logo -->
        <div class="auth-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>

        <!-- Header -->
        <div class="auth-header">
          <h1 class="auth-title">欢迎回来</h1>
          <p class="auth-subtitle">登录以继续使用 AI Native研发平台</p>
        </div>

        <!-- Login Tabs -->
        <div class="auth-tabs">
          <button
            class="auth-tab"
            :class="{ active: loginTab === 'password' }"
            @click="loginTab = 'password'"
          >
            账号密码
          </button>
          <button
            class="auth-tab"
            :class="{ active: loginTab === 'gitlab' }"
            @click="loginTab = 'gitlab'"
          >
            GitLab
          </button>
        </div>

        <!-- Password Login Form -->
        <div v-if="loginTab === 'password'" class="form-container">
          <div class="input-group">
            <input
              v-model="passwordForm.login"
              type="text"
              class="auth-input"
              placeholder="邮箱或用户名"
              @keyup.enter="handlePasswordLogin"
            />
          </div>

          <div class="input-group">
            <input
              v-model="passwordForm.password"
              type="password"
              class="auth-input"
              placeholder="密码"
              @keyup.enter="handlePasswordLogin"
            />
          </div>

          <div class="form-actions">
            <a class="forgot-link" href="#">忘记密码？</a>
          </div>

          <button class="submit-btn" @click="handlePasswordLogin" :disabled="loading">
            <span v-if="!loading">登录</span>
            <span v-else class="loading-spinner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-dasharray="60" stroke-dashoffset="20"/>
              </svg>
              登录中...
            </span>
          </button>
        </div>

        <!-- GitLab Login -->
        <div v-else class="gitlab-container">
          <button class="gitlab-btn" @click="handleGitLabLogin" :disabled="loading">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 01-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 015 1.8a.43.43 0 01.41 0l2.44 7.51h8.3l2.44-7.51a.43.43 0 01.41 0 .42.42 0 01.33.36l2.44 7.51 1.22 3.78a.84.84 0 01-.3.94z"/>
            </svg>
            <span v-if="!loading">使用 GitLab 登录</span>
            <span v-else>跳转中...</span>
          </button>
        </div>

        <!-- Divider -->
        <div class="divider">
          <span>或</span>
        </div>

        <!-- Register Link -->
        <div class="auth-footer">
          <span>还没有账户？</span>
          <a class="link" @click="isLoginMode = false">立即注册</a>
        </div>
      </div>

      <!-- Register Mode -->
      <div v-else class="register-mode">
        <!-- Logo -->
        <div class="auth-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>

        <!-- Header -->
        <div class="auth-header">
          <h1 class="auth-title">创建账户</h1>
          <p class="auth-subtitle">开始使用 AI Native研发平台</p>
        </div>

        <!-- Register Form -->
        <div class="form-container">
          <div class="input-group">
            <input
              v-model="registerForm.username"
              type="text"
              class="auth-input"
              placeholder="用户名"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.email"
              type="email"
              class="auth-input"
              placeholder="邮箱地址"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.password"
              type="password"
              class="auth-input"
              placeholder="密码"
            />
          </div>

          <div class="input-group">
            <input
              v-model="registerForm.confirmPassword"
              type="password"
              class="auth-input"
              placeholder="确认密码"
              @keyup.enter="handleRegister"
            />
          </div>

          <button class="submit-btn" @click="handleRegister" :disabled="loading">
            <span v-if="!loading">注册</span>
            <span v-else class="loading-spinner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" stroke-dasharray="60" stroke-dashoffset="20"/>
              </svg>
              注册中...
            </span>
          </button>
        </div>

        <!-- Divider -->
        <div class="divider">
          <span>或</span>
        </div>

        <!-- Login Link -->
        <div class="auth-footer">
          <span>已有账户？</span>
          <a class="link" @click="isLoginMode = true">立即登录</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { notify } from '@/utils/notification'

const router = useRouter()
const authStore = useAuthStore()

const isLoginMode = ref(true)
const loginTab = ref('password')
const loading = ref(false)

const passwordForm = ref({
  login: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

async function handlePasswordLogin() {
  if (!passwordForm.value.login || !passwordForm.value.password) {
    notify.warning('请输入用户名/邮箱和密码')
    return
  }

  loading.value = true
  try {
    const result = await authStore.loginWithPassword(
      passwordForm.value.login,
      passwordForm.value.password
    )
    if (result.success) {
      router.push('/dashboard')
    } else {
      notify.error(result.message || '登录失败')
    }
  } catch (e) {
    notify.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

async function handleGitLabLogin() {
  loading.value = true
  try {
    await authStore.loginWithGitLab()
  } catch (e) {
    notify.error('登录失败，请稍后重试')
    loading.value = false
  }
}

async function handleRegister() {
  const { username, email, password, confirmPassword } = registerForm.value

  if (!username || !email || !password || !confirmPassword) {
    notify.warning('请填写所有字段')
    return
  }

  if (password !== confirmPassword) {
    notify.warning('两次输入的密码不一致')
    return
  }

  if (password.length < 6) {
    notify.warning('密码长度至少为6个字符')
    return
  }

  loading.value = true
  try {
    const result = await authStore.register({
      username,
      email,
      password
    })
    if (result.success) {
      notify.success('注册成功，请登录')
      isLoginMode.value = true
      passwordForm.value.login = username
      passwordForm.value.password = ''
    } else {
      notify.error(result.message || '注册失败')
    }
  } catch (e) {
    notify.error('注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Base Layout */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
  overflow: hidden;
}

/* Background Layer */
.background-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

/* Sky Gradient - Deep teal to navy blue */
.sky-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #0d3b3a 0%, #1a4a5a 30%, #2d4a6a 60%, #1e3a5f 100%);
}

/* Stars */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    radial-gradient(1px 1px at 20px 30px, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 40px 70px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 50px 160px, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.5), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 160px 120px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 200px 50px, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1px 1px at 250px 90px, rgba(255, 255, 255, 0.5), transparent),
    radial-gradient(1px 1px at 300px 140px, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 350px 60px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 400px 100px, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1px 1px at 450px 30px, rgba(255, 255, 255, 0.5), transparent),
    radial-gradient(1px 1px at 500px 80px, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 550px 120px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1px 1px at 600px 40px, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1.5px 1.5px at 25px 50px, rgba(255, 255, 255, 0.9), transparent),
    radial-gradient(1.5px 1.5px at 75px 90px, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(1.5px 1.5px at 125px 140px, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1.5px 1.5px at 175px 60px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1.5px 1.5px at 225px 110px, rgba(255, 255, 255, 0.9), transparent),
    radial-gradient(2px 2px at 60px 20px, rgba(255, 255, 255, 1), transparent),
    radial-gradient(2px 2px at 150px 180px, rgba(255, 255, 255, 0.8), transparent);
  animation: twinkle 4s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

/* Aurora Borealis - Northern lights effect */
.aurora {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 50%;
  background:
    linear-gradient(135deg, transparent 30%, rgba(72, 187, 120, 0.1) 40%, rgba(52, 211, 153, 0.15) 50%, transparent 60%),
    linear-gradient(160deg, transparent 40%, rgba(45, 212, 191, 0.08) 50%, rgba(34, 211, 238, 0.12) 55%, transparent 65%),
    linear-gradient(140deg, transparent 35%, rgba(72, 187, 120, 0.06) 45%, rgba(167, 139, 250, 0.08) 50%, transparent 60%);
  filter: blur(40px);
  animation: aurora 8s ease-in-out infinite alternate;
}

@keyframes aurora {
  0% { transform: translateX(-5%) translateY(-5%); }
  50% { transform: translateX(5%) translateY(5%); }
  100% { transform: translateX(-5%) translateY(-5%); }
}

/* Moon with halo */
.moon {
  position: absolute;
  top: 10%;
  right: 12%;
  width: 80px;
  height: 80px;
}

.moon::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 60px;
  height: 60px;
  background: radial-gradient(circle at 30% 30%, #fef3c7, #fbbf24);
  border-radius: 50%;
  box-shadow: 0 0 40px rgba(251, 191, 36, 0.4), 0 0 80px rgba(251, 191, 36, 0.2);
}

.moon::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90px;
  height: 90px;
  border: 1px solid rgba(251, 191, 36, 0.15);
  border-radius: 50%;
}

/* Mountains */
.mountains {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 30%;
  background:
    linear-gradient(105deg, transparent 30%, #3b5a7c 30%, #3b5a7c 35%, transparent 35%),
    linear-gradient(75deg, transparent 40%, #4a6a8a 40%, #4a6a8a 45%, transparent 45%),
    linear-gradient(90deg, transparent 25%, #527a9a 25%, #527a9a 32%, transparent 32%),
    linear-gradient(110deg, transparent 50%, #6a8aaa 50%, #6a8aaa 58%, transparent 58%),
    linear-gradient(70deg, transparent 55%, #7a9aba 55%, #7a9aba 65%, transparent 65%);
  opacity: 0.6;
}

/* Foliage - Abstract geometric plants */
.foliage {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 25%;
  background:
    linear-gradient(160deg, transparent 50%, #1a4a3a 50%, #1a4a3a 52%, transparent 52%),
    linear-gradient(140deg, transparent 55%, #1e5a4a 55%, #1e5a4a 57%, transparent 57%),
    linear-gradient(170deg, transparent 60%, #2a6a5a 60%, #2a6a5a 62%, transparent 62%),
    linear-gradient(150deg, transparent 65%, #1a4a3a 65%, #1a4a3a 67%, transparent 67%);
  opacity: 0.7;
}

/* Decorative circles (abstract elements) */
.background-layer::before {
  content: '';
  position: absolute;
  bottom: 15%;
  left: 8%;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(45, 212, 191, 0.15), transparent);
  border-radius: 50%;
  filter: blur(20px);
}

.background-layer::after {
  content: '';
  position: absolute;
  bottom: 20%;
  right: 15%;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.1), transparent);
  border-radius: 50%;
  filter: blur(25px);
}

/* Auth Container */
.auth-container {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: rgba(18, 18, 18, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

/* Logo */
.auth-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.auth-logo svg {
  width: 48px;
  height: 48px;
  color: #3b82f6;
}

/* Auth Header */
.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-title {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  font-size: 14px;
  color: #888;
  margin: 0;
}

/* Auth Tabs */
.auth-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  padding: 4px;
  background: #1e1e1e;
  border-radius: 12px;
}

.auth-tab {
  flex: 1;
  padding: 10px 16px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.auth-tab:hover {
  color: #888;
}

.auth-tab.active {
  background: #2a2a2a;
  color: #fff;
}

/* Form Container */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.auth-input {
  width: 100%;
  padding: 14px 16px;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 10px;
  font-size: 14px;
  color: #fff;
  outline: none;
  transition: all 0.2s ease;
}

.auth-input::placeholder {
  color: #555;
}

.auth-input:focus {
  border-color: #3b82f6;
  background: #252525;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: -8px;
}

.forgot-link {
  font-size: 12px;
  color: #666;
  text-decoration: none;
  transition: color 0.15s ease;
}

.forgot-link:hover {
  color: #888;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: #e5e7eb;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #121212;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: #d1d5db;
}

.submit-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.loading-spinner svg {
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* GitLab Button */
.gitlab-container {
  margin-top: 8px;
}

.gitlab-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.gitlab-btn svg {
  width: 18px;
  height: 18px;
  color: #FC6D26;
}

.gitlab-btn:hover:not(:disabled) {
  background: #2a2a2a;
  border-color: #444;
  color: #fff;
}

.gitlab-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  margin: 20px 0;
  color: #555;
  font-size: 12px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #333;
}

.divider span {
  padding: 0 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Auth Footer */
.auth-footer {
  text-align: center;
  font-size: 13px;
  color: #666;
}

.auth-footer .link {
  color: #888;
  font-weight: 500;
  cursor: pointer;
  margin-left: 4px;
  transition: color 0.15s ease;
}

.auth-footer .link:hover {
  color: #aaa;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 640px) {
  .auth-container {
    padding: 32px 24px;
    margin: 20px;
    border-radius: 20px;
  }

  .auth-title {
    font-size: 24px;
  }

  .moon {
    width: 60px;
    height: 60px;
  }

  .moon::before {
    width: 45px;
    height: 45px;
  }

  .moon::after {
    width: 70px;
    height: 70px;
  }
}
</style>
