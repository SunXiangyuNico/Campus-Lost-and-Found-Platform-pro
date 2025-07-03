<template>
  <div class="post-detail">
    <!-- 用户信息头部 -->
    <div class="post-header">
      <div class="user-info">
        <el-avatar 
          :src="getAvatarUrl(post.user?.avatar || post.avatar)" 
          size="large"
          class="user-avatar"
          @click="handleAvatarClick"
        >
          {{ getUserDisplayName(post)[0] || 'U' }}
        </el-avatar>
        <div class="user-details">
          <div class="user-name clickable" @click="handleAvatarClick">{{ getUserDisplayName(post) }}</div>
          <div class="post-meta">
            <span class="post-time">{{ formatTime(post.time) }}</span>
            <span class="post-type-badge" :class="post.type">
              {{ post.type === 'lost' ? '失物' : '招领' }}
            </span>
          </div>
        </div>
      </div>
      <div class="post-actions">
        <div class="action-buttons">
          <el-button 
            type="primary" 
            size="large"
            :disabled="isClaimed" 
            @click="onContact"
            class="contact-btn"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2H2C1.46957 2 0.960859 2.21071 0.585786 2.58579C0.210714 2.96086 0 3.46957 0 4V22C0 22.5304 0.210714 23.0391 0.585786 23.4142C0.960859 23.7893 1.46957 24 2 24H22C22.5304 24 23.0391 23.7893 23.4142 23.4142C23.7893 23.0391 24 22.5304 24 22V4C24 3.46957 23.7893 2.96086 23.4142 2.58579C23.0391 2.21071 22.5304 2 22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ isClaimed ? '已认领' : '联系帖主' }}
          </el-button>
          <el-button 
            v-if="post.status === 'found' && !isClaimed" 
            type="success" 
            size="large"
            @click="onClaim"
            class="claim-btn"
          >
            申请认领
          </el-button>
        </div>
        <div v-if="isClaimed" class="claimed-info">
          <el-tag type="success" size="large">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            此物品已被认领
          </el-tag>
          <div class="claimed-details">
            <span v-if="post.claimedAt || post.claimed_at" class="claimed-time">
              认领时间：{{ formatTime(post.claimedAt || post.claimed_at) }}
            </span>
            <div v-if="post.claimedBy || post.claimed_by" class="claimed-by">
              <span>认领者：</span>
              <el-avatar 
                :src="getClaimedUserAvatar()" 
                size="small"
                class="claimed-user-avatar"
                @click="handleClaimedUserClick"
              >
                {{ getClaimedUserName()[0] || 'U' }}
              </el-avatar>
              <span class="claimed-user-name clickable" @click="handleClaimedUserClick">
                {{ getClaimedUserName() }}
              </span>
              <span class="claimed-contact-tip">（可私信联系）</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          物品描述
        </h3>
        <p class="post-description">{{ post.desc }}</p>
      </div>

      <!-- 图片展示 -->
      <div v-if="post.images && post.images.length" class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="8.5" cy="8.5" r="1.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="21,15 16,10 5,21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          相关图片
        </h3>
        <div class="image-gallery">
          <div 
            v-for="(img, idx) in post.images" 
            :key="idx" 
            class="image-item"
            @click="previewImage(img)"
          >
            <img :src="img" :alt="`图片 ${idx + 1}`" />
          </div>
        </div>
      </div>

      <!-- 地点信息 -->
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 7.61305 3.94821 5.32387 5.63604 3.63604C7.32387 1.94821 9.61305 1 12 1C14.3869 1 16.6761 1.94821 18.364 3.63604C20.0518 5.32387 21 7.61305 21 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          丢失/拾取地点
        </h3>
        <div class="location-info">
          <div class="location-text">{{ post.locationText }}</div>
          <div class="map-container">
            <img :src="mapImg" class="map-img" alt="校园地图" />
            <div v-if="post.locationCoord" class="map-marker" :style="markerStyle"></div>
          </div>
        </div>
      </div>

      <!-- 评论区 -->
      <div class="content-section">
        <h3 class="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          评论区
        </h3>
        
        <div v-if="post.comments && post.comments.length" class="comments-list">
          <div v-for="(comment, i) in post.comments" :key="i" class="comment-item">
            <el-avatar 
              :src="getAvatarUrl(comment.avatar)" 
              size="small"
              class="comment-avatar"
              @click="handleCommentAvatarClick(comment)"
            >
              {{ comment.nickname?.[0] || 'U' }}
            </el-avatar>
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author clickable" @click="handleCommentAvatarClick(comment)">{{ comment.nickname }}</span>
                <span class="comment-time">{{ formatTime(comment.time) }}</span>
              </div>
              <p class="comment-text">{{ comment.content }}</p>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-comments">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>暂无评论</p>
        </div>
        
        <div class="comment-input">
          <el-input 
            v-model="commentText" 
            placeholder="写下你的评论..." 
            type="textarea"
            :rows="3"
            maxlength="200"
            show-word-limit
          />
          <el-button 
            type="primary" 
            @click="onSendComment" 
            :disabled="!commentText.trim()"
            class="send-btn"
          >
            发送评论
          </el-button>
        </div>
      </div>
    </div>

    <!-- 私信弹窗 -->
    <SendMessageDialog 
      v-model:visible="sendMessageDialog.show"
      :user="sendMessageDialog.user"
      :related-item="sendMessageDialog.relatedItem"
      @sent="handleMessageSent"
    />
  </div>
