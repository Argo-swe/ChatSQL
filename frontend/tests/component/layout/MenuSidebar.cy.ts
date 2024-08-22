import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';
import AppFooter from '../../../src/components/layout/AppFooter.vue';
import AppMenu from '../../../src/components/layout/AppMenu.vue';
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
      PgButton: Button,
      AppMenu,
      AppFooter
    },
    props
  });
}

describe('MenuSidebar Component', () => {
  it('should display correctly', () => {
    mountMenuSidebar();
    cy.get('[data-testid="menu-sidebar"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="footer"]').should('be.visible');
  });

  it('should toggle close button when viewport changes', () => {
    mountMenuSidebar();
    cy.viewport(992, 558);
    cy.get('#close-menu-sidebar').should('not.be.visible');
    cy.viewport('iphone-x');
    cy.get('#close-menu-sidebar').should('be.visible');
  });
});
