<template>
  <!-- 页面内容 -->
  <div class="repository-manage-page">
    <!-- 操作栏 -->
    <div class="action-bar">
      <span class="repo-count">{{ repositories.length }} 个仓库</span>
      <button class="btn btn--primary" @click="showAddDialog">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        添加仓库
      </button>
    </div>

    <!-- 仓库列表 -->
    <div class="repo-list">
      <div
        v-for="repo in repositories"
        :key="repo.id"
        class="repo-card"
        :class="{ 'repo-card--disabled': !repo.enabled }"
      >
        <div class="repo-card__header">
          <div class="repo-card__left">
            <div class="repo-card__icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 7v10c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2h-6l-2-2H5c-1.1 0-2 .9-2 2z"/>
              </svg>
            </div>
            <div class="repo-card__info">
              <h3 class="repo-card__name">
                {{ repo.name }}
                <span v-if="!repo.enabled" class="badge badge--disabled">已禁用</span>
              </h3>
              <p class="repo-card__url">{{ repo.url }}</p>
              <p v-if="repo.description" class="repo-card__desc">{{ repo.description }}</p>
            </div>
          </div>
          <div class="repo-card__status" :class="`status--${getStatusClass(repo.sync_status)}`">
            {{ getStatusText(repo.sync_status) }}
          </div>
        </div>

        <div class="repo-card__meta" v-if="repo.branch || repo.path">
          <span v-if="repo.branch" class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M11 4H4v2h7V4z"/><path d="M4 8h4v2H4V8z"/><path d="M4 12h5v2H4v-2z"/></svg>
            {{ repo.branch }}
          </span>
          <span v-if="repo.path" class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M14 1H2v14h12V1zM3 2h10v12H3V2z"/></svg>
            {{ repo.path }}
          </span>
          <span class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><circle cx="5" cy="5" r="3"/><path d="M5 9a5 5 0 0 0-5 5h10a5 5 0 0 0-5-5z"/></svg>
            {{ getAuthTypeText(repo.auth_type) }}
          </span>
          <span class="meta-tag">
            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 3a5 5 0 1 0 0 10 5 5 0 0 0 0-10z"/></svg>
            {{ getSyncModeText(repo.sync_mode) }}
          </span>
        </div>

        <div class="repo-card__footer">
          <div class="repo-stats">
            <span class="stat">
              <strong>{{ repo.resource_count || 0 }}</strong>
              <small>资源</small>
            </span>
            <span class="stat">
              <strong>{{ formatDate(repo.last_sync_at) }}</strong>
              <small>最后同步</small>
            </span>
          </div>
          <div class="repo-actions">
            <button class="icon-btn" @click="handleToggle(repo)" :title="repo.enabled ? '禁用' : '启用'" :class="{ 'icon-btn--active': repo.enabled }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path v-if="repo.enabled" d="M12 6v12M8 10l4 4 4-4"/>
                <path v-else d="M15 9l-6 6M9 9l6 6"/>
              </svg>
            </button>
            <button class="icon-btn" @click="handleSync(repo)" :disabled="!repo.enabled || repo.syncing" title="同步">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" :class="{ 'spinning': repo.syncing }">
                <path d="M23 4v6h-6M1 20v-6h6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
            </button>
            <button class="icon-btn" @click="showEditDialog(repo)" title="编辑">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="icon-btn icon-btn--danger" @click="handleDelete(repo)" title="删除">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="repositories.length === 0 && !loading" class="empty-state">
        <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M8 16v36c0 2.2 1.8 4 4 4h40c2.2 0 4-1.8 4-4V24c0-2.2-1.8-4-4-4H32l-4-4H12c-2.2 0-4 1.8-4 4z"/>
        </svg>
        <p>暂无仓库</p>
        <button class="btn btn--primary" @click="showAddDialog">添加第一个仓库</button>
      </div>
    </div>

    <!-- 仓库表单对话框 -->
    <RepositoryFormDialog
      v-model:visible="showRepoDialog"
      :edit-repo="editRepoData"
      @success="onDialogSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { repositoryApi } from '@/api/repositories'
import { notify } from '@/utils/notification'
import RepositoryFormDialog from '@/components/RepositoryFormDialog.vue'

const repositories = ref([])
const loading = ref(false)
const showRepoDialog = ref(false)
const editRepoData = ref(null)

