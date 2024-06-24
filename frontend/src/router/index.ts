import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [{
        path: '/',
        component: AppLayout,
        children: [{
                path: '/',
                name: 'chat',
                component: () =>
                    import ('@/views/Chat.vue')
            },
            {
                path: '/dizionari',
                name: 'dizionari',
                component: () =>
                    import ('@/views/Dizionari.vue')
            },
            {
                path: '/debug',
                name: 'debug',
                component: () =>
                    import ('@/views/Debug.vue')
            },
            {
                path: '/log',
                name: 'log',
                component: () =>
                    import ('@/views/Log.vue')
            },
            {
                path: '/addDizionario',
                name: 'addDizionario',
                component: () =>
                    import ('@/views/AddDizionario.vue')
            }
        ]
    }]
});

export default router;