</template>

<script setup>
import { ref, watch, computed, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { sendClaimRequest } from '../api/messages'
import { useUserStore } from '../store/user'
import SendMessageDialog from './SendMessageDialog.vue'
import { getAvatarUrl, getUserDisplayName, formatTime } from '../utils/index.js'

const props = defineProps({
  post: {
    type: Object,
    required: true
  },
  mapImg: {
    type: String,
    required: false
  },
  isLogin: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['claim', 'comment', 'require-login'])
const commentText = ref('')
const userStore = useUserStore()

// 私信弹窗相关
const sendMessageDialog = reactive({
  show: false,
  user: null,
  relatedItem: null
})

// 计算是否已被认领
const isClaimed = computed(() => {
  return props.post.claimed || props.post.is_claimed
})

function onContact() {
  if (isClaimed.value) {
    ElMessage.info('该物品已被认领')
    return
  }
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再联系！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }
  
  // 显示发布者的联系方式
  const contactInfo = props.post.contact || props.post.user?.email || '暂无联系方式'
  ElMessageBox.alert(
    `请通过以下方式联系帖主：\n${contactInfo}`,
    '联系方式',
    {
      confirmButtonText: '我知道了',
      type: 'info',
      center: true
    }
  )
}

async function onClaim() {
  if (!props.isLogin) {
    emit('require-login')
    return
  }

  // 检查是否是自己的帖子
  if (props.post.user?.id === userStore.userInfo?.id || props.post.userId === userStore.userInfo?.id) {
    ElMessage.error('不能认领自己发布的物品')
    return
  }
  
  try {
    const { value: claimMessage } = await ElMessageBox.prompt(
      '请说明您认领这个物品的原因或提供相关证明：',
      '发送认领申请',
      {
        confirmButtonText: '发送申请',
        cancelButtonText: '取消',
        inputType: 'textarea',
        inputPlaceholder: '例如：这是我丢失的物品，物品特征是...',
        inputValidator: (value) => {
          if (!value || value.trim().length < 10) {
            return '请至少输入10个字符说明认领原因'
          }
          if (value.length > 500) {
            return '说明内容不能超过500字符'
          }
          return true
        }
      }
    )
    
    await sendClaimRequest(props.post.id, claimMessage.trim())
    ElMessage.success('认领申请已发送，请等待物品发布者确认')
    
    // 触发全局消息更新事件
    window.dispatchEvent(new CustomEvent('message-updated'))
    
    // 注意：这里不再触发claim事件，因为认领还未完成，只是发送了申请
    // 状态会在发帖者批准后通过其他方式更新
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发送认领申请失败:', error)
      
      // 根据错误类型提供更详细的提示
      let errorMessage = '发送认领申请失败'
      if (error.response) {
        const status = error.response.status
        const data = error.response.data
        
        switch (status) {
          case 400:
            if (data.message === 'Item has already been claimed') {
              errorMessage = '此物品已被他人认领'
            } else if (data.message === 'You cannot claim your own item') {
              errorMessage = '不能认领自己发布的物品'
            } else if (data.message === 'You have already sent a claim request for this item') {
              errorMessage = '您已经申请过认领此物品，请勿重复申请'
            } else {
              errorMessage = data.message || '请求参数错误'
            }
            break
          case 401:
            errorMessage = '请先登录后再进行认领申请'
            break
          case 404:
            errorMessage = '物品不存在或已被删除'
            break
          case 500:
            errorMessage = '服务器错误，请稍后重试'
            break
          default:
            errorMessage = data.message || '网络错误，请检查网络连接'
        }
      }
      
      ElMessage.error(errorMessage)
    }
  }
}

