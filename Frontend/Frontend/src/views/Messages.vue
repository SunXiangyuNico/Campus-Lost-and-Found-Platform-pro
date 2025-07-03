<template>
  <div class="messages-container">
    <div class="messages-header">
      <div class="header-left">
        <h1>我的消息</h1>
      </div>
      <div class="header-right">
        <el-button type="primary" icon="house" @click="goToHome">
          返回首页
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="messages-tabs">
      <!-- 系统通知标签页 -->
      <el-tab-pane name="notifications">
        <template #label>
          <span class="tab-label">
            系统通知
            <el-badge v-if="unreadCounts.notifications > 0" :value="unreadCounts.notifications" class="tab-badge"/>
          </span>
        </template>
        
        <div class="tab-content">
          <div v-if="loading.notifications" class="loading-container" v-loading="loading.notifications" element-loading-text="加载中...">
            <div style="height: 100px;"></div>
          </div>
          
          <div v-else-if="notifications.length === 0" class="empty-state">
            <el-empty description="暂无系统通知" />
          </div>
          
          <div v-else class="notification-list">
            <div
              v-for="notification in notifications"
              :key="notification.id"
              class="notification-item"
              :class="{ 'unread': !notification.isRead, 'clickable': !!notification.itemId }"
              @click="markNotificationAsRead(notification)"
            >
              <div class="notification-content">
                <div class="notification-text">
                  {{ notification.content }}
                  <span v-if="notification.itemId" class="click-hint">（点击查看帖子详情）</span>
                </div>
                <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
              </div>
              <div v-if="!notification.isRead" class="unread-dot"></div>
              <div v-if="notification.itemId" class="jump-icon">→</div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 待处理帖子标签页 -->
      <el-tab-pane name="claims">
        <template #label>
          <span class="tab-label">
            待处理帖子
            <el-badge v-if="unreadCounts.claims > 0" :value="unreadCounts.claims" class="tab-badge"/>
          </span>
        </template>
        
        <div class="tab-content">
          <div v-if="loading.claims" class="loading-container" v-loading="loading.claims" element-loading-text="加载中...">
            <div style="height: 100px;"></div>
          </div>
          
          <div v-else-if="claimRequests.length === 0" class="empty-state">
            <el-empty description="暂无认领申请" />
          </div>
          
          <div v-else class="claim-list">
                      <div
            v-for="claim in claimRequests"
            :key="claim.id"
            class="claim-item"
            :class="{ 'unread': !claim.isRead }"
            @click="markClaimAsRead(claim)"
          >
              <div class="claim-content">
                <div class="claim-header">
                  <div class="claim-requester">
                    <strong>{{ claim.requester?.name || '未知用户' }}</strong>
                    <span class="claim-action">申请认领</span>
                    <strong>{{ claim.item?.name || '未知物品' }}</strong>
                  </div>
                  <div class="claim-status">
                    <el-tag 
                      v-if="claim.status === 'pending'" 
                      type="warning" 
                      size="small"
                    >
                      待处理
                    </el-tag>
                    <el-tag 
                      v-else-if="claim.status === 'approved'" 
                      type="success" 
                      size="small"
                    >
                      已批准
                    </el-tag>
                    <el-tag 
                      v-else-if="claim.status === 'rejected'" 
                      type="danger" 
                      size="small"
                    >
                      已拒绝
                    </el-tag>
                  </div>
                </div>
                <div class="claim-text">{{ claim.content }}</div>
                <div class="claim-time">{{ formatTime(claim.timestamp) }}</div>
                
                <div v-if="claim.status === 'pending'" class="claim-actions">
                  <el-button 
                    type="success" 
                    size="small" 
                    @click="handleClaimResponse(claim.id, 'approved')"
                  >
                    批准
                  </el-button>
                  <el-button 
                    type="danger" 
                    size="small" 
                    @click="handleClaimResponse(claim.id, 'rejected')"
                  >
                    拒绝
                  </el-button>
                </div>
              </div>
              <div v-if="!claim.isRead" class="unread-dot"></div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 私信列表标签页 -->
      <el-tab-pane name="conversations">
        <template #label>
          <span class="tab-label">
            私信列表
            <el-badge v-if="unreadCounts.conversations > 0" :value="unreadCounts.conversations" class="tab-badge"/>
          </span>
        </template>
        
        <div class="tab-content">
          <div v-if="loading.conversations" class="loading-container" v-loading="loading.conversations" element-loading-text="加载中...">
            <div style="height: 100px;"></div>
          </div>
          
          <div v-else-if="conversations.length === 0" class="empty-state">
            <el-empty description="暂无私信" />
          </div>
          
          <div v-else class="conversation-list">
            <div
              v-for="conversation in conversations"
              :key="conversation.otherUserId"
              class="conversation-item"
              :class="{ 'unread': conversation.unreadCount > 0 }"
              @click="openConversation(conversation)"
            >
              <div class="conversation-avatar">
                <el-avatar :src="conversation.otherUserAvatar">
                  {{ conversation.otherUserName?.charAt(0) || '用' }}
                </el-avatar>
              </div>
              <div class="conversation-content">
                <div class="conversation-header">
                  <span class="other-user-name">{{ conversation.otherUserName || '未知用户' }}</span>
                  <span class="last-time">{{ formatTime(conversation.lastMessageTime) }}</span>
                </div>
                <div class="last-message">{{ conversation.lastMessage }}</div>
              </div>
              <div v-if="conversation.unreadCount > 0" class="unread-badge">
                <el-badge :value="conversation.unreadCount" />
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 私信对话弹窗 -->
    <el-dialog 
      v-model="showConversationDialog" 
      :title="`与 ${currentConversation?.otherUserName || '用户'} 的对话`"
      width="600px"
      class="conversation-dialog"
    >
      <div class="conversation-messages" ref="messagesContainer">
        <div
          v-for="message in currentMessages"
          :key="message.id"
          class="message-item"
          :class="{ 'own-message': message.sender === 'me' }"
        >
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>
      
      <div class="message-input-area">
        <el-input
          v-model="newMessage"
          type="textarea"
          :rows="3"
          placeholder="输入消息..."
          @keydown.ctrl.enter="sendMessage"
        />
        <div class="input-actions">
          <span class="input-tip">Ctrl + Enter 发送</span>
          <el-button type="primary" @click="sendMessage" :disabled="!newMessage.trim()">
            发送
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'
import { 
  getSystemNotifications, 
  getClaimRequests, 
  getConversations, 
  getMessagesWithUser,
  handleClaimResponse as apiHandleClaimResponse,
  sendPrivateMessage,
  markMessagesAsRead,
  getUnreadCount
} from '../api/messages'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { formatTime } from '../utils/index.js'

