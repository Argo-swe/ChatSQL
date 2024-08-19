import AppMenuItem from '../../../src/components/layout/AppMenuItem.vue';

describe('AppMenuItem', () => {
    it('renders correctly', () => {
      cy.mount(AppMenuItem);
  
      cy.get('li').should('be.visible');
    });
  });