function onSendComment() {
  if (!commentText.value.trim()) return
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再评论！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }
  emit('comment', commentText.value)
  ElMessage.success('评论已发送')
  commentText.value = ''
}

function previewImage(img) {
  // 这里可以实现图片预览功能
  window.open(img, '_blank')
}

// 获取认领者信息的方法
function getClaimedUserName() {
  const claimedBy = props.post.claimedBy || props.post.claimed_by
  if (typeof claimedBy === 'object' && claimedBy !== null) {
    return claimedBy.name || claimedBy.username || '认领者'
  }
  return '认领者'
}

function getClaimedUserAvatar() {
  const claimedBy = props.post.claimedBy || props.post.claimed_by
  if (typeof claimedBy === 'object' && claimedBy !== null) {
    return getAvatarUrl(claimedBy.avatar)
  }
  return null
}

function handleClaimedUserClick() {
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再发送私信！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }

  const claimedBy = props.post.claimedBy || props.post.claimed_by
  if (!claimedBy || typeof claimedBy !== 'object') {
    ElMessage.warning('无法获取认领者信息')
    return
  }

  // 检查是否是自己
  if (claimedBy.id === userStore.userInfo?.id) {
    ElMessage.info('这是您认领的物品')
    return
  }

  // 构造认领者信息
  const claimedUser = {
    id: claimedBy.id,
    name: claimedBy.name || claimedBy.username || '认领者',
    avatar: claimedBy.avatar
  }

  // 构造物品信息
  const relatedItem = {
    id: props.post.id,
    name: props.post.title || props.post.name,
    description: props.post.desc || props.post.description
  }

  // 显示私信弹窗
  sendMessageDialog.user = claimedUser
  sendMessageDialog.relatedItem = relatedItem
  sendMessageDialog.show = true
}

// 当帖子切换时清空评论输入框
watch(() => props.post.id, () => { 
  commentText.value = '' 
})

const markerStyle = computed(() => {
  if (!props.post.locationCoord) return {}
  const [x, y] = props.post.locationCoord
  return {
    left: x + 'px',
    top: y + 'px'
  }
})

// 处理用户头像点击
function handleAvatarClick() {
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再发送私信！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }

  // 检查是否是自己的帖子
  if (props.post.user?.id === userStore.userInfo?.id || props.post.userId === userStore.userInfo?.id) {
    ElMessage.info('不能给自己发送私信')
    return
  }

  // 构造用户信息
  const postUser = {
    id: props.post.user?.id || props.post.userId,
    name: getUserDisplayName(props.post),
    avatar: props.post.user?.avatar || props.post.avatar
  }

  // 构造物品信息
  const relatedItem = {
    id: props.post.id,
    name: props.post.title || props.post.name,
    description: props.post.desc || props.post.description
  }

  // 显示私信弹窗
  sendMessageDialog.user = postUser
  sendMessageDialog.relatedItem = relatedItem
  sendMessageDialog.show = true
}

// 处理评论区用户头像点击
function handleCommentAvatarClick(comment) {
  if (!props.isLogin) {
    ElMessageBox.confirm(
      '您还未登录，请先登录后再发送私信！',
      '未登录',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        distinguishCancelAndClose: true
      }
    ).then(() => {
      emit('require-login')
    }).catch(() => {
      // 用户点击关闭或取消，不做任何处理
    })
    return
  }

  // 检查是否是自己
  if (comment.author_id === userStore.userInfo?.id) {
    ElMessage.info('不能给自己发送私信')
    return
  }

  // 构造用户信息
  const commentUser = {
    id: comment.author_id,
    name: comment.nickname,
    avatar: comment.avatar
  }

  // 构造物品信息
  const relatedItem = {
    id: props.post.id,
    name: props.post.title || props.post.name,
    description: props.post.desc || props.post.description
  }

  // 显示私信弹窗
  sendMessageDialog.user = commentUser
  sendMessageDialog.relatedItem = relatedItem
  sendMessageDialog.show = true
}

