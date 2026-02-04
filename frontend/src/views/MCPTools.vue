<template>
  <!-- 顶部标签栏 -->
      <div class="tabs-bar">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'tools' }"
          @click="activeTab = 'tools'"
        >
          Tools
          <span class="tab-count">{{ totalTools }}</span>
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'servers' }"
          @click="activeTab = 'servers'"
        >
          Servers
          <span class="tab-count">{{ totalServers }}</span>
        </button>
      </div>

      <!-- Tools 内容 -->
      <div v-if="activeTab === 'tools'" class="content">
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
            placeholder="Search tools..."
          />
          <span class="search-shortcut">⌘K</span>
        </div>

        <!-- Server 筛选 -->
        <div class="filter-tabs">
          <button
            class="filter-tab"
            :class="{ active: !selectedServer }"
            @click="selectedServer = ''"
          >All Servers</button>
          <button
            v-for="server in serverList"
            :key="server.id"
            class="filter-tab"
            :class="{ active: selectedServer === server.id }"
            @click="selectedServer = server.id"
          >{{ server.name }} ({{ server.tool_count }})</button>
        </div>

        <!-- Tools 网格 -->
        <div v-if="loading" class="loading-state">
          <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10" stroke-dasharray="60" stroke-dashoffset="20"/>
          </svg>
          <p>Loading...</p>
        </div>

        <div v-else-if="filteredTools.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="4" width="16" height="16" rx="2"/>
            <circle cx="12" cy="12" r="4"/>
          </svg>
          <p>No tools found</p>
        </div>

        <div v-else class="tools-grid">
          <div
            v-for="tool in filteredTools"
            :key="tool.id"
            class="tool-card"
            @click="showToolDetail(tool)"
          >
            <div class="tool-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <circle cx="12" cy="12" r="4"/>
              </svg>
            </div>
            <h3 class="tool-name">{{ tool.name }}</h3>
            <p class="tool-desc">{{ tool.description || 'No description' }}</p>
            <div class="tool-server">{{ getServerName(tool.server_id) }}</div>
            <div class="tool-meta">
              <span v-if="tool.call_count" class="tool-calls">{{ tool.call_count }} calls</span>
              <span v-if="tool.input_schema" class="tool-has-params">Has params</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Servers 内容 -->
      <div v-else class="content">
        <!-- 操作栏 -->
        <div class="action-bar">
          <!-- 归属筛选 -->
          <div class="ownership-filter">
            <button
              class="filter-btn"
              :class="{ active: serversOwnershipFilter === 'all' }"
              @click="serversOwnershipFilter = 'all'"
            >All</button>
            <button
              class="filter-btn"
              :class="{ active: serversOwnershipFilter === 'mine' }"
              @click="serversOwnershipFilter = 'mine'"
            >Mine</button>
          </div>
          <button class="btn-primary" @click="showAddDialog">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 4v16m8-8H4"/>
            </svg>
            Add Server
          </button>
        </div>

        <!-- 服务器列表 -->
        <div v-if="filteredServers.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="4" width="16" height="16" rx="2"/>
            <circle cx="12" cy="12" r="4"/>
          </svg>
          <p>No servers found</p>
        </div>

        <div v-else class="servers-list">
          <div
            v-for="server in filteredServers"
            :key="server.id"
            class="server-card"
            @click="showServerDetail(server)"
          >
            <div class="server-header">
              <div class="server-info">
                <div class="server-type-badge" :class="`type--${server.transport_type}`">
                  {{ server.transport_type.toUpperCase() }}
                </div>
                <h3 class="server-name">{{ server.name }}</h3>
                <p class="server-desc">{{ server.description || 'No description' }}</p>
              </div>
              <div class="server-status" :class="server.enabled ? 'active' : 'inactive'">
                {{ server.enabled ? 'Active' : 'Inactive' }}
              </div>
            </div>
            <div class="server-meta">
              <span class="meta-item">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l1.6-1.6a1 1 0 00-1.4 0l-1.6-1.6zM12.3 8.7a1 1 0 000-1.4l-1.6-1.6a1 1 0 00-1.4 0l-1.6 1.6a1 1 0 001.4 0l1.6 1.6z"/>
                </svg>
                {{ server.total_tools || 0 }} Tools
              </span>
              <span v-if="server.total_resources" class="meta-item">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 0a8 8 0 100 16A8 8 0 008 0z"/>
                  <path d="M8 4a4 4 0 100 8 4 4 0 000-8z"/>
                </svg>
                {{ server.total_resources }} Resources
              </span>
              <span v-if="server.contributor" class="meta-item">
                <svg viewBox="0 0 16 16" fill="currentColor">
                  <path d="M8 8a3 3 0 100-6 3 3 0 000 6z"/>
                  <path d="M14 7.2a2 2 0 00-2-2c-.526 0-1 .135-1.4.355a4.969 4.969 0 00-6 0c-.4.22-.22-.874-.355-1.4-.355a2 2 0 00-2 2c0 .608.272 1.152.7 1.572a5 5 0 0010 0c.428.42.7.964.7 1.572z"/>
                </svg>
                {{ server.contributor.name || server.contributor.username || 'Unknown' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    <!-- Tool 详情弹窗 -->
    <div v-if="selectedTool" class="modal" :class="{ show: showModal }" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedTool.name }}</h3>
          <button class="modal-close" @click="closeModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <span class="detail-label">Server</span>
            <span class="detail-value">{{ getServerName(selectedTool.server_id) }}</span>
          </div>
          <div class="detail-section">
            <span class="detail-label">Description</span>
            <p class="detail-desc">{{ selectedTool.description || 'No description' }}</p>
          </div>
          <div v-if="selectedTool.input_schema" class="detail-section">
            <span class="detail-label">Parameters</span>
            <pre class="detail-code">{{ JSON.stringify(selectedTool.input_schema, null, 2) }}</pre>
          </div>
          <div class="detail-section">
            <span class="detail-label">Stats</span>
            <span class="detail-value">{{ selectedTool.call_count || 0 }} calls</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Close</button>
          <button class="btn-primary" @click="callTool" :disabled="calling">
            {{ calling ? 'Calling...' : 'Test Call' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Server 详情弹窗 -->
    <div v-if="selectedServer" class="modal" :class="{ show: showServerModal }" @click.self="closeServerModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedServer.name }}</h3>
          <button class="modal-close" @click="closeServerModal">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <span class="detail-label">Type</span>
            <span class="detail-value">{{ selectedServer.transport_type.toUpperCase() }}</span>
          </div>
          <div class="detail-section">
            <span class="detail-label">Status</span>
            <span class="detail-value" :class="selectedServer.enabled ? 'status-active' : 'status-inactive'">
              {{ selectedServer.enabled ? 'Active' : 'Inactive' }}
            </span>
          </div>
          <div v-if="selectedServer.description" class="detail-section">
            <span class="detail-label">Description</span>
            <p class="detail-desc">{{ selectedServer.description }}</p>
          </div>
          <div class="detail-section">
            <span class="detail-label">Tools</span>
            <span class="detail-value">{{ selectedServer.total_tools || 0 }}</span>
          </div>
          <div v-if="selectedServer.contributor" class="detail-section">
            <span class="detail-label">Contributor</span>
            <span class="detail-value">{{ selectedServer.contributor.name || selectedServer.contributor.username }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeServerModal">Close</button>
          <router-link v-if="canEditServer(selectedServer)" to="/admin" class="btn-primary">
            Manage Server
          </router-link>
        </div>
      </div>
    </div>

  <!-- MCP Server 表单对话框 -->
  <MCPServerFormDialog
    v-model:visible="showServerDialog"
    :edit-server="editServerData"
    @success="onServerDialogSuccess"
  />
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { mcpApi } from '@/api/mcp'
import { notify } from '@/utils/notification'
import MCPServerFormDialog from '@/components/MCPServerFormDialog.vue'
import { useAuthStore } from '@/store/auth'

// State
const authStore = useAuthStore()
const currentUser = computed(() => authStore.user)
const activeTab = ref('tools')
const loading = ref(true)
const toolsGrouped = ref({})
const allTools = ref([])
const serversList = ref([])
const selectedTool = ref(null)
const showModal = ref(false)
const calling = ref(false)
const searchQuery = ref('')
const selectedServer = ref('')
const serversOwnershipFilter = ref('all')
const selectedServerData = ref(null)
const showServerModal = ref(false)
const showServerDialog = ref(false)
const editServerData = ref(null)

// Computed
const totalServers = computed(() => serversList.value.length)
const totalTools = computed(() => allTools.value.length)

const serverList = computed(() => {
  return serversList.value.map(s => ({
    id: s.id,
    name: s.name,
    tool_count: s.total_tools || 0
  }))
})

const filteredTools = computed(() => {
  let tools = allTools.value

  if (selectedServer.value) {
    tools = tools.filter(t => t.server_id == selectedServer.value)
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    tools = tools.filter(t =>
      t.name.toLowerCase().includes(query) ||
      (t.description && t.description.toLowerCase().includes(query))
    )
  }

  return tools
})

const filteredServers = computed(() => {
  let servers = serversList.value

  if (serversOwnershipFilter.value === 'mine' && currentUser.value) {
    servers = servers.filter(s => s.contributor && s.contributor.id === currentUser.value.id)
  }

  return servers
})

// Methods
function getServerName(serverId) {
  const server = serversList.value.find(s => s.id === serverId)
  return server?.name || toolsGrouped.value[serverId]?.server_name || `Server ${serverId}`
}

function canEditServer(server) {
  if (!server || !currentUser.value) return false
  return server.contributor && server.contributor.id === currentUser.value.id
}

async function loadData() {
  loading.value = true
  try {
    const [serversRes, toolsRes] = await Promise.all([
      mcpApi.getServers(),
      mcpApi.getToolsGrouped()
    ])

    if (serversRes.success) {
      serversList.value = serversRes.data
    }

    if (toolsRes.success) {
      toolsGrouped.value = toolsRes.data
      allTools.value = Object.entries(toolsRes.data).flatMap(([serverId, data]) =>
        data.tools.map(tool => ({
          ...tool,
          server_id: parseInt(serverId)
        }))
      )
    }
  } catch (e) {
    console.error('Failed to load MCP data:', e)
  } finally {
    loading.value = false
  }
}

function showToolDetail(tool) {
  selectedTool.value = tool
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  setTimeout(() => {
    selectedTool.value = null
  }, 200)
}

function showServerDetail(server) {
  selectedServerData.value = server
  showServerModal.value = true
}

function closeServerModal() {
  showServerModal.value = false
  setTimeout(() => {
    selectedServerData.value = null
  }, 200)
}

async function callTool() {
  notify.info('Tool call feature coming soon')
}

function showAddDialog() {
  editServerData.value = null
  showServerDialog.value = true
}

function onServerDialogSuccess() {
  loadData()
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
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
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

/* ===== Filter Tabs ===== */
.filter-tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}

.filter-tab {
  padding: var(--space-2) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-tab:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.filter-tab.active {
  background: var(--color-accent-primary);
  border-color: var(--color-accent-primary);
  color: white;
}

/* ===== Tools Grid ===== */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
}

.tool-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--transition-base);
}

.tool-card:hover {
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
  transform: translateY(-2px);
}

.tool-icon {
  width: 44px;
  height: 44px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-4);
}

