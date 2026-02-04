<template>
  <div class="resource-detail-page">
    <!-- 左侧导航 -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
        </svg>
        <span>AI Native 研发平台</span>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
        <router-link to="/skills" class="nav-item">Skills</router-link>
        <router-link to="/mcp" class="nav-item">MCP Tools</router-link>
        <router-link to="/hooks" class="nav-item">Hooks</router-link>
        <router-link to="/admin" class="nav-item">Settings</router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info" v-if="currentUser">
          <div class="user-avatar">{{ (currentUser.name || currentUser.username || 'U').charAt(0).toUpperCase() }}</div>
          <div class="user-details">
            <div class="user-name">{{ currentUser.name || currentUser.username }}</div>
            <div class="user-role">{{ currentUser.role || 'Developer' }}</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 右侧内容 -->
    <main class="main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
        </svg>
      </div>

      <div v-else-if="resource" class="detail-container">
        <!-- 返回按钮 -->
        <button class="back-button" @click="$router.back()">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          返回
        </button>

        <!-- 重新设计的头部 -->
        <div class="detail-header">
          <!-- 第一行：名称 + 类型 + 版本 + 元信息 -->
          <div class="header-row header-row-main">
            <h1 class="resource-name">{{ resource.name }}</h1>
            <div class="header-right">
              <div class="header-badges">
                <div class="type-badge" :class="`type-${resource.type}`">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
                  </svg>
                  {{ resource.type.toUpperCase() }}
                </div>
                <span class="version">{{ resource.version || 'v1.0.0' }}</span>
              </div>
              <div class="header-meta-inline">
                <span v-if="resource.repository_owner" class="meta-item" title="仓库添加者">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M20 21v-2c0-1.1-.9-2-2-2H6c-1.1 0-2 .9-2 2v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  {{ resource.repository_owner }}
                </span>
                <span v-if="resource.repository_url" class="meta-item link-item" @click="openRepository" title="打开仓库">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M3 7v10c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2h-6l-2-2H5c-1.1 0-2 .9-2 2z"/>
                  </svg>
                  <svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5c-1.1 0-2-.9-2-2V8c0-1.1.9-2 2-2h6"/>
                    <polyline points="15 3 21 3 21 9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                  </svg>
                </span>
                <span class="meta-divider" v-if="(resource.repository_owner || resource.repository_url) && (resource.updated_at || resource.view_count || resource.install_count)">•</span>
                <span class="meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 8v4l3 3m-3-3v8"/>
                    <path d="M6 12h6"/>
                    <circle cx="12" cy="12" r="10"/>
                  </svg>
                  {{ formatDate(resource.updated_at) }}
                </span>
                <span class="meta-divider">•</span>
                <span class="meta-item stat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  {{ formatNumber(resource.view_count) }}
                </span>
                <span class="meta-divider">•</span>
                <span class="meta-item stat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15v4c0 .5304-.2107 1.0391-.5858 1.4142-.3905.3752-.8787.5858-1.4142.5858H5c-.5304 0-1.0391-.2107-1.4142-.5858C3.2107 17.0391 3 16.5304 3 16v-4"/>
                    <path d="M7 10l5 5 5-5"/>
                    <path d="M12 3v12"/>
                  </svg>
                  {{ formatNumber(resource.install_count) }}
                </span>
              </div>
            </div>
          </div>

          <!-- 第二行：描述 -->
          <div v-if="resource.description" class="header-description">
            {{ resource.description }}
          </div>

          <!-- 第三行：安装命令 -->
          <div class="command-area">
            <span class="command-prompt">$</span>
            <code class="command-text">{{ resource.install_command }}</code>
            <button class="copy-icon-btn" @click="copyCommand" :title="copied ? '已复制!' : '复制命令'">
              <svg v-if="!copied" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="9" y="9" width="13" height="13" rx="2"/>
                <path d="M5 15H4c-.5304 0-1.0391-.2107-1.4142-.5858C2.2107 14.2107 2 13.5304 2 13V4c0-.5304.2107-1.0391.5858-1.4142C2.9609 2.2107 3.4696 2 4 2h9c.5304 0 1.0391.2107 1.4142.5858C14.7893 2.7893 15 3.4696 15 4v1"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
            </button>
            <button class="install-inline-btn" @click="handleInstall" :disabled="installing">
              <svg v-if="!installing" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15"/>
                <path d="M7 10L12 15L17 10M12 15V3"/>
              </svg>
              <svg v-else class="spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4"/>
              </svg>
              {{ installing ? '安装中...' : '安装' }}
            </button>
          </div>
        </div>

        <!-- 内容 -->
        <div v-if="resource.readme_content" class="content-section">
          <div class="section-header">
            <div class="section-header-left">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"/>
                <path d="M14 2V8H20"/>
              </svg>
              <span>内容</span>
            </div>
            <div class="view-mode-toggle">
              <button
                class="mode-btn"
                :class="{ active: contentViewMode === 'preview' }"
                @click="contentViewMode = 'preview'"
                title="预览模式"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M1 12s4-8 11-8 11 11 0 0 0 11 8 8 8 0 0 0-11-8 8 8 0 0 0-11 8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <span>预览</span>
              </button>
              <button
                class="mode-btn"
                :class="{ active: contentViewMode === 'markdown' }"
                @click="contentViewMode = 'markdown'"
                title="Markdown 源码"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"/>
                  <path d="M14 2V8H20"/>
                  <path d="M9 11h6M9 15h6"/>
                </svg>
                <span>Markdown</span>
              </button>
            </div>
          </div>
          <div v-if="contentViewMode === 'preview'" class="readme-content" v-html="renderMarkdown(resource.readme_content)"></div>
          <pre v-else class="markdown-source">{{ resource.readme_content }}</pre>
        </div>

        <!-- 元数据 -->
        <div v-if="resource.extra_data && Object.keys(resource.extra_data).length > 0" class="content-section">
          <div class="section-header">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="3" y="3" width="7" height="7"/>
              <rect x="14" y="3" width="7" height="7"/>
              <rect x="14" y="14" width="7" height="7"/>
              <rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span>元数据</span>
          </div>
          <pre class="metadata-content">{{ JSON.stringify(resource.extra_data, null, 2) }}</pre>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/>
          <path d="M12 8V12L15 15"/>
        </svg>
        <p>资源不存在</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { resourceApi } from '@/api/resources'
