<template>
  <el-dialog 
    v-model="show" 
    :title="`发送私信给 ${user?.name || '用户'}`"
    width="500px"
    destroy-on-close
    @close="handleClose"
  >
    <div class="send-message-form">
      <div class="user-info">
        <el-avatar :size="40" :src="getAvatarUrl(user?.avatar)">
          {{ user?.name?.[0] || 'U' }}
        </el-avatar>
        <div class="user-details">
          <div class="user-name">{{ user?.name || '未知用户' }}</div>
          <div v-if="relatedItem" class="related-item">
            关于物品：{{ relatedItem.name }}
          </div>
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="60px">
        <el-form-item label="消息" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="6"
            placeholder="输入您要发送的消息..."
            maxlength="1000"
            show-word-limit
            @keyup.ctrl.enter="handleSend"
          />
        </el-form-item>
      </el-form>

      <div class="message-tips">
        <el-alert
          title="提示"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <div class="tips-content">
              <p>• 请文明用语，友善交流</p>
              <p>• 建议在消息中说明您的需求或情况</p>
              <p>• 可以按 Ctrl + Enter 快速发送</p>
            </div>
          </template>
        </el-alert>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleSend"
          :loading="sending"
          :disabled="!form.content.trim()"
        >
          {{ sending ? '发送中...' : '发送消息' }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store/user'
import { sendPrivateMessage } from '../api/messages'
import { getAvatarUrl } from '../utils/index.js'

const userStore = useUserStore()

// Props
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  user: {
    type: Object,
    default: null
  },
  relatedItem: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:visible', 'sent'])

// 响应式数据
const show = ref(false)
const sending = ref(false)
const formRef = ref()

const form = reactive({
  content: ''
})

const rules = {
  content: [
    { required: true, message: '请输入消息内容', trigger: 'blur' },
    { min: 1, max: 1000, message: '消息长度应在 1 到 1000 个字符之间', trigger: 'blur' }
  ]
}

// 监听visible变化
watch(() => props.visible, (newVal) => {
  show.value = newVal
  if (newVal) {
    // 如果有关联物品，预填充一些内容
    if (props.relatedItem) {
      form.content = `您好，我对您发布的"${props.relatedItem.name}"感兴趣，`
    } else {
      form.content = ''
    }
  }
})

// 监听show变化
watch(show, (newVal) => {
  emit('update:visible', newVal)
})

// 方法
const handleClose = () => {
  show.value = false
  form.content = ''
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

const handleSend = async () => {
  if (!formRef.value) return
  
  // 防止重复提交
  if (sending.value) return
  
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  if (!props.user?.id) {
    ElMessage.error('用户信息无效')
    return
  }

  if (!userStore.token) {
    ElMessage.error('请先登录')
    return
  }

  sending.value = true
  
  // 显示发送状态
  const loadingMessage = ElMessage({
    message: '正在发送消息...',
    type: 'info',
    duration: 0,
    showClose: false
  })

  try {
    await sendPrivateMessage(
      props.user.id,
      form.content.trim(),
      props.relatedItem?.id
    )

    loadingMessage.close()
    ElMessage.success('消息发送成功')
    
    // 触发全局消息更新事件
    window.dispatchEvent(new CustomEvent('message-updated'))
    
    // 触发父组件的sent事件
    emit('sent', {
      user: props.user,
      content: form.content.trim(),
      relatedItem: props.relatedItem
    })

    handleClose()
  } catch (error) {
    loadingMessage.close()
    console.error('发送消息失败:', error)
    
    // 友好的错误处理
    let errorMessage = '发送消息失败'
    
    if (error.response?.status === 401) {
      errorMessage = '登录已过期，请重新登录'
    } else if (error.response?.status === 403) {
      errorMessage = '没有权限发送消息'
    } else if (error.response?.status === 404) {
      errorMessage = '接收用户不存在'
    } else if (error.response?.status === 400) {
      errorMessage = error.response?.data?.message || '请求参数有误'
    } else if (error.response?.status >= 500) {
      errorMessage = '服务器繁忙，请稍后再试'
    } else if (error.code === 'NETWORK_ERROR' || !navigator.onLine) {
      errorMessage = '网络连接失败，请检查网络后重试'
    } else if (error.message) {
      errorMessage = error.message
    }
    
    ElMessage.error(errorMessage)
  } finally {
    sending.value = false
  }
}


</script>

<style scoped>
.send-message-form {
  padding: 8px 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background-color: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #1a202c;
  margin-bottom: 4px;
}

.related-item {
  font-size: 14px;
  color: #4a5568;
}

.message-tips {
  margin-top: 16px;
}

.tips-content p {
  margin: 4px 0;
  font-size: 13px;
  color: #6b7280;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
  resize: vertical;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-alert) {
  border-radius: 6px;
}

:deep(.el-alert__content) {
  padding: 0;
}

:deep(.el-alert__title) {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
}
</style> 