<template>
  <main class="resource-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
      </svg>
    </div>

    <template v-else-if="resource">
      <div class="detail-layout">
        <!-- 左侧信息面板 -->
        <aside class="info-panel">
          <!-- 返回按钮 -->
          <button class="back-button" @click="$router.back()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            返回
          </button>

          <!-- 资源标题和类型 -->
          <h1 class="resource-name">{{ resource.name }}</h1>

          <!-- 类型徽章 -->
          <div class="type-badge" :class="`type-${resource.type}`">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
            </svg>
            <span>{{ resource.type.toUpperCase() }}</span>
          </div>

          <!-- 描述 -->
          <div v-if="resource.description" class="description">
            {{ resource.description }}
          </div>

          <!-- 安装命令 -->
          <div class="install-section">
            <div class="command-box">
              <span class="prompt">$</span>
              <code class="command">{{ resource.install_command }}</code>
              <button class="copy-btn" @click="copyCommand" :title="copied ? '已复制!' : '复制'">
                <svg v-if="!copied" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="9" y="9" width="13" height="13" rx="2"/>
                  <path d="M5 15H4c-.5304 0-1.0391-.2107-1.4142-.5858C2.2107 14.2107 2 13.5304 2 13V4c0-.5304.2107-1.0391.5858-1.4142C2.9609 2.2107 3.4696 2 4 2h9c.5304 0 1.0391.2107 1.4142.5858C14.7893 2.7893 15 3.4696 15 4v1"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
              </button>
            </div>
            <button class="install-action-btn" @click="handleInstall" :disabled="installing">
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

          <!-- 统计信息 -->
          <div class="stats">
            <div class="stat-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M1 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7Z"/>
                <circle cx="10" cy="12" r="3"/>
              </svg>
              <span>{{ formatNumber(resource.view_count) }}</span>
              <span>浏览</span>
            </div>
            <div class="stat-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15v4c0 .5304-.2107 1.0391-.5858 1.4142-.3905.3752-.8787.5858-1.4142.5858H5c-.5304 0-1.0391-.2107-1.4142-.5858C3.2107 17.0391 3 16.5304 3 16v-4"/>
                <path d="M7 10l5 5 5-5"/>
                <path d="M12 3v12"/>
              </svg>
              <span>{{ formatNumber(resource.install_count) }}</span>
              <span>安装</span>
            </div>
          </div>

          <!-- 元信息 -->
          <div class="meta-info">
            <div class="meta-row" v-if="resource.version">
              <span class="meta-label">版本</span>
              <span class="meta-value">{{ resource.version }}</span>
            </div>
            <div class="meta-row" v-if="resource.repository_owner">
              <span class="meta-label">作者</span>
              <span class="meta-value">{{ resource.repository_owner }}</span>
            </div>
            <div class="meta-row" v-if="resource.updated_at">
              <span class="meta-label">更新</span>
              <span class="meta-value">{{ formatDate(resource.updated_at) }}</span>
            </div>
            <div class="meta-row" v-if="resource.repository_url">
              <a class="repo-link" :href="resource.repository_url" target="_blank">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M3 7v10c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2h-6l-2-2H5c-1.1 0-2 .9-2 2z"/>
                </svg>
                打开仓库
              </a>
            </div>
          </div>

          <!-- 元数据 -->
          <div v-if="resource.extra_data && Object.keys(resource.extra_data).length > 0" class="extra-data">
            <div class="extra-data-header">元数据</div>
            <pre class="extra-data-content">{{ JSON.stringify(resource.extra_data, null, 2) }}</pre>
          </div>
        </aside>

        <!-- 右侧内容区域 -->
        <section class="content-panel">
          <div v-if="resource.readme_content" class="readme-container">
            <div class="readme-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"/>
                <path d="M14 2V8H20"/>
              </svg>
              <span>SKILL.md</span>
              <div class="view-mode-toggle">
                <button
                  class="mode-btn"
                  :class="{ active: contentViewMode === 'preview' }"
                  @click="contentViewMode = 'preview'"
                  title="预览模式"
                >
                  预览
                </button>
                <button
                  class="mode-btn"
                  :class="{ active: contentViewMode === 'markdown' }"
                  @click="contentViewMode = 'markdown'"
                  title="Markdown 源码"
                >
                  源码
                </button>
              </div>
            </div>
            <div v-if="contentViewMode === 'preview'" class="readme-content" v-html="renderMarkdown(resource.readme_content)"></div>
            <pre v-else class="markdown-source">{{ resource.readme_content }}</pre>
          </div>
          <div v-else class="no-readme">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"/>
            </svg>
            <p>暂无 SKILL 内容</p>
          </div>
        </section>
      </div>
    </template>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 8V12L15 15"/>
      </svg>
      <p>资源不存在</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { resourceApi } from '@/api/resources'
