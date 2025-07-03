<template>
  <div class="register-form">
    <el-form 
      ref="formRef" 
      :model="form" 
      :rules="rules" 
      @submit.prevent="handleSubmit"
      class="form"
    >
      <div class="form-header">
        <h2>创建账户</h2>
        <p>加入我们的校园失物招领平台</p>
      </div>
      
      <el-form-item prop="realname">
        <el-input 
          v-model="form.realname" 
          placeholder="请输入姓名"
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="studentId">
        <el-input 
          v-model="form.studentId" 
          placeholder="请输入学号"
          size="large"
          prefix-icon="User"
        />
      </el-form-item>
      
      <el-form-item prop="email">
        <el-input 
          v-model="form.email" 
          placeholder="请输入邮箱"
          size="large"
          prefix-icon="Message"
        />
      </el-form-item>
      
      <el-form-item prop="password">
        <el-input 
          v-model="form.password" 
          type="password" 
          placeholder="请输入密码"
          size="large"
          prefix-icon="Lock"
          show-password
        />
      </el-form-item>
      <el-form-item prop="confirmPassword">
        <el-input 
          v-model="form.confirmPassword" 
          type="password" 
          placeholder="确认密码"
          size="large"
          prefix-icon="Lock"
          show-password
        />
      </el-form-item>
      
      <div class="form-options">
        <el-checkbox v-model="agreeTerms">
          我已阅读并同意 <a href="#" class="terms-link">服务条款</a> 和 <a href="#" class="terms-link">隐私政策</a>
        </el-checkbox>
      </div>
      
      <el-form-item>
        <el-button 
          type="primary" 
          size="large" 
          class="submit-btn"
          :loading="loading"
          :disabled="!agreeTerms"
          @click="handleSubmit"
        >
          注册
        </el-button>
      </el-form-item>
      
      <div class="form-footer">
        <p>已有账户？ <a href="#" @click="$emit('switchToLogin')">立即登录</a></p>
      </div>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['success', 'switchToLogin'])

const formRef = ref()
const loading = ref(false)
const agreeTerms = ref(false)

const form = reactive({
  realname: '',
  studentId: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  realname: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{6,20}$/, message: '学号应为6-20位数字', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

async function handleSubmit() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 模拟注册请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('注册成功！')
    emit('success')
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error('注册失败，请检查输入信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-form {
  padding: var(--spacing-lg);
}

.form-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.form-header h2 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
}

.form-header p {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-options {
  margin-bottom: var(--spacing-md);
}

.terms-link {
  color: var(--brand-blue);
  text-decoration: none;
  transition: color 0.2s ease;
}

.terms-link:hover {
  color: var(--brand-blue-light);
}

.submit-btn {
  width: 100%;
  padding: var(--spacing-md);
  font-weight: 500;
  border-radius: var(--radius-lg);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  text-align: center;
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
}

.form-footer p {
  margin: 0;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.form-footer a {
  color: var(--brand-blue);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.form-footer a:hover {
  color: var(--brand-blue-light);
}
</style> 