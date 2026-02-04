<template>
  <div class="admin-page">
    <!-- 内部侧边栏 -->
    <aside class="inner-sidebar">
      <nav class="inner-nav">
        <button
          v-for="item in menuItems"
          :key="item.key"
          class="inner-nav-item"
          :class="{ active: activeTab === item.key }"
          @click="activeTab = item.key"
        >
          <component :is="item.icon" class="nav-icon" />
          <span class="nav-text">{{ item.label }}</span>
        </button>
      </nav>
    </aside>

    <!-- 内容区域 -->
    <div class="content-area">
      <!-- OAuth2 配置 -->
      <div v-if="activeTab === 'oauth'" class="content-card">
        <h2 class="card-title">OAuth 配置</h2>
        <div class="oauth-container">
          <!-- GitLab -->
          <div class="oauth-card">
            <div class="oauth-header">
              <div class="oauth-brand gitlab">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 01-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 015 1.8a.43.43 0 01.41 0l2.44 7.51h8.3l2.44-7.51a.43.43 0 01.41 0 .42.42 0 01.33.36l2.44 7.51 1.22 3.78a.84.84 0 01-.3.94z"/>
                </svg>
                <span>GitLab</span>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="gitlabEnabled" />
                <span class="slider"></span>
              </label>
            </div>
            <div v-if="gitlabEnabled" class="oauth-fields">
              <div class="field">
                <label>URL</label>
                <input v-model="gitlabConfig.url" placeholder="https://gitlab.com" />
              </div>
              <div class="field">
                <label>Application ID</label>
                <input v-model="gitlabConfig.clientId" placeholder="Application ID" />
              </div>
              <div class="field">
                <label>Secret</label>
                <input v-model="gitlabConfig.clientSecret" type="password" placeholder="Secret" />
              </div>
              <div class="field">
                <label>回调地址</label>
                <input v-model="gitlabConfig.redirectUri" placeholder="http://localhost:3000/auth/callback" />
              </div>
              <div class="actions">
                <button class="btn-primary" @click="saveGitLabConfig">保存</button>
                <button class="btn-ghost" @click="testGitLabConfig">测试</button>
              </div>
            </div>
          </div>

          <!-- GitHub -->
          <div class="oauth-card">
            <div class="oauth-header">
              <div class="oauth-brand github">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>GitHub</span>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="githubEnabled" />
                <span class="slider"></span>
              </label>
            </div>
            <div v-if="githubEnabled" class="oauth-fields">
              <div class="field">
                <label>Client ID</label>
                <input v-model="githubConfig.clientId" placeholder="Client ID" />
              </div>
              <div class="field">
                <label>Client Secret</label>
                <input v-model="githubConfig.clientSecret" type="password" placeholder="Client Secret" />
              </div>
              <div class="field">
                <label>回调地址</label>
                <input v-model="githubConfig.redirectUri" placeholder="http://localhost:3000/auth/callback" />
              </div>
              <div class="actions">
                <button class="btn-primary" @click="saveGitHubConfig">保存</button>
                <button class="btn-ghost" @click="testGitHubConfig">测试</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 仓库管理 -->
      <div v-if="activeTab === 'repos'" class="content-card content-card--full">
        <RepositoryManage />
      </div>

      <!-- MCP Server 管理 -->
      <div v-if="activeTab === 'mcp'" class="content-card content-card--full">
        <MCPServerManage />
      </div>

      <!-- 其他占位内容 -->
      <div v-else class="content-card">
        <div class="placeholder">
          <div class="placeholder-icon">
            <component :is="getCurrentIcon()" />
          </div>
          <h3>{{ getCurrentTitle() }}</h3>
          <p>{{ getCurrentDesc() }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { h, ref } from 'vue'
import RepositoryManage from './RepositoryManage.vue'
import MCPServerManage from './MCPServerManage.vue'

// 图标组件
const UsersIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2' }),
      h('circle', { cx: '9', cy: '7', r: '4' })
    ])
  }
}

const RolesIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M12 15a3 3 0 100-6 3 3 0 000 6z' }),
      h('path', { d: 'M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z' })
    ])
  }
}

const ReposIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M3 7V17C3 18.1046 3.89543 19 5 19H19C20.1046 19 21 18.1046 21 17V9C21 7.89543 20.1046 7 19 7H13L11 5H5C3.89543 5 3 5.89543 3 7Z' })
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

const OAuthIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z' }),
      h('path', { d: 'M12 16V12' }),
      h('path', { d: 'M12 8H12.01' })
    ])
  }
}

