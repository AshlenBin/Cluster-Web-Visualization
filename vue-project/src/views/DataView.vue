<script setup>
import global_storage from '../global.js'
import DeepLearningBar from '@/components/DeepLearningBar.vue'
import { ref, computed, onMounted, getCurrentInstance } from 'vue'
import Echarts from 'vue-echarts'
import * as ecStat from 'echarts-stat'
import * as echarts from 'echarts'
// import { color } from 'echarts/core.js'
// import Math from 'mathjs'
const { proxy } = getCurrentInstance()

const option_scatter = ref(null)
const echart_scatter_mounted = () => {
  if (global_storage.kmeans_data === null) {
    // 如果没有数据，跳转到首页
    proxy.$router.push('/')
    return
  }

  var x_umap = global_storage.kmeans_data.x_umap
  var cluster_ids_x = global_storage.kmeans_data.cluster_ids_x

  // 散点颜色
  var n = cluster_ids_x.reduce((max, item) => Math.max(max, item), -Infinity)
  var colors = []
  var saturation = 70 // 饱和度
  var lightness = 50 // 亮度
  for (let i = 0; i < n; i++) {
    var hue = (i * 360) / n // 均匀分布色相
    colors.push(`hsla(${hue}, ${saturation}%, ${lightness}%,50%)`) // 透明度：50%
  }

  // 将数据转换为 ECharts 所需的格式
  var scatterData = []
  for (let i = 0; i < x_umap.length; i++) {
    scatterData.push({
      value: [x_umap[i][0], x_umap[i][1], cluster_ids_x[i]], // 横纵坐标
      itemStyle: {
        color: colors[cluster_ids_x[i]], // 根据标签设置颜色
      },
    })
  }

  // ECharts 配置
  option_scatter.value = {
    title: {
      text: '聚类分布图',
      left: 'center',
    },
    xAxis: {
      type: 'value', // 数值轴
      scale: true, // 自适应缩放
    },
    yAxis: {
      type: 'value', // 数值轴
      scale: true, // 自适应缩放
    },
    series: [
      {
        type: 'scatter', // 散点图
        data: scatterData, // 数据
        symbolSize: 5, // 点的大小
      },
    ],
    visualMap: {
      type: 'continuous', // 连续式 visualMap
      min: 1, // 最小值
      max: n, // 最大值（n 是标签的数量）
      color: colors.reverse(), // 颜色数组（数字是从下往上排的，而颜色是从上往下排的，纯逆天）
      calculable: true, // 是否显示拖拽用的手柄
      show: true, // 显示 visualMap 的图例
      orient: 'vertical', // 垂直放置
      left: 'right', // 图例放置在右侧
      top: 'middle', // 图例垂直居中
      itemHeight: 400, // 颜色柱高度与图表等高
    },
    dataZoom: {
      type: 'inside', // 鼠标滚轮缩放
      xAxisIndex: 0, // 对第0个 x 轴缩放
      yAxisIndex: 0, // 对第0个 y 轴缩放
      moveOnMouseMove: true, // 鼠标拖动
    },
  }
  echart_histogram_mounted(1, colors[1])
}
const scatterData_clicked = (params) => {
  // 散点图点击事件：显示对应聚类的直方图
  console.log('scatterData_clicked:', params)
  var color = params.color
  color = color.replace('50%)', '90%)') // 把透明度改为90%
  echart_histogram_mounted(params.value[2], color)
}

// Protein的频数分布直方图
const option_histogram = ref(null)
const echart_histogram_mounted = (id, color) => {
  var cluster_ids_x = global_storage.kmeans_data.cluster_ids_x
  var Protein = global_storage.kmeans_data.Protein
  // 筛选出cluster_ids_x==id的Protein
  var histogramData = Protein.filter((item, index) => cluster_ids_x[index] == id)
  // console.log('histogramData:', histogramData)
  // var histogramData = Protein
  const bins = ecStat.histogram(histogramData) // 计算频数分布
  // console.log('bins:', bins)
  option_histogram.value = {
    title: {
      text: 'Protein的频数分布直方图',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    xAxis: {
      type: 'category',
      data: bins.data.map((subArray) => subArray[2]),
      boundaryGap: true,
      name: '区间',
      nameLocation: 'center',
      nameGap: 30,
    },
    yAxis: {
      type: 'value',
      name: '频率',
      nameLocation: 'center',
      nameGap: 30,
    },
    dataZoom: [
      {
        type: 'inside', // 内置型 dataZoom，支持鼠标滚轮缩放
        xAxisIndex: 0, // 控制 x 轴
        yAxisIndex: 0, // 控制 y 轴
      },
      {
        type: 'slider', // 滑动条型 dataZoom
        xAxisIndex: 0,
        yAxisIndex: 0,
      },
    ],
    series: [
      {
        name: '频率',
        type: 'bar',
        data: bins.data.map((subArray) => subArray[1]), // 频率数据
        barGap: '0%', // 柱子之间无间隙
        barCategoryGap: '0%', // 类目之间无间隙
        itemStyle: {
          color: color, // 设置柱状图颜色
        },
      },
    ],
  }
}
onMounted(() => {
  echart_scatter_mounted()
})
</script>
 
<template>
  <v-row>
    <v-col cols="6">
      <Echarts
        id="echart_scatter"
        class="chart"
        :option="option_scatter"
        @click="scatterData_clicked"
      />
    </v-col>
    <v-col cols="6">
      <Echarts id="echart_histogram" class="chart" :option="option_histogram" />
      <DeepLearningBar />
    </v-col>
  </v-row>

  <br />
</template>
 


<style>
#echart_scatter {
  width: 600px;
  height: 600px;
}
#echart_histogram {
  width: 600px;
  height: 300px;
}
</style>
