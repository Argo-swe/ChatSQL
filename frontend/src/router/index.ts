import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
import AuthService from '@/services/auth.service';

const router = createRouter({
    history: createWebHistory(),
    routes: [{
        path: '/',
        redirect: { path: "/chat" },
        component: AppLayout,
        children: [{
                path: '/chat',
                name: 'chat',
                component: () =>
                    import ('@/views/Chat.vue')
            },
            {
                path: '/dictionary',
                name: 'dictionary',
                component: () =>
                    import ('@/views/DictionariesList.vue')
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
            }
        ]
    }]
});

router.beforeEach(async (to, from) => {
    // make sure the user is authenticated and avoid an infinite redirect
    if (!AuthService.isLogged() && to.name !== 'chat') {
      // redirect the user to the chat page
      return { name: 'chat' }
    }
})

export default router;
