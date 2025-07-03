<template>
  <div class="profile-layout">
    <div v-if="!isLogin" class="not-login-tip">
      <el-card style="max-width:400px;margin:60px auto;text-align:center;">
        <div style="font-size:20px;color:#ff9800;margin-bottom:12px;">未登录</div>
        <div style="margin-bottom:16px;">请先登录后再访问个人中心</div>
        <el-button type="primary" @click="goHome">返回主页</el-button>
      </el-card>
    </div>
    <div v-else>
      <div class="profile-navbar">
        <el-button type="primary" icon="el-icon-arrow-left" @click="goHome" round>返回主页</el-button>
        <span class="profile-title">个人中心</span>
      </div>

      <!-- 用户信息卡片 -->
      <el-card class="user-info-card">
        <div class="user-info-header">
          <div class="avatar-section">
            <el-avatar :size="80" :src="avatarUrl" @click="showAvatarDialog = true">
              <span v-if="!avatarUrl">{{ userInfo.name?.charAt(0) || '用' }}</span>
            </el-avatar>
            <el-button text type="primary" @click="showAvatarDialog = true" class="change-avatar-btn">
              更换头像
            </el-button>
          </div>
          <div class="user-details">
            <h2>{{ userInfo.name }}</h2>
            <p><strong>学号：</strong>{{ userInfo.studentId }}</p>
            <p><strong>邮箱：</strong>{{ userInfo.email }}</p>
            <p><strong>电话：</strong>{{ userInfo.phone || '未设置' }}</p>
            <p><strong>微信：</strong>{{ userInfo.wechat || '未设置' }}</p>
          </div>
          <div class="user-actions">
            <el-button type="primary" @click="showPasswordDialog = true">修改密码</el-button>
            <el-button type="warning" @click="showDeleteDialog = true">注销账户</el-button>
          </div>
        </div>
      </el-card>

      <!-- 帖子管理 -->
      <el-card class="profile-card">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="我的发布" name="published">
            <div class="posts-header">
              <h3>我的发布 ({{ myPosts.length }})</h3>
              <el-button type="primary" @click="handlePublishClick">发布新帖</el-button>
            </div>
            <div v-if="myPosts.length === 0" class="empty-posts">
              <el-empty description="还没有发布任何帖子">
                <el-button type="primary" @click="handlePublishClick">发布第一个帖子</el-button>
              </el-empty>
            </div>
            <div v-else class="posts-grid">
              <div v-for="post in myPosts" :key="post.id" class="post-card">
                <div class="post-image">
                  <img v-if="post.images && post.images.length > 0" :src="post.images[0]" alt="帖子图片" />
                  <div v-else class="no-image">无图片</div>
                </div>
                <div class="post-content">
                  <div class="post-header">
                    <el-tag :type="post.status === 'lost' ? 'danger' : 'success'">
                      {{ post.status === 'lost' ? '丢失' : '拾取' }}
                    </el-tag>
                    <el-tag effect="plain">{{ getCategoryText(post.category) }}</el-tag>
                  </div>
                  <h4 class="post-title">{{ post.name }}</h4>
                  <p class="post-desc">{{ post.desc }}</p>
                  <p class="post-location">📍 {{ post.locationText }}</p>
                  <p class="post-time">🕒 {{ formatTime(post.time) }}</p>
                  <div class="post-actions">
                    <el-button size="small" @click="viewPost(post)">查看</el-button>
                    <el-button size="small" type="warning" @click="editPost(post)">编辑</el-button>
                    <el-button size="small" type="danger" @click="deletePost(post)">删除</el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="我的认领" name="claimed">
            <div class="posts-header">
              <h3>我的认领 ({{ myClaims.length }})</h3>
            </div>
            <div v-if="myClaims.length === 0" class="empty-posts">
              <el-empty description="还没有认领任何物品" />
            </div>
            <div v-else class="posts-grid">
              <div v-for="post in myClaims" :key="post.id" class="post-card">
                <div class="post-image">
                  <img v-if="post.images && post.images.length > 0" :src="post.images[0]" alt="帖子图片" />
                  <div v-else class="no-image">无图片</div>
                </div>
                <div class="post-content">
                  <div class="post-header">
                    <el-tag type="success">已认领</el-tag>
                    <el-tag effect="plain">{{ getCategoryText(post.category) }}</el-tag>
                  </div>
                  <h4 class="post-title">{{ post.name }}</h4>
                  <p class="post-desc">{{ post.desc }}</p>
                  <p class="post-location">📍 {{ post.locationText }}</p>
                  <p class="post-time">🕒 认领时间：{{ formatTime(post.claimedAt) }}</p>
                  <div class="post-actions">
                    <el-button size="small" @click="viewPost(post)">查看</el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

    <!-- 更换头像对话框 -->
    <el-dialog v-model="showAvatarDialog" title="更换头像" width="400px">
      <div class="avatar-upload-dialog">
        <el-upload
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
          :on-change="handleAvatarChange"
          accept="image/*"
          :auto-upload="false"
        >
          <div class="avatar-preview-large">
            <img v-if="avatarPreview" :src="avatarPreview" alt="头像预览" />
            <img v-else-if="avatarUrl" :src="avatarUrl" alt="当前头像" />
            <div v-else class="no-avatar">
              <el-icon size="60"><Plus /></el-icon>
              <div>点击选择头像</div>
            </div>
          </div>
        </el-upload>
        <p class="upload-tip">支持jpg、png格式，大小不超过2MB</p>
      </div>
      <template #footer>
        <el-button @click="showAvatarDialog = false">取消</el-button>
        <el-button type="primary" @click="uploadAvatar" :loading="uploading">保存</el-button>
      </template>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="showPasswordDialog" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="80px">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="changePassword" :loading="passwordLoading">确认修改</el-button>
      </template>
    </el-dialog>

    <!-- 注销账户对话框 -->
    <el-dialog v-model="showDeleteDialog" title="注销账户" width="400px">
      <el-alert title="警告" type="warning" :closable="false" style="margin-bottom: 20px;">
        注销账户将永久删除您的所有数据，包括发布的帖子、评论等，此操作不可恢复！
      </el-alert>
      <el-form :model="deleteForm" :rules="deleteRules" ref="deleteFormRef" label-width="80px">
        <el-form-item label="确认密码" prop="password">
          <el-input v-model="deleteForm.password" type="password" show-password placeholder="请输入密码确认注销" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDeleteDialog = false">取消</el-button>
        <el-button type="danger" @click="deleteAccount" :loading="deleteLoading">确认注销</el-button>
      </template>
    </el-dialog>

    <!-- 编辑帖子对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑帖子" width="600px">
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="80px">
        <el-form-item label="物品名称" prop="name">
          <el-input v-model="editForm.name" placeholder="请输入物品名称" />
        </el-form-item>
        
        <el-form-item label="物品类型" prop="category">
          <el-select v-model="editForm.category" placeholder="请选择物品类型">
            <el-option label="证件" value="id"></el-option>
            <el-option label="电子产品" value="electronics"></el-option>
            <el-option label="书籍文具" value="book"></el-option>
            <el-option label="衣物用品" value="clothes"></el-option>
            <el-option label="钥匙卡片" value="key"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="物品状态" prop="status">
          <el-radio-group v-model="editForm.status">
            <el-radio value="lost">丢失</el-radio>
            <el-radio value="found">拾取</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="详细描述" prop="description">
          <el-input 
            v-model="editForm.description" 
            type="textarea" 
            rows="4" 
            placeholder="请详细描述物品特征，包括颜色、品牌、外观等信息..."
          />
        </el-form-item>

        <el-form-item label="地点描述" prop="location">
          <el-input v-model="editForm.location" placeholder="请描述丢失或拾取的具体地点" />
        </el-form-item>

        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="editForm.contact" placeholder="请输入手机号或微信号" />
        </el-form-item>

        <el-form-item label="时间" prop="date">
          <el-date-picker
            v-model="editForm.date"
            type="datetime"
            placeholder="选择丢失或拾取时间"
            format="YYYY-MM-DD HH:mm"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEditPost" :loading="editLoading">保存修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'
