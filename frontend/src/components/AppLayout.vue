<template>
  <div class="app-layout">
    <!-- 左侧导航栏 -->
    <aside class="sidebar">
      <!-- 品牌 Logo -->
      <div class="sidebar-brand">
        <svg class="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z"/>
        </svg>
        <span class="brand-text">AI Native 研发平台</span>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <component :is="item.icon" class="nav-icon" />
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="user-section" v-if="currentUser">
          <div class="user-avatar">
            {{ (currentUser.name || currentUser.username || 'U').charAt(0).toUpperCase() }}
          </div>
          <div class="user-info">
            <div class="user-name">{{ currentUser.name || currentUser.username }}</div>
            <div class="user-email">{{ currentUser.email || 'developer@company.com' }}</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <div class="content-wrapper">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const currentUser = ref(null)

// 获取当前用户
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

currentUser.value = getCurrentUser()

// 导航菜单项
const navItems = [
  {
    path: '/dashboard',
    label: 'Dashboard',
    icon: 'DashboardIcon'
  },
  {
    path: '/skills',
    label: 'Skills',
    icon: 'SkillsIcon'
  },
  {
    path: '/mcp',
    label: 'MCP',
    icon: 'McpIcon'
  },
  {
    path: '/hooks',
    label: 'Hooks',
    icon: 'HooksIcon'
  },
  {
    path: '/admin',
    label: '系统设置',
    icon: 'SettingsIcon'
  }
]

// 判断当前路径是否活跃
const isActive = (path) => {
  if (path === '/dashboard') {
    return route.path === '/dashboard'
  }
  return route.path.startsWith(path)
}
</script>

<script>
import { h } from 'vue'

const DashboardIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('rect', { x: '3', y: '3', width: '7', height: '7' }),
      h('rect', { x: '14', y: '3', width: '7', height: '7' }),
      h('rect', { x: '3', y: '14', width: '7', height: '7' }),
      h('rect', { x: '14', y: '14', width: '7', height: '7' })
    ])
  }
}

const SkillsIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M12 2L15 8L21 9L17 14L18 20L12 17L6 20L7 14L3 9L9 8L12 2Z' })
    ])
  }
}

const McpIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('rect', { x: '4', y: '4', width: '16', height: '16', rx: '2' }),
      h('circle', { cx: '12', cy: '12', r: '4' })
    ])
  }
}

const HooksIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M9 18C5.68629 18 3 15.3137 3 12C3 8.68629 5.68629 6 9 6' }),
      h('path', { d: 'M15 6C18.3137 6 21 8.68629 21 12C21 15.3137 18.3137 18 15 18' }),
      h('circle', { cx: '15', cy: '12', r: '3' }),
      h('circle', { cx: '9', cy: '12', r: '3' })
    ])
  }
}

const SettingsIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 0 .7 1.53l1.06 1.06a2 2 0 0 1 0 2.83 0 2 2 0 0 1-2.83 0l-1.06-1.06a2 2 0 0 0-.7-1.53V4a2 2 0 0 0-2-2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 0 .7 1.53l1.06 1.06a2 2 0 0 1 0 2.83 0 2 2 0 0 1-2.83 0l-1.06-1.06a2 2 0 0 0-.7-1.53V4a2 2 0 0 0-2-2zM11 15.66V8.34a2 2 0 0 0-2 2v.18a2 2 0 0 0 .7 1.53l1.06 1.06a2 2 0 0 1 0 2.83 0 2 2 0 0 1-2.83 0l-1.06-1.06a2 2 0 0 0-.7-1.53V8.34a2 2 0 0 0-2-2' })
    ])
  }
}

export default {
  components: {
    DashboardIcon,
    SkillsIcon,
    McpIcon,
    HooksIcon,
    SettingsIcon
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background: var(--color-bg-primary);
}

/* ========== 侧边栏 ========== */
.sidebar {
  width: var(--sidebar-width);
  background: var(--color-bg-sidebar);
  border-right: 1px solid var(--color-border-subtle);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

/* 品牌 Logo */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-5);
  border-bottom: 1px solid var(--color-border-subtle);
  height: 52px;
}

.brand-icon {
  width: 24px;
  height: 24px;
  color: var(--color-accent-primary);
}

.brand-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.5px;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: var(--space-3);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
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
  background: var(--color-accent-primary);
}

.nav-item .nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-item .nav-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 底部用户区域 */
.sidebar-footer {
  padding: var(--space-3);
  border-top: 1px solid var(--color-border-subtle);
}

.user-section {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-accent-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 11px;
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  overflow-y: auto;
  background: var(--color-bg-primary);
}

.content-wrapper {
  max-width: var(--content-max-width);
  margin: 0 auto;
  min-height: 100%;
  padding: var(--space-6);
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }

  .content-wrapper {
    padding: var(--space-4);
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: var(--space-3);
  }
}
</style>