.tool-icon svg {
  width: 22px;
  height: 22px;
  color: var(--color-success);
}

.tool-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px;
}

.tool-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0 0 12px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 38px;
}

.tool-server {
  padding: 6px 10px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-bottom: var(--space-3);
}

.tool-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: 12px;
}

.tool-calls {
  color: var(--color-text-muted);
}

.tool-has-params {
  padding: 4px 10px;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 12px;
  color: var(--color-success);
}

/* ===== Action Bar ===== */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.ownership-filter {
  display: flex;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.filter-btn {
  padding: var(--space-2) var(--space-4);
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.filter-btn:hover {
  color: var(--color-text-primary);
}

.filter-btn.active {
  background: var(--color-accent-primary);
  color: white;
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

.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-secondary:hover {
  background: var(--color-bg-tertiary);
  color: var(--color-text-primary);
}

/* ===== Servers List ===== */
.servers-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.server-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  cursor: pointer;
  transition: all var(--transition-base);
}

.server-card:hover {
  border-color: var(--color-accent-primary);
  box-shadow: var(--shadow-accent);
}

.server-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-3);
}

.server-type-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  margin-bottom: var(--space-2);
}

.type--stdio {
  background: var(--color-accent-light);
  color: var(--color-accent-primary);
}

.type--http {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.server-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 6px;
}

