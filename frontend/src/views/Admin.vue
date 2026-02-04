<template>
  <div class="admin-page">
    <!-- 顶部标签栏 -->
    <div class="tabs-bar">
      <button
        v-for="item in menuItems"
        :key="item.key"
        class="tab-btn"
        :class="{ active: activeTab === item.key }"
        @click="activeTab = item.key"
      >
        <component :is="item.icon" class="tab-icon" />
        <span class="tab-text">{{ item.label }}</span>
      </button>
    </div>

    <!-- 内容区域 -->
    <div class="content">
      <!-- 个人设置 -->
      <div v-if="activeTab === 'profile'">
        <!-- 操作栏 -->
        <div class="action-bar">
          <h2 class="page-title">个人设置</h2>
        </div>

        <!-- 卡片列表 -->
        <div class="card-list">
          <!-- 头像卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon avatar-icon">
                {{ (currentUser?.name || currentUser?.username || 'U').charAt(0).toUpperCase() }}
              </div>
              <div class="card-info">
                <h3 class="card-name">{{ currentUser?.name || currentUser?.username || '用户' }}</h3>
                <p class="card-desc">{{ currentUser?.email || 'user@example.com' }}</p>
              </div>
              <button class="action-btn" @click="showAvatarDialog = true" title="更换头像">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                  <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
            </div>
            <div class="card-meta">
              <span class="meta-item">个人资料</span>
            </div>
          </div>

          <!-- 个人信息卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">个人信息</h3>
                <p class="card-desc">用户名: {{ currentUser?.username || '-' }} | 姓名: {{ currentUser?.name || '-' }}</p>
              </div>
              <button class="action-btn" @click="showProfileEditDialog = true" title="编辑">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                  <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
            </div>
            <div class="card-meta">
              <span class="meta-item">{{ currentUser?.email || 'user@example.com' }}</span>
            </div>
          </div>

          <!-- 账户详情卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">账户详情</h3>
                <p class="card-desc">创建时间: {{ formatDate(currentUser?.created_at) }}</p>
              </div>
            </div>
            <div class="card-meta">
              <span class="meta-item">最后登录: {{ formatDate(currentUser?.last_login_at) }}</span>
              <span class="meta-item status success">活动</span>
            </div>
          </div>

          <!-- 安全设置卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">安全设置</h3>
                <p class="card-desc">修改密码、账户安全</p>
              </div>
              <button class="action-btn" @click="showPasswordDialog = true" title="修改密码">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                  <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </button>
            </div>
            <div class="card-meta">
              <span class="meta-item">密码保护</span>
            </div>
          </div>
        </div>
      </div>

      <!-- OAuth2 配置 -->
      <div v-if="activeTab === 'oauth'">
        <!-- 操作栏 -->
        <div class="action-bar">
          <h2 class="page-title">OAuth 配置</h2>
        </div>

        <div class="card-list">
          <!-- GitLab 卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon gitlab-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 01-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 015 1.8a.43.43 0 01.41 0l2.44 7.51h8.3l2.44-7.51a.43.43 0 01.41 0 .42.42 0 01.33.36l2.44 7.51 1.22 3.78a.84.84 0 01-.3.94z"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">GitLab OAuth</h3>
                <p class="card-desc">{{ gitlabConfig.url }}</p>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="gitlabEnabled" />
                <span class="slider"></span>
              </label>
            </div>
            <div v-if="gitlabEnabled" class="card-expanded">
              <div class="oauth-fields">
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
          </div>

          <!-- GitHub 卡片 -->
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon github-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">GitHub OAuth</h3>
                <p class="card-desc">https://github.com</p>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="githubEnabled" />
                <span class="slider"></span>
              </label>
            </div>
            <div v-if="githubEnabled" class="card-expanded">
              <div class="oauth-fields">
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
      </div>

      <!-- 仓库管理 -->
      <div v-if="activeTab === 'repos'" class="content-card content-card--full">
        <RepositoryManage />
      </div>

      <!-- MCP Server 管理 -->
      <div v-if="activeTab === 'mcp'" class="content-card content-card--full">
        <MCPServerManage />
      </div>

      <!-- 用户管理 -->
      <div v-if="activeTab === 'users'">
        <div class="action-bar">
          <h2 class="page-title">用户管理</h2>
          <button class="btn-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 4v16m8-8H4"/>
            </svg>
            添加用户
          </button>
        </div>

        <div class="card-list">
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">Admin User</h3>
                <p class="card-desc">admin@example.com</p>
              </div>
              <div class="card-actions">
                <button class="action-btn" title="编辑">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </button>
                <button class="action-btn danger" title="删除">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2M10 11v6M14 11v6M5 6h14l1 14H4L5 6z"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="card-meta">
              <span class="meta-item status success">活动</span>
              <span class="meta-item">管理员</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 角色管理 -->
      <div v-if="activeTab === 'roles'">
        <div class="action-bar">
          <h2 class="page-title">角色管理</h2>
          <button class="btn-primary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 4v16m8-8H4"/>
            </svg>
            添加角色
          </button>
        </div>

        <div class="card-list">
          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">管理员</h3>
                <p class="card-desc">拥有所有权限</p>
              </div>
              <div class="card-actions">
                <button class="action-btn" title="编辑">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="card-meta">
              <span class="meta-item">3 个用户</span>
              <span class="meta-item">全部权限</span>
            </div>
          </div>

          <div class="setting-card">
            <div class="card-header">
              <div class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </div>
              <div class="card-info">
                <h3 class="card-name">普通用户</h3>
                <p class="card-desc">基本使用权限</p>
              </div>
              <div class="card-actions">
                <button class="action-btn" title="编辑">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.12 2.12 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="card-meta">
              <span class="meta-item">12 个用户</span>
              <span class="meta-item">查看、编辑</span>
            </div>
          </div>
        </div>
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

    <!-- 个人信息编辑对话框 -->
    <ProfileEditDialog
      v-model:visible="showProfileEditDialog"
      :user="currentUser"
      @success="onProfileUpdated"
    />

    <!-- 修改密码对话框 -->
    <PasswordChangeDialog
      v-model:visible="showPasswordDialog"
      @success="onPasswordChanged"
    />

    <!-- 更换头像对话框 -->
    <AvatarEditDialog
      v-model:visible="showAvatarDialog"
      :current-avatar="currentUser?.avatar_url"
      @success="onAvatarUpdated"
    />
  </div>
