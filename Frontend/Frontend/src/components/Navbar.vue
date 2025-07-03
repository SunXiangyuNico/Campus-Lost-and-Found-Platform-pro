<template>
  <header class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <div class="logo-section">
          <div class="logo-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <span class="brand">校园失物招领平台</span>
        </div>
        
        <div class="search-section">
          <div class="search-wrapper">
            <div class="search-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <input 
              type="text" 
              placeholder="搜索物品名称、描述、地点..." 
              class="search-input"
              v-model="searchQuery"
              @keyup.enter="performSearch"
              @input="onSearchInput"
            />
            <el-button 
              type="primary" 
              class="search-btn"
              @click="performSearch"
              :disabled="!searchQuery.trim()"
            >
              搜索
            </el-button>
            <el-button 
              v-if="searchQuery.trim()"
              type="text" 
              class="clear-btn"
              @click="clearSearch"
              title="清除搜索"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="navbar-right">
        <nav class="nav-menu">
          <router-link to="/home" class="nav-item" :class="{ active: $route.path === '/home' }">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            首页
          </router-link>
          <router-link 
            v-if="isLogin"
            to="/messages" 
            class="nav-item message-nav" 
            :class="{ active: $route.path.startsWith('/messages') }"
            @click="handleMessagesClick"
          >
            <div class="nav-icon-wrapper">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <el-badge 
                v-if="unreadCount > 0" 
                :value="unreadCount > 99 ? '99+' : unreadCount" 
                :max="99"
                class="message-badge"
              />
            </div>
            我的消息
          </router-link>
          <router-link 
            to="/profile" 
            class="nav-item" 
            :class="{ active: $route.path.startsWith('/profile') }"
            @click.prevent="handleProfileClick"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            个人中心
          </router-link>
        </nav>
        
        <div class="auth-section">
          <el-button 
            v-if="!isLogin" 
            type="text" 
            class="login-btn"
            @click="goLogin"
          >
            登录
          </el-button>
          <el-button 
            v-if="!isLogin" 
            type="text" 
            class="register-btn"
            @click="goRegister"
          >
            注册
          </el-button>
          <el-button 
            type="primary" 
            class="publish-btn"
            @click="goPublish"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            发布
          </el-button>
          
          <el-dropdown v-if="isLogin" class="user-dropdown">
            <div class="user-info">
              <el-avatar 
                :size="32" 
                :src="userStore.userInfo?.avatar ? getAvatarUrl(userStore.userInfo.avatar) : undefined"
              >
                {{ userStore.userInfo?.name?.[0] || 'U' }}
              </el-avatar>
              <span class="username">{{ userStore.userInfo?.name || '用户' }}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <polyline points="6,9 12,15 18,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <polyline points="16,17 21,12 16,7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '../store/user'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { getAvatarUrl } from '../utils/index.js'

const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

// 修改登录状态判断，使用更宽松的条件
const isLogin = computed(() => !!userStore.token)  // 只检查token存在性
const searchQuery = ref('')

// 未读消息数量
const unreadCount = ref(0)
let unreadCountInterval = null

// 防抖定时器
let searchTimeout = null

function performSearch() {
  const query = searchQuery.value.trim()
  if (query) {
    emit('search', query)
  }
}

// 输入时的实时搜索（防抖）
function onSearchInput() {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  const query = searchQuery.value.trim()
  if (query) {
    searchTimeout = setTimeout(() => {
      emit('search', query)
    }, 300) // 300ms防抖
  } else {
    // 如果搜索框为空，清除搜索
    emit('search', '')
  }
}

function clearSearch() {
  searchQuery.value = ''
  emit('search', '')
}

function goLogin() {
  emit('login')
}

function goRegister() {
  emit('register')
}

function goPublish() {
  if (!isLogin.value) {
    ElMessage.warning('请先登录后再发布信息')
    emit('login')
    return
  }
  emit('publish')
}

function logout() {
  userStore.logout()
  // 如果当前在首页，刷新页面以更新状态；否则跳转到首页
  if (route.path === '/home') {
    // 刷新当前页面以更新登录状态
    window.location.reload()
  } else {
    router.push('/home')
  }
}

async function handleProfileClick() {
  if (!isLogin.value) {
    goLogin()
    return
  }
  
  // 确保用户信息是最新的
  try {
    await userStore.checkLoginStatus()
    if (userStore.isLogin) {
      router.push('/profile')
    } else {
      goLogin()
    }
  } catch (error) {
    console.error('检查登录状态失败:', error)
    goLogin()
  }
}

function handleMessagesClick() {
  console.log('=== 点击我的消息按钮 ===')
  console.log('Token:', userStore.token ? '存在' : '不存在')
  console.log('用户信息:', userStore.userInfo)
  console.log('当前登录状态(isLogin):', isLogin.value)
  console.log('Store状态:', {
    hasToken: !!userStore.token,
    hasUserInfo: !!userStore.userInfo,
    hasUserId: !!(userStore.userInfo && userStore.userInfo.id)
  })
  
  // 不阻止默认的router-link导航行为
  console.log('让router-link执行默认导航...')
}

