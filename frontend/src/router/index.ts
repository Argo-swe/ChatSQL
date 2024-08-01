import AppLayout from '@/views/AppLayout.vue';
import AuthService from '@/services/auth.service';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: { path: '/chat' },
      component: AppLayout,
      children: [
        {
          path: '/chat',
          name: 'chat',
          component: () => import('@/views/ChatView.vue')
        },
        {
          path: '/dictionary',
          name: 'dictionary',
          component: () => import('@/views/DictionariesListView.vue')
        },
        {
          path: '/debug',
          name: 'debug',
          component: () => import('@/views/DebugView.vue')
        }
      ]
    }
  ]
});

router.beforeEach(async (to) => {
  // make sure the user is authenticated and avoid an infinite redirect
  if (!AuthService.isLogged() && to.name !== 'chat') {
    // redirect the user to the chat page
    return { name: 'chat' };
  }
});

export default router;
