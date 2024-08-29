// External dependencies
import ConfirmationService from 'primevue/confirmationservice';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';

// Internal dependencies
import AppLogo from '@/components/AppLogo.vue';
import AppTopbar from '@/components/layout/AppTopbar.vue';
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
 * Performs the mounting of the AppTopbar component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountAppTopbar(props?) {
  return cy.mount(AppTopbar, {
    global: {
      plugins: [i18n, router, ConfirmationService],
      mocks: {
        t: (key) => key
      },
      components: {
        AppLogo
      }
    },
    props
  });
}

/**
 * Test suite for the AppTopbar component.
 */
describe('AppTopbar Component', () => {
  // Single and isolated test case
  it('should display correctly', () => {
    mountAppTopbar();
    cy.get('[data-testid="topbar"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_icona.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', '40');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 'auto');
    cy.get('[data-testid="option-menu"]').should('exist');
  });

  // Single and isolated test case
  it('should render the login button if the user is not logged in', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    mountAppTopbar();
    cy.get('[data-testid="login-button"]').should('exist');
    cy.get('[data-testid="logout-button"]').should('not.exist');
  });

  // Single and isolated test case
  it('should perform the logout action if the user is logged in and clicks the logout button', () => {
    cy.stub(AuthService, 'isLogged').returns(true);
    cy.spy(AuthService, 'logout').as('logoutSpy');
    mountAppTopbar().then(({ component }) => {
      cy.stub(component.confirm, 'require').callsFake((options) => {
        options.accept();
      });
    });
    cy.get('[data-testid="login-button"]').should('not.exist');
    cy.get('[data-testid="logout-button"]').should('exist').click();
    cy.get('@logoutSpy').should('have.been.called');
  });

  // Single and isolated test case
  it('should toggle option-menu class on click event', () => {
    mountAppTopbar();
    cy.get('[data-testid="option-menu"]').should(
      'not.have.class',
      'layout-topbar-menu-mobile-active'
    );
    cy.get('[data-testid="open-option-menu-button"]').should('exist').click();
    cy.get('[data-testid="option-menu"]').should('have.class', 'layout-topbar-menu-mobile-active');

    // Simulates a click in the upper left corner
    cy.get('body').click(0, 0);
    cy.get('[data-testid="option-menu"]').should(
      'not.have.class',
      'layout-topbar-menu-mobile-active'
    );
  });
});
