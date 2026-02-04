<template>
  <div class="mcp-manage-page">
    <!-- 页面标题栏 -->
    <div class="page-header">
      <h2 class="page-title">MCP Server 管理</h2>
      <button class="btn btn--primary" @click="showAddDialog">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        添加 Server
      </button>
    </div>

    <!-- Server 列表 -->
    <div class="server-list">
      <div
        v-for="server in filteredServers"
        :key="server.id"
        class="server-card"
        :class="{ 'server-card--disabled': !server.enabled }"
      >
        <div class="server-card__header">
          <div class="server-card__left">
            <div class="server-card__icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <circle cx="12" cy="12" r="4"/>
              </svg>
            </div>
            <div class="server-card__info">
              <h3 class="server-card__name">
                {{ server.name }}
                <span v-if="!server.enabled" class="badge badge--disabled">已禁用</span>
                <span class="badge" :class="`badge--${server.transport_type}`">{{ server.transport_type.toUpperCase() }}</span>
              </h3>
              <p v-if="server.description" class="server-card__description">{{ server.description }}</p>
            </div>
          </div>
          <div class="server-card__status" :class="`status--${getSyncStatusClass(server)}`">
            {{ getSyncStatusText(server) }}
          </div>
        </div>

        <div class="server-card__meta">
          <span v-if="server.transport_type === 'stdio'" class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4 2h8v2H4z"/><path d="M2 6h12v2H2z"/><path d="M2 10h12v2H2z"/><path d="M4 14h8v2H4z"/></svg>
            {{ server.command || '未知命令' }}
          </span>
          <span v-if="server.transport_type === 'http'" class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm0 14.5a6.5 6.5 0 110-13 6.5 6.5 0 010 13z"/><path d="M8 4a4 4 0 100 8 4 4 0 000-8z"/></svg>
            {{ server.url || '未知 URL' }}
          </span>
          <span class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 3a5 5 0 015 5h-2a3 3 0 00-3-3V3z"/><path d="M8 13a5 5 0 01-5-5h2a3 3 0 003 3v2z"/><path d="M13 8a5 5 0 01-5 5v-2a3 3 0 003-3h2z"/></svg>
            {{ server.timeout || 30 }}s 超时
          </span>
          <span v-if="server.contributor" class="meta-tag meta-tag--contributor">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 8a3 3 0 100-6 3 3 0 000 6zm0 0c1.535 0 2.848.541 3.805-1.5a1 1 0 10-1.61-1.19A2 2 0 118 8z"/><path d="M14 7.2a2 2 0 00-2-2c-.526 0-1 .135-1.4.355a4.969 4.969 0 00-6 0c-.422-.22-.874-.355-1.4-.355a2 2 0 00-2 2c0 .608.272 1.152.7 1.572a5 5 0 0010 0c.428.42.7.964.7 1.572zM8 .5a4.969 4.969 0 00-5 2.5c0 .626.216 1.207.574 1.672A5 5 0 018 3c.465-.465.672-1.046.672-1.672A4.969 4.969 0 008 .5z"/></svg>
            {{ server.contributor.name || server.contributor.username || '未知用户' }}
          </span>
        </div>

        <div class="server-card__footer">
          <div class="server-stats">
            <span class="stat">
              <strong>{{ server.total_tools || 0 }}</strong>
              <small>Tools</small>
            </span>
            <span class="stat">
              <strong>{{ server.total_resources || 0 }}</strong>
              <small>Resources</small>
            </span>
          </div>
          <div class="server-actions" v-if="canEditServer(server)">
            <button class="icon-btn" @click="handleToggle(server)" :title="server.enabled ? '禁用' : '启用'" :class="{ 'icon-btn--active': server.enabled }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path v-if="server.enabled" d="M12 6v12M8 10l4 4 4-4"/>
                <path v-else d="M15 9l-6 6M9 9l6 6"/>
              </svg>
            </button>
            <button class="icon-btn" @click="handleSync(server)" :disabled="!server.enabled || server.syncing" title="同步">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" :class="{ 'spinning': server.syncing }">
                <path d="M23 4v6h-6M1 20v-6h6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
            </button>
            <button class="icon-btn" @click="showEditDialog(server)" title="编辑">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="icon-btn icon-btn--danger" @click="handleDelete(server)" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredServers.length === 0 && !loading" class="empty-state">
        <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="12" y="12" width="40" height="40" rx="4"/>
          <circle cx="32" cy="32" r="8"/>
          <path d="M32 8v8M32 48v8M8 32h8M48 32h8"/>
        </svg>
        <p>暂无 MCP Server</p>
        <button class="btn btn--primary" @click="showAddDialog">添加第一个 Server</button>
      </div>
    </div>

    <!-- MCP Server 表单对话框 -->
    <MCPServerFormDialog
      v-model:visible="showServerDialog"
      :edit-server="editServerData"
      @success="onDialogSuccess"
    />
  </div>
