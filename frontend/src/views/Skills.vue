<template>
  <!-- 顶部标签栏 -->
      <div class="tabs-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'skills' }"
          @click="activeTab = 'skills'"
        >
          Skills
          <span class="tab-count">{{ totalSkills }}</span>
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'repositories' }"
          @click="activeTab = 'repositories'"
        >
          Repositories
          <span class="tab-count">{{ repositories.length }}</span>
        </button>
      </div>

      <!-- Skills 内容 -->
      <div v-if="activeTab === 'skills'" class="content">
        <!-- 搜索栏 -->
        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="Search skills..."
            @input="handleSearch"
          />
          <span class="search-shortcut">⌘K</span>
        </div>

        <!-- 分类标签 -->
        <div class="category-tabs">
          <button
            class="category-tab"
            :class="{ active: !selectedCategory }"
            @click="selectedCategory = ''"
          >All</button>
          <button
            v-for="category in categories"
            :key="category"
            class="category-tab"
            :class="{ active: selectedCategory === category }"
            @click="selectedCategory = category"
          >{{ category }}</button>
        </div>

        <!-- Skills 网格 -->
        <div v-if="loading" class="loading-state">
          <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
          </svg>
          <p>Loading...</p>
        </div>

        <div v-else-if="filteredSkills.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 8v4m0 4h.01"/>
          </svg>
          <p>No skills found</p>
        </div>

        <div v-else class="skills-grid">
          <div
            v-for="skill in filteredSkills"
            :key="skill.id"
            class="skill-card"
            @click="goToSkillDetail(skill.id)"
          >
            <div class="skill-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
              </svg>
            </div>
            <h3 class="skill-name">{{ skill.name }}</h3>
            <p class="skill-desc">{{ skill.description || 'No description' }}</p>
            <div class="skill-meta">
              <span class="skill-category">{{ skill.category || 'General' }}</span>
              <span v-if="skill.view_count" class="skill-views">{{ skill.view_count }} views</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Repositories 内容 -->
      <div v-else class="content">
        <!-- 操作栏 -->
        <div class="action-bar">
          <button class="btn-primary" @click="showAddRepoDialog">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 4v16m8-8H4"/>
            </svg>
            Add Repository
          </button>
        </div>

        <!-- 仓库列表 -->
        <div v-if="repositories.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 7v10c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2h-6l-2-2H5c-1.1 0-2 .9-2 2z"/>
          </svg>
          <p>No repositories yet</p>
        </div>

        <div v-else class="repo-list">
          <div
            v-for="repo in repositories"
            :key="repo.id"
            class="repo-card"
          >
            <div class="repo-header">
              <div class="repo-info">
                <h3 class="repo-name">{{ repo.name }}</h3>
                <p class="repo-desc">{{ repo.description || 'No description' }}</p>
              </div>
              <div class="repo-actions">
                <button
                  class="action-btn"
                  :disabled="repo.syncing"
                  @click="handleSync(repo)"
                  title="Sync"
                >
                  <svg v-if="!repo.syncing" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 2v6h-6M3 12a9 9 0 0115-6.7L21 8M3 22v-6h6M21 12a9 9 0 01-15 6.7L3 16"/>
                  </svg>
                  <svg v-else class="spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
                  </svg>
                </button>
                <button
                  class="action-btn"
                  @click="editRepo(repo)"
                  title="Edit"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </button>
                <button
                  class="action-btn danger"
                  @click="deleteRepo(repo)"
                  title="Delete"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6M5 6h14l1 14H4L5 6z"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="repo-meta">
              <span class="repo-status" :class="repo.enabled ? 'success' : 'muted'">
                {{ repo.enabled ? 'Active' : 'Inactive' }}
              </span>
              <span class="repo-count">{{ repo.skill_count || 0 }} skills</span>
              <span class="repo-updated">{{ formatDate(repo.last_sync_at) }}</span>
            </div>
          </div>
        </div>
      </div>
  <!-- 仓库对话框 -->
  <RepositoryFormDialog
    v-model:visible="showRepoDialog"
    :edit-repo="editRepoData"
    @success="onRepoDialogSuccess"
  />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { resourceApi } from '@/api/resources'
import { repositoryApi } from '@/api/repositories'
import { notify } from '@/utils/notification'
import RepositoryFormDialog from '@/components/RepositoryFormDialog.vue'

const router = useRouter()

// State
const activeTab = ref('skills')
const loading = ref(false)
const skills = ref([])
const repositories = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const showRepoDialog = ref(false)
const editRepoData = ref(null)

// Computed
const categories = computed(() => {
  const cats = new Set()
  skills.value.forEach(s => {
    if (s.category) cats.add(s.category)
  })
  return Array.from(cats).sort()
})

const totalSkills = computed(() => skills.value.length)

