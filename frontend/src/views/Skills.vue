<template>
  <!-- Skills 内容 -->
  <div class="content">
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
      />
      <span class="search-shortcut">⌘K</span>
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { resourceApi } from '@/api/resources'

const router = useRouter()

// State
const loading = ref(false)
const skills = ref([])
const searchQuery = ref('')

// Computed
const filteredSkills = computed(() => {
  let filtered = skills.value

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
    const skillsRes = await resourceApi.getList({ type: 'skill' })

    if (skillsRes.success) {
      skills.value = skillsRes.data || []
    }
  } catch (e) {
    console.error('Failed to load data:', e)
  } finally {
    loading.value = false
  }
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
.content {
  padding: var(--space-6);
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
  .skills-grid {
    grid-template-columns: 1fr;
  }

  .content {
    padding: var(--space-4);
  }
}
</style>
