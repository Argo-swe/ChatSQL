// Internal dependencies
import AppLogo from '@/components/AppLogo.vue';
import { useLayout } from '@/composables/layout';

const { layoutConfig } = useLayout();
let originalDarkThemeValue: boolean;

/**
 * Performs the mounting of the AppLogo component.
 * @param props - (Optional) Properties to pass to the component during mount.
 */
function mountAppLogo(props?) {
  return cy.mount(AppLogo, {
    props
  });
}

/**
 * Test suite for the AppLogo component.
 */
describe('AppLogo Component', () => {
  // Hook that runs before each test
  beforeEach(() => {
    originalDarkThemeValue = layoutConfig.darkTheme.value;
    layoutConfig.darkTheme.value = false;

    mountAppLogo({
      path: 'icons/argo_trasparente.svg',
      width: 150,
      height: 150
    });
  });

  // Hook that runs after each test
  afterEach(() => {
    layoutConfig.darkTheme.value = originalDarkThemeValue;
  });

  // Single and isolated test case
  it('should render correctly', () => {
    cy.get('[data-testid="logo-img"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_trasparente.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 150);
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', 150);
    cy.get('[data-testid="logo-img"]').should('not.have.class', 'logo-dark-theme-filter');
  });

  // Single and isolated test case
  it('should render correctly with width and height unset', () => {
    mountAppLogo({
      path: 'icons/argo_trasparente.svg'
    });
    cy.get('[data-testid="logo-img"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_trasparente.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 'auto');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', 'auto');
  });

  // Single and isolated test case
  it('should change the color of the logo when the theme changes', () => {
    layoutConfig.darkTheme.value = true;
    cy.get('[data-testid="logo-img"]').should('have.class', 'logo-dark-theme-filter');
  });
});
