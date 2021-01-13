import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'

import App from './App.vue'
import Homepage from './pages/Homepage.vue'
import Login from './pages/Login.vue'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.use(VueAxios, axios)
Vue.use(BootstrapVue)

const router = new VueRouter({
    routes: [
        {
            path: '/',
            name: 'login',
            component: Login
        },
        {
            path: '/devices',
            name: 'devices',
            component: Homepage,
            beforeEnter: (to, from, next) => {
                if (localStorage.getItem('session_token') === null){
                    next({ name: 'login' })
                }else{
                    next()
                }
            }
        }
    ]
})

new Vue({
    render: h => h(App),
    router
}).$mount('#app')