// 处理私信发送成功
function handleMessageSent(data) {
  ElMessage.success(`已向 ${data.user.name} 发送私信`)
}
</script>

<style scoped>
.post-detail {
  background: var(--bg-white);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-light);
  overflow: hidden;
}

.post-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--border-light);
  background: linear-gradient(135deg, var(--bg-gray), var(--bg-white));
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.user-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.post-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.post-time {
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

.post-type-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.post-type-badge.lost {
  background: rgba(245, 108, 108, 0.1);
  color: var(--status-lost);
  border: 1px solid rgba(245, 108, 108, 0.2);
}

.post-type-badge.found {
  background: rgba(103, 194, 58, 0.1);
  color: var(--status-found);
  border: 1px solid rgba(103, 194, 58, 0.2);
}

.post-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.claimed-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.claimed-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 8px;
}

.claimed-by {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.claimed-user-avatar {
  cursor: pointer;
  transition: all 0.2s ease;
}

.claimed-user-avatar:hover {
  transform: scale(1.1);
}

.claimed-user-name {
  font-weight: 500;
  color: #409eff;
  cursor: pointer;
  transition: color 0.2s ease;
}

.claimed-user-name:hover {
  color: #66b1ff;
}

.claimed-contact-tip {
  font-size: 12px;
  color: #909399;
  font-style: italic;
}

.claimed-time {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.contact-btn,
.claim-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-lg);
  font-weight: 500;
  border-radius: var(--radius-lg);
  flex: 1;
  min-width: 140px;
  justify-content: center;
}

.post-content {
  padding: var(--spacing-xl);
}

.post-title {
  margin: 0 0 var(--spacing-xl) 0;
  font-size: var(--font-size-title);
  font-weight: 700;
  color: var(--text-primary);
  line-height: var(--line-height-tight);
}

.content-section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.post-description {
  margin: 0;
  font-size: var(--font-size-md);
  line-height: var(--line-height-relaxed);
  color: var(--text-secondary);
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
}

.image-item {
  aspect-ratio: 4/3;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.image-item:hover {
  transform: scale(1.02);
}

.image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.location-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.location-text {
  font-size: var(--font-size-md);
  font-weight: 500;
  color: var(--text-primary);
  text-align: center;
}

.map-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 300px;
  margin: 0 auto;
  background: var(--bg-gray);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-light);
}

.map-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.map-marker {
  position: absolute;
  width: 12px;
  height: 12px;
  background: #ff4d4f;
  border: 2px solid white;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 8px rgba(255, 77, 79, 0.6);
  z-index: 10;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(255, 77, 79, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0);
  }
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.comment-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-gray);
  border-radius: var(--radius-lg);
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}

.comment-author {
  font-weight: 600;
  color: var(--text-primary);
}

.comment-time {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.comment-text {
  margin: 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
  color: var(--text-secondary);
}

.empty-comments {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-xl);
  color: var(--text-muted);
  text-align: center;
}

.empty-comments svg {
  margin-bottom: var(--spacing-md);
  color: var(--text-light);
}

.empty-comments p {
  margin: 0;
  font-size: var(--font-size-sm);
}

.comment-input {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.send-btn {
  align-self: flex-end;
  padding: var(--spacing-sm) var(--spacing-lg);
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .post-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
  }
  
  .post-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .contact-btn,
  .claim-btn {
    width: 100%;
    min-width: unset;
  }
  
  .post-content {
    padding: var(--spacing-lg);
  }
  
  .post-title {
    font-size: var(--font-size-xl);
  }
  
  .image-gallery {
    grid-template-columns: 1fr;
  }
  
  .map-container {
    height: 200px;
  }
}

/* 私信功能相关样式 */
.user-name.clickable {
  cursor: pointer;
  transition: color 0.2s ease;
}

.user-name.clickable:hover {
  color: var(--brand-blue);
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.comment-avatar {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.comment-avatar:hover {
  transform: scale(1.1);
}

.comment-author.clickable {
  cursor: pointer;
  transition: color 0.2s ease;
}

.comment-author.clickable:hover {
  color: var(--brand-blue);
}
</style> 