const filteredSkills = computed(() => {
  let filtered = skills.value

  if (selectedCategory.value) {
    filtered = filtered.filter(s => s.category === selectedCategory.value)
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(s =>
      s.name.toLowerCase().includes(query) ||
      (s.description && s.description.toLowerCase().includes(query))
    )
  }

  return filtered
})

// Methods
async function loadData() {
  loading.value = true
  try {
    const [skillsRes, reposRes] = await Promise.all([
      resourceApi.getList({ type: 'skill' }),
      repositoryApi.getList()
    ])

    if (skillsRes.success) {
      skills.value = skillsRes.data || []
    }

    if (reposRes.success) {
      repositories.value = reposRes.data || []
    }
  } catch (e) {
    console.error('Failed to load data:', e)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  // Search is handled by computed property
}

function showAddRepoDialog() {
  editRepoData.value = null
  showRepoDialog.value = true
}

function editRepo(repo) {
  editRepoData.value = repo
  showRepoDialog.value = true
}

async function deleteRepo(repo) {
  if (!confirm(`Are you sure you want to delete "${repo.name}"?`)) return

  try {
    const res = await repositoryApi.delete(repo.id)
    if (res.success) {
      notify.success('Repository deleted')
      await loadData()
    } else {
      notify.error(res.message || 'Failed to delete')
    }
  } catch (e) {
    console.error('Failed to delete repository:', e)
    notify.error('Failed to delete')
  }
}

async function handleSync(repo) {
  repo.syncing = true
  try {
    const res = await repositoryApi.sync(repo.id)
    if (res.success) {
      notify.success(`Synced: ${res.data.added} added, ${res.data.updated} updated`)
      await loadData()
    } else {
      notify.error(res.message || 'Sync failed')
    }
  } catch (e) {
    console.error('Failed to sync repository:', e)
    notify.error('Sync failed')
  } finally {
    repo.syncing = false
  }
}

function onRepoDialogSuccess() {
  loadData()
}

function formatDate(dateStr) {
  if (!dateStr) return 'Never'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))

  if (hours < 1) return 'Just now'
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}d ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function goToSkillDetail(id) {
  router.push(`/resource/${id}`)
}

// Keyboard shortcuts
function handleKeydown(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    document.querySelector('.search-input')?.focus()
  }
}

onMounted(() => {
  loadData()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* ===== Main Content ===== */

/* ===== Tabs Bar ===== */
.tabs-bar {
  display: flex;
  gap: 4px;
  padding: var(--space-4) var(--space-6) 0;
  border-bottom: 1px solid var(--color-border-subtle);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--color-text-tertiary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: -1px;
}

.tab-btn:hover {
  color: var(--color-text-secondary);
}

.tab-btn.active {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-accent-primary);
}

.tab-count {
  padding: 2px 8px;
  background: var(--color-bg-elevated);
  border-radius: 10px;
  font-size: 12px;
}

.tab-btn.active .tab-count {
  background: var(--color-accent-light);
  color: var(--color-accent-primary);
}

/* ===== Content Area ===== */
.content {
  padding: 0;
  overflow-y: auto;
}

/* ===== Search Bar ===== */
.search-bar {
  display: flex;
  align-items: center;
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-6);
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

/* ===== Category Tabs ===== */
.category-tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}

.category-tab {
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.category-tab:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.category-tab.active {
  background: var(--color-accent-primary);
  border-color: var(--color-accent-primary);
  color: white;
}

/* ===== Skills Grid ===== */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.skill-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--transition-base);
}

.skill-card:hover {
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
  transform: translateY(-2px);
}

.skill-icon {
  width: 44px;
  height: 44px;
  background: var(--color-accent-light);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.skill-icon svg {
  width: 22px;
  height: 22px;
  color: var(--color-accent-primary);
}

.skill-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px;
}

.skill-desc {
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

.skill-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.skill-category {
  padding: 4px 10px;
  background: var(--color-bg-elevated);
  border-radius: 12px;
  color: var(--color-text-tertiary);
}

.skill-views {
  color: var(--color-text-muted);
}

/* ===== Action Bar ===== */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-5);
  background: var(--color-accent-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity var(--transition-fast);
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-primary svg {
  width: 18px;
  height: 18px;
}

/* ===== Repository List ===== */
.repo-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.repo-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.repo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
}

.repo-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px;
}

.repo-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

.repo-actions {
  display: flex;
  gap: var(--space-2);
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.action-btn.danger:hover {
  background: var(--color-error-bg);
  color: var(--color-error);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.repo-meta {
  display: flex;
  gap: var(--space-4);
  font-size: 12px;
}

.repo-status {
  color: var(--color-text-muted);
}

.repo-status.success {
  color: var(--color-success);
}

.repo-count,
.repo-updated {
  color: var(--color-text-muted);
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

  .skills-grid {
    grid-template-columns: 1fr;
  }

  .tabs-bar {
    padding: 12px 16px 0;
  }

  .content {
    padding: 16px;
  }
}
</style>