</template>

<script>
import { h, ref, computed } from 'vue'
import RepositoryManage from './RepositoryManage.vue'
import MCPServerManage from './MCPServerManage.vue'
import ProfileEditDialog from '@/components/ProfileEditDialog.vue'
import PasswordChangeDialog from '@/components/PasswordChangeDialog.vue'
import AvatarEditDialog from '@/components/AvatarEditDialog.vue'
import { useAuthStore } from '@/store/auth'

// 图标组件
const UsersIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2' }),
      h('circle', { cx: '9', cy: '7', r: '4' })
    ])
  }
}

const ProfileIcon = {
  render() {
    return h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.5' }, [
      h('path', { d: 'M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2' }),
      h('circle', { cx: '12', cy: '7', r: '4' })
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
    ProfileIcon,
    UsersIcon,
    RolesIcon,
    ReposIcon,
    McpIcon,
    OAuthIcon,
    RepositoryManage,
    MCPServerManage,
    ProfileEditDialog,
    PasswordChangeDialog,
    AvatarEditDialog
  },
  setup() {
    const activeTab = ref('profile')
    const authStore = useAuthStore()
    const currentUser = computed(() => authStore.user)

    const menuItems = [
      { key: 'profile', label: '个人设置', icon: 'ProfileIcon' },
      { key: 'oauth', label: 'OAuth配置', icon: 'OAuthIcon' },
      { key: 'users', label: '用户管理', icon: 'UsersIcon' },
      { key: 'roles', label: '角色管理', icon: 'RolesIcon' },
      { key: 'repos', label: 'Skills仓库', icon: 'ReposIcon' },
      { key: 'mcp', label: 'MCP Server', icon: 'McpIcon' }
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

    // 用户设置对话框
    const showProfileEditDialog = ref(false)
    const showPasswordDialog = ref(false)
    const showAvatarDialog = ref(false)

    function formatDate(dateStr) {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    function onProfileUpdated() {
      // 用户信息已更新，auth store 会自动同步
      console.log('Profile updated')
    }

    function onPasswordChanged() {
      showPasswordDialog.value = false
      console.log('Password changed')
    }

    function onAvatarUpdated() {
      showAvatarDialog.value = false
      console.log('Avatar updated')
    }

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
      currentUser,
      gitlabEnabled,
      gitlabConfig,
      githubEnabled,
      githubConfig,
      saveGitLabConfig,
      testGitLabConfig,
      saveGitHubConfig,
      testGitHubConfig,
      showProfileEditDialog,
      showPasswordDialog,
      showAvatarDialog,
      getCurrentIcon,
      getCurrentTitle,
      getCurrentDesc,
      formatDate,
      onProfileUpdated,
      onPasswordChanged,
      onAvatarUpdated
    }
  }
}
</script>

<style scoped>
.admin-page {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* 顶部标签栏 */
.tabs-bar {
  display: flex;
  gap: 4px;
  padding: var(--space-4) var(--space-6) 0;
  border-bottom: 1px solid var(--color-border-subtle);
  flex-shrink: 0;
  overflow-x: auto;
}

.tabs-bar::-webkit-scrollbar {
  height: 4px;
}

.tabs-bar::-webkit-scrollbar-track {
  background: transparent;
}

.tabs-bar::-webkit-scrollbar-thumb {
  background: #444;
  border-radius: 2px;
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
  white-space: nowrap;
}

.tab-btn:hover {
  color: var(--color-text-secondary);
}

.tab-btn.active {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-accent-primary);
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.tab-text {
  white-space: nowrap;
}

/* 内容区域 */
.content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  background: transparent;
}

.content-card {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
}

.content-card--full {
  max-width: none;
  padding: 0;
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

.actions {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.btn-secondary {
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

.btn-secondary:hover {
  background: var(--color-bg-tertiary);
  border-color: var(--color-border-light);
  color: var(--color-text-primary);
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

/* 卡片列表 */
.card-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.setting-card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
}

.card-icon {
  width: 44px;
  height: 44px;
  background: var(--color-accent-light);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 22px;
  height: 22px;
  color: var(--color-accent-primary);
}

.card-icon.avatar-icon {
  background: linear-gradient(135deg, var(--color-blue) 0%, #8b5cf6 100%);
  font-size: 20px;
  font-weight: 600;
  color: white;
}

.card-icon.gitlab-icon svg {
  color: #FC6D26;
}

.card-icon.github-icon svg {
  color: #fff;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 4px;
}

.card-desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-actions {
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
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.action-btn.danger:hover {
  background: var(--color-error-bg);
  color: var(--color-error);
  border-color: var(--color-error);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.card-meta {
  display: flex;
  gap: var(--space-4);
  padding: 0 var(--space-5) var(--space-4);
  font-size: 12px;
}

.meta-item {
  color: var(--color-text-muted);
}

.meta-item.status {
  color: #22c55e;
}

.meta-item.status.success {
  color: #22c55e;
}

/* 展开内容 */
.card-expanded {
  border-top: 1px solid var(--color-border);
}

/* OAuth 字段 */
.oauth-fields {
  padding: var(--space-5);
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

/* 开关 */
.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
  flex-shrink: 0;
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
  .tabs-bar {
    padding: 12px 16px 0;
  }

  .tab-btn {
    padding: 8px 12px;
    font-size: 13px;
  }

  .tab-icon {
    width: 14px;
    height: 14px;
  }

  .content {
    padding: var(--space-4);
  }

  .content-card {
    padding: 0;
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
