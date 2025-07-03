<template>
  <div class="home-layout">
    <Navbar 
      @publish="showPostDialog = true" 
      @login="showLoginDialog = true"
      @register="showRegisterDialog = true"
      @search="handleSearch"
    />
    <!-- 添加加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-loading :loading="loading" text="加载中...">
        <div style="height: 400px;"></div>
      </el-loading>
    </div>
    
    <div v-else class="main-content">
      <div class="left-panel">
        <div class="filter-section">
          <!-- 搜索状态指示器 -->
          <div v-if="isSearchMode" class="search-status">
            <div class="search-info">
              <span class="search-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              <span class="search-text">搜索："{{ currentSearchQuery }}"</span>
              <span class="search-count">({{ searchResults.length }}条结果)</span>
            </div>
            <el-button 
              type="text" 
              size="small" 
              class="clear-search-btn"
              @click="clearSearch"
            >
              清除搜索
            </el-button>
          </div>
          
          <div class="filter-tabs">
            <button 
              v-for="tab in filterTabs" 
              :key="tab.value"
              :class="['filter-tab', { active: typeFilter === tab.value }]"
              @click="typeFilter = tab.value"
            >
              <span class="tab-icon">
                <svg v-if="tab.value === 'all'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 3H21V21H3V3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M3 9H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 21V9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else-if="tab.value === 'lost'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else-if="tab.value === 'found'" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 11.08V12C21.9988 14.1564 21.3005 16.2547 20.0093 17.9818C18.7182 19.7088 16.9033 20.9725 14.8354 21.5839C12.7674 22.1953 10.5573 22.1219 8.53447 21.3746C6.51168 20.6273 4.78465 19.2461 3.61096 17.4371C2.43727 15.628 1.87979 13.4881 2.02168 11.3363C2.16356 9.18455 2.99721 7.13631 4.39828 5.49706C5.79935 3.85781 7.69279 2.71537 9.79619 2.24013C11.8996 1.76488 14.1003 1.98232 16.07 2.85999" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              {{ tab.label }}
            </button>
          </div>
          
          <div class="advanced-filters">
            <div class="filter-group">
              <label class="filter-label">时间筛选</label>
              <el-date-picker 
                v-model="dateFilter" 
                type="date" 
                placeholder="显示此日期后的帖子" 
                class="date-picker"
                size="small"
                clearable
              />
            </div>
            
            <div class="filter-group">
              <label class="filter-label">类别筛选</label>
              <el-select 
                v-model="categoryFilter" 
                placeholder="选择类别" 
                size="small"
                class="category-picker"
                clearable
              >
                <el-option label="全部类别" value="all" />
                <el-option label="证件卡类" value="id" />
                <el-option label="电子设备" value="electronics" />
                <el-option label="书籍文具" value="book" />
                <el-option label="衣物包类" value="clothes" />
                <el-option label="钥匙卡类" value="key" />
                <el-option label="其他物品" value="other" />
              </el-select>
            </div>
          </div>
        </div>
        
        <div v-if="loading || searchLoading" class="loading-container">
          <el-loading :loading="true" text="加载中...">
            <div style="height: 200px;"></div>
          </el-loading>
        </div>
        <PostList 
          v-else
          :posts="filteredPosts" 
          :selectedId="selectedPostId" 
          :is-login="isLogin"
          @select="selectPost" 
          @require-login="showLoginDialog = true"
        />
      </div>
      
      <div class="right-panel">
        <div class="detail-container">
                  <PostDetail 
          v-if="selectedPost" 
          :post="selectedPost" 
          :map-img="mapImg" 
          :is-login="isLogin" 
          @require-login="showLoginDialog = true" 
          @comment="handleAddComment"
        />
          <div v-else class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 21L16.514 16.506L21 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3>请选择一条帖子</h3>
            <p>从左侧列表中选择一条帖子查看详细信息</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 发布对话框 -->
    <el-dialog 
      v-model="showPostDialog" 
      title="发布新信息" 
      width="650px" 
      :close-on-click-modal="false"
      class="post-dialog"
    >
      <NewPostForm @success="handlePostSuccess" />
    </el-dialog>
    
    <!-- 登录对话框 -->
    <Login 
      v-model:visible="showLoginDialog"
      @switch-register="switchToRegister"
    />
    
    <!-- 注册对话框 -->
    <Register 
      v-model:visible="showRegisterDialog"
      @switch-login="switchToLogin"
    />
    
    <el-dialog v-model="showLoginTipDialog" title="未登录" width="340px" :show-close="true" center>
      <div style="text-align:center;">
        <div style="font-size:18px;color:#ff9800;margin-bottom:12px;">请先登录后再访问个人中心</div>
        <el-button type="primary" @click="goLoginFromTip">去登录</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import Navbar from '../components/Navbar.vue'
