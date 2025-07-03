<template>
  <div class="post-list-container">
    <div v-if="posts && posts.length > 0" class="post-list-scroll">
      <div 
        v-for="post in posts" 
        :key="post.id" 
        :class="['post-item', { selected: post.id === selectedId }]" 
        @click="$emit('select', post.id)"
      >
        <div class="status-icon" :class="getStatusClass(post)">
          {{ getStatusText(post) }}
          <div v-if="post.claimed || post.is_claimed" class="claimed-badge">✓</div>
        </div>
        <div class="post-info">
          <div class="info-row top">
            <span class="post-name">{{ post.name }}</span>
            <span class="user-name">{{ post.user.name }}</span>
          </div>
          <div class="info-row bottom">
            <span class="location">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 10c0 7-9 13-9 13s-9-7-9-10a9 9 0 1 1 18 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M12 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
              {{ post.location || '未指定地点' }}
            </span>
            <span class="post-date">{{ formatDate(post.date) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 19.5a8.5 8.5 0 1 0 0-17 8.5 8.5 0 0 0 0 17zM21.5 21.5l-4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
      </div>
      <p>暂无相关帖子</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  posts: {
    type: Array,
    required: true,
  },
  selectedId: {
    type: String,
    default: null,
  },
});

defineEmits(['select']);

// 日期格式化函数，转换为 "M月d日"
function formatDate(isoString) {
  if (!isoString) return '未知日期';
  try {
    const date = new Date(isoString);
    return `${date.getMonth() + 1}月${date.getDate()}日`;
  } catch (e) {
    return '无效日期';
  }
}

// 获取帖子状态类名
function getStatusClass(post) {
  if (post.claimed || post.is_claimed) {
    return 'claimed';
  }
  return post.status === 'lost' ? 'lost' : 'found';
}

// 获取帖子状态文字
function getStatusText(post) {
  if (post.claimed || post.is_claimed) {
    return post.status === 'lost' ? '失' : '拾';
  }
  return post.status === 'lost' ? '失' : '拾';
}
</script>

<style scoped>
.post-list-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  background-color: #f7f8fa;
}

.post-list-scroll {
  padding: 8px;
}

.post-item {
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  background-color: #fff;
  border: 1px solid #ebedf0;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.post-item:hover {
  background-color: #fafafa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.post-item.selected {
  background-color: #e6f7ff;
  border-color: #91d5ff;
}

.status-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  color: #fff;
  margin-right: 12px;
  position: relative;
}

.status-icon.lost {
  background-color: #fa5151; /* 红色 */
}

.status-icon.found {
  background-color: #07c160; /* 绿色 */
}

.status-icon.claimed {
  background-color: #909399; /* 灰色表示已认领 */
  opacity: 0.8;
}

.claimed-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 16px;
  height: 16px;
  background-color: #67c23a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
  border: 2px solid white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.post-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow: hidden;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-name {
  font-size: 15px;
  font-weight: 500;
  color: #323233;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-name {
  font-size: 13px;
  color: #969799;
}

.location {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #646566;
}

.location svg {
  flex-shrink: 0;
}

.post-date {
  font-size: 13px;
  color: #969799;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #c8c9cc;
}

.empty-icon {
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

/* 滚动条美化 */
.post-list-container::-webkit-scrollbar {
  width: 6px;
}
.post-list-container::-webkit-scrollbar-track {
  background: transparent;
}
.post-list-container::-webkit-scrollbar-thumb {
  background: #dcdee0;
  border-radius: 3px;
}
.post-list-container::-webkit-scrollbar-thumb:hover {
  background: #c8c9cc;
}
</style>