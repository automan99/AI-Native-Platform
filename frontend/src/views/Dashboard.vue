<template>
  <!-- 搜索区域 -->
      <div class="search-section">
        <div class="tagline">
          <span class="tagline-main">发现与管理 AI Agent 资源</span>
          <span class="tagline-sub">Skills · MCP · Hooks</span>
        </div>

        <div class="search-container">
          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="11" cy="11" r="8"/>
              <path d="M21 21L16.65 16.65"/>
            </svg>
            <input
              v-model="searchKeyword"
              ref="searchInput"
              type="text"
              class="search-input"
              placeholder="搜索 Skills、MCP、Hooks..."
              @keyup.enter="handleSearch"
            />
            <button v-if="searchKeyword" class="clear-btn" @click="clearSearch">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
            <button class="search-btn" @click="handleSearch">搜索</button>
          </div>
        </div>

        <!-- 数据统计标签 -->
        <div class="stats-tags">
          <div class="stat-tag" @click="$router.push('/skills')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
            </svg>
            <span class="stat-label">Skills</span>
            <span class="stat-value">{{ formatNumber(overview.total_skills) }}</span>
          </div>
          <div class="stat-tag" @click="$router.push('/mcp')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="4" y="4" width="16" height="16" rx="2"/>
              <circle cx="12" cy="12" r="4"/>
            </svg>
            <span class="stat-label">MCP</span>
            <span class="stat-value">{{ formatNumber(overview.total_mcps) }}</span>
          </div>
          <div class="stat-tag" @click="$router.push('/hooks')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18C5.68629 18 3 15.3137 3 12C3 8.68629 5.68629 6 9 6"/>
              <path d="M15 6C18.3137 6 21 8.68629 21 12C21 15.3137 18.3137 18 15 18"/>
              <circle cx="15" cy="12" r="3"/>
              <circle cx="9" cy="12" r="3"/>
            </svg>
            <span class="stat-label">Hooks</span>
            <span class="stat-value">{{ formatNumber(overview.total_hooks) }}</span>
          </div>
          <div class="stat-tag stat-tag-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
            <span class="stat-label">总浏览</span>
            <span class="stat-value">{{ formatNumber(totalViews) }}</span>
          </div>
          <div class="stat-tag stat-tag-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15v4c0 .5304-.2107 1.0391-.5858 1.4142-.3905.3752-.8787.5858-1.4142.5858H5c-.5304 0-1.0391-.2107-1.4142-.5858C3.2107 17.0391 3 16.5304 3 16v-4"/>
              <path d="M7 10l5 5 5-5"/>
              <path d="M12 3v12"/>
            </svg>
            <span class="stat-label">总下载</span>
            <span class="stat-value">{{ formatNumber(totalDownloads) }}</span>
          </div>
        </div>
      </div>

      <!-- 资源列表区域 -->
      <div class="resources-section" v-if="!isSearching">
        <!-- 热门与最新资源 -->
        <div class="content-grid">
          <!-- 热门资源 -->
          <div class="resource-section">
            <div class="section-header">
              <h3 class="section-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/>
                  <path d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z"/>
                </svg>
                热门资源
              </h3>
              <router-link to="/skills" class="section-more">查看全部</router-link>
            </div>
            <div v-if="topResources.length === 0" class="empty-state">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4l3 3"/>
              </svg>
              <p>暂无数据</p>
            </div>
            <div v-else class="resource-grid">
              <div
                v-for="(item, index) in topResources"
                :key="item.id"
                class="resource-card"
                @click="goToDetail(item.id)"
              >
                <div class="resource-card-header">
                  <span class="resource-rank" :class="`rank-${Math.min(index + 1, 3)}`">{{ index + 1 }}</span>
                  <div class="resource-icon" :class="`type-${item.type}`">
                    <component :is="getTypeIcon(item.type)" />
                  </div>
                </div>
                <h4 class="resource-card-name">{{ item.name }}</h4>
                <p class="resource-card-desc">{{ item.description || '暂无描述' }}</p>
                <div class="resource-card-meta">
                  <span class="resource-type">{{ item.type.toUpperCase() }}</span>
                  <span class="resource-stat">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15"/>
                      <path d="M7 10L12 15L17 10M12 15V3"/>
                    </svg>
                    {{ formatNumber(item.install_count) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- 最新资源 -->
          <div class="resource-section">
            <div class="section-header">
              <h3 class="section-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                最新资源
              </h3>
              <router-link to="/skills" class="section-more">查看全部</router-link>
            </div>
            <div v-if="latestResources.length === 0" class="empty-state">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 8v4l3 3"/>
              </svg>
              <p>暂无数据</p>
            </div>
            <div v-else class="resource-grid">
              <div
                v-for="item in latestResources"
                :key="item.id"
                class="resource-card"
                @click="goToDetail(item.id)"
              >
                <div class="resource-card-header">
                  <div class="resource-icon" :class="`type-${item.type}`">
                    <component :is="getTypeIcon(item.type)" />
                  </div>
                </div>
                <h4 class="resource-card-name">{{ item.name }}</h4>
                <p class="resource-card-desc">{{ item.description || '暂无描述' }}</p>
                <div class="resource-card-meta">
                  <span class="resource-type">{{ item.type.toUpperCase() }}</span>
                  <span class="resource-date">{{ formatDate(item.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div class="search-results" v-else>
        <div class="search-results-header">
          <span>搜索 "{{ searchKeyword }}" 的结果</span>
          <button class="clear-search-btn" @click="clearSearch">清除搜索</button>
        </div>
        <div v-if="searchResults.length === 0" class="empty-state">
          <p>未找到相关资源</p>
        </div>
        <div v-else class="resource-grid">
          <div
            v-for="item in searchResults"
            :key="item.id"
            class="resource-card"
            @click="goToDetail(item.id)"
          >
            <div class="resource-card-header">
              <div class="resource-icon" :class="`type-${item.type}`">
                <component :is="getTypeIcon(item.type)" />
              </div>
            </div>
            <h4 class="resource-card-name">{{ item.name }}</h4>
            <p class="resource-card-desc">{{ item.description || '暂无描述' }}</p>
            <div class="resource-card-meta">
              <span class="resource-type">{{ item.type.toUpperCase() }}</span>
              <span class="resource-stat">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15"/>
                  <path d="M7 10L12 15L17 10M12 15V3"/>
                </svg>
                {{ formatNumber(item.install_count) }}
              </span>
            </div>
          </div>
        </div>
      </div>
  <!-- 搜索区域 ends here -->
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { statsApi } from '@/api/stats'
import { resourceApi } from '@/api/resources'

const router = useRouter()

const searchInput = ref(null)
const overview = ref({})
const topResources = ref([])
const latestResources = ref([])
const searchKeyword = ref('')
const searchResults = ref([])
const isSearching = ref(false)

const totalViews = computed(() => {
  return [...topResources.value, ...latestResources.value].reduce((sum, item) => sum + (item.view_count || 0), 0)
})

const totalDownloads = computed(() => {
  return [...topResources.value, ...latestResources.value].reduce((sum, item) => sum + (item.install_count || 0), 0)
})

onMounted(() => {
  loadOverview()
  loadTopResources()
  loadLatestResources()

  // Focus search input on mount
  if (searchInput.value) {
    searchInput.value.focus()
  }
})

async function loadOverview() {
  try {
    const res = await statsApi.getOverview()
    if (res.success) {
      overview.value = res.data
    }
  } catch (e) {
    console.error('Failed to load overview:', e)
  }
}

async function loadTopResources() {
  try {
    const res = await statsApi.getTop({ limit: 6 })
    if (res.success) {
      topResources.value = res.data
    }
  } catch (e) {
    console.error('Failed to load top resources:', e)
  }
}

async function loadLatestResources() {
  try {
    const res = await statsApi.getLatest({ limit: 6 })
    if (res.success) {
      latestResources.value = res.data
    }
  } catch (e) {
    console.error('Failed to load latest resources:', e)
  }
}

async function handleSearch() {
  if (!searchKeyword.value.trim()) return

  isSearching.value = true
  try {
    const res = await resourceApi.getList({
      keyword: searchKeyword.value,
      page: 1,
      page_size: 20
    })
    if (res.success) {
      searchResults.value = res.data
    }
  } catch (e) {
    console.error('Search failed:', e)
  }
}

function clearSearch() {
  searchKeyword.value = ''
  searchResults.value = []
  isSearching.value = false
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
  return date.toLocaleDateString('zh-CN')
}

function goToDetail(id) {
  router.push(`/resource/${id}`)
}

function getTypeIcon(type) {
  const icons = {
    skill: 'SkillIcon',
    mcp: 'McpIcon',
    hook: 'HookIcon'
  }
  return icons[type] || 'SkillIcon'
}
</script>

<script>
import { h } from 'vue'

const SkillIcon = {
  render() {
    return h('svg', {
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '1.5'
    }, [
      h('path', { d: 'M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z' })
    ])
  }
}

const McpIcon = {
  render() {
    return h('svg', {
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '1.5'
    }, [
      h('rect', { x: '4', y: '4', width: '16', height: '16', rx: '2' }),
      h('circle', { cx: '12', cy: '12', r: '4' })
    ])
  }
}

const HookIcon = {
  render() {
    return h('svg', {
      viewBox: '0 0 24 24',
      fill: 'none',
      stroke: 'currentColor',
      'stroke-width': '1.5'
    }, [
      h('path', { d: 'M9 18C5.68629 18 3 15.3137 3 12C3 8.68629 5.68629 6 9 6' }),
      h('path', { d: 'M15 6C18.3137 6 21 8.68629 21 12C21 15.3137 18.3137 18 15 18' }),
      h('circle', { cx: '15', cy: '12', r: '3' }),
      h('circle', { cx: '9', cy: '12', r: '3' })
    ])
  }
}

export default {
  components: {
    SkillIcon,
    McpIcon,
    HookIcon
  }
}
</script>

<style scoped>
/* 主内容区 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 搜索区域 */
.search-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: var(--space-10);
  margin-top: var(--space-8);
}

.tagline {
  text-align: center;
  margin-bottom: var(--space-8);
}

.tagline-main {
  display: block;
  font-size: 28px;
  font-weight: 600;
  color: var(--color-blue);
  margin-bottom: var(--space-2);
}

.tagline-sub {
  display: block;
  font-size: 16px;
  color: var(--color-text-secondary);
}

.search-container {
  width: 100%;
  max-width: 580px;
  margin-bottom: var(--space-6);
}

.search-box {
  display: flex;
  align-items: center;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 24px;
  padding: var(--space-3) var(--space-5);
  transition: all var(--transition-base);
}

.search-box:focus-within {
  background: var(--color-bg-surface);
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
}

.search-icon {
  width: 20px;
  height: 20px;
  color: var(--color-text-muted);
  margin-right: 12px;
}

.search-input {
  flex: 1;
  border: none;
  background: none;
  font-size: 16px;
  color: var(--color-text-primary);
  outline: none;
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.clear-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.clear-btn:hover {
  background: var(--color-bg-tertiary);
  color: var(--color-text-secondary);
}

.clear-btn svg {
  width: 16px;
  height: 16px;
}

.search-btn {
  padding: 8px 20px;
  background: var(--color-blue);
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  transition: all var(--transition-base);
}

.search-btn:hover {
  background: var(--color-blue-light);
}

/* 数据统计标签 */
.stats-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-3);
}

.stat-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.stat-tag:hover {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-hover);
  transform: translateY(-1px);
}

.stat-tag.stat-tag-secondary {
  background: transparent;
  border-style: dashed;
}

.stat-tag svg {
  width: 14px;
  height: 14px;
  color: var(--color-text-muted);
}

.stat-label {
  color: var(--color-text-secondary);
}

.stat-value {
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 内容网格 */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--space-5);
}

/* 资源区块 */
.resource-section {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.section-title svg {
  width: 18px;
  height: 18px;
  color: var(--color-accent-primary);
}

.section-more {
  font-size: 13px;
  color: var(--color-accent-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.section-more:hover {
  color: var(--color-accent-hover);
}

/* 资源卡片网格 */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
  padding: var(--space-4);
}

.resource-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
}

.resource-card:hover {
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
  transform: translateY(-2px);
}

.resource-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}

.resource-rank {
  width: 22px;
  height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 600;
  background: var(--color-bg-hover);
  color: var(--color-text-muted);
}

.resource-rank.rank-1 {
  background: #f59e0b;
  color: white;
}

.resource-rank.rank-2 {
  background: #9ca3af;
  color: white;
}

.resource-rank.rank-3 {
  background: #6b7280;
  color: white;
}

.resource-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.resource-icon svg {
  width: 18px;
  height: 18px;
}

.resource-icon.type-skill {
  background: var(--color-accent-light);
  color: var(--color-accent-primary);
}

.resource-icon.type-mcp {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.resource-icon.type-hook {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.resource-card-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-2);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resource-card-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin: 0 0 var(--space-3);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
  min-height: 34px;
}

.resource-card-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: var(--color-text-muted);
  padding-top: var(--space-2);
  border-top: 1px solid var(--color-border);
}

.resource-type {
  font-weight: 500;
  padding: 2px 8px;
  background: var(--color-bg-hover);
  border-radius: 4px;
}

.resource-stat,
.resource-date {
  display: flex;
  align-items: center;
  gap: 4px;
}

.resource-stat svg {
  width: 12px;
  height: 12px;
}

/* 搜索结果 */
.search-results {
  max-width: 900px;
  margin: 0 auto;
}

.search-results .resource-grid {
  grid-template-columns: repeat(3, 1fr);
}

.search-results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
  color: var(--color-text-secondary);
}

.clear-search-btn {
  padding: var(--space-1) var(--space-3);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.clear-search-btn:hover {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: var(--color-text-muted);
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 响应式 */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .main-content {
    padding: 20px;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .resource-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: var(--space-2);
    padding: var(--space-3);
  }

  .resource-card {
    padding: var(--space-3);
  }

  .tagline-main {
    font-size: 20px;
  }

  .stats-tags {
    gap: 8px;
  }

  .stat-tag {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>
