<template>
  <v-expand-transition>
    <div v-show="show" class="content">
      <slot>请等待...</slot>
      <span style="margin-left: 10px"></span>
      <v-progress-circular color="blue-lighten-3" indeterminate />
    </div>
  </v-expand-transition>
</template>

<script>
export default {
  props: {
    show: Boolean, // 【笔记】在props里声明的属性，不要在data()里再次声明，否则命名冲突
  },
}
</script>

<style scoped>
.content {
  font-size: large;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 100%;
}
.expand-enter-active,
.expand-leave-active {
  transition: height 0.3s ease;
}
.expand-enter, .expand-leave-to /* .expand-leave-active in <2.1.8 */ {
  height: 0;
}
</style>