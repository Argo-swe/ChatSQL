// External dependencies
import Button from 'primevue/button';
import PrimeVue from 'primevue/config';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

// Internal dependencies
import AppFooter from '@/components/layout/AppFooter.vue';
import AppMenu from '@/components/layout/AppMenu.vue';
import MenuSidebar from '@/components/layout/MenuSidebar.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

// Mock VueRouter
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
});

/**
 * Performs the mounting of the MenuSidebar component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
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

/**
 * Test suite for the MenuSidebar component.
 */
describe('MenuSidebar Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    mountMenuSidebar();
  });

  // Single and isolated test case
  it('should display correctly', () => {
    cy.get('[data-testid="menu-sidebar"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="footer"]').should('be.visible');
  });

  // Single and isolated test case
  it('should toggle close button when viewport changes', () => {
    cy.viewport(992, 558);
    cy.get('#close-menu-sidebar').should('not.be.visible');
    cy.viewport('iphone-x');
    cy.get('#close-menu-sidebar').should('be.visible');
  });
});
