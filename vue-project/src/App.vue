<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, getCurrentInstance } from 'vue'
import TestRoom from './TestRoom.vue'
const { proxy } = getCurrentInstance()
</script>

<template>
  <header>
    <h1>聚类可视化</h1>
  </header>
  <RouterView />
</template>

<style scoped>
h1 {
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
