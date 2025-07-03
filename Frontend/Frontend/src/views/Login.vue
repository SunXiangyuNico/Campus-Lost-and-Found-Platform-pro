<template>
  <el-dialog :model-value="visible" @update:model-value="onDialogVisible" width="400px" :show-close="true" center title="用户登录" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="70px" size="large">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onLogin" style="width:100%">登录</el-button>
      </el-form-item>
      <el-form-item style="text-align:center; width:100%">
        <span>还没有账号？<a @click.prevent="$emit('switch-register')" style="color:#409eff;cursor:pointer">立即注册</a></span>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { login } from '../api/auth'
import { useUserStore } from '../store/user'
const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible', 'switch-register', 'login-success'])
const formRef = ref()
const form = ref({
  username: '',
  password: ''
})
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}
const userStore = useUserStore()

async function onLogin() {
  formRef.value.validate(async valid => {
    if (!valid) return
    
    try {
      const response = await login({
        username: form.value.username,
        password: form.value.password
      })
      
      // 保存token和用户信息
      userStore.setToken(response.data.token)
      userStore.setUserInfo(response.data.user)
      
      ElMessage.success('登录成功')
      emit('update:visible', false)
      emit('login-success')
      
      // 清空表单
      form.value.username = ''
      form.value.password = ''
    } catch (error) {
      ElMessage.error(error.response?.data?.message || '登录失败')
    }
  })
}
function onClose() {
  emit('update:visible', false)
}
function onDialogVisible(val) {
  emit('update:visible', val)
}
</script>

<style scoped>
</style> 