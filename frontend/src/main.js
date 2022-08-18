import { createApp } from 'vue'
import moment from 'moment'
import VueCryptojs from 'vue-cryptojs'
import App from './App.vue'
import router from './router'
import { createVuestic } from 'vuestic-ui'
import VueNumber from 'vue-number-animation'
var app = createApp(App)
app.config.globalProperties.$moment = moment
app.use(router)
app.use(VueCryptojs)
app.use(VueNumber)
app.use(createVuestic())
app.mount('#app')