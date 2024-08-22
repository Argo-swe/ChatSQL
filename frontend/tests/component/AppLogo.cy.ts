import AppLogo from '../../src/components/AppLogo.vue';
import { useLayout } from '../../src/composables/layout';

let originalDarkThemeValue: boolean;

function mountAppLogo(props?) {
  return cy.mount(AppLogo, {
    props
  });
}

describe('AppLogo Component', () => {
  beforeEach(() => {
    const { layoutConfig } = useLayout();
    originalDarkThemeValue = layoutConfig.darkTheme.value;

    mountAppLogo({
      path: 'icons/argo_trasparente.svg',
      width: 150,
      height: 150
    });
  });

  afterEach(() => {
    const { layoutConfig } = useLayout();
    layoutConfig.darkTheme.value = originalDarkThemeValue;
  });

  it('should render correctly', () => {
    cy.get('[data-testid="logo-img"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_trasparente.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 150);
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', 150);
    cy.get('[data-testid="logo-img"]').should('not.have.class', 'logo-dark-theme-filter');
  });

  it('should render correctly with width and height unset', () => {
    mountAppLogo({
      path: 'icons/argo_trasparente.svg'
    });
    cy.get('[data-testid="logo-img"]').should('be.visible');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'src', 'icons/argo_trasparente.svg');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'width', 'auto');
    cy.get('[data-testid="logo-img"]').should('have.attr', 'height', 'auto');
  });

  it('should change color when the theme changes', () => {
    const { layoutConfig } = useLayout();
    layoutConfig.darkTheme.value = true;
    cy.get('[data-testid="logo-img"]').should('have.class', 'logo-dark-theme-filter');
  });
});
