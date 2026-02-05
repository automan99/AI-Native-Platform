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

      <!-- 标签切换 -->
      <div class="modal-tabs">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'url' }"
          @click="activeTab = 'url'"
        >URL 链接</button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'upload' }"
          @click="activeTab = 'upload'"
        >上传文件</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <!-- URL 方式 -->
        <div v-if="activeTab === 'url'" class="form-field">
          <label class="form-label">头像 URL</label>
          <input
            v-model="avatarUrl"
            type="url"
            class="form-input"
            placeholder="请输入图片 URL，例如: https://example.com/avatar.png"
          />
          <p class="form-hint">请输入有效的图片链接地址</p>
        </div>

        <!-- 上传方式 -->
        <div v-else class="form-field">
          <label class="form-label">选择图片</label>
          <div
            class="upload-zone"
            :class="{ dragging: isDragging, 'has-file': selectedFile }"
            @click="selectFile"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
          >
            <input
              ref="fileInput"
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
              @change="handleFileChange"
              style="display: none"
            />
            <div v-if="!selectedFile" class="upload-prompt">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="17,8 12,3 7,8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <p>点击或拖拽图片到此处</p>
              <span>支持 PNG、JPG、JPEG、GIF、WEBP，最大 5MB</span>
            </div>
            <div v-else class="selected-file">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21,15 16,10 5,21"/>
              </svg>
              <span>{{ selectedFile.name }}</span>
              <button type="button" class="clear-file" @click.stop="clearFile">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 预览 -->
        <div v-if="previewUrl" class="avatar-preview">
          <label class="form-label">预览</label>
          <div class="preview-container">
            <img
              v-if="!imageError"
              :src="previewUrl"
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
        <button
          type="button"
          class="btn-primary"
          @click="handleSubmit"
          :disabled="submitting || !canSubmit"
        >
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
import api from '@/api'

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

const activeTab = ref('url')
const avatarUrl = ref('')
const selectedFile = ref(null)
const previewUrl = ref('')
const error = ref('')
const submitting = ref(false)
const imageError = ref(false)
const isDragging = ref(false)
const fileInput = ref(null)

const canSubmit = computed(() => {
  return activeTab.value === 'url' ? avatarUrl.value?.trim() : selectedFile.value
})

watch(() => props.visible, (val) => {
  if (val) {
    activeTab.value = 'url'
    avatarUrl.value = ''
    selectedFile.value = null
    previewUrl.value = props.currentAvatar || ''
    error.value = ''
    imageError.value = false
  }
})

watch(() => avatarUrl.value, (val) => {
  previewUrl.value = val
  imageError.value = false
})

function selectFile() {
  fileInput.value?.click()
}

function handleFileChange(e) {
  const file = e.target.files?.[0]
  validateAndSetFile(file)
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer.files?.[0]
  validateAndSetFile(file)
}

function validateAndSetFile(file) {
  error.value = ''

  if (!file) return

  // 检查文件类型
  const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    error.value = '只支持 PNG、JPG、JPEG、GIF、WEBP 格式的图片'
    return
  }

  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    error.value = '文件大小不能超过 5MB'
    return
  }

  selectedFile.value = file
  // 生成预览
  previewUrl.value = URL.createObjectURL(file)
  imageError.value = false
}

function clearFile() {
  selectedFile.value = null
  previewUrl.value = props.currentAvatar || ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

async function handleSubmit() {
  error.value = ''

  if (activeTab.value === 'url') {
    await submitUrl()
  } else {
    await submitUpload()
  }
}

async function submitUrl() {
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

async function submitUpload() {
  if (!selectedFile.value) {
    error.value = '请选择图片文件'
    return
  }

  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    const result = await api.post('/user/avatar/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (result.success) {
      notify.success('头像上传成功')
      handleClose()
      emit('success')
    } else {
      error.value = result.message || '上传失败'
    }
  } catch (e) {
    console.error('Upload avatar error:', e)
    error.value = '上传失败，请稍后重试'
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
  max-width: 500px;
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

.modal-tabs {
  display: flex;
  gap: 4px;
  padding: 12px 20px 0;
  border-bottom: 1px solid #333;
}

.tab-btn {
  padding: 8px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #737373;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s;
  margin-bottom: -1px;
}

.tab-btn:hover {
  color: #b4b4b4;
}

.tab-btn.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
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

.upload-zone {
  border: 2px dashed #444;
  border-radius: 8px;
  padding: 32px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #121212;
}

.upload-zone:hover {
  border-color: #666;
  background: #1a1a1a;
}

.upload-zone.dragging {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
}

.upload-zone.has-file {
  border-style: solid;
  border-color: #3b82f6;
}

.upload-prompt svg {
  width: 40px;
  height: 40px;
  color: #737373;
  margin-bottom: 12px;
}

.upload-prompt p {
  margin: 0 0 4px;
  font-size: 14px;
  color: #b4b4b4;
}

.upload-prompt span {
  font-size: 12px;
  color: #737373;
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
}

.selected-file svg {
  width: 24px;
  height: 24px;
  color: #3b82f6;
  flex-shrink: 0;
}

.selected-file span {
  flex: 1;
  font-size: 13px;
  color: #fff;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-file {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  border-radius: 4px;
  color: #737373;
  cursor: pointer;
  flex-shrink: 0;
}

.clear-file:hover {
  background: #333;
  color: #fff;
}

.clear-file svg {
  width: 16px;
  height: 16px;
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
