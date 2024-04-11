import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PerceptionTest from "@/components/PerceptionTest.vue";
import TestForm from "@/components/TestForm.vue";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/perceptiontest',
            name: 'perceptiontest',
            component: PerceptionTest,
        },
    ]
})

export default router