</template>

<style scoped>
/* 模态框动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .dialog-modal,
.modal-leave-to .dialog-modal {
  transform: scale(0.96);
}

/* 模态框容器 */
.modal-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999 !important;
  padding: 16px;
}

.dialog-modal {
  background: #1e1e1e;
  border: 1px solid #333333;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #333333;
}

.dialog-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.dialog-close {
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dialog-close:hover {
  background: #333;
  color: #fff;
}

.dialog-close svg {
  width: 16px;
  height: 16px;
}

.dialog-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.dialog-body::-webkit-scrollbar {
  width: 6px;
}

.dialog-body::-webkit-scrollbar-track {
  background: #1e1e1e;
}

.dialog-body::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #333333;
  background: #1e1e1e;
}

/* 表单 */
.form-field {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #ccc;
  margin-bottom: 6px;
}

.required {
  color: #ef4444;
}

.form-input,
.form-textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid #333;
  border-radius: 8px;
  font-size: 14px;
  color: #fff;
  background: #1e1e1e;
  transition: border-color 0.2s;
}

.form-input--mono {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #666;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

/* 单选卡片 */
.radio-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.radio-card {
  position: relative;
}

.radio-card input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.radio-card > span {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  border: 1px solid #333;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  background: #1e1e1e;
}

.radio-card svg {
  width: 24px;
  height: 24px;
  color: #888;
}

.radio-card span span {
  font-size: 13px;
  font-weight: 500;
  color: #ccc;
}

.radio-card small {
  font-size: 11px;
  color: #666;
  font-weight: 400;
}

.radio-card:hover > span {
  background: #222;
  border-color: #444;
}

.radio-card--active > span {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.radio-card--active svg {
  color: #3b82f6;
}

/* 复选框 */
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #ccc;
}

.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #3b82f6;
}

.checkbox--large {
  padding: 12px;
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 8px;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.checkbox--large input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.checkbox-content strong {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #fff;
}

.checkbox-content small {
  display: block;
  font-size: 12px;
  color: #888;
  margin-top: 2px;
}

/* 按钮样式 */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn--primary {
  background: #3b82f6;
  color: white;
}

.btn--primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn--secondary {
  background: transparent;
  color: #ccc;
  border: 1px solid #333;
}

.btn--secondary:hover {
  background: #222;
  border-color: #444;
  color: #fff;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 640px) {
  .modal-overlay {
    padding: 12px;
  }

  .dialog-modal {
    max-width: 100%;
    max-height: 100vh;
    border-radius: 12px;
  }

  .dialog-header {
    padding: 16px;
  }

  .dialog-body {
    padding: 16px;
  }

  .dialog-footer {
    padding: 12px 16px;
  }

  .radio-cards {
    grid-template-columns: 1fr;
  }
}

/* ==================== 向导样式 ==================== */
.dialog-modal--wizard {
  max-width: 560px;
}

.dialog-body--wizard {
  padding: 0;
}

/* 步骤指示器 */
.wizard-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  border-bottom: 1px solid #333;
}

.wizard-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
  max-width: 100px;
}

.wizard-step__circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #121212;
  border: 2px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  color: #888;
  transition: all 0.2s;
}

