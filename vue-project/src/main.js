import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
    components,
    directives,
    })
const SERVER_PORT = 'http://127.0.0.1:5000' // 服务器的IP地址和端口号，`http://`记得加！不然会被post方法认成相对路径

const app = createApp(App).use(vuetify)
app.config.globalProperties.$serverPort = SERVER_PORT // 设置“服务器的IP地址和端口号”为全局变量


app.use(router)

app.mount('#app')
