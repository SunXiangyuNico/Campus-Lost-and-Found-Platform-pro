<template>
  <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" size="large">
    <el-form-item label="帖子类型" prop="status">
      <el-select v-model="form.status" placeholder="请选择">
        <el-option label="我丢失了物品 (发布失物帖)" value="lost" />
        <el-option label="我捡到了物品 (发布招领帖)" value="found" />
      </el-select>
    </el-form-item>
    <el-form-item label="物品名称" prop="name">
      <el-input v-model="form.name" placeholder="请输入物品名称" />
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
    <el-form-item :label="form.status === 'found' ? '捡到时间' : '丢失时间'" prop="date">
      <el-date-picker v-model="form.date" type="datetime" placeholder="请选择准确的日期和时间" style="width: 100%" />
    </el-form-item>
    <el-form-item :label="form.status === 'found' ? '捡到地点' : '丢失地点'" prop="mapCoord">
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
    <el-form-item :label="form.status === 'found' ? '详细地点描述' : '详细地点描述'" prop="location">
      <el-input 
        v-model="form.location" 
        placeholder="请输入具体地点，如：图书馆三楼、教学楼A座门口、食堂二楼等" 
        type="textarea"
        :rows="2"
        maxlength="100"
        show-word-limit
      />
      <div class="location-tip">
        请详细描述物品的具体位置，方便失主/拾主准确找到地点
      </div>
    </el-form-item>
    <el-form-item label="物品图片" prop="images">
      <el-upload
        action="#"
        list-type="picture-card"
        :auto-upload="false"
        :on-change="handleImageChange"
        :file-list="form.images"
        :limit="3"
        multiple
        accept="image/*"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
    </el-form-item>
    <el-form-item label="详细描述" prop="description">
      <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请详细描述物品的特征，如品牌、颜色、尺寸等" />
    </el-form-item>
    <el-form-item label="联系方式" prop="contact">
      <el-input v-model="form.contact" placeholder="请输入您的邮箱或电话，方便失主/拾主联系" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit" :loading="loading" style="width:100%">确认发布</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, computed, defineEmits } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Minus, Refresh } from '@element-plus/icons-vue'
import { createItem } from '../api/items'

const emit = defineEmits(['success'])
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

// 字段名与后端模型完全对齐
const form = reactive({
  status: 'lost', // 默认为 lost
  name: '',
  category: '',
  date: null,
  mapCoord: null, // [x, y]
  location: '', // 新增地点描述字段
  images: [],
  description: '',
  contact: ''
})

// 验证规则与后端模型完全对齐
const rules = {
  status: [{ required: true, message: '请选择帖子类型', trigger: 'change' }],
  name: [{ required: true, message: '请输入物品名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择物品类别', trigger: 'change' }],
  date: [{ required: true, message: '请选择时间', trigger: 'change' }],
  mapCoord: [{ required: true, message: '请在地图上选择位置', trigger: 'change' }],
  location: [{ required: true, message: '请输入详细地点描述', trigger: 'blur' }],
  description: [{ required: true, message: '请输入详细描述', trigger: 'blur' }],
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
  form.images = fileList
}

async function onSubmit() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch (error) {
    ElMessage.error('表单填写不完整，请检查所有必填项')
    return
  }

  loading.value = true;
  try {
    const formData = new FormData();
    // 确保所有发送的字段名与后端控制器和模型完全一致
    formData.append('name', form.name);
    formData.append('description', form.description);
    formData.append('category', form.category);
    formData.append('status', form.status);
    formData.append('date', form.date.toISOString());
    formData.append('contact', form.contact);
    formData.append('mapCoord', JSON.stringify(form.mapCoord));
    formData.append('location', form.location); // 添加地点描述字段
    
    form.images.forEach(file => {
      if (file.raw) {
        formData.append('images', file.raw);
      }
    });

    const response = await createItem(formData);

    if (response.status === 201) {
      ElMessage.success('发布成功！');
      emit('success'); 
      formRef.value.resetFields();
      form.images = [] // 手动清空图片列表
    } else {
      ElMessage.warning(`操作完成，但服务器状态为: ${response.status}`);
    }

  } catch (error) {
    const errorMsg = error.response?.data?.msg || '发布失败，请检查网络或联系管理员';
    ElMessage.error(errorMsg);
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
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
.location-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
  line-height: 1.4;
}
</style> 