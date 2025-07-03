<template>
  <div class="welcome-container">
    <div class="background-overlay"></div>
    
    <div class="welcome-content">
      <div class="welcome-header">
        <h1 class="welcome-title">校园失物招领平台</h1>
        <p class="welcome-subtitle">找回遗失的物品，传递温暖的心意</p>
      </div>
      
      <div class="welcome-actions">
        <el-button 
          type="primary" 
          size="large" 
          class="action-button login-btn"
          @click="showLoginDialog = true"
        >
          登录
        </el-button>
        
        <el-button 
          type="default" 
          size="large" 
          class="action-button register-btn"
          @click="showRegisterDialog = true"
        >
          注册
        </el-button>
        
        <el-button 
          type="text" 
          size="large" 
          class="action-button guest-btn"
          @click="guestLogin"
        >
          进入/游客访问
        </el-button>
      </div>
      

    </div>
    
    <!-- 登录对话框 -->
    <Login 
      v-model:visible="showLoginDialog"
      @switch-register="switchToRegister"
      @login-success="handleLoginSuccess"
    />
    
    <!-- 注册对话框 -->
    <Register 
      v-model:visible="showRegisterDialog"
      @switch-login="switchToLogin"
      @register-success="handleRegisterSuccess"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Login from './Login.vue'
import Register from './Register.vue'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const showLoginDialog = ref(false)
const showRegisterDialog = ref(false)

// 切换到注册对话框
function switchToRegister() {
  showLoginDialog.value = false
  showRegisterDialog.value = true
}

// 切换到登录对话框
function switchToLogin() {
  showRegisterDialog.value = false
  showLoginDialog.value = true
}

// 游客登录 - 直接进入主页面
function guestLogin() {
  router.push('/home')
}

// 处理登录成功事件
function handleLoginSuccess() {
  router.push('/home')
}

// 处理注册成功事件
function handleRegisterSuccess() {
  router.push('/home')
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(2px);
}

.welcome-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  max-width: 800px;
  padding: 40px 20px;
}

.welcome-header {
  margin-bottom: 40px;
}

.welcome-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 16px;
  color: #ffffff;
  text-shadow: 
    2px 2px 4px rgba(0, 0, 0, 0.8),
    0 0 20px rgba(255, 255, 255, 0.3);
  letter-spacing: 2px;
}

.welcome-subtitle {
  font-size: 1.25rem;
  font-weight: 400;
  opacity: 0.9;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  margin-bottom: 0;
}

.welcome-actions {
  display: flex;
  gap: 24px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
  max-width: 480px;
  margin-left: auto;
  margin-right: auto;
}

.action-button {
  width: 140px;
  height: 52px;
  font-size: 17px;
  font-weight: 600;
  border-radius: 26px;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  border: none;
}

.login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.login-btn:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.register-btn {
  background: rgba(255, 255, 255, 0.95);
  color: #444;
  border: 2px solid rgba(255, 255, 255, 0.6);
}

.register-btn:hover {
  background: rgba(255, 255, 255, 1);
  color: #333;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.8);
}

.guest-btn {
  color: rgba(255, 255, 255, 0.95);
  border: 2px solid rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.15);
  font-weight: 500;
}

.guest-btn:hover {
  color: white;
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.7);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 255, 255, 0.2);
}



/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-title {
    font-size: 2.5rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .welcome-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .action-button {
    width: 160px;
    height: 48px;
    font-size: 16px;
  }
  

  
  .welcome-content {
    padding: 20px 15px;
  }
}

@media (max-width: 480px) {
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 0.9rem;
  }
}
</style> 