import { 
  getMyPosts, 
  changePassword as changePasswordAPI, 
  updateAvatar as updateAvatarAPI,
  deleteAccount as deleteAccountAPI 
} from '../api/auth'
import { deleteItem, updateItem, getMyClaims } from '../api/items'
import { getAvatarUrl, formatTime } from '../utils/index.js'

const userStore = useUserStore()
const router = useRouter()

// 用户信息和登录状态
const isLogin = computed(() => userStore.isLogin)
const userInfo = computed(() => userStore.userInfo || {
  name: '未登录',
  studentId: '',
  email: '',
  phone: '',
  wechat: '',
  avatar: null
})

// 头像相关
const avatarUrl = computed(() => {
  return getAvatarUrl(userInfo.value.avatar)
})

// 我的帖子
const myPosts = ref([])
const myClaims = ref([])
const activeTab = ref('published')

// 对话框状态
const showAvatarDialog = ref(false)
const showPasswordDialog = ref(false)
const showDeleteDialog = ref(false)
const showEditDialog = ref(false)

// 头像上传
const avatarPreview = ref('')
const avatarFile = ref(null)
const uploading = ref(false)

// 密码修改
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordFormRef = ref()
const passwordLoading = ref(false)

// 账户注销
const deleteForm = ref({
  password: ''
})
const deleteFormRef = ref()
const deleteLoading = ref(false)