.wizard-step--active .wizard-step__circle {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.wizard-step--completed .wizard-step__circle {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.wizard-step--completed .wizard-step__circle svg {
  width: 16px;
  height: 16px;
}

.wizard-step__label {
  font-size: 12px;
  color: #888;
  text-align: center;
}

.wizard-step--active .wizard-step__label {
  color: #fff;
  font-weight: 500;
}

/* 向导面板 */
.wizard-panel {
  padding: 20px;
}

.wizard-panel__title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.wizard-panel__desc {
  font-size: 13px;
  color: #888;
  margin-bottom: 20px;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

/* 配置摘要 */
.config-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.config-section {
  background: #121212;
  border: 1px solid #333;
  border-radius: 8px;
  overflow: hidden;
}

.config-section__title {
  font-size: 13px;
  font-weight: 500;
  color: #888;
  padding: 10px 16px;
  background: #1a1a1a;
  border-bottom: 1px solid #333;
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 16px;
  border-bottom: 1px solid #222;
}

.config-item:last-child {
  border-bottom: none;
}

.config-item__label {
  font-size: 13px;
  color: #888;
  flex-shrink: 0;
  width: 80px;
}

.config-item__value {
  font-size: 13px;
  color: #fff;
  text-align: right;
  word-break: break-all;
}

.config-item__value--mono {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
}

.config-item__value--badge {
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.badge--stdio {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge--http {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.config-item__value--status {
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-enabled {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.status-disabled {
  background: rgba(107, 114, 128, 0.15);
  color: #6b7280;
}

.dialog-footer--wizard {
  gap: 12px;
}

.dialog-footer--wizard .btn {
  flex: 1;
  justify-content: center;
}

/* Server 卡片描述 */
.server-card__description {
  font-size: 13px;
  color: #888;
  margin: 4px 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { mcpApi } from '@/api/mcp'
import { notify } from '@/utils/notification'
import MCPServerFormDialog from '@/components/MCPServerFormDialog.vue'

// Get current user from localStorage
const getCurrentUser = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
  return null
}

const currentUser = ref(getCurrentUser())
const servers = ref([])
const loading = ref(false)
const showServerDialog = ref(false)
const editServerData = ref(null)

// All servers (no filtering)
const filteredServers = computed(() => servers.value)

// Check if current user can edit the server
function canEditServer(server) {
  if (!currentUser.value) return false
  return server.user_id === currentUser.value.id
}

onMounted(() => {
  loadServers()
})

async function loadServers() {
  loading.value = true
  try {
    const res = await mcpApi.getServers()
    if (res.success) {
      servers.value = res.data.map(item => ({ ...item, syncing: false }))
    }
  } catch (e) {
    console.error('Failed to load servers:', e)
  } finally {
    loading.value = false
  }
}

function showAddDialog() {
  editServerData.value = null
  showServerDialog.value = true
}

function showEditDialog(server) {
  editServerData.value = server
  showServerDialog.value = true
}

function onDialogSuccess() {
  loadServers()
}

async function handleSubmit() {
  submitting.value = true
  try {
    const apiData = convertFormToApi()
    let res
    if (isEdit.value) {
      res = await mcpApi.update(currentEditId.value, apiData)
    } else {
      res = await mcpApi.create(apiData)
    }

    if (res.success) {
      notify.success(isEdit.value ? 'Server 更新成功' : 'Server 添加成功')
      closeDialog()
      loadServers()
    } else {
      notify.error(res.message || '操作失败')
    }
  } catch (e) {
    console.error('Failed to submit:', e)
    notify.error('操作失败')
  } finally {
    submitting.value = false
  }
}

async function handleSync(server) {
  server.syncing = true
  try {
    const res = await mcpApi.sync(server.id)
    if (res.success) {
      notify.success(`同步成功: ${res.data.tool_count} Tools, ${res.data.resource_count} Resources`)
      loadServers()
    } else {
      notify.error(res.message || '同步失败')
    }
  } catch (e) {
    console.error('Failed to sync server:', e)
    notify.error('同步失败')
  } finally {
    server.syncing = false
  }
}

async function handleToggle(server) {
  try {
    const res = await mcpApi.toggle(server.id)
    if (res.success) {
      notify.success(res.message)
      loadServers()
    } else {
      notify.error(res.message || '操作失败')
    }
  } catch (e) {
    console.error('Failed to toggle server:', e)
    notify.error('操作失败')
  }
}

async function handleDelete(server) {
  if (confirm(`确定要删除 Server "${server.name}" 吗？此操作不可恢复。`)) {
    try {
      const res = await mcpApi.delete(server.id)
      if (res.success) {
        notify.success('删除成功')
        loadServers()
      } else {
        notify.error(res.message || '删除失败')
      }
    } catch (e) {
      console.error('Failed to delete server:', e)
      notify.error('删除失败')
    }
  }
}

function getSyncStatusClass(server) {
  if (server.syncing) return 'warning'
  if (!server.enabled) return 'default'
  if (server.total_tools > 0) return 'success'
  return 'default'
}

function getSyncStatusText(server) {
  if (server.syncing) return '同步中'
  if (!server.enabled) return '已禁用'
  if (server.total_tools > 0) return '已同步'
  return '待同步'
}
</script>

<style scoped>
/* ==================== 页面容器 ==================== */
.mcp-manage-page {
  width: 100%;
  max-width: 100%;
  position: relative;
}

/* ==================== 页面标题栏 ==================== */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

/* ==================== 操作栏 ==================== */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.server-count {
  font-size: 13px;
  color: var(--color-text-muted);
}

/* ==================== 按钮 ==================== */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  position: relative;
  z-index: 1;
}

.btn svg {
  width: 18px;
  height: 18px;
  pointer-events: none;
}

.btn--primary {
  background: #3b82f6;
  color: white;
}

.btn--primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn--secondary {
  background: transparent;
  color: #ccc;
  border: 1px solid #333;
}

.btn--secondary:hover {
  background: #222;
  border-color: #444;
  color: #fff;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ==================== Server 列表 ==================== */
.server-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.server-card {
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
}

.server-card:hover:not(.server-card--disabled) {
  border-color: #3b82f6;
}

.server-card--disabled {
  opacity: 0.5;
}

.server-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
}

.server-card__left {
  display: flex;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.server-card__icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #121212;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  flex-shrink: 0;
}

.server-card__icon svg {
  width: 20px;
  height: 20px;
}

.server-card__info {
  flex: 1;
  min-width: 0;
}

.server-card__name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin: 0 0 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.server-card__code {
  font-size: 12px;
  color: #888;
  margin: 0;
  font-family: 'Courier New', monospace;
}

.server-card__status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.status--default { background: #121212; color: #888; }
.status--warning { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
.status--success { background: rgba(16, 185, 129, 0.2); color: #10b981; }
.status--error { background: rgba(239, 68, 68, 0.2); color: #ef4444; }

.server-card__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 16px 12px;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #121212;
  border-radius: 6px;
  font-size: 12px;
  color: #888;
}

.meta-tag svg {
  width: 14px;
  height: 14px;
  opacity: 0.7;
}

.server-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #121212;
  border-top: 1px solid #333;
}

.server-stats {
  display: flex;
  gap: 16px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat strong {
  font-size: 14px;
  color: #fff;
}

.stat small {
  font-size: 11px;
  color: #888;
}

.server-actions {
  display: flex;
  gap: 4px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #888;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.icon-btn svg {
  width: 18px;
  height: 18px;
}

.icon-btn:hover {
  background: #222;
  color: #fff;
}

.icon-btn--active {
  color: #10b981;
}

.icon-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.icon-btn--danger:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.badge--disabled {
  background: #121212;
  color: #666;
}

.badge--stdio {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge--http {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

/* ==================== 空状态 ==================== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #888;
}

.empty-state svg {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
  opacity: 0.4;
}

.empty-state p {
  margin: 0 0 20px;
  font-size: 14px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 768px) {
  .server-card__header {
    flex-direction: column;
    gap: 12px;
  }

  .server-card__left {
    width: 100%;
  }

  .server-card__status {
    align-self: flex-start;
  }

  .server-card__footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .server-stats {
    justify-content: center;
  }

  .server-actions {
    justify-content: center;
  }
}
</style>
