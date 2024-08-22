import ConfirmationService from 'primevue/confirmationservice';
import { createI18n } from 'vue-i18n';
import AppLogo from '../../../src/components/AppLogo.vue';
import AppTopbar from '../../../src/components/layout/AppTopbar.vue';
import AuthService from '../../../src/services/auth.service';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

function mountAppTopbar(props?) {
  return cy.mount(AppTopbar, {
    global: {
      plugins: [i18n, ConfirmationService],
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

describe('AppTopbar Component', () => {
  it('should display correctly', () => {
    mountAppTopbar();
    cy.get('[data-testid="topbar"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_icona.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', '40');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 'auto');
    cy.get('[data-testid="option-menu"]').should('exist');
  });

  it('should render the login button if the user is not logged in', () => {
    cy.stub(AuthService, 'isLogged').returns(false);
    mountAppTopbar();
    cy.get('[data-testid="login-button"]').should('exist');
    cy.get('[data-testid="logout-button"]').should('not.exist');
  });

  it('should render the logout button if the user is logged in', () => {
    cy.stub(AuthService, 'isLogged').returns(true);
    mountAppTopbar();
    cy.get('[data-testid="logout-button"]').should('exist');
    cy.get('[data-testid="login-button"]').should('not.exist');
  });

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