import PostList from '../components/PostList.vue'
import PostDetail from '../components/PostDetail.vue'
import NewPostForm from '../components/NewPostForm.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import { useUserStore } from '../store/user'
import { useRoute } from 'vue-router'
import { getAllItems, addComment, searchItems } from '../api/items'

const mapImg = '/map.png'
const route = useRoute()

const posts = ref([])
const loading = ref(false)
const cache = ref(new Map())

// 搜索相关状态
const currentSearchQuery = ref('')
const searchResults = ref([])
const isSearchMode = ref(false)
const searchLoading = ref(false)

// 添加防抖功能
let fetchTimeout = null
let searchTimeout = null

async function fetchPosts(useCache = true) {
  // 检查缓存
  if (useCache && cache.value.has('posts')) {
    const cached = cache.value.get('posts')
    if (Date.now() - cached.timestamp < 30000) { // 30秒缓存
      posts.value = cached.data
      if (posts.value?.length > 0 && !selectedPostId.value) {
        selectedPostId.value = posts.value[0].id
      }
      return
    }
  }
  
  loading.value = true
  try {
    const resp = await getAllItems()
    posts.value = resp.data
    
    // 更新缓存
    cache.value.set('posts', {
      data: resp.data,
      timestamp: Date.now()
    })
    
    // 获取到数据后，默认选中第一条
    if (posts.value && posts.value.length > 0 && !selectedPostId.value) {
      selectedPostId.value = posts.value[0].id
    }
  } catch (e) {
    console.error('获取帖子失败:', e)
    posts.value = []
  } finally {
    loading.value = false
  }
}

// 防抖刷新
function debouncedFetch() {
  if (fetchTimeout) clearTimeout(fetchTimeout)
  fetchTimeout = setTimeout(() => fetchPosts(false), 300)
}

// 搜索功能
async function performSearch(query) {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(async () => {
    try {
      currentSearchQuery.value = query
      
      if (!query || !query.trim()) {
        // 清空搜索，回到正常模式
        isSearchMode.value = false
        searchResults.value = []
        selectedPostId.value = posts.value?.length > 0 ? posts.value[0].id : null
        return
      }
      
      isSearchMode.value = true
      searchLoading.value = true
      
      const response = await searchItems(query.trim())
      searchResults.value = response.data.results || []
      
      // 搜索后默认选中第一条结果
      if (searchResults.value.length > 0) {
        selectedPostId.value = searchResults.value[0].id
      } else {
        selectedPostId.value = null
      }
      
    } catch (error) {
      console.error('搜索失败:', error)
      searchResults.value = []
      selectedPostId.value = null
    } finally {
      searchLoading.value = false
    }
  }, 300)
}

// 处理从导航栏传来的搜索事件
function handleSearch(query) {
  performSearch(query)
}

// 清除搜索
function clearSearch() {
  currentSearchQuery.value = ''
  isSearchMode.value = false
  searchResults.value = []
  selectedPostId.value = posts.value?.length > 0 ? posts.value[0].id : null
}

onMounted(async () => {
  // 初始化用户状态
  if (userStore.token && !userStore.userInfo) {
    try {
      await userStore.refreshUserInfo()
    } catch (error) {
      console.error('初始化用户状态失败:', error)
    }
  }
  
  // 获取帖子数据
  fetchPosts()
  
  // 监听全局登录弹窗事件
  window.addEventListener('show-login-tip', handleShowLoginTip)
  
  // 监听全局发布对话框事件
  window.addEventListener('show-publish-dialog', () => {
    showPostDialog.value = true
  })
  
  // 添加窗口焦点事件监听（防抖刷新）
  window.addEventListener('focus', debouncedFetch)
  
  // 监听全局发布成功事件
  window.addEventListener('post-published', () => {
    fetchPosts(false) // 发布成功后刷新数据
  })
  
  // 监听认领状态更新事件
  window.addEventListener('claim-status-updated', handleClaimStatusUpdate)
})

