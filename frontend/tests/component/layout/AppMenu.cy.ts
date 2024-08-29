// External dependencies
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

// Internal dependencies
import AppMenu from '@/components/layout/AppMenu.vue';
import AppMenuItem from '@/components/layout/AppMenuItem.vue';
import AuthService from '@/services/auth.service';

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
 * Performs the mounting of the AppMenu component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountAppMenu(props?) {
  return cy.mount(AppMenu, {
    global: {
      plugins: [i18n, router],
      mocks: {
        t: (key) => key
      },
      components: {
        AppMenuItem
      }
    },
    props
  });
}

/**
 * Test suite for the AppMenu component.
 */
describe('AppMenu Component', () => {
  // Single and isolated test case
  it('should display user menu correctly', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    mountAppMenu();
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length.greaterThan', 0);
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-comments').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-database').should('not.exist');
  });

  // Single and isolated test case
  it('should display technician menu correctly', () => {
    cy.stub(AuthService, 'isLogged').returns(true);
    mountAppMenu();
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length.greaterThan', 1);
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-comments').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-database').should('exist');
  });
});
