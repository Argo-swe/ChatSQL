/**
 * Test suite for settings configuration requirements.
 */
describe('Chat - HomePage', () => {
  // Hook that runs before each tests
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-testid="open-settings-button"]').click();
  });

  // Test case
  it('verify that the user can decrease the scale', () => {
    cy.decreaseScale();
  });

  // Test case
  it('verify that the user can increase the scale', () => {
    cy.increaseScale();
  });

  // Test case
  it('verify that the user can change the theme', () => {
    cy.get('[data-testid=theme-input-switch]').find('input[type="checkbox"]').check();
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-theme-dark');
    cy.get('[data-testid=theme-input-switch]').find('input[type="checkbox"]').uncheck();
    cy.get('[data-testid="global-layout-wrapper"]').should('have.class', 'layout-theme-light');
  });

  // Test case
  it('verify that the user can change the language', () => {
    cy.get('[data-testid="request-input"]')
      .invoke('attr', 'placeholder')
      .should('equal', 'Inserisci una richiesta in linguaggio naturale');
    cy.get('[data-testid="global-language-dropdown"]').click();
    cy.get('li')
      .find('[data-testid="global-language-option"]')
      .contains('inglese')
      .click({ force: true });
    cy.get('body').click(0, 0);
    cy.get('[data-testid="request-input"]')
      .invoke('attr', 'placeholder')
      .should('equal', 'Enter a natural language request');
  });
});