export default {
  components: {
    UsersIcon,
    RolesIcon,
    ReposIcon,
    McpIcon,
    OAuthIcon,
    RepositoryManage,
    MCPServerManage
  },
  setup() {
    const activeTab = ref('oauth')

    const menuItems = [
      { key: 'oauth', label: 'OAuth', icon: 'OAuthIcon' },
      { key: 'users', label: '用户', icon: 'UsersIcon' },
      { key: 'roles', label: '角色', icon: 'RolesIcon' },
      { key: 'repos', label: 'Skills仓库', icon: 'ReposIcon' },
      { key: 'mcp', label: 'MCP', icon: 'McpIcon' }
    ]

    const gitlabEnabled = ref(true)
    const gitlabConfig = ref({
      url: 'https://gitlab.com',
      clientId: '',
      clientSecret: '',
      redirectUri: 'http://localhost:3000/auth/callback'
    })

    const githubEnabled = ref(false)
    const githubConfig = ref({
      clientId: '',
      clientSecret: '',
      redirectUri: 'http://localhost:3000/auth/callback'
    })

    function saveGitLabConfig() {
      console.log('保存 GitLab 配置:', gitlabConfig.value)
    }

    function testGitLabConfig() {
      console.log('测试 GitLab 连接')
    }

    function saveGitHubConfig() {
      console.log('保存 GitHub 配置:', githubConfig.value)
    }

    function testGitHubConfig() {
      console.log('测试 GitHub 连接')
    }

    function getCurrentIcon() {
      const item = menuItems.find(i => i.key === activeTab.value)
      return item?.icon || 'UsersIcon'
    }

    function getCurrentTitle() {
      const titles = {
        users: '用户管理',
        roles: '角色管理',
        repos: '仓库管理',
        mcp: 'MCP Server'
      }
      return titles[activeTab.value] || '开发中'
    }

    function getCurrentDesc() {
      const descs = {
        users: '管理系统用户和权限',
        roles: '定义角色和权限策略',
        repos: '管理 GitLab 仓库',
        mcp: '配置 MCP 服务器'
      }
      return descs[activeTab.value] || '功能开发中'
    }

    return {
      activeTab,
      menuItems,
      gitlabEnabled,
      gitlabConfig,
      githubEnabled,
      githubConfig,
      saveGitLabConfig,
      testGitLabConfig,
      saveGitHubConfig,
      testGitHubConfig,
      getCurrentIcon,
      getCurrentTitle,
      getCurrentDesc
    }
  }
}
</script>

<style scoped>
.admin-page {
  display: flex;
  height: 100%;
  background: var(--color-bg-primary);
}

/* 内部侧边栏 */
.inner-sidebar {
  width: 180px;
  background: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  padding: 20px 12px;
  flex-shrink: 0;
}

.inner-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.inner-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  font-size: 13px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.nav-icon {
  width: 16px;
  height: 16px;
  opacity: 0.7;
}

.inner-nav-item:hover {
  color: var(--color-text-primary);
  background: var(--color-bg-hover);
}

.inner-nav-item.active {
  color: var(--color-text-primary);
  background: var(--color-blue);
}

.inner-nav-item.active .nav-icon {
  opacity: 1;
}

/* 内容区域 */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
}

.content-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  min-height: 400px;
}

.content-card--full {
  background: transparent;
  border: none;
  padding: 0;
  min-height: auto;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-6) 0;
}

/* OAuth 容器 */
.oauth-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.oauth-card {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.oauth-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  background: var(--color-bg-surface);
  border-bottom: 1px solid var(--color-border);
}

.oauth-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.oauth-brand svg {
  width: 20px;
  height: 20px;
}

.oauth-brand.gitlab svg {
  color: #FC6D26;
}

.oauth-brand.github svg {
  color: #fff;
}

/* 开关 */
.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-border);
  transition: var(--transition-base);
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background: white;
  transition: var(--transition-base);
  border-radius: 50%;
}

.switch input:checked + .slider {
  background: var(--color-blue);
}

.switch input:checked + .slider:before {
  transform: translateX(18px);
}

/* OAuth 字段 */
.oauth-fields {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.field input {
  padding: 10px 12px;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 13px;
  color: var(--color-text-primary);
  outline: none;
  transition: border-color var(--transition-fast);
}

.field input:focus {
  border-color: var(--color-blue);
}

.field input::placeholder {
  color: var(--color-text-muted);
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.btn-primary {
  padding: 9px 16px;
  background: var(--color-blue);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity var(--transition-fast);
}

.btn-primary:hover {
  opacity: 0.85;
}

.btn-ghost {
  padding: 9px 16px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-ghost:hover {
  background: var(--color-bg-tertiary);
  border-color: var(--color-border-light);
  color: var(--color-text-primary);
}

/* 占位符 */
.placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  min-height: 400px;
  color: var(--color-text-muted);
}

.placeholder-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.placeholder-icon svg {
  width: 100%;
  height: 100%;
}

.placeholder h3 {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}

.placeholder p {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

/* 响应式 */
@media (max-width: 768px) {
  .inner-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }

  .inner-nav {
    flex-direction: row;
    overflow-x: auto;
  }

  .inner-nav-item {
    flex-shrink: 0;
    white-space: nowrap;
  }

  .actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-ghost {
    width: 100%;
  }
}
</style>