export default {
  name: 'Messages',
  components: {
  },
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    
    // 返回首页方法
    const goToHome = () => {
      router.push('/')
    }
    
    // 响应式数据
    const activeTab = ref('notifications')
    const notifications = ref([])
    const claimRequests = ref([])
    const conversations = ref([])
    const currentMessages = ref([])
    const currentConversation = ref(null)
    const showConversationDialog = ref(false)
    const newMessage = ref('')
    const messagesContainer = ref(null)
    
    const loading = reactive({
      notifications: false,
      claims: false,
      conversations: false
    })
    
    const unreadCounts = reactive({
      notifications: 0,
      claims: 0,
      conversations: 0
    })



    // 加载系统通知
    const loadNotifications = async () => {
      loading.notifications = true
      try {
        const response = await getSystemNotifications()
        // 后端直接返回数组，统一数据格式
        notifications.value = Array.isArray(response) ? response : response.data || []
        unreadCounts.notifications = notifications.value.filter(n => !n.isRead).length
      } catch (error) {
        console.error('加载系统通知失败:', error)
        ElMessage.error('加载系统通知失败')
      } finally {
        loading.notifications = false
      }
    }

    // 加载认领申请
    const loadClaimRequests = async () => {
      loading.claims = true
      try {
        const response = await getClaimRequests()
        // 后端直接返回数组，统一数据格式
        claimRequests.value = Array.isArray(response) ? response : response.data || []
        unreadCounts.claims = claimRequests.value.filter(c => !c.isRead).length
      } catch (error) {
        console.error('加载认领申请失败:', error)
        
        // 根据错误类型提供更详细的提示
        let errorMessage = '加载认领申请失败'
        if (error.response) {
          const status = error.response.status
          switch (status) {
            case 401:
              errorMessage = '登录已过期，请重新登录'
              break
            case 403:
              errorMessage = '没有权限访问认领申请'
              break
            case 500:
              errorMessage = '服务器错误，请稍后重试'
              break
            default:
              errorMessage = '网络错误，请检查网络连接'
          }
        }
        
        ElMessage.error(errorMessage)
      } finally {
        loading.claims = false
      }
    }

    // 加载私信对话列表
    const loadConversations = async () => {
      loading.conversations = true
      try {
        const response = await getConversations()
        // 后端直接返回数组，统一数据格式
        const conversationsData = Array.isArray(response) ? response : response.data || []
        
        // 转换数据格式以匹配模板中使用的字段名
        conversations.value = conversationsData.map(conv => ({
          otherUserId: conv.withUser?.id,
          otherUserName: conv.withUser?.name || conv.withUser?.username,
          otherUserAvatar: conv.withUser?.avatar,
          lastMessage: conv.lastMessage,
          lastMessageTime: conv.timestamp,
          unreadCount: conv.unreadCount || 0,
          item: conv.item
        }))
        
        unreadCounts.conversations = conversations.value.reduce((sum, conv) => sum + (conv.unreadCount || 0), 0)
      } catch (error) {
        console.error('加载私信列表失败:', error)
        ElMessage.error('加载私信列表失败')
      } finally {
        loading.conversations = false
      }
    }

    // 标记通知为已读并跳转到相关帖子
    const markNotificationAsRead = async (notification) => {
      try {
        // 标记为已读
        if (!notification.isRead) {
          await markMessagesAsRead([notification.id], 'system_notification')
          notification.isRead = true
          unreadCounts.notifications--
          
          // 立即通知导航栏更新红点
          window.dispatchEvent(new CustomEvent('refresh-unread-count'))
        }
        
        // 如果通知有关联的帖子ID，跳转到帖子详情
        if (notification.itemId) {
          router.push({
            path: '/',
            query: { selected: notification.itemId }
          })
        }
      } catch (error) {
        console.error('处理通知失败:', error)
        ElMessage.error('处理通知失败')
      }
    }

    // 标记认领申请为已读
    const markClaimAsRead = async (claim) => {
      if (claim.isRead) return
      
      try {
        await markMessagesAsRead([claim.id], 'claim_request')
        claim.isRead = true
        unreadCounts.claims--
        
        // 立即通知导航栏更新红点
        window.dispatchEvent(new CustomEvent('refresh-unread-count'))
      } catch (error) {
        console.error('标记认领申请已读失败:', error)
      }
    }

    // 处理认领申请响应
    const handleClaimResponse = async (claimId, response) => {
      try {
        await ElMessageBox.confirm(
          `确定要${response === 'approved' ? '批准' : '拒绝'}这个认领申请吗？`,
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await apiHandleClaimResponse(claimId, response)
        ElMessage.success(`已${response === 'approved' ? '批准' : '拒绝'}认领申请`)
        
        // 标记该认领申请消息为已读
        await markMessagesAsRead([claimId], 'claim_request')
        
        // 更新本地数据
        const claim = claimRequests.value.find(c => c.id === claimId)
        if (claim) {
          claim.status = response
          claim.isRead = true
          unreadCounts.claims = Math.max(0, unreadCounts.claims - 1)
        }
        
        // 立即通知导航栏更新红点
        window.dispatchEvent(new CustomEvent('refresh-unread-count'))
        
        // 如果批准了认领申请，触发全局事件通知其他组件更新状态
        if (response === 'approved') {
          window.dispatchEvent(new CustomEvent('claim-status-updated'))
        }
      } catch (error) {
        if (error !== 'cancel') {
          console.error('处理认领申请失败:', error)
          ElMessage.error('处理认领申请失败')
        }
      }
    }

    // 打开私信对话
    const openConversation = async (conversation) => {
      currentConversation.value = conversation
      showConversationDialog.value = true
      
      try {
        const response = await getMessagesWithUser(conversation.otherUserId)
        currentMessages.value = response.messages || []
        
        // 标记消息为已读
        if (conversation.unreadCount > 0) {
          const originalUnreadCount = conversation.unreadCount
          await markMessagesAsRead([], 'private_message', conversation.otherUserId)
          conversation.unreadCount = 0
          unreadCounts.conversations = Math.max(0, unreadCounts.conversations - originalUnreadCount)
          
          // 立即通知导航栏更新红点
          window.dispatchEvent(new CustomEvent('refresh-unread-count'))
        }
        
        // 滚动到底部
        await nextTick()
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      } catch (error) {
        console.error('加载对话消息失败:', error)
        ElMessage.error('加载对话消息失败')
      }
    }

    // 发送私信
    const sendMessage = async () => {
      if (!newMessage.value.trim()) return
      
      try {
        const response = await sendPrivateMessage(
          currentConversation.value.otherUserId,
          newMessage.value.trim()
        )
        
        // 添加新消息到列表
        currentMessages.value.push(response)
        newMessage.value = ''
        
        // 滚动到底部
        await nextTick()
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
        
        // 更新对话列表中的最后一条消息
        const conversation = conversations.value.find(c => c.otherUserId === currentConversation.value.otherUserId)
        if (conversation) {
          conversation.lastMessage = response.content
          conversation.lastMessageTime = response.timestamp
          
          // 将当前对话移到列表顶部
          const index = conversations.value.indexOf(conversation)
          if (index > 0) {
            conversations.value.splice(index, 1)
            conversations.value.unshift(conversation)
          }
        }
      } catch (error) {
        console.error('发送消息失败:', error)
        ElMessage.error('发送消息失败')
      }
      
      // 触发全局消息更新事件，通知其他组件
      window.dispatchEvent(new CustomEvent('message-updated'))
    }

    // 刷新所有消息数据
    const refreshAllMessages = () => {
      loadNotifications()
      loadClaimRequests()
      loadConversations()
    }

    // 定期刷新消息（30秒）
    let refreshInterval = null

    // 初始化数据
    onMounted(() => {
      loadNotifications()
      loadClaimRequests()
      loadConversations()
      
      // 设置定期刷新
      refreshInterval = setInterval(refreshAllMessages, 30000)
      
      // 监听全局消息更新事件
      window.addEventListener('message-updated', refreshAllMessages)
    })
    
    // 清理定时器
    onBeforeUnmount(() => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }
      window.removeEventListener('message-updated', refreshAllMessages)
    })

    return {
      activeTab,
      notifications,
      claimRequests,
      conversations,
      currentMessages,
      currentConversation,
      showConversationDialog,
      newMessage,
      messagesContainer,
      loading,
      unreadCounts,
      formatTime,
      goToHome,
      markNotificationAsRead,
      markClaimAsRead,
      handleClaimResponse,
      openConversation,
      sendMessage,
      refreshAllMessages
    }
  }
}
</script>

