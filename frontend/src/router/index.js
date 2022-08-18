import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [{
    path: '/',
    name: 'Home',
    meta: { title: 'Eagle 猜歌遊戲 - 首頁' },
    component: () =>
        import ('../views/Home.vue')
}, {
    path: '/room/:room_id',
    name: 'Room',
    meta: { title: `Eagle 猜歌遊戲 - 載入中` },
    component: () =>
        import ('../views/Room.vue')
}, ]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})
router.beforeEach((to, from, next) => {
    window.document.title = to.meta.title;
    next()
})
export default router