onUnmounted(() => {
  // 清理事件监听器
  window.removeEventListener('show-login-tip', handleShowLoginTip)
  window.removeEventListener('show-publish-dialog', () => {
    showPostDialog.value = true
  })
  window.removeEventListener('focus', debouncedFetch)
  window.removeEventListener('post-published', () => {
    fetchPosts(false)
  })
  window.removeEventListener('claim-status-updated', handleClaimStatusUpdate)
  
  // 清理定时器
  if (fetchTimeout) clearTimeout(fetchTimeout)
})

// 监听路由查询参数变化
watch(() => route.query.selected, (selectedId) => {
  if (selectedId && posts.value.length > 0) {
    selectedPostId.value = selectedId
  }
}, { immediate: true })

// 监听posts变化，处理URL中的selected参数
watch(posts, (newPosts) => {
  if (newPosts.length > 0 && route.query.selected) {
    const postExists = newPosts.find(p => p.id === route.query.selected)
    if (postExists) {
      selectedPostId.value = route.query.selected
    }
  }
}, { immediate: true })

function handlePostSuccess() {
  showPostDialog.value = false
  fetchPosts(false) // 发布成功后，重新获取帖子，不使用缓存
}

async function handleAddComment(content) {
  if (!selectedPostId.value || !content.trim()) return
  
  try {
    await addComment(selectedPostId.value, content.trim())
    // 评论成功后重新获取帖子列表以更新评论
    await fetchPosts(false)
    // 保持当前选中的帖子
    selectedPostId.value = selectedPostId.value
  } catch (error) {
    console.error('添加评论失败:', error)
  }
}

// 处理认领状态更新的函数
async function handleClaimStatusUpdate() {
  // 当收到认领申请被批准的通知时，刷新帖子列表
  try {
    cache.value.clear()
    await fetchPosts(false)
    
    // 如果在搜索模式，也重新搜索以更新结果
    if (isSearchMode.value && currentSearchQuery.value) {
      await performSearch(currentSearchQuery.value)
    }
  } catch (error) {
    console.error('刷新数据失败:', error)
  }
}

const typeFilter = ref('all') // 'all', 'lost', 'found'
const dateFilter = ref(null)
const categoryFilter = ref('all')
const selectedPostId = ref(null)

const filterTabs = [
  { label: '全部', value: 'all' },
  { label: '失物', value: 'lost' },
  { label: '招领', value: 'found' },
  { label: '已认领', value: 'claimed' }
]

const selectedPost = computed(() => {
  if (!selectedPostId.value) return null
  
  // 根据当前模式从对应的数据源中查找
  const sourceData = isSearchMode.value ? searchResults.value : posts.value;
  if (!sourceData) return null
  
  return sourceData.find(p => p.id === selectedPostId.value)
})

const filteredPosts = computed(() => {
  // 根据是否在搜索模式选择数据源
  const sourceData = isSearchMode.value ? searchResults.value : posts.value;
  
  if (!sourceData || sourceData.length === 0) return [];

  // 先过滤数据
  const filtered = sourceData.filter(p => {
    // 1. 类型过滤（失物/招领/已认领）
    const matchType = (() => {
      if (typeFilter.value === 'all') return true;
      if (typeFilter.value === 'claimed') return p.claimed || p.is_claimed;
      if (typeFilter.value === 'found') return (p.status === 'found') && !(p.claimed || p.is_claimed);
      return p.status === typeFilter.value && !(p.claimed || p.is_claimed);
    })();

    // 2. 类别过滤
    const matchCategory = categoryFilter.value === 'all' || p.category === categoryFilter.value;

    // 3. 日期过滤 - 筛选该日期之后发布的帖子
    const matchDate = (() => {
      if (!dateFilter.value) return true;
      if (!p.date && !p.created_at) return false;
      
      try {
        // 使用创建时间或日期字段
        const postDateStr = p.created_at || p.date;
        const postDate = new Date(postDateStr);
        const filterDate = new Date(dateFilter.value);
        
        // 只显示选择日期之后发布的帖子
        return postDate >= filterDate;
      } catch (e) {
        return false;
      }
    })();
    
    return matchType && matchCategory && matchDate;
  });

  // 然后排序 - 按照需求排序
  return filtered.sort((a, b) => {
    // 如果显示全部帖子，已认领的放在底部
    if (typeFilter.value === 'all') {
      const aIsClaimed = a.claimed || a.is_claimed;
      const bIsClaimed = b.claimed || b.is_claimed;
      
      // 已认领的帖子排在后面
      if (aIsClaimed && !bIsClaimed) return 1;
      if (!aIsClaimed && bIsClaimed) return -1;
      
      // 同类型内按时间排序（使用拾取/丢失时间，即date字段）
      if (aIsClaimed && bIsClaimed) {
        // 已认领的按认领时间倒序
        const aClaimedTime = new Date(a.claimedAt || a.claimed_at || a.created_at || a.date);
        const bClaimedTime = new Date(b.claimedAt || b.claimed_at || b.created_at || b.date);
        return bClaimedTime - aClaimedTime;
      }
    }
    
    // 其他情况按拾取/丢失时间排序（即date字段，倒序 - 最新的在前）
    const aTime = new Date(a.date || a.created_at);
    const bTime = new Date(b.date || b.created_at);
    return bTime - aTime;
  });
});


