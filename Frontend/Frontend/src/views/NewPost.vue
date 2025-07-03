<template>
  <div class="new-post-container">
    <el-card class="form-card">
      <h2 class="form-title">发布新信息</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" size="large">
        <el-form-item label="帖子类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择">
            <el-option label="捡到物品帖" value="found" />
            <el-option label="丢失物品帖" value="lost" />
          </el-select>
        </el-form-item>
        <el-form-item label="物品名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入物品名称" />
        </el-form-item>
        <el-form-item label="物品类别" prop="category">
          <el-select v-model="form.category" placeholder="请选择">
            <el-option label="证件" value="id" />
            <el-option label="电子产品" value="electronics" />
            <el-option label="书籍" value="book" />
            <el-option label="衣物" value="clothes" />
            <el-option label="钥匙" value="key" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item :label="form.type === 'found' ? '捡到时间' : '丢失时间'" prop="date">
          <el-date-picker v-model="form.date" type="date" placeholder="yyyy/mm/dd" style="width: 100%" />
        </el-form-item>
        <el-form-item :label="form.type === 'found' ? '捡到地点' : '丢失地点'" prop="location">
          <div class="map-select-block">
            <div class="map-select-tip">请在地图上点击选择具体位置（可使用右下角按钮缩放地图）</div>
            
            <!-- 地图容器 -->
            <div class="map-container" ref="mapContainer">
              <!-- 地图图片容器 -->
              <div 
                class="map-wrapper" 
                ref="mapWrapper"
                :style="mapWrapperStyle"
                @click="onMapClick($event)"
                @mousedown="onMapMouseDown"
                @mousemove="onMapMouseMove"
                @mouseup="onMapMouseUp"
                @mouseleave="onMapMouseUp"
                @wheel="onMapWheel"
              >
                <img src="/map.png" class="map-img" ref="mapRef" draggable="false" />
                <div v-if="form.mapCoord" class="map-marker" :style="markerStyle"></div>
              </div>
              
              <!-- 缩放控制按钮 -->
              <div class="map-controls">
                <el-button-group>
                  <el-button size="small" @click="zoomIn" :disabled="scale >= maxScale">
                    <el-icon><Plus /></el-icon>
                  </el-button>
                  <el-button size="small" @click="zoomOut" :disabled="scale <= minScale">
                    <el-icon><Minus /></el-icon>
                  </el-button>
                  <el-button size="small" @click="resetView">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </el-button-group>
                <div class="zoom-indicator">{{ Math.round(scale * 100) }}%</div>
              </div>
            </div>
            
            <div class="map-coord-tip" v-if="form.mapCoord">
              已选择位置：X: {{ form.mapCoord[0].toFixed(2) }}, Y: {{ form.mapCoord[1].toFixed(2) }}
            </div>
          </div>
        </el-form-item>
        <el-form-item label="物品图片" prop="images">
          <el-upload
            class="upload-demo"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleImageChange"
            :file-list="form.images"
            :limit="5"
            multiple
            accept="image/*"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="物品描述" prop="desc">
          <el-input v-model="form.desc" type="textarea" :rows="3" placeholder="请输入物品描述" />
        </el-form-item>
        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="form.contact" placeholder="如手机号/微信/QQ" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" :loading="loading" style="width:100%">发布</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Minus, Refresh } from '@element-plus/icons-vue'

const formRef = ref()
const mapRef = ref()
const mapContainer = ref()
const mapWrapper = ref()
const loading = ref(false)

// 地图缩放相关状态
const scale = ref(1)
const minScale = 0.5
const maxScale = 3
const translateX = ref(0)
const translateY = ref(0)

// 拖拽相关状态
const isDragging = ref(false)
const lastMousePos = reactive({ x: 0, y: 0 })

const form = reactive({
  type: '',
  title: '',
  category: '',
  date: '',
  location: '',
  mapCoord: null, // [x, y]
  images: [],
  desc: '',
  contact: ''
})

const rules = {
  type: [{ required: true, message: '请选择帖子类型', trigger: 'change' }],
  title: [{ required: true, message: '请输入物品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择物品类别', trigger: 'change' }],
  date: [{ required: true, message: '请选择时间', trigger: 'change' }],
  mapCoord: [{ required: true, message: '请选择地图位置', trigger: 'change' }],
  desc: [{ required: true, message: '请输入物品描述', trigger: 'blur' }],
  contact: [{ required: true, message: '请输入联系方式', trigger: 'blur' }]
}

