<script setup>
import CsvInput from './components/CsvInput.vue'
import Waiting from './components/Waiting.vue'
import { ref, onMounted, getCurrentInstance } from 'vue'
import axios from 'axios'
import DataView from './views/DataView.vue'
</script>
<template>
  <h1>TestRoom.vue</h1>
  <DataView />
</template>


<style scoped>
</style>
