<template>
  <div v-if="visible" class="modal-overlay" @click.self="handleClose">
    <div class="modal" :class="{ show: visible }">
      <div class="modal-header">
        <h3>更换头像</h3>
        <button class="modal-close" @click="handleClose">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-field">
          <label class="form-label">头像 URL</label>
          <input
            v-model="avatarUrl"
            type="url"
            class="form-input"
            placeholder="请输入图片 URL，例如: https://example.com/avatar.png"
          />
          <p class="form-hint">请输入有效的图片链接地址</p>
        </div>

        <div v-if="avatarUrl" class="avatar-preview">
          <label class="form-label">预览</label>
          <div class="preview-container">
            <img
              v-if="!imageError"
              :src="avatarUrl"
              alt="Avatar preview"
              @error="imageError = true"
            />
            <div v-else class="preview-error">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4M12 16h.01"/>
              </svg>
              <span>图片加载失败</span>
            </div>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>

      <div class="modal-footer">
        <button type="button" class="btn-secondary" @click="handleClose">取消</button>
        <button type="button" class="btn-primary" @click="handleSubmit" :disabled="submitting || !avatarUrl">
          {{ submitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useAuthStore } from '@/store/auth'
import { notify } from '@/utils/notification'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  currentAvatar: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:visible', 'success'])

const authStore = useAuthStore()

const avatarUrl = ref('')
const error = ref('')
const submitting = ref(false)
const imageError = ref(false)

watch(() => props.visible, (val) => {
  if (val) {
    avatarUrl.value = props.currentAvatar || ''
    error.value = ''
    imageError.value = false
  }
})

watch(() => avatarUrl.value, () => {
  // 当 URL 改变时重置图片错误状态
  imageError.value = false
})

async function handleSubmit() {
  error.value = ''

  if (!avatarUrl.value?.trim()) {
    error.value = '请输入头像 URL'
    return
  }

  // URL 格式验证
  try {
    new URL(avatarUrl.value)
  } catch {
    error.value = '请输入有效的 URL 地址'
    return
  }

  submitting.value = true
  try {
    const result = await authStore.updateAvatar(avatarUrl.value)
    if (result.success) {
      notify.success('头像更新成功')
      handleClose()
      emit('success')
    } else {
      error.value = result.message || '更新头像失败'
    }
  } catch (e) {
    console.error('Update avatar error:', e)
    error.value = '更新头像失败，请稍后重试'
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
  max-width: 450px;
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

.form-hint {
  font-size: 12px;
  color: #737373;
  margin-top: 6px;
}

.avatar-preview {
  margin-top: 16px;
}

.preview-container {
  width: 100%;
  height: 200px;
  background: #121212;
  border: 1px solid #333;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.preview-container img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.preview-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #737373;
}

.preview-error svg {
  width: 32px;
  height: 32px;
}

.preview-error span {
  font-size: 13px;
}

.error-message {
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 6px;
  color: #ef4444;
  font-size: 13px;
  margin-top: 12px;
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