import { notify } from '@/utils/notification'

const route = useRoute()
const router = useRouter()

const resource = ref(null)
const loading = ref(true)
const installing = ref(false)
const copied = ref(false)
const contentViewMode = ref('preview')
const currentUser = ref(null)

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

onMounted(() => {
  currentUser.value = getCurrentUser()
  loadResource()
})

async function loadResource() {
  loading.value = true
  try {
    const res = await resourceApi.getDetail(route.params.id)
    if (res.success) {
      resource.value = res.data
    } else {
      notify.error(res.message || '加载失败')
    }
  } catch (e) {
    console.error('Failed to load resource:', e)
    notify.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function handleInstall() {
  installing.value = true
  try {
    const res = await resourceApi.recordInstall(resource.value.id)
    if (res.success) {
      resource.value.install_count++
      notify.success('安装记录成功！')
      copyCommand()
    }
  } catch (e) {
    console.error('Failed to record install:', e)
  } finally {
    installing.value = false
  }
}

function copyCommand() {
  const command = resource.value.install_command
  navigator.clipboard.writeText(command).then(() => {
    copied.value = true
    notify.success('命令已复制到剪贴板')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }).catch(() => {
    notify.warning('复制失败，请手动复制')
  })
}

function openRepository() {
  if (resource.value?.repository_url) {
    window.open(resource.value.repository_url, '_blank')
  }
}

function formatNumber(num) {
  if (!num) return '0'
  return num.toLocaleString()
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}月前`
  return `${Math.floor(days / 365)}年前`
}

function renderMarkdown(content) {
  if (!content) return ''
  return content
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/\n/gim, '<br>')
}
</script>

<style scoped>
.resource-detail-page {
  display: flex;
  height: 100vh;
  background: var(--color-bg-primary);
}

/* 侧边栏样式 */
.sidebar {
  width: 220px;
  background: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
  border-bottom: 1px solid var(--color-border);
}

.sidebar-logo svg {
  width: 28px;
  height: 28px;
  color: var(--color-blue);
}

.sidebar-logo span {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 14px;
  transition: all var(--transition-fast);
}

.nav-item:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.nav-item.active {
  color: var(--color-text-primary);
  background: var(--color-blue);
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--color-border);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-blue);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: var(--color-text-muted);
}

/* 主内容区 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
}

/* 返回按钮 */
.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 24px;
}

.back-button:hover {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-color: var(--color-border-light);
}

.back-button svg {
  width: 16px;
  height: 16px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.spinner {
  width: 40px;
  height: 40px;
  color: var(--color-blue);
  animation: spin 1s linear infinite;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 容器 */
.detail-container {
  max-width: 900px;
}

/* 重新设计的头部 */
.detail-header {
  padding: var(--space-6);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
}

/* 头部行通用样式 */
.header-row {
  display: flex;
  align-items: center;
}

/* 第一行：名称 + 类型徽章 + 版本 */
.header-row-main {
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  gap: var(--space-4);
}

.resource-name {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.3;
  flex: 1;
}

.header-badges {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

/* 第一行右侧容器 */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  flex-shrink: 0;
}

/* 内联元信息 */
.header-meta-inline {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: 12px;
  color: var(--color-text-secondary);
}

.header-meta-inline .meta-item svg {
  width: 13px;
  height: 13px;
  opacity: 0.7;
}

.header-meta-inline .meta-item.stat {
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-meta-inline .meta-item.stat svg {
  opacity: 1;
}

.header-meta-inline .meta-divider {
  margin: 0 var(--space-2);
  color: var(--color-border);
}

.header-meta-inline .meta-item.link-item {
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.header-meta-inline .meta-item.link-item:hover {
  color: var(--color-blue);
}

.header-meta-inline .meta-item.link-item svg {
  opacity: 0.7;
}

.header-meta-inline .meta-item.link-item:hover svg {
  opacity: 1;
}

.header-meta-inline .external-icon {
  position: absolute;
  width: 10px;
  height: 10px;
  top: 50%;
  right: -6px;
  transform: translate(100%, -50%);
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.header-meta-inline .meta-item.link-item:hover .external-icon {
  opacity: 1;
}

.type-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-badge svg {
  width: 12px;
  height: 12px;
}

.type-badge.type-skill {
  background: rgba(33, 150, 243, 0.15);
  color: var(--color-blue);
}

.type-badge.type-mcp {
  background: rgba(0, 255, 0, 0.15);
  color: var(--color-green);
}

.type-badge.type-hook {
  background: rgba(168, 85, 247, 0.15);
  color: var(--color-purple);
}

.version {
  padding: 4px 8px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

/* 第二行：描述 */
.header-description {
  margin-bottom: var(--space-4);
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* 第三行：命令区域 */
.command-area {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.command-area:hover {
  border-color: var(--color-blue);
}

.command-prompt {
  color: var(--color-green);
  font-family: 'Courier New', monospace;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.command-text {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.copy-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: none;
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.copy-icon-btn svg {
  width: 16px;
  height: 16px;
}

.copy-icon-btn:hover {
  background: var(--color-blue);
  color: var(--color-bg-primary);
}

.copy-icon-btn.copied {
  background: var(--color-green);
  color: var(--color-bg-primary);
}

/* 命令行内的安装按钮 */
.install-inline-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--color-border);
  background: var(--color-blue);
  color: var(--color-bg-primary);
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.install-inline-btn svg {
  width: 14px;
  height: 14px;
}

.install-inline-btn:hover:not(:disabled) {
  background: var(--color-blue-light);
}

.install-inline-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 内容区域 */
.content-section {
  padding: var(--space-6);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.section-header-left {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.section-header svg {
  width: 18px;
  height: 18px;
  color: var(--color-blue);
}

/* 模式切换按钮 */
.view-mode-toggle {
  display: flex;
  gap: 2px;
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 2px;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.mode-btn svg {
  width: 14px;
  height: 14px;
}

.mode-btn:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.mode-btn.active {
  background: var(--color-blue);
  color: var(--color-bg-primary);
}

.mode-btn.active svg {
  color: var(--color-bg-primary);
}

/* Markdown 源码显示 */
.markdown-source {
  background: var(--color-bg-tertiary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: 0;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  overflow-x: auto;
  color: var(--color-text-secondary);
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* README */
.readme-content {
  line-height: 1.7;
  color: var(--color-text-secondary);
}

.readme-content :deep(h1),
.readme-content :deep(h2),
.readme-content :deep(h3) {
  margin-top: var(--space-4);
  margin-bottom: var(--space-2);
  color: var(--color-text-primary);
}

.readme-content :deep(code) {
  background: var(--color-bg-tertiary);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--color-green);
}

.readme-content :deep(pre) {
  background: var(--color-bg-tertiary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: var(--space-3) 0;
}

.readme-content :deep(pre code) {
  padding: 0;
  background: none;
}

/* 元数据 */
.metadata-content {
  background: var(--color-bg-tertiary);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  margin: 0;
  font-size: 12px;
  overflow-x: auto;
  color: var(--color-text-secondary);
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-text-tertiary);
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-3);
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 响应式 */
@media (max-width: 640px) {
  .sidebar {
    display: none;
  }

  .main-content {
    padding: 20px;
  }

  .header-row-main {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
  }

  .header-right {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-3);
    width: 100%;
  }

  .header-badges {
    width: 100%;
  }

  .header-meta-inline {
    font-size: 11px;
    flex-wrap: wrap;
  }

  .resource-name {
    font-size: 20px;
  }

  .command-area {
    flex-wrap: wrap;
    padding: var(--space-3);
  }

  .command-text {
    min-width: 0;
    flex-basis: 100%;
    margin-bottom: var(--space-2);
  }

  .install-inline-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
