import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';
import AppMenu from '../../../src/components/layout/AppMenu.vue';
import AppMenuItem from '../../../src/components/layout/AppMenuItem.vue';
import AuthService from '../../../src/services/auth.service';

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

describe('AppMenu Component', () => {
  it('should display user menu correctly', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    mountAppMenu();
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length.greaterThan', 0);
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-comments').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-database').should('not.exist');
  });

  it('should display technician menu correctly', () => {
    cy.stub(AuthService, 'isLogged').returns(true);
    mountAppMenu();
    cy.get('[data-testid="main-nav-menu"]').should('be.visible');
    cy.get('[data-testid="main-nav-menu"]').children().should('have.length.greaterThan', 1);
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-comments').should('exist');
    cy.get('[data-testid="main-nav-menu"]').children().find('.pi-database').should('exist');
  });
});
