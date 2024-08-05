import AuthService from '@/services/auth.service';
import AppLayout from '@/views/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

/**
 * Create a new instance of Vue Router with specific configuration
 */
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

/**
 * Redirect the user to the chat page if not authenticated.
 * Avoid an infinite redirect.
 */
router.beforeEach(async (to) => {
  if (!AuthService.isLogged() && to.name !== 'chat') {
    return { name: 'chat' };
  }
});

export default router;
