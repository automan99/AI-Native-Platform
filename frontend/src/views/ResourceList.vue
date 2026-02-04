<template>
  <!-- 页面标题 -->
      <div class="page-title-bar">
        <h1>{{ typeConfig.title }} Resources</h1>
        <span class="total-count">{{ total }} total</span>
      </div>

      <!-- 搜索和筛选栏 -->
      <div class="filter-bar">
        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            v-model="searchKeyword"
            type="text"
            class="search-input"
            :placeholder="`Search ${typeConfig.title.toLowerCase()}...`"
            @keyup.enter="handleSearch"
          />
          <span class="search-shortcut">⌘K</span>
        </div>
      </div>

      <!-- 资源网格 -->
      <div class="content">
        <div v-if="loading" class="loading-state">
          <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
          </svg>
          <p>Loading...</p>
        </div>

        <div v-else-if="resources.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 8v4m0 4h.01"/>
          </svg>
          <p>No {{ typeConfig.title.toLowerCase() }} found</p>
        </div>

        <div v-else class="resource-grid">
          <div
            v-for="item in resources"
            :key="item.id"
            class="resource-card"
            @click="goToDetail(item.id)"
          >
            <div class="resource-icon" :class="`type-${resourceType}`">
              <component :is="getTypeIcon(item.type || resourceType)" />
            </div>
            <h3 class="resource-name">{{ item.name }}</h3>
            <p class="resource-desc">{{ item.description || 'No description' }}</p>
            <div class="resource-meta">
              <span v-if="item.author" class="resource-author">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                {{ item.author }}
              </span>
              <div class="resource-stats">
                <span v-if="item.view_count" class="stat-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M1 12S5 4 12 4S23 12 23 12S19 20 12 20"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  {{ formatNumber(item.view_count) }}
                </span>
                <span v-if="item.install_count" class="stat-item">
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

        <!-- 分页 -->
        <div v-if="total > 0 && totalPages > 1" class="pagination">
          <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M15 18L9 12L15 6"/>
            </svg>
          </button>
          <div class="page-numbers">
            <button
              v-for="page in displayPages"
              :key="page"
              class="page-num"
              :class="{ active: page === currentPage }"
              @click="goToPage(page)"
            >{{ page }}</button>
          </div>
          <button
            class="page-btn"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 18L15 12L9 6"/>
            </svg>
          </button>
        </div>
      </div>
  <!-- 页面标题 ends here -->
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { resourceApi } from '@/api/resources'

const props = defineProps({
  resourceType: {
    type: String,
    default: ''
  }
})

const router = useRouter()

// State
const resources = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const loading = ref(false)

// Type configs
const typeConfigs = {
  skill: {
    title: 'Skill',
    color: '#3b82f6',
    icon: 'SkillIcon'
  },
  mcp: {
    title: 'MCP',
    color: '#10b981',
    icon: 'McpIcon'
  },
  hook: {
    title: 'Hook',
    color: '#a855f7',
    icon: 'HookIcon'
  }
}

const typeConfig = computed(() => {
  return typeConfigs[props.resourceType] || typeConfigs.skill
})

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})

const displayPages = computed(() => {
  const pages = []
  const maxShow = 5
  let start = Math.max(1, currentPage.value - Math.floor(maxShow / 2))
  let end = Math.min(totalPages.value, start + maxShow - 1)

  if (end - start < maxShow - 1) {
    start = Math.max(1, end - maxShow + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})

// Methods
async function loadResources() {
  loading.value = true
  try {
    const res = await resourceApi.getList({
      type: props.resourceType,
      keyword: searchKeyword.value,
      page: currentPage.value,
      page_size: pageSize.value
    })

    if (res.success) {
      resources.value = res.data || []
      total.value = res.total || 0
    }
  } catch (e) {
    console.error('Failed to load resources:', e)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  loadResources()
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  loadResources()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function formatNumber(num) {
  if (!num) return '0'
  return num.toLocaleString()
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

// Keyboard shortcuts
function handleKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    document.querySelector('.search-input')?.focus()
  }
}

onMounted(() => {
  loadResources()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
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
/* ===== Main Content ===== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ===== Page Title Bar ===== */
.page-title-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border-subtle);
}

.page-title-bar h1 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.total-count {
  font-size: 14px;
  color: var(--color-text-tertiary);
}

/* ===== Filter Bar ===== */
.filter-bar {
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border-subtle);
}

.search-bar {
  display: flex;
  align-items: center;
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}

.search-icon {
  width: 18px;
  height: 18px;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  border: none;
  background: none;
  padding: 0 12px;
  font-size: 14px;
  color: var(--color-text-primary);
}

.search-input::placeholder {
  color: var(--color-text-muted);
}

.search-input:focus {
  outline: none;
}

.search-shortcut {
  padding: 4px 8px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-sm);
  font-size: 11px;
  color: var(--color-text-muted);
}

/* ===== Content Area ===== */
.content {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
}

/* ===== Resource Grid ===== */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.resource-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--transition-base);
}

.resource-card:hover {
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
  transform: translateY(-2px);
}

.resource-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.resource-icon svg {
  width: 22px;
  height: 22px;
}

.resource-icon.type-skill {
  background: var(--color-accent-light);
}

.resource-icon.type-skill svg {
  color: var(--color-accent-primary);
}

.resource-icon.type-mcp {
  background: rgba(16, 185, 129, 0.15);
}

.resource-icon.type-mcp svg {
  color: var(--color-success);
}

.resource-icon.type-hook {
  background: rgba(168, 85, 247, 0.15);
}

.resource-icon.type-hook svg {
  color: #a855f7;
}

.resource-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px;
}

.resource-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0 0 16px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 38px;
}

.resource-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.resource-author {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-text-muted);
}

.resource-author svg {
  width: 14px;
  height: 14px;
}

.resource-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--color-text-muted);
}

.stat-item svg {
  width: 13px;
  height: 13px;
}

/* ===== Pagination ===== */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  margin-top: var(--space-6);
}

.page-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.page-btn:hover:not(:disabled) {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-btn svg {
  width: 14px;
  height: 14px;
}

.page-numbers {
  display: flex;
  gap: 2px;
}

.page-num {
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.page-num:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.page-num.active {
  background: var(--color-accent-primary);
  border-color: var(--color-accent-primary);
  color: white;
}

/* ===== Loading & Empty States ===== */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--color-text-muted);
}

.spinner {
  width: 40px;
  height: 40px;
  color: var(--color-accent-primary);
  animation: spin 1s linear infinite;
  margin-bottom: var(--space-4);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-state svg,
.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.loading-state p,
.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .resource-grid {
    grid-template-columns: 1fr;
  }

  .page-title-bar {
    padding: 16px;
  }

  .filter-bar {
    padding: 16px;
  }

  .content {
    padding: 16px;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .page-btn,
  .page-num {
    flex-shrink: 0;
  }
}
</style>
