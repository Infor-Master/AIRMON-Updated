import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueAxios from 'vue-axios'
import VueFusionCharts from 'vue-fusioncharts'
import FusionCharts from 'fusioncharts';
import Column2D from 'fusioncharts/fusioncharts.charts';
import FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import TimeSeries from 'fusioncharts/fusioncharts.timeseries';

import App from './App.vue'
import Device from './pages/Device.vue'
import Homepage from './pages/Homepage.vue'
import Login from './pages/Login.vue'

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.use(BootstrapVue);
Vue.use(VueFusionCharts, FusionCharts, TimeSeries, Column2D, FusionTheme);

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
        },
        {
            path: '/devices/:id',
            name: 'device',
            component: Device,
        },
        {
            path: '/logout',
            name: 'logout',
            beforeEnter: (to, from, next) => {
                sessionStorage.removeItem('session_token')
                next({ name: 'login' })
            }
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.name !== 'login' && sessionStorage.getItem('session_token') === null) next({ name: 'login' })
    else next()
})

new Vue({
    render: h => h(App),
    router
}).$mount('#app')