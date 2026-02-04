<template>
  <!-- 登录页面单独处理 -->
  <router-view v-if="isLoginPage" />

  <!-- 使用侧边栏布局 -->
  <SidebarLayout v-else />
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SidebarLayout from '@/components/SidebarLayout.vue'

const route = useRoute()

const isLoginPage = computed(() => route.path === '/login' || route.path === '/auth/callback')
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  /* 配色方案 */
  --color-bg-primary: #1E1E1E;
  --color-bg-secondary: #252525;
  --color-bg-tertiary: #2a2a2a;
  --color-bg-hover: #3A3A3A;
  --color-bg-elevated: #252525;
  --color-bg-surface: #1e1e1e;
  --color-bg-glass: rgba(30, 30, 30, 0.95);
  --color-border: #333333;
  --color-border-subtle: #333333;
  --color-border-light: #444444;
  --color-border-hover: #444444;
  --color-text-primary: #ffffff;
  --color-text-secondary: #B0B0B0;
  --color-text-tertiary: #888888;
  --color-text-muted: #888888;
  --color-blue: #3b82f6;
  --color-blue-light: #60a5fa;
  --color-accent-primary: #3b82f6;
  --color-accent-light: rgba(59, 130, 246, 0.15);
  --color-blue-glow: rgba(59, 130, 246, 0.3);
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-error-bg: rgba(239, 68, 68, 0.15);
  --color-green: #10b981;
  --color-red: #ef4444;
  --color-yellow: #f59e0b;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --transition-fast: 0.15s ease;
  --transition-base: 0.2s ease;

  /* 间距 */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-accent: 0 4px 12px rgba(59, 130, 246, 0.15);
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
}

#app {
  width: 100%;
  height: 100%;
}
</style>