.server-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

.server-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.server-status.active {
  background: rgba(16, 185, 129, 0.15);
  color: var(--color-success);
}

.server-status.inactive {
  background: var(--color-bg-elevated);
  color: var(--color-text-muted);
}

.server-meta {
  display: flex;
  gap: var(--space-4);
  font-size: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--color-text-muted);
}

.meta-item svg {
  width: 14px;
  height: 14px;
}

/* ===== Modal ===== */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all var(--transition-base);
}

.modal.show {
  opacity: 1;
  visibility: visible;
}

.modal-content {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.modal-close:hover {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
}

.modal-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: var(--space-5);
  overflow-y: auto;
  flex: 1;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  color: var(--color-text-primary);
}

.detail-value.status-active {
  color: var(--color-success);
}

.detail-value.status-inactive {
  color: var(--color-text-muted);
}

.detail-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

.detail-code {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  font-size: 12px;
  color: var(--color-text-secondary);
  overflow-x: auto;
  font-family: 'Courier New', monospace;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border);
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

  .tools-grid {
    grid-template-columns: 1fr;
  }

  .tabs-bar {
    padding: 12px 16px 0;
  }

  .content {
    padding: 16px;
  }

  .action-bar {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .ownership-filter {
    width: 100%;
  }

  .filter-btn {
    flex: 1;
  }
}
</style>
