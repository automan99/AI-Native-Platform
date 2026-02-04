<template>
  <div v-if="visible" class="modal-overlay" @click.self="handleClose">
    <div class="modal" :class="{ show: visible }">
      <div class="modal-header">
        <h3>修改密码</h3>
        <button class="modal-close" @click="handleClose">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-field">
          <label class="form-label">当前密码</label>
          <div class="password-input">
            <input
              v-model="formData.oldPassword"
              :type="showOldPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入当前密码"
            />
            <button
              type="button"
              class="toggle-btn"
              @click="showOldPassword = !showOldPassword"
            >
              <svg v-if="!showOldPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M1 12s4-8 4-8 4 4 8 4 8-4M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17.94 17.94A10.07 10.07 0 0112 20zm-1-7.07a8 8 0 01-11.32 0"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="form-field">
          <label class="form-label">新密码</label>
          <div class="password-input">
            <input
              v-model="formData.newPassword"
              :type="showNewPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入新密码（至少6位）"
            />
            <button
              type="button"
              class="toggle-btn"
              @click="showNewPassword = !showNewPassword"
            >
              <svg v-if="!showNewPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M1 12s4-8 4-8 4 4 8 4 8-4M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17.94 17.94A10.07 10.07 0 0112 20zm-1-7.07a8 8 0 01-11.32 0"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="form-field">
          <label class="form-label">确认新密码</label>
          <div class="password-input">
            <input
              v-model="formData.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请再次输入新密码"
            />
            <button
              type="button"
              class="toggle-btn"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M1 12s4-8 4-8 4 4 8 4 8-4M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17.94 17.94A10.07 10.07 0 0112 20zm-1-7.07a8 8 0 01-11.32 0"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="formData.newPassword && formData.confirmPassword && formData.newPassword !== formData.confirmPassword" class="error-message">
          两次输入的新密码不一致
        </div>
      </form>

      <div class="modal-footer">
        <button type="button" class="btn-secondary" @click="handleClose">取消</button>
        <button type="button" class="btn-primary" @click="handleSubmit" :disabled="!canSubmit || submitting">
          {{ submitting ? '修改中...' : '确认修改' }}
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
  }
})

const emit = defineEmits(['update:visible', 'success'])

const authStore = useAuthStore()

const formData = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const error = ref('')
const submitting = ref(false)
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

const canSubmit = computed(() => {
  return formData.value.oldPassword &&
         formData.value.newPassword &&
         formData.value.confirmPassword &&
         formData.value.newPassword === formData.value.confirmPassword &&
         formData.value.newPassword.length >= 6
})

watch(() => props.visible, (val) => {
  if (val) {
    formData.value = {
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    error.value = ''
    showOldPassword.value = false
    showNewPassword.value = false
    showConfirmPassword.value = false
  }
})

async function handleSubmit() {
  error.value = ''

  // 验证
  if (!formData.value.oldPassword) {
    error.value = '请输入当前密码'
    return
  }

  if (!formData.value.newPassword) {
    error.value = '请输入新密码'
    return
  }

  if (formData.value.newPassword.length < 6) {
    error.value = '新密码长度不能少于6位'
    return
  }

  if (formData.value.newPassword !== formData.value.confirmPassword) {
    error.value = '两次输入的新密码不一致'
    return
  }

  submitting.value = true
  try {
    const result = await authStore.changePassword(
      formData.value.oldPassword,
      formData.value.newPassword
    )
    if (result.success) {
      notify.success('密码修改成功')
      handleClose()
      emit('success')
      // 重置表单
      formData.value = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } else {
      error.value = result.message || '修改密码失败'
    }
  } catch (e) {
    console.error('Change password error:', e)
    error.value = '修改密码失败，请稍后重试'
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
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #b4b4b4;
  margin-bottom: 8px;
}

.password-input {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input .form-input {
  padding-right: 40px;
}

.toggle-btn {
  position: absolute;
  right: 8px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #737373;
  cursor: pointer;
}

.toggle-btn:hover {
  color: #b4b4b4;
}

.toggle-btn svg {
  width: 18px;
  height: 18px;
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

.error-message {
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 6px;
  color: #ef4444;
  font-size: 13px;
  margin-top: -12px;
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
