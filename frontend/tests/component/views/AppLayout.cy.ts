import { ref } from 'vue';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import DialogService from 'primevue/dialogservice';
import ToastService from 'primevue/toastservice';

import LoginDialog from '@/components/LoginDialog.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
import ConfigSidebar from '@/components/layout/ConfigSidebar.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';

import AppLayout from '@/views/AppLayout.vue';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

function mountAppLayout(props?) {
  return cy.mount(AppLayout, {
    global: {
      plugins: [i18n, PrimeVue, ConfirmationService, DialogService, ToastService, router],
      mocks: {
        t: (key) => key,
      },
      components: {
        LoginDialog,
        AppTopbar,
        ConfigSidebar,
        MenuSidebar
      },
      /* stubs: {
        AppMenu: true
      } */
    },
    props
  });
}

describe('AppLayout Component', () => {
  it('should render correctly', () => {
    mountAppLayout();
    cy.get('[data-testid="layout-wrapper"]').should('be.visible');
  });
});