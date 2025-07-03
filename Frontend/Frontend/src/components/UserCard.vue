<template>
  <el-card class="user-card">
    <div class="user-info">
      <el-avatar :src="user.avatar" size="large" />
      <div class="user-meta">
        <div class="nickname">{{ user.nickname }}</div>
        <div class="student-id">学号：{{ user.studentId }}</div>
      </div>
    </div>
    <div class="user-extra">
      <div v-if="user.contact"><el-icon><el-icon-phone /></el-icon> {{ user.contact }}</div>
      <div v-if="user.college"><el-icon><el-icon-office-building /></el-icon> {{ user.college }}</div>
    </div>
  </el-card>
</template>

<script setup>
const user = {
  avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=mock',
  nickname: '测试用户',
  studentId: '2023123456',
  contact: '12345678901',
  college: '计算机学院'
}
</script>

<style scoped>
.user-card {
  margin-bottom: 18px;
  padding: 18px 12px 12px 12px;
  border-radius: 12px;
  font-size: 17px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 14px;
}
.user-meta .nickname {
  font-weight: bold;
  font-size: 20px;
  margin-bottom: 2px;
}
.user-meta .student-id {
  color: #888;
  font-size: 15px;
}
.user-extra {
  margin-top: 10px;
  color: #666;
  font-size: 15px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
</style> 