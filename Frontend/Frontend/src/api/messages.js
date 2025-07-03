import axios from 'axios'

// 发送私信
export const sendPrivateMessage = async (recipientId, content, itemId = null) => {
  const response = await axios.post('/api/messages', {
    recipientId,
    content,
    itemId
  })
  return response.data
}

// 发送认领申请
export const sendClaimRequest = async (itemId, content) => {
  const response = await axios.post('/api/messages/claim-request', {
    itemId,
    content
  })
  return response.data
}

// 处理认领申请响应
export const handleClaimResponse = async (claimRequestId, response, content) => {
  const res = await axios.post('/api/messages/claim-response', {
    claimRequestId,
    response,
    content
  })
  return res.data
}

// 获取对话列表
export const getConversations = async () => {
  const response = await axios.get('/api/messages/conversations')
  return response.data
}

// 获取与指定用户的消息历史
export const getMessagesWithUser = async (userId) => {
  const response = await axios.get(`/api/messages/conversations/${userId}`)
  return response.data
}

// 获取系统通知
export const getSystemNotifications = async () => {
  const response = await axios.get('/api/messages/notifications')
  return response.data
}

// 获取认领申请列表
export const getClaimRequests = async () => {
  const response = await axios.get('/api/messages/claim-requests')
  return response.data
}

// 获取未读消息数量
export const getUnreadCount = async () => {
  const response = await axios.get('/api/messages/unread-count')
  return response.data
}

// 标记消息为已读
export const markMessagesAsRead = async (messageIds, messageType, otherUserId = null) => {
  const data = {
    messageIds,
    messageType
  }
  
  // 如果提供了otherUserId，添加到请求数据中
  if (otherUserId) {
    data.otherUserId = otherUserId
  }
  
  const response = await axios.post('/api/messages/mark-read', data)
  return response.data
} 