import AppLogo from '../../src/components/AppLogo.vue';

describe('AppLogo', () => {
  it('renders correctly', () => {
    cy.mount(AppLogo, {
      propsData: {
        path: 'icons/argo_trasparente.svg'
      }
    });

    // Assert that the component renders correctly
    cy.get('img').should('be.visible');
    cy.get('img').should('have.attr', 'src', 'icons/argo_trasparente.svg');
  });
});