<style scoped>
.messages-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.messages-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  flex: 1;
}

.header-right {
  display: flex;
  align-items: center;
}

.messages-header h1 {
  color: #333;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.messages-tabs {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-badge {
  margin-left: 4px;
}

.tab-content {
  padding: 20px;
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 系统通知样式 */
.notification-list {
  space-y: 12px;
}

.notification-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.notification-item:hover {
  background-color: #f5f7fa;
  border-color: #409eff;
}

.notification-item.unread {
  background-color: #f0f9ff;
  border-color: #409eff;
}

.notification-item.clickable {
  cursor: pointer;
}

.notification-item.clickable:hover {
  background-color: #e6f7ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.notification-content {
  flex: 1;
}

.notification-text {
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}

.notification-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.unread-dot {
  width: 8px;
  height: 8px;
  background-color: #f56c6c;
  border-radius: 50%;
  margin-left: 12px;
}

.click-hint {
  color: #409eff;
  font-size: 12px;
  font-style: italic;
}

.jump-icon {
  color: #409eff;
  font-size: 18px;
  font-weight: bold;
  margin-left: 8px;
  transition: transform 0.2s;
}

.notification-item.clickable:hover .jump-icon {
  transform: translateX(3px);
}

/* 认领申请样式 */
.claim-list {
  space-y: 12px;
}

.claim-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.claim-item.unread {
  background-color: #f0f9ff;
  border-color: #409eff;
}

.claim-content {
  flex: 1;
}

  .claim-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .claim-requester {
    font-weight: bold;
    color: #333;
    display: flex;
    align-items: center;
    flex: 1;
  }
  
  .claim-action {
    font-size: 12px;
    color: #999;
    margin: 0 8px;
    font-weight: normal;
  }
  
  .claim-status {
    display: flex;
    justify-content: flex-end;
  }

.claim-text {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
}

.claim-time {
  font-size: 12px;
  color: #999;
}

.claim-actions {
  display: flex;
  gap: 8px;
}

/* 私信对话样式 */
.conversation-list {
  space-y: 12px;
}

.conversation-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.conversation-item:hover {
  background-color: #f5f7fa;
  border-color: #409eff;
}

.conversation-item.unread {
  background-color: #f0f9ff;
  border-color: #409eff;
}

.conversation-avatar {
  margin-right: 12px;
}

.conversation-content {
  flex: 1;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.other-user-name {
  font-weight: bold;
  color: #333;
}

.last-time {
  font-size: 12px;
  color: #999;
}

.last-message {
  font-size: 14px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.unread-badge {
  margin-left: 12px;
}

/* 对话弹窗样式 */
.conversation-dialog {
  .el-dialog__body {
    padding: 0;
  }
}

.conversation-messages {
  max-height: 400px;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.message-item {
  margin-bottom: 16px;
  display: flex;
}

.message-item.own-message {
  justify-content: flex-end;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 12px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.own-message .message-content {
  background-color: #409eff;
  color: white;
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 12px;
  margin-top: 4px;
  opacity: 0.7;
}

.message-input-area {
  padding: 20px;
  border-top: 1px solid #e4e7ed;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.input-tip {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .messages-container {
    padding: 10px;
  }
  
  .tab-content {
    padding: 10px;
  }
  
  .conversation-dialog {
    width: 95% !important;
  }
  
  .message-content {
    max-width: 85%;
  }
}
</style> 