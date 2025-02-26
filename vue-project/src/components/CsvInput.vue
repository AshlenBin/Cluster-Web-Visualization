<!-- 上传csv文件，单击或拖入 -->
<template>
  <div class="csv-input">
    <input
      type="file"
      ref="fileInput"
      @change="handleFileUpload"
      accept=".csv"
      style="display: none"
    />
    <div
      class="drop-zone"
      :class="{ 'drop-zone-active': isDragging }"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
      @click="triggerFileInput"
    >
      {{ uploadFile_text }}
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue'
import axios from 'axios'
const { proxy } = getCurrentInstance()
// 定义响应式数据
const isDragging = ref(false)
const uploadFile_text = ref('拖入CSV文件或点击上传')

// 定义 emits
const emit = defineEmits(['data_processe'])

// 触发文件输入框点击
const triggerFileInput = () => {
  fileInput.value.click()
}

// 处理文件上传事件
const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    uploadFile(file)
  }
}

// 处理拖拽悬停事件
const handleDragOver = () => {
  isDragging.value = true
}

// 处理拖拽离开事件
const handleDragLeave = () => {
  isDragging.value = false
}

// 处理拖拽放下事件
const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    uploadFile(file)
  }
}

// 上传成功提示
const uploadFile_success = (filename) => {
  uploadFile_text.value = '上传成功：' + filename
}

// 上传失败提示
const uploadFile_fail = (msg) => {
  uploadFile_text.value = '上传失败：' + msg
}

// 文件上传逻辑
const uploadFile = (file) => {
  uploadFile_text.value = '正在上传：' + file.name
  console.log('前端上传的文件名:', file.name)

  const formData = new FormData()
  formData.append('file', file)

  axios
    .post(`${proxy.$serverPort}/upload`, formData)
    .then((response) => {
      console.log(response)
      if (response.status === 200) {
        uploadFile_success(file.name)
        emit('data_processe', file.name) // 触发父组件事件
      } else {
        uploadFile_fail('服务器返回错误')
      }
    })
    .catch((error) => {
      console.error('文件上传失败:', error)
      uploadFile_fail(error.message)
    })
}

// 获取文件输入框的引用
const fileInput = ref(null)
</script>

<style scoped>
.csv-input {
  width: 100%;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.drop-zone {
  width: 100%;
  height: 100%;
  font-weight: bold;
  font-size: large;
  border: 3px dashed #ccc;
  border-radius: 10pt;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-align: center;

  transition: border-color 0.2s, background-color 0.2s;
}

.drop-zone:hover {
  border-color: #aaa;
}

.drop-zone-active {
  /* 拖动文件到控件上时，为控件添加此『类』，颜色变深 */
  border-color: #aaa;
  background-color: #f0f0f0;
}
</style>
