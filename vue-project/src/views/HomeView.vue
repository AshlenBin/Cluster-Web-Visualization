<script setup>
import global_storage from '../global.js'
import CsvInput from '../components/CsvInput.vue'
import Waiting from '../components/Waiting.vue'
import { ref, onMounted, getCurrentInstance } from 'vue'
import axios from 'axios'

const data_preprocessing = ref(false)
const imageSrc = ref(null)
const { proxy } = getCurrentInstance()
const data_preprocess = (filename) => {
  data_preprocessing.value = true
  axios
    .get(`${proxy.$serverPort}/data_preprocess?filename=${filename}`)
    .then((response) => {
      console.log('数据预处理成功:', response)
      global_storage.kmeans_data = response.data
      data_preprocessing.value = false
      proxy.$router.push('/data')
    })
    .catch((error) => {
      console.error('数据预处理失败:', error)
      data_preprocessing.value = false
    })
}
onMounted(() => {
  // 某些功能
})
</script>
<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2" md="2" lg="1">
        <v-card class="pa-4">
          开发者：<br />
          蔡诗彬
        </v-card>
      </v-col>

      <v-col cols="8" md="8" lg="10">
        <v-card class="pa-4">
          <CsvInput @data_processe="(filename) => data_preprocess(filename)" />
          <Waiting :show="data_preprocessing" style="margin-top: 20px">
            数据处理中，请等待...
          </Waiting>
          <img v-if="imageSrc" :src="imageSrc" alt="Processed Image" />
        </v-card>
      </v-col>

      <v-col cols="2" md="2" lg="1">
        <v-card class="pa-4"> </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>


<style scoped>
.card {
  height: 100%;
}
</style>
