<template>
  <el-dialog :model-value="visible" @update:model-value="onDialogVisible" width="480px" :show-close="true" center title="用户注册" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" size="large">
      <el-form-item label="头像" prop="avatar">
        <div class="avatar-upload">
          <el-upload
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :on-change="handleAvatarChange"
            accept="image/*"
            :auto-upload="false"
          >
            <div class="avatar-wrapper">
              <img v-if="avatarPreview" :src="avatarPreview" class="avatar-preview" alt="头像预览" />
              <div v-else class="avatar-placeholder">
                <el-icon size="40"><Plus /></el-icon>
                <div>选择头像</div>
              </div>
            </div>
          </el-upload>
          <div class="avatar-tip">支持jpg、png格式，大小不超过2MB</div>
        </div>
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" maxlength="20" show-word-limit placeholder="请输入姓名" />
      </el-form-item>
      <el-form-item label="学号" prop="studentId">
        <el-input v-model="form.studentId" maxlength="12" show-word-limit placeholder="请输入学号（8-12位数字）" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" maxlength="40" placeholder="请输入邮箱" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="form.confirmPassword" type="password" placeholder="确认密码" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onRegister" style="width:100%">注册</el-button>
      </el-form-item>
      <el-form-item style="text-align:center; width:100%">
        <span>已有账号？<a @click.prevent="$emit('switch-login')" style="color:#409eff;cursor:pointer">去登录</a></span>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { register, getUserInfo } from '../api/auth'
import { useUserStore } from '../store/user'

const props = defineProps({
  visible: Boolean
})
const emit = defineEmits(['update:visible', 'switch-login', 'register-success'])
const formRef = ref()
const avatarPreview = ref('')
const avatarFile = ref(null)
const form = ref({
  name: '',
  studentId: '',
  email: '',
  password: '',
  confirmPassword: ''
})
const rules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { pattern: /^\d{8,12}$/, message: '学号为8-12位数字', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}
const userStore = useUserStore()

function validateConfirmPassword(rule, value, callback) {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.value.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

function beforeAvatarUpload(file) {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('头像必须是图片格式！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('头像大小不能超过 2MB！')
    return false
  }
  return false // 阻止自动上传
}

function handleAvatarChange(file) {
  if (beforeAvatarUpload(file.raw)) {
    return
  }
  
  avatarFile.value = file.raw
  
  // 创建预览URL
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.readAsDataURL(file.raw)
}

async function onRegister() {
  formRef.value.validate(async valid => {
    if (!valid) return
    
    try {
      const registerData = {
        password: form.value.password,
        name: form.value.name,
        studentId: form.value.studentId,
        email: form.value.email
      }
      
      // 如果有头像文件，添加到表单数据中
      if (avatarFile.value) {
        registerData.avatar = avatarFile.value
      }
      
      const response = await register(registerData)
      
      // 保存token和用户信息
      userStore.setToken(response.data.token)
      const userInfoResp = await getUserInfo(response.data.token)
      userStore.setUserInfo(userInfoResp.data)
      
      ElMessage.success('注册成功')
      emit('update:visible', false)
      emit('register-success')
      
      // 清空表单
      form.value.name = ''
      form.value.studentId = ''
      form.value.email = ''
      form.value.password = ''
      form.value.confirmPassword = ''
      avatarPreview.value = ''
      avatarFile.value = null
    } catch (error) {
      // 修复：将 .message 修改为 .msg，以匹配后端返回的字段名
      ElMessage.error(error.response?.data?.msg || '注册失败')
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
.avatar-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-wrapper {
  width: 80px;
  height: 80px;
  border: 2px dashed #d9d9d9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
  overflow: hidden;
}

.avatar-wrapper:hover {
  border-color: #409eff;
}

.avatar-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #8c939d;
  font-size: 12px;
}

.avatar-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
  text-align: center;
}
</style>