// 地图容器样式
const mapWrapperStyle = computed(() => {
  return {
    transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
    transformOrigin: '0 0',
    cursor: isDragging.value ? 'grabbing' : 'crosshair'
  }
})

// 标记点样式 - 更小更精准
const markerStyle = computed(() => {
  if (!form.mapCoord) return {}
  return {
    left: form.mapCoord[0] + 'px',
    top: form.mapCoord[1] + 'px'
  }
})

// 地图点击标记位置
function onMapClick(e) {
  if (isDragging.value) return // 如果正在拖拽，不进行标记
  
  const rect = mapWrapper.value.getBoundingClientRect()
  // 计算相对于原始图片的精确坐标
  const relativeX = (e.clientX - rect.left - translateX.value) / scale.value
  const relativeY = (e.clientY - rect.top - translateY.value) / scale.value
  
  // 保留2位小数，提高精度
  form.mapCoord = [Number(relativeX.toFixed(2)), Number(relativeY.toFixed(2))]
}

// 缩放功能
function zoomIn() {
  if (scale.value < maxScale) {
    scale.value = Math.min(scale.value * 1.2, maxScale)
  }
}

function zoomOut() {
  if (scale.value > minScale) {
    scale.value = Math.max(scale.value / 1.2, minScale)
  }
}

function resetView() {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

// 鼠标滚轮缩放
function onMapWheel(e) {
  e.preventDefault()
  const rect = mapWrapper.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top
  
  const oldScale = scale.value
  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.max(minScale, Math.min(maxScale, oldScale * delta))
  
  if (newScale !== oldScale) {
    // 以鼠标位置为中心进行缩放
    const scaleRatio = newScale / oldScale
    translateX.value = mouseX - (mouseX - translateX.value) * scaleRatio
    translateY.value = mouseY - (mouseY - translateY.value) * scaleRatio
    scale.value = newScale
  }
}

// 地图拖拽功能
function onMapMouseDown(e) {
  e.preventDefault()
  isDragging.value = true
  lastMousePos.x = e.clientX
  lastMousePos.y = e.clientY
}

function onMapMouseMove(e) {
  if (!isDragging.value) return
  
  const deltaX = e.clientX - lastMousePos.x
  const deltaY = e.clientY - lastMousePos.y
  
  translateX.value += deltaX
  translateY.value += deltaY
  
  lastMousePos.x = e.clientX
  lastMousePos.y = e.clientY
}

function onMapMouseUp() {
  isDragging.value = false
}

function handleImageChange(file, fileList) {
  form.images = fileList.slice(0, 5)
}

function onSubmit() {
  formRef.value.validate(valid => {
    if (!valid) return
    loading.value = true
    setTimeout(() => {
      ElMessage.success('发布成功！')
      loading.value = false
      // 清空表单
      Object.assign(form, { type: '', title: '', category: '', date: '', location: '', mapCoord: null, images: [], desc: '', contact: '' })
      // 重置地图视图
      resetView()
    }, 1000)
  })
}
</script>

<style scoped>
.new-post-container {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: #f5f6fa;
  padding: 32px 0;
}
.form-card {
  width: 600px;
  padding: 32px 36px 12px 36px;
  border-radius: 12px;
  box-shadow: 0 4px 24px #e6e8f0;
}
.form-title {
  text-align: center;
  margin-bottom: 24px;
  font-weight: bold;
  font-size: 24px;
}
.map-select-block {
  width: 100%;
}

.map-select-tip {
  color: #888;
  font-size: 14px;
  margin-bottom: 6px;
}

.map-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  height: 350px;
  margin: 0 auto;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.map-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.1s ease-out;
  user-select: none;
}

.map-img {
  display: block;
  width: 500px;
  height: auto;
  border-radius: 6px;
  pointer-events: none;
}

.map-marker {
  position: absolute;
  width: 10px;
  height: 10px;
  background: #ff4d4f;
  border: 2px solid #fff;
  border-radius: 50%;
  left: 0;
  top: 0;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 8px rgba(255, 77, 79, 0.6);
  z-index: 10;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(255, 77, 79, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0);
  }
}

.map-controls {
  position: absolute;
  bottom: 12px;
  right: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(255, 255, 255, 0.95);
  padding: 8px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.zoom-indicator {
  font-size: 12px;
  color: #666;
  text-align: center;
  margin-top: 4px;
  font-weight: 500;
}

.map-coord-tip {
  color: #409eff;
  font-size: 15px;
  margin-top: 6px;
  text-align: center;
}
</style> 