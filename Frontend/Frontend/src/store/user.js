import { defineStore } from 'pinia'
import { getUserInfo, login as loginAPI } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null,
    isLoading: false,
  }),
  getters: {
    isLogin: (state) => !!(state.token && state.userInfo && state.userInfo.id)
  },
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    setUserInfo(info) {
      this.userInfo = info
    },
    async refreshUserInfo() {
      if (!this.token) {
        this.userInfo = null
        return false
      }
      
      this.isLoading = true
      try {
        const response = await getUserInfo(this.token)
        if (response.data && response.data.id) {
          this.userInfo = response.data
          return true
        } else {
          throw new Error('Invalid user data received')
        }
      } catch (error) {
        console.error('刷新用户信息失败:', error)
        if (error.response?.status === 401 || error.response?.status === 403) {
          this.logout()
        }
        this.userInfo = null
        return false
      } finally {
        this.isLoading = false
      }
    },
    async login(credentials) {
      try {
        const response = await loginAPI(credentials)
        if (response.data && response.data.token && response.data.user) {
          this.setToken(response.data.token)
          this.setUserInfo(response.data.user)
          return response
        } else {
          throw new Error('Invalid login response')
        }
      } catch (error) {
        this.logout()
        throw error
      }
    },
    logout() {
      this.token = ''
      this.userInfo = null
      this.isLoading = false
      localStorage.removeItem('token')
    },
    async checkLoginStatus() {
      if (!this.token) {
        return false
      }
      if (this.userInfo && this.userInfo.id) {
        return true
      }
      return await this.refreshUserInfo()
    }
  }
}) 