import { notify } from '@/utils/notification'

const route = useRoute()

const resource = ref(null)
const loading = ref(true)
const installing = ref(false)
const copied = ref(false)
const contentViewMode = ref('preview')

onMounted(() => {
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
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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

/* 主布局 */
.detail-layout {
  display: flex;
  flex: 1;
  min-height: 0;
  gap: 0;
}

/* 左侧信息面板 */
.info-panel {
  width: 320px;
  flex-shrink: 0;
  padding: 24px;
  background: var(--color-bg-surface);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
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
}

.back-button:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
  border-color: var(--color-border-light);
}

.back-button svg {
  width: 16px;
  height: 16px;
}

/* 资源图标 - 已删除，整合到类型徽章中 */

/* 资源名称 */
.resource-name {
  font-size: 22px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.3;
}

/* 类型徽章 */
.type-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-badge svg {
  width: 14px;
  height: 14px;
}

.type-badge.type-skill {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-blue);
}

.type-badge.type-mcp {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-green);
}

.type-badge.type-hook {
  background: rgba(168, 85, 247, 0.15);
  color: var(--color-purple);
}

/* 描述 */
.description {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

/* 安装区域 */
.install-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.command-box {
  display: flex;
  align-items: center;
  padding: 12px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: border-color var(--transition-fast);
}

.command-box:hover {
  border-color: var(--color-blue);
}

.prompt {
  color: var(--color-green);
  font-family: 'Courier New', monospace;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.command {
  flex: 1;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  color: var(--color-text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 0 8px;
}

.copy-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  border: none;
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.copy-btn svg {
  width: 14px;
  height: 14px;
}

.copy-btn:hover {
  background: var(--color-blue);
  color: var(--color-bg-primary);
}

.copy-btn.copied {
  background: var(--color-green);
  color: var(--color-bg-primary);
}

.install-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  background: var(--color-blue);
  color: var(--color-bg-primary);
  transition: all var(--transition-fast);
}

.install-action-btn svg {
  width: 16px;
  height: 16px;
}

.install-action-btn:hover:not(:disabled) {
  background: var(--color-blue-light);
}

.install-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 统计信息 */
.stats {
  display: flex;
  gap: 8px;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.stat-item svg {
  width: 16px;
  height: 16px;
  color: var(--color-text-muted);
}

.stat-item span:nth-child(2) {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.stat-item span:nth-child(3) {
  font-size: 11px;
  color: var(--color-text-muted);
}

/* 元信息 */
.meta-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--color-border);
}

.meta-row:last-child {
  border-bottom: none;
}

.meta-label {
  font-size: 13px;
  color: var(--color-text-muted);
}

.meta-value {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.repo-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-blue);
  text-decoration: none;
}

.repo-link svg {
  width: 14px;
  height: 14px;
}

.repo-link:hover {
  text-decoration: underline;
}

/* 元数据 */
.extra-data {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.extra-data-header {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.extra-data-content {
  margin: 0;
  padding: 12px;
  font-size: 11px;
  overflow-x: auto;
  color: var(--color-text-secondary);
  background: var(--color-bg-elevated);
  border-radius: var(--radius-md);
}

/* 右侧内容区域 */
.content-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg-primary);
}

.readme-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.readme-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 24px;
  background: var(--color-bg-surface);
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  flex-shrink: 0;
}

.readme-header svg {
  width: 18px;
  height: 18px;
  color: var(--color-blue);
}

.view-mode-toggle {
  margin-left: auto;
  display: flex;
  gap: 4px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 3px;
}

.mode-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 12px;
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
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

.readme-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
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
  background: var(--color-bg-elevated);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: var(--color-green);
}

.readme-content :deep(pre) {
  background: var(--color-bg-elevated);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: var(--space-3) 0;
}

.readme-content :deep(pre code) {
  padding: 0;
  background: none;
}

.markdown-source {
  flex: 1;
  margin: 0;
  padding: 24px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  overflow: auto;
  color: var(--color-text-secondary);
  background: var(--color-bg-elevated);
}

.no-readme {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-text-muted);
}

.no-readme svg {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.no-readme p {
  margin: 0;
  font-size: 14px;
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
@media (max-width: 768px) {
  .detail-layout {
    flex-direction: column;
  }

  .info-panel {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }

  .content-panel {
    min-height: 400px;
  }
}
</style>
