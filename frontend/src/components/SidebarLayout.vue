<template>
  <div class="sidebar-layout">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ 'sidebar--collapsed': isCollapsed }">
      <!-- 顶部 Logo 区 -->
      <div class="sidebar-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
          <span class="logo-text" v-show="!isCollapsed">AI Native 研发平台</span>
        </div>
        <button class="collapse-btn" @click="toggleCollapse" :title="isCollapsed ? '展开' : '收起'">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M15 18l-6-6 6-6" v-if="!isCollapsed"/>
            <path d="M9 18l6-6-6-6" v-else/>
          </svg>
        </button>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <div
          v-for="item in navItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
          :title="isCollapsed ? item.label : ''"
          @click="navigateTo(item.path)"
        >
          <!-- 首页 -->
          <svg v-if="item.path === '/dashboard'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="7" height="7" rx="1"></rect>
            <rect x="14" y="3" width="7" height="7" rx="1"></rect>
            <rect x="14" y="14" width="7" height="7" rx="1"></rect>
            <rect x="3" y="14" width="7" height="7" rx="1"></rect>
          </svg>
          <!-- Skills -->
          <svg v-else-if="item.path === '/skills'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"></path>
          </svg>
          <!-- MCP -->
          <svg v-else-if="item.path === '/mcp'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="4" y="4" width="16" height="16" rx="2"></rect>
            <circle cx="12" cy="12" r="4"></circle>
            <path d="M12 2V4"></path>
            <path d="M12 20V22"></path>
            <path d="M2 12H4"></path>
            <path d="M20 12H22"></path>
          </svg>
          <!-- Hooks -->
          <svg v-else-if="item.path === '/hooks'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M9 18C5.68629 18 3 15.3137 3 12C3 8.68629 5.68629 6 9 6"></path>
            <path d="M15 6C18.3137 6 21 8.68629 21 12C21 15.3137 18.3137 18 15 18"></path>
            <circle cx="15" cy="12" r="3"></circle>
            <circle cx="9" cy="12" r="3"></circle>
          </svg>
          <span class="nav-label" v-show="!isCollapsed">{{ item.label }}</span>
          <span class="nav-badge" v-if="item.badge && !isCollapsed">{{ item.badge }}</span>
        </div>

        <!-- 分隔线 -->
        <div class="nav-divider" v-show="!isCollapsed"></div>

        <!-- 管理中心 -->
        <div
          class="nav-item nav-item--admin"
          :class="{ active: isActive('/admin') }"
          title="管理中心"
          @click="navigateTo('/admin')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 15a3 3 0 100-6 3 3 0 000 6z"/>
            <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
          </svg>
          <span class="nav-label" v-show="!isCollapsed">管理中心</span>
        </div>
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="user-section" v-if="isAuthenticated">
          <img
            :src="authStore.user?.avatar_url || defaultAvatar"
            class="user-avatar"
            :alt="authStore.user?.name || 'User'"
          />
          <div class="user-info" v-show="!isCollapsed">
            <div class="user-name">{{ authStore.user?.name || authStore.user?.gitlab_username || 'User' }}</div>
            <div class="user-email">{{ authStore.user?.email || authStore.user?.gitlab_email || '' }}</div>
          </div>
          <button class="logout-btn" @click="handleLogout" title="退出登录">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9"/>
              <path d="M16 17L21 12L16 7"/>
              <path d="M21 12H9"/>
            </svg>
          </button>
        </div>
        <div v-else class="login-section" @click="navigateTo('/login')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20 21V19C20 17.9391 19.5304 16.9217 18.8284 16.1716C18.0783 15.24 3 8.68629 3 12C3 8.68629 5.68629 6 9 6"/>
            <path d="M12 15a3 3 0 100-6 3 3 0 000 6z"/>
          </svg>
          <span v-show="!isCollapsed">登录</span>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <component :is="Component" />
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isCollapsed = ref(false)
const defaultAvatar = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23666"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>'

const isAuthenticated = computed(() => authStore.isAuthenticated)

const navItems = [
  { path: '/dashboard', label: '首页' },
  { path: '/skills', label: 'Skills' },
  { path: '/mcp', label: 'MCP' },
  { path: '/hooks', label: 'Hooks' }
]

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

async function navigateTo(path) {
  try {
    await router.push(path)
  } catch (e) {
    // 忽略导航到当前路由的错误
    if (!e.message.includes('redundant')) {
      console.error('导航错误:', e)
    }
  }
}

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* ==================== 布局容器 ==================== */
.sidebar-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background: #1E1E1E;
}

/* ==================== 侧边栏 ==================== */
.sidebar {
  width: 260px;
  min-width: 260px;
  background: #252525;
  border-right: 1px solid #333333;
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease;
  flex-shrink: 0;
}

.sidebar--collapsed {
  width: 64px;
  min-width: 64px;
}

/* 顶部 Logo 区 */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  height: 60px;
  border-bottom: 1px solid #333333;
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.logo svg {
  width: 24px;
  height: 24px;
  color: #3b82f6;
  flex-shrink: 0;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #888;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.collapse-btn:hover {
  background: #333333;
  color: #ffffff;
}

.collapse-btn svg {
  width: 18px;
  height: 18px;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 6px;
  color: #B0B0B0;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.15s;
  white-space: nowrap;
  position: relative;
  cursor: pointer;
  user-select: none;
  pointer-events: auto;
}

.nav-item:hover {
  color: #ffffff;
  background: #3A3A3A;
}

.nav-item.active {
  color: #ffffff;
  background: #3b82f6;
}

.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-badge {
  background: #ef4444;
  color: #ffffff;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: 500;
}

.nav-divider {
  height: 1px;
  background: #333333;
  margin: 8px 0;
}

/* 底部用户区 */
.sidebar-footer {
  padding: 12px;
  border-top: 1px solid #333333;
  flex-shrink: 0;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.user-section:hover {
  background: #3A3A3A;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 11px;
  color: #888;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: #888;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}

.logout-btn:hover {
  background: #ef4444;
  color: #ffffff;
}

.logout-btn svg {
  width: 16px;
  height: 16px;
}

.login-section {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  color: #B0B0B0;
  font-size: 14px;
  transition: all 0.15s;
  cursor: pointer;
  user-select: none;
}

.login-section:hover {
  color: #ffffff;
  background: #3A3A3A;
}

.login-section svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

/* ==================== 主内容区 ==================== */
.main-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background: #1E1E1E;
}

.content-wrapper {
  min-height: 100%;
  padding: 24px;
}

/* ==================== 响应式 ==================== */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
    transform: translateX(-100%);
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .content-wrapper {
    padding: 16px;
  }
}
</style>
