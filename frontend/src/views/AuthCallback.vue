<template>
  <div class="callback-page">
    <div class="callback-container">
      <div v-if="status === 'loading'" class="loading-state">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
        </svg>
        <p>正在登录...</p>
      </div>

      <div v-else-if="status === 'success'" class="success-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M20 6L9 17L4 12"/>
        </svg>
        <p>登录成功！正在跳转...</p>
      </div>

      <div v-else-if="status === 'error'" class="error-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M15 9L9 15M9 9L15 15"/>
        </svg>
        <p>登录失败，请重试</p>
        <button class="retry-btn" @click="goToLogin">返回登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const status = ref('loading')

onMounted(async () => {
  const code = route.query.code

  if (!code) {
    status.value = 'error'
    return
  }

  try {
    const success = await authStore.handleCallback(code)
    if (success) {
      status.value = 'success'
      setTimeout(() => {
        router.push('/dashboard')
      }, 1000)
    } else {
      status.value = 'error'
    }
  } catch (e) {
    console.error('Callback error:', e)
    status.value = 'error'
  }
})

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.callback-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #121827;
}

.callback-container {
  text-align: center;
}

.spinner {
  width: 48px;
  height: 48px;
  color: var(--color-blue);
  animation: spin 1s linear infinite;
  margin: 0 auto var(--space-4);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-state,
.success-state,
.error-state {
  padding: var(--space-6);
}

.loading-state p,
.success-state p,
.error-state p {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin: 0;
}

.success-state svg {
  width: 48px;
  height: 48px;
  color: var(--color-green);
  margin: 0 auto var(--space-4);
}

.error-state svg {
  width: 48px;
  height: 48px;
  color: #ef4444;
  margin: 0 auto var(--space-4);
}

.retry-btn {
  margin-top: var(--space-4);
  padding: var(--space-3) var(--space-5);
  background: var(--color-blue);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background var(--transition-fast);
}

.retry-btn:hover {
  background: #2563eb;
}
</style>
