<template>
  <!-- 添加全局加载状态 -->
  <div v-if="userStore.isLoading" class="global-loading">
    <el-loading :loading="true" text="初始化中..." />
  </div>
  <router-view v-else />
</template>

<script setup>
import { useUserStore } from './store/user'

const userStore = useUserStore()
</script>

<style>
/* 全局设计系统 */
:root {
  /* 主色调 */
  --brand-blue: #4A90E2;
  --brand-blue-light: #6BA3E8;
  --brand-blue-dark: #357ABD;
  
  /* 背景色 */
  --bg-gray: #F5F7FA;
  --bg-white: #FFFFFF;
  --bg-card: #FFFFFF;
  
  /* 文本色 */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-muted: #888888;
  --text-light: #AAAAAA;
  
  /* 状态色 */
  --status-lost: #F56C6C;
  --status-found: #67C23A;
  --status-warning: #E6A23C;
  --status-info: #909399;
  
  /* 边框和阴影 */
  --border-light: #E0E0E0;
  --border-medium: #D0D0D0;
  --shadow-light: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-medium: 0 4px 12px rgba(0, 0, 0, 0.12);
  --shadow-heavy: 0 8px 24px rgba(0, 0, 0, 0.16);
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 48px;
  
  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* 字体 */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-xxl: 24px;
  --font-size-title: 28px;
  
  /* 行高 */
  --line-height-tight: 1.4;
  --line-height-normal: 1.6;
  --line-height-relaxed: 1.8;
}

/* 全局重置 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: var(--font-family);
  font-size: var(--font-size-md);
  line-height: var(--line-height-normal);
  color: var(--text-primary);
  background-color: var(--bg-gray);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 全局过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 全局按钮样式优化 */
.el-button {
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.2s ease;
}

.el-button--primary {
  background-color: var(--brand-blue);
  border-color: var(--brand-blue);
}

.el-button--primary:hover {
  background-color: var(--brand-blue-light);
  border-color: var(--brand-blue-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-medium);
}

/* 全局卡片样式优化 */
.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-light);
  transition: box-shadow 0.2s ease;
}

.el-card:hover {
  box-shadow: var(--shadow-medium);
}

/* 全局输入框样式优化 */
.el-input__wrapper {
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
}

.el-input__wrapper:hover {
  box-shadow: 0 0 0 1px var(--brand-blue-light);
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 1px var(--brand-blue);
}

/* 全局标签样式优化 */
.el-tag {
  border-radius: var(--radius-sm);
  font-weight: 500;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #D0D0D0;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #B0B0B0;
}

/* 工具类 */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: var(--spacing-xs); }
.mb-2 { margin-bottom: var(--spacing-sm); }
.mb-3 { margin-bottom: var(--spacing-md); }
.mb-4 { margin-bottom: var(--spacing-lg); }
.mb-5 { margin-bottom: var(--spacing-xl); }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: var(--spacing-xs); }
.mt-2 { margin-top: var(--spacing-sm); }
.mt-3 { margin-top: var(--spacing-md); }
.mt-4 { margin-top: var(--spacing-lg); }
.mt-5 { margin-top: var(--spacing-xl); }

.p-0 { padding: 0; }
.p-1 { padding: var(--spacing-xs); }
.p-2 { padding: var(--spacing-sm); }
.p-3 { padding: var(--spacing-md); }
.p-4 { padding: var(--spacing-lg); }
.p-5 { padding: var(--spacing-xl); }

/* 全局加载样式 */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
</style> 