// 获取未读消息数量
async function fetchUnreadCount() {
  if (!isLogin.value || !userStore.token) {
    unreadCount.value = 0
    return
  }
  
  try {
    const response = await axios.get('/api/messages/unread-count')
    unreadCount.value = response.data.total || 0
  } catch (error) {
    console.error('获取未读消息数量失败:', error)
  }
}

// 启动未读消息数量轮询
function startUnreadCountPolling() {
  if (unreadCountInterval) {
    clearInterval(unreadCountInterval)
  }
  
  // 立即获取一次
  fetchUnreadCount()
  
  // 每30秒更新一次
  unreadCountInterval = setInterval(() => {
    fetchUnreadCount()
  }, 30000)
}

// 停止未读消息数量轮询
function stopUnreadCountPolling() {
  if (unreadCountInterval) {
    clearInterval(unreadCountInterval)
    unreadCountInterval = null
  }
  unreadCount.value = 0
}

const emit = defineEmits(['search', 'publish', 'login', 'register'])



  // 监听登录状态变化
  watch(isLogin, (newValue) => {
  if (newValue) {
    startUnreadCountPolling()
  } else {
    stopUnreadCountPolling()
  }
})

// 页面加载时刷新用户信息
onMounted(async () => {
  if (userStore.token && !userStore.userInfo) {
    try {
      await userStore.refreshUserInfo()
    } catch (error) {
      console.error('初始化用户信息失败:', error)
    }
  }
  
  // 如果已登录，启动未读消息轮询
  if (isLogin.value) {
    startUnreadCountPolling()
  }
  
  // 监听全局头像更新事件
  window.addEventListener('avatar-updated', () => {
    userStore.refreshUserInfo()
  })
  
  // 监听消息更新事件
  window.addEventListener('message-updated', () => {
    fetchUnreadCount()
  })
  
  // 监听立即刷新未读计数事件
  window.addEventListener('refresh-unread-count', () => {
    fetchUnreadCount()
  })
})

// 清理事件监听器
onUnmounted(() => {
  stopUnreadCountPolling()
  
  window.removeEventListener('avatar-updated', () => {
    userStore.refreshUserInfo()
  })
  
  window.removeEventListener('message-updated', () => {
    fetchUnreadCount()
  })
  
  window.removeEventListener('refresh-unread-count', () => {
    fetchUnreadCount()
  })
})
</script>

<style scoped>
.navbar {
  background: var(--bg-white);
  box-shadow: var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--border-light);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  flex: 1;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  min-width: 200px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--brand-blue), var(--brand-blue-light));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand {
  font-weight: 600;
  font-size: var(--font-size-lg);
  color: var(--text-primary);
  white-space: nowrap;
}

.search-section {
  flex: 1;
  max-width: 500px;
}

.search-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.search-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  z-index: 1;
}

.search-input {
  flex: 1;
  height: 40px;
  padding: 0 var(--spacing-md) 0 44px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  background: var(--bg-gray);
  transition: all 0.2s ease;
}

.search-btn {
  height: 40px;
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  padding: 0 var(--spacing-lg);
  white-space: nowrap;
}

.clear-btn {
  height: 40px;
  width: 40px;
  border-radius: var(--radius-lg);
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  background: transparent;
  border: none;
  transition: all 0.2s ease;
}

.clear-btn:hover {
  color: var(--text-secondary);
  background: rgba(0, 0, 0, 0.05);
}

.search-input:focus {
  outline: none;
  border-color: var(--brand-blue);
  background: var(--bg-white);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.nav-item.active {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.1);
}

/* 消息相关样式 */
.nav-icon-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.message-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  z-index: 10;
}

.message-nav .el-badge__content {
  background-color: #f56565;
  border: 1px solid #fff;
  font-size: 12px;
  min-width: 18px;
  height: 18px;
  line-height: 16px;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.login-btn {
  color: var(--text-secondary);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
}

.login-btn:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.register-btn {
  color: var(--text-secondary);
  font-weight: 500;
  padding: var(--spacing-sm) var(--spacing-md);
}

.register-btn:hover {
  color: var(--brand-blue);
  background: rgba(74, 144, 226, 0.05);
}

.publish-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-weight: 500;
  border-radius: var(--radius-lg);
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-md);
  transition: background 0.2s ease;
}

.user-info:hover {
  background: var(--bg-gray);
}

.username {
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--text-primary);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .navbar-container {
    padding: 0 var(--spacing-lg);
  }
  
  .navbar-left {
    gap: var(--spacing-lg);
  }
  
  .search-section {
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 var(--spacing-md);
  }
  
  .navbar-left {
    gap: var(--spacing-md);
  }
  
  .logo-section {
    min-width: auto;
  }
  
  .brand {
    display: none;
  }
  
  .search-section {
    max-width: 200px;
  }
  
  .nav-menu {
    display: none;
  }
}

@media (max-width: 480px) {
  .search-section {
    display: none;
  }
  
  .auth-section {
    gap: var(--spacing-xs);
  }
  
  .publish-btn {
    padding: var(--spacing-sm);
  }
  
  .publish-btn span {
    display: none;
  }
}
</style> 