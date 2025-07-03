import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// --- 全局 Axios 配置 ---
// 1. 设置基础 URL
axios.defaults.baseURL = 'http://localhost:5000'

// 2. 设置请求拦截器，为每个请求自动附加 Token
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 应用挂载
app.mount('#app')

// 应用挂载后初始化用户状态
import { useUserStore } from './store/user'

// 延迟初始化，确保DOM已经挂载
setTimeout(async () => {
  const userStore = useUserStore()
  
  console.log('=== 应用启动，初始化用户状态 ===')
  console.log('localStorage中的token:', localStorage.getItem('token') ? '存在' : '不存在')
  console.log('store中的token:', userStore.token ? '存在' : '不存在')
  
  if (userStore.token) {
    console.log('发现token，尝试获取用户信息...')
    try {
      const refreshResult = await userStore.refreshUserInfo()
      console.log('用户信息初始化结果:', refreshResult)
      if (refreshResult) {
        console.log('用户信息加载成功:', userStore.userInfo)
      } else {
        console.log('用户信息加载失败，token可能已过期')
      }
    } catch (error) {
      console.error('初始化用户信息时发生错误:', error)
      console.log('清除无效的登录状态')
      userStore.logout()
    }
  } else {
    console.log('没有token，用户未登录')
  }
}, 100) 