import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';
import MenuSidebar from '../../../src/components/layout/MenuSidebar.vue';

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

function mountMenuSidebar(props?) {
  return cy.mount(MenuSidebar, {
    global: {
      plugins: [i18n, router, PrimeVue],
      mocks: {
        t: (key) => key
      }
    },
    components: {
      PgButton: Button
    },
    props
  });
}

describe('MenuSidebar Component', () => {
  it('should display correctly', () => {
    mountMenuSidebar();

    cy.get('[data-test-id="menu-sidebar"]').should('be.visible');
  });

  it('should show button when viewport is small', () => {
    mountMenuSidebar();

    // cy.get('[data-test-id="menu-sidebar"]').should('be.visible');
    cy.viewport('iphone-x');
    cy.get('#close-menu-sidebar').should('not.be.visible');
    // cy.get('#close-menu-sidebar').click();
  });
});
