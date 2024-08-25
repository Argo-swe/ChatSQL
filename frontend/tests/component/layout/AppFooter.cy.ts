// External dependencies
import { createI18n } from 'vue-i18n';

// Internal dependencies
import AppFooter from '@/components/layout/AppFooter.vue';

// Mock VueI18n
const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  globalInjection: true,
  message: 'Mock translation'
});

/**
 * Performs the mounting of the AppFooter component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountAppFooter(props?) {
  return cy.mount(AppFooter, {
    global: {
      plugins: [i18n],
      mocks: {
        t: (key) => key,
        version: Cypress.env('VITE_VERSION')
      }
    },
    props
  });
}

/**
 * Test suite for the AppFooter component.
 */
describe('AppFooter Component', () => {
  // Single and isolated test case
  it('should display correctly', () => {
    mountAppFooter();
    cy.get('[data-testid="footer"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_trasparente.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', '40');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 'auto');
    cy.get('[data-testid="app-version"]').should('have.text', 'v' + Cypress.env('VITE_VERSION'));
  });
});
