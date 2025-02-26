<script setup>
import { ref, getCurrentInstance } from 'vue'
import axios from 'axios'
const { proxy } = getCurrentInstance()
</script>

<template>
  <v-row>
    <v-col cols="6">
      <div>
        batch_size:
        <v-text-field v-model="batch_size" />
      </div>
      <div>
        epochs:
        <v-text-field v-model="epochs" />
      </div>
    </v-col>
    <v-col cols="6">
      <div>
        选用模型：
        <v-select
          v-model="selected_model"
          :items="['CNN+Transfomer', '随机森林', 'CNN']"
          label="请选择模型"
        />
      </div>
      <div>
        optimizer:
        <v-select v-model="optimizer" :items="['adam', 'sgd', 'rmsprop']" label="请选择优化器" />
      </div>
      <v-btn @click="train">开始训练</v-btn>
    </v-col>
  </v-row>
</template>