function selectPost(id) {
  selectedPostId.value = id
}

function switchToRegister() {
  showLoginDialog.value = false
  showRegisterDialog.value = true
}

function switchToLogin() {
  showRegisterDialog.value = false
  showLoginDialog.value = true
}

const userStore = useUserStore()
const showPostDialog = ref(false)
const showLoginDialog = ref(false)
const showRegisterDialog = ref(false)
const showLoginTipDialog = ref(false)
// 修改登录状态判断，使用store的isLogin计算属性
const isLogin = computed(() => userStore.isLogin)

function handleShowLoginTip() {
  showLoginTipDialog.value = true
}

onMounted(() => {
  window.addEventListener('show-login-tip', handleShowLoginTip)
})
onUnmounted(() => {
  window.removeEventListener('show-login-tip', handleShowLoginTip)
})

function goLoginFromTip() {
  showLoginTipDialog.value = false
  showLoginDialog.value = true
}

// handleSearch已在上面定义
</script>

<style scoped>
.home-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-gray);
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.left-panel {
  width: 380px;
  min-width: 320px;
  background: var(--bg-white);
  border-right: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-light);
}

.filter-section {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-white);
}

.search-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(74, 144, 226, 0.05);
  border: 1px solid rgba(74, 144, 226, 0.2);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
}

.search-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  flex: 1;
}

.search-icon {
  color: var(--brand-blue);
  display: flex;
  align-items: center;
}

.search-text {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  font-weight: 500;
}

.search-count {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.clear-search-btn {
  color: var(--brand-blue);
  font-size: var(--font-size-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
}

.filter-tabs {
  display: flex;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.filter-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  background: var(--bg-white);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-tab:hover {
  border-color: var(--brand-blue-light);
  color: var(--brand-blue);
}

.filter-tab.active {
  background: var(--brand-blue);
  border-color: var(--brand-blue);
  color: white;
}

.tab-icon {
  display: flex;
  align-items: center;
}

.advanced-filters {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.filter-label {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: var(--spacing-xs);
}

.date-picker,
.category-picker {
  width: 100%;
}

.right-panel {
  flex: 1;
  padding: var(--spacing-xl);
  overflow-y: auto;
  background: var(--bg-gray);
}

.detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  margin-bottom: var(--spacing-lg);
  color: var(--text-light);
}

.empty-state h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-secondary);
}

.empty-state p {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-relaxed);
}

/* 对话框样式优化 */
:deep(.el-dialog) {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-heavy);
}

:deep(.el-dialog__header) {
  padding: var(--spacing-lg) var(--spacing-xl) var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

:deep(.el-dialog__title) {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

:deep(.el-dialog__body) {
  padding: var(--spacing-xl);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .left-panel {
    width: 340px;
    min-width: 280px;
  }
  
  .right-panel {
    padding: var(--spacing-lg);
  }
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .left-panel {
    width: 100%;
    min-width: 0;
    border-right: none;
    border-bottom: 1px solid var(--border-light);
  }
  
  .filter-section {
    padding: var(--spacing-md);
  }
  
  .right-panel {
    padding: var(--spacing-md);
  }
  
  .detail-container {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .filter-tabs {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .filter-tab {
    justify-content: flex-start;
  }
 }
</style>