onMounted(() => {
  loadRepositories()
})

async function loadRepositories() {
  loading.value = true
  try {
    const res = await repositoryApi.getList()
    if (res.success) {
      repositories.value = res.data.map(item => ({ ...item, syncing: false }))
    }
  } catch (e) {
    console.error('Failed to load repositories:', e)
  } finally {
    loading.value = false
  }
}

function showAddDialog() {
  editRepoData.value = null
  showRepoDialog.value = true
}

function showEditDialog(repo) {
  editRepoData.value = repo
  showRepoDialog.value = true
}

function onDialogSuccess() {
  loadRepositories()
}

async function handleSync(repo) {
  repo.syncing = true
  try {
    const res = await repositoryApi.sync(repo.id)
    if (res.success) {
      notify.success(`同步成功: 新增 ${res.data.added} 个, 更新 ${res.data.updated} 个`)
      loadRepositories()
    } else {
      notify.error(res.message || '同步失败')
    }
  } catch (e) {
    console.error('Failed to sync repository:', e)
    notify.error('同步失败')
  } finally {
    repo.syncing = false
  }
}

async function handleToggle(repo) {
  try {
    const res = await repositoryApi.toggle(repo.id)
    if (res.success) {
      notify.success(res.message)
      loadRepositories()
    } else {
      notify.error(res.message || '操作失败')
    }
  } catch (e) {
    console.error('Failed to toggle repository:', e)
    notify.error('操作失败')
  }
}

async function handleDelete(repo) {
  if (confirm(`确定要删除仓库 "${repo.name}" 吗？此操作不可恢复。`)) {
    const res = await repositoryApi.delete(repo.id)
    if (res.success) {
      notify.success('删除成功')
      loadRepositories()
    } else {
      notify.error(res.message || '删除失败')
    }
  }
}

function getStatusClass(status) {
  const map = { pending: 'default', syncing: 'warning', success: 'success', failed: 'error' }
  return map[status] || 'default'
}

function getStatusText(status) {
  const map = { pending: '待同步', syncing: '同步中', success: '成功', failed: '失败' }
  return map[status] || status
}

function getAuthTypeText(type) {
  const map = { public: '公开仓库', token: 'Token 认证', ssh: 'SSH 密钥' }
  return map[type] || type
}

function getSyncModeText(mode) {
  const map = { manual: '手动同步', scheduled: '定时同步', webhook: 'Webhook' }
  return map[mode] || mode
}

function formatDate(dateStr) {
  if (!dateStr) return '从未'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))

  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
/* ==================== 页面容器 ==================== */
.repository-manage-page {
  width: 100%;
  max-width: 100%;
  position: relative;
}

/* ==================== 操作栏 ==================== */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 16px 20px;
  background: #1e1e1e;
  border: 1px solid #333333;
  border-radius: 8px;
}

.repo-count {
  font-size: 13px;
  color: #888;
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
  border: 1px solid #333333;
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

/* ==================== 仓库列表 ==================== */
.repo-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.repo-card {
  background: #1e1e1e;
  border: 1px solid #333333;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s;
}

.repo-card:hover:not(.repo-card--disabled) {
  border-color: #3b82f6;
}

.repo-card--disabled {
  opacity: 0.5;
}

.repo-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
}

.repo-card__left {
  display: flex;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.repo-card__icon {
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

.repo-card__icon svg {
  width: 20px;
  height: 20px;
}

.repo-card__info {
  flex: 1;
  min-width: 0;
}

.repo-card__name {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  margin: 0 0 4px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.repo-card__url {
  font-size: 12px;
  color: #888;
  margin: 0 0 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.repo-card__desc {
  font-size: 13px;
  color: #888;
  margin: 0;
  word-break: break-word;
}

.repo-card__status {
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

.repo-card__meta {
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

.repo-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #121212;
  border-top: 1px solid #333333;
}

.repo-stats {
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

.repo-actions {
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
  .repo-card__header {
    flex-direction: column;
    gap: 12px;
  }

  .repo-card__left {
    width: 100%;
  }

  .repo-card__status {
    align-self: flex-start;
  }

  .repo-card__footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .repo-stats {
    justify-content: center;
  }

  .repo-actions {
    justify-content: center;
  }
}
</style>