// 编辑帖子
const editForm = ref({
  name: '',
  category: '',
  status: '',
  description: '',
  location: '',
  contact: '',
  date: null
})
const editFormRef = ref()
const editLoading = ref(false)
const currentEditPost = ref(null)

// 验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const deleteRules = {
  password: [
    { required: true, message: '请输入密码确认注销', trigger: 'blur' }
  ]
}

const editRules = {
  name: [
    { required: true, message: '请输入物品名称', trigger: 'blur' },
    { min: 1, max: 50, message: '物品名称长度在1到50个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择物品类型', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择物品状态', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入详细描述', trigger: 'blur' },
    { min: 10, max: 500, message: '描述长度在10到500个字符', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入地点描述', trigger: 'blur' }
  ],
  contact: [
    { required: true, message: '请输入联系方式', trigger: 'blur' }
  ],
  date: [
    { required: true, message: '请选择时间', trigger: 'change' }
  ]
}

function validateConfirmPassword(rule, value, callback) {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.value.newPassword) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

// 获取我的帖子
async function loadMyPosts() {
  try {
    const response = await getMyPosts()
    myPosts.value = response.data
    console.log('获取到的我的帖子数据:', myPosts.value)
  } catch (error) {
    console.error('获取我的帖子失败:', error)
    
    // 根据错误类型提供更详细的提示
    let errorMessage = '获取我的帖子失败'
    if (error.response) {
      const status = error.response.status
      switch (status) {
        case 401:
          errorMessage = '登录已过期，请重新登录'
          break
        case 500:
          errorMessage = '服务器错误，请稍后重试'
          break
        default:
          errorMessage = '网络错误，请检查网络连接'
      }
    }
    
    ElMessage.error(errorMessage)
  }
}

// 获取我的认领
async function loadMyClaims() {
  try {
    const response = await getMyClaims()
    myClaims.value = response.data
  } catch (error) {
    console.error('获取我的认领失败:', error)
    
    // 根据错误类型提供更详细的提示
    let errorMessage = '获取我的认领失败'
    if (error.response) {
      const status = error.response.status
      switch (status) {
        case 401:
          errorMessage = '登录已过期，请重新登录'
          break
        case 500:
          errorMessage = '服务器错误，请稍后重试'
          break
        default:
          errorMessage = '网络错误，请检查网络连接'
      }
    }
    
    ElMessage.error(errorMessage)
  }
}

// 头像处理
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

async function uploadAvatar() {
  if (!avatarFile.value) {
    ElMessage.warning('请先选择头像')
    return
  }

  uploading.value = true
  try {
    const response = await updateAvatarAPI(avatarFile.value, userStore.token)
    ElMessage.success('头像更新成功')
    
    // 更新用户信息
    await userStore.refreshUserInfo()
    
    // 通知其他组件头像已更新
    window.dispatchEvent(new CustomEvent('avatar-updated'))
    
    showAvatarDialog.value = false
    avatarPreview.value = ''
    avatarFile.value = null
  } catch (error) {
    ElMessage.error(error.response?.data?.msg || '头像更新失败')
  } finally {
    uploading.value = false
  }
}

// 修改密码
async function changePassword() {
  passwordFormRef.value.validate(async (valid) => {
    if (!valid) return

    passwordLoading.value = true
    try {
      await changePasswordAPI(passwordForm.value, userStore.token)
      ElMessage.success('密码修改成功')
      showPasswordDialog.value = false
      
      // 清空表单
      passwordForm.value = {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    } catch (error) {
      ElMessage.error(error.response?.data?.msg || '密码修改失败')
    } finally {
      passwordLoading.value = false
    }
  })
}

// 注销账户
async function deleteAccount() {
  deleteFormRef.value.validate(async (valid) => {
    if (!valid) return

    deleteLoading.value = true
    try {
      await deleteAccountAPI(deleteForm.value.password, userStore.token)
      ElMessage.success('账户注销成功')
      
      // 清除本地数据并跳转到首页
      userStore.logout()
      router.push('/')
    } catch (error) {
      ElMessage.error(error.response?.data?.msg || '账户注销失败')
    } finally {
      deleteLoading.value = false
    }
  })
}

// 帖子操作
function viewPost(post) {
  // 跳转到首页并选中该帖子
  router.push(`/?selected=${post.id}`)
}

async function deletePost(post) {
  try {
    console.log('删除帖子 - post对象:', post)
    console.log('删除帖子 - post.id:', post.id)
    
    await ElMessageBox.confirm(
      `确定要删除帖子"${post.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await deleteItem(post.id)
    ElMessage.success('帖子删除成功')
    
    // 重新加载我的帖子
    await loadMyPosts()
  } catch (error) {
    console.error('删除帖子错误:', error)
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.msg || '删除失败')
    }
  }
}

// 编辑帖子
function editPost(post) {
  currentEditPost.value = post
  
  // 填充编辑表单
  editForm.value = {
    name: post.name,
    category: post.category,
    status: post.status,
    description: post.desc || post.description,
    location: post.locationText || post.location,
    contact: post.contact,
    date: post.time ? new Date(post.time) : null
  }
  
  showEditDialog.value = true
}

// 保存编辑
async function saveEditPost() {
  editFormRef.value.validate(async (valid) => {
    if (!valid) return

    editLoading.value = true
    try {
      console.log('编辑帖子 - currentEditPost:', currentEditPost.value)
      console.log('编辑帖子 - currentEditPost.id:', currentEditPost.value?.id)
      
      // 构建更新数据
      const updateData = {
        name: editForm.value.name,
        category: editForm.value.category,
        status: editForm.value.status,
        description: editForm.value.description,
        location: editForm.value.location,
        contact: editForm.value.contact,
        date: editForm.value.date.toISOString()
      }
      
      console.log('编辑帖子 - 更新数据:', updateData)
      
      await updateItem(currentEditPost.value.id, updateData)
      ElMessage.success('帖子更新成功')
      
      showEditDialog.value = false
      
      // 重新加载我的帖子
      await loadMyPosts()
    } catch (error) {
      console.error('编辑帖子错误:', error)
      ElMessage.error(error.response?.data?.msg || '更新失败')
    } finally {
      editLoading.value = false
    }
  })
}

// 工具函数
function getCategoryText(category) {
  const categoryMap = {
    'id': '证件',
    'electronics': '电子产品',
    'book': '书籍文具',
    'clothes': '衣物用品',
    'key': '钥匙卡片',
    'other': '其他'
  }
  return categoryMap[category] || '其他'
}



function goHome() {
  router.push('/')
}

// 统一的发布处理逻辑
function handlePublishClick() {
  // 跳转到首页并触发发布对话框
  router.push('/').then(() => {
    // 使用事件总线来触发首页的发布对话框
    window.dispatchEvent(new CustomEvent('show-publish-dialog'))
  })
}

// 监听Tab切换
watch(activeTab, (newTab) => {
  if (newTab === 'claimed' && myClaims.value.length === 0) {
    loadMyClaims()
  }
})

// 页面加载时获取数据
onMounted(async () => {
  // 首先检查登录状态
  if (!userStore.token) {
    // 没有token，直接返回
    return
  }
  
  try {
    // 验证token有效性并刷新用户信息
    const isLoggedIn = await userStore.checkLoginStatus()
    
    if (isLoggedIn && userStore.isLogin) {
      // 登录状态有效，加载数据
      await loadMyPosts()
    } else {
      // 登录状态无效，清除状态
      userStore.logout()
    }
  } catch (error) {
    console.error('验证登录状态失败:', error)
    userStore.logout()
  }
})
</script>

<style scoped>
.profile-navbar {
  width: 1000px;
  max-width: 95vw;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.profile-title {
  font-size: 22px;
  color: #ff9800;
  font-weight: bold;
}

.profile-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f5f6fa;
  min-height: calc(100vh - 56px);
  padding: 32px 0 0 0;
}

.user-info-card {
  width: 1000px;
  max-width: 95vw;
  margin-bottom: 18px;
  border-radius: 16px !important;
  box-shadow: 0 4px 24px #ffe0b2 !important;
}

.user-info-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.change-avatar-btn {
  font-size: 12px;
}

.user-details {
  flex: 1;
}

.user-details h2 {
  margin: 0 0 16px 0;
  color: #333;
  font-size: 24px;
}

.user-details p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}

.user-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-card {
  width: 1000px;
  max-width: 95vw;
  border-radius: 16px !important;
  box-shadow: 0 4px 24px #ffe0b2 !important;
  background: #fff8e1 !important;
  padding: 24px 32px 32px 32px;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-header h3 {
  margin: 0;
  color: #333;
}

.empty-posts {
  text-align: center;
  padding: 40px 0;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.post-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  transition: box-shadow 0.3s;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.post-image {
  height: 150px;
  overflow: hidden;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999;
}

.post-content {
  padding: 16px;
}

.post-header {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.post-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.post-desc {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-location,
.post-time {
  margin: 4px 0;
  font-size: 12px;
  color: #999;
}

.post-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.post-actions .el-button {
  flex: 1;
  min-width: 70px;
  justify-content: center;
  font-size: 12px;
}

/* 按钮颜色自动由Element Plus的type属性控制 */

/* 移动端按钮垂直排列 */
@media (max-width: 480px) {
  .post-actions {
    flex-direction: column;
    gap: 6px;
  }
  
  .post-actions .el-button {
    width: 100%;
    min-width: unset;
    flex: none;
  }
}

/* 中等屏幕优化 */
@media (max-width: 768px) and (min-width: 481px) {
  .post-actions .el-button {
    min-width: 60px;
    font-size: 11px;
    padding: 4px 8px;
  }
}

/* 对话框样式 */
.avatar-upload-dialog {
  text-align: center;
}

.avatar-preview-large {
  width: 150px;
  height: 150px;
  border: 2px dashed #d9d9d9;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
  overflow: hidden;
  margin-bottom: 16px;
}

.avatar-preview-large:hover {
  border-color: #409eff;
}

.avatar-preview-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.no-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #8c939d;
  font-size: 14px;
}

.upload-tip {
  font-size: 12px;
  color: #999;
}

.not-login-tip {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

@media (max-width: 1100px) {
  .user-info-card, 
  .profile-card, 
  .profile-navbar {
    width: 100%;
    min-width: 0;
  }
  
  .user-info-header {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .user-actions {
    flex-direction: row;
    justify-content: center;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .post-actions {
    flex-direction: column;
  }
  
  .post-actions .el-button {
    width: 100%;
    min-width: unset;
  }
}

@media (max-width: 768px) {
  .profile-card {
    padding: 16px;
  }
  
  .user-info-header {
    padding: 16px;
  }
}
</style> 