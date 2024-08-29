// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands';

// Alternatively you can use CommonJS syntax:
// require('./commands')

declare global {
  namespace Cypress {
    interface Chainable {
      setupDictionary(): Chainable<void>;
      cleanupDictionary(): Chainable<void>;
      login(): Chainable<void>;
      logout(): Chainable<void>;
      handleSession(): Chainable<void>;
      selectDictionary(): Chainable<void>;
      decreaseScale(): Chainable<void>;
      increaseScale(): Chainable<void>;
      getDictionaryRow(): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', () => {
  cy.get('[data-testid="login-button"]').click();
  cy.get('[data-testid="input-username"]').type('admin');
  cy.get('[data-testid="input-password"]').type('admin');
  cy.get('[data-testid="login-submit-button"]').click();
});

Cypress.Commands.add('logout', () => {
  cy.get('[data-testid="logout-button"]').click();
  cy.get('[data-testid="confirm-dialog"]').find('[data-pc-name="acceptbutton"]').click();
});

Cypress.Commands.add('handleSession', () => {
  cy.session('login', () => {
    cy.visit('/');
    cy.login();
  });
});

Cypress.Commands.add('setupDictionary', () => {
  cy.login().then(() => {
    cy.visit('/dictionary');
    cy.get('[data-testid="dictionary-create-button"]').click();
    cy.get('[data-testid="dictionary-name-input"]').type('System Test Orders');
    cy.get('[data-testid="dictionary-description-input"]').type('System Test Orders dictionary');
    cy.get('[data-testid="dictionary-file-upload"]')
      .find('input[type="file"]')
      .selectFile('cypress/fixtures/orders.json', { force: true });

    cy.get('[data-testid="dictionary-submit-button"]').click();
    cy.logout();
  });
});

Cypress.Commands.add('getDictionaryRow', () => {
  cy.get('[data-testid="dictionaries-table"] tr').contains('System Test Orders').parents('tr');
});

Cypress.Commands.add('cleanupDictionary', () => {
  cy.visit('/dictionary');
  cy.getDictionaryRow().within(() => {
    cy.get('[data-testid="dictionary-delete-button"]').click();
  });
  cy.get('[data-testid="confirm-dialog"]').find('[data-pc-name="acceptbutton"]').click();
});

Cypress.Commands.add('selectDictionary', () => {
  cy.get('[data-testid="dictionary-dropdown"]').click();
  cy.get('ul > li').contains('System Test Orders').click();
});
