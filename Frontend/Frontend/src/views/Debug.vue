<template>
  <div style="padding: 20px; font-family: monospace;">
    <h1>🔍 登录状态诊断</h1>
    
    <div style="background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px;">
      <h3>📊 用户Store状态</h3>
      <p><strong>Token存在:</strong> {{ hasToken ? '✅ 是' : '❌ 否' }}</p>
      <p><strong>Token值:</strong> {{ tokenDisplay }}</p>
      <p><strong>用户信息存在:</strong> {{ hasUserInfo ? '✅ 是' : '❌ 否' }}</p>
      <p><strong>用户信息:</strong> {{ userInfoDisplay }}</p>
      <p><strong>用户ID存在:</strong> {{ hasUserId ? '✅ 是' : '❌ 否' }}</p>
      <p><strong>isLogin状态:</strong> {{ isLoginValue ? '✅ 已登录' : '❌ 未登录' }}</p>
    </div>

    <div style="background: #e8f4fd; padding: 15px; margin: 10px 0; border-radius: 5px;">
      <h3>🔧 操作按钮</h3>
      <button @click="refreshUserInfo" style="margin: 5px; padding: 8px 15px;">刷新用户信息</button>
      <button @click="testMessagesRoute" style="margin: 5px; padding: 8px 15px;">测试消息路由</button>
      <button @click="checkLocalStorage" style="margin: 5px; padding: 8px 15px;">检查localStorage</button>
    </div>

    <div style="background: #fff2e8; padding: 15px; margin: 10px 0; border-radius: 5px;">
      <h3>📝 日志输出</h3>
      <div v-for="(log, index) in logs" :key="index" style="margin: 5px 0;">
        {{ log }}
      </div>
    </div>

    <div style="background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px;">
      <h3>🎯 消息按钮可见性测试</h3>
      <p><strong>消息按钮应该显示:</strong> {{ shouldShowMessageButton ? '✅ 是' : '❌ 否' }}</p>
      <div v-if="shouldShowMessageButton">
        <router-link to="/messages" style="display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 10px 0;">
          🔗 测试消息链接
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const logs = ref([])

// 计算属性
const hasToken = computed(() => !!userStore.token)
const hasUserInfo = computed(() => !!userStore.userInfo)
const hasUserId = computed(() => !!(userStore.userInfo && userStore.userInfo.id))
const isLoginValue = computed(() => userStore.isLogin)
const shouldShowMessageButton = computed(() => isLoginValue.value)

const tokenDisplay = computed(() => {
  if (!userStore.token) return '无'
  return userStore.token.substring(0, 20) + '...'
})

const userInfoDisplay = computed(() => {
  if (!userStore.userInfo) return '无'
  return JSON.stringify(userStore.userInfo, null, 2)
})

function addLog(message) {
  const timestamp = new Date().toLocaleTimeString()
  logs.value.push(`[${timestamp}] ${message}`)
}

async function refreshUserInfo() {
  addLog('开始刷新用户信息...')
  try {
    const result = await userStore.refreshUserInfo()
    addLog(`用户信息刷新结果: ${result}`)
  } catch (error) {
    addLog(`用户信息刷新失败: ${error.message}`)
  }
}

function testMessagesRoute() {
  addLog('尝试跳转到消息页面...')
  router.push('/messages').then(() => {
    addLog('路由跳转成功')
  }).catch(error => {
    addLog(`路由跳转失败: ${error.message}`)
  })
}

function checkLocalStorage() {
  addLog('检查localStorage...')
  const token = localStorage.getItem('token')
  addLog(`localStorage中的token: ${token ? '存在' : '不存在'}`)
  if (token) {
    addLog(`Token值: ${token.substring(0, 20)}...`)
  }
}

onMounted(() => {
  addLog('诊断页面加载完成')
  addLog(`当前路由: ${router.currentRoute.value.path}`)
  
  // 自动检查localStorage
  checkLocalStorage()
})
</script> 