<template>
  <div v-if="visible" class="modal-overlay" @click.self="handleClose">
    <div class="modal" :class="{ show: visible }">
      <div class="modal-header">
        <h3>编辑个人信息</h3>
        <button class="modal-close" @click="handleClose">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-field">
          <label class="form-label">用户名</label>
          <input
            v-model="formData.username"
            type="text"
            class="form-input"
            placeholder="请输入用户名"
            :disabled="!canEditUsername"
          />
          <p v-if="!canEditUsername" class="form-hint">该账户使用第三方登录，无法修改用户名</p>
        </div>

        <div class="form-field">
          <label class="form-label">姓名</label>
          <input
            v-model="formData.name"
            type="text"
            class="form-input"
            placeholder="请输入姓名"
          />
        </div>

        <div class="form-field">
          <label class="form-label">邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            class="form-input"
            placeholder="请输入邮箱"
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>

      <div class="modal-footer">
        <button type="button" class="btn-secondary" @click="handleClose">取消</button>
        <button type="button" class="btn-primary" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { notify } from '@/utils/notification'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'success'])

const authStore = useAuthStore()
const currentUser = computed(() => authStore.user)

const formData = ref({
  username: '',
  name: '',
  email: ''
})

const error = ref('')
const submitting = ref(false)

const canEditUsername = computed(() => {
  // 如果用户有 password_hash，说明是邮箱密码注册用户，可以修改用户名
  return currentUser.value?.password_hash
})

watch(() => props.visible, (val) => {
  if (val && props.user) {
    formData.value = {
      username: props.user.username || '',
      name: props.user.name || '',
      email: props.user.email || ''
    }
    error.value = ''
  }
})

async function handleSubmit() {
  error.value = ''

  // 验证
  if (!formData.value.username?.trim()) {
    error.value = '用户名不能为空'
    return
  }

  if (!formData.value.name?.trim()) {
    error.value = '姓名不能为空'
    return
  }

  if (!formData.value.email?.trim()) {
    error.value = '邮箱不能为空'
    return
  }

  // 邮箱格式验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(formData.value.email)) {
    error.value = '邮箱格式不正确'
    return
  }

  submitting.value = true
  try {
    const result = await authStore.updateProfile(formData.value)
    if (result.success) {
      notify.success('个人信息更新成功')
      handleClose()
      emit('success')
    } else {
      error.value = result.message || '更新失败'
    }
  } catch (e) {
    console.error('Update profile error:', e)
    error.value = '更新失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}

function handleClose() {
  emit('update:visible', false)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s;
}

.modal.show {
  opacity: 1;
  visibility: visible;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #333;
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: 6px;
  color: #b4b4b4;
  cursor: pointer;
  transition: all 0.15s;
}

.modal-close:hover {
  background: #222;
  color: #fff;
}

.modal-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.form-field {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #b4b4b4;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 10px 12px;
  background: #121212;
  border: 1px solid #333;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
}

.form-input:focus {
  border-color: #3b82f6;
}

.form-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-hint {
  font-size: 12px;
  color: #737373;
  margin-top: 4px;
}

.error-message {
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 6px;
  color: #ef4444;
  font-size: 13px;
  margin-bottom: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #333;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.15s;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid #333;
  border-radius: 6px;
  color: #b4b4b4;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-secondary:hover {
  background: #222;
  color: